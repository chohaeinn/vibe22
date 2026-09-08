import hashlib
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. 페이지 및 기본 설정
st.set_page_config(
    page_title="Vibe Venue - 스마트 공간 대시보드",
    page_icon="📐",
    layout="wide",
)

USER_DB_FILE = "users.json"


# 2. 로그인/회원가입 계정 관리
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


# 3. 디테일한 평면도 생성 (Plotly rx, ry 오류 완벽 수정)
def create_advanced_floor_plan(
    venue_shape,
    event_type,
    attendees,
    include_vip=True,
    include_catering=True,
):
    fig = go.Figure()

    # (1) 공간 외벽
    if venue_shape == "L자형":
        fig.add_shape(
            type="path",
            path="M 0,0 L 100,0 L 100,50 L 50,50 L 50,100 L 0,100 Z",
            line=dict(color="#0284C7", width=4),
            fillcolor="#1E293B",
        )
    else:
        fig.add_shape(
            type="rect",
            x0=0,
            y0=0,
            x1=100,
            y1=100,
            line=dict(color="#0284C7", width=4),
            fillcolor="#1E293B",
        )

    # (2) 메인 입구 및 안내 데스크 (하단)
    fig.add_shape(
        type="rect",
        x0=38,
        y0=0,
        x1=62,
        y1=10,
        line=dict(color="#10B981", width=2),
        fillcolor="#064E3B",
    )
    fig.add_trace(
        go.Scatter(
            x=[50],
            y=[5],
            text=["🚪 메인 입구 & 안내 데스크"],
            mode="text",
            textfont=dict(color="#A7F3D0", size=12),
            showlegend=False,
        )
    )

    # (3) 화장실 (남/여) (우측 하단)
    fig.add_shape(
        type="rect",
        x0=82,
        y0=2,
        x1=98,
        y1=18,
        line=dict(color="#6366F1", width=2),
        fillcolor="#312E81",
    )
    fig.add_trace(
        go.Scatter(
            x=[90],
            y=[10],
            text=["🚻 화장실\n(남/여)"],
            mode="text",
            textfont=dict(color="#E0E7FF", size=11),
            showlegend=False,
        )
    )

    # (4) 비상구 표시 (3개소)
    exits = [(0, 50, "← 비상구"), (100, 50, "비상구 →"), (50, 100, "↑ 비상구")]
    for ex_x, ex_y, label in exits:
        if venue_shape == "L자형" and ex_x == 100 and ex_y > 50:
            continue
        fig.add_trace(
            go.Scatter(
                x=[ex_x],
                y=[ex_y],
                mode="text",
                text=[f"🚨 {label}"],
                textfont=dict(color="#EF4444", size=11),
                showlegend=False,
            )
        )

    # (5) 선택 옵션: 케이터링 존 (좌측 하단)
    if include_catering:
        fig.add_shape(
            type="rect",
            x0=2,
            y0=2,
            x1=22,
            y1=18,
            line=dict(color="#F59E0B", width=2),
            fillcolor="#78350F",
        )
        fig.add_trace(
            go.Scatter(
                x=[12],
                y=[10],
                text=["☕ 케이터링\n& 스낵존"],
                mode="text",
                textfont=dict(color="#FDE68A", size=11),
                showlegend=False,
            )
        )

    # (6) 선택 옵션: VIP 라운지 (좌측 상단)
    if include_vip:
        fig.add_shape(
            type="rect",
            x0=2,
            y0=80,
            x1=22,
            y1=98,
            line=dict(color="#EC4899", width=2),
            fillcolor="#831843",
        )
        fig.add_trace(
            go.Scatter(
                x=[12],
                y=[89],
                text=["👑 VIP 라운지"],
                mode="text",
                textfont=dict(color="#FBCFE8", size=11),
                showlegend=False,
            )
        )

    # (7) 행사 유형별 메인 존 및 배치
    if event_type == "세미나/강연":
        # 메인 무대
        fig.add_shape(
            type="rect",
            x0=28,
            y0=78,
            x1=72,
            y1=95,
            line=dict(color="#3B82F6", width=2),
            fillcolor="#1E3A8A",
        )
        fig.add_trace(
            go.Scatter(
                x=[50],
                y=[86.5],
                text=["🎤 MAIN STAGE (강연 무대 & 대형 스크린)"],
                mode="text",
                textfont=dict(color="#93C5FD", size=12),
                showlegend=False,
            )
        )

        # 객석 배치
        cols = 10
        max_seats = min(attendees, 80)
        x_coords, y_coords = [], []
        for i in range(max_seats):
            r = i // cols
            c = i % cols
            x_coords.append(22 + c * 6)
            y_coords.append(68 - r * 5)

        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                mode="markers",
                marker=dict(size=8, color="#38BDF8", symbol="square"),
                name="일반 좌석",
            )
        )

    elif event_type == "연회/파티":
        # 메인 댄스/이벤트 플로어
        fig.add_shape(
            type="rect",
            x0=40,
            y0=40,
            x1=60,
            y1=60,
            line=dict(color="#F43F5E", width=2),
            fillcolor="#881337",
        )
        fig.add_trace(
            go.Scatter(
                x=[50],
                y=[50],
                text=["💃 메인 플로어"],
                mode="text",
                textfont=dict(color="#FECDD3", size=12),
                showlegend=False,
            )
        )

        # 원형 연회 테이블
        table_centers = [
            (25, 30),
            (25, 70),
            (75, 30),
            (75, 70),
            (30, 50),
            (70, 50),
            (50, 78),
        ]
        for idx, (tx, ty) in enumerate(table_centers):
            fig.add_shape(
                type="circle",
                x0=tx - 6,
                y0=ty - 6,
                x1=tx + 6,
                y1=ty + 6,
                line=dict(color="#F59E0B", width=2),
                fillcolor="#451A03",
            )
            fig.add_trace(
                go.Scatter(
                    x=[tx],
                    y=[ty],
                    text=[f"T-{idx+1}"],
                    mode="text",
                    textfont=dict(color="#FDE68A", size=11),
                    showlegend=False,
                )
            )

    else:  # 전시회
        # 전시 부스 배치
        booths = [
            (25, 65, "A-1"),
            (45, 65, "A-2"),
            (65, 65, "A-3"),
            (25, 35, "B-1"),
            (45, 35, "B-2"),
            (65, 35, "B-3"),
        ]
        for bx, by, bname in booths:
            fig.add_shape(
                type="rect",
                x0=bx - 7,
                y0=by - 7,
                x1=bx + 7,
                y1=by + 7,
                line=dict(color="#10B981", width=2),
                fillcolor="#064E3B",
            )
            fig.add_trace(
                go.Scatter(
                    x=[bx],
                    y=[by],
                    text=[f"🏛️ 부스\n{bname}"],
                    mode="text",
                    textfont=dict(color="#D1FAE5", size=11),
                    showlegend=False,
                )
            )

    fig.update_layout(
        title=dict(
            text=f"📐 [상세 평면도] {venue_shape} | {event_type} (참석: {attendees}명)",
            font=dict(size=16, color="#F8FAFC"),
        ),
        xaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(
            range=[-5, 105],
            showgrid=False,
            zeroline=False,
            visible=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        width=800,
        height=650,
        plot_bgcolor="#0F172A",
        paper_bgcolor="#0F172A",
        margin=dict(l=10, r=10, t=40, b=10),
    )

    return fig


# 4. 로그인 / 회원가입 화면
def auth_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 Vibe Venue 대시보드")
        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
        users = load_users()

        with tab1:
            login_id = st.text_input("아이디", key="login_id")
            login_pw = st.text_input("비밀번호", type="password", key="login_pw")

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
                    st.warning("아이디와 비밀번호를 모두 입력해주세요.")
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


# 5. 메인 앱 대시보드
def main_app():
    st.sidebar.title("🎛️ 공간 옵션 설정")
    st.sidebar.write(f"👤 **{st.session_state['username']}** 님")

    if st.sidebar.button("🚪 로그아웃", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    st.sidebar.markdown("---")
    venue_shape = st.sidebar.selectbox(
        "장소 형태", ["직사각형", "정사각형", "L자형"]
    )
    event_type = st.sidebar.selectbox(
        "행사 유형", ["세미나/강연", "연회/파티", "전시회"]
    )
    attendees = st.sidebar.slider(
        "참석 인원 수", min_value=10, max_value=300, value=80, step=10
    )

    st.sidebar.markdown("---")
    include_vip = st.sidebar.checkbox("👑 VIP 라운지 포함", value=True)
    include_catering = st.sidebar.checkbox("☕ 케이터링 존 포함", value=True)

    # 지표 요약 대시보드
    st.title("📊 Vibe Venue - 통합 공간 관리 대시보드")

    m1, m2, m3, m4 = st.columns(4)
    total_area = 500 if venue_shape != "L자형" else 375
    m1.metric("총 공간 면적", f"{total_area} ㎡")
    m2.metric("예상 참석 인원", f"{attendees} 명")
    m3.metric("밀도 지수", f"{round(attendees / (total_area / 100), 1)} 명/100㎡")
    m4.metric("비상 대피로", "🟢 3개소 확보")

    st.markdown("---")

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(
        ["🗺️ 상세 평면도", "📈 공간 점유율 분석", "📋 구역 명세서"]
    )

    with tab1:
        col_map, col_legend = st.columns([3, 1])
        with col_map:
            fig_plan = create_advanced_floor_plan(
                venue_shape,
                event_type,
                attendees,
                include_vip,
                include_catering,
            )
            st.plotly_chart(fig_plan, use_container_width=True)

        with col_legend:
            st.markdown("### 💡 주요 구역 범례")
            st.markdown(
                """
            - **🚪 메인 입구**: 출입 및 안내
            - **🚻 화장실**: 남/여/장애인 (우측 하단)
            - **🚨 비상구**: 총 3개소 (좌/우/상단)
            """
            )
            if include_catering:
                st.markdown("- **☕ 케이터링**: 다과 및 스낵존")
            if include_vip:
                st.markdown("- **👑 VIP 라운지**: 귀빈 전용 대기실")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📊 구역별 면적 점유율")
            df_pie = pd.DataFrame(
                {
                    "구역": [
                        "메인 이벤트존",
                        "통로 및 이동 동선",
                        "화장실 및 안내데스크",
                        "편의시설",
                    ],
                    "비율": [50, 25, 15, 10],
                }
            )
            fig_pie = px.pie(
                df_pie,
                names="구역",
                values="비율",
                color_discrete_sequence=px.colors.sequential.Darkmint,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            st.subheader("⏱️ 시간대별 예상 혼잡도")
            df_bar = pd.DataFrame(
                {
                    "시간대": ["09:00", "11:00", "13:00", "15:00", "17:00"],
                    "혼잡도(%)": [30, 85, 60, 95, 40],
                }
            )
            fig_bar = px.bar(
                df_bar,
                x="시간대",
                y="혼잡도(%)",
                color="혼잡도(%)",
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        st.subheader("📋 전체 구역 세부 명세")
        table_data = [
            {
                "구역": "메인존",
                "위치": "중앙/상단",
                "수용 인원": f"최대 {attendees}명",
                "설비": "무대, 음향, 대형 스크린",
            },
            {
                "구역": "안내 데스크",
                "위치": "하단 입구",
                "수용 인원": "운영진 4~6명",
                "설비": "태블릿 등록기, 안내 배너",
            },
            {
                "구역": "화장실",
                "위치": "하단 우측",
                "수용 인원": "동시 10명",
                "설비": "남/여 구분 세면대",
            },
            {
                "구역": "비상구",
                "위치": "좌/우/상단 3곳",
                "수용 인원": "대피용",
                "설비": "유도등, 소화기",
            },
        ]
        if include_catering:
            table_data.append(
                {
                    "구역": "케이터링존",
                    "위치": "하단 좌측",
                    "수용 인원": "15명",
                    "설비": "커피머신, 정수기, 바 테이블",
                }
            )
        if include_vip:
            table_data.append(
                {
                    "구역": "VIP 라운지",
                    "위치": "상단 좌측",
                    "수용 인원": "10명",
                    "설비": "고급 소파, 독립 방음 벽체",
                }
            )

        st.dataframe(pd.DataFrame(table_data), use_container_width=True)


# 6. 진입점
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    auth_screen()
