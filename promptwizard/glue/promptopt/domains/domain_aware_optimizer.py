# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Domain-aware prompt optimizer that integrates domain knowledge
into the prompt optimization process.
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from .base_domain import (
    DomainConfig,
    DomainEvaluator,
    DomainCritiqueGenerator,
    DomainRegistry
)


class DomainAwarePromptOptimizer:
    """
    Extends the base prompt optimization with domain-specific knowledge.
    Integrates tacit knowledge, domain-specific evaluation, and critique.
    """

    def __init__(
        self,
        domain_config: DomainConfig,
        llm_client: Any = None,
        evaluator: DomainEvaluator = None,
        logger: Any = None
    ):
        """
        Initialize domain-aware optimizer.

        Args:
            domain_config: Domain configuration with tacit knowledge
            llm_client: LLM client for generating responses
            evaluator: Custom domain evaluator (optional)
            logger: Logger instance
        """
        self.domain_config = domain_config
        self.llm_client = llm_client
        self.logger = logger

        # Initialize evaluator
        if evaluator:
            self.evaluator = evaluator
        else:
            # Try to get registered evaluator for this domain
            evaluator_class = DomainRegistry.get_evaluator(domain_config.domain_type)
            if evaluator_class:
                self.evaluator = evaluator_class(domain_config, llm_client)
            else:
                self.evaluator = None

        # Initialize critique generator
        self.critique_generator = DomainCritiqueGenerator(domain_config, llm_client)

    def enhance_base_instruction(self, base_instruction: str) -> str:
        """
        Enhance base instruction with domain knowledge.

        Args:
            base_instruction: Original base instruction

        Returns:
            Enhanced instruction with domain context
        """
        knowledge = self.domain_config.knowledge

        # Build domain context
        domain_context_parts = []

        # Add domain identification
        domain_context_parts.append(
            f"당신은 {self.domain_config.domain_name} 분야의 전문가입니다."
        )

        # Add key principles
        if knowledge.principles:
            principles_text = "\n".join(f"- {p}" for p in knowledge.principles[:3])
            domain_context_parts.append(f"\n핵심 원칙:\n{principles_text}")

        # Add constraints
        if knowledge.constraints:
            constraints_text = "\n".join(f"- {c}" for c in knowledge.constraints[:3])
            domain_context_parts.append(f"\n준수사항:\n{constraints_text}")

        domain_context = "\n".join(domain_context_parts)

        # Combine with base instruction
        enhanced = f"{domain_context}\n\n{base_instruction}"

        return enhanced

    def generate_domain_thinking_styles(self) -> List[str]:
        """
        Get domain-specific thinking styles for mutation.

        Returns:
            List of domain thinking styles
        """
        return self.domain_config.knowledge.thinking_styles

    def get_domain_expert_prompt(self) -> str:
        """
        Generate expert persona prompt for the domain.

        Returns:
            Expert persona description
        """
        personas = self.domain_config.knowledge.expert_personas
        if not personas:
            return f"당신은 {self.domain_config.domain_name} 분야의 전문가입니다."

        # Use primary persona
        primary = personas[0]
        expert_prompt = f"""당신은 {primary.role}입니다.
전문 분야: {primary.focus}
배경: {primary.background}
접근 방식: {primary.thinking_approach}"""

        return expert_prompt

    def evaluate_response(
        self,
        response: str,
        ground_truth: str = "",
        question: str = ""
    ) -> Dict[str, float]:
        """
        Evaluate response using domain-specific criteria.

        Args:
            response: Generated response to evaluate
            ground_truth: Expected answer (if available)
            question: Original question

        Returns:
            Dictionary of evaluation scores
        """
        if self.evaluator:
            return self.evaluator.evaluate(response, ground_truth, question)

        # Default evaluation if no custom evaluator
        return self._default_evaluate(response, ground_truth)

    def _default_evaluate(
        self,
        response: str,
        ground_truth: str
    ) -> Dict[str, float]:
        """Default evaluation without custom evaluator."""
        scores = {}

        # Basic accuracy
        if ground_truth:
            response_lower = response.lower()
            truth_lower = ground_truth.lower()
            overlap = len(set(response_lower.split()) & set(truth_lower.split()))
            total = len(set(truth_lower.split()))
            scores['accuracy'] = overlap / total if total > 0 else 0.5

        # Constraint compliance (simple check)
        scores['constraint_compliance'] = self._check_basic_constraints(response)

        # Calculate overall
        if scores:
            scores['overall'] = sum(scores.values()) / len(scores)
        else:
            scores['overall'] = 0.5

        return scores

    def _check_basic_constraints(self, response: str) -> float:
        """Basic constraint checking."""
        constraints = self.domain_config.knowledge.constraints
        if not constraints:
            return 1.0

        response_lower = response.lower()
        violations = 0

        for constraint in constraints:
            # Simple keyword-based violation check
            if "금지" in constraint:
                # Extract what's forbidden
                forbidden_terms = self._extract_terms(constraint)
                for term in forbidden_terms:
                    if term.lower() in response_lower:
                        violations += 1
                        break

        return max(0.0, 1.0 - (violations / len(constraints)))

    def _extract_terms(self, text: str) -> List[str]:
        """Extract key terms from text."""
        # Simple extraction - override for better logic
        words = text.split()
        return [w for w in words if len(w) > 2]

    def generate_domain_critique(
        self,
        instruction: str,
        examples: str,
        scores: Dict[str, float] = None
    ) -> str:
        """
        Generate domain-aware critique prompt.

        Args:
            instruction: Current instruction being evaluated
            examples: Example responses
            scores: Evaluation scores (optional)

        Returns:
            Formatted critique prompt
        """
        return self.critique_generator.generate_critique_prompt(
            instruction, examples, scores
        )

    def generate_domain_refinement(
        self,
        instruction: str,
        examples: str,
        critique: str
    ) -> str:
        """
        Generate domain-aware refinement prompt.

        Args:
            instruction: Current instruction
            examples: Example responses
            critique: Generated critique

        Returns:
            Formatted refinement prompt
        """
        return self.critique_generator.generate_refinement_prompt(
            instruction, examples, critique
        )

    def get_critical_test_cases(self) -> List[Dict[str, Any]]:
        """
        Get critical test cases from domain case library.

        Returns:
            List of critical test cases
        """
        cases = []
        for case in self.domain_config.case_library.critical_cases:
            cases.append({
                "question": case.question,
                "expected_elements": case.expected_elements,
                "forbidden_elements": case.forbidden_elements,
                "category": case.category,
                "difficulty": case.difficulty
            })
        return cases

    def validate_against_cases(
        self,
        prompt: str,
        generate_response_fn: callable
    ) -> Tuple[float, List[Dict]]:
        """
        Validate prompt against domain case library.

        Args:
            prompt: Prompt to validate
            generate_response_fn: Function to generate response from prompt

        Returns:
            Tuple of (overall score, list of case results)
        """
        all_cases = self.domain_config.case_library.get_all_cases()
        if not all_cases:
            return 1.0, []

        results = []
        total_score = 0.0

        for case in all_cases:
            # Generate response for this case
            try:
                response = generate_response_fn(prompt, case.question)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to generate response for case: {e}")
                response = ""

            # Evaluate response
            case_score = self._evaluate_case_response(response, case)
            total_score += case_score

            results.append({
                "question": case.question,
                "category": case.category,
                "score": case_score,
                "response": response[:200] + "..." if len(response) > 200 else response
            })

        overall_score = total_score / len(all_cases) if all_cases else 1.0
        return overall_score, results

    def _evaluate_case_response(self, response: str, case) -> float:
        """Evaluate response against a single case."""
        if not response:
            return 0.0

        response_lower = response.lower()

        # Check expected elements
        expected_found = sum(
            1 for elem in case.expected_elements
            if elem.lower() in response_lower
        )
        expected_score = expected_found / len(case.expected_elements) if case.expected_elements else 1.0

        # Check forbidden elements
        forbidden_found = sum(
            1 for elem in case.forbidden_elements
            if elem.lower() in response_lower
        )
        forbidden_penalty = forbidden_found * 0.25  # 25% penalty per forbidden element

        return max(0.0, expected_score - forbidden_penalty)

    def get_domain_summary(self) -> Dict[str, Any]:
        """
        Get summary of domain configuration.

        Returns:
            Dictionary with domain summary
        """
        knowledge = self.domain_config.knowledge

        return {
            "domain_type": self.domain_config.domain_type,
            "domain_name": self.domain_config.domain_name,
            "description": self.domain_config.description,
            "num_principles": len(knowledge.principles),
            "num_constraints": len(knowledge.constraints),
            "num_quality_criteria": len(knowledge.quality_criteria),
            "num_thinking_styles": len(knowledge.thinking_styles),
            "num_expert_personas": len(knowledge.expert_personas),
            "num_critical_cases": len(self.domain_config.case_library.critical_cases),
            "num_edge_cases": len(self.domain_config.case_library.edge_cases),
            "has_custom_critique_template": bool(self.domain_config.critique_template),
            "has_custom_refinement_template": bool(self.domain_config.refinement_template)
        }


