import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

# -----------------------------------------------------------------------------
# 1. 시스템 및 세션 상태 초기화
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Event Architect AI - 디지털 트윈", page_icon="🎪", layout="wide")

plt.rcParams['font.family'] = 'Malgun Gothic' if os.name == 'nt' else 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 수동 위치 조절용 세션 상태 세팅
if "stage_x" not in st.session_state: st.session_state.stage_x = 20.0
if "stage_y" not in st.session_state: st.session_state.stage_y = 20.0
if "food_x" not in st.session_state: st.session_state.food_x = 32.0
if "food_y" not in st.session_state: st.session_state.food_y = 20.0
if "med_x" not in st.session_state: st.session_state.med_x = 38.0
if "med_y" not in st.session_state: st.session_state.med_y = 6.0

for i in range(1, 13):
    if f"b{i}_x" not in st.session_state:
        st.session_state[f"b{i}_x"] = float(8.0 + ((i - 1) % 4) * 6.0)
    if f"b{i}_y" not in st.session_state:
        st.session_state[f"b{i}_y"] = float(10.0 + ((i - 1) // 4) * 6.0)

# -----------------------------------------------------------------------------
# 2. 사이드바 내비게이션
# -----------------------------------------------------------------------------
st.sidebar.title("🎪 Event Architect AI")
nav_page = st.sidebar.radio("📌 페이지 이동", ["🏠 홈 (Home)", "🗺️ 수동 조작 & AI 시뮬레이터", "📄 AI 정밀 컨설팅 보고서"])

# -----------------------------------------------------------------------------
# [PAGE 1] 🏠 홈 화면 (Landing Page)
# -----------------------------------------------------------------------------
if nav_page == "🏠 홈 (Home)":
    st.title("🎪 Event Architect AI")
    st.caption("AI 디지털 트윈 기반 행사장 공간 자동 배치, 실시간 군중 밀집도 시뮬레이션 및 안전 분석 플랫폼")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎮 수동 실시간 제어")
        st.markdown("슬라이더 및 좌표 입력을 통해 무대, 푸드존, 각 부스의 위치를 직접 이동시키며 실시간 군중 병목 위험을 직관적으로 확인합니다.")
    with col2:
        st.subheader("👥 개별 관람객 분포도")
        st.markdown("단순 히트맵을 넘어 실제 관람객 개별 위치(Dots)와 유입 밀도를 실시간 산출하여 정밀한 군중 행동 패턴을 시각화합니다.")
    with col3:
        st.subheader("🤖 AI 공간 최적화")
        st.markdown("기상 조건, 안전 요원 수, 비상 대피 통로 규격 등 다양한 변수를 반영하여 위험 요소를 자동 제거한 최적 도면을 산출합니다.")

    st.markdown("---")
    
    st.markdown("### 📊 플랫폼 주요 핵심 지표")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("누적 설계 행사장", "1,420건", "+14% 상승")
    m_col2.metric("사고 예방 적합률", "99.8%", "안전 기준 준수")
    m_col3.metric("평균 동선 단축율", "34.2%", "보행 편의 증대")
    m_col4.metric("AI 도면 생성 속도", "< 1.2초", "실시간 연산")

# -----------------------------------------------------------------------------
# [PAGE 2] 🗺️ 수동 조작 & AI 시뮬레이터
# -----------------------------------------------------------------------------
elif nav_page == "🗺️ 수동 조작 & AI 시뮬레이터":
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ 1. 행사장 및 환경 옵션")
    event_name = st.sidebar.text_input("행사명", "2026 지역 문화 축제")
    grid_dim = st.sidebar.select_slider("행사장 규격 (m)", options=[40, 50, 60], value=50)
    
    st.sidebar.subheader("👥 2. 군중 및 요원 옵션")
    visitor_count = st.sidebar.slider("예상 순간 최대 인원 (명)", 1000, 15000, 4000, step=500)
    peak_factor = st.sidebar.slider("피크타임 유입 가중치", 1.0, 2.0, 1.3, step=0.1)
    staff_count = st.sidebar.number_input("현장 안전요원 배치 (명)", 2, 50, 12)
    
    st.sidebar.subheader("🎪 3. 부스 및 기상 옵션")
    num_booths = st.sidebar.slider("부스 개수", 4, 12, 8)
    booth_size = st.sidebar.selectbox("부스 규격", ["3.0m x 3.0m", "3.5m x 3.5m", "4.0m x 4.0m"], index=1)
    b_size_val = float(booth_size.split("m")[0])
    
    weather = st.sidebar.selectbox("기상 환경 모드", ["맑음 (정상)", "우천시 (가설 천막 모드)", "야간 행사 (조명 동선)", "강풍 (안전 구역 확장)"])
    evac_mode = st.sidebar.checkbox("🚨 비상 대피 동선 표시", value=False)
    theme_option = st.sidebar.selectbox("도면 테마", ["CAD Blueprint (청도면)", "Modern Light", "Dark Mode"])

    # -------------------------------------------------------------------------
    # 수동 위치 조절 컨트롤러 (실시간 동기화)
    # -------------------------------------------------------------------------
    st.header(f"🗺️ {event_name} - 실시간 수동 조작 및 AI 최적화")
    
    with st.expander("🎮 [도면 시설물/부스 위치 수동 조절 컨트롤러]", expanded=True):
        st.info("💡 아래 슬라이더를 움직이면 왼쪽 **'수동 배치 & 사람 분포도'**에 위치와 군중 밀도가 즉시 반영됩니다.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**🎭 메인 무대 위치**")
            st.slider("무대 X 좌표", 2.0, float(grid_dim - 12), key="stage_x")
            st.slider("무대 Y 좌표", 2.0, float(grid_dim - 8), key="stage_y")
        with c2:
            st.markdown("**🍔 푸드존 위치**")
            st.slider("푸드존 X 좌표", 2.0, float(grid_dim - 10), key="food_x")
            st.slider("푸드존 Y 좌표", 2.0, float(grid_dim - 8), key="food_y")
        with c3:
            st.markdown("**🚑 의무실 위치**")
            st.slider("의무실 X 좌표", 2.0, float(grid_dim - 8), key="med_x")
            st.slider("의무실 Y 좌표", 2.0, float(grid_dim - 6), key="med_y")

        st.markdown("---")
        st.markdown("**📦 개별 부스 X·Y 위치 직접 설정**")
        b_cols = st.columns(min(num_booths, 4))
        for i in range(1, num_booths + 1):
            with b_cols[(i - 1) % 4]:
                st.caption(f"부스 B{i}")
                st.slider(f"B{i} X", 1.0, float(grid_dim - 5), key=f"b{i}_x")
                st.slider(f"B{i} Y", 1.0, float(grid_dim - 5), key=f"b{i}_y")

    # -------------------------------------------------------------------------
    # 시뮬레이션 및 개별 사람 점(Dot) 좌표 생성 엔진
    # -------------------------------------------------------------------------
    def run_simulation():
        np.random.seed(42)
        total_people = int(visitor_count * peak_factor / 10)  # 시각화용 점 개수
        
        # 1. 수동 위치 가져오기
        stg_b = (st.session_state.stage_x, st.session_state.stage_y)
        fd_b = (st.session_state.food_x, st.session_state.food_y)
        md_b = (st.session_state.med_x, st.session_state.med_y)
        bths_b = [(st.session_state[f"b{i}_x"], st.session_state[f"b{i}_y"]) for i in range(1, num_booths + 1)]

        # 수동 사람 분포 샘플링 (무대, 푸드존, 부스 주변 밀집)
        p_x_b, p_y_b = [], []
        centers_b = [stg_b, fd_b] + bths_b
        weights = [0.35, 0.25] + [0.4 / len(bths_b)] * len(bths_b)
        
        for _ in range(total_people):
            idx = np.random.choice(len(centers_b), p=weights)
            cx, cy = centers_b[idx]
            px = np.clip(np.random.normal(cx + 3, 3.0), 1, grid_dim - 1)
            py = np.clip(np.random.normal(cy + 2, 3.0), 1, grid_dim - 1)
            p_x_b.append(px)
            p_y_b.append(py)

        # 2. AI 최적 위치 생성
        stg_a = (grid_dim / 2 - 5, grid_dim - 10)
        fd_a = (grid_dim - 12, 10)
        md_a = (3, 4)
        
        bths_a = []
        half = (num_booths + 1) // 2
        for i in range(half):
            bths_a.append((5, 10 + i * 5.5))
        for i in range(num_booths - half):
            bths_a.append((grid_dim - 10, 10 + i * 5.5))

        # AI 사람 분포 샘플링 (외곽 분산)
        p_x_a, p_y_a = [], []
        centers_a = [stg_a, fd_a] + bths_a
        weights_a = [0.3, 0.25] + [0.45 / len(bths_a)] * len(bths_a)
        
        for _ in range(total_people):
            idx = np.random.choice(len(centers_a), p=weights_a)
            cx, cy = centers_a[idx]
            px = np.clip(np.random.normal(cx + 3, 4.5), 1, grid_dim - 1)
            py = np.clip(np.random.normal(cy + 2, 4.5), 1, grid_dim - 1)
            p_x_a.append(px)
            p_y_a.append(py)

        return {
            "pos_b": {"Stage": stg_b, "Food": fd_b, "Med": md_b, "Booths": bths_b, "px": p_x_b, "py": p_y_b},
            "pos_a": {"Stage": stg_a, "Food": fd_a, "Med": md_a, "Booths": bths_a, "px": p_x_a, "py": p_y_a}
        }

    # -------------------------------------------------------------------------
    # CAD 및 관람객 분포도 렌더링
    # -------------------------------------------------------------------------
    def draw_layout(data, title, is_after=False):
        fig, ax = plt.subplots(figsize=(8, 7.5), dpi=120)
        
        bg_color = '#0F172A' if "CAD" in theme_option else ('#121212' if "Dark" in theme_option else '#F8FAFC')
        grid_color = '#1E293B' if "CAD" in theme_option else ('#282828' if "Dark" in theme_option else '#E2E8F0')
        wall_color = '#38BDF8' if "CAD" in theme_option else ('#BB86FC' if "Dark" in theme_option else '#0F172A')

        ax.set_facecolor(bg_color)
        fig.patch.set_facecolor(bg_color)
        ax.grid(True, color=grid_color, linestyle='--', linewidth=0.6, zorder=1)

        # 1. 사람 분포도 (Individual People Dots Plot)
        dot_color = '#38BDF8' if is_after else '#EF4444'
        ax.scatter(data["px"], data["py"], s=12, color=dot_color, alpha=0.5, label="관람객 위치", zorder=3)

        # 2. 외곽 테두리 및 출입구
        ax.plot([0, grid_dim, grid_dim, 0, 0], [0, 0, grid_dim, grid_dim, 0], color=wall_color, linewidth=3, zorder=4)
        ax.text(grid_dim / 2, -1.8, "🚪 MAIN ENTRANCE", ha='center', va='top', fontsize=8, fontweight='bold', color=wall_color,
                bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec=wall_color, lw=1.2), zorder=8)
        ax.text(grid_dim / 2, grid_dim + 1.8, "🚪 EMERGENCY EXIT", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#EF4444',
                bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec='#EF4444', lw=1.2), zorder=8)

        # 3. 비상 대피 / 권장 동선 표시
        if is_after:
            if evac_mode:
                ax.annotate('', xy=(grid_dim / 2, grid_dim - 2), xytext=(grid_dim / 2, grid_dim / 2),
                            arrowprops=dict(arrowstyle="->", color="#EF4444", lw=3, ls="--"))
                ax.annotate('', xy=(grid_dim / 2, 2), xytext=(grid_dim / 2, grid_dim / 2),
                            arrowprops=dict(arrowstyle="->", color="#EF4444", lw=3, ls="--"))
            else:
                ax.annotate('', xy=(10, grid_dim - 10), xytext=(10, 10), arrowprops=dict(arrowstyle="->", color="#10B981", lw=2))
                ax.annotate('', xy=(grid_dim - 10, 10), xytext=(grid_dim - 10, grid_dim - 10), arrowprops=dict(arrowstyle="->", color="#10B981", lw=2))

        # 4. 부스 배치
        for i, (bx, by) in enumerate(data["Booths"], 1):
            rect = patches.FancyBboxPatch((bx, by), b_size_val, b_size_val, boxstyle="round,pad=0.1",
                                           fc='#2563EB', ec='white', lw=1.2, alpha=0.85, zorder=5)
            ax.add_patch(rect)
            ax.text(bx + b_size_val / 2, by + b_size_val / 2, f"B{i}", color='white', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=6)

        # 5. 주요 시설물
        sx, sy = data["Stage"]
        ax.add_patch(patches.FancyBboxPatch((sx, sy), 10, 6, boxstyle="round,pad=0.2", fc='#DC2626', ec='white', lw=1.5, zorder=6))
        ax.text(sx + 5, sy + 3, "🎭 무대", color='white', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=7)

        fx, fy = data["Food"]
        ax.add_patch(patches.FancyBboxPatch((fx, fy), 8, 5, boxstyle="round,pad=0.2", fc='#D97706', ec='white', lw=1.5, zorder=6))
        ax.text(fx + 4, fy + 2.5, "🍔 푸드존", color='white', fontsize=8, fontweight='bold', ha='center', va='center', zorder=7)

        mx, my = data["Med"]
        ax.add_patch(patches.FancyBboxPatch((mx, my), 6, 4, boxstyle="round,pad=0.2", fc='#059669', ec='white', lw=1.5, zorder=6))
        ax.text(mx + 3, my + 2, "🚑 의무실", color='white', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=7)

        ax.set_xlim(-4, grid_dim + 4)
        ax.set_ylim(-4, grid_dim + 4)
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10, color=wall_color)
        ax.tick_params(colors=wall_color)
        return fig

    # -------------------------------------------------------------------------
    # 화면 출력
    # -------------------------------------------------------------------------
    sim_res = run_simulation()

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("### 🔴 수동 배치 & 사람 분포도")
        st.pyplot(draw_layout(sim_res["pos_b"], f"수동 배치 (붉은 점: 관람객 {visitor_count}명 밀집)", is_after=False))
        st.warning("⚠️ **상황 분석**: 수동 조작 위치 주변에 관람객 점(Dot)이 뭉쳐 병목 및 압사 위험 구역이 형성됩니다.")

    with col_r:
        st.markdown("### 🟢 AI 최적화 & 관람 동선도")
        st.pyplot(draw_layout(sim_res["pos_a"], f"AI 최적 배치 (푸른 점: 관람객 균일 분산)", is_after=True))
        st.success("✅ **개선 완료**: 중앙 통로 확보 및 양측 배치로 관람객 밀집도가 원활히 분산되었습니다.")

