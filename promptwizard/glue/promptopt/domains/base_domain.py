# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Base classes for domain-specific prompt optimization.
Provides infrastructure for integrating tacit knowledge into prompt optimization.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod
import yaml
import os


@dataclass
class QualityCriterion:
    """Single quality criterion for domain evaluation."""
    name: str
    weight: float
    description: str = ""
    evaluation_prompt: str = ""


@dataclass
class ExpertPersona:
    """Domain expert persona definition."""
    role: str
    focus: str
    background: str = ""
    thinking_approach: str = ""


@dataclass
class DomainKnowledge:
    """
    Container for domain-specific tacit knowledge.
    Captures principles, constraints, and quality criteria that experts use implicitly.
    """
    # Core principles that guide domain decisions
    principles: List[str] = field(default_factory=list)

    # Hard constraints that must never be violated
    constraints: List[str] = field(default_factory=list)

    # Quality criteria with weights for evaluation
    quality_criteria: List[QualityCriterion] = field(default_factory=list)

    # Domain-specific thinking styles
    thinking_styles: List[str] = field(default_factory=list)

    # Expert personas for the domain
    expert_personas: List[ExpertPersona] = field(default_factory=list)

    # Domain-specific terminology and definitions
    terminology: Dict[str, str] = field(default_factory=dict)

    # Common patterns and anti-patterns
    patterns: List[str] = field(default_factory=list)
    anti_patterns: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomainKnowledge":
        """Create DomainKnowledge from dictionary."""
        quality_criteria = []
        for qc in data.get("quality_criteria", []):
            if isinstance(qc, dict):
                quality_criteria.append(QualityCriterion(**qc))

        expert_personas = []
        for ep in data.get("expert_personas", []):
            if isinstance(ep, dict):
                expert_personas.append(ExpertPersona(**ep))

        return cls(
            principles=data.get("principles", []),
            constraints=data.get("constraints", []),
            quality_criteria=quality_criteria,
            thinking_styles=data.get("thinking_styles", []),
            expert_personas=expert_personas,
            terminology=data.get("terminology", {}),
            patterns=data.get("patterns", []),
            anti_patterns=data.get("anti_patterns", [])
        )


@dataclass
class CaseExample:
    """Single test case for domain evaluation."""
    question: str
    expected_elements: List[str] = field(default_factory=list)
    forbidden_elements: List[str] = field(default_factory=list)
    category: str = ""
    difficulty: str = "medium"
    explanation: str = ""


@dataclass
class CaseLibrary:
    """Collection of domain-specific test cases."""
    critical_cases: List[CaseExample] = field(default_factory=list)
    edge_cases: List[CaseExample] = field(default_factory=list)
    common_cases: List[CaseExample] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CaseLibrary":
        """Create CaseLibrary from dictionary."""
        def parse_cases(cases_data: List[Dict]) -> List[CaseExample]:
            result = []
            for category_data in cases_data:
                category = category_data.get("category", "")
                for case in category_data.get("cases", []):
                    if isinstance(case, dict):
                        case["category"] = category
                        result.append(CaseExample(**case))
            return result

        return cls(
            critical_cases=parse_cases(data.get("critical_cases", [])),
            edge_cases=parse_cases(data.get("edge_cases", [])),
            common_cases=parse_cases(data.get("common_cases", []))
        )

    def get_all_cases(self) -> List[CaseExample]:
        """Get all cases combined."""
        return self.critical_cases + self.edge_cases + self.common_cases

    def get_cases_by_category(self, category: str) -> List[CaseExample]:
        """Get cases filtered by category."""
        all_cases = self.get_all_cases()
        return [c for c in all_cases if c.category == category]


