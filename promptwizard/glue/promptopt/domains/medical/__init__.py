# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Medical domain module for healthcare-specific prompt optimization.
"""

from .evaluator import MedicalDomainEvaluator
from .config import get_medical_domain_config, MEDICAL_DOMAIN_CONFIG

__all__ = [
    "MedicalDomainEvaluator",
    "get_medical_domain_config",
    "MEDICAL_DOMAIN_CONFIG"
]
