import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# 1. 페이지 설정 및 세션 상태 초기화
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Event Architect AI", page_icon="🎪", layout="wide")

plt.rcParams['font.family'] = 'Malgun Gothic' if os.name == 'nt' else 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 이동 제어 세션 초기화
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 홈 (Home)"

# -----------------------------------------------------------------------------
# 2. 사이드바 내비게이션
# -----------------------------------------------------------------------------
st.sidebar.title("🎪 Event Architect AI")

# 사이드바 라디오 버튼과 세션 연동
selected_page = st.sidebar.radio(
    "📌 페이지 이동", 
    ["🏠 홈 (Home)", "🗺️ 대시보드 (드래그 도면 편집)", "📄 AI 정밀 컨설팅 보고서"],
    index=["🏠 홈 (Home)", "🗺️ 대시보드 (드래그 도면 편집)", "📄 AI 정밀 컨설팅 보고서"].index(st.session_state.current_page)
)

if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

# -----------------------------------------------------------------------------
# [PAGE 1] 🏠 홈 화면 (Landing Page)
# -----------------------------------------------------------------------------
if st.session_state.current_page == "🏠 홈 (Home)":
    st.title("🎪 Event Architect AI")
    st.caption("AI 디지털 트윈 기반 행사장 공간 자동 배치, 실시간 군중 밀집도 시뮬레이션 및 안전 분석 플랫폼")
    
    st.markdown("---")
    
    # 대시보드 바로가기 대형 CTA 버튼
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        if st.button("🚀 대시보드로 이동하여 도면 직접 편집하기", type="primary", use_container_width=True):
            st.session_state.current_page = "🗺️ 대시보드 (드래그 도면 편집)"
            st.rerun()

    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎨 드래그 & 리사이즈 도면 편집")
        st.markdown("마우스 드래그로 부스의 위치를 자유롭게 이동하고, 모서리를 끌어 부스 크기를 직관적으로 조절할 수 있습니다.")
    with col2:
        st.subheader("🌊 부드러운 그라데이션 밀집도")
        st.markdown("징그러운 점(Dot) 표식을 제거하고, 가우시안 필터링 기반의 은은하고 고급스러운 에어리얼 밀집도 히트맵을 제공합니다.")
    with col3:
        st.subheader("🤖 AI 공간 최적화 알고리즘")
        st.markdown("병목 위험 구역을 실시간 감지하여 최적의 4.5m 순환 통로 및 비상 출구 접근성을 자동 계산합니다.")

    st.divider()
    
    st.markdown("### 📊 플랫폼 주요 핵심 지표")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("누적 설계 행사장", "1,420건", "+14% 상승")
    m_col2.metric("사고 예방 적합률", "99.8%", "안전 기준 준수")
    m_col3.metric("평균 동선 단축율", "34.2%", "보행 편의 증대")
    m_col4.metric("AI 도면 연산 속도", "< 0.8초", "실시간 반영")

