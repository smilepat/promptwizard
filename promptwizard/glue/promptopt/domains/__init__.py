# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Domain-specific prompt optimization module.
Provides domain knowledge integration for tacit knowledge-aware prompt optimization.

Supported domains:
- medical: Healthcare and medical advice
- legal: Legal information and guidance
- finance: Financial and investment information
- english_question: English test item generation

Usage:
    from promptwizard.glue.promptopt.domains import (
        DomainConfig,
        create_domain_optimizer,
        MEDICAL_DOMAIN_CONFIG,
        LEGAL_DOMAIN_CONFIG,
        FINANCE_DOMAIN_CONFIG
    )

    # Create domain-aware optimizer
    optimizer = create_domain_optimizer("medical")

    # Or use pre-configured domain config
    config = MEDICAL_DOMAIN_CONFIG
"""

from .base_domain import (
    DomainConfig,
    DomainKnowledge,
    DomainEvaluator,
    DomainCritiqueGenerator,
    DomainRegistry,
    QualityCriterion,
    ExpertPersona,
    CaseLibrary,
    CaseExample
)

from .domain_aware_optimizer import (
    DomainAwarePromptOptimizer,
    create_domain_optimizer
)

# Import domain-specific configs
from .medical import MEDICAL_DOMAIN_CONFIG, MedicalDomainEvaluator
from .legal import LEGAL_DOMAIN_CONFIG
from .finance import FINANCE_DOMAIN_CONFIG
from .english_question import ENGLISH_QUESTION_DOMAIN_CONFIG

# Register default domains
DomainRegistry.register_domain(MEDICAL_DOMAIN_CONFIG, MedicalDomainEvaluator)
DomainRegistry.register_domain(LEGAL_DOMAIN_CONFIG)
DomainRegistry.register_domain(FINANCE_DOMAIN_CONFIG)
DomainRegistry.register_domain(ENGLISH_QUESTION_DOMAIN_CONFIG)

__all__ = [
    # Base classes
    "DomainConfig",
    "DomainKnowledge",
    "DomainEvaluator",
    "DomainCritiqueGenerator",
    "DomainRegistry",
    "QualityCriterion",
    "ExpertPersona",
    "CaseLibrary",
    "CaseExample",

    # Optimizer
    "DomainAwarePromptOptimizer",
    "create_domain_optimizer",

    # Pre-configured domains
    "MEDICAL_DOMAIN_CONFIG",
    "LEGAL_DOMAIN_CONFIG",
    "FINANCE_DOMAIN_CONFIG",
    "ENGLISH_QUESTION_DOMAIN_CONFIG",

    # Domain-specific evaluators
    "MedicalDomainEvaluator"
]
