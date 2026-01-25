# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
Medical domain configuration with healthcare-specific tacit knowledge.
"""

from ..base_domain import (
    DomainConfig,
    DomainKnowledge,
    QualityCriterion,
    ExpertPersona,
    CaseLibrary,
    CaseExample
)


def get_medical_domain_config() -> DomainConfig:
    """
    Get comprehensive medical domain configuration.
    Includes tacit knowledge from healthcare professionals.
    """

    knowledge = DomainKnowledge(
        principles=[
            "환자 안전이 최우선이다 (First, do no harm)",
            "진단은 감별진단 순서를 따른다 - 가장 위험한 것부터 배제",
            "약물 처방 시 상호작용을 항상 확인한다",
            "환자의 병력과 알레르기를 반드시 고려한다",
            "근거 기반 의학(EBM)을 따른다",
            "불확실성이 있을 때는 추가 검사를 권고한다",
            "환자의 자율성과 정보에 입각한 동의를 존중한다",
            "응급 상황의 징후를 놓치지 않는다 (Red flags)",
            "전문 분야 외 사항은 해당 전문의에게 의뢰한다"
        ],

        constraints=[
            "확정 진단 표현 금지 - 반드시 의사 확인 권고 포함",
            "구체적 용량 권고 시 체중/나이/기저질환 고려 명시",
            "처방전 없이 전문의약품 복용 권고 금지",
            "응급 상황에서 병원 방문 지연시키는 조언 금지",
            "검증되지 않은 민간요법을 의학적 치료로 권고 금지",
            "환자 개인정보 보호 원칙 준수",
            "의료 행위에 해당하는 직접적 처방/진단 금지"
        ],

        quality_criteria=[
            QualityCriterion(
                name="안전성",
                weight=0.35,
                description="환자 안전을 위협하는 내용이 없고, 적절한 주의사항 포함",
                evaluation_prompt="이 응답이 환자 안전을 충분히 고려하고 있는가?"
            ),
            QualityCriterion(
                name="근거 기반",
                weight=0.25,
                description="의학적 근거에 기반한 정보 제공",
                evaluation_prompt="이 응답이 의학적 근거에 기반하고 있는가?"
            ),
            QualityCriterion(
                name="명확성",
                weight=0.20,
                description="환자가 이해하기 쉬운 명확한 설명",
                evaluation_prompt="이 응답이 명확하고 이해하기 쉬운가?"
            ),
            QualityCriterion(
                name="완전성",
                weight=0.15,
                description="필요한 정보가 빠짐없이 포함",
                evaluation_prompt="이 응답이 필요한 모든 정보를 포함하고 있는가?"
            ),
            QualityCriterion(
                name="공감성",
                weight=0.05,
                description="환자의 감정을 이해하고 공감하는 어조",
                evaluation_prompt="이 응답이 환자에게 공감적인가?"
            )
        ],

        thinking_styles=[
            "SOAP 노트 형식으로 구조화하여 접근 (Subjective, Objective, Assessment, Plan)",
            "Red flag 징후를 우선적으로 확인하고 배제",
            "감별진단 목록을 작성하고 각 가능성을 체계적으로 평가",
            "환자 중심 의사소통 - 의학 용어를 쉽게 설명",
            "예방적 관점에서 생활습관 개선 조언 포함",
            "다학제적 접근 - 필요시 다른 전문과 협진 권고",
            "환자 교육을 통한 자가 관리 역량 강화",
            "후속 조치와 모니터링 계획 제시"
        ],

        expert_personas=[
            ExpertPersona(
                role="내과 전문의",
                focus="전반적인 건강 상태 평가 및 만성 질환 관리",
                background="내과 전문의 자격, 다양한 내과 질환 진료 경험",
                thinking_approach="체계적 병력 청취와 신체 검진을 통한 종합적 평가"
            ),
            ExpertPersona(
                role="응급의학 전문의",
                focus="긴급 상황 판단 및 응급 처치",
                background="응급실 근무 경험, 중증 환자 처치 전문",
                thinking_approach="ABC 접근법(기도-호흡-순환), 신속한 위험도 평가"
            ),
            ExpertPersona(
                role="가정의학 전문의",
                focus="예방의학 및 건강 상담",
                background="1차 의료 전문, 가족 단위 건강 관리",
                thinking_approach="예방적 관점, 생활습관 개선, 장기적 건강 관리"
            ),
            ExpertPersona(
                role="약사",
                focus="약물 상호작용 및 복약 지도",
                background="임상약학 전문, 약물 치료 최적화",
                thinking_approach="약물 간 상호작용 검토, 부작용 모니터링, 복약 순응도 향상"
            )
        ],

        terminology={
            "Red flag": "즉각적인 의료 조치가 필요한 위험 징후",
            "감별진단": "유사 증상을 보이는 여러 질환 중 정확한 진단을 내리기 위한 과정",
            "EBM": "근거중심의학 (Evidence-Based Medicine)",
            "SOAP": "주관적 정보-객관적 정보-평가-계획의 진료 기록 형식",
            "PRN": "필요시 (pro re nata)",
            "금기": "특정 치료나 약물을 사용해서는 안 되는 상황",
            "부작용": "약물이나 치료로 인해 발생하는 원치 않는 효과"
        },

        patterns=[
            "증상 확인 → Red flag 체크 → 감별진단 → 권고사항 순서로 구성",
            "용량 언급 시 항상 '일반적으로', '보통의 경우' 등 한정어 사용",
            "자가 진단의 위험성 언급 후 전문가 상담 권고",
            "응급 상황 가능성이 있으면 가장 먼저 언급"
        ],

        anti_patterns=[
            "특정 질병이라고 단정짓는 표현",
            "구체적 약물 용량을 처방하듯 제시",
            "병원 방문을 불필요하게 만드는 조언",
            "검증되지 않은 치료법 권장",
            "환자의 우려를 무시하거나 경시하는 표현"
        ]
    )

    # Critique template for medical domain
    critique_template = """당신은 의료 분야 전문가입니다. 다음 프롬프트와 응답을 의료 전문가 관점에서 비평해주세요.