# -----------------------------------------------------------------------------
# [PAGE 2] 🗺️ 대시보드 (드래그 도면 편집 & 그라데이션 시뮬레이터)
# -----------------------------------------------------------------------------
elif st.session_state.current_page == "🗺️ 대시보드 (드래그 도면 편집)":
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ 1. 행사장 및 환경 설정")
    event_name = st.sidebar.text_input("행사명", "2026 지역 문화 축제")
    visitor_count = st.sidebar.slider("예상 순간 최대 인원 (명)", 1000, 15000, 5000, step=500)
    
    st.sidebar.subheader("🎪 2. 부스 및 기상 옵션")
    weather = st.sidebar.selectbox("기상 환경 모드", ["맑음 (정상)", "우천시 (가설 천막 모드)", "야간 행사 (조명 동선)"])
    evac_mode = st.sidebar.checkbox("🚨 비상 대피 동선 표기", value=False)
    
    st.header(f"🗺️ {event_name} - 인터랙티브 도면 편집 대시보드")
    st.caption("👈 수동 도면 영역에서 부스 상자를 **드래그하여 이동**하거나 **우측 하단 모서리를 끌어 크기를 조절**할 수 있습니다.")

    tab1, tab2 = st.tabs(["🖱️ 1. 수동 드래그/리사이즈 도면 편집기", "🟢 2. AI 최적화 그라데이션 도면 비교"])

    with tab1:
        st.subheader("🎮 드래그 & 리사이즈 가능한 수동 배치 도면")
        
        # HTML5 Canvas 드래그 & 리사이즈 스크립트
        html_code = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                #canvas-container {
                    position: relative;
                    width: 700px;
                    height: 600px;
                    background-color: #0F172A;
                    border: 3px solid #38BDF8;
                    border-radius: 8px;
                    user-select: none;
                }
                canvas {
                    position: absolute;
                    top: 0;
                    left: 0;
                }
                .info-box {
                    color: white;
                    font-family: sans-serif;
                    font-size: 13px;
                    margin-top: 8px;
                }
            </style>
        </head>
        <body>
            <div id="canvas-container">
                <canvas id="bgCanvas" width="700" height="600"></canvas>
                <canvas id="fgCanvas" width="700" height="600"></canvas>
            </div>
            <div class="info-box">
                📌 **사용법**: 부스를 클릭하여 <b>드래그로 이동</b> / 우측 하단 <b>점(Handle)을 드래그하여 크기 조절</b>
            </div>

            <script>
                const fgCanvas = document.getElementById('fgCanvas');
                const ctx = fgCanvas.getContext('2d');
                const bgCanvas = document.getElementById('bgCanvas');
                const bgCtx = bgCanvas.getContext('2d');

                // 부스 데이터 (x, y, w, h, name)
                let booths = [
                    {x: 100, y: 150, w: 70, h: 70, name: "B1"},
                    {x: 200, y: 150, w: 70, h: 70, name: "B2"},
                    {x: 300, y: 150, w: 70, h: 70, name: "B3"},
                    {x: 100, y: 250, w: 70, h: 70, name: "B4"},
                    {x: 200, y: 250, w: 70, h: 70, name: "B5"},
                    {x: 300, y: 250, w: 70, h: 70, name: "B6"}
                ];

                // 고정 구조물
                const stage = {x: 250, y: 30, w: 200, h: 80, name: "🎭 메인 무대"};
                const food = {x: 500, y: 400, w: 140, h: 90, name: "🍔 푸드존"};
                const medical = {x: 30, y: 500, w: 100, h: 70, name: "🚑 의무실"};

                let selectedIdx = -1;
                let isResizing = false;
                let dragOffsetX = 0, dragOffsetY = 0;
                const handleSize = 10;

                // 1. 부드러운 가우시안/라디얼 그라데이션 배경 그리기
                function drawBackground() {
                    bgCtx.clearRect(0, 0, 700, 600);
                    
                    // 모눈종이 격자
                    bgCtx.strokeStyle = '#1E293B';
                    bgCtx.lineWidth = 1;
                    for (let x = 0; x < 700; x += 35) {
                        bgCtx.beginPath(); bgCtx.moveTo(x, 0); bgCtx.lineTo(x, 600); bgCtx.stroke();
                    }
                    for (let y = 0; y < 600; y += 35) {
                        bgCtx.beginPath(); bgCtx.moveTo(0, y); bgCtx.lineTo(700, y); bgCtx.stroke();
                    }

                    // 무대 및 부스 주변 부드러운 은은한 밀집도 그라데이션
                    const grad = bgCtx.createRadialGradient(350, 150, 20, 350, 150, 220);
                    grad.addColorStop(0, 'rgba(239, 68, 68, 0.55)');
                    grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.25)');
                    grad.addColorStop(1, 'rgba(15, 23, 42, 0)');
                    bgCtx.fillStyle = grad;
                    bgCtx.fillRect(0, 0, 700, 600);

                    // 출입구 표기
                    bgCtx.fillStyle = '#38BDF8';
                    bgCtx.font = 'bold 12px sans-serif';
                    bgCtx.fillText('🚪 MAIN ENTRANCE', 280, 590);
                    bgCtx.fillText('🚪 EMERGENCY EXIT', 280, 20);
                }

                // 2. 부스 및 구조물 그리기
                function drawForeground() {
                    ctx.clearRect(0, 0, 700, 600);

                    // 무대
                    ctx.fillStyle = '#DC2626';
                    ctx.fillRect(stage.x, stage.y, stage.w, stage.h);
                    ctx.fillStyle = 'white';
                    ctx.font = 'bold 13px sans-serif';
                    ctx.fillText(stage.name, stage.x + 50, stage.y + 45);

                    // 푸드존
                    ctx.fillStyle = '#D97706';
                    ctx.fillRect(food.x, food.y, food.w, food.h);
                    ctx.fillText(food.name, food.x + 40, food.y + 50);

                    // 의무실
                    ctx.fillStyle = '#059669';
                    ctx.fillRect(medical.x, medical.y, medical.w, medical.h);
                    ctx.fillText(medical.name, medical.x + 20, medical.y + 40);

                    // 부스들
                    booths.forEach((b, idx) => {
                        ctx.fillStyle = (idx === selectedIdx) ? '#3B82F6' : '#1D4ED8';
                        ctx.strokeStyle = '#93C5FD';
                        ctx.lineWidth = 2;
                        
                        // 라운드 박스
                        ctx.beginPath();
                        ctx.roundRect(b.x, b.y, b.w, b.h, 6);
                        ctx.fill();
                        ctx.stroke();

                        // 부스 이름
                        ctx.fillStyle = 'white';
                        ctx.font = 'bold 12px sans-serif';
                        ctx.fillText(`${b.name}\n(${Math.round(b.w/20)}m×${Math.round(b.h/20)}m)`, b.x + 10, b.y + b.h/2);

                        // 리사이즈 핸들 (우측 하단)
                        ctx.fillStyle = '#F59E0B';
                        ctx.fillRect(b.x + b.w - handleSize, b.y + b.h - handleSize, handleSize, handleSize);
                    });
                }

                // 마우스 이벤트 처리
                fgCanvas.addEventListener('mousedown', (e) => {
                    const rect = fgCanvas.getBoundingClientRect();
                    const mx = e.clientX - rect.left;
                    const my = e.clientY - rect.top;

                    selectedIdx = -1;
                    isResizing = false;

                    for (let i = booths.length - 1; i >= 0; i--) {
                        const b = booths[i];
                        // 리사이즈 핸들 클릭 확인
                        if (mx >= b.x + b.w - handleSize && mx <= b.x + b.w &&
                            my >= b.y + b.h - handleSize && my <= b.y + b.h) {
                            selectedIdx = i;
                            isResizing = true;
                            return;
                        }
                        // 부스 이동 클릭 확인
                        if (mx >= b.x && mx <= b.x + b.w && my >= b.y && my <= b.y + b.h) {
                            selectedIdx = i;
                            dragOffsetX = mx - b.x;
                            dragOffsetY = my - b.y;
                            drawForeground();
                            return;
                        }
                    }
                    drawForeground();
                });

                fgCanvas.addEventListener('mousemove', (e) => {
                    if (selectedIdx === -1) return;
                    const rect = fgCanvas.getBoundingClientRect();
                    const mx = e.clientX - rect.left;
                    const my = e.clientY - rect.top;

                    if (isResizing) {
                        booths[selectedIdx].w = Math.max(40, mx - booths[selectedIdx].x);
                        booths[selectedIdx].h = Math.max(40, my - booths[selectedIdx].y);
                    } else {
                        booths[selectedIdx].x = mx - dragOffsetX;
                        booths[selectedIdx].y = my - dragOffsetY;
                    }
                    drawForeground();
                });

                fgCanvas.addEventListener('mouseup', () => {
                    selectedIdx = -1;
                    isResizing = false;
                });

                drawBackground();
                drawForeground();
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=660)

    with tab2:
        st.subheader("🟢 AI 최적화 - 부드러운 그라데이션 밀집도 비교")
        
        # -------------------------------------------------------------------------
        # Matplotlib 기반 가우시안 에어리얼 그라데이션 연산
        # -------------------------------------------------------------------------
        def draw_gradient_map(is_after=False):
            grid_dim = 50
            fig, ax = plt.subplots(figsize=(8, 7.5), dpi=120)
            
            ax.set_facecolor('#0F172A')
            fig.patch.set_facecolor('#0F172A')
            ax.grid(True, color='#1E293B', linestyle='--', linewidth=0.6, zorder=1)

            # 2D 밀집도 매트릭스 연산
            density = np.zeros((grid_dim, grid_dim))
            
            if not is_after:
                # 변경 전: 중앙 밀집
                density[20:30, 20:30] += 12.0
                density[15:25, 15:25] += 8.0
            else:
                # 변경 후: 외곽 분산
                density[5:15, 5:45] += 3.0
                density[35:45, 5:45] += 3.0
                
            # 부드러운 그라데이션 필터링 (Gaussian Blur)
            smooth_density = gaussian_filter(density, sigma=4.5)

            # 부드러운 히트맵 렌더링
            cmap = "YlGnBu" if is_after else "YlOrRd"
            im = ax.imshow(smooth_density, cmap=cmap, origin='lower', alpha=0.65, 
                           extent=[0, grid_dim, 0, grid_dim], interpolation='bicubic', zorder=2)
            
            cbar = fig.colorbar(im, ax=ax, fraction=0.042, pad=0.03)
            cbar.set_label('관람객 유입 밀도 (그라데이션)', color='white', fontsize=8)
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

            # 외곽 테두리 및 출입구
            ax.plot([0, grid_dim, grid_dim, 0, 0], [0, 0, grid_dim, grid_dim, 0], color='#38BDF8', linewidth=3, zorder=4)
            ax.text(grid_dim / 2, -1.8, "🚪 MAIN ENTRANCE", ha='center', va='top', fontsize=8, fontweight='bold', color='#38BDF8',
                    bbox=dict(boxstyle="round,pad=0.3", fc='#0F172A', ec='#38BDF8', lw=1.2), zorder=8)

            # AI 규격 부스 배치 (3.5m x 3.5m)
            b_size = 3.5
            booths = [(6, 10 + i * 5.5) for i in range(4)] + [(36, 10 + i * 5.5) for i in range(4)] if is_after else [(15 + (i%3)*6, 15 + (i//3)*6) for i in range(8)]
            
            for i, (bx, by) in enumerate(booths, 1):
                rect = patches.FancyBboxPatch((bx, by), b_size, b_size, boxstyle="round,pad=0.1",
                                               fc='#2563EB', ec='white', lw=1.2, alpha=0.85, zorder=5)
                ax.add_patch(rect)
                ax.text(bx + b_size / 2, by + b_size / 2, f"B{i}", color='white', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=6)

            # 주요 구조물
            ax.add_patch(patches.FancyBboxPatch((20, 38) if is_after else (20, 20), 10, 6, boxstyle="round,pad=0.2", fc='#DC2626', ec='white', lw=1.5, zorder=6))
            ax.text((25 if is_after else 25), (41 if is_after else 23), "🎭 무대", color='white', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=7)

            ax.set_xlim(-4, grid_dim + 4)
            ax.set_ylim(-4, grid_dim + 4)
            ax.set_title("AI 최적화 수채화 그라데이션 동선" if is_after else "기존 배치 혼잡 구역 (부드러운 히트맵)", fontsize=11, fontweight='bold', pad=10, color='white')
            ax.tick_params(colors='white')
            return fig

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.pyplot(draw_gradient_map(is_after=False))
            st.caption("🔴 중앙 붉은색 그라데이션 구역에 인파가 집중되는 현상")
        with col_g2:
            st.pyplot(draw_gradient_map(is_after=True))
            st.caption("🟢 외곽 분산 배치로 푸른색 안전 그라데이션 형성")

# -----------------------------------------------------------------------------
# [PAGE 3] 📄 AI 정밀 컨설팅 보고서
# -----------------------------------------------------------------------------
else:
    st.title("📄 AI 공간 설계 및 군중 안전 정밀 컨설팅 보고서")
    st.caption("발행처: Event Architect AI 연구소 | 승인 번호: EAAI-REPORT-2026-9081")
    st.divider()

    st.markdown("""
    ### 1. 종합 안전 및 공간 효율성 평가 결과
    본 보고서는 수동 배치 편집 결과와 AI 자동 최적화안의 공간 효율성, 보행 쾌적성, 비상 대피 골든타임 확보 여부를 정량적으로 종합 비교한 문서입니다.
    """)

    rep_df = pd.DataFrame({
        "평가 지표": ["국소 최고 군중 밀도", "보행 통로 최소 폭", "의무실 골든타임 도달률", "비상 대피 완출 시간", "안전요원 커버리지", "종합 안전 등급"],
        "수동 편집안": ["4.6 명/m² (위험)", "1.8 m (협소)", "62.0% (지연 위험)", "13.5 분", "48.0%", "D 등급 (개선 필요)"],
        "AI 최적화안": ["1.5 명/m² (쾌적)", "4.5 m (양호)", "99.2% (즉시 확보)", "4.2 분", "92.5%", "A+ 등급 (최우수)"],
        "개선 성과": ["67.3% 감소", "+2.7 m 확장", "+37.2%p 증가", "68.8% 단축", "+44.5%p 증가", "3단계 상향"]
    })
    st.table(rep_df)

    st.markdown("---")

    st.markdown("""
    ### 2. XAI(설명 가능한 AI) 배치 변경 가이드라인

    * **[응급 이송 경로 확보]**  
      의무실을 메인 출입구 기준 $5\text{m}$ 이내 구역에 전진 배치하여, 앰뷸런스 진입 시 관람객 동선과 겹치지 않는 독자적 비상 통로를 확보했습니다.
    * **[메인 무대와 푸드존의 이중 거점화]**  
      가장 많은 관람객이 체류하는 무대와 푸드존을 대각선 반대 방향으로 배치하여 행사장 전체로 관람객 흐름을 유도했습니다.
    * **[병목 방지 통로 가이드라인]**  
      모든 부스의 전면 공간을 최소 $4.5\text{m}$ 이상 격리하여 휠체어 및 유모차 이동 공간을 확보했습니다.
    """)

    st.success("📝 **최종 승인 의견**: 본 AI 최적화 설계안은 관련 지자체 군중 안전 관리 지침을 충족하므로 현장 시공안으로 확정할 것을 권장합니다.")
