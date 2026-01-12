# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Legal domain configuration with law-specific tacit knowledge.
"""

from ..base_domain import (
    DomainConfig,
    DomainKnowledge,
    QualityCriterion,
    ExpertPersona,
    CaseLibrary,
    CaseExample
)


def get_legal_domain_config() -> DomainConfig:
    """
    Get comprehensive legal domain configuration.
    Includes tacit knowledge from legal professionals.
    """

    knowledge = DomainKnowledge(
        principles=[
            "법률 조언은 변호사만 제공할 수 있다 (변호사법 준수)",
            "모든 법적 판단은 구체적 사실관계에 따라 달라진다",
            "법령은 시간에 따라 개정되므로 최신 법령 확인 필요",
            "판례는 구속력이 있으나 사안에 따라 적용이 다를 수 있다",
            "법적 권리와 의무는 계약, 법령, 판례에 근거한다",
            "소멸시효와 제척기간을 항상 확인해야 한다",
            "관할권과 적용 법률을 먼저 확인해야 한다",
            "법적 분쟁은 협의, 조정, 소송 순서로 해결을 고려한다"
        ],

        constraints=[
            "법률 자문 제공 금지 - 일반적 법률 정보 제공만 가능",
            "특정 사안에 대한 승소 가능성 예측 금지",
            "변호사 선임 없이 진행 가능하다는 조언 금지 (복잡한 사안)",
            "최종 법적 판단을 내리는 표현 금지",
            "오래된 법령/판례를 현행법처럼 안내 금지",
            "상대방에게 불이익을 주는 불법적 조언 금지"
        ],

        quality_criteria=[
            QualityCriterion(
                name="법적 정확성",
                weight=0.35,
                description="현행 법령과 판례에 부합하는 정보",
                evaluation_prompt="이 응답이 현행 법령에 정확한가?"
            ),
            QualityCriterion(
                name="한계 명시",
                weight=0.25,
                description="법률 정보의 한계와 전문가 상담 필요성 명시",
                evaluation_prompt="법률 정보의 한계가 명확히 설명되었는가?"
            ),
            QualityCriterion(
                name="실용성",
                weight=0.20,
                description="실제 상황에 적용 가능한 실용적 정보",
                evaluation_prompt="이 정보가 실제로 도움이 되는가?"
            ),
            QualityCriterion(
                name="명확성",
                weight=0.15,
                description="법률 용어를 쉽게 설명",
                evaluation_prompt="비전문가가 이해할 수 있는가?"
            ),
            QualityCriterion(
                name="중립성",
                weight=0.05,
                description="편향 없는 객관적 정보 제공",
                evaluation_prompt="특정 입장에 편향되지 않았는가?"
            )
        ],

        thinking_styles=[
            "IRAC 방식 적용: 쟁점(Issue) → 규정(Rule) → 적용(Application) → 결론(Conclusion)",
            "관련 법령과 판례를 먼저 확인한 후 사안에 적용",
            "시효, 기간, 관할 등 절차적 요건을 먼저 검토",
            "당사자들의 권리와 의무를 균형있게 분석",
            "예상되는 법적 리스크와 대응 방안 제시",
            "협의/조정/소송 등 분쟁해결 단계별 접근",
            "증거 확보와 문서화의 중요성 강조"
        ],

        expert_personas=[
            ExpertPersona(
                role="민사 전문 변호사",
                focus="계약, 손해배상, 부동산 분쟁",
                background="민사소송 다수 수행 경험",
                thinking_approach="당사자 간 권리의무 관계 분석, 입증책임 검토"
            ),
            ExpertPersona(
                role="형사 전문 변호사",
                focus="형사 사건 변호, 고소/고발",
                background="검찰 및 법원 실무 경험",
                thinking_approach="구성요건 해당성, 위법성, 책임 순차 검토"
            ),
            ExpertPersona(
                role="노동법 전문가",
                focus="근로관계, 해고, 임금",
                background="노동위원회 및 법원 사건 처리",
                thinking_approach="근로기준법 적용, 근로자 보호 원칙"
            ),
            ExpertPersona(
                role="가사 전문 변호사",
                focus="이혼, 양육권, 상속",
                background="가정법원 사건 전문",
                thinking_approach="가족관계 법률 적용, 자녀 최선의 이익"
            )
        ],

        terminology={
            "소멸시효": "권리를 행사할 수 있는 기간이 지나 권리가 소멸하는 것",
            "제척기간": "권리 자체가 존속하는 기간, 중단/정지 불가",
            "내용증명": "발송 내용과 일자를 우체국이 증명하는 우편",
            "가처분": "본안 소송 전 권리를 임시로 보전하는 절차",
            "항변": "상대방 주장을 배척하는 방어 방법",
            "구상권": "타인의 채무를 대신 변제한 자가 그 타인에게 상환을 청구할 권리"
        },

        patterns=[
            "법적 쟁점 파악 → 관련 법령 설명 → 일반적 판례 경향 → 전문가 상담 권고",
            "기간/시효 관련 사항은 반드시 먼저 언급",
            "법률 용어 사용 시 괄호 안에 쉬운 설명 병기",
            "복잡한 사안일수록 변호사 상담 필요성 강조"
        ],

        anti_patterns=[
            "특정 결과를 보장하는 표현",
            "변호사 없이 충분히 해결 가능하다는 조언",
            "법원이나 상대방의 판단을 예단하는 표현",
            "불법적인 방법을 암시하는 조언"
        ]
    )

    critique_template = """당신은 법률 분야 전문가입니다. 다음 프롬프트와 응답을 법률 전문가 관점에서 비평해주세요.

