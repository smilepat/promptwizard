# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
English Question Generation domain configuration.
영어 문항 생성 도메인 설정 - 교육용 영어 문제 생성을 위한 암묵지
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ..base_domain import (
    DomainConfig,
    DomainKnowledge,
    QualityCriterion,
    ExpertPersona,
    CaseLibrary,
    CaseExample
)


# ============================================================================
# 문항 유형별 템플릿 정의
# ============================================================================

@dataclass
class QuestionTemplate:
    """문항 유형별 프롬프트 템플릿"""
    type_id: str
    type_name: str
    description: str
    prompt_template: str
    output_format: str
    examples: List[str] = field(default_factory=list)
    tips: List[str] = field(default_factory=list)


QUESTION_TEMPLATES: Dict[str, QuestionTemplate] = {
    "grammar_tense": QuestionTemplate(
        type_id="grammar_tense",
        type_name="문법 - 시제",
        description="영어 시제(현재, 과거, 미래, 완료 등)를 묻는 문항",
        prompt_template="""당신은 영어 문법 문항 출제 전문가입니다.

## 문항 유형: 시제 문법 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 영어 시제 문법 문항을 생성하세요:

### 필수 조건:
1. 목표 시제: {target_tense}
2. 문맥이 있는 문장에서 시제 선택 문항
3. 4-5개의 선택지 (정답 1개, 매력적 오답 3-4개)
4. 오답은 학습자의 전형적 오류를 반영

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "grammar_tense",
  "target_grammar": "시제명",
  "stem": "문항 지시문",
  "context": "문맥 문장 (빈칸 포함)",
  "options": [
    {"number": "①", "text": "선택지1", "is_answer": false},
    {"number": "②", "text": "선택지2", "is_answer": true},
    {"number": "③", "text": "선택지3", "is_answer": false},
    {"number": "④", "text": "선택지4", "is_answer": false},
    {"number": "⑤", "text": "선택지5", "is_answer": false}
  ],
  "answer": "②",
  "explanation": "정답 해설",
  "distractor_analysis": "오답 선택지 설계 근거"
}
```""",
        examples=[
            "다음 빈칸에 들어갈 가장 적절한 것을 고르시오.\nShe ___ to the library yesterday.",
            "밑줄 친 부분 중 어법상 틀린 것을 고르시오."
        ],
        tips=[
            "시제 혼동이 잦은 상황(현재완료 vs 과거) 활용",
            "시간 부사(yesterday, since, for 등)와 함께 제시",
            "문맥에서 시제를 추론해야 하는 문항 권장"
        ]
    ),

    "grammar_structure": QuestionTemplate(
        type_id="grammar_structure",
        type_name="문법 - 문장구조",
        description="관계사, 분사구문, 가정법 등 문장 구조 문항",
        prompt_template="""당신은 영어 문법 문항 출제 전문가입니다.

## 문항 유형: 문장구조 문법 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 영어 문장구조 문법 문항을 생성하세요:

### 필수 조건:
1. 목표 문법: {target_grammar} (관계사/분사/가정법/도치 등)
2. 실제 사용 맥락이 있는 문장
3. 4-5개의 선택지
4. 문법적으로 유사하지만 의미가 다른 오답 설계

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "grammar_structure",
  "target_grammar": "문법 요소명",
  "stem": "문항 지시문",
  "passage": "지문 (필요시)",
  "context": "문맥 문장",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "grammar_point": "핵심 문법 포인트 설명"
}
```""",
        examples=[
            "다음 빈칸에 들어갈 말로 가장 적절한 것은?\nThe book ___ I bought yesterday was very interesting.",
            "밑줄 친 부분을 어법에 맞게 고친 것은?"
        ],
        tips=[
            "관계대명사 vs 관계부사 혼동 활용",
            "분사의 능동/수동 구분 문항",
            "실제 의사소통 상황에서의 문법 사용"
        ]
    ),

    "vocabulary_context": QuestionTemplate(
        type_id="vocabulary_context",
        type_name="어휘 - 문맥상 의미",
        description="문맥에서 어휘의 적절한 의미를 파악하는 문항",
        prompt_template="""당신은 영어 어휘 문항 출제 전문가입니다.

## 문항 유형: 문맥상 어휘 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 영어 어휘 문항을 생성하세요:

### 필수 조건:
1. 목표 어휘 수준: {vocabulary_level}
2. 문맥에서 의미를 추론해야 하는 문항
3. 다의어 또는 유의어 활용
4. 5개의 선택지

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "vocabulary_context",
  "target_word": "목표 어휘",
  "word_level": "어휘 수준",
  "stem": "문항 지시문",
  "passage": "지문",
  "underlined_word": "밑줄 친 단어",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "word_meaning": "문맥상 의미"
}
```""",
        examples=[
            "밑줄 친 'run'과 의미가 가장 가까운 것은?",
            "빈칸에 들어갈 단어로 가장 적절한 것은?"
        ],
        tips=[
            "다의어의 맥락별 의미 차이 활용",
            "동의어/반의어 관계 활용",
            "어근, 접두사, 접미사 단서 제공"
        ]
    ),

    "reading_main_idea": QuestionTemplate(
        type_id="reading_main_idea",
        type_name="독해 - 주제/요지",
        description="글의 주제, 요지, 제목을 파악하는 문항",
        prompt_template="""당신은 영어 독해 문항 출제 전문가입니다.

## 문항 유형: 주제/요지 파악 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 영어 독해 문항을 생성하세요:

### 필수 조건:
1. 지문 길이: {passage_length}단어 내외
2. 지문 주제: {topic}
3. 글의 유형: {text_type}
4. 5개의 선택지 (주제문 1개, 부분적/확대 해석 오답)

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "reading_main_idea",
  "question_subtype": "주제/요지/제목",
  "stem": "문항 지시문",
  "passage": "영어 지문",
  "passage_korean": "지문 한글 번역 (참고용)",
  "word_count": 단어수,
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "main_idea": "핵심 주제",
  "passage_structure": "글의 구조 분석"
}
```""",
        examples=[
            "다음 글의 주제로 가장 적절한 것은?",
            "다음 글의 제목으로 가장 적절한 것은?",
            "다음 글의 요지로 가장 적절한 것은?"
        ],
        tips=[
            "주제문이 명시적/암시적인 경우 모두 포함",
            "부분적 내용을 전체 주제로 오해하는 오답",
            "지나치게 일반화하거나 축소하는 오답"
        ]
    ),

    "reading_blank": QuestionTemplate(
        type_id="reading_blank",
        type_name="독해 - 빈칸 추론",
        description="글의 흐름에 맞는 빈칸 내용을 추론하는 문항",
        prompt_template="""당신은 영어 독해 문항 출제 전문가입니다.

## 문항 유형: 빈칸 추론 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 빈칸 추론 문항을 생성하세요:

### 필수 조건:
1. 지문 길이: {passage_length}단어 내외
2. 빈칸 유형: {blank_type} (단어/구/절/문장)
3. 추론 난이도: {inference_level}
4. 5개의 선택지

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "reading_blank",
  "blank_type": "빈칸 유형",
  "stem": "문항 지시문",
  "passage": "영어 지문 (빈칸 포함)",
  "word_count": 단어수,
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "logical_flow": "논리적 흐름 분석",
  "clue_sentences": ["단서가 되는 문장들"]
}
```""",
        examples=[
            "다음 글의 빈칸에 들어갈 말로 가장 적절한 것은?",
            "다음 글의 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?"
        ],
        tips=[
            "빈칸 전후의 논리적 연결 관계 활용",
            "역접, 인과, 예시 등 담화 표지 활용",
            "paraphrase된 표현을 정답으로"
        ]
    ),

    "reading_order": QuestionTemplate(
        type_id="reading_order",
        type_name="독해 - 순서 배열",
        description="글의 순서를 논리적으로 배열하는 문항",
        prompt_template="""당신은 영어 독해 문항 출제 전문가입니다.

## 문항 유형: 순서 배열 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 순서 배열 문항을 생성하세요:

### 필수 조건:
1. 도입문 + 3개 문단 (A), (B), (C)
2. 총 길이: {passage_length}단어 내외
3. 논리적 연결어 및 지시어 활용
4. 5개의 순서 조합 선택지

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "reading_order",
  "stem": "문항 지시문",
  "intro": "도입문",
  "paragraph_A": "(A) 문단",
  "paragraph_B": "(B) 문단",
  "paragraph_C": "(C) 문단",
  "options": [
    {"number": "①", "order": "(A)-(C)-(B)"},
    {"number": "②", "order": "(B)-(A)-(C)"},
    ...
  ],
  "answer": "정답 번호",
  "correct_order": "정답 순서",
  "explanation": "정답 해설",
  "cohesion_devices": ["연결 장치 목록"]
}
```""",
        examples=[
            "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?"
        ],
        tips=[
            "대명사-선행사 관계 활용",
            "시간/논리 순서 연결어 활용",
            "this, such, however 등 담화 표지 활용"
        ]
    ),

    "reading_insertion": QuestionTemplate(
        type_id="reading_insertion",
        type_name="독해 - 문장 삽입",
        description="주어진 문장이 들어갈 위치를 찾는 문항",
        prompt_template="""당신은 영어 독해 문항 출제 전문가입니다.

## 문항 유형: 문장 삽입 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 문장 삽입 문항을 생성하세요:

### 필수 조건:
1. 지문 길이: {passage_length}단어 내외
2. 삽입 문장: 지문 흐름에 필수적인 문장
3. 5개의 삽입 위치 표시
4. 논리적 연결이 명확한 정답

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "reading_insertion",
  "stem": "문항 지시문",
  "given_sentence": "삽입할 문장",
  "passage_with_markers": "지문 (① ② ③ ④ ⑤ 위치 표시)",
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "connection_analysis": "연결 관계 분석"
}
```""",
        examples=[
            "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?"
        ],
        tips=[
            "삽입 문장에 지시어/연결어 포함",
            "전후 문맥과의 논리적 연결",
            "오답 위치에서 의미 단절 발생"
        ]
    ),

    "conversation": QuestionTemplate(
        type_id="conversation",
        type_name="대화문 - 응답 완성",
        description="대화 맥락에 맞는 적절한 응답을 고르는 문항",
        prompt_template="""당신은 영어 대화문 문항 출제 전문가입니다.

## 문항 유형: 대화 응답 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 대화문 문항을 생성하세요:

### 필수 조건:
1. 대화 상황: {situation}
2. 대화 턴 수: {turns}회
3. 화용론적으로 적절한 응답
4. 5개의 선택지

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "conversation",
  "situation": "대화 상황",
  "stem": "문항 지시문",
  "dialogue": [
    {"speaker": "A", "utterance": "발화1"},
    {"speaker": "B", "utterance": "발화2"},
    {"speaker": "A", "utterance": "_______"}
  ],
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "pragmatic_function": "화행 기능"
}
```""",
        examples=[
            "대화의 빈칸에 들어갈 말로 가장 적절한 것은?",
            "대화의 흐름으로 보아, B의 응답으로 가장 적절한 것은?"
        ],
        tips=[
            "간접 화행 활용 (요청, 거절, 제안 등)",
            "상황 맥락에 맞는 공손 표현",
            "문화적으로 적절한 응답"
        ]
    ),

    "listening_comprehension": QuestionTemplate(
        type_id="listening_comprehension",
        type_name="듣기 - 내용 이해",
        description="듣기 지문의 내용을 이해하는 문항 (스크립트 기반)",
        prompt_template="""당신은 영어 듣기 문항 출제 전문가입니다.

## 문항 유형: 듣기 이해 문항
## 대상 학년: {grade_level}
## 난이도: {difficulty}
## CEFR 레벨: {cefr_level}

다음 조건에 맞는 듣기 문항을 생성하세요:

### 필수 조건:
1. 듣기 유형: {listening_type} (대화/담화/안내문 등)
2. 길이: {duration}초 분량
3. 세부 정보 또는 추론 문항
4. 5개의 선택지

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_type": "listening_comprehension",
  "listening_type": "듣기 유형",
  "stem": "문항 지시문 (듣기 전 제시)",
  "script": "듣기 스크립트",
  "duration_seconds": 예상 소요 시간,
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "key_information": "핵심 정보"
}
```""",
        examples=[
            "대화를 듣고, 남자가 할 일로 가장 적절한 것을 고르시오.",
            "담화를 듣고, 주제로 가장 적절한 것을 고르시오."
        ],
        tips=[
            "핵심 정보는 한 번만 언급",
            "paraphrase된 표현을 정답으로",
            "실제 듣기 상황의 자연스러운 발화"
        ]
    ),
}


