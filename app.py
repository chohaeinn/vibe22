import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="AI 행사장 설계 디자이너", page_icon="🎪", layout="wide")

st.title("🎪 AI 행사장 설계 디자이너")
st.markdown("행사의 기본 정보를 입력하면 최적의 공간 배치, 혼잡도 시뮬레이션, 그리고 모두를 위한 유니버설 설계도를 제안합니다.")

# 사이드바: 사용자 입력 폼
with st.sidebar:
    st.header("📋 행사 기본 정보 입력")
    event_type = st.selectbox("행사 유형", ["컨퍼런스/학술대회", "공연/콘서트", "전시회", "네트워킹 파티", "지역 축제", "기타"])
    attendees = st.number_input("예상 인원수 (명)", min_value=10, max_value=50000, step=50, value=100)
    duration = st.slider("진행 시간 (시간)", min_value=1, max_value=24, value=4)
    atmosphere = st.selectbox("원하는 분위기", ["차분하고 전문적인", "활기차고 신나는", "고급스럽고 우아한", "자유롭고 창의적인"])
    fee = st.number_input("입장료 (원, 무료는 0)", min_value=0, step=1000, value=0)
    age_group = st.multiselect("예상 연령대", ["10대 이하", "20대", "30대", "40대", "50대 이상"], default=["20대", "30대"])
    extra_req = st.text_area("추가 요구사항 (예: 휠체어 경사로 필수, 케이터링 공간 필요 등)")
    
    submit_btn = st.button("설계도 생성하기")

# 메인 화면: 결과 출력
if submit_btn:
    st.success("데이터 분석 완료! 최적의 행사장 설계를 확인하세요.")
    
    # 4개의 탭으로 나누어 정보 제공
    tab1, tab2, tab3, tab4 = st.tabs(["📊 공간 배치도", "🚶 혼잡도 시뮬레이션", "🤝 모두를 위한 설계 (배리어 프리)", "💡 추가 추천 사항"])
    
    with tab1:
        st.subheader("최적의 행사장 기본 설계")
        col1, col2, col3 = st.columns(3)
        # 인원수에 따른 단순 계산 로직 (예시)
        required_area = attendees * 1.5
        staff_needed = (attendees // 20) + 2
        
        col1.metric("권장 최소 공간 면적", f"{required_area:,.0f} ㎡")
        col2.metric("권장 최소 스태프 수", f"{staff_needed} 명")
        col3.metric("휴게 공간 권장 비율", "전체 면적의 20%")
        
        st.markdown("### 🗺️ 구역별 공간 배치 가이드")
        st.info("입력하신 행사 유형에 맞춘 권장 공간 할당 비율입니다.")
        
        # 공간 비율 더미 데이터 시각화
        layout_data = pd.DataFrame({
            "구역": ["메인 행사/무대", "대기 및 접수처", "휴게 및 식음료", "화장실 및 기타 편의시설"],
            "비율(%)": [50, 15, 25, 10]
        })
        st.bar_chart(layout_data.set_index("구역"))

    with tab2:
        st.subheader("혼잡도 시뮬레이션 및 동선 안내")
        st.markdown("**예상 최대 혼잡 시간대:** 행사 시작 30분 전 및 종료 직후")
        
        # 혼잡도 게이지바 (임의의 로직 적용)
        congestion_level = min(attendees / 1000, 1.0)
        st.progress(congestion_level)
        if congestion_level > 0.7:
            st.warning("⚠️ 인구 밀집도가 높습니다. 입구와 출구를 반드시 분리하고, 비상 대피로를 2곳 이상 확보하세요.")
        else:
            st.info("✅ 쾌적한 행사 진행이 가능한 인원입니다. 단일 출입구로도 운영이 가능합니다.")
            
    with tab3:
        st.subheader("모두가 참여할 수 있는 행사 (유니버설 디자인)")
        st.markdown("- **이동 편의성:** 전 구역 단차 제거 및 휠체어/유모차 전용 통로(폭 1.2m 이상) 확보")
        st.markdown("- **시청각 지원:** 주요 안내문에 큰 글씨 및 픽토그램 적용, 필요시 수어 통역사 배치 공간 마련")
        st.markdown("- **안심 휴식 공간:** 조명과 소음이 차단된 '콰이어트 룸(Quiet Room)' 배치 (자폐 스펙트럼 등 감각에 예민한 참가자 배려)")
        st.markdown("- **접근성 화장실:** 성별에 구애받지 않고 휠체어 접근이 가능한 다목적 가족 화장실 설치")
        
        if extra_req:
            st.success(f"**반영된 추가 요구사항:** {extra_req}")

    with tab4:
        st.subheader("행사의 퀄리티를 높이는 추가 제안")
        st.markdown(f"**'{atmosphere}'** 분위기와 **'{event_type}'**의 특성을 살릴 수 있는 아이디어입니다.")
        st.markdown("- **스마트 사이니지:** 실시간으로 화장실 및 휴게실 혼잡도를 스크린에 띄워 관람객 분산 유도")
        st.markdown("- **친환경 요소:** 입장권 대신 모바일 QR 티켓 사용 및 다회용 컵 대여소 운영")
        st.markdown("- **네트워킹 존:** 스탠딩 테이블을 곳곳에 배치하여 자연스러운 대화 유도")
