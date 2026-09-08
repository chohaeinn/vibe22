import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="AI 행사장 종합 디자이너 대시보드",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished Dashboard look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38BDF8;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #94A3B8;
    }
    .card-box {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎪 AI 행사장 설계 & 시뮬레이션 대시보드")
st.caption("행사 형태와 전체 행사장 구조에 맞춰 정밀 공간 설계, 유니버설(배리어 프리) 가이드라인, 동선 시뮬레이션을 한눈에 제공합니다.")

# ---------------------------------------------------------
# 사이드바 설정
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 행사 및 공간 조건 설정")
    
    event_type = st.selectbox(
        "행사 유형",
        ["컨퍼런스/학술대회", "공연/콘서트", "전시회/박람회", "네트워킹 파티", "지역 축제/야외 행사"]
    )
    
    venue_shape = st.selectbox(
        "🏢 행사장 총 구조 (건물 형태)",
        ["사각형 홀 (Rectangular)", "원형 돔 (Circular Dome)", "타원형/경기장 (Oval Stadium)", "야외 공원/가변형 (Outdoor Park)"]
    )
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        attendees = st.number_input("예상 인원 (명)", min_value=20, max_value=50000, value=500, step=50)
    with col_sb2:
        duration = st.number_input("진행 시간 (h)", min_value=1, max_value=24, value=4)
        
    atmosphere = st.selectbox(
        "원하는 분위기",
        ["차분하고 전문적인", "활기차고 신나는", "고급스럽고 우아한", "자유롭고 창의적인"]
    )
    
    age_group = st.multiselect(
        "주요 연령대",
        ["10대 이하", "20대", "30대", "40대", "50대 이상"],
        default=["20대", "30대"]
    )
    
    barrier_free_priority = st.toggle("♿ 유니버설/배리어 프리 강하게 적용", value=True)
    
    extra_req = st.text_area("추가 요구사항 (예: 수어 통역, 휠체어 충전소, 콰이어트룸 등)")

# ---------------------------------------------------------
# 정밀 2D 평면도 생성 함수 (건물 구조별 커스텀 렌더링)
# ---------------------------------------------------------
def create_advanced_floor_plan(shape, event_type, attendees):
    fig = go.Figure()
    
    # 기본 스타일링: 블루프린트 / CAD 분위기 Dark Slate
    canvas_bg = "#0F172A"
    grid_color = "#1E293B"
    
    fig.update_xaxes(range=[-10, 110], showgrid=True, gridcolor=grid_color, zeroline=False, visible=False)
    fig.update_yaxes(range=[-10, 110], showgrid=True, gridcolor=grid_color, zeroline=False, visible=False)
    
    # 1. 외곽 구조선 (Wall/Boundary) 및 기본 레이아웃 세팅
    if "원형" in shape:
        # 외곽 원
        fig.add_shape(type="circle", x0=0, y0=0, x1=100, y1=100,
                      line=dict(color="#38BDF8", width=3), fillcolor="#1E293B")
        # 중앙 무대 (원형)
        fig.add_shape(type="circle", x0=35, y0=65, x1=65, y1=95,
                      line=dict(color="#F43F5E", width=2), fillcolor="rgba(244, 63, 94, 0.2)")
        fig.add_annotation(x=50, y=80, text="🎤 메인 무대/발표존", showarrow=False, font=dict(color="#F43F5E", size=13))
        
        # 좌석/관람 구역 (방사형 격자 점)
        angles = np.linspace(0, np.pi, 15)
        radii = [20, 28, 36]
        seat_x, seat_y = [], []
        for r in radii:
            for a in angles:
                seat_x.append(50 + r * np.cos(a))
                seat_y.append(45 + r * np.sin(a) * 0.7)
        fig.add_trace(go.Scatter(x=seat_x, y=seat_y, mode='markers',
                                 marker=dict(size=6, color='#60A5FA', symbol='square'),
                                 name='관람석/스탠딩'))
        
        # 외곽 편의시설 링 (호 형태 구역)
        fig.add_shape(type="rect", x0=5, y0=5, x1=30, y1=25, rx=8, ry=8,
                      fillcolor="rgba(251, 191, 36, 0.2)", line=dict(color="#FBBF24", width=2))
        fig.add_annotation(x=17.5, y=15, text="☕ F&B / 휴게 라운지", showarrow=False, font=dict(color="#FBBF24", size=11))
        
        fig.add_shape(type="rect", x0=70, y0=5, x1=95, y1=25, rx=8, ry=8,
                      fillcolor="rgba(52, 211, 153, 0.2)", line=dict(color="#34D399", width=2))
        fig.add_annotation(x=82.5, y=15, text="♿ 콰이어트룸 & 의무실", showarrow=False, font=dict(color="#34D399", size=11))

        # 입구
        fig.add_annotation(x=50, y=-3, text="🚪 메인 출입구 (휠체어 경사로)", showarrow=False, font=dict(color="#38BDF8", size=13))
        fig.add_annotation(x=50, y=5, text="⬇️", showarrow=False, font=dict(color="#38BDF8", size=18))

    elif "타원형" in shape:
        # 타원 외곽
        fig.add_shape(type="path", path="M 0,50 A 50,35 0 1,0 100,50 A 50,35 0 1,0 0,50 Z",
                      line=dict(color="#38BDF8", width=3), fillcolor="#1E293B")
        
        # 중앙 스테이지 (필드 중앙)
        fig.add_shape(type="rect", x0=30, y0=35, x1=70, y1=65, rx=10, ry=10,
                      fillcolor="rgba(168, 85, 247, 0.25)", line=dict(color="#A855F7", width=2))
        fig.add_annotation(x=50, y=50, text=f"🎪 {event_type} 메인 필드", showarrow=False, font=dict(color="#C084FC", size=14))
        
        # 좌우 트랙 편의존
        fig.add_shape(type="rect", x0=5, y0=35, x1=20, y1=65, rx=5, ry=5,
                      fillcolor="rgba(251, 191, 36, 0.2)", line=dict(color="#FBBF24", width=1.5))
        fig.add_annotation(x=12.5, y=50, text="📋 등록/안내", showarrow=False, font=dict(color="#FBBF24", size=10))

        fig.add_shape(type="rect", x0=80, y0=35, x1=95, y1=65, rx=5, ry=5,
                      fillcolor="rgba(52, 211, 153, 0.2)", line=dict(color="#34D399", width=1.5))
        fig.add_annotation(x=87.5, y=50, text="🚻 다목적 화장실", showarrow=False, font=dict(color="#34D399", size=10))

        # 입구 / 비상구
        fig.add_annotation(x=50, y=10, text="🚨 비상구 A", showarrow=False, font=dict(color="#F43F5E", size=11))
        fig.add_annotation(x=50, y=90, text="🚪 주 출입구 B", showarrow=False, font=dict(color="#38BDF8", size=11))

    elif "야외" in shape:
        # 야외 곡선 테두리 (자연스러운 외곽)
        fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, rx=20, ry=20,
                      line=dict(color="#10B981", width=3, dash="dot"), fillcolor="#064E3B")
        
        # 야외 메인 무대 천막
        fig.add_shape(type="path", path="M 20,70 L 80,70 L 50,95 Z",
                      fillcolor="rgba(244, 63, 94, 0.3)", line=dict(color="#F43F5E", width=2))
        fig.add_annotation(x=50, y=78, text="🎪 야외 메인 무대", showarrow=False, font=dict(color="#F43F5E", size=13))
        
        # 야외 푸드트럭 / 부스 존
        for i, pos_x in enumerate([15, 35, 65, 85]):
            fig.add_shape(type="rect", x0=pos_x-8, y0=30, x1=pos_x+8, y1=45,
                          fillcolor="rgba(251, 191, 36, 0.25)", line=dict(color="#FBBF24", width=1.5))
            fig.add_annotation(x=pos_x, y=37.5, text=f"🛖 부스/트럭 {i+1}", showarrow=False, font=dict(color="#FBBF24", size=10))

        # 잔디 휴계 존
        fig.add_shape(type="circle", x0=35, y0=5, x1=65, y1=25,
                      fillcolor="rgba(16, 185, 129, 0.3)", line=dict(color="#10B981", width=1.5))
        fig.add_annotation(x=50, y=15, text="🌿 피크닉/휴식 존", showarrow=False, font=dict(color="#6EE7B7", size=11))

    else:
        # 사각형 직관적 그리드 (Standard Rectangular Hall)
        fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, rx=4, ry=4,
                      line=dict(color="#38BDF8", width=3), fillcolor="#1E293B")
        
        # 1. 무대 (상단)
        fig.add_shape(type="rect", x0=15, y0=75, x1=85, y1=95, rx=6, ry=6,
                      fillcolor="rgba(99, 102, 241, 0.3)", line=dict(color="#818CF8", width=2))
        fig.add_annotation(x=50, y=85, text=f"🎤 메인 {event_type} 스테이지", showarrow=False, font=dict(color="#A5B4FC", size=14))

        # 2. 메인 관람/참여석 (중앙 격자 배치를 상세히 그리기)
        grid_x, grid_y = np.meshgrid(np.linspace(20, 80, 10), np.linspace(35, 65, 6))
        fig.add_trace(go.Scatter(
            x=grid_x.flatten(), y=grid_y.flatten(), mode='markers',
            marker=dict(size=7, color='#38BDF8', symbol='circle'),
            name='관람석 / 테이블'
        ))

        # 통로 (Aisle Vector Arrows)
        fig.add_annotation(x=50, y=25, ax=50, ay=70, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowsize=1.2, arrowcolor="#64748B")
        fig.add_annotation(x=50, y=28, text="↔ 중앙 주 이동 통로 (폭 2.5m 이상)", showarrow=False, font=dict(color="#94A3B8", size=10))

        # 3. 좌측: F&B 및 네트워킹
        fig.add_shape(type="rect", x0=3, y0=30, x1=14, y1=70, rx=4, ry=4,
                      fillcolor="rgba(251, 191, 36, 0.2)", line=dict(color="#FBBF24", width=1.5))
        fig.add_annotation(x=8.5, y=50, text="☕ F&B<br>스탠딩존", showarrow=False, font=dict(color="#FBBF24", size=10))

        # 4. 우측: 배리어 프리 콰이어트 룸 및 의료실
        fig.add_shape(type="rect", x0=86, y0=30, x1=97, y1=70, rx=4, ry=4,
                      fillcolor="rgba(52, 211, 153, 0.2)", line=dict(color="#34D399", width=1.5))
        fig.add_annotation(x=91.5, y=50, text="♿ 콰이어트룸<br>& 의무실", showarrow=False, font=dict(color="#34D399", size=10))

        # 5. 하단: 접수처 & 주 출입구
        fig.add_shape(type="rect", x0=20, y0=5, x1=80, y1=20, rx=4, ry=4,
                      fillcolor="rgba(56, 189, 248, 0.15)", line=dict(color="#38BDF8", width=1.5))
        fig.add_annotation(x=50, y=12.5, text="📋 체크인 및 리셉션 데스크", showarrow=False, font=dict(color="#7DD3FC", size=11))
        
        # 입출구 화살표
        fig.add_annotation(x=10, y=-4, text="🚪 입구 (경사로)", showarrow=False, font=dict(color="#34D399", size=11))
        fig.add_annotation(x=90, y=-4, text="🚨 출구 (비상로)", showarrow=False, font=dict(color="#F43F5E", size=11))

    # 레이아웃 미세 조정
    fig.update_layout(
        title=dict(text=f"📐 [{shape}] 기반 2D 아키텍처 구역 배치도", font=dict(size=16, color="#F8FAFC")),
        plot_bgcolor=canvas_bg,
        paper_bgcolor=canvas_bg,
        height=520,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )
    return fig