def create_domain_optimizer(
    domain_type: str,
    llm_client: Any = None,
    custom_config: DomainConfig = None,
    logger: Any = None
) -> DomainAwarePromptOptimizer:
    """
    Factory function to create domain-aware optimizer.

    Args:
        domain_type: Type of domain ('medical', 'legal', 'finance', etc.)
        llm_client: LLM client for generating responses
        custom_config: Custom domain config (overrides default)
        logger: Logger instance

    Returns:
        Configured DomainAwarePromptOptimizer
    """
    if custom_config:
        config = custom_config
    else:
        # Try to get from registry
        config = DomainRegistry.get_domain(domain_type)

        if not config:
            # Load default configs
            if domain_type == "medical":
                from .medical import MEDICAL_DOMAIN_CONFIG
                config = MEDICAL_DOMAIN_CONFIG
            elif domain_type == "legal":
                from .legal import LEGAL_DOMAIN_CONFIG
                config = LEGAL_DOMAIN_CONFIG
            elif domain_type == "finance":
                from .finance import FINANCE_DOMAIN_CONFIG
                config = FINANCE_DOMAIN_CONFIG
            else:
                raise ValueError(f"Unknown domain type: {domain_type}")

    # Get custom evaluator if available
    evaluator = None
    if domain_type == "medical":
        from .medical import MedicalDomainEvaluator
        evaluator = MedicalDomainEvaluator(config, llm_client)

    return DomainAwarePromptOptimizer(
        domain_config=config,
        llm_client=llm_client,
        evaluator=evaluator,
        logger=logger
    )