## 현재 프롬프트 지시문:
{instruction}

## 생성된 예제 응답:
{examples}

## 법률 도메인 핵심 원칙:
{principles}

## 준수해야 할 제약조건:
{constraints}

## 비평 관점:
1. **법적 정확성**: 현행 법령과 판례에 부합하는가?
2. **한계 명시**: 법률 정보와 법률 자문의 차이가 명확한가?
3. **절차적 안내**: 시효, 관할 등 절차적 사항이 포함되었는가?
4. **실용성**: 실제 도움이 되는 정보를 제공하는가?
5. **전문가 연계**: 적절히 변호사 상담을 권고하는가?

비평 결과를 상세히 작성해주세요."""

    refinement_template = """당신은 {domain_name} 분야의 전문가입니다.

## 현재 프롬프트 지시문:
{instruction}

## 비평 내용:
{critique}

## 법률 도메인 핵심 원칙:
{principles}

## 개선 요청:
위의 비평과 법률 도메인 지식을 바탕으로 프롬프트를 개선해주세요.

개선 시 반드시 다음을 포함하세요:
1. 법률 정보 제공의 한계 명시
2. IRAC 방식의 체계적 분석 유도
3. 시효/기간/관할 확인 유도
4. 전문가 상담 권고 포함
5. 법률 용어의 쉬운 설명 유도

개선된 프롬프트를 <IMPROVED_PROMPT></IMPROVED_PROMPT> 태그 안에 작성해주세요."""

    case_library = CaseLibrary(
        critical_cases=[
            CaseExample(
                question="회사에서 부당해고 당했는데 어떻게 해야 하나요?",
                expected_elements=[
                    "부당해고 구제신청",
                    "노동위원회",
                    "3개월",
                    "해고 통보서",
                    "증거 확보"
                ],
                forbidden_elements=[
                    "100% 이길 수 있습니다",
                    "변호사 없이도"
                ],
                category="노동법",
                difficulty="medium"
            ),
            CaseExample(
                question="교통사고 합의금 얼마나 받을 수 있나요?",
                expected_elements=[
                    "과실 비율",
                    "진단서",
                    "치료비",
                    "위자료",
                    "보험사"
                ],
                forbidden_elements=[
                    "정확히 얼마",
                    "받을 수 있습니다"
                ],
                category="손해배상",
                difficulty="medium"
            )
        ],
        edge_cases=[
            CaseExample(
                question="채무자가 돈을 안 갚는데 소멸시효가 언제인가요?",
                expected_elements=[
                    "10년",
                    "3년",
                    "상사",
                    "시효 중단",
                    "내용증명"
                ],
                forbidden_elements=[],
                category="채권",
                difficulty="medium"
            )
        ],
        common_cases=[]
    )

    return DomainConfig(
        domain_type="legal",
        domain_name="법률",
        description="법률 관련 질의응답을 위한 도메인 설정. 법률 정보 제공과 법률 자문의 경계를 준수합니다.",
        knowledge=knowledge,
        critique_template=critique_template,
        refinement_template=refinement_template,
        case_library=case_library,
        metadata={
            "version": "1.0.0",
            "jurisdiction": "대한민국",
            "last_updated": "2024-01-01"
        }
    )


LEGAL_DOMAIN_CONFIG = get_legal_domain_config()
