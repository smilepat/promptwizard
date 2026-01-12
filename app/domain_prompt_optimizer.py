"""
Domain-Aware Prompt Optimization App
도메인 특화 프롬프트 최적화 웹 애플리케이션

Usage:
    streamlit run app/domain_prompt_optimizer.py
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from promptwizard.glue.promptopt.domains import (
    DomainConfig,
    DomainKnowledge,
    DomainRegistry,
    QualityCriterion,
    ExpertPersona,
    CaseExample,
    CaseLibrary,
    DomainAwarePromptOptimizer,
    create_domain_optimizer,
    MEDICAL_DOMAIN_CONFIG,
    LEGAL_DOMAIN_CONFIG,
    FINANCE_DOMAIN_CONFIG,
)

# Page configuration
st.set_page_config(
    page_title="Domain-Aware Prompt Optimizer",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .domain-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1E88E5;
    }
    .metric-card {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .score-high { color: #4CAF50; font-weight: bold; }
    .score-medium { color: #FF9800; font-weight: bold; }
    .score-low { color: #f44336; font-weight: bold; }
    .constraint-box {
        background-color: #fff3e0;
        border-radius: 5px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #FF9800;
    }
    .principle-box {
        background-color: #e8f5e9;
        border-radius: 5px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)


def get_domain_config(domain_type: str) -> DomainConfig:
    """Get domain configuration by type."""
    configs = {
        "medical": MEDICAL_DOMAIN_CONFIG,
        "legal": LEGAL_DOMAIN_CONFIG,
        "finance": FINANCE_DOMAIN_CONFIG
    }
    return configs.get(domain_type)


def render_header():
    """Render app header."""
    st.markdown('<p class="main-header">🧙 Domain-Aware Prompt Optimizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">도메인 암묵지를 반영한 프롬프트 최적화 시스템</p>', unsafe_allow_html=True)


def render_domain_selector():
    """Render domain selection sidebar."""
    st.sidebar.header("🎯 도메인 선택")

    domain_options = {
        "medical": "🏥 의료/헬스케어",
        "legal": "⚖️ 법률",
        "finance": "💰 금융/투자"
    }

    selected_domain = st.sidebar.selectbox(
        "도메인 유형",
        options=list(domain_options.keys()),
        format_func=lambda x: domain_options[x]
    )

    return selected_domain


def render_domain_info(config: DomainConfig):
    """Render domain information panel."""
    st.header(f"📋 {config.domain_name} 도메인 정보")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("핵심 원칙", f"{len(config.knowledge.principles)}개")
    with col2:
        st.metric("제약조건", f"{len(config.knowledge.constraints)}개")
    with col3:
        st.metric("품질 기준", f"{len(config.knowledge.quality_criteria)}개")

    # Tabs for different info sections
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 핵심 원칙", "🚫 제약조건", "📊 품질 기준", "🧠 사고방식"])

    with tab1:
        for i, principle in enumerate(config.knowledge.principles, 1):
            st.markdown(f'<div class="principle-box">{i}. {principle}</div>', unsafe_allow_html=True)

    with tab2:
        for i, constraint in enumerate(config.knowledge.constraints, 1):
            st.markdown(f'<div class="constraint-box">{i}. {constraint}</div>', unsafe_allow_html=True)

    with tab3:
        for qc in config.knowledge.quality_criteria:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{qc.name}**: {qc.description}")
            with col_b:
                st.progress(qc.weight)
                st.caption(f"가중치: {int(qc.weight * 100)}%")

    with tab4:
        for i, style in enumerate(config.knowledge.thinking_styles, 1):
            st.info(f"{i}. {style}")


def render_prompt_input():
    """Render prompt input section."""
    st.header("✍️ 프롬프트 입력")

    col1, col2 = st.columns(2)

    with col1:
        task_description = st.text_area(
            "작업 설명 (Task Description)",
            placeholder="예: 환자의 증상에 대해 의학적 정보를 제공하는 AI 어시스턴트입니다.",
            height=100
        )

    with col2:
        base_instruction = st.text_area(
            "기본 지시문 (Base Instruction)",
            placeholder="예: 환자의 질문에 정확하고 안전한 의학 정보를 제공하세요.",
            height=100
        )

    answer_format = st.text_input(
        "답변 형식 지정",
        placeholder="예: 답변 마지막에 <ANS_START>최종답변<ANS_END> 형식으로 작성하세요."
    )

    return task_description, base_instruction, answer_format


def render_test_case_section(config: DomainConfig):
    """Render test case section."""
    st.header("🧪 테스트 케이스")

    all_cases = config.case_library.get_all_cases()

    if not all_cases:
        st.info("등록된 테스트 케이스가 없습니다.")
        return None

    case_options = {f"{c.category}: {c.question[:50]}...": c for c in all_cases}

    selected_case_key = st.selectbox(
        "테스트 케이스 선택",
        options=list(case_options.keys())
    )

    if selected_case_key:
        selected_case = case_options[selected_case_key]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 질문")
            st.write(selected_case.question)

            st.subheader("✅ 기대 요소")
            for elem in selected_case.expected_elements:
                st.success(f"• {elem}")

        with col2:
            st.subheader("ℹ️ 정보")
            st.write(f"**카테고리:** {selected_case.category}")
            st.write(f"**난이도:** {selected_case.difficulty}")

            if selected_case.forbidden_elements:
                st.subheader("❌ 금지 요소")
                for elem in selected_case.forbidden_elements:
                    st.error(f"• {elem}")

        return selected_case

    return None


def evaluate_response(optimizer: DomainAwarePromptOptimizer, response: str, question: str = ""):
    """Evaluate response using domain evaluator."""
    scores = optimizer.evaluate_response(response, question=question)
    return scores


def render_evaluation_results(scores: dict):
    """Render evaluation results."""
    st.header("📊 평가 결과")

    # Overall score
    overall = scores.get('overall', 0)

    if overall >= 0.7:
        score_class = "score-high"
        emoji = "✅"
    elif overall >= 0.4:
        score_class = "score-medium"
        emoji = "⚠️"
    else:
        score_class = "score-low"
        emoji = "❌"

    st.markdown(f"""
    <div class="metric-card">
        <h2>{emoji} 종합 점수</h2>
        <h1 class="{score_class}">{int(overall * 100)}%</h1>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Individual scores
    cols = st.columns(len(scores) - 1)  # Exclude 'overall'

    i = 0
    for metric, score in scores.items():
        if metric == 'overall':
            continue

        with cols[i % len(cols)]:
            score_pct = int(score * 100)
            st.metric(
                label=metric,
                value=f"{score_pct}%",
                delta=f"{score_pct - 50}%" if score_pct != 50 else None
            )
        i += 1