# ---------------------------------------------------------
# 통합 대시보드 화면 구성
# ---------------------------------------------------------

# 상단 주요 지표 (Metric Cards)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

req_area = attendees * 1.6
staff_cnt = int(attendees / 22) + 2
congestion_score = min(round((attendees / 1200) * 10, 1), 10.0)

with col_m1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">📐 권장 필요 면적</div><div class="metric-value">{req_area:,.0f} ㎡</div></div>', unsafe_allow_html=True)

with col_m2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">👨‍💼 추천 운영 스태프</div><div class="metric-value">{staff_cnt} 명</div></div>', unsafe_allow_html=True)

with col_m3:
    status_color = "#F43F5E" if congestion_score > 6.5 else "#34D399"
    st.markdown(f'<div class="metric-card"><div class="metric-label">🏃 혼잡도 예상 지수</div><div class="metric-value" style="color:{status_color}">{congestion_score} / 10</div></div>', unsafe_allow_html=True)

with col_m4:
    st.markdown('<div class="metric-card"><div class="metric-label">♿ 유니버설 설계 점수</div><div class="metric-value" style="color: #FBBF24">95 점</div></div>', unsafe_allow_html=True)

st.write("")

# 메인 2분할 레이아웃 (좌: 시각화 평면도, 우: 혼잡도 시뮬레이션 & 면적 배분)
col_left, col_right = st.columns([1.3, 0.9])