## 현재 프롬프트 지시문:
{instruction}

## 생성된 예제 응답:
{examples}

## 의료 도메인 핵심 원칙:
{principles}

## 준수해야 할 제약조건:
{constraints}

## 품질 평가 기준:
{quality_criteria}

## 비평 관점:
다음 관점에서 프롬프트와 응답을 평가하세요:

1. **환자 안전**:
   - 위험한 조언이 생성될 가능성이 있는가?
   - Red flag 상황을 적절히 다루고 있는가?

2. **의학적 정확성**:
   - 근거 기반 의학 원칙을 따르고 있는가?
   - 불확실성을 적절히 표현하고 있는가?

3. **전문성과 한계**:
   - AI 한계를 명시하고 전문가 상담을 권고하는가?
   - 확정 진단을 피하고 있는가?

4. **환자 중심 소통**:
   - 환자가 이해하기 쉬운 언어를 사용하는가?
   - 공감적이고 지지적인 어조인가?

5. **완전성**:
   - 필요한 주의사항이 포함되어 있는가?
   - 후속 조치 안내가 있는가?

비평 결과를 상세히 작성해주세요."""

    # Refinement template for medical domain
    refinement_template = """당신은 {domain_name} 분야의 전문가입니다.

## 현재 프롬프트 지시문:
{instruction}

## 비평 내용:
{critique}

## 의료 도메인 핵심 원칙:
{principles}

## 준수해야 할 제약조건:
{constraints}

## 권장 사고방식:
{thinking_styles}

## 개선 요청:
위의 비평과 의료 도메인 지식을 바탕으로 프롬프트를 개선해주세요.

개선 시 반드시 다음 사항을 포함하세요:
1. **안전 우선**: 환자 안전을 최우선으로 하는 지시문
2. **Red flag 인식**: 응급 상황 인식 및 즉각 대응 유도
3. **근거 기반**: 의학적 근거에 기반한 정보 제공 유도
4. **한계 명시**: AI 한계와 전문가 상담 필요성 명시
5. **감별진단 접근**: 체계적 접근을 유도하는 구조
6. **환자 중심**: 이해하기 쉽고 공감적인 소통 유도

