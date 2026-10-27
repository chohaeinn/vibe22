import io
import json
import math
import random
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="INCLUSE | AI 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Theme / helpers
# -----------------------------
st.markdown("""
<style>
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px;}
    .hero {padding: 1.4rem 1.6rem; border-radius: 18px; color: white;
           background: linear-gradient(120deg, #102a43 0%, #176b87 55%, #38a3a5 100%);}
    .hero h1 {margin: 0; font-size: 2.0rem;}
    .hero p {margin: .5rem 0 0 0; opacity: .92;}
    .small-note {font-size: .83rem; color: #64748b;}
    .section-card {padding: 1rem 1.2rem; border: 1px solid #e2e8f0; border-radius: 14px;}
    div[data-testid="stMetric"] {background: #f8fafc; padding: .8rem; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

ZONE_TYPES = {
    "공연장": "stage",
    "체험부스": "booth",
    "푸드존": "food",
    "휴게공간": "rest",
    "화장실": "toilet",
    "안내센터": "info",
    "응급의료센터": "medical",
    "출입구": "gate",
}
COLORS = {
    "공연장": "#7c3aed",
    "체험부스": "#2563eb",
    "푸드존": "#f97316",
    "휴게공간": "#16a34a",
    "화장실": "#64748b",
    "안내센터": "#0891b2",
    "응급의료센터": "#dc2626",
    "출입구": "#111827",
}

def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)

def clamp(value, low=0, high=100):
    return max(low, min(high, float(value)))

def generate_layout(shape, width, height, booth_count, visitor_count, priorities, seed=42):
    """Rule-based prototype layout. Not a trained AI or validated crowd simulator."""
    seed_everything(seed)
    rows = []
    # Gate positions around perimeter
    gate_points = [(0.06, 0.50), (0.94, 0.50)]
    if shape == "원형":
        gate_points = [(0.5, 0.05), (0.95, 0.5), (0.5, 0.95), (0.05, 0.5)]
    elif shape == "돔형":
        gate_points = [(0.22, 0.10), (0.78, 0.10), (0.95, 0.55), (0.5, 0.92)]
    for i, (x, y) in enumerate(gate_points[:3]):
        rows.append({"구역": f"출입구 {i+1}", "시설 유형": "출입구", "x": x, "y": y,
                     "너비(m)": 5, "높이(m)": 4, "예상 이용량": int(visitor_count / max(1, len(gate_points))),
                     "혼잡도(예측)": 22 + i * 4, "접근성": 95, "설계 근거": "출입 분산을 위해 외곽에 배치"})
    # Core facilities
    core = [
        ("공연장", 0.50, 0.27, 22, 13, "관람객 집중 구역을 중앙부에 두고 주변 통로를 확보"),
        ("응급의료센터", 0.10, 0.78, 8, 6, "외곽 진입로와 가까운 위치에 배치해 접근 시간을 줄임"),
        ("안내센터", 0.87, 0.20, 6, 5, "입장 직후 쉽게 찾을 수 있도록 입구 인근에 배치"),
        ("휴게공간", 0.80, 0.78, 10, 7, "혼잡 구역에서 떨어진 곳에 휴식 공간 확보"),
        ("화장실", 0.12, 0.25, 7, 5, "행사장 가장자리에서 접근할 수 있도록 배치"),
        ("푸드존", 0.72, 0.48, 12, 8, "대기열이 주요 이동 통로를 막지 않도록 외곽 쪽에 배치"),
    ]
    for name, x, y, w, h, reason in core:
        rows.append({"구역": name, "시설 유형": name, "x": x, "y": y,
                     "너비(m)": w, "높이(m)": h,
                     "예상 이용량": int(visitor_count * (0.35 if name == "공연장" else 0.12 if name == "푸드존" else 0.04)),
                     "혼잡도(예측)": int(np.random.uniform(25, 55)), "접근성": int(np.random.uniform(76, 98)),
                     "설계 근거": reason})
    # Booths distributed in bands, avoid center stage and paths
    candidate_positions = []
    for y in [0.16, 0.40, 0.60, 0.86]:
        for x in np.linspace(0.22, 0.78, max(2, booth_count // 4 + 2)):
            if not (0.39 < x < 0.61 and 0.19 < y < 0.38):
                candidate_positions.append((float(x), float(y)))
    random.shuffle(candidate_positions)
    for i in range(booth_count):
        x, y = candidate_positions[i % len(candidate_positions)]
        w, h = 5, 4
        rows.append({"구역": f"체험부스 {i+1}", "시설 유형": "체험부스", "x": x, "y": y,
                     "너비(m)": w, "높이(m)": h,
                     "예상 이용량": int(visitor_count * 0.025),
                     "혼잡도(예측)": int(np.random.uniform(20, 65)), "접근성": int(np.random.uniform(70, 98)),
                     "설계 근거": "부스 사이 보행 통로와 주요 시설 접근성을 고려해 분산 배치"})
    return pd.DataFrame(rows)

def score_layout(layout, budget, visitors, purpose, duration, accessibility_priority):
    if layout.empty:
        return {}
    congestion = float(layout["혼잡도(예측)"].mean())
    accessibility = float(layout["접근성"].mean())
    # Transparent heuristic scores; not measured/validated outputs.
    safety = clamp(100 - congestion * 0.72 + (8 if purpose == "안전 중심" else 0))
    crowd = clamp(100 - congestion)
    access = clamp(accessibility + (8 if accessibility_priority else 0))
    operations = clamp(84 - max(0, visitors / 500 - 4) * 2 + (5 if purpose == "운영 효율 중심" else 0))
    estimated_cost = 280 + len(layout) * 34 + visitors * 0.012
    budget_eff = clamp(100 - max(0, estimated_cost - budget) / max(1, budget) * 100)
    participation = clamp(78 + (6 if purpose == "참여 중심" else 0) - congestion * 0.12)
    weights = {
        "안전 중심": [0.30, 0.20, 0.20, 0.15, 0.05, 0.10],
        "참여 중심": [0.18, 0.15, 0.18, 0.15, 0.24, 0.10],
        "운영 효율 중심": [0.22, 0.22, 0.12, 0.26, 0.08, 0.10],
        "예산 중심": [0.18, 0.18, 0.12, 0.15, 0.10, 0.27],
    }.get(purpose, [0.22, 0.20, 0.16, 0.20, 0.12, 0.10])
    values = [safety, crowd, access, operations, participation, budget_eff]
    total = sum(w * v for w, v in zip(weights, values))
    return {
        "안전성": round(safety, 1), "혼잡도 관리": round(crowd, 1),
        "접근성": round(access, 1), "운영 효율성": round(operations, 1),
        "참여성": round(participation, 1), "예산 효율성": round(budget_eff, 1),
        "종합 점수": round(total, 1), "예상 비용(만원)": round(estimated_cost, 1),
        "평균 혼잡도": round(congestion, 1),
    }

def layout_chart(layout, shape, width, height, heat=False):
    fig = go.Figure()
    if heat:
        # A simple illustrative heat grid, not a live crowd simulation.
        xs = np.linspace(0, 1, 24)
        ys = np.linspace(0, 1, 18)
        z = np.zeros((len(ys), len(xs)))
        for _, row in layout.iterrows():
            xx, yy = row["x"], row["y"]
            amp = max(0.2, row["혼잡도(예측)"] / 100)
            z += amp * np.exp(-(((np.array(ys)[:, None] - yy) ** 2) / 0.012 +
                                ((np.array(xs)[None, :] - xx) ** 2) / 0.018))
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=z, colorscale="YlOrRd", opacity=0.75,
                                 colorbar=dict(title="상대 혼잡도")))
    for typ in layout["시설 유형"].unique():
        sub = layout[layout["시설 유형"] == typ]
        fig.add_trace(go.Scatter(
            x=sub["x"], y=sub["y"], mode="markers+text",
            text=sub["구역"], textposition="top center",
            name=typ, marker=dict(size=[max(10, min(35, float(a)*1.4)) for a in sub["너비(m)"]],
                                  color=COLORS.get(typ, "#2563eb"),
                                  line=dict(width=1, color="white")),
            customdata=sub[["너비(m)", "높이(m)", "혼잡도(예측)", "접근성"]].to_numpy(),
            hovertemplate="<b>%{text}</b><br>x=%{x:.2f}, y=%{y:.2f}<br>너비=%{customdata[0]}m<br>높이=%{customdata[1]}m<br>혼잡도=%{customdata[2]}<br>접근성=%{customdata[3]}<extra></extra>",
        ))
    fig.update_layout(
        height=570, margin=dict(l=10, r=10, t=25, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(range=[0, 1], title="행사장 가로 방향(상대 좌표)", showgrid=True, zeroline=False),
        yaxis=dict(range=[0, 1], title="행사장 세로 방향(상대 좌표)", scaleanchor="x", scaleratio=1, showgrid=True, zeroline=False),
    )
    if shape == "원형":
        fig.add_shape(type="circle", x0=0.02, y0=0.02, x1=0.98, y1=0.98, line=dict(color="#64748b", width=3))
    elif shape == "돔형":
        fig.add_shape(type="path", path="M 0.05,0.25 Q 0.5,1.1 0.95,0.25 L 0.95,0.95 L 0.05,0.95 Z",
                      line=dict(color="#64748b", width=3))
    else:
        fig.add_shape(type="rect", x0=0.02, y0=0.02, x1=0.98, y1=0.98, line=dict(color="#64748b", width=3))
    return fig

def make_pdf_bytes(report):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except Exception:
        return None
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = [Paragraph("INCLUSE | AI 기반 행사 설계 분석 리포트", styles["Title"]), Spacer(1, 12)]
    story.append(Paragraph("본 문서는 입력값과 규칙 기반 프로토타입 계산을 정리한 참고용 결과입니다. 실제 안전 인증이나 전문 군중 시뮬레이션을 대체하지 않습니다.", styles["BodyText"]))
    story.append(Spacer(1, 12))
    data = [["항목", "내용"]] + [[str(k), str(v)] for k, v in report.items()]
    table = Table(data, colWidths=[140, 340])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#123047")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.4, colors.lightgrey),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("PADDING", (0,0), (-1,-1), 7),
    ]))
    story.append(table)
    doc.build(story)
    return buffer.getvalue()

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
  <h1>🎪 INCLUSE | 생성형 AI 기반 행사 자동 설계 플랫폼</h1>
  <p>안전성 · 접근성 · 혼잡도 · 운영 효율 · 예산을 함께 고려하는 행사 설계 대시보드</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📝 행사 설계 조건")
    event_name = st.text_input("행사명", "INCLUSE 학교 축제")
    location = st.text_input("행사 장소", "건양고등학교 운동장")
    event_type = st.selectbox("행사 유형", ["학교 축제", "지역 축제", "박람회", "공연·페스티벌", "체육대회", "플리마켓", "기타"])
    purpose = st.selectbox("최적화 목표", ["안전 중심", "참여 중심", "운영 효율 중심", "예산 중심"])
    shape = st.selectbox("행사장 형태", ["정사각형", "직사각형", "원형", "돔형"])
    width = st.slider("행사장 가로 길이(m)", 30, 300, 100, 5)
    height = st.slider("행사장 세로 길이(m)", 30, 300, 80, 5)
    visitors = st.number_input("예상 방문객 수(명)", min_value=50, max_value=200000, value=1500, step=50)
    budget = st.number_input("예산(만원)", min_value=50, max_value=1000000, value=3000, step=100)
    duration = st.slider("행사 진행 시간(시간)", 1, 24, 6)
    booth_count = st.slider("체험부스 개수", 1, 40, 12)
    booth_width = st.slider("부스 너비(m)", 2, 15, 5)
    booth_height = st.slider("부스 높이/깊이(m)", 2, 15, 4)
    accessibility_priority = st.checkbox("접근성 우선 고려", value=True)
    user_groups = st.multiselect("주요 이용자 특성", ["어린이", "노인", "휠체어 이용자", "유모차 이용 가족", "외국인"], default=["어린이", "휠체어 이용자", "유모차 이용 가족"])
    st.caption("※ 현재 버전은 외부 AI 모델 연결 전의 실행 가능한 규칙 기반 프로토타입입니다.")
    generate = st.button("✨ 행사 설계안 생성 / 재계산", type="primary", use_container_width=True)

if "layout" not in st.session_state:
    st.session_state.layout = None
    st.session_state.scores = None
    st.session_state.before_scores = None
    st.session_state.incidents = []
    st.session_state.generation = 0

if generate or st.session_state.layout is None:
    st.session_state.generation += 1
    layout = generate_layout(shape, width, height, booth_count, visitors, purpose, seed=42 + st.session_state.generation)
    layout["너비(m)"] = layout["너비(m)"].where(layout["시설 유형"] != "체험부스", booth_width)
    layout["높이(m)"] = layout["높이(m)"].where(layout["시설 유형"] != "체험부스", booth_height)
    st.session_state.layout = layout
    st.session_state.scores = score_layout(layout, budget, visitors, purpose, duration, accessibility_priority)
    # Approximate "before" scores for illustrative comparison only
    before = dict(st.session_state.scores)
    before["안전성"] = round(max(0, before["안전성"] - 12), 1)
    before["혼잡도 관리"] = round(max(0, before["혼잡도 관리"] - 15), 1)
    before["접근성"] = round(max(0, before["접근성"] - 10), 1)
    before["운영 효율성"] = round(max(0, before["운영 효율성"] - 8), 1)
    before["참여성"] = round(max(0, before["참여성"] - 5), 1)
    before["종합 점수"] = round(max(0, before["종합 점수"] - 10), 1)
    st.session_state.before_scores = before

layout = st.session_state.layout
scores = st.session_state.scores
if layout is None:
    st.info("왼쪽에서 행사 조건을 입력하고 설계안을 생성하세요.")
    st.stop()

# Top metrics
st.subheader("📊 행사 설계 요약")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("행사", event_name)
c2.metric("방문객", f"{int(visitors):,}명")
c3.metric("행사장 면적", f"{width*height:,}㎡")
c4.metric("종합 점수", f"{scores['종합 점수']:.1f}점", f"{scores['종합 점수'] - st.session_state.before_scores['종합 점수']:+.1f}점 vs 설계 전")
c5.metric("예상 비용", f"{scores['예상 비용(만원)']:,.0f}만원", f"예산 {budget:,.0f}만원", delta_color="off")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ 디지털 트윈 배치도", "📈 점수·근거 분석", "🚨 돌발상황 대응", "🧭 이용자 접근성", "📄 결과 리포트"])

with tab1:
    left, right = st.columns([1.7, 1])
    with left:
        view = st.radio("시각화", ["시설 배치도", "혼잡도 Heatmap"], horizontal=True)
        st.plotly_chart(layout_chart(layout, shape, width, height, heat=(view == "혼잡도 Heatmap")), use_container_width=True)
        st.caption("배치도는 상대 좌표 기반의 시각화이며, 실제 측량 도면 또는 실시간 군중 시뮬레이션이 아닙니다.")
    with right:
        st.markdown("#### 배치 구성")
        summary = layout.groupby("시설 유형").size().reset_index(name="개수")
        st.dataframe(summary, hide_index=True, use_container_width=True)
        st.markdown("#### 설계 근거")
        for _, row in layout.head(8).iterrows():
            st.write(f"**{row['구역']}** — {row['설계 근거']}")
    st.markdown("#### 부스 배치 조정")
    booth_rows = layout[layout["시설 유형"] == "체험부스"].copy()
    if not booth_rows.empty:
        edited = st.data_editor(
            booth_rows[["구역", "x", "y", "너비(m)", "높이(m)"]],
            use_container_width=True, hide_index=True,
            column_config={
                "x": st.column_config.NumberColumn("x 좌표", min_value=0.0, max_value=1.0, step=0.01),
                "y": st.column_config.NumberColumn("y 좌표", min_value=0.0, max_value=1.0, step=0.01),
                "너비(m)": st.column_config.NumberColumn("너비(m)", min_value=1, max_value=30, step=1),
                "높이(m)": st.column_config.NumberColumn("높이(m)", min_value=1, max_value=30, step=1),
            }, key="booth_editor"
        )
        if st.button("부스 수정 내용 적용"):
            for _, edited_row in edited.iterrows():
                idx = st.session_state.layout.index[st.session_state.layout["구역"] == edited_row["구역"]][0]
                for col in ["x", "y", "너비(m)", "높이(m)"]:
                    st.session_state.layout.loc[idx, col] = edited_row[col]
            st.session_state.scores = score_layout(st.session_state.layout, budget, visitors, purpose, duration, accessibility_priority)
            st.success("수정한 부스 위치와 크기를 적용했습니다.")
            st.rerun()

with tab2:
    st.markdown("#### 설계 평가 지표")
    score_names = ["안전성", "혼잡도 관리", "접근성", "운영 효율성", "참여성", "예산 효율성"]
    score_df = pd.DataFrame({
        "평가 지표": score_names,
        "설계 전(예시)": [st.session_state.before_scores[k] for k in score_names],
        "AI 설계 후(규칙 기반 추정)": [scores[k] for k in score_names],
    })
    fig = go.Figure()
    fig.add_trace(go.Bar(name="설계 전(예시)", x=score_df["평가 지표"], y=score_df["설계 전(예시)"]))
    fig.add_trace(go.Bar(name="설계 후(추정)", x=score_df["평가 지표"], y=score_df["AI 설계 후(규칙 기반 추정)"]))
    fig.update_layout(barmode="group", yaxis=dict(range=[0, 100], title="점수(0~100)"), height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(score_df, hide_index=True, use_container_width=True)
    st.markdown("#### 점수 산정 근거")
    st.write("- **안전성:** 평균 예측 혼잡도가 낮을수록 높게 계산합니다. 안전 중심 목표를 선택하면 가중 보정합니다.")
    st.write("- **혼잡도 관리:** 시설별 추정 혼잡도 평균을 100점에서 차감한 규칙 기반 지표입니다.")
    st.write("- **접근성:** 시설별 접근성 추정치 평균에 접근성 우선 옵션을 반영합니다.")
    st.write("- **운영 효율성·참여성:** 방문객 규모와 선택한 행사 목표를 반영한 시제품용 휴리스틱입니다.")
    st.write("- **예산 효율성:** 추정 비용이 입력 예산을 초과하는 정도에 따라 계산합니다.")
    st.warning("점수는 시제품에서 설명을 위해 정의한 휴리스틱이며, 실제 측정 데이터나 검증된 안전 지표가 아닙니다.")

with tab3:
    st.markdown("#### 돌발상황 시나리오 테스트")
    scenario = st.selectbox("가정할 상황", ["방문객 급증", "우천 발생", "공연 지연", "출입구 혼잡", "응급환자 발생"])
    severity = st.slider("상황 강도", 1, 5, 3)
    incident_zone = st.selectbox("발생 구역", layout["구역"].tolist())
    incident_note = st.text_area("상황 메모", placeholder="예: 체험부스 3번 앞에서 어지럼증 호소자 발생")
    if st.button("시나리오 분석"):
        st.session_state.incidents.append({
            "시각": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "상황": scenario, "강도": severity, "발생 구역": incident_zone,
            "메모": incident_note or "(메모 없음)",
        })
        st.success("시나리오를 기록했습니다. 아래 대응 권고는 참고용이며 실제 현장 지휘·응급 대응을 대체하지 않습니다.")
    if scenario == "방문객 급증":
        recommendations = ["입장 대기열을 외곽에 분산하고 출입구별 유입량을 확인합니다.", "공연장·푸드존 주변 통로를 비우고 병목 지점을 현장 요원이 확인합니다.", "혼잡이 지속되면 입장 속도 조절 및 안내 방송을 검토합니다."]
    elif scenario == "우천 발생":
        recommendations = ["미끄럼 위험 구역을 확인하고 전선·전기 설비 주변 접근을 통제합니다.", "실내 대피 공간의 수용 가능 인원과 이동 경로를 확인합니다.", "기상 상황과 시설 안전성을 확인한 뒤 운영 지속 여부를 책임자가 결정합니다."]
    elif scenario == "공연 지연":
        recommendations = ["대기 인파가 한 곳에 집중되지 않도록 안내 정보를 반복 제공합니다.", "푸드존·출입구로 이어지는 주 통로를 확보합니다.", "공연 시작 시간 변경을 여러 안내 채널에 동일하게 공지합니다."]
    elif scenario == "출입구 혼잡":
        recommendations = ["출입구별 인파와 이동 방향을 현장에서 확인합니다.", "안전요원이 통로를 확보하고 역방향 흐름을 줄이도록 안내합니다.", "필요하면 대체 출입구를 개방하되 현장 책임자의 승인과 안내를 거칩니다."]
    else:
        recommendations = ["현장 응급 담당자와 119에 즉시 연락하고, 환자의 상태와 정확한 위치를 전달합니다.", "주변 인파를 안전하게 분산하고 구급대 접근 통로를 확보합니다.", "훈련된 담당자가 아닌 경우 환자를 불필요하게 이동시키지 말고 지시에 따릅니다."]
    st.markdown("#### 권고 체크리스트")
    for rec in recommendations:
        st.checkbox(rec, key="rec_" + str(abs(hash(rec))) + "_" + scenario)
    if st.session_state.incidents:
        st.markdown("#### 기록된 상황")
        st.dataframe(pd.DataFrame(st.session_state.incidents), hide_index=True, use_container_width=True)
        st.download_button("상황 기록 CSV 다운로드", pd.DataFrame(st.session_state.incidents).to_csv(index=False).encode("utf-8-sig"),
                           file_name="incident_log.csv", mime="text/csv")

with tab4:
    st.markdown("#### 이용자 유형별 접근성 점검")
    access_data = []
    groups = user_groups or ["일반 방문객"]
    for group in groups:
        if group == "휠체어 이용자":
            note, value = "주 통로 폭, 단차 없는 경로, 응급시설 접근을 현장 확인", 78
        elif group == "유모차 이용 가족":
            note, value = "좁은 부스 사이 통로와 대기열 우회 경로 확인", 82
        elif group == "어린이":
            note, value = "보호자 대기 공간, 위험 시설 접근 제한, 안내 표지 확인", 80
        elif group == "노인":
            note, value = "휴게 의자, 그늘, 화장실 접근 거리 확인", 84
        else:
            note, value = "그림 중심 안내, 다국어 표지, 안내센터 위치 확인", 76
        access_data.append({"이용자 유형": group, "접근성 참고 점수": value, "점검 항목": note})
    access_df = pd.DataFrame(access_data)
    st.dataframe(access_df, hide_index=True, use_container_width=True)
    st.info("접근성 점수는 체크 항목을 설명하기 위한 예시 값입니다. 실제 시설 규격·법령 준수 여부는 현장 측정과 전문가 검토가 필요합니다.")
    st.markdown("#### 권장 공통 점검")
    for item in ["주요 통로와 비상 대피로에 시설물이 놓이지 않았는가?", "휠체어·유모차가 이동할 수 있는 연속 경로가 있는가?",
                 "안내 표지와 응급의료센터 위치가 쉽게 식별되는가?", "휴게공간·화장실까지 이동 거리가 과도하지 않은가?",
                 "비상 상황에서 구급대가 진입할 수 있는가?"]:
        st.checkbox(item, key="access_" + str(abs(hash(item))))

with tab5:
    st.markdown("#### 최종 설계 리포트")
    report = {
        "행사명": event_name,
        "행사 유형": event_type,
        "장소": location,
        "행사장 형태": shape,
        "행사장 크기": f"{width}m × {height}m ({width*height:,}㎡)",
        "예상 방문객": f"{int(visitors):,}명",
        "예산": f"{budget:,.0f}만원",
        "행사 시간": f"{duration}시간",
        "부스 수": f"{booth_count}개",
        "최적화 목표": purpose,
        **{k: v for k, v in scores.items()},
        "이용자 특성": ", ".join(user_groups) if user_groups else "일반 방문객",
        "생성 시각": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    st.json(report, expanded=True)
    csv_data = layout.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 배치 데이터 CSV 다운로드", csv_data, file_name="event_layout.csv", mime="text/csv")
    st.download_button("📥 분석 리포트 JSON 다운로드", json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"),
                       file_name="event_report.json", mime="application/json")
    pdf_bytes = make_pdf_bytes(report)
    if pdf_bytes:
        st.download_button("📄 PDF 리포트 다운로드", pdf_bytes, file_name="event_design_report.pdf", mime="application/pdf")
    else:
        st.caption("PDF 생성 라이브러리가 없으면 requirements.txt를 설치한 뒤 다시 실행하세요.")

st.divider()
st.caption("INCLUSE 프로토타입 · 본 앱의 배치·혼잡도·점수는 규칙 기반 예시 추정입니다. 실제 행사 운영 전에는 현장 도면, 수용 인원, 법령·소방 기준, 접근성 규격 및 안전 전문가 검토가 반드시 필요합니다.")
