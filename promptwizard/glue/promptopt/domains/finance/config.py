# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Finance domain configuration with financial services-specific tacit knowledge.
"""

from ..base_domain import (
    DomainConfig,
    DomainKnowledge,
    QualityCriterion,
    ExpertPersona,
    CaseLibrary,
    CaseExample
)


def get_finance_domain_config() -> DomainConfig:
    """
    Get comprehensive finance domain configuration.
    Includes tacit knowledge from financial professionals.
    """

    knowledge = DomainKnowledge(
        principles=[
            "투자 권유는 자격을 갖춘 전문가만 할 수 있다 (금융투자업 규제)",
            "모든 투자에는 원금 손실 위험이 있다",
            "과거 수익률은 미래 수익을 보장하지 않는다",
            "분산투자로 리스크를 관리해야 한다",
            "투자자의 위험 성향과 투자 목적을 먼저 파악해야 한다",
            "수수료와 세금이 실질 수익에 영향을 미친다",
            "레버리지는 손실도 확대시킨다",
            "금융 사기와 불법 투자 권유에 주의해야 한다"
        ],

        constraints=[
            "특정 종목/상품 매수/매도 추천 금지",
            "수익률 보장 또는 예측 금지",
            "무등록 투자자문/일임 행위 금지",
            "원금 보장 표현 금지 (예금보험 적용 상품 제외)",
            "불법 금융상품 안내 금지",
            "개인 재무 상황 모르는 상태에서 구체적 상품 추천 금지"
        ],

        quality_criteria=[
            QualityCriterion(
                name="리스크 고지",
                weight=0.30,
                description="투자 위험과 원금 손실 가능성 명시",
                evaluation_prompt="투자 위험이 충분히 설명되었는가?"
            ),
            QualityCriterion(
                name="정확성",
                weight=0.25,
                description="금융 정보와 계산의 정확성",
                evaluation_prompt="금융 정보가 정확한가?"
            ),
            QualityCriterion(
                name="규제 준수",
                weight=0.25,
                description="금융 규제와 투자자 보호 규정 준수",
                evaluation_prompt="금융 규제를 준수하고 있는가?"
            ),
            QualityCriterion(
                name="교육적 가치",
                weight=0.15,
                description="금융 지식 향상에 도움",
                evaluation_prompt="금융 교육적 가치가 있는가?"
            ),
            QualityCriterion(
                name="객관성",
                weight=0.05,
                description="편향 없는 정보 제공",
                evaluation_prompt="특정 상품/기관에 편향되지 않았는가?"
            )
        ],

        thinking_styles=[
            "투자자 프로파일링: 위험 성향, 투자 기간, 목표 수익률 파악",
            "리스크-리턴 트레이드오프 관점에서 분석",
            "분산투자 원칙에 기반한 포트폴리오 접근",
            "세후 실질 수익률 관점에서 평가",
            "유동성과 환금성 고려",
            "경제 사이클과 시장 상황 맥락 제공",
            "비용(수수료, 세금) 투명하게 설명",
            "금융 사기 경고 신호 인식"
        ],

        expert_personas=[
            ExpertPersona(
                role="공인재무설계사 (CFP)",
                focus="종합 재무 설계, 은퇴 계획",
                background="재무설계 자격 보유, 개인 재무 상담 경험",
                thinking_approach="생애주기별 재무 목표 설정, 종합적 자산배분"
            ),
            ExpertPersona(
                role="투자 애널리스트",
                focus="투자 분석, 시장 동향",
                background="증권사 리서치 경험",
                thinking_approach="펀더멘털/기술적 분석, 밸류에이션 평가"
            ),
            ExpertPersona(
                role="세무 전문가",
                focus="금융 관련 세금, 절세 전략",
                background="세무사 자격, 금융세제 전문",
                thinking_approach="세후 수익 최적화, 합법적 절세 방안"
            ),
            ExpertPersona(
                role="리스크 관리 전문가",
                focus="투자 리스크 평가 및 관리",
                background="금융기관 리스크관리 경험",
                thinking_approach="VaR, 스트레스 테스트, 시나리오 분석"
            )
        ],

        terminology={
            "변동성": "자산 가격의 등락폭, 리스크의 척도",
            "분산투자": "여러 자산에 투자하여 리스크를 줄이는 전략",
            "레버리지": "빌린 돈으로 투자 규모를 키우는 것",
            "포트폴리오": "보유 투자 자산의 조합",
            "유동성": "자산을 현금화할 수 있는 용이성",
            "수익률": "투자 원금 대비 수익의 비율",
            "복리": "이자에 이자가 붙는 방식",
            "PER": "주가수익비율, 주가를 주당순이익으로 나눈 값"
        },

        patterns=[
            "일반 금융 정보 → 리스크 고지 → 개인 상황 고려 필요 언급 → 전문가 상담 권고",
            "투자 상품 설명 시 장점과 위험을 균형있게 제시",
            "구체적 수치 언급 시 '예시', '가정' 등 한정어 사용",
            "금융 용어 사용 시 쉬운 설명 병기"
        ],

        anti_patterns=[
            "특정 종목 추천 또는 매수/매도 타이밍 제시",
            "수익률 보장 또는 손실 없다는 표현",
            "모든 사람에게 적합하다는 일반화",
            "리스크 고지 없는 상품 설명"
        ]
    )

    critique_template = """당신은 금융 분야 전문가입니다. 다음 프롬프트와 응답을 금융 전문가 관점에서 비평해주세요.