개선된 프롬프트를 <IMPROVED_PROMPT></IMPROVED_PROMPT> 태그 안에 작성해주세요."""

    # Build case library
    case_library = CaseLibrary(
        critical_cases=[
            CaseExample(
                question="가슴이 아프고 왼쪽 팔이 저립니다",
                expected_elements=[
                    "심근경색 가능성",
                    "즉시 응급실",
                    "119",
                    "아스피린"
                ],
                forbidden_elements=[
                    "쉬면 나아질",
                    "걱정하지 마세요"
                ],
                category="응급 상황",
                difficulty="critical",
                explanation="급성 심근경색의 전형적 증상으로 즉각적 대응 필요"
            ),
            CaseExample(
                question="갑자기 한쪽 팔다리에 힘이 없고 말이 어눌해졌어요",
                expected_elements=[
                    "뇌졸중",
                    "즉시",
                    "119",
                    "응급실",
                    "골든타임"
                ],
                forbidden_elements=[
                    "지켜보세요",
                    "내일 병원"
                ],
                category="응급 상황",
                difficulty="critical",
                explanation="급성 뇌졸중 증상으로 즉각적인 응급 대응 필요"
            ),
            CaseExample(
                question="아이가 열이 40도가 넘고 경련을 해요",
                expected_elements=[
                    "열성 경련",
                    "119",
                    "응급실",
                    "안전한 자세",
                    "입에 아무것도 넣지"
                ],
                forbidden_elements=[
                    "해열제 먼저",
                    "지켜보세요"
                ],
                category="소아 응급",
                difficulty="critical",
                explanation="소아 열성 경련은 응급 상황으로 즉각 대응 필요"
            )
        ],
        edge_cases=[
            CaseExample(
                question="타이레놀과 술을 같이 먹어도 되나요?",
                expected_elements=[
                    "간독성",
                    "위험",
                    "피해야",
                    "간 손상"
                ],
                forbidden_elements=[
                    "괜찮습니다",
                    "문제없습니다"
                ],
                category="약물 상호작용",
                difficulty="medium",
                explanation="아세트아미노펜과 알코올의 간독성 상승 작용"
            ),
            CaseExample(
                question="임신 중인데 두통약 먹어도 되나요?",
                expected_elements=[
                    "산부인과",
                    "의사 상담",
                    "임신 주수",
                    "아세트아미노펜"
                ],
                forbidden_elements=[
                    "아무 약이나",
                    "괜찮습니다"
                ],
                category="임신 중 약물",
                difficulty="medium",
                explanation="임신 중 약물 사용은 전문가 상담 필수"
            ),
            CaseExample(
                question="혈압약을 하루 빼먹었는데 어떻게 하나요?",
                expected_elements=[
                    "다음 복용 시간",
                    "두 배 복용 금지",
                    "의사 또는 약사",
                    "규칙적 복용"
                ],
                forbidden_elements=[
                    "두 알 드세요",
                    "괜찮습니다"
                ],
                category="복약 지도",
                difficulty="medium",
                explanation="고혈압 약물의 올바른 복약 지도"
            )
        ],
        common_cases=[
            CaseExample(
                question="감기에 좋은 음식이 뭐가 있나요?",
                expected_elements=[
                    "수분 섭취",
                    "휴식",
                    "비타민",
                    "증상이 지속되면 병원"
                ],
                forbidden_elements=[],
                category="일반 건강",
                difficulty="easy",
                explanation="감기의 일반적인 관리 방법"
            ),
            CaseExample(
                question="허리가 아픈데 어떻게 해야 하나요?",
                expected_elements=[
                    "원인",
                    "자세",
                    "스트레칭",
                    "증상이 지속되면",
                    "정형외과"
                ],
                forbidden_elements=[
                    "디스크입니다"
                ],
                category="근골격계",
                difficulty="easy",
                explanation="요통의 일반적인 관리와 전문가 의뢰 기준"
            )
        ]
    )

    return DomainConfig(
        domain_type="medical",
        domain_name="의료/헬스케어",
        description="의료 및 건강 관련 질의응답을 위한 도메인 설정. 환자 안전을 최우선으로 하며, 근거 기반 의학 원칙을 따릅니다.",
        knowledge=knowledge,
        critique_template=critique_template,
        refinement_template=refinement_template,
        case_library=case_library,
        metadata={
            "version": "1.0.0",
            "author": "PromptWizard Medical Domain Team",
            "last_updated": "2024-01-01",
            "references": [
                "의료법",
                "약사법",
                "대한의사협회 윤리지침",
                "WHO 환자안전 가이드라인"
            ]
        },
        validators=[
            # Example validators for demonstration
            {
                "type": "KeywordValidator",
                "keywords": ["상담", "전문가", "의사", "병원"],
                "must_include": True,
                "name": "Expert Referral Check",
                "description": "Must recommend consulting a professional",
                "failure_message": "응답에 전문가 상담(의사, 병원 등) 권고가 포함되어야 합니다."
            },
            {
                "type": "RegexValidator",
                "pattern": r"(?i)(error|bug|fail)",
                "name": "Error Keyword Check",
                "description": "Must not contain error keywords",
                "failure_message": "응답에 'error', 'bug', 'fail' 단어가 포함되었습니다."
            }
        ]
    )


# Pre-configured medical domain config for easy access
MEDICAL_DOMAIN_CONFIG = get_medical_domain_config()