with col_left:
    st.subheader("🗺️ 구체적 2D 가상 평면도 시뮬레이션")
    fig_plan = create_advanced_floor_plan(venue_shape, event_type, attendees)
    st.plotly_chart(fig_plan, use_container_width=True)

with col_right:
    st.subheader("📊 동선 & 혼잡도 시간대별 분석")
    
    # 시간대별 혼잡도 피크 그래프
    hours = [f"{h}:00" for h in range(1, duration + 1)]
    np.random.seed(42)
    crowd_pattern = [20, 85, 60, 50, 45, 90][:duration]
    if len(crowd_pattern) < duration:
        crowd_pattern += [40] * (duration - len(crowd_pattern))
        
    df_crowd = pd.DataFrame({"시간": hours, "예상 혼잡률(%)": crowd_pattern})
    
    fig_crowd = px.area(
        df_crowd, x="시간", y="예상 혼잡률(%)",
        title="⏰ 행사 시간대별 인파 집중도 시뮬레이션",
        markers=True,
        color_discrete_sequence=["#38BDF8"]
    )
    fig_crowd.update_layout(
        plot_bgcolor="#0F172A",
        paper_bgcolor="#0F172A",
        font=dict(color="#94A3B8"),
        height=240,
        margin=dict(l=10, r=10, t=35, b=10)
    )
    st.plotly_chart(fig_crowd, use_container_width=True)
    
    st.subheader("🍰 구역별 공간 할당 비율")
    layout_pie = pd.DataFrame({
        "구역": ["메인 무대/발표", "접수/대기존", "F&B/휴게", "편의/콰이어트룸"],
        "비율": [45, 20, 20, 15]
    })
    fig_pie = px.pie(
        layout_pie, names="구역", values="비율", hole=0.4,
        color_discrete_sequence=["#818CF8", "#38BDF8", "#FBBF24", "#34D399"]
    )
    fig_pie.update_layout(
        plot_bgcolor="#0F172A", paper_bgcolor="#0F172A",
        font=dict(color="#F8FAFC"), height=210,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# 하단 2분할 카드 레이아웃 (유니버설 설계 & 추가 추천 제안)
col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    st.markdown("""
    <div class="card-box">
        <h3 style="color:#34D399; margin-top:0;">♿ 모두를 위한 유니버설 설계 (배리어 프리)</h3>
        <ul style="color:#E2E8F0; line-height: 1.7;">
            <li><b>단차 제로(Zero-step) 동선:</b> 모든 주 출입구 및 무대 접근로에 경사각 1:12 이하 휠체어 램프 설치</li>
            <li><b>콰이어트 룸 (Quiet Room):</b> 자폐 스펙트럼 및 감각과부하 참가자를 위한 저조음·저소음 차단 휴게 공간 운영</li>
            <li><b>다목적 가방/가족 화장실:</b> 남녀 구별 없는 넓은 접근성 화장실 배치 (성별 이분법 및 장애 유무 초월)</li>
            <li><b>시청각 보조:</b> 실시간 자막 전광판 설치 및 주요 수어 통역사 시야 확보 구역 지정</li>
            <li><b>점자 및 고대비 안내판:</b> 시각 장애인을 위한 촉지도 및 픽토그램 보도 블록 설치</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_bottom2:
    age_str = ", ".join(age_group) if age_group else "전 연령"
    extra_str = f"<p style='color:#38BDF8;'>📌 <b>추가 요청 반영:</b> {extra_req}</p>" if extra_req else ""
    st.markdown(f"""
    <div class="card-box">
        <h3 style="color:#38BDF8; margin-top:0;">💡 '{atmosphere}' 분위기 맞춤 기획 & 연출 제안</h3>
        <ul style="color:#E2E8F0; line-height: 1.7;">
            <li><b>디지털 사이니지 혼잡도 안내:</b> 출입구 스크린에 각 구역 실시간 밀집도를 색상으로 표시하여 자연스러운 분산 유도</li>
            <li><b>스마트 네트워킹 스탠딩존:</b> {age_str} 연령대가 선호하는 자율 교류용 하이테이블 및 QR 프로필 교환 존 배치</li>
            <li><b>친환경 Zero-Waste 운영:</b> 종이 리플렛 대신 모바일 맵 제공, 다회용 컵 회수함 구역별 2개 이상 설치</li>
            <li><b>안전 보안 요원 배치:</b> 병목현상이 예상되는 접수처 및 퇴장로에 전담 스태프 우선 배치</li>
        </ul>
        {extra_str}
    </div>
    """, unsafe_allow_html=True)
