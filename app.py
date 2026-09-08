import hashlib
import json
import math
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 세션 초기화
# ---------------------------------------------------------
st.set_page_config(
    page_title="Vibe Venue - Pro 공간 설계 대시보드",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

USER_DB_FILE = "users.json"


def load_users():
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_users(users):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------------------------------------
# 2. 둥근 사각형 SVG Path 생성 함수 (Plotly rx/ry 에러 방지)
# ---------------------------------------------------------
def get_rounded_rect_path(x0, y0, x1, y1, r=2):
    w = abs(x1 - x0)
    h = abs(y1 - y0)
    r = min(r, w / 2, h / 2)
    return (
        f"M {x0+r},{y0} "
        f"L {x1-r},{y0} Q {x1},{y0} {x1},{y0+r} "
        f"L {x1},{y1-r} Q {x1},{y1} {x1-r},{y1} "
        f"L {x0+r},{y1} Q {x0},{y1} {x0},{y1-r} "
        f"L {x0},{y0+r} Q {x0},{y0} {x0+r},{y0} Z"
    )


# ---------------------------------------------------------
# 3. 고도화된 건축형 평면도 생성 엔진
# ---------------------------------------------------------
def draw_pro_floor_plan(opts):
    fig = go.Figure()

    # 테마 색상 설정
    theme_colors = {
        "Dark Tech": {
            "bg": "#0F172A",
            "wall": "#0284C7",
            "wall_fill": "#1E293B",
            "text": "#F8FAFC",
            "grid": "#334155",
        },
        "Blueprint": {
            "bg": "#1E3A8A",
            "wall": "#93C5FD",
            "wall_fill": "#1E40AF",
            "text": "#FFFFFF",
            "grid": "#3B82F6",
        },
        "Modern Light": {
            "bg": "#F8FAFC",
            "wall": "#334155",
            "wall_fill": "#E2E8F0",
            "text": "#0F172A",
            "grid": "#CBD5E1",
        },
    }
    tc = theme_colors.get(
        opts["theme"], theme_colors["Dark Tech"]
    )

    # (1) 건물 외벽 (Shape)
    if opts["shape"] == "L자형":
        path = "M 0,0 L 100,0 L 100,50 L 50,50 L 50,100 L 0,100 Z"
    elif opts["shape"] == "U자형":
        path = "M 0,0 L 100,0 L 100,100 L 70,100 L 70,30 L 30,30 L 30,100 L 0,100 Z"
    else:  # 직사각형 / 정사각형
        path = get_rounded_rect_path(0, 0, 100, 100, r=1)

    fig.add_shape(
        type="path",
        path=path,
        line=dict(color=tc["wall"], width=4),
        fillcolor=tc["wall_fill"],
    )

    # (2) 부속 구역 그리기 전용 헬퍼 함수
    def add_zone(
        x0,
        y0,
        x1,
        y1,
        title,
        icon,
        border_color,
        fill_color,
        text_color="#FFFFFF",
    ):
        fig.add_shape(
            type="path",
            path=get_rounded_rect_path(x0, y0, x1, y1, r=2),
            line=dict(color=border_color, width=2),
            fillcolor=fill_color,
        )
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2,
            text=f"<b>{icon} {title}</b>",
            showarrow=False,
            font=dict(color=text_color, size=11),
            align="center",
        )

    # (3) 구역배치 - 안내/등록 데스크
    if opts["show_reg_desk"]:
        add_zone(
            35,
            2,
            65,
            12,
            "안내 / 등록 데스크",
            "📋",
            "#10B981",
            "#064E3B",
            "#A7F3D0",
        )

    # (4) 구역배치 - 화장실
    if opts["restroom_pos"] == "우측 하단":
        add_zone(
            80, 2, 98, 18, "남/여 화장실", "🚻", "#8B5CF6", "#4C1D95", "#DDD6FE"
        )
    elif opts["restroom_pos"] == "좌측 하단":
        add_zone(
            2, 2, 20, 18, "남/여 화장실", "🚻", "#8B5CF6", "#4C1D95", "#DDD6FE"
        )

    # (5) 구역배치 - VIP 라운지
    if opts["show_vip"]:
        add_zone(
            2,
            80,
            24,
            98,
            "VIP 라운지",
            "👑",
            "#EC4899",
            "#831843",
            "#FBCFE8",
        )

    # (6) 구역배치 - 케이터링 & 바
    if opts["show_catering"]:
        add_zone(
            76,
            80,
            98,
            98,
            "케이터링 & 바",
            "☕",
            "#F59E0B",
            "#78350F",
            "#FDE68A",
        )

    # (7) 구역배치 - 포토존
    if opts["show_photo"]:
        add_zone(
            2,
            40,
            18,
            60,
            "포토존",
            "📸",
            "#06B6D4",
            "#164E63",
            "#CFFAFE",
        )

    # (8) 구역배치 - 음향/조명 제어실 (Console)
    if opts["show_control"]:
        add_zone(
            38,
            15,
            62,
            23,
            "음향 / 조명 제어석",
            "🜲",
            "#64748B",
            "#334155",
            "#E2E8F0",
        )

    # (9) 무대(Stage) 위치 설정
    if opts["stage_pos"] != "없음":
        st_coords = {
            "상단": (25, 82, 75, 98),
            "중앙": (35, 42, 65, 58),
            "좌측": (2, 30, 18, 70),
        }
        sx0, sy0, sx1, sy1 = st_coords[opts["stage_pos"]]
        add_zone(
            sx0,
            sy0,
            sx1,
            sy1,
            "MAIN STAGE",
            "🎤",
            "#3B82F6",
            "#1E3A8A",
            "#93C5FD",
        )

    # (10) 좌석/테이블/부스 세부 배치 연산
    layout_style = opts["layout_style"]
    count = min(opts["attendees"], 120)

    if layout_style == "강의식 (Theater)":
        cols = 10
        for i in range(count):
            r, c = i // cols, i % cols
            x = 22 + c * 6
            y = 72 - r * 4.5
            if (
                opts["stage_pos"] == "상단" and y > 78
            ):  # 무대와 겹침 방지
                continue
            fig.add_shape(
                type="rect",
                x0=x - 2,
                y0=y - 1.5,
                x1=x + 2,
                y1=y + 1.5,
                line=dict(color="#38BDF8", width=1),
                fillcolor="#0284C7",
            )

    elif layout_style == "연회식 (Round Table)":
        tables = [
            (30, 35),
            (50, 35),
            (70, 35),
            (30, 60),
            (50, 60),
            (70, 60),
            (40, 78),
            (60, 78),
        ]
        for idx, (tx, ty) in enumerate(tables):
            fig.add_shape(
                type="circle",
                x0=tx - 5,
                y0=ty - 5,
                x1=tx + 5,
                y1=ty + 5,
                line=dict(color="#F59E0B", width=2),
                fillcolor="#451A03",
            )
            fig.add_annotation(
                x=tx,
                y=ty,
                text=f"T-{idx+1}",
                showarrow=False,
                font=dict(color="#FDE68A", size=10),
            )

    elif layout_style == "전시 부스 (Exhibition)":
        booths = [
            (30, 70, "A-1"),
            (50, 70, "A-2"),
            (70, 70, "A-3"),
            (30, 45, "B-1"),
            (50, 45, "B-2"),
            (70, 45, "B-3"),
        ]
        for bx, by, bname in booths:
            add_zone(
                bx - 7,
                by - 6,
                bx + 7,
                by + 6,
                f"부스 {bname}",
                "🏛️",
                "#10B981",
                "#064E3B",
                "#D1FAE5",
            )

    elif layout_style == "ㄷ자형 회의 (U-Shape)":
        u_pts = [
            (25, y) for y in range(30, 75, 6)
        ] + [
            (x, 30) for x in range(25, 78, 6)
        ] + [
            (75, y) for y in range(30, 75, 6)
        ]
        for px_pos, py_pos in u_pts:
            fig.add_shape(
                type="rect",
                x0=px_pos - 1.8,
                y0=py_pos - 1.8,
                x1=px_pos + 1.8,
                y1=py_pos + 1.8,
                line=dict(color="#A855F7", width=1),
                fillcolor="#6B21A8",
            )

    # (11) 동선 및 비상구 표시
    if opts["show_routes"]:
        # 비상구 라벨
        exits = [(50, 0, "메인 출입구 🚪"), (0, 50, "🚨 비상구 A"), (100, 50, "🚨 비상구 B")]
        for ex, ey, elabel in exits:
            fig.add_annotation(
                x=ex,
                y=ey,
                text=elabel,
                showarrow=True,
                arrowhead=2,
                arrowcolor="#EF4444",
                font=dict(color="#EF4444", size=11),
                bgcolor=tc["bg"],
            )

    # 레이아웃 스타일 적용
    fig.update_layout(
        title=dict(
            text=f"📐 [도면] {opts['shape']} | {opts['layout_style']} (수용: {opts['attendees']}명)",
            font=dict(size=16, color=tc["text"]),
        ),
        xaxis=dict(
            range=[-8, 108],
            showgrid=opts["show_grid"],
            gridcolor=tc["grid"],
            zeroline=False,
            visible=opts["show_grid"],
        ),
        yaxis=dict(
            range=[-8, 108],
            showgrid=opts["show_grid"],
            gridcolor=tc["grid"],
            zeroline=False,
            visible=opts["show_grid"],
            scaleanchor="x",
            scaleratio=1,
        ),
        width=850,
        height=680,
        plot_bgcolor=tc["bg"],
        paper_bgcolor=tc["bg"],
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


# ---------------------------------------------------------
# 4. 로그인 / 회원가입 UI
# ---------------------------------------------------------
def auth_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 Vibe Venue 로그인")
        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
        users = load_users()

        with tab1:
            login_id = st.text_input("아이디", key="login_id")
            login_pw = st.text_input(
                "비밀번호", type="password", key="login_pw"
            )

            if st.button("로그인", use_container_width=True, type="primary"):
                hashed = hash_password(login_pw)
                if login_id in users and users[login_id] == hashed:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = login_id
                    st.success(f"{login_id}님 환영합니다!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

        with tab2:
            new_id = st.text_input("새 아이디", key="new_id")
            new_pw = st.text_input("새 비밀번호", type="password", key="new_pw")
            new_pw_confirm = st.text_input(
                "비밀번호 확인", type="password", key="new_pw_confirm"
            )

            if st.button("회원가입 완료", use_container_width=True):
                if not new_id or not new_pw:
                    st.warning("아이디와 비밀번호를 입력해주세요.")
                elif new_id in users:
                    st.warning("이미 존재하는 아이디입니다.")
                elif new_pw != new_pw_confirm:
                    st.error("비밀번호가 일치하지 않습니다.")
                else:
                    users[new_id] = hash_password(new_pw)
                    save_users(users)
                    st.success(
                        "회원가입 완료! 로그인 탭에서 로그인해 주세요."
                    )


# ---------------------------------------------------------
# 5. 메인 대시보드
# ---------------------------------------------------------
def main_app():
    st.sidebar.title("🎛️ 커스텀 공간 커스텀 설정")
    st.sidebar.write(f"👤 사용자: **{st.session_state['username']}**")

    if st.sidebar.button("🚪 로그아웃", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    st.sidebar.markdown("---")

    # [옵션 그룹 1] 기본 공간 구조
    st.sidebar.subheader("1. 공간 구조 및 규모")
    shape = st.sidebar.selectbox(
        "장소 형태", ["직사각형", "정사각형", "L자형", "U자형"]
    )
    width = st.sidebar.slider(
        "가로 길이 (m)", min_value=10, max_value=50, value=25
    )
    height = st.sidebar.slider(
        "세로 길이 (m)", min_value=10, max_value=50, value=20
    )
    attendees = st.sidebar.number_input(
        "목표 참석 인원 (명)", min_value=10, max_value=300, value=80, step=10
    )

    # [옵션 그룹 2] 배치 스타일
    st.sidebar.subheader("2. 내부 배치 모드")
    layout_style = st.sidebar.selectbox(
        "좌석 및 부스 배치",
        [
            "강의식 (Theater)",
            "연회식 (Round Table)",
            "전시 부스 (Exhibition)",
            "ㄷ자형 회의 (U-Shape)",
        ],
    )
    stage_pos = st.sidebar.selectbox(
        "메인 무대 위치", ["상단", "중앙", "좌측", "없음"]
    )

    # [옵션 그룹 3] 부속 구역 토글
    st.sidebar.subheader("3. 부속 구역 옵션")
    show_reg_desk = st.sidebar.checkbox("📋 안내/등록 데스크", value=True)
    restroom_pos = st.sidebar.selectbox(
        "🚻 화장실 위치", ["우측 하단", "좌측 하단", "외부/없음"]
    )
    show_vip = st.sidebar.checkbox("👑 VIP 라운지", value=True)
    show_catering = st.sidebar.checkbox("☕ 케이터링 & 바", value=True)
    show_photo = st.sidebar.checkbox("📸 포토존 / 이벤트 존", value=False)
    show_control = st.sidebar.checkbox("🜲 음향/조명 제어석", value=True)

    # [옵션 그룹 4] 시각화 및 테마
    st.sidebar.subheader("4. 도면 시각화 설정")
    show_routes = st.sidebar.checkbox("🚨 동선 및 비상구 표시", value=True)
    show_grid = st.sidebar.checkbox("📐 모눈종이 그리드", value=True)
    theme = st.sidebar.selectbox(
        "🎨 도면 테마", ["Dark Tech", "Blueprint", "Modern Light"]
    )

    # 옵션 딕셔너리 구성
    opts = {
        "shape": shape,
        "width": width,
        "height": height,
        "attendees": attendees,
        "layout_style": layout_style,
        "stage_pos": stage_pos,
        "show_reg_desk": show_reg_desk,
        "restroom_pos": restroom_pos,
        "show_vip": show_vip,
        "show_catering": show_catering,
        "show_photo": show_photo,
        "show_control": show_control,
        "show_routes": show_routes,
        "show_grid": show_grid,
        "theme": theme,
    }

    # 대시보드 상단 요약
    st.title("🏛️ Pro 공간 설계 & 배치 대시보드")

    area = width * height
    if shape == "L자형":
        area *= 0.75
    elif shape == "U자형":
        area *= 0.70

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📐 총 면적", f"{int(area)} ㎡ ({int(area*0.3025)}평)")
    col2.metric("👥 계획 인원", f"{attendees} 명")
    col3.metric("📏 1인당 점유 면적", f"{round(area/attendees, 2)} ㎡/명")
    col4.metric(
        "🛡️ 안전 기준",
        "🟢 적합" if (area / attendees) >= 1.2 else "🔴 혼잡 우려",
    )

    st.markdown("---")

    # 메인 탭
    tab1, tab2, tab3 = st.tabs(
        [
            "🗺️ 건축형 평면 도면",
            "📊 공간 활용도 분석",
            "📋 구역 및 장비 명세",
        ]
    )

    with tab1:
        fig = draw_pro_floor_plan(opts)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("💡 구역별 면적 배분")
            df_pie = pd.DataFrame(
                {
                    "구역": [
                        "메인 행사장",
                        "통로 및 동선",
                        "부속 편의시설",
                        "여유 공간",
                    ],
                    "비율": [55, 25, 12, 8],
                }
            )
            fig_pie = px.pie(
                df_pie,
                names="구역",
                values="비율",
                color_discrete_sequence=px.colors.qualitative.Set3,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("⏱️ 시간대별 예상 이동 인량")
            df_bar = pd.DataFrame(
                {
                    "시간": [
                        "행사 1시간 전",
                        "개회 직전",
                        "메인 세션",
                        "휴식 시간",
                        "종료 후",
                    ],
                    "유입 인원(명)": [
                        int(attendees * 0.2),
                        int(attendees * 0.8),
                        attendees,
                        int(attendees * 0.9),
                        int(attendees * 0.3),
                    ],
                }
            )
            fig_bar = px.bar(
                df_bar,
                x="시간",
                y="유입 인원(명)",
                color="유입 인원(명)",
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        st.subheader("📋 구역 배치 상세 명세서")
        specs = [
            {
                "구역명": "메인 이벤트존",
                "배치 유형": layout_style,
                "권장 수용": f"{attendees}명",
                "비고": f"무대 위치: {stage_pos}",
            },
            {
                "구역명": "안내/등록 데스크",
                "배치 유형": "출입구 직련",
                "권장 수용": "4명",
                "비고": "등록 태블릿 및 명찰 배부",
            },
        ]
        if show_vip:
            specs.append(
                {
                    "구역명": "VIP 라운지",
                    "배치 유형": "독립 구획",
                    "권장 수용": "8~10명",
                    "비고": "고급 소파 및 음료 서비스",
                }
            )
        if show_catering:
            specs.append(
                {
                    "구역명": "케이터링 존",
                    "배치 유형": "스탠딩 테이블",
                    "권장 수용": "15명 동시",
                    "비고": "다과 및 머신 배치",
                }
            )
        if show_control:
            specs.append(
                {
                    "구역명": "음향/조명 제어석",
                    "배치 유형": "콘솔 테이블",
                    "권장 수용": "2명 엔지니어",
                    "비고": "무대 직시 가능 위치",
                }
            )

        st.dataframe(pd.DataFrame(specs), use_container_width=True)


# ---------------------------------------------------------
# 6. 진입점
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    auth_screen()
