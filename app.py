import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="AI 행사장 설계 디자이너", page_icon="🎪", layout="wide")

st.title("🎪 AI 행사장 설계 디자이너")
st.markdown("행사의 기본 정보를 입력하면 최적의 공간 배치, 혼잡도 시뮬레이션, 그리고 모두를 위한 유니버설 설계도를 제안합니다.")

# 사이드바: 사용자 입력 폼
with st.sidebar:
    st.header("📋 행사 기본 정보 입력")
    event_type = st.selectbox("행사 유형", ["컨퍼런스/학술대회", "공연/콘서트", "전시회", "네트워킹 파티", "지역 축제", "기타"])
    attendees = st.number_input("예상 인원수 (명)", min_value=10, max_value=50000, step=50, value=500)
    duration = st.slider("진행 시간 (시간)", min_value=1, max_value=24, value=4)
    atmosphere = st.selectbox("원하는 분위기", ["차분하고 전문적인", "활기차고 신나는", "고급스럽고 우아한", "자유롭고 창의적인"])
    extra_req = st.text_area("추가 요구사항 (예: 휠체어 경사로 필수, 케이터링 공간 필요 등)")
    
    submit_btn = st.button("설계도 생성하기")

# --- 평면도 생성 함수 ---
def draw_2d_floor_plan(event_type, attendees):
    fig = go.Figure()

    # 축 숨기기 및 배경 설정
    fig.update_xaxes(range=[0, 100], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[0, 100], showgrid=False, zeroline=False, visible=False)

    # 1. 메인 무대 / 행사장 (50%)
    fig.add_shape(type="rect", x0=0, y0=30, x1=70, y1=100, 
                  fillcolor="#A0C4FF", line=dict(color="black", width=2))
    fig.add_annotation(x=35, y=65, text=f"🎤 메인 {event_type} 구역<br>(최대 수용 인원: {int(attendees*0.7)}명)", 
                       showarrow=False, font=dict(size=16, color="black"))

    # 2. 휴게 및 식음료 존 (25%)
    fig.add_shape(type="rect", x0=70, y0=30, x1=100, y1=100, 
                  fillcolor="#CAFFBF", line=dict(color="black", width=2))
    fig.add_annotation(x=85, y=65, text="☕ 휴게/F&B 존<br>스탠딩 테이블 배치", 
                       showarrow=False, font=dict(size=14, color="black"))

    # 3. 대기 및 접수처 (15%)
    fig.add_shape(type="rect", x0=0, y0=0, x1=70, y1=30, 
                  fillcolor="#FDFFB6", line=dict(color="black", width=2))
    fig.add_annotation(x=35, y=15, text="📋 접수처 및 대기 라인<br>(체크인 데스크)", 
                       showarrow=False, font=dict(size=14, color="black"))

    # 4. 화장실 및 편의시설 (10%)
    fig.add_shape(type="rect", x0=70, y0=0, x1=100, y1=30, 
                  fillcolor="#FFADAD", line=dict(color="black", width=2))
    fig.add_annotation(x=85, y=15, text="🚻 화장실/의무실<br>(배리어프리 포함)", 
                       showarrow=False, font=dict(size=14, color="black"))

    # 출입구 화살표
    fig.add_annotation(x=35, y=-5, text="⬆️ 메인 출입구 (입/퇴장)", showarrow=False, 
                       font=dict(size=16, color="red", weight="bold"))

    fig.update_layout(
        title=f"🗺️ {event_type} 가상 2D 평면도 (마우스로 확대/축소 가능)",
        width=800, height=500,
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=50, b=30),
        hovermode="closest"
    )
    return fig

# 메인 화면: 결과 출력
if submit_btn:
    st.success("데이터 분석 완료! 최적의 행사장 설계를 확인하세요.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 시각화 평면도", "🚶 혼잡도 시뮬레이션", "🤝 모두를 위한 설계 (배리어 프리)", "💡 추가 추천 사항"])
    
    with tab1:
        st.subheader("최적의 행사장 시각화 설계")
        
        # 상단 요약 지표
        required_area = attendees * 1.5
        staff_needed = (attendees // 20) + 2
        col1, col2, col3 = st.columns(3)
        col1.metric("권장 최소 공간 면적", f"{required_area:,.0f} ㎡")
        col2.metric("권장 최소 스태프 수", f"{staff_needed} 명")
        col3.metric("휴게 공간 권장 비율", "전체 면적의 20%")
        
        st.divider()
        
        # 2D 평면도 시각화 출력
        st.markdown("### 🔍 2D 가상 평면도 시뮬레이션")
        st.info("실제 행사장 구역이 어떻게 배치되는지 위에서 내려다본 평면도입니다.")
        floor_plan_fig = draw_2d_floor_plan(event_type, attendees)
        st.plotly_chart(floor_plan_fig, use_container_width=True)
        
        st.divider()
        
        # 공간 비율 트리맵 시각화
        st.markdown("### 🧩 공간 할당 비율 트리맵")
        layout_data = pd.DataFrame({
            "구역": ["메인 행사장", "접수 및 대기", "휴게/식음료", "편의시설(화장실 등)"],
            "비율": [50, 15, 25, 10]
        })
        fig_tree = px.treemap(layout_data, path=["구역"], values="비율", 
                              color="비율", color_continuous_scale="Blues",
                              title="각 구역이 전체 면적에서 차지하는 비중")
        st.plotly_chart(fig_tree, use_container_width=True)

    with tab2:
        st.subheader("혼잡도 시뮬레이션 및 동선 안내")
        st.markdown("**예상 최대 혼잡 시간대:** 행사 시작 30분 전 및 종료 직후")
        congestion_level = min(attendees / 1000, 1.0)
        st.progress(congestion_level)
        if congestion_level > 0.7:
            st.warning("⚠️ 인구 밀집도가 높습니다. 입구와 출구를 반드시 분리하고, 비상 대피로를 2곳 이상 확보하세요.")
        else:
            st.info("✅ 쾌적한 행사 진행이 가능한 인원입니다. 단일 출입구로도 운영이 가능합니다.")
            
    with tab3:
        st.subheader("모두가 참여할 수 있는 행사 (유니버설 디자인)")
        st.markdown("- **이동 편의성:** 전 구역 단차 제거 및 휠체어/유모차 전용 통로(폭 1.2m 이상) 확보")
        st.markdown("- **시청각 지원:** 주요 안내문에 큰 글씨 및 픽토그램 적용, 수어 통역사 배치")
        st.markdown("- **안심 휴식 공간:** 조명과 소음이 차단된 '콰이어트 룸(Quiet Room)' 배치")
        st.markdown("- **접근성 화장실:** 휠체어 접근이 가능한 다목적 가족 화장실 설치")
        if extra_req:
            st.success(f"**반영된 추가 요구사항:** {extra_req}")

    with tab4:
        st.subheader("행사의 퀄리티를 높이는 추가 제안")
        st.markdown(f"**'{atmosphere}'** 분위기와 **'{event_type}'**의 특성을 살릴 수 있는 아이디어입니다.")
        st.markdown("- **스마트 사이니지:** 실시간 혼잡도를 스크린에 띄워 관람객 분산 유도")
        st.markdown("- **친환경 요소:** 다회용 컵 대여소 운영 및 모바일 티켓 사용")