# ============================================================================
# 난이도/학년 체계 정의
# ============================================================================

@dataclass
class DifficultyLevel:
    """난이도 레벨 정의"""
    level_id: str
    level_name: str
    cefr: str
    grade_range: str
    vocabulary_range: str
    grammar_scope: List[str]
    passage_length: str
    description: str


DIFFICULTY_LEVELS: Dict[str, DifficultyLevel] = {
    "elementary_low": DifficultyLevel(
        level_id="elementary_low",
        level_name="초급 하",
        cefr="A1",
        grade_range="초등 3-4학년",
        vocabulary_range="기초 어휘 300-500단어",
        grammar_scope=["be동사", "일반동사 현재", "단순 의문문"],
        passage_length="30-50단어",
        description="기초 영어 학습자를 위한 수준"
    ),
    "elementary_high": DifficultyLevel(
        level_id="elementary_high",
        level_name="초급 상",
        cefr="A2",
        grade_range="초등 5-6학년",
        vocabulary_range="기초 어휘 500-800단어",
        grammar_scope=["과거 시제", "미래 표현", "조동사 기초"],
        passage_length="50-80단어",
        description="초등 고학년 수준"
    ),
    "intermediate_low": DifficultyLevel(
        level_id="intermediate_low",
        level_name="중급 하",
        cefr="B1",
        grade_range="중학교 1-2학년",
        vocabulary_range="중학 필수 어휘 1000-1500단어",
        grammar_scope=["현재완료", "수동태", "to부정사", "동명사"],
        passage_length="80-120단어",
        description="중학교 저학년 수준"
    ),
    "intermediate_mid": DifficultyLevel(
        level_id="intermediate_mid",
        level_name="중급 중",
        cefr="B1+",
        grade_range="중학교 3학년",
        vocabulary_range="중학 필수 어휘 1500-2000단어",
        grammar_scope=["관계대명사", "분사", "가정법 기초"],
        passage_length="120-150단어",
        description="중학교 고학년 수준"
    ),
    "intermediate_high": DifficultyLevel(
        level_id="intermediate_high",
        level_name="중급 상",
        cefr="B2",
        grade_range="고등학교 1학년",
        vocabulary_range="고등 필수 어휘 2000-2500단어",
        grammar_scope=["관계부사", "분사구문", "가정법"],
        passage_length="150-200단어",
        description="고등학교 1학년 수준"
    ),
    "advanced_low": DifficultyLevel(
        level_id="advanced_low",
        level_name="고급 하",
        cefr="B2+",
        grade_range="고등학교 2학년",
        vocabulary_range="수능 필수 어휘 2500-3000단어",
        grammar_scope=["도치", "강조", "복합 관계사"],
        passage_length="200-250단어",
        description="고등학교 2학년/수능 기초 수준"
    ),
    "advanced_high": DifficultyLevel(
        level_id="advanced_high",
        level_name="고급 상",
        cefr="C1",
        grade_range="고등학교 3학년/수능",
        vocabulary_range="수능 어휘 3000-3500단어",
        grammar_scope=["전체 문법 범위", "복합 구조"],
        passage_length="250-350단어",
        description="수능/대입 수준"
    ),
    "proficiency": DifficultyLevel(
        level_id="proficiency",
        level_name="숙달",
        cefr="C1+",
        grade_range="대학/성인",
        vocabulary_range="TOEFL/IELTS 수준 어휘",
        grammar_scope=["학술 영어 전체"],
        passage_length="300-500단어",
        description="공인 시험/학술 영어 수준"
    ),
}