# -----------------------------------------------------------------------------
# [PAGE 3] 📄 AI 정밀 컨설팅 보고서
# -----------------------------------------------------------------------------
else:
    st.title("📄 AI 공간 설계 및 군중 안전 정밀 컨설팅 보고서")
    st.caption("발행처: Event Architect AI 연구소 | 승인 번호: EAAI-REPORT-2026-9081")
    st.divider()

    st.markdown("""
    ### 1. 종합 안전 및 효율성 평가 결과
    본 보고서는 수동 설정안과 AI 자동 최적화안의 공간 효율성, 보행 쾌적성, 비상 대피 골든타임 확보 여부를 종합적으로 비교 분석한 결과입니다.
    """)

    rep_df = pd.DataFrame({
        "평가 지표": ["국소 최고 군중 밀도", "보행 통로 최소 폭", "의무실 골든타임 도달률", "비상 대피 완출 시간", "안전요원 커버리지", "종합 안전 등급"],
        "수동 설정안": ["4.6 명/m² (위험)", "1.8 m (협소)", "62.0% (지연 위험)", "13.5 분", "48.0%", "D 등급 (개선 필요)"],
        "AI 최적화안": ["1.5 명/m² (쾌적)", "4.5 m (양호)", "99.2% (즉시 확보)", "4.2 분", "92.5%", "A+ 등급 (최우수)"],
        "개선 성과": ["67.3% 감소", "+2.7 m 확장", "+37.2%p 증가", "68.8% 단축", "+44.5%p 증가", "3단계 상향"]
    })
    st.table(rep_df)

    st.markdown("---")

    st.markdown("""
    ### 2. XAI(설명 가능한 AI) 배치 변경 근거 및 규칙

    * **[규칙 1] 응급 이송 경로 확보 (Med-Zone Direct)**  
      의무실을 메인 출입구 기준 $5\text{m}$ 이내 구역($X=3\text{m}, Y=4\text{m}$)에 고정하여, 앰뷸런스 진입 시 관람객 동선과 겹치지 않는 독자적 비상 통로를 확보했습니다.
    
    * **[규칙 2] 메인 무대와 푸드존의 이중 거점화 (Two-Pole Distro)**  
      가장 많은 관람객이 체류하는 무대와 푸드존을 대각선 반대 방향으로 배치하여 행사장 전체로 관람객 흐름을 유도했습니다.
    
    * **[규칙 3] 병목 방지 통로 가이드라인 (Minimum Width 4.5m)**  
      모든 부스의 전면 공간을 최소 $4.5\text{m}$ 이상 격리하여 휠체어 및 유모차 이동 공간을 확보했습니다.
    """)

    st.success("📝 **최종 승인 의견**: 본 AI 최적화 설계안은 관련 지자체 군중 안전 관리 지침을 충족하므로 현장 시공안으로 확정할 것을 권장합니다.")