def render_enhanced_prompt(optimizer: DomainAwarePromptOptimizer, base_instruction: str):
    """Render enhanced prompt."""
    st.header("🚀 강화된 프롬프트")

    enhanced = optimizer.enhance_base_instruction(base_instruction)

    st.code(enhanced, language="markdown")

    # Copy button
    if st.button("📋 복사"):
        st.write("프롬프트가 클립보드에 복사되었습니다!")
        st.session_state['copied_prompt'] = enhanced


def render_critique_section(optimizer: DomainAwarePromptOptimizer, instruction: str, response: str):
    """Render critique generation section."""
    st.header("📝 도메인 비평 생성")

    if st.button("비평 생성"):
        with st.spinner("도메인 지식 기반 비평 생성 중..."):
            critique_prompt = optimizer.generate_domain_critique(
                instruction=instruction,
                examples=response
            )

            st.subheader("생성된 비평 프롬프트")
            st.code(critique_prompt, language="markdown")


def render_case_validation(optimizer: DomainAwarePromptOptimizer, response: str, case: CaseExample):
    """Render case validation results."""
    st.header("🔍 케이스 검증 결과")

    response_lower = response.lower()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ 기대 요소 체크")
        found_count = 0
        for elem in case.expected_elements:
            if elem.lower() in response_lower:
                st.success(f"✓ {elem}")
                found_count += 1
            else:
                st.warning(f"✗ {elem}")

        if case.expected_elements:
            st.metric("발견율", f"{found_count}/{len(case.expected_elements)}")

    with col2:
        st.subheader("❌ 금지 요소 체크")
        violation_count = 0
        for elem in case.forbidden_elements:
            if elem.lower() in response_lower:
                st.error(f"⚠️ 위반: {elem}")
                violation_count += 1
            else:
                st.success(f"✓ 미포함: {elem}")

        if case.forbidden_elements:
            st.metric("위반 수", f"{violation_count}/{len(case.forbidden_elements)}")