# ============================================================================
# 교육과정 성취기준 (2015 개정 교육과정 기반)
# ============================================================================

ACHIEVEMENT_STANDARDS = {
    "middle_school": {
        "listening": [
            {"code": "[9영01-01]", "content": "어구나 문장을 듣고 연음, 축약 등의 현상을 식별한다"},
            {"code": "[9영01-02]", "content": "일상생활 관련 주제에 관한 말이나 대화를 듣고 세부 정보를 파악한다"},
            {"code": "[9영01-03]", "content": "일상생활 관련 주제에 관한 말이나 대화를 듣고 화자의 의도나 목적을 파악한다"},
        ],
        "speaking": [
            {"code": "[9영02-01]", "content": "주변의 사람, 사물에 대해 묻고 답한다"},
            {"code": "[9영02-02]", "content": "일상생활에 관해 간단히 묻고 답한다"},
            {"code": "[9영02-03]", "content": "자신의 경험이나 계획에 대해 간단히 말한다"},
        ],
        "reading": [
            {"code": "[9영03-01]", "content": "문장을 의미 단위로 끊어 읽으면서 의미를 파악한다"},
            {"code": "[9영03-02]", "content": "일상생활이나 친숙한 일반적 주제의 글을 읽고 세부 정보를 파악한다"},
            {"code": "[9영03-03]", "content": "일상생활이나 친숙한 일반적 주제의 글을 읽고 논리적 관계를 파악한다"},
        ],
        "writing": [
            {"code": "[9영04-01]", "content": "문장에서 알맞은 어휘를 활용하여 완성한다"},
            {"code": "[9영04-02]", "content": "간단한 초대, 감사, 축하 등의 글을 쓴다"},
            {"code": "[9영04-03]", "content": "자신의 경험이나 계획에 대해 간단히 쓴다"},
        ],
    },
    "high_school": {
        "listening": [
            {"code": "[10영01-01]", "content": "친숙한 일반적 주제에 관한 말이나 대화를 듣고 세부 정보를 파악한다"},
            {"code": "[10영01-02]", "content": "친숙한 일반적 주제에 관한 말이나 대화를 듣고 주제 및 요지를 파악한다"},
            {"code": "[10영01-03]", "content": "친숙한 일반적 주제에 관한 말이나 대화를 듣고 화자의 의도나 목적을 추론한다"},
        ],
        "reading": [
            {"code": "[10영03-01]", "content": "친숙한 일반적 주제에 관한 글을 읽고 세부 정보를 파악한다"},
            {"code": "[10영03-02]", "content": "친숙한 일반적 주제에 관한 글을 읽고 주제 및 요지를 파악한다"},
            {"code": "[10영03-03]", "content": "친숙한 일반적 주제에 관한 글을 읽고 논리적 관계를 파악한다"},
            {"code": "[10영03-04]", "content": "친숙한 일반적 주제에 관한 글을 읽고 필자의 의도나 목적을 추론한다"},
        ],
    },
}


