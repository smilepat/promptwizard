# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Domain-specific prompt optimization module.
Provides domain knowledge integration for tacit knowledge-aware prompt optimization.
"""

from .base_domain import (
    DomainConfig,
    DomainKnowledge,
    DomainEvaluator,
    DomainCritiqueGenerator,
    DomainRegistry
)

__all__ = [
    "DomainConfig",
    "DomainKnowledge",
    "DomainEvaluator",
    "DomainCritiqueGenerator",
    "DomainRegistry"
]