@dataclass
class DomainConfig:
    """
    Complete domain configuration for prompt optimization.
    Combines domain knowledge, critique templates, and case library.
    """
    domain_type: str
    domain_name: str
    description: str = ""

    # Domain knowledge (tacit knowledge)
    knowledge: DomainKnowledge = field(default_factory=DomainKnowledge)

    # Domain-specific critique template
    critique_template: str = ""

    # Domain-specific refinement template
    refinement_template: str = ""

    # Case library for testing
    case_library: CaseLibrary = field(default_factory=CaseLibrary)

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "DomainConfig":
        """Load domain configuration from YAML file."""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomainConfig":
        """Create DomainConfig from dictionary."""
        knowledge_data = data.get("tacit_knowledge", data.get("knowledge", {}))
        knowledge = DomainKnowledge.from_dict(knowledge_data)

        case_library_data = data.get("case_library", {})
        case_library = CaseLibrary.from_dict(case_library_data)

        return cls(
            domain_type=data.get("domain_type", "general"),
            domain_name=data.get("domain_name", data.get("domain_type", "general")),
            description=data.get("description", ""),
            knowledge=knowledge,
            critique_template=data.get("critique_template", ""),
            refinement_template=data.get("refinement_template", ""),
            case_library=case_library,
            metadata=data.get("metadata", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "domain_type": self.domain_type,
            "domain_name": self.domain_name,
            "description": self.description,
            "tacit_knowledge": {
                "principles": self.knowledge.principles,
                "constraints": self.knowledge.constraints,
                "quality_criteria": [
                    {"name": qc.name, "weight": qc.weight, "description": qc.description}
                    for qc in self.knowledge.quality_criteria
                ],
                "thinking_styles": self.knowledge.thinking_styles,
                "expert_personas": [
                    {"role": ep.role, "focus": ep.focus, "background": ep.background}
                    for ep in self.knowledge.expert_personas
                ],
                "terminology": self.knowledge.terminology,
                "patterns": self.knowledge.patterns,
                "anti_patterns": self.knowledge.anti_patterns
            },
            "critique_template": self.critique_template,
            "refinement_template": self.refinement_template,
            "metadata": self.metadata
        }


class DomainEvaluator(ABC):
    """
    Abstract base class for domain-specific evaluation.
    Implements multi-dimensional evaluation based on domain knowledge.
    """

    def __init__(self, domain_config: DomainConfig, llm_client: Any = None):
        self.domain_config = domain_config
        self.llm_client = llm_client

    def evaluate(self, response: str, ground_truth: str = "",
                 question: str = "") -> Dict[str, float]:
        """
        Perform comprehensive domain-specific evaluation.

        Args:
            response: LLM generated response to evaluate
            ground_truth: Expected correct answer (if available)
            question: Original question (for context)

        Returns:
            Dictionary of scores for each evaluation dimension
        """
        scores = {}

        # 1. Basic accuracy (if ground truth provided)
        if ground_truth:
            scores['accuracy'] = self.check_accuracy(response, ground_truth)

        # 2. Constraint compliance
        scores['constraint_compliance'] = self.check_constraints(response)

        # 3. Principle alignment
        scores['principle_alignment'] = self.check_principles(response)

        # 4. Domain-specific quality criteria
        for criterion in self.domain_config.knowledge.quality_criteria:
            scores[criterion.name] = self.evaluate_criterion(response, criterion)

        # 5. Case-specific evaluation (if question matches a case)
        case_score = self.evaluate_against_cases(response, question)
        if case_score is not None:
            scores['case_coverage'] = case_score

        # Calculate weighted average
        scores['overall'] = self.calculate_weighted_score(scores)

        return scores

    @abstractmethod
    def check_accuracy(self, response: str, ground_truth: str) -> float:
        """Check basic accuracy against ground truth."""
        pass

    def check_constraints(self, response: str) -> float:
        """
        Check if response violates any domain constraints.
        Returns 1.0 if no violations, decreases with each violation.
        """
        if not self.domain_config.knowledge.constraints:
            return 1.0

        violations = 0
        total_constraints = len(self.domain_config.knowledge.constraints)

        for constraint in self.domain_config.knowledge.constraints:
            if self._violates_constraint(response, constraint):
                violations += 1

        return 1.0 - (violations / total_constraints)

    def _violates_constraint(self, response: str, constraint: str) -> bool:
        """
        Check if response violates a specific constraint.
        Override in subclass for domain-specific logic.
        """
        # Default implementation using keyword matching
        # Subclasses should implement LLM-based checking
        constraint_lower = constraint.lower()
        response_lower = response.lower()

        # Check for negation patterns
        if "금지" in constraint_lower or "하지 않" in constraint_lower:
            # Extract what is forbidden
            forbidden_keywords = self._extract_forbidden_keywords(constraint)
            for keyword in forbidden_keywords:
                if keyword.lower() in response_lower:
                    return True

        return False

    def _extract_forbidden_keywords(self, constraint: str) -> List[str]:
        """Extract keywords that are forbidden based on constraint."""
        # Simple implementation - override for better extraction
        return []

    def check_principles(self, response: str) -> float:
        """
        Check how well response aligns with domain principles.
        Returns score from 0.0 to 1.0.
        """
        if not self.domain_config.knowledge.principles:
            return 1.0

        aligned_count = 0
        total_principles = len(self.domain_config.knowledge.principles)

        for principle in self.domain_config.knowledge.principles:
            if self._aligns_with_principle(response, principle):
                aligned_count += 1

        return aligned_count / total_principles

    def _aligns_with_principle(self, response: str, principle: str) -> bool:
        """
        Check if response aligns with a specific principle.
        Override in subclass for domain-specific logic.
        """
        # Default: assume aligned (subclass should implement proper checking)
        return True

    def evaluate_criterion(self, response: str, criterion: QualityCriterion) -> float:
        """
        Evaluate response against a specific quality criterion.
        Override in subclass for domain-specific evaluation.
        """
        # Default implementation - subclass should override
        return 0.5

    def evaluate_against_cases(self, response: str, question: str) -> Optional[float]:
        """
        Evaluate response against matching cases from case library.
        """
        if not question or not self.domain_config.case_library:
            return None

        matching_cases = self._find_matching_cases(question)
        if not matching_cases:
            return None

        total_score = 0.0
        for case in matching_cases:
            case_score = self._evaluate_single_case(response, case)
            total_score += case_score

        return total_score / len(matching_cases)

    def _find_matching_cases(self, question: str) -> List[CaseExample]:
        """Find cases that match the given question."""
        # Simple keyword matching - override for better matching
        matching = []
        question_lower = question.lower()

        for case in self.domain_config.case_library.get_all_cases():
            case_question_lower = case.question.lower()
            # Check for significant overlap
            if self._questions_match(question_lower, case_question_lower):
                matching.append(case)

        return matching

    def _questions_match(self, q1: str, q2: str) -> bool:
        """Check if two questions are similar enough."""
        # Simple word overlap check
        words1 = set(q1.split())
        words2 = set(q2.split())
        overlap = len(words1 & words2)
        min_len = min(len(words1), len(words2))

        if min_len == 0:
            return False

        return overlap / min_len > 0.5

    def _evaluate_single_case(self, response: str, case: CaseExample) -> float:
        """Evaluate response against a single case."""
        response_lower = response.lower()

        # Check expected elements
        expected_found = 0
        for element in case.expected_elements:
            if element.lower() in response_lower:
                expected_found += 1

        expected_score = expected_found / len(case.expected_elements) if case.expected_elements else 1.0

        # Check forbidden elements (penalty)
        forbidden_found = 0
        for element in case.forbidden_elements:
            if element.lower() in response_lower:
                forbidden_found += 1

        forbidden_penalty = forbidden_found / len(case.forbidden_elements) if case.forbidden_elements else 0.0

        return max(0.0, expected_score - forbidden_penalty)

    def calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted average of all scores."""
        if not scores:
            return 0.0

        # Build weight map from quality criteria
        weight_map = {
            qc.name: qc.weight
            for qc in self.domain_config.knowledge.quality_criteria
        }

        # Default weights for standard metrics
        default_weights = {
            'accuracy': 0.3,
            'constraint_compliance': 0.25,
            'principle_alignment': 0.2,
            'case_coverage': 0.25
        }

        total_weight = 0.0
        weighted_sum = 0.0

        for metric, score in scores.items():
            if metric == 'overall':
                continue

            weight = weight_map.get(metric, default_weights.get(metric, 0.1))
            weighted_sum += score * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0


class DomainCritiqueGenerator:
    """
    Generates domain-aware critiques for prompt refinement.
    Uses domain knowledge to provide specialized feedback.
    """

    def __init__(self, domain_config: DomainConfig, llm_client: Any = None):
        self.domain_config = domain_config
        self.llm_client = llm_client

    def generate_critique_prompt(self, instruction: str, examples: str,
                                  evaluation_scores: Dict[str, float] = None) -> str:
        """
        Generate a domain-aware critique prompt.

        Args:
            instruction: Current prompt instruction being evaluated
            examples: Example responses from the current prompt
            evaluation_scores: Optional scores from domain evaluation

        Returns:
            Formatted critique prompt incorporating domain knowledge
        """
        # Use custom template if provided
        if self.domain_config.critique_template:
            return self._format_custom_template(instruction, examples, evaluation_scores)

        # Generate default domain-aware critique prompt
        return self._generate_default_critique(instruction, examples, evaluation_scores)

    def _format_custom_template(self, instruction: str, examples: str,
                                 scores: Dict[str, float] = None) -> str:
        """Format custom critique template with variables."""
        template = self.domain_config.critique_template

        # Prepare template variables
        variables = {
            "instruction": instruction,
            "examples": examples,
            "domain_type": self.domain_config.domain_type,
            "domain_name": self.domain_config.domain_name,
            "principles": self._format_list(self.domain_config.knowledge.principles),
            "constraints": self._format_list(self.domain_config.knowledge.constraints),
            "quality_criteria": self._format_criteria(),
            "thinking_styles": self._format_list(self.domain_config.knowledge.thinking_styles),
            "scores": self._format_scores(scores) if scores else ""
        }

        # Format template
        try:
            return template.format(**variables)
        except KeyError as e:
            # If template has unknown variables, return with available ones
            for key, value in variables.items():
                template = template.replace(f"{{{key}}}", str(value))
            return template

    def _generate_default_critique(self, instruction: str, examples: str,
                                    scores: Dict[str, float] = None) -> str:
        """Generate default domain-aware critique prompt."""

        critique_prompt = f"""당신은 {self.domain_config.domain_name} 분야의 전문가입니다.
다음 프롬프트 지시문과 예제 응답을 평가하고 개선점을 제시하세요.

## 현재 프롬프트 지시문:
{instruction}

## 예제 응답:
{examples}

## 도메인 원칙 (이 원칙들이 잘 반영되었는지 확인):
{self._format_list(self.domain_config.knowledge.principles)}

## 도메인 제약조건 (위반사항이 없는지 확인):
{self._format_list(self.domain_config.knowledge.constraints)}

## 품질 평가 기준:
{self._format_criteria()}
"""

        if scores:
            critique_prompt += f"""
## 현재 평가 점수:
{self._format_scores(scores)}
"""

        critique_prompt += """
## 비평 요청:
위의 도메인 지식을 바탕으로 다음 관점에서 프롬프트를 비평해주세요:
1. 도메인 원칙 반영도: 핵심 원칙들이 충분히 반영되어 있는가?
2. 제약조건 준수: 위반 가능성이 있는 부분은 없는가?
3. 품질 기준 충족: 각 품질 기준에서 개선이 필요한 부분은?
4. 전문성 수준: 도메인 전문가 관점에서 부족한 점은?
5. 구체적 개선 제안: 어떻게 수정하면 더 나은 결과를 얻을 수 있는가?

비평 결과를 상세히 작성해주세요.
"""
        return critique_prompt

    def generate_refinement_prompt(self, instruction: str, examples: str,
                                    critique: str) -> str:
        """
        Generate a domain-aware refinement prompt.

        Args:
            instruction: Current prompt instruction
            examples: Example responses
            critique: Generated critique

        Returns:
            Formatted refinement prompt
        """
        if self.domain_config.refinement_template:
            return self._format_refinement_template(instruction, examples, critique)

        return self._generate_default_refinement(instruction, examples, critique)

    def _format_refinement_template(self, instruction: str, examples: str,
                                     critique: str) -> str:
        """Format custom refinement template."""
        template = self.domain_config.refinement_template

        variables = {
            "instruction": instruction,
            "examples": examples,
            "critique": critique,
            "domain_type": self.domain_config.domain_type,
            "domain_name": self.domain_config.domain_name,
            "principles": self._format_list(self.domain_config.knowledge.principles),
            "constraints": self._format_list(self.domain_config.knowledge.constraints),
            "thinking_styles": self._format_list(self.domain_config.knowledge.thinking_styles)
        }

        try:
            return template.format(**variables)
        except KeyError:
            for key, value in variables.items():
                template = template.replace(f"{{{key}}}", str(value))
            return template

    def _generate_default_refinement(self, instruction: str, examples: str,
                                      critique: str) -> str:
        """Generate default domain-aware refinement prompt."""

        expert_context = ""
        if self.domain_config.knowledge.expert_personas:
            persona = self.domain_config.knowledge.expert_personas[0]
            expert_context = f"당신은 {persona.role}로서, {persona.focus}에 집중합니다."

        return f"""## 역할
{expert_context if expert_context else f"당신은 {self.domain_config.domain_name} 분야의 전문가입니다."}

## 현재 프롬프트 지시문:
{instruction}

## 비평 내용:
{critique}

## 도메인 핵심 원칙:
{self._format_list(self.domain_config.knowledge.principles)}

## 준수해야 할 제약조건:
{self._format_list(self.domain_config.knowledge.constraints)}

## 권장 사고방식:
{self._format_list(self.domain_config.knowledge.thinking_styles)}

## 개선 요청:
위의 비평과 도메인 지식을 바탕으로 프롬프트를 개선해주세요.

개선 시 다음 사항을 반드시 포함하세요:
1. 도메인 원칙이 명시적으로 반영되도록 수정
2. 제약조건 위반을 방지하는 가이드라인 추가
3. 전문가 사고방식을 유도하는 지시문 포함
4. 품질 기준을 충족하도록 구체화

개선된 프롬프트를 <IMPROVED_PROMPT></IMPROVED_PROMPT> 태그 안에 작성해주세요.
"""

    def _format_list(self, items: List[str]) -> str:
        """Format list as numbered items."""
        if not items:
            return "(없음)"
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def _format_criteria(self) -> str:
        """Format quality criteria with weights."""
        criteria = self.domain_config.knowledge.quality_criteria
        if not criteria:
            return "(기본 품질 기준 적용)"

        lines = []
        for qc in criteria:
            weight_pct = int(qc.weight * 100)
            desc = f" - {qc.description}" if qc.description else ""
            lines.append(f"- {qc.name} (가중치: {weight_pct}%){desc}")

        return "\n".join(lines)

    def _format_scores(self, scores: Dict[str, float]) -> str:
        """Format evaluation scores."""
        if not scores:
            return ""

        lines = []
        for metric, score in scores.items():
            pct = int(score * 100)
            lines.append(f"- {metric}: {pct}%")

        return "\n".join(lines)


class DomainRegistry:
    """
    Registry for managing domain configurations.
    Allows dynamic registration and lookup of domain configs.
    """

    _domains: Dict[str, DomainConfig] = {}
    _evaluators: Dict[str, type] = {}

    @classmethod
    def register_domain(cls, domain_config: DomainConfig,
                        evaluator_class: type = None) -> None:
        """Register a domain configuration."""
        cls._domains[domain_config.domain_type] = domain_config
        if evaluator_class:
            cls._evaluators[domain_config.domain_type] = evaluator_class

    @classmethod
    def get_domain(cls, domain_type: str) -> Optional[DomainConfig]:
        """Get domain configuration by type."""
        return cls._domains.get(domain_type)

    @classmethod
    def get_evaluator(cls, domain_type: str) -> Optional[type]:
        """Get evaluator class for domain type."""
        return cls._evaluators.get(domain_type)

    @classmethod
    def list_domains(cls) -> List[str]:
        """List all registered domain types."""
        return list(cls._domains.keys())

    @classmethod
    def load_from_directory(cls, directory: str) -> None:
        """Load all domain configs from a directory."""
        if not os.path.exists(directory):
            return

        for filename in os.listdir(directory):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                filepath = os.path.join(directory, filename)
                try:
                    config = DomainConfig.from_yaml(filepath)
                    cls.register_domain(config)
                except Exception as e:
                    print(f"Warning: Failed to load domain config from {filepath}: {e}")

    @classmethod
    def clear(cls) -> None:
        """Clear all registered domains."""
        cls._domains.clear()
        cls._evaluators.clear()