# ============================================================================
# 확장된 테스트 케이스
# ============================================================================

def get_extended_case_library() -> CaseLibrary:
    """확장된 테스트 케이스 라이브러리 생성"""

    critical_cases = [
        # 문법 - 시제
        CaseExample(
            question="다음 빈칸에 들어갈 가장 적절한 것을 고르시오.\nShe ___ to the library every day since she started her research project.",
            expected_elements=["has been going", "현재완료진행", "since와 함께 사용"],
            forbidden_elements=["goes", "went", "is going", "단순 현재/과거"],
            category="Grammar - Tense",
            difficulty="intermediate_high"
        ),
        # 문법 - 관계사
        CaseExample(
            question="다음 빈칸에 들어갈 말로 가장 적절한 것은?\nThis is the house ___ the famous writer lived for twenty years.",
            expected_elements=["where", "in which", "관계부사", "장소 선행사"],
            forbidden_elements=["which (전치사 없이)", "that (장소에 단독)", "who"],
            category="Grammar - Relative",
            difficulty="intermediate_mid"
        ),
        # 독해 - 빈칸 추론 (고난도)
        CaseExample(
            question="다음 글의 빈칸에 들어갈 말로 가장 적절한 것은? [3점]",
            expected_elements=["추상적 개념", "논리적 추론", "paraphrase"],
            forbidden_elements=["지문에서 직접 인용", "부분적 내용"],
            category="Reading - Blank Inference",
            difficulty="advanced_high"
        ),
    ]

    edge_cases = [
        # 다의어 문맥
        CaseExample(
            question="밑줄 친 'run'이 다음 글에서 의미하는 것으로 가장 적절한 것은?",
            expected_elements=["문맥상 의미", "다의어 구별", "정확한 해석"],
            forbidden_elements=["일반적인 '달리다' 의미만", "문맥 무시"],
            category="Vocabulary - Polysemy",
            difficulty="intermediate_high"
        ),
        # 함축 의미 추론
        CaseExample(
            question="밑줄 친 표현이 의미하는 바로 가장 적절한 것은?",
            expected_elements=["함축적 의미", "비유적 표현", "맥락 기반 추론"],
            forbidden_elements=["문자적 의미만", "직역"],
            category="Reading - Implication",
            difficulty="advanced_low"
        ),
    ]

    common_cases = [
        # Grammar - 시제 (기초)
        CaseExample(
            question="다음 빈칸에 들어갈 가장 적절한 것을 고르시오.\nShe ___ to the store yesterday.",
            expected_elements=["went", "과거 시제", "yesterday와 호응"],
            forbidden_elements=["go", "goes", "going", "has gone"],
            category="Grammar - Tense",
            difficulty="elementary_high"
        ),
        # Grammar - 조동사
        CaseExample(
            question="다음 빈칸에 들어갈 말로 가장 적절한 것은?\nYou ___ finish your homework before watching TV.",
            expected_elements=["must", "should", "have to", "의무 표현"],
            forbidden_elements=["can", "may", "단순 능력/허가"],
            category="Grammar - Modal",
            difficulty="intermediate_low"
        ),
        # 독해 - 주제
        CaseExample(
            question="다음 글의 주제로 가장 적절한 것은?",
            expected_elements=["중심 내용", "핵심 메시지", "전체 요약"],
            forbidden_elements=["세부 사항만", "부분적 내용", "지나친 일반화"],
            category="Reading - Main Idea",
            difficulty="intermediate_mid"
        ),
        # 독해 - 제목
        CaseExample(
            question="다음 글의 제목으로 가장 적절한 것은?",
            expected_elements=["핵심 키워드", "글의 초점", "함축적 표현"],
            forbidden_elements=["지나치게 구체적", "지나치게 일반적"],
            category="Reading - Title",
            difficulty="intermediate_high"
        ),
        # 독해 - 요지
        CaseExample(
            question="다음 글의 요지로 가장 적절한 것은?",
            expected_elements=["핵심 주장", "결론", "필자 의도"],
            forbidden_elements=["세부 예시만", "부분적 주장"],
            category="Reading - Gist",
            difficulty="advanced_low"
        ),
        # 독해 - 순서 배열
        CaseExample(
            question="주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
            expected_elements=["논리적 연결", "지시어 활용", "담화 표지"],
            forbidden_elements=["임의 배열", "연결 무시"],
            category="Reading - Order",
            difficulty="advanced_low"
        ),
        # 독해 - 문장 삽입
        CaseExample(
            question="글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?",
            expected_elements=["문맥 연결", "지시어 연결", "논리적 위치"],
            forbidden_elements=["흐름 단절", "부자연스러운 연결"],
            category="Reading - Insertion",
            difficulty="advanced_high"
        ),
        # 어휘 - 문맥상 의미
        CaseExample(
            question="밑줄 친 단어와 의미가 가장 가까운 것은?",
            expected_elements=["동의어", "문맥상 의미", "정확한 대체어"],
            forbidden_elements=["다른 의미의 동음어", "반의어"],
            category="Vocabulary - Synonym",
            difficulty="intermediate_mid"
        ),
        # 어휘 - 빈칸 어휘
        CaseExample(
            question="다음 글의 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
            expected_elements=["문맥상 어휘", "논리적 연결어", "적절한 조합"],
            forbidden_elements=["문맥 무관", "논리 불일치"],
            category="Vocabulary - Blank",
            difficulty="advanced_low"
        ),
        # 대화문
        CaseExample(
            question="대화의 빈칸에 들어갈 말로 가장 적절한 것은?",
            expected_elements=["맥락 적합", "화용적 적절성", "자연스러운 응답"],
            forbidden_elements=["맥락 무시", "부자연스러운 표현", "문화적 부적절"],
            category="Conversation",
            difficulty="intermediate_low"
        ),
        # 듣기 - 목적
        CaseExample(
            question="다음을 듣고, 화자가 하는 말의 목적으로 가장 적절한 것을 고르시오.",
            expected_elements=["화자 의도", "담화 목적", "핵심 메시지"],
            forbidden_elements=["세부 정보만", "부분적 내용"],
            category="Listening - Purpose",
            difficulty="intermediate_mid"
        ),
        # 듣기 - 세부정보
        CaseExample(
            question="대화를 듣고, 남자가 할 일로 가장 적절한 것을 고르시오.",
            expected_elements=["구체적 행동", "명시적 정보", "정확한 파악"],
            forbidden_elements=["추측", "언급되지 않은 내용"],
            category="Listening - Detail",
            difficulty="intermediate_low"
        ),
    ]

    return CaseLibrary(
        critical_cases=critical_cases,
        edge_cases=edge_cases,
        common_cases=common_cases
    )