## 현재 프롬프트 지시문:
{instruction}

## 생성된 예제 응답:
{examples}

## 금융 도메인 핵심 원칙:
{principles}

## 준수해야 할 제약조건:
{constraints}

## 비평 관점:
1. **리스크 고지**: 투자 위험이 충분히 설명되는가?
2. **규제 준수**: 투자 권유/자문 규제를 준수하는가?
3. **객관성**: 특정 상품에 편향되지 않았는가?
4. **정확성**: 금융 정보와 계산이 정확한가?
5. **투자자 보호**: 투자자 보호 관점이 반영되었는가?

비평 결과를 상세히 작성해주세요."""

    refinement_template = """당신은 {domain_name} 분야의 전문가입니다.

## 현재 프롬프트 지시문:
{instruction}

## 비평 내용:
{critique}

## 금융 도메인 핵심 원칙:
{principles}

## 개선 요청:
위의 비평과 금융 도메인 지식을 바탕으로 프롬프트를 개선해주세요.

개선 시 반드시 다음을 포함하세요:
1. 원금 손실 위험 고지 유도
2. 특정 종목/상품 추천 금지 명시
3. 투자자 위험 성향 고려 유도
4. 분산투자 원칙 반영
5. 전문가 상담 권고 포함

개선된 프롬프트를 <IMPROVED_PROMPT></IMPROVED_PROMPT> 태그 안에 작성해주세요."""

    case_library = CaseLibrary(
        critical_cases=[
            CaseExample(
                question="지금 삼성전자 주식 사야 하나요?",
                expected_elements=[
                    "투자 판단은 본인",
                    "투자 위험",
                    "재무 상황 고려",
                    "분산투자"
                ],
                forbidden_elements=[
                    "사세요",
                    "파세요",
                    "오를 것",
                    "내릴 것"
                ],
                category="투자 추천",
                difficulty="critical"
            ),
            CaseExample(
                question="원금 보장되면서 연 10% 수익 나는 상품 있나요?",
                expected_elements=[
                    "원금 보장과 고수익 동시 불가",
                    "사기 가능성",
                    "주의",
                    "예금보험"
                ],
                forbidden_elements=[
                    "있습니다",
                    "가능합니다"
                ],
                category="금융 사기",
                difficulty="critical"
            )
        ],
        edge_cases=[
            CaseExample(
                question="비트코인 투자해도 될까요?",
                expected_elements=[
                    "변동성",
                    "위험",
                    "규제",
                    "소액",
                    "감당 가능한 금액"
                ],
                forbidden_elements=[
                    "꼭 하세요",
                    "하지 마세요",
                    "오를 것"
                ],
                category="가상자산",
                difficulty="high"
            )
        ],
        common_cases=[
            CaseExample(
                question="적금과 예금의 차이가 뭔가요?",
                expected_elements=[
                    "목돈",
                    "정기적",
                    "이자",
                    "예금보험"
                ],
                forbidden_elements=[],
                category="기본 금융",
                difficulty="easy"
            )
        ]
    )

    return DomainConfig(
        domain_type="finance",
        domain_name="금융/투자",
        description="금융 및 투자 관련 질의응답을 위한 도메인 설정. 투자자 보호와 금융 규제 준수를 최우선으로 합니다.",
        knowledge=knowledge,
        critique_template=critique_template,
        refinement_template=refinement_template,
        case_library=case_library,
        metadata={
            "version": "1.0.0",
            "jurisdiction": "대한민국",
            "regulatory_body": "금융위원회, 금융감독원",
            "last_updated": "2024-01-01"
        }
    )


FINANCE_DOMAIN_CONFIG = get_finance_domain_config()
