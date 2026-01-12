# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Domain-enhanced critique and refine technique.
Extends the base CritiqueNRefine with domain-specific knowledge integration.
"""

import random
import re
from typing import Any, Dict, List, Optional

from .core_logic import CritiqueNRefine
from .base_classes import CritiqueNRefinePromptPool
from ...domains import DomainConfig, DomainRegistry
from ...domains.domain_aware_optimizer import DomainAwarePromptOptimizer, create_domain_optimizer
from ...constants import PromptOptimizationParams
from ..common_logic import DatasetSpecificProcessing
from ....common.base_classes import SetupConfig


class DomainEnhancedCritiqueNRefine(CritiqueNRefine):
    """
    Domain-enhanced version of CritiqueNRefine.
    Integrates domain-specific tacit knowledge into prompt optimization.
    """

    def __init__(
        self,
        dataset: List,
        base_path: str,
        setup_config: SetupConfig,
        prompt_pool: CritiqueNRefinePromptPool,
        data_processor: DatasetSpecificProcessing,
        logger,
        domain_config: DomainConfig = None,
        domain_type: str = None
    ):
        """
        Initialize domain-enhanced optimizer.

        Args:
            dataset: Training dataset
            base_path: Base path for logging
            setup_config: Setup configuration
            prompt_pool: Prompt pool with templates
            data_processor: Dataset-specific processor
            logger: Logger instance
            domain_config: Optional domain configuration
            domain_type: Domain type string (if domain_config not provided)
        """
        super().__init__(
            dataset=dataset,
            base_path=base_path,
            setup_config=setup_config,
            prompt_pool=prompt_pool,
            data_processor=data_processor,
            logger=logger
        )

        # Initialize domain optimizer
        self.domain_optimizer = None
        self.domain_config = domain_config

        if domain_config:
            self.domain_optimizer = DomainAwarePromptOptimizer(
                domain_config=domain_config,
                logger=logger
            )
        elif domain_type:
            try:
                self.domain_optimizer = create_domain_optimizer(
                    domain_type=domain_type,
                    logger=logger
                )
                self.domain_config = self.domain_optimizer.domain_config
            except ValueError as e:
                logger.warning(f"Could not load domain config: {e}")

    def gen_different_styles(
        self,
        base_instruction: str,
        task_description: str,
        mutation_rounds: int = 2,
        thinking_styles_count: int = 10
    ) -> List:
        """
        Generate different variations using domain-specific thinking styles.

        Overrides base method to incorporate domain thinking styles.
        """
        # Enhance base instruction with domain knowledge
        if self.domain_optimizer:
            enhanced_instruction = self.domain_optimizer.enhance_base_instruction(
                base_instruction
            )
        else:
            enhanced_instruction = base_instruction

        # Get domain-specific thinking styles if available
        domain_thinking_styles = []
        if self.domain_optimizer:
            domain_thinking_styles = self.domain_optimizer.generate_domain_thinking_styles()

        # Combine with general thinking styles
        if domain_thinking_styles:
            combined_styles = domain_thinking_styles + self.prompt_pool.thinking_styles[:thinking_styles_count - len(domain_thinking_styles)]
        else:
            combined_styles = self.prompt_pool.thinking_styles[:thinking_styles_count]

        candidate_prompts = [task_description + "\n" + enhanced_instruction]

        for mutation_round in range(mutation_rounds):
            mutated_sample_prompt = self.prompt_pool.meta_sample_template.format(
                task_description=task_description,
                meta_prompts="\n".join(combined_styles),
                num_variations=len(combined_styles),
                prompt_instruction=enhanced_instruction
            )
            generated_mutated_prompt = self.chat_completion(mutated_sample_prompt)

            matches = re.findall(
                DatasetSpecificProcessing.TEXT_DELIMITER_PATTERN_MUTATION,
                generated_mutated_prompt
            )
            candidate_prompts.extend(matches)

            self.logger.info(
                f"mutation_round={mutation_round} "
                f"mutated_sample_prompt={mutated_sample_prompt}"
                f"mutated_prompt_generation={generated_mutated_prompt}"
            )

        return candidate_prompts

    def critique_and_refine(
        self,
        prompt: str,
        critique_example_set: List,
        further_enhance: bool = False
    ) -> str:
        """
        Domain-aware critique and refinement.

        Overrides base method to use domain-specific critique templates.
        """
        example_string = self.data_processor.collate_to_str(
            critique_example_set,
            self.prompt_pool.quest_reason_ans
        )

        # Use domain-specific critique if available
        if self.domain_optimizer:
            # Get evaluation scores for context
            scores = None
            if critique_example_set:
                # Sample evaluation
                sample_response = critique_example_set[0].get(
                    DatasetSpecificProcessing.ANSWER_WITH_REASON_LITERAL, ""
                )
                if sample_response:
                    scores = self.domain_optimizer.evaluate_response(sample_response)

            # Generate domain-aware critique prompt
            meta_critique_prompt = self.domain_optimizer.generate_domain_critique(
                instruction=prompt,
                examples=example_string,
                scores=scores
            )
        else:
            # Fall back to base implementation
            if further_enhance:
                meta_critique_prompt = self.prompt_pool.meta_positive_critique_template
            else:
                meta_critique_prompt = self.prompt_pool.meta_critique_template

            meta_critique_prompt = meta_critique_prompt.format(
                instruction=prompt,
                examples=example_string
            )

        # Get expert profile
        if self.domain_optimizer:
            expert_profile = self.domain_optimizer.get_domain_expert_prompt()
        else:
            expert_profile = self.prompt_pool.expert_profile

        critique_text = self.chat_completion(meta_critique_prompt, expert_profile)

        # Generate refinement
        if self.domain_optimizer:
            critique_refine_prompt = self.domain_optimizer.generate_domain_refinement(
                instruction=prompt,
                examples=example_string,
                critique=critique_text
            )
        else:
            critique_refine_prompt = self.prompt_pool.critique_refine_template.format(
                instruction=prompt,
                examples=example_string,
                critique=critique_text,
                steps_per_sample=1
            )

        refined_prompts = self.chat_completion(critique_refine_prompt, expert_profile)

        # Extract refined prompt
        refined_prompts = re.findall(
            DatasetSpecificProcessing.TEXT_DELIMITER_PATTERN,
            refined_prompts
        )

        if refined_prompts:
            final_refined_prompts = refined_prompts[0]
        else:
            # Try domain-specific pattern
            domain_pattern = r'<IMPROVED_PROMPT>(.*?)</IMPROVED_PROMPT>'
            matches = re.findall(domain_pattern, refined_prompts if isinstance(refined_prompts, str) else str(refined_prompts), re.DOTALL)
            if matches:
                final_refined_prompts = matches[0].strip()
            else:
                raise ValueError("The LLM output is not in the expected format. Please rerun the code...")

        self.logger.info(
            f"Prompt to get critique:\n {meta_critique_prompt}"
            f"critique received from LLM:\n {critique_text}"
            f"Prompt to get Refinement after critique, from LLM:\n {critique_refine_prompt}"
            f"Refined prompts received from LLM:\n {final_refined_prompts}"
        )

        return final_refined_prompts

    def evaluate(self, generated_text: str, dataset_subset: List) -> List:
        """
        Domain-aware evaluation.

        Extends base evaluation with domain-specific criteria.
        """
        # First, get base evaluation results
        wrong_examples = super().evaluate(generated_text, dataset_subset)

        # If domain optimizer available, add domain-specific evaluation
        if self.domain_optimizer and dataset_subset:
            for i, example in enumerate(dataset_subset):
                if example in wrong_examples:
                    continue  # Already marked as wrong

                question = example.get(DatasetSpecificProcessing.QUESTION_LITERAL, "")

                # Domain evaluation
                scores = self.domain_optimizer.evaluate_response(
                    response=generated_text,
                    question=question
                )

                # Check if domain evaluation flags issues
                if scores.get('constraint_compliance', 1.0) < 0.5:
                    # Domain constraint violation
                    if example not in wrong_examples:
                        wrong_examples.append(example)
                        self.logger.info(
                            f"Domain evaluation flagged example due to constraint violation: "
                            f"score={scores.get('constraint_compliance')}"
                        )

        return wrong_examples

    def generate_expert_identity(self, task_description: str) -> str:
        """
        Generate domain-aware expert identity.

        Overrides base method to use domain expert personas.
        """
        if self.domain_optimizer:
            return self.domain_optimizer.get_domain_expert_prompt()

        # Fall back to base implementation
        return super().generate_expert_identity(task_description)

    def get_best_prompt(
        self,
        params: PromptOptimizationParams,
        use_examples: bool = False,
        run_without_train_examples: bool = False,
        generate_synthetic_examples: bool = False
    ) -> tuple:
        """
        Get best prompt with domain validation.

        Extends base method to validate against domain case library.
        """
        # Get best prompt from base implementation
        best_prompt, expert_identity = super().get_best_prompt(
            params=params,
            use_examples=use_examples,
            run_without_train_examples=run_without_train_examples,
            generate_synthetic_examples=generate_synthetic_examples
        )

        # Validate against domain cases if available
        if self.domain_optimizer and best_prompt:
            self._log_domain_validation(best_prompt)

        return best_prompt, expert_identity

    def _log_domain_validation(self, prompt: str) -> None:
        """Log domain validation results."""
        if not self.domain_optimizer:
            return

        critical_cases = self.domain_optimizer.get_critical_test_cases()
        if not critical_cases:
            return

        self.logger.info(
            f"Domain validation: {len(critical_cases)} critical cases available for testing"
        )
        self.logger.info(
            f"Domain summary: {self.domain_optimizer.get_domain_summary()}"
        )

    def get_domain_enhanced_final_prompt(
        self,
        base_prompt: str,
        params: PromptOptimizationParams
    ) -> str:
        """
        Enhance final prompt with domain-specific elements.

        Args:
            base_prompt: Base optimized prompt
            params: Optimization parameters

        Returns:
            Domain-enhanced final prompt
        """
        if not self.domain_optimizer:
            return base_prompt

        knowledge = self.domain_config.knowledge

        # Add domain-specific sections
        enhanced_parts = [base_prompt]

        # Add key constraints as reminders
        if knowledge.constraints:
            constraints_section = "\n\n## 중요 준수사항:\n"
            constraints_section += "\n".join(f"- {c}" for c in knowledge.constraints[:3])
            enhanced_parts.append(constraints_section)

        # Add quality criteria hints
        if knowledge.quality_criteria:
            quality_section = "\n\n## 응답 품질 기준:\n"
            for qc in knowledge.quality_criteria[:3]:
                quality_section += f"- {qc.name}: {qc.description}\n"
            enhanced_parts.append(quality_section)

        return "".join(enhanced_parts)


def create_domain_enhanced_optimizer(
    domain_type: str,
    dataset: List,
    base_path: str,
    setup_config: SetupConfig,
    prompt_pool: CritiqueNRefinePromptPool,
    data_processor: DatasetSpecificProcessing,
    logger,
    custom_domain_config: DomainConfig = None
) -> DomainEnhancedCritiqueNRefine:
    """
    Factory function to create domain-enhanced optimizer.

    Args:
        domain_type: Type of domain ('medical', 'legal', 'finance')
        dataset: Training dataset
        base_path: Base path for logging
        setup_config: Setup configuration
        prompt_pool: Prompt pool with templates
        data_processor: Dataset-specific processor
        logger: Logger instance
        custom_domain_config: Optional custom domain config

    Returns:
        Configured DomainEnhancedCritiqueNRefine instance
    """
    return DomainEnhancedCritiqueNRefine(
        dataset=dataset,
        base_path=base_path,
        setup_config=setup_config,
        prompt_pool=prompt_pool,
        data_processor=data_processor,
        logger=logger,
        domain_config=custom_domain_config,
        domain_type=domain_type
    )
