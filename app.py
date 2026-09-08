import hashlib
import json
import os
import plotly.graph_objects as go
import streamlit as st

# 1. 사용자 정보 저장 및 불러오기 (JSON 기반)
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


# 2. 배치도 생성 함수 (Plotly rx, ry 에러 수정 완료)
def create_advanced_floor_plan(venue_shape, event_type, attendees):
    fig = go.Figure()

    # 외곽 레이아웃 (rx, ry 파라미터 제외)
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=100,
        y1=100,
        line=dict(color="#38BDF8", width=3),
        fillcolor="#1E293B",
    )

    # 무대 / 주요 구역
    if event_type == "세미나/강연":
        fig.add_shape(
            type="rect",
            x0=30,
            y0=80,
            x1=70,
            y1=95,
            line=dict(color="#F59E0B", width=2),
            fillcolor="#78350F",
        )
        fig.add_trace(
            go.Scatter(
                x=[50],
                y=[87.5],
                text=["무대 (Stage)"],
                mode="text",
                textfont=dict(color="#FFFFFF", size=14),
                showlegend=False,
            )
        )

    # 참석자 좌석 배치 예시
    cols = 10
    display_count = min(attendees, 80)
    x_coords, y_coords = [], []

    for i in range(display_count):
        r = i // cols
        c = i % cols
        x_coords.append(12 + c * 8.5)
        y_coords.append(15 + r * 7.5)

    fig.add_trace(
        go.Scatter(
            x=x_coords,
            y=y_coords,
            mode="markers",
            marker=dict(size=10, color="#38BDF8"),
            name="좌석",
        )
    )

    fig.update_layout(
        title=f"{venue_shape} 형태 - {event_type} 배치도 (참석 인원: {attendees}명)",
        xaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
        width=700,
        height=600,
        plot_bgcolor="#0F172A",
        paper_bgcolor="#0F172A",
        font=dict(color="#F8FAFC"),
    )

    return fig


# 3. 로그인 / 회원가입 화면
def auth_screen():
    st.title("🔒 Vibe Venue - 로그인 / 회원가입")

    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    users = load_users()

    with tab1:
        st.subheader("로그인")
        login_id = st.text_input("아이디", key="login_id")
        login_pw = st.text_input("비밀번호", type="password", key="login_pw")

        if st.button("로그인", use_container_width=True):
            hashed = hash_password(login_pw)
            if login_id in users and users[login_id] == hashed:
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_id
                st.success(f"{login_id}님 환영합니다!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    with tab2:
        st.subheader("회원가입")
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
                    "회원가입이 완료되었습니다! 로그인 탭에서 로그인해 주세요."
                )


# 4. 메인 애플리케이션 화면
def main_app():
    st.sidebar.write(f"👤 **{st.session_state['username']}** 님")
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    st.title("📐 스마트 공간 배치도 생성기")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("설정 옵션")
        venue_shape = st.selectbox(
            "장소 형태", ["직사각형", "정사각형", "L자형"]
        )
        event_type = st.selectbox(
            "행사 유형", ["세미나/강연", "연회/파티", "전시회"]
        )
        attendees = st.number_input(
            "참석 인원 수", min_value=1, max_value=500, value=50
        )

    with col2:
        st.subheader("배치도 시각화")
        fig_plan = create_advanced_floor_plan(
            venue_shape, event_type, attendees
        )
        st.plotly_chart(fig_plan, use_container_width=True)


# 5. 세션 상태 초기화 및 실행 진입점
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    auth_screen()