def render_custom_domain_editor():
    """Render custom domain configuration editor."""
    st.header("🛠️ 커스텀 도메인 설정")

    with st.expander("새 도메인 설정 만들기"):
        domain_name = st.text_input("도메인 이름", placeholder="예: 교육/학습")
        domain_type = st.text_input("도메인 타입", placeholder="예: education")

        st.subheader("핵심 원칙")
        principles = st.text_area(
            "원칙 목록 (줄바꿈으로 구분)",
            placeholder="학습자 중심 교육\n단계적 난이도 조절\n..."
        )

        st.subheader("제약조건")
        constraints = st.text_area(
            "제약조건 목록 (줄바꿈으로 구분)",
            placeholder="오답을 정답으로 제시 금지\n..."
        )

        if st.button("도메인 설정 생성"):
            if domain_name and domain_type:
                principles_list = [p.strip() for p in principles.split('\n') if p.strip()]
                constraints_list = [c.strip() for c in constraints.split('\n') if c.strip()]

                custom_config = DomainConfig(
                    domain_type=domain_type,
                    domain_name=domain_name,
                    knowledge=DomainKnowledge(
                        principles=principles_list,
                        constraints=constraints_list
                    )
                )

                st.session_state['custom_domain'] = custom_config
                st.success(f"'{domain_name}' 도메인 설정이 생성되었습니다!")

                # Show generated config
                st.json(custom_config.to_dict())


def main():
    """Main app function."""
    render_header()

    # Sidebar
    selected_domain = render_domain_selector()

    # Get domain config
    config = get_domain_config(selected_domain)

    if not config:
        st.error("도메인 설정을 불러올 수 없습니다.")
        return

    # Create optimizer
    try:
        optimizer = create_domain_optimizer(selected_domain)
    except Exception as e:
        st.error(f"최적화기 생성 실패: {e}")
        optimizer = DomainAwarePromptOptimizer(domain_config=config)

    # Main content tabs
    main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
        "📋 도메인 정보",
        "✍️ 프롬프트 최적화",
        "🧪 응답 평가",
        "🛠️ 커스텀 도메인"
    ])

    with main_tab1:
        render_domain_info(config)

    with main_tab2:
        task_desc, base_inst, ans_format = render_prompt_input()

        if base_inst:
            st.divider()
            render_enhanced_prompt(optimizer, base_inst)

            # Expert prompt
            st.subheader("👤 전문가 페르소나")
            expert_prompt = optimizer.get_domain_expert_prompt()
            st.code(expert_prompt, language="markdown")

    with main_tab3:
        st.subheader("📝 응답 입력")
        test_response = st.text_area(
            "평가할 응답",
            placeholder="AI가 생성한 응답을 입력하세요...",
            height=200
        )

        # Test case selection
        selected_case = render_test_case_section(config)

        if test_response:
            st.divider()

            # Evaluate response
            question = selected_case.question if selected_case else ""
            scores = evaluate_response(optimizer, test_response, question)
            render_evaluation_results(scores)

            # Case validation if case selected
            if selected_case:
                st.divider()
                render_case_validation(optimizer, test_response, selected_case)

    with main_tab4:
        render_custom_domain_editor()

    # Sidebar additional info
    st.sidebar.divider()
    st.sidebar.header("📖 사용 가이드")
    st.sidebar.markdown("""
    1. **도메인 선택**: 최적화할 도메인 선택
    2. **도메인 정보**: 암묵지 및 제약조건 확인
    3. **프롬프트 최적화**: 기본 지시문 입력 및 강화
    4. **응답 평가**: AI 응답의 도메인 적합성 평가
    5. **커스텀 도메인**: 새로운 도메인 설정 생성
    """)

    st.sidebar.divider()
    st.sidebar.info("🧙 PromptWizard Domain Extension v1.0")


if __name__ == "__main__":
    main()
