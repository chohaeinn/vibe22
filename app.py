import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - AI 행사장 설계 및 동선 최적화",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_AI_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI - AI 행사장 설계 시스템</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR",Roboto,sans-serif;
  color:#1e293b;
  background:#f8fafc;
  overflow-x:hidden;
}
button,input,select,textarea{font:inherit;}
button{cursor:pointer;}

/* Layout Setup */
.app-container{
  display:flex;
  min-height:100vh;
  background:#f8fafc;
}

/* Dark Sidebar (Matches Image) */
.sidebar{
  width:240px;
  background:#0f172a;
  color:#94a3b8;
  padding:20px 14px;
  display:flex;
  flex-direction:column;
  gap:20px;
  flex-shrink:0;
}
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  padding:0 8px;
  color:#fff;
}
.brand-icon{
  width:36px;
  height:36px;
  background:linear-gradient(135deg,#3b82f6,#2563eb);
  border-radius:10px;
  display:grid;
  place-items:center;
  font-size:20px;
  font-weight:900;
  box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.brand-title{font-size:18px;font-weight:800;letter-spacing:-0.5px;}
.brand-sub{font-size:10px;color:#64748b;margin-top:2px;}

.nav-group{display:flex;flex-direction:column;gap:4px;}
.nav-item{
  display:flex;
  align-items:center;
  gap:12px;
  padding:11px 14px;
  border-radius:10px;
  font-size:13.5px;
  font-weight:700;
  color:#94a3b8;
  cursor:pointer;
  transition:all 0.2s ease;
}
.nav-item:hover{background:rgba(255,255,255,0.06);color:#e2e8f0;}
.nav-item.active{
  background:#2563eb;
  color:#ffffff;
  box-shadow:0 4px 12px rgba(37,99,235,0.3);
}
.nav-icon{font-size:16px;width:20px;text-align:center;}

.side-banner{
  margin-top:auto;
  background:linear-gradient(135deg,rgba(30,58,138,0.5),rgba(30,41,59,0.8));
  border:1px solid rgba(59,130,246,0.3);
  padding:14px;
  border-radius:14px;
  color:#e2e8f0;
}
.side-banner h5{font-size:12px;font-weight:800;color:#60a5fa;margin-bottom:4px;}
.side-banner p{font-size:11px;color:#94a3b8;line-height:1.4;}

/* Main Content Area */
.main-content{
  flex:1;
  padding:20px 24px;
  display:flex;
  flex-direction:column;
  gap:16px;
  min-width:0;
  overflow-y:auto;
}

/* Top Navigation / Header */
.header-bar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  background:#ffffff;
  padding:14px 20px;
  border-radius:16px;
  border:1px solid #e2e8f0;
  box-shadow:0 2px 8px rgba(0,0,0,0.03);
}
.header-title h2{font-size:20px;font-weight:800;color:#0f172a;}
.header-title p{font-size:12px;color:#64748b;margin-top:2px;}
.user-profile{
  display:flex;
  align-items:center;
  gap:10px;
  font-size:12px;
  font-weight:700;
  color:#334155;
  background:#f1f5f9;
  padding:6px 12px;
  border-radius:20px;
}

/* Pages Control */
.page-view{display:none;}
.page-view.active{display:block;}

/* Home View Input Card */
.home-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:18px;
  padding:24px;
  box-shadow:0 4px 20px rgba(0,0,0,0.03);
}
.section-head{
  font-size:16px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:16px;
  display:flex;
  align-items:center;
  gap:8px;
}
.input-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:16px;
  margin-bottom:20px;
}
.form-group{
  display:flex;
  flex-direction:column;
  gap:6px;
}
.form-group label{
  font-size:12px;
  font-weight:800;
  color:#475569;
}
.form-group input, .form-group select, .form-group textarea{
  padding:10px 12px;
  border:1px solid #cbd5e1;
  border-radius:10px;
  background:#f8fafc;
  color:#0f172a;
  font-weight:600;
  font-size:13px;
  outline:none;
  transition:border-color 0.2s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus{
  border-color:#2563eb;
  background:#fff;
}

/* Event Basic Info Bar (Matches Top Section in Reference Image) */
.event-info-bar{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:12px;
  box-shadow:0 2px 10px rgba(0,0,0,0.02);
}
.info-items-group{
  display:flex;
  align-items:center;
  gap:18px;
  flex-wrap:wrap;
}
.info-item-box{
  display:flex;
  align-items:center;
  gap:8px;
  font-size:12px;
}
.info-item-icon{
  width:32px;
  height:32px;
  border-radius:8px;
  background:#eff6ff;
  color:#2563eb;
  display:grid;
  place-items:center;
  font-size:14px;
}
.info-item-text label{display:block;font-size:10px;color:#64748b;font-weight:700;}
.info-item-text span{font-weight:800;color:#0f172a;font-size:13px;}

.btn-ai-generate{
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  color:#ffffff;
  border:none;
  padding:12px 22px;
  border-radius:12px;
  font-weight:800;
  font-size:13px;
  box-shadow:0 4px 14px rgba(37,99,235,0.35);
  display:flex;
  align-items:center;
  gap:8px;
  transition:transform 0.15s;
}
.btn-ai-generate:hover{transform:translateY(-1px);}

/* Grid Panels (Reference Layout) */
.dashboard-grid-top{
  display:grid;
  grid-template-columns: 1.4fr 1fr 1.1fr;
  gap:16px;
}
.dashboard-grid-bottom{
  display:grid;
  grid-template-columns: 1fr 1.2fr 1fr;
  gap:16px;
}

.panel-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:16px;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
  display:flex;
  flex-direction:column;
}
.panel-title{
  font-size:14px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:12px;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.panel-title .sub-tag{
  font-size:10px;
  background:#f1f5f9;
  color:#64748b;
  padding:3px 8px;
  border-radius:12px;
}

/* Digital Twin Map Container */
.map-canvas-container{
  position:relative;
  width:100%;
  height:360px;
  background:#f1f5f9;
  border:1px solid #cbd5e1;
  border-radius:12px;
  overflow:hidden;
}
#venueCanvas,#heatmapCanvas,#peopleCanvas{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
}
#peopleCanvas{z-index:10;pointer-events:none;}
#heatmapCanvas{z-index:5;opacity:0.85;pointer-events:none;}
.map-zoom-controls{
  position:absolute;
  right:10px;
  top:10px;
  z-index:20;
  display:flex;
  flex-direction:column;
  gap:4px;
}
.zoom-btn{
  width:28px;
  height:28px;
  background:#ffffff;
  border:1px solid #cbd5e1;
  border-radius:6px;
  font-weight:800;
  color:#334155;
}

/* Booth Legend Overlay */
.booth-legend{
  position:absolute;
  left:10px;
  bottom:10px;
  z-index:20;
  background:rgba(255,255,255,0.92);
  padding:6px 10px;
  border-radius:8px;
  font-size:10px;
  border:1px solid #e2e8f0;
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:4px 8px;
}
.legend-dot{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:4px;}

/* AI Scores Table */
.score-table{width:100%;border-collapse:collapse;font-size:12px;margin-top:4px;}
.score-table th,.score-table td{padding:8px;text-align:left;border-bottom:1px solid #f1f5f9;}
.score-badge{
  display:inline-block;
  padding:3px 8px;
  border-radius:10px;
  font-weight:800;
  font-size:10px;
}
.badge-excellent{background:#dcfce7;color:#15803d;}
.badge-good{background:#e0f2fe;color:#0369a1;}

/* Before / After Comparison */
.compare-box{
  display:grid;
  grid-template-columns:1fr 30px 1fr;
  align-items:center;
  gap:8px;
  background:#f8fafc;
  border-radius:12px;
  padding:12px;
  border:1px solid #e2e8f0;
}
.compare-col h5{font-size:11px;color:#64748b;margin-bottom:6px;}
.compare-metric{display:flex;justify-content:space-between;font-size:11px;margin-bottom:4px;font-weight:700;}
.text-danger{color:#ef4444;}
.text-success{color:#10b981;}

/* Workflow Steps */
.workflow-steps{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:4px;
  margin-top:10px;
}
.wf-step{
  flex:1;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 4px;
  border-radius:8px;
  text-align:center;
  font-size:10px;
}
.wf-step.active{background:#eff6ff;border-color:#3b82f6;color:#1d4ed8;font-weight:800;}
.wf-arrow{color:#94a3b8;font-size:10px;}

/* AI Assistant & Chat Box */
.ai-assistant-container{
  display:flex;
  flex-direction:column;
  height:100%;
}
.chat-messages{
  flex:1;
  min-height:110px;
  max-height:140px;
  overflow-y:auto;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  border-radius:10px;
  padding:10px;
  font-size:11px;
  display:flex;
  flex-direction:column;
  gap:8px;
  margin-bottom:10px;
}
.chat-msg{
  padding:7px 10px;
  border-radius:8px;
  max-width:90%;
  line-height:1.4;
}
.chat-msg.ai{background:#e0f2fe;color:#0369a1;align-self:flex-start;}
.chat-msg.user{background:#2563eb;color:#ffffff;align-self:flex-end;}

.chat-input-row{
  display:flex;
  gap:6px;
}
.chat-input-row input{
  flex:1;
  padding:8px 10px;
  border:1px solid #cbd5e1;
  border-radius:8px;
  font-size:11px;
}
.chat-input-row button{
  background:#2563eb;
  color:#fff;
  border:none;
  padding:0 12px;
  border-radius:8px;
  font-size:11px;
  font-weight:800;
}

/* Quick Prompt Suggestions */
.quick-prompts{
  display:flex;
  gap:4px;
  flex-wrap:wrap;
  margin-top:6px;
}
.quick-btn{
  background:#f1f5f9;
  border:1px solid #cbd5e1;
  padding:4px 8px;
  border-radius:6px;
  font-size:10px;
  color:#334155;
}
.quick-btn:hover{background:#e2e8f0;}

/* Simulation Controller Bar */
.sim-controls-bar{
  display:flex;
  align-items:center;
  gap:10px;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 12px;
  border-radius:10px;
  margin-top:10px;
}
.sim-btn{
  padding:6px 14px;
  border-radius:8px;
  border:none;
  font-weight:800;
  font-size:11px;
}
.sim-btn-primary{background:#2563eb;color:#ffffff;}
.sim-btn-secondary{background:#e2e8f0;color:#334155;}

/* Modal for AI Report */
.modal-overlay{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,0.6);
  z-index:999;
  display:none;
  place-items:center;
}
.modal-overlay.active{display:grid;}
.modal-card{
  background:#ffffff;
  width:min(90%,650px);
  border-radius:20px;
  padding:24px;
  box-shadow:0 20px 40px rgba(0,0,0,0.2);
}

</style>
</head>
<body>

<div class="app-container">

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon">✦</div>
      <div>
        <div class="brand-title">Event AI</div>
        <div class="brand-sub">AI 기반 행사 설계 및 동선 분석</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item active" onclick="switchPage('home', this)">
        <span class="nav-icon">🏠</span> 홈 (설계 입력)
      </div>
      <div class="nav-item" onclick="switchPage('design', this)">
        <span class="nav-icon">🏢</span> 행사 설계
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span class="nav-icon">⚙️</span> 설계 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span class="nav-icon">📊</span> AI 보고서 보기
      </div>
      <div class="nav-item" onclick="switchPage('assistantPage', this)">
        <span class="nav-icon">🤖</span> AI 어시스턴트
      </div>
    </nav>

    <div class="side-banner">
      <h5>AI 실시간 지원</h5>
      <p>행사장 규모와 인원을 입력하면 최적의 부스 배치 및 동선을 실시간 자동 제안합니다.</p>
    </div>
  </aside>

  <!-- MAIN CONTENT AREA -->
  <main class="main-content">

    <!-- Top Header Bar -->
    <header class="header-bar">
      <div class="header-title">
        <h2 id="pageTitleText">행사 설계 입력</h2>
        <p id="pageSubText">행사 정보를 입력하시면 AI가 최적의 행사장을 설계해드립니다.</p>
      </div>
      <div class="user-profile">
        <span>👤 추천님 (관리자)</span>
      </div>
    </header>

    <!-- PAGE 1: HOME INPUT FORM -->
    <section id="pageHome" class="page-view active">
      <div class="home-card">
        <div class="section-head">📝 행사 기본 정보 및 요구사항 입력</div>
        <div class="input-grid">
          <div class="form-group">
            <label>행사명</label>
            <input type="text" id="inputEventName" value="2026 청소년 미래 과학 박람회">
          </div>
          <div class="form-group">
            <label>행사장 크기</label>
            <select id="inputVenueSize">
              <option value="20x15">20m × 15m (소형)</option>
              <option value="30x20">30m × 20m (중형)</option>
              <option value="40x25" selected>40m × 25m (대형)</option>
              <option value="60x40">60m × 40m (초대형)</option>
            </select>
          </div>
          <div class="form-group">
            <label>행사장 모양</label>
            <select id="inputVenueShape">
              <option value="rect" selected>직사각형</option>
              <option value="square">정사각형</option>
              <option value="lshape">L자형</option>
              <option value="wide">가로 파노라마형</option>
            </select>
          </div>
          <div class="form-group">
            <label>예상 관람객 수</label>
            <select id="inputVisitorCount">
              <option value="300">300명</option>
              <option value="500">500명</option>
              <option value="1000" selected>1,000명</option>
              <option value="3000">3,000명</option>
              <option value="5000">5,000명</option>
            </select>
          </div>
          <div class="form-group">
            <label>운영 시간 및 대대</label>
            <input type="text" id="inputEventTime" value="10:00 - 18:00 (8시간)">
          </div>
          <div class="form-group">
            <label>입장료 / 티켓 가격</label>
            <input type="text" id="inputTicketFee" value="무료 (사전예약)">
          </div>
          <div class="form-group">
            <label>예산 및 예상 매출</label>
            <input type="text" id="inputBudget" value="5,000만원">
          </div>
          <div class="form-group" style="grid-column:1 / -1;">
            <label>추가 요구사항 (AI 설계 반영)</label>
            <textarea id="inputRequirements" rows="3" placeholder="예: 메인 무대는 중앙에 배치하고, 푸드존과 휴식 구역은 출구 부근으로 분산시켜 병목현상을 방지해줘.">메인 무대 시야 확보, 인기 체험부스 병목 방지, 의료 안전존 입구 배치, 푸드존 휴식구역 이격 배치</textarea>
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn-ai-generate" onclick="runAIGenerate()">
            ✦ AI 최적 행사 설계하기
          </button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: EVENT DESIGN DASHBOARD (Matches Image Visuals) -->
    <section id="pageDesign" class="page-view">

      <!-- Event Basic Info Header Bar -->
      <div class="event-info-bar">
        <div class="info-items-group">
          <div class="info-item-box">
            <div class="info-item-icon">📋</div>
            <div class="info-item-text">
              <label>행사명</label>
              <span id="displayEventName">2026 청소년 미래 과학 박람회</span>
            </div>
          </div>
          <div class="info-item-box">
            <div class="info-item-icon">📐</div>
            <div class="info-item-text">
              <label>규모 및 모양</label>
              <span id="displayVenueDim">40m x 25m (직사각형)</span>
            </div>
          </div>
          <div class="info-item-box">
            <div class="info-item-icon">👥</div>
            <div class="info-item-text">
              <label>예상 관람객</label>
              <span id="displayVisitors">1,000명</span>
            </div>
          </div>
          <div class="info-item-box">
            <div class="info-item-icon">⏰</div>
            <div class="info-item-text">
              <label>운영 시간</label>
              <span id="displayTime">10:00 - 18:00</span>
            </div>
          </div>
          <div class="info-item-box">
            <div class="info-item-icon">🎫</div>
            <div class="info-item-text">
              <label>입장료</label>
              <span id="displayFee">무료</span>
            </div>
          </div>
        </div>
        <button class="btn-ai-generate" onclick="runAIGenerate()">
          ✦ AI 재설계 실행
        </button>
      </div>

      <!-- Top Dashboard Grid -->
      <div class="dashboard-grid-top" style="margin-top:14px;">

        <!-- 1. Digital Twin Layout Map -->
        <div class="panel-card">
          <div class="panel-title">
            <span>🗺️ 행사장 배치도 (디지털 트윈)</span>
            <span class="sub-tag">AI 최적화 완료</span>
          </div>
          <div class="map-canvas-container" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>
            <div class="map-zoom-controls">
              <button class="zoom-btn" onclick="zoomMap(0.1)">+</button>
              <button class="zoom-btn" onclick="zoomMap(-0.1)">-</button>
            </div>
            <div class="booth-legend">
              <div><span class="legend-dot" style="background:#2563eb;"></span> 메인 무대</div>
              <div><span class="legend-dot" style="background:#f43f5e;"></span> 체험 부스</div>
              <div><span class="legend-dot" style="background:#eab308;"></span> 푸드 존</div>
              <div><span class="legend-dot" style="background:#10b981;"></span> 의료/안전</div>
              <div><span class="legend-dot" style="background:#06b6d4;"></span> 휴식 구역</div>
              <div><span class="legend-dot" style="background:#64748b;"></span> 일반 전시</div>
            </div>
          </div>

          <!-- Controls under Map -->
          <div class="sim-controls-bar">
            <button class="sim-btn sim-btn-primary" id="btnPlaySim" onclick="toggleSim()">▶ 다방향 동선 시뮬레이션</button>
            <button class="sim-btn sim-btn-secondary" onclick="resetSim()">🔄 초기화</button>
            <span style="font-size:11px;color:#64748b;margin-left:auto;" id="simTimeText">경과 시간: 00:00</span>
          </div>
        </div>

        <!-- 2. Live Heatmap Panel -->
        <div class="panel-card">
          <div class="panel-title">
            <span>🔥 혼잡도 Heatmap</span>
            <span class="sub-tag">실시간 감지</span>
          </div>
          <div class="map-canvas-container">
            <canvas id="heatmapCanvas"></canvas>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:10px;color:#64748b;margin-top:8px;">
            <span>🟢 원활</span>
            <span>🟡 보통</span>
            <span>🟠 혼잡</span>
            <span>🔴 매우 혼잡</span>
          </div>
        </div>

        <!-- 3. AI Evaluation Result -->
        <div class="panel-card">
          <div class="panel-title">
            <span>💡 AI 평가 결과</span>
            <span class="sub-tag">종합 점수 94점</span>
          </div>
          <table class="score-table">
            <thead>
              <tr><th>평가 항목</th><th>점수</th><th>등급</th></tr>
            </thead>
            <tbody>
              <tr><td>안전성</td><td>92점</td><td><span class="score-badge badge-excellent">매우 우수</span></td></tr>
              <tr><td>동선 효율성</td><td>87점</td><td><span class="score-badge badge-good">우수</span></td></tr>
              <tr><td>접근성</td><td>98점</td><td><span class="score-badge badge-excellent">매우 우수</span></td></tr>
              <tr><td>혼잡도 관리</td><td>84점</td><td><span class="score-badge badge-good">우수</span></td></tr>
              <tr><td>공간 활용도</td><td>88점</td><td><span class="score-badge badge-good">우수</span></td></tr>
            </tbody>
          </table>
          <div style="margin-top:12px;font-size:11px;color:#334155;background:#f8fafc;padding:10px;border-radius:8px;border:1px solid #e2e8f0;line-height:1.4;">
            <b>💡 AI 개선 제안:</b><br>
            • 안전을 위해 메인무대 앞 보행 통로 폭을 3.5m로 확보했습니다.<br>
            • 의료존을 입구 근처로 배치하여 긴급 상황 접근성을 최적화했습니다.
          </div>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-grid-bottom" style="margin-top:16px;">

        <!-- 1. Before vs After Comparison -->
        <div class="panel-card">
          <div class="panel-title">
            <span>⚖️ 설계 전 / 후 비교</span>
          </div>
          <div class="compare-box">
            <div class="compare-col">
              <h5>기존 설계안</h5>
              <div class="compare-metric"><span>혼잡도</span><span class="text-danger">72%</span></div>
              <div class="compare-metric"><span>동선점수</span><span>61점</span></div>
              <div class="compare-metric"><span>병목구역</span><span class="text-danger">4곳</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#94a3b8;">→</div>
            <div class="compare-col">
              <h5>AI 최적안</h5>
              <div class="compare-metric"><span>혼잡도</span><span class="text-success">28%</span></div>
              <div class="compare-metric"><span>동선점수</span><span class="text-success">92점</span></div>
              <div class="compare-metric"><span>병목구역</span><span class="text-success">0곳</span></div>
            </div>
          </div>
        </div>

        <!-- 2. AI Workflow Step Visualizer -->
        <div class="panel-card">
          <div class="panel-title">
            <span>⚙️ AI 행사 설계 프로세스</span>
          </div>
          <div class="workflow-steps">
            <div class="wf-step active">1. 정보 입력</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">2. 공간 분석</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">3. AI 자동 배치</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">4. 시뮬레이션</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">5. 최종 리포트</div>
          </div>
          <p style="font-size:11px;color:#64748b;margin-top:10px;text-align:center;">
            수천 가지 이동 시나리오 분석을 통해 최적의 부스 레이아웃을 산출했습니다.
          </p>
        </div>

        <!-- 3. AI Assistant Box -->
        <div class="panel-card">
          <div class="panel-title">
            <span>💬 AI 어시스턴트 (실시간 수정)</span>
          </div>
          <div class="ai-assistant-container">
            <div class="chat-messages" id="chatBox">
              <div class="chat-msg ai">
                안녕하세요! 행사장 레이아웃에 관해 추가 수정이나 요청사항이 있으시면 말씀해주세요.
              </div>
            </div>
            <div class="chat-input-row">
              <input type="text" id="chatInput" placeholder="예: 체험부스를 조금 더 띄워줘" onkeydown="if(event.key==='Enter') sendChat()">
              <button onclick="sendChat()">전송</button>
            </div>
            <div class="quick-prompts">
              <button class="quick-btn" onclick="applyQuickPrompt('의료부스 입구 배치')">의료부스 입구 배치</button>
              <button class="quick-btn" onclick="applyQuickPrompt('푸드존 출구 이동')">푸드존 출구 이동</button>
              <button class="quick-btn" onclick="applyQuickPrompt('동선 통로 확대')">동선 통로 확대</button>
            </div>
          </div>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS DETAIL VIEW -->
    <section id="pageProcess" class="page-view">
      <div class="home-card">
        <div class="section-head">🔄 AI 설계 프로세스 상세 설명</div>
        <div style="font-size:13px;line-height:1.6;color:#334155;display:flex;flex-direction:column;gap:12px;">
          <p><b>1단계: 조건 데이터 입력</b> - 사용자가 입력한 공간 크기, 예측 인원, 필수 부스 유형을 파악합니다.</p>
          <p><b>2단계: 공간 안전성 분석</b> - 비상구, 출입구 및 주요 이동 통로의 최소 너비를 계산합니다.</p>
          <p><b>3단계: AI 군중 다방향 동선 계산</b> - 에이전트 기반 모델을 통해 사람들이 특정 시간에 무대, 푸드존, 체험존으로 분산 이동하는 패턴을 시뮬레이션합니다.</p>
          <p><b>4단계: 최종 레이아웃 확정</b> - 병목현상을 최소화하는 알고리즘을 적용하여 디지털 트윈 평면도를 완성합니다.</p>
        </div>
      </div>
    </section>

    <!-- PAGE 5: AI ASSISTANT FULL VIEW -->
    <section id="pageAssistant" class="page-view">
      <div class="home-card">
        <div class="section-head">🤖 AI 전담 어시스턴트 대화창</div>
        <p style="font-size:12px;color:#64748b;margin-bottom:12px;">행사장 맞춤 요구사항을 입력하시면 즉시 배치를 재조정합니다.</p>
        <div id="fullChatBox" class="chat-messages" style="height:250px;max-height:none;margin-bottom:12px;">
          <div class="chat-msg ai">무엇을 도와드릴까요? 행사장의 안전성, 푸드존 위치, 동선 혼잡도 개선 요청을 처리해드립니다.</div>
        </div>
        <div class="chat-input-row">
          <input type="text" id="fullChatInput" placeholder="요청사항을 입력하세요..." onkeydown="if(event.key==='Enter') sendFullChat()">
          <button onclick="sendFullChat()">수정 요청하기</button>
        </div>
      </div>
    </section>

  </main>
</div>

<!-- AI REPORT MODAL -->
<div class="modal-overlay" id="reportModal">
  <div class="modal-card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
      <h3 style="font-size:18px;font-weight:800;color:#0f172a;">📊 AI 행사장 종합 분석 리포트</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:18px;font-weight:900;">✕</button>
    </div>
    <div style="font-size:13px;color:#334155;line-height:1.6;display:flex;flex-direction:column;gap:10px;">
      <p><b>• 종합 평가:</b> 본 설계안은 1,000명 이상의 관람객을 안전하게 수용할 수 있으며 동선 점수 92점을 달성했습니다.</p>
      <p><b>• 안전 및 이탈률:</b> 비상구 및 출입구 주변 혼잡도가 28% 감소하여 비상 상황 시 신속 탈출이 가능합니다.</p>
      <p><b>• 체류 시간 증대:</b> 체험존과 휴식 공간의 적절한 분산 배치로 평균 체류시간이 18% 상승할 것으로 예측됩니다.</p>
    </div>
    <div style="margin-top:20px;display:flex;justify-content:flex-end;gap:8px;">
      <button class="sim-btn sim-btn-secondary" onclick="closeReportModal()">닫기</button>
      <button class="sim-btn sim-btn-primary" onclick="alert('PDF 리포트가 다운로드 되었습니다.');closeReportModal();">PDF 다운로드</button>
    </div>
  </div>
</div>

<script>
/* ==============================================
   STATE MANAGEMENT & ROUTING
   ============================================== */
let venue = { width: 40, height: 25, shape: 'rect' };
let booths = [];
let people = [];
let simRunning = false;
let simTime = 0;
let mapScale = 1.0;

function switchPage(pageId, navEl){
  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  if(navEl) navEl.classList.add('active');

  const titleEl = document.getElementById('pageTitleText');
  const subEl = document.getElementById('pageSubText');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
    titleEl.textContent = '행사 설계 입력';
    subEl.textContent = '행사 정보를 입력하시면 AI가 최적의 행사장을 설계해드립니다.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    titleEl.textContent = '행사 설계 및 동선 분석';
    subEl.textContent = 'AI가 최적화한 디지털 트윈 공간 및 관람객 동선 시뮬레이션입니다.';
    setTimeout(initCanvases, 50);
  } else if(pageId === 'process'){
    document.getElementById('pageProcess').classList.add('active');
    titleEl.textContent = '설계 프로세스';
    subEl.textContent = 'AI 분석 및 자동 배치 알고리즘의 단계별 과정입니다.';
  } else if(pageId === 'assistantPage'){
    document.getElementById('pageAssistant').classList.add('active');
    titleEl.textContent = 'AI 어시스턴트';
    subEl.textContent = '대화를 통해 실시간으로 행사장 배치를 개선할 수 있습니다.';
  }
}

function openReportModal(){ document.getElementById('reportModal').classList.add('active'); }
function closeReportModal(){ document.getElementById('reportModal').classList.remove('active'); }

/* ==============================================
   AI GENERATE & BOOTH INITIALIZATION
   ============================================== */
function runAIGenerate(){
  // Read Inputs
  const name = document.getElementById('inputEventName').value;
  const sizeVal = document.getElementById('inputVenueSize').value;
  const shape = document.getElementById('inputVenueShape').value;
  const visitors = document.getElementById('inputVisitorCount').value;
  const time = document.getElementById('inputEventTime').value;
  const fee = document.getElementById('inputTicketFee').value;

  const [w, h] = sizeVal.split('x').map(Number);
  venue = { width: w, height: h, shape: shape };

  // Update Display Text
  document.getElementById('displayEventName').textContent = name;
  document.getElementById('displayVenueDim').textContent = `${w}m x ${h}m (${getShapeLabel(shape)})`;
  document.getElementById('displayVisitors').textContent = `${visitors}명`;
  document.getElementById('displayTime').textContent = time;
  document.getElementById('displayFee').textContent = fee;

  // Build Booth Layout based on Shape & Requirements
  generateOptimizedBooths(w, h, shape);

  // Transition directly to Design View
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
  resetSim();
}

function getShapeLabel(s){
  return {rect:'직사각형', square:'정사각형', lshape:'L자형', wide:'파노라마'}[s] || s;
}

function generateOptimizedBooths(w, h, shape){
  booths = [
    { id:'b1', name:'메인 무대', type:'main', x: w*0.35, y: h*0.08, w: w*0.3, h: h*0.2, color:'#2563eb' },
    { id:'b2', name:'인기 체험존 A', type:'popular', x: w*0.08, y: h*0.35, w: w*0.18, h: h*0.18, color:'#f43f5e' },
    { id:'b3', name:'인기 체험존 B', type:'popular', x: w*0.74, y: h*0.35, w: w*0.18, h: h*0.18, color:'#f43f5e' },
    { id:'b4', name:'의료/안전센터', type:'medical', x: w*0.08, y: h*0.78, w: w*0.15, h: h*0.15, color:'#10b981' },
    { id:'b5', name:'푸드 공간', type:'food', x: w*0.75, y: h*0.72, w: w*0.18, h: h*0.2, color:'#eab308' },
    { id:'b6', name:'중앙 휴식터', type:'rest', x: w*0.4, y: h*0.42, w: w*0.2, h: h*0.18, color:'#06b6d4' },
    { id:'b7', name:'IT 전시관', type:'normal', x: w*0.08, y: h*0.58, w: w*0.18, h: h*0.15, color:'#64748b' },
  ];

  if(shape === 'lshape'){
    // Adjust booths to avoid upper right corner cutout
    booths.forEach(b => {
      if(b.x > w*0.6 && b.y < h*0.4){
        b.x = w*0.35; b.y = h*0.7;
      }
    });
  }
}

/* ==============================================
   MULTI-DIRECTIONAL DYNAMIC SIMULATION
   ============================================== */
function initPeople(){
  people = [];
  const count = 70; // Representative agents for smooth canvas performance

  for(let i=0; i<count; i++){
    const startGateX = venue.width * (0.45 + (Math.random()-0.5)*0.15);
    const startGateY = venue.height * 0.92;

    people.push({
      x: startGateX,
      y: startGateY,
      vx: 0,
      vy: 0,
      speed: 0.12 + Math.random()*0.1,
      // Multi-destination route for diverse flow!
      targets: generateRandomSequence(),
      currentTargetIdx: 0,
      dwellTime: 0
    });
  }
}

function generateRandomSequence(){
  // People move in multiple directions across various booth destinations
  const indices = [0, 1, 2, 3, 4, 5, 6];
  // Shuffle array
  for (let i = indices.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [indices[i], indices[j]] = [indices[j], indices[i]];
  }
  return indices;
}

function updateSimulation(){
  if(!simRunning) return;

  simTime += 1;
  const mm = String(Math.floor(simTime / 60)).padStart(2, '0');
  const ss = String(simTime % 60).padStart(2, '0');
  document.getElementById('simTimeText').textContent = `경과 시간: ${mm}:${ss}`;

  people.forEach(p => {
    if(p.dwellTime > 0){
      p.dwellTime -= 1;
      return;
    }

    const targetBooth = booths[p.targets[p.currentTargetIdx]];
    if(!targetBooth) {
      p.currentTargetIdx = 0;
      return;
    }

    const tx = targetBooth.x + targetBooth.w/2 + (Math.random()-0.5)*2;
    const ty = targetBooth.y + targetBooth.h/2 + (Math.random()-0.5)*2;

    const dx = tx - p.x;
    const dy = ty - p.y;
    const dist = Math.hypot(dx, dy);

    if(dist < 1.5){
      // Reached destination, wait a bit then head to next!
      p.dwellTime = Math.floor(20 + Math.random()*40);
      p.currentTargetIdx = (p.currentTargetIdx + 1) % p.targets.length;
    } else {
      // Natural walking vector with slight noise
      p.x += (dx / dist) * p.speed + (Math.random()-0.5)*0.03;
      p.y += (dy / dist) * p.speed + (Math.random()-0.5)*0.03;
    }
  });

  drawPeople();
  drawHeatmap();
  requestAnimationFrame(updateSimulation);
}

function toggleSim(){
  simRunning = !simRunning;
  const btn = document.getElementById('btnPlaySim');
  if(simRunning){
    btn.textContent = '⏸ 일시정지';
    updateSimulation();
  } else {
    btn.textContent = '▶ 다방향 동선 시뮬레이션';
  }
}

function resetSim(){
  simRunning = false;
  simTime = 0;
  document.getElementById('simTimeText').textContent = '경과 시간: 00:00';
  document.getElementById('btnPlaySim').textContent = '▶ 다방향 동선 시뮬레이션';
  initPeople();
  drawVenue();
  drawPeople();
  drawHeatmap();
}

/* ==============================================
   CANVAS DRAWING (MAP & HEATMAP)
   ============================================== */
let venueCanvas, venueCtx;
let peopleCanvas, peopleCtx;
let heatmapCanvas, heatmapCtx;

function initCanvases(){
  venueCanvas = document.getElementById('venueCanvas');
  peopleCanvas = document.getElementById('peopleCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');

  if(!venueCanvas) return;

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth;
  const h = wrap.clientHeight;

  [venueCanvas, peopleCanvas, heatmapCanvas].forEach(c => {
    c.width = w;
    c.height = h;
  });

  venueCtx = venueCanvas.getContext('2d');
  peopleCtx = peopleCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');

  drawVenue();
  drawPeople();
  drawHeatmap();
}

function drawVenue(){
  if(!venueCtx) return;
  const w = venueCanvas.width;
  const h = venueCanvas.height;

  venueCtx.clearRect(0, 0, w, h);

  // Background Grid
  venueCtx.strokeStyle = '#e2e8f0';
  venueCtx.lineWidth = 1;
  const step = 20;
  for(let x=0; x<w; x+=step){
    venueCtx.beginPath(); venueCtx.moveTo(x,0); venueCtx.lineTo(x,h); venueCtx.stroke();
  }
  for(let y=0; y<h; y+=step){
    venueCtx.beginPath(); venueCtx.moveTo(0,y); venueCtx.lineTo(w,y); venueCtx.stroke();
  }

  // Draw Booths
  booths.forEach(b => {
    const bx = (b.x / venue.width) * w;
    const by = (b.y / venue.height) * h;
    const bw = (b.w / venue.width) * w;
    const bh = (b.h / venue.height) * h;

    venueCtx.fillStyle = b.color;
    venueCtx.globalAlpha = 0.85;
    venueCtx.beginPath();
    venueCtx.roundRect(bx, by, bw, bh, 8);
    venueCtx.fill();
    venueCtx.globalAlpha = 1.0;

    venueCtx.strokeStyle = '#1e293b';
    venueCtx.lineWidth = 1.5;
    venueCtx.stroke();

    // Text Label
    venueCtx.fillStyle = '#ffffff';
    venueCtx.font = 'bold 11px sans-serif';
    venueCtx.textAlign = 'center';
    venueCtx.fillText(b.name, bx + bw/2, by + bh/2 + 4);
  });

  // Entry / Exit Gate Marker
  const gateX = w * 0.45;
  const gateY = h * 0.92;
  venueCtx.fillStyle = '#10b981';
  venueCtx.beginPath();
  venueCtx.roundRect(gateX, gateY, w*0.1, h*0.06, 4);
  venueCtx.fill();
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 10px sans-serif';
  venueCtx.fillText('주출입구', gateX + (w*0.1)/2, gateY + 12);
}

function drawPeople(){
  if(!peopleCtx) return;
  const w = peopleCanvas.width;
  const h = peopleCanvas.height;

  peopleCtx.clearRect(0, 0, w, h);

  people.forEach(p => {
    const px = (p.x / venue.width) * w;
    const py = (p.y / venue.height) * h;

    peopleCtx.fillStyle = '#2563eb';
    peopleCtx.beginPath();
    peopleCtx.arc(px, py, 3.5, 0, Math.PI * 2);
    peopleCtx.fill();
  });
}

function drawHeatmap(){
  if(!heatmapCtx) return;
  const w = heatmapCanvas.width;
  const h = heatmapCanvas.height;

  heatmapCtx.clearRect(0, 0, w, h);

  people.forEach(p => {
    const px = (p.x / venue.width) * w;
    const py = (p.y / venue.height) * h;

    const grad = heatmapCtx.createRadialGradient(px, py, 0, px, py, 25);
    grad.addColorStop(0, 'rgba(239, 68, 68, 0.4)');
    grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.2)');
    grad.addColorStop(1, 'rgba(245, 158, 11, 0)');

    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(px, py, 25, 0, Math.PI * 2);
    heatmapCtx.fill();
  });
}

function zoomMap(delta){
  mapScale = Math.max(0.8, Math.min(1.5, mapScale + delta));
  const wrap = document.getElementById('mapWrap');
  wrap.style.transform = `scale(${mapScale})`;
  wrap.style.transformOrigin = 'center center';
}

/* ==============================================
   AI ASSISTANT INTERACTION
   ============================================== */
function sendChat(){
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if(!msg) return;

  appendChatMsg(msg, 'user', 'chatBox');
  input.value = '';

  setTimeout(() => {
    processAICommand(msg, 'chatBox');
  }, 500);
}

function sendFullChat(){
  const input = document.getElementById('fullChatInput');
  const msg = input.value.trim();
  if(!msg) return;

  appendChatMsg(msg, 'user', 'fullChatBox');
  input.value = '';

  setTimeout(() => {
    processAICommand(msg, 'fullChatBox');
  }, 500);
}

function applyQuickPrompt(text){
  appendChatMsg(text, 'user', 'chatBox');
  setTimeout(() => {
    processAICommand(text, 'chatBox');
  }, 400);
}

function appendChatMsg(text, sender, boxId){
  const box = document.getElementById(boxId);
  const div = document.createElement('div');
  div.className = `chat-msg ${sender}`;
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function processAICommand(cmd, boxId){
  let reply = "요청사항을 반영하여 레이아웃 및 동선을 조정했습니다.";

  if(cmd.includes('의료') || cmd.includes('안전')){
    reply = "의료/안전센터를 주출입구 바로 옆으로 이동시켜 비상시 접근성을 극대화했습니다.";
    const med = booths.find(b => b.type === 'medical');
    if(med){ med.x = venue.width * 0.08; med.y = venue.height * 0.78; }
  } else if(cmd.includes('푸드') || cmd.includes('출구')){
    reply = "푸드 공간을 우측 하단 출구 방향으로 재배치하여 음식 냄새 확산을 방지하고 관람객 체류를 분산했습니다.";
    const food = booths.find(b => b.type === 'food');
    if(food){ food.x = venue.width * 0.76; food.y = venue.height * 0.72; }
  } else if(cmd.includes('동선') || cmd.includes('통로') || cmd.includes('확대')){
    reply = "중앙 주요 통로 폭을 2.5m에서 3.5m로 확장하여 관람객 병목현상을 해결했습니다.";
    const rest = booths.find(b => b.type === 'rest');
    if(rest){ rest.w = venue.width * 0.16; }
  }

  appendChatMsg(reply, 'ai', boxId);
  drawVenue();
  drawPeople();
}

// Initial Boot
window.addEventListener('load', () => {
  runAIGenerate();
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=1100, scrolling=True)
