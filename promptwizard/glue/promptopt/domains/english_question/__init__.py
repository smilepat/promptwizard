# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
English Question Generation domain module for educational English test item creation.
영어 문항 생성 도메인 모듈
"""

from .config import get_english_question_domain_config, ENGLISH_QUESTION_DOMAIN_CONFIG

__all__ = [
    "get_english_question_domain_config",
    "ENGLISH_QUESTION_DOMAIN_CONFIG"
]