# ============================================================================
# 메인 설정 함수
# ============================================================================

def get_english_question_domain_config() -> DomainConfig:
    """
    Get comprehensive English question generation domain configuration.
    Includes tacit knowledge from English education experts.
    """

    knowledge = DomainKnowledge(
        principles=[
            "문항은 측정하고자 하는 학습 목표에 정확히 부합해야 한다",
            "문항의 난이도는 대상 학습자 수준에 적합해야 한다",
            "지문과 문항은 명확하고 모호하지 않아야 한다",
            "오답 선택지는 그럴듯하지만 명확히 틀려야 한다 (Plausible Distractors)",
            "문법, 어휘, 독해, 듣기 영역별 특성을 고려해야 한다",
            "실생활 맥락과 연계된 authentic materials 활용을 권장한다",
            "Bloom's Taxonomy에 따른 인지 수준을 고려한다",
            "문화적 편향이나 차별적 요소를 배제해야 한다",
            "문항 간 독립성을 유지하여 한 문항이 다른 문항의 힌트가 되지 않도록 한다",
            "교육과정 성취기준과 연계하여 평가 목표를 명확히 한다"
        ],

        constraints=[
            "정답이 2개 이상이거나 정답이 없는 문항 생성 금지",
            "지문 없이 풀 수 있는 문항 (passage-independent) 지양",
            "특정 문화권/성별/인종에 유리하거나 불리한 내용 금지",
            "저작권이 있는 원문을 그대로 사용하는 것 금지",
            "문항 stem에 불필요한 정보나 혼란 요소 포함 금지",
            "정답 선택지가 다른 선택지보다 현저히 길거나 짧은 것 지양",
            "절대적 표현(always, never 등)을 정답에만 사용하는 패턴 지양",
            "이중 부정이나 복잡한 문장 구조로 인한 혼란 유발 금지",
            "정답 위치가 특정 번호에 편중되지 않도록 분산 배치"
        ],

        quality_criteria=[
            QualityCriterion(
                name="타당도",
                weight=0.25,
                description="문항이 측정하고자 하는 능력을 정확히 측정하는가",
                evaluation_prompt="이 문항이 의도한 영어 능력을 정확히 측정하고 있는가?"
            ),
            QualityCriterion(
                name="난이도 적절성",
                weight=0.20,
                description="대상 학습자 수준에 적합한 난이도인가",
                evaluation_prompt="이 문항의 난이도가 목표 학습자 수준에 적합한가?"
            ),
            QualityCriterion(
                name="명확성",
                weight=0.20,
                description="문항과 선택지가 명확하고 모호하지 않은가",
                evaluation_prompt="이 문항의 지시문, 지문, 선택지가 명확하고 이해하기 쉬운가?"
            ),
            QualityCriterion(
                name="변별도",
                weight=0.15,
                description="상위 학습자와 하위 학습자를 구분할 수 있는가",
                evaluation_prompt="이 문항이 학습자의 능력을 효과적으로 변별할 수 있는가?"
            ),
            QualityCriterion(
                name="오답 매력도",
                weight=0.10,
                description="오답 선택지가 그럴듯하여 적절한 기능을 하는가",
                evaluation_prompt="오답 선택지들이 적절히 매력적이면서도 명확히 오답인가?"
            ),
            QualityCriterion(
                name="교육과정 연계",
                weight=0.10,
                description="교육과정 성취기준과 적절히 연계되어 있는가",
                evaluation_prompt="이 문항이 해당 학년의 교육과정 성취기준에 부합하는가?"
            )
        ],

        thinking_styles=[
            "역방향 설계: 측정하고자 하는 능력/목표를 먼저 정의하고 문항 설계",
            "오류 분석 기반: 학습자의 전형적인 오류 패턴을 오답에 반영",
            "맥락 우선: 실제 영어 사용 상황을 고려한 authentic context 제공",
            "수준별 조정: 어휘, 문법, 문장 길이를 학습자 수준에 맞게 조절",
            "다중 인지 수준: 기억, 이해, 적용, 분석, 평가, 창조 수준 균형 배치",
            "지문 재활용: 하나의 지문으로 다양한 유형의 문항 개발",
            "Item writing guidelines 준수: 검증된 문항 작성 원칙 적용",
            "성취기준 매핑: 교육과정 성취기준에 따른 문항 설계"
        ],

        expert_personas=[
            ExpertPersona(
                role="영어교육학 교수",
                focus="언어 평가 이론 및 문항 개발 방법론",
                background="영어교육학 박사, 언어 평가 연구 전문",
                thinking_approach="이론적 타당성과 실제 적용의 균형, 연구 기반 접근"
            ),
            ExpertPersona(
                role="수능/TOEIC 출제위원",
                focus="대규모 표준화 시험 문항 개발",
                background="10년 이상 출제 경험, 문항 검토 전문",
                thinking_approach="공정성, 변별력, 난이도 조절의 정교함"
            ),
            ExpertPersona(
                role="원어민 영어 강사",
                focus="자연스러운 영어 표현 및 실용성",
                background="ESL/EFL 교육 경험, 원어민 화자 관점",
                thinking_approach="실제 사용되는 자연스러운 영어, 문화적 적절성"
            ),
            ExpertPersona(
                role="중고등학교 영어 교사",
                focus="학교 현장에서의 적용 가능성",
                background="교육 현장 경험, 학생 수준 파악",
                thinking_approach="교육과정 연계, 학생 동기 유발, 실제 수업 활용"
            )
        ],

        terminology={
            "Stem": "문항의 질문 부분, 물음 내용",
            "Distractor": "오답 선택지, 매력적 오답",
            "Key": "정답 선택지",
            "Passage": "읽기 문항의 지문",
            "Cloze": "빈칸 채우기 문항 유형",
            "Bloom's Taxonomy": "교육 목표 분류 체계 (기억-이해-적용-분석-평가-창조)",
            "Washback": "시험이 교육에 미치는 영향",
            "Item Difficulty": "문항 난이도 (정답률)",
            "Item Discrimination": "문항 변별도",
            "Authentic Materials": "실제 사용되는 자료 (신문, 광고 등)",
            "CEFR": "유럽공통참조기준 (A1-C2)",
            "Achievement Standard": "교육과정 성취기준"
        },

        patterns=[
            "문항 유형 명시 → 학습 목표 설정 → 지문 선정/작성 → 문항 및 선택지 개발",
            "Grammar 문항: 목표 문법 요소 → 전형적 오류 분석 → 오답 선택지 설계",
            "Vocabulary 문항: 목표 어휘 → 맥락 제시 → 동의어/반의어/문맥적 의미 활용",
            "Reading 문항: 글의 유형 결정 → 핵심 정보 파악 → 추론/요약/세부정보 문항 개발",
            "Listening 문항: 담화 유형 → 핵심 발화 설계 → 이해도 측정 문항 개발"
        ],

        anti_patterns=[
            "'All of the above', 'None of the above' 선택지 남용",
            "선택지 간 문법적 불일치 (정답만 문법적으로 맞는 경우)",
            "정답에만 구체적 정보, 오답은 모호한 표현 사용",
            "지문 문장을 그대로 정답으로 사용 (기계적 matching 유도)",
            "특정 위치에 정답 배치 패턴 (예: 정답이 항상 C)",
            "부정문 stem과 부정적 선택지의 이중 부정",
            "문항 간 정답 연쇄 또는 힌트 제공"
        ]
    )

    # Critique template for English question generation domain
    critique_template = """당신은 영어 평가 및 문항 개발 전문가입니다. 다음 프롬프트와 생성된 문항을 전문가 관점에서 비평해주세요.

## 현재 프롬프트 지시문:
{instruction}

## 생성된 예제 문항:
{examples}

## 비평 관점:
1. **타당도**: 문항이 의도한 영어 능력을 정확히 측정하고 있는가?
2. **난이도**: 대상 학습자 수준에 적합한가?
3. **명확성**: 지시문, 지문, 선택지가 명확하고 모호하지 않은가?
4. **오답 선택지 질**: 매력적이면서도 명확히 오답인가?
5. **문항 작성 원칙 준수**: Item writing guidelines를 따르고 있는가?
6. **공정성**: 특정 집단에 유불리가 없는가?
7. **교육과정 연계**: 성취기준에 부합하는가?

## 개선 제안:
구체적인 개선 방향을 제시해주세요.
"""

    # Refinement template
    refinement_template = """당신은 영어 평가 전문가입니다. 다음 비평을 바탕으로 프롬프트를 개선해주세요.

## 원본 프롬프트:
{original_instruction}

## 받은 비평:
{critique}

## 도메인 원칙 (반드시 반영):
- 문항은 측정 목표에 정확히 부합해야 함
- 오답 선택지는 그럴듯하지만 명확히 틀려야 함
- 정답이 2개 이상이거나 없는 문항은 금지
- 문화적 편향 요소 배제
- 교육과정 성취기준 연계

## 개선된 프롬프트:
위 비평과 원칙을 반영하여 개선된 프롬프트를 작성하세요.
"""

    # Case library with extended test cases
    case_library = get_extended_case_library()

    return DomainConfig(
        domain_type="english_question",
        domain_name="영어문항생성",
        knowledge=knowledge,
        critique_template=critique_template,
        refinement_template=refinement_template,
        case_library=case_library,
        metadata={
            "version": "2.0.0",
            "author": "PromptWizard English Education Team",
            "last_updated": "2024-01-25",
            "references": [
                "2015 개정 교육과정 영어과",
                "2022 개정 교육과정 영어과",
                "ETS TOEIC/TOEFL 출제 가이드라인",
                "Cambridge English Assessment Guidelines",
                "Bloom's Taxonomy of Educational Objectives",
                "Item Writing Guidelines for Language Testing",
                "CEFR (Common European Framework of Reference)"
            ],
            "question_templates": list(QUESTION_TEMPLATES.keys()),
            "difficulty_levels": list(DIFFICULTY_LEVELS.keys()),
            "achievement_standards": ACHIEVEMENT_STANDARDS
        },
        validators=[
            {
                "type": "KeywordValidator",
                "keywords": ["정답", "선택지", "지문", "문항", "①", "②", "③", "④", "⑤"],
                "must_include": True,
                "min_matches": 2
            },
            {
                "type": "PatternValidator",
                "pattern": r"[①②③④⑤]|[1-5]\)|[A-E]\)",
                "should_match": True,
                "description": "선택지 번호 형식 확인"
            },
            {
                "type": "PatternValidator",
                "pattern": r"(정답|answer|key)\s*[:：]\s*[①②③④⑤1-5A-E]",
                "should_match": True,
                "description": "정답 표시 확인"
            }
        ]
    )


# Pre-configured domain config instance
ENGLISH_QUESTION_DOMAIN_CONFIG = get_english_question_domain_config()

# Export additional utilities
__all__ = [
    "ENGLISH_QUESTION_DOMAIN_CONFIG",
    "get_english_question_domain_config",
    "QUESTION_TEMPLATES",
    "DIFFICULTY_LEVELS",
    "ACHIEVEMENT_STANDARDS",
    "QuestionTemplate",
    "DifficultyLevel",
]
