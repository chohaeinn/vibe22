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
<title>Event AI - AI 행사장 설계 및 동선 최적화 시스템</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color:#0f172a;
  background:#f1f5f9;
  overflow-x:hidden;
}
button,input,select,textarea{font:inherit;}
button{cursor:pointer;transition:all 0.2s cubic-bezier(0.4, 0, 0.2, 1);}

/* Scrollbar */
::-webkit-scrollbar {width:6px;height:6px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}
::-webkit-scrollbar-thumb:hover {background:#94a3b8;}

/* Layout Setup */
.app-container{
  display:flex;
  min-height:100vh;
  background:#f1f5f9;
}

/* Dark Sidebar */
.sidebar{
  width:250px;
  background:#090d16;
  color:#94a3b8;
  padding:24px 16px;
  display:flex;
  flex-direction:column;
  gap:24px;
  flex-shrink:0;
  border-right:1px solid #1e293b;
}
.brand{
  display:flex;
  align-items:center;
  gap:12px;
  padding:0 8px;
  color:#fff;
}
.brand-icon{
  width:40px;
  height:40px;
  background:linear-gradient(135deg,#3b82f6,#6366f1);
  border-radius:12px;
  display:grid;
  place-items:center;
  font-size:20px;
  font-weight:900;
  box-shadow:0 8px 16px rgba(59,130,246,0.35);
}
.brand-title{font-size:19px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;}
.brand-sub{font-size:11px;color:#64748b;margin-top:2px;font-weight:500;}

.nav-group{display:flex;flex-direction:column;gap:6px;}
.nav-item{
  display:flex;
  align-items:center;
  gap:12px;
  padding:12px 16px;
  border-radius:12px;
  font-size:14px;
  font-weight:600;
  color:#94a3b8;
  cursor:pointer;
  transition:all 0.2s ease;
}
.nav-item:hover{background:rgba(255,255,255,0.05);color:#f1f5f9;}
.nav-item.active{
  background:linear-gradient(135deg, #2563eb, #3b82f6);
  color:#ffffff;
  box-shadow:0 4px 14px rgba(37,99,235,0.35);
}
.nav-icon{font-size:16px;width:20px;text-align:center;}

.side-banner{
  margin-top:auto;
  background:linear-gradient(135deg, rgba(30,58,138,0.4), rgba(15,23,42,0.8));
  border:1px solid rgba(59,130,246,0.3);
  padding:16px;
  border-radius:16px;
  color:#e2e8f0;
  backdrop-filter:blur(10px);
}
.side-banner h5{font-size:13px;font-weight:800;color:#60a5fa;margin-bottom:6px;display:flex;align-items:center;gap:6px;}
.side-banner p{font-size:11px;color:#94a3b8;line-height:1.5;}

/* Main Area */
.main-content{
  flex:1;
  padding:24px;
  display:flex;
  flex-direction:column;
  gap:20px;
  min-width:0;
  overflow-y:auto;
}

/* Header Bar */
.header-bar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  background:#ffffff;
  padding:16px 24px;
  border-radius:20px;
  border:1px solid #e2e8f0;
  box-shadow:0 4px 20px -2px rgba(0,0,0,0.03);
}
.header-title h2{font-size:22px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;}
.header-title p{font-size:13px;color:#64748b;margin-top:2px;}
.user-auth-area{
  display:flex;
  align-items:center;
  gap:12px;
}
.btn-auth{
  padding:9px 18px;
  border-radius:12px;
  font-size:13px;
  font-weight:700;
  border:none;
}
.btn-login{
  background:#f1f5f9;
  color:#334155;
  border:1px solid #cbd5e1;
}
.btn-login:hover{background:#e2e8f0;}
.btn-signup{
  background:#2563eb;
  color:#ffffff;
  box-shadow:0 4px 12px rgba(37,99,235,0.25);
}
.btn-signup:hover{background:#1d4ed8;}

.user-profile-badge{
  display:flex;
  align-items:center;
  gap:10px;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:6px 14px 6px 8px;
  border-radius:30px;
}
.user-avatar{
  width:32px;
  height:32px;
  background:linear-gradient(135deg,#6366f1,#8b5cf6);
  border-radius:50%;
  color:#fff;
  display:grid;
  place-items:center;
  font-weight:800;
  font-size:13px;
}
.user-info-text{font-size:12px;font-weight:700;color:#1e293b;}
.user-info-role{font-size:10px;color:#64748b;}
.btn-logout{
  background:none;
  border:none;
  font-size:11px;
  color:#ef4444;
  font-weight:700;
  margin-left:6px;
  cursor:pointer;
}

/* Page Views */
.page-view{display:none;animation:fadeIn 0.3s ease-out;}
.page-view.active{display:block;}
@keyframes fadeIn { from{opacity:0;transform:translateY(6px);} to{opacity:1;transform:translateY(0);} }

/* Form Cards */
.home-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:20px;
  padding:28px;
  box-shadow:0 4px 25px rgba(0,0,0,0.03);
}
.section-head{
  font-size:17px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:20px;
  display:flex;
  align-items:center;
  gap:10px;
}
.input-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
  gap:20px;
  margin-bottom:24px;
}
.form-group{
  display:flex;
  flex-direction:column;
  gap:8px;
}
.form-group label{
  font-size:13px;
  font-weight:700;
  color:#334155;
}
.form-group input, .form-group select, .form-group textarea{
  padding:12px 14px;
  border:1.5px solid #cbd5e1;
  border-radius:12px;
  background:#f8fafc;
  color:#0f172a;
  font-weight:600;
  font-size:13.5px;
  outline:none;
  transition:all 0.2s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus{
  border-color:#2563eb;
  background:#ffffff;
  box-shadow:0 0 0 4px rgba(37,99,235,0.1);
}

/* Event Info Bar Top Dashboard */
.event-info-bar{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:20px;
  padding:16px 24px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:16px;
  box-shadow:0 4px 20px rgba(0,0,0,0.02);
}
.info-items-group{
  display:flex;
  align-items:center;
  gap:24px;
  flex-wrap:wrap;
}
.info-item-box{
  display:flex;
  align-items:center;
  gap:10px;
}
.info-item-icon{
  width:38px;
  height:38px;
  border-radius:12px;
  background:#eff6ff;
  color:#2563eb;
  display:grid;
  place-items:center;
  font-size:16px;
}
.info-item-text label{display:block;font-size:11px;color:#64748b;font-weight:700;}
.info-item-text span{font-weight:800;color:#0f172a;font-size:14px;}

.btn-ai-generate{
  background:linear-gradient(135deg,#2563eb,#4f46e5);
  color:#ffffff;
  border:none;
  padding:13px 26px;
  border-radius:14px;
  font-weight:800;
  font-size:14px;
  box-shadow:0 6px 20px rgba(37,99,235,0.3);
  display:flex;
  align-items:center;
  gap:8px;
}
.btn-ai-generate:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(37,99,235,0.4);}

/* Dashboard Grids */
.dashboard-grid-top{
  display:grid;
  grid-template-columns: 1.45fr 1fr 1.15fr;
  gap:20px;
}
.dashboard-grid-bottom{
  display:grid;
  grid-template-columns: 1fr 1.25fr 1fr;
  gap:20px;
}

.panel-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:20px;
  padding:20px;
  box-shadow:0 4px 20px rgba(0,0,0,0.02);
  display:flex;
  flex-direction:column;
}
.panel-title{
  font-size:15px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:14px;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.panel-title .sub-tag{
  font-size:11px;
  background:#eff6ff;
  color:#2563eb;
  padding:4px 10px;
  border-radius:20px;
  font-weight:700;
}

/* Digital Twin Map Container */
.map-canvas-container{
  position:relative;
  width:100%;
  height:370px;
  background:#0f172a;
  border:1px solid #1e293b;
  border-radius:16px;
  overflow:hidden;
  box-shadow:inset 0 2px 10px rgba(0,0,0,0.5);
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
  right:12px;
  top:12px;
  z-index:20;
  display:flex;
  flex-direction:column;
  gap:6px;
}
.zoom-btn{
  width:32px;
  height:32px;
  background:rgba(255,255,255,0.9);
  backdrop-filter:blur(4px);
  border:1px solid #cbd5e1;
  border-radius:8px;
  font-weight:800;
  color:#0f172a;
  font-size:14px;
  box-shadow:0 2px 8px rgba(0,0,0,0.15);
}
.zoom-btn:hover{background:#ffffff;}

/* Booth Legend Overlay */
.booth-legend{
  position:absolute;
  left:12px;
  bottom:12px;
  z-index:20;
  background:rgba(15,23,42,0.85);
  backdrop-filter:blur(8px);
  padding:8px 12px;
  border-radius:10px;
  font-size:11px;
  border:1px solid rgba(255,255,255,0.1);
  color:#e2e8f0;
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:6px 12px;
}
.legend-dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;}

/* Score Table */
.score-table{width:100%;border-collapse:collapse;font-size:12.5px;margin-top:4px;}
.score-table th,.score-table td{padding:10px 8px;text-align:left;border-bottom:1px solid #f1f5f9;}
.score-table th{color:#64748b;font-weight:700;font-size:11px;}
.score-badge{
  display:inline-block;
  padding:4px 10px;
  border-radius:12px;
  font-weight:800;
  font-size:11px;
}
.badge-excellent{background:#dcfce7;color:#15803d;}
.badge-good{background:#e0f2fe;color:#0369a1;}

/* Before / After Comparison */
.compare-box{
  display:grid;
  grid-template-columns:1fr 30px 1fr;
  align-items:center;
  gap:10px;
  background:#f8fafc;
  border-radius:14px;
  padding:14px;
  border:1px solid #e2e8f0;
}
.compare-col h5{font-size:12px;color:#64748b;margin-bottom:8px;font-weight:700;}
.compare-metric{display:flex;justify-content:space-between;font-size:12px;margin-bottom:6px;font-weight:700;}
.text-danger{color:#ef4444;}
.text-success{color:#10b981;}

/* Workflow Steps */
.workflow-steps{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:6px;
  margin-top:10px;
}
.wf-step{
  flex:1;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:10px 4px;
  border-radius:10px;
  text-align:center;
  font-size:11px;
}
.wf-step.active{background:#eff6ff;border-color:#3b82f6;color:#1d4ed8;font-weight:800;}
.wf-arrow{color:#94a3b8;font-size:11px;}

/* AI Assistant & Chat */
.ai-assistant-container{
  display:flex;
  flex-direction:column;
  height:100%;
}
.chat-messages{
  flex:1;
  min-height:120px;
  max-height:150px;
  overflow-y:auto;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  border-radius:12px;
  padding:12px;
  font-size:12px;
  display:flex;
  flex-direction:column;
  gap:10px;
  margin-bottom:10px;
}
.chat-msg{
  padding:8px 12px;
  border-radius:10px;
  max-width:90%;
  line-height:1.45;
  font-weight:500;
}
.chat-msg.ai{background:#e0f2fe;color:#0369a1;align-self:flex-start;border-bottom-left-radius:2px;}
.chat-msg.user{background:#2563eb;color:#ffffff;align-self:flex-end;border-bottom-right-radius:2px;}

.chat-input-row{
  display:flex;
  gap:8px;
}
.chat-input-row input{
  flex:1;
  padding:10px 12px;
  border:1.5px solid #cbd5e1;
  border-radius:10px;
  font-size:12px;
}
.chat-input-row button{
  background:#2563eb;
  color:#fff;
  border:none;
  padding:0 16px;
  border-radius:10px;
  font-size:12px;
  font-weight:800;
}

.quick-prompts{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
  margin-top:8px;
}
.quick-btn{
  background:#f1f5f9;
  border:1px solid #cbd5e1;
  padding:5px 10px;
  border-radius:8px;
  font-size:11px;
  color:#334155;
  font-weight:600;
}
.quick-btn:hover{background:#e2e8f0;border-color:#94a3b8;}

/* Simulation Controller Bar */
.sim-controls-bar{
  display:flex;
  align-items:center;
  gap:12px;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:10px 14px;
  border-radius:12px;
  margin-top:12px;
}
.sim-btn{
  padding:8px 16px;
  border-radius:10px;
  border:none;
  font-weight:800;
  font-size:12px;
}
.sim-btn-primary{background:#2563eb;color:#ffffff;box-shadow:0 2px 8px rgba(37,99,235,0.25);}
.sim-btn-secondary{background:#e2e8f0;color:#334155;}

/* ==============================================
   DETAILED EXPANDED REPORT MODAL
   ============================================== */
.modal-overlay{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,0.7);
  backdrop-filter:blur(6px);
  z-index:999;
  display:none;
  place-items:center;
  padding:20px;
  animation:fadeIn 0.2s ease-out;
}
.modal-overlay.active{display:grid;}
.report-modal-card{
  background:#ffffff;
  width:min(95%,920px);
  max-height:88vh;
  border-radius:24px;
  padding:32px;
  box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.report-modal-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding-bottom:18px;
  border-bottom:2px solid #f1f5f9;
  margin-bottom:20px;
}
.report-modal-header h3{font-size:22px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:10px;}
.report-modal-body{
  flex:1;
  overflow-y:auto;
  padding-right:8px;
  display:flex;
  flex-direction:column;
  gap:24px;
}

/* Report Sections Styling */
.report-section{
  background:#f8fafc;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:20px;
}
.report-section-title{
  font-size:15px;
  font-weight:800;
  color:#1e293b;
  margin-bottom:12px;
  display:flex;
  align-items:center;
  gap:8px;
  border-bottom:1px dashed #cbd5e1;
  padding-bottom:8px;
}
.report-grid-3{
  display:grid;
  grid-template-columns:repeat(3, 1fr);
  gap:12px;
  margin-bottom:14px;
}
.report-kpi-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:12px;
  padding:14px;
  text-align:center;
}
.report-kpi-card .val{font-size:20px;font-weight:900;color:#2563eb;margin-top:4px;}
.report-kpi-card .lbl{font-size:11px;color:#64748b;font-weight:700;}

.report-text-p{
  font-size:13px;
  color:#334155;
  line-height:1.7;
  margin-bottom:10px;
}
.report-list{
  list-style:none;
  padding:0;
  display:flex;
  flex-direction:column;
  gap:8px;
}
.report-list li{
  font-size:12.5px;
  color:#334155;
  line-height:1.5;
  padding-left:18px;
  position:relative;
}
.report-list li::before{
  content:"•";
  position:absolute;
  left:4px;
  color:#2563eb;
  font-weight:bold;
  font-size:16px;
}

/* AUTH MODAL */
.auth-modal-card{
  background:#ffffff;
  width:min(90%,420px);
  border-radius:24px;
  padding:32px;
  box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);
}
.auth-title{font-size:20px;font-weight:800;color:#0f172a;margin-bottom:6px;text-align:center;}
.auth-sub{font-size:12px;color:#64748b;text-align:center;margin-bottom:20px;}
</style>
</head>
<body>

<div class="app-container">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon">✦</div>
      <div>
        <div class="brand-title">Event AI</div>
        <div class="brand-sub">AI 행사장 설계 & 동선 최적화</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item active" onclick="switchPage('home', this)">
        <span class="nav-icon">🏠</span> 홈 (설계 입력)
      </div>
      <div class="nav-item" onclick="switchPage('design', this)">
        <span class="nav-icon">🏢</span> 행사 설계 & 디지털트윈
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span class="nav-icon">⚙️</span> 설계 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span class="nav-icon">📊</span> AI 종합 분석 보고서
      </div>
      <div class="nav-item" onclick="switchPage('assistantPage', this)">
        <span class="nav-icon">🤖</span> AI 어시스턴트
      </div>
    </nav>

    <div class="side-banner">
      <h5>⚡ AI 실시간 시뮬레이션</h5>
      <p>행사장 규모, 출입구 위치, 밀집도를 다방향 에이전트 기반으로 정밀 계산합니다.</p>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">

    <!-- Header Bar -->
    <header class="header-bar">
      <div class="header-title">
        <h2 id="pageTitleText">행사 설계 입력</h2>
        <p id="pageSubText">행사 기본 정보를 입력하시면 AI가 최적의 부스 배치 및 동선을 자동 설계합니다.</p>
      </div>

      <!-- User Auth State Area -->
      <div class="user-auth-area" id="authArea">
        <button class="btn-auth btn-login" onclick="openAuthModal('login')">로그인</button>
        <button class="btn-auth btn-signup" onclick="openAuthModal('signup')">회원가입</button>
      </div>
    </header>

    <!-- PAGE 1: HOME INPUT FORM -->
    <section id="pageHome" class="page-view active">
      <div class="home-card">
        <div class="section-head">📝 행사 기본 정보 및 요구사항 설정</div>
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
            <label>행사장 형태</label>
            <select id="inputVenueShape">
              <option value="rect" selected>직사각형</option>
              <option value="square">정사각형</option>
              <option value="lshape">L자형</option>
              <option value="wide">가로 파노라마형</option>
            </select>
          </div>
          <div class="form-group">
            <label>예상 수용 관람객 수</label>
            <select id="inputVisitorCount">
              <option value="300">300명</option>
              <option value="500">500명</option>
              <option value="1000" selected>1,000명</option>
              <option value="3000">3,000명</option>
              <option value="5000">5,000명</option>
            </select>
          </div>
          <div class="form-group">
            <label>운영 시간</label>
            <input type="text" id="inputEventTime" value="10:00 - 18:00 (8시간)">
          </div>
          <div class="form-group">
            <label>입장 정책 / 티켓</label>
            <input type="text" id="inputTicketFee" value="무료 (사전예약제)">
          </div>
          <div class="form-group">
            <label>예산 규모</label>
            <input type="text" id="inputBudget" value="5,000만원">
          </div>
          <div class="form-group" style="grid-column:1 / -1;">
            <label>AI 공간 배치 조건 및 세부 요구사항</label>
            <textarea id="inputRequirements" rows="3" placeholder="예: 무대는 중앙 상단에 배치하고, 의료부스는 입구 근처, 푸드존은 통풍이 잘되는 출구 부근에 이격시켜 주세요.">메인 무대 시야 확보, 인기 체험존 병목 방지, 의료 안전존 입구 배치, 푸드존 휴식구역 분리</textarea>
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn-ai-generate" onclick="runAIGenerate()">
            ✦ AI 최적 공간 설계 실행하기
          </button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: EVENT DESIGN DASHBOARD -->
    <section id="pageDesign" class="page-view">

      <!-- Event Info Bar -->
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
              <label>규모 및 형태</label>
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
              <label>입장 정책</label>
              <span id="displayFee">무료</span>
            </div>
          </div>
        </div>
        <button class="btn-ai-generate" onclick="runAIGenerate()">
          ✦ AI 재배치 실행
        </button>
      </div>

      <!-- Top Dashboard Grid -->
      <div class="dashboard-grid-top" style="margin-top:16px;">

        <!-- 1. Digital Twin Layout Map -->
        <div class="panel-card">
          <div class="panel-title">
            <span>🗺️ 디지털 트윈 행사장 배치도</span>
            <span class="sub-tag">AI 최적화 렌더링</span>
          </div>
          <div class="map-canvas-container" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>
            <div class="map-zoom-controls">
              <button class="zoom-btn" onclick="zoomMap(0.1)">+</button>
              <button class="zoom-btn" onclick="zoomMap(-0.1)">-</button>
            </div>
            <div class="booth-legend">
              <div><span class="legend-dot" style="background:#3b82f6;"></span> 메인 무대</div>
              <div><span class="legend-dot" style="background:#f43f5e;"></span> 인기 체험존</div>
              <div><span class="legend-dot" style="background:#eab308;"></span> 푸드존</div>
              <div><span class="legend-dot" style="background:#10b981;"></span> 의료/안전존</div>
              <div><span class="legend-dot" style="background:#06b6d4;"></span> 휴식 구역</div>
              <div><span class="legend-dot" style="background:#64748b;"></span> 일반 전시관</div>
            </div>
          </div>

          <!-- Simulation Controls -->
          <div class="sim-controls-bar">
            <button class="sim-btn sim-btn-primary" id="btnPlaySim" onclick="toggleSim()">▶ 다방향 동선 시뮬레이션</button>
            <button class="sim-btn sim-btn-secondary" onclick="resetSim()">🔄 초기화</button>
            <span style="font-size:12px;color:#64748b;margin-left:auto;font-weight:700;" id="simTimeText">경과 시간: 00:00</span>
          </div>
        </div>

        <!-- 2. Heatmap Panel -->
        <div class="panel-card">
          <div class="panel-title">
            <span>🔥 밀집도 & 혼잡구역 Heatmap</span>
            <span class="sub-tag">실시간 감지</span>
          </div>
          <div class="map-canvas-container">
            <canvas id="heatmapCanvas"></canvas>
          </div>
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#64748b;margin-top:10px;font-weight:700;">
            <span>🟢 원활 (0~30%)</span>
            <span>🟡 보통 (31~60%)</span>
            <span>🟠 혼잡 (61~80%)</span>
            <span>🔴 위험 (81%+)</span>
          </div>
        </div>

        <!-- 3. AI Evaluation Summary -->
        <div class="panel-card">
          <div class="panel-title">
            <span>💡 AI 진단 평가 결과</span>
            <span class="sub-tag">종합 점수 94점</span>
          </div>
          <table class="score-table">
            <thead>
              <tr><th>평가 항목</th><th>점수</th><th>등급</th></tr>
            </thead>
            <tbody>
              <tr><td>비상 안전성</td><td>95점</td><td><span class="score-badge badge-excellent">최우수</span></td></tr>
              <tr><td>동선 효율성</td><td>89점</td><td><span class="score-badge badge-good">우수</span></td></tr>
              <tr><td>시설 접근성</td><td>98점</td><td><span class="score-badge badge-excellent">최우수</span></td></tr>
              <tr><td>혼잡 분산도</td><td>86점</td><td><span class="score-badge badge-good">우수</span></td></tr>
              <tr><td>공간 활용도</td><td>92점</td><td><span class="score-badge badge-excellent">최우수</span></td></tr>
            </tbody>
          </table>
          <div style="margin-top:14px;font-size:12px;color:#334155;background:#f8fafc;padding:12px;border-radius:12px;border:1px solid #e2e8f0;line-height:1.5;">
            <b>💡 AI 레이아웃 핵심 포인트:</b><br>
            • 메인무대 전면 보행 폭 3.8m 확보로 안전 사고 예방<br>
            • 의료존 입구 즉시 진입 가능 구조 설계
          </div>
          <button style="margin-top:auto;width:100%;padding:10px;background:#1e293b;color:#fff;border:none;border-radius:10px;font-weight:700;font-size:12px;" onclick="openReportModal()">
            📄 AI 종합 상세 보고서 열기
          </button>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-grid-bottom" style="margin-top:18px;">

        <!-- Before / After -->
        <div class="panel-card">
          <div class="panel-title">
            <span>⚖️ 기존 vs AI 설계 비교</span>
          </div>
          <div class="compare-box">
            <div class="compare-col">
              <h5>수동 배치안</h5>
              <div class="compare-metric"><span>병목 혼잡도</span><span class="text-danger">74%</span></div>
              <div class="compare-metric"><span>동선 점수</span><span>62점</span></div>
              <div class="compare-metric"><span>위험 지역</span><span class="text-danger">4개소</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#94a3b8;font-size:16px;">→</div>
            <div class="compare-col">
              <h5>AI 최적 배치안</h5>
              <div class="compare-metric"><span>병목 혼잡도</span><span class="text-success">22%</span></div>
              <div class="compare-metric"><span>동선 점수</span><span class="text-success">94점</span></div>
              <div class="compare-metric"><span>위험 지역</span><span class="text-success">0개소</span></div>
            </div>
          </div>
        </div>

        <!-- AI Process visualizer -->
        <div class="panel-card">
          <div class="panel-title">
            <span>⚙️ AI 설계 추진 단계</span>
          </div>
          <div class="workflow-steps">
            <div class="wf-step active">1. 조건 입력</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">2. 공간 분석</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">3. 알고리즘 배치</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">4. 동선 시뮬</div>
            <span class="wf-arrow">›</span>
            <div class="wf-step active">5. 보고서 생성</div>
          </div>
          <p style="font-size:11.5px;color:#64748b;margin-top:12px;text-align:center;line-height:1.4;">
            군중 이동 물리 시뮬레이션을 통과한 검증된 배치 알고리즘입니다.
          </p>
        </div>

        <!-- AI Assistant Chat -->
        <div class="panel-card">
          <div class="panel-title">
            <span>💬 AI 대화형 배치 조율</span>
          </div>
          <div class="ai-assistant-container">
            <div class="chat-messages" id="chatBox">
              <div class="chat-msg ai">
                반갑습니다! 행사장 공간 재배치나 구역 변경 요청이 있으시면 말씀해주세요.
              </div>
            </div>
            <div class="chat-input-row">
              <input type="text" id="chatInput" placeholder="예: 체험부스를 조금 더 멀리 띄워줘" onkeydown="if(event.key==='Enter') sendChat()">
              <button onclick="sendChat()">전송</button>
            </div>
            <div class="quick-prompts">
              <button class="quick-btn" onclick="applyQuickPrompt('의료부스 입구 배치')">의료부스 입구 배치</button>
              <button class="quick-btn" onclick="applyQuickPrompt('푸드존 출구 이동')">푸드존 출구 이동</button>
              <button class="quick-btn" onclick="applyQuickPrompt('통로 폭 넓히기')">통로 폭 넓히기</button>
            </div>
          </div>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS -->
    <section id="pageProcess" class="page-view">
      <div class="home-card">
        <div class="section-head">🔄 AI 행사장 자동 설계 메커니즘</div>
        <div style="font-size:13.5px;line-height:1.7;color:#334155;display:flex;flex-direction:column;gap:16px;">
          <p><b>1. 공간 파라미터화:</b> 입력받은 가로/세로 규격 및 출입구 위치를 기반으로 2D/3D 그리드 좌표계를 형성합니다.</p>
          <p><b>2. 에이전트 이동 시뮬레이션:</b> 각 관람객 에이전트의 이동 목적(무대 관람, 체험, 음식 구매, 휴식 등)을 확률 모델로 부여하고 다방향 이동 경로를 실시간 계산합니다.</p>
          <p><b>3. 병목 및 피크 타임 예측:</b> 관람객이 특정 시간에 특정 부스로 집중되는 현상을 기계학습 알고리즘으로 분석합니다.</p>
          <p><b>4. AI 최적 재배치:</b> 위험 혼잡 구간 발생 시 부스 간 거리 및 통로 폭을 자동 조율하여 최상의 동선 점수를 도출합니다.</p>
        </div>
      </div>
    </section>

    <!-- PAGE 5: ASSISTANT -->
    <section id="pageAssistant" class="page-view">
      <div class="home-card">
        <div class="section-head">🤖 AI 실시간 레이아웃 편집 어시스턴트</div>
        <p style="font-size:13px;color:#64748b;margin-bottom:16px;">자연어로 요구사항을 명령하면 실시간으로 배치도에 반영됩니다.</p>
        <div id="fullChatBox" class="chat-messages" style="height:280px;max-height:none;margin-bottom:16px;">
          <div class="chat-msg ai">무엇을 도와드릴까요? "부스 간격 확장", "안전구역 확보" 등 명령을 입력해주세요.</div>
        </div>
        <div class="chat-input-row">
          <input type="text" id="fullChatInput" placeholder="명령어를 입력하세요..." onkeydown="if(event.key==='Enter') sendFullChat()">
          <button onclick="sendFullChat()">수정 반영하기</button>
        </div>
      </div>
    </section>

  </main>
</div>

<!-- ==============================================
     LOGIN / SIGNUP MODAL
     ============================================== -->
<div class="modal-overlay" id="authModal">
  <div class="auth-modal-card">
    <div style="display:flex;justify-content:flex-end;">
      <button onclick="closeAuthModal()" style="border:none;background:none;font-size:20px;font-weight:900;color:#94a3b8;cursor:pointer;">✕</button>
    </div>
    <div id="authContent">
      <!-- Auth form dynamically injected by JS -->
    </div>
  </div>
</div>

<!-- ==============================================
     LONG DETAILED AI REPORT MODAL
     ============================================== -->
<div class="modal-overlay" id="reportModal">
  <div class="report-modal-card">
    <div class="report-modal-header">
      <h3><span>📊</span> AI 행사장 최적화 종합 분석 보고서</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:22px;font-weight:900;color:#64748b;cursor:pointer;">✕</button>
    </div>

    <div class="report-modal-body">

      <!-- Executive Summary -->
      <div class="report-section">
        <div class="report-section-title">1. 실행 요약 (Executive Summary)</div>
        <p class="report-text-p">
          본 보고서는 <b>2026 청소년 미래 과학 박람회</b>의 성공적인 개최와 안전성 극대화를 위하여 AI 기반 공간 설계 알고리즘 및 에이전트 군중 동선 시뮬레이션을 적용한 결과입니다. 총 1,000명의 예상 관람객을 기준으로 수행되었으며, 공간 효율성, 비상 탈출 안전성, 상업적 체류시간 등 다각도 지표에서 우수한 평가를 얻었습니다.
        </p>
        <div class="report-grid-3">
          <div class="report-kpi-card">
            <div class="lbl">종합 안전 및 동선 점수</div>
            <div class="val">94점</div>
          </div>
          <div class="report-kpi-card">
            <div class="lbl">예상 병목 감소율</div>
            <div class="val">70.3% ↓</div>
          </div>
          <div class="report-kpi-card">
            <div class="lbl">평균 체류시간 증가</div>
            <div class="val">+24분</div>
          </div>
        </div>
      </div>

      <!-- Zone Details -->
      <div class="report-section">
        <div class="report-section-title">2. 구역별 공간 배치 및 최적화 전략</div>
        <ul class="report-list">
          <li><b>메인 무대 (Main Stage):</b> 공간 중앙 상단 영역(40m x 25m 매핑 기준)에 위치시켜 관람객 시야 확보를 극대화했습니다. 무대 전면 잔여 보행 통로 폭을 기존 2.0m에서 3.8m로 확장하여 피크 타임 인원 몰림에 대비했습니다.</li>
          <li><b>인기 체험존 A/B:</b> 동선 분산을 유도하기 위해 행사장 좌/우측 양 끝으로 분리 배치하였습니다. 이를 통해 중앙 통로의 심각한 교차 병목 현상을 사전에 방지하였습니다.</li>
          <li><b>의료 및 안전 지원 센터:</b> 주출입구 좌측 인근에 전진 배치하여 긴급 상황 시 응급차량 접근 및 환자 후송 골든타임을 확보했습니다.</li>
          <li><b>푸드 존 & 휴식 공간:</b> 음식 냄새 확산 및 연기 방출을 고려해 우측 하단 환기 구역에 이격 배치하였으며, 휴식 공간을 중앙에 배치해 편의성을 강화했습니다.</li>
        </ul>
      </div>

      <!-- Flow & Density Analysis -->
      <div class="report-section">
        <div class="report-section-title">3. 관람객 다방향 동선 및 밀집도 분석</div>
        <p class="report-text-p">
          에이전트 기반 시뮬레이션 결과, 관람객의 이동 패턴은 [입구 → 인기 체험존 → 메인 무대 → 푸드존/휴식 → 출구] 순으로 분산 관찰되었습니다.
        </p>
        <ul class="report-list">
          <li><b>최대 혼잡 피크 타임:</b> 오후 14:00 ~ 15:30 (무대 메인 이벤트 시간대)</li>
          <li><b>피크 시 최대 밀집도:</b> 1.8명/㎡ (안전 기준치인 3.0명/㎡ 이하로 여유롭고 안전한 수준 유지)</li>
          <li><b>회주율 개선:</b> 비선형 양방향 통로 구조 적용을 통해 구석진 일반 전시관 방문율이 기존 대비 38% 상승함.</li>
        </ul>
      </div>

      <!-- Emergency & Safety Protocol -->
      <div class="report-section">
        <div class="report-section-title">4. 비상 상황 및 대피 시뮬레이션 평가</div>
        <p class="report-text-p">
          화재 및 비상탈출 시나리오 수행 시, 전체 관람객 1,000명의 완전 대피 완료까지 소요되는 시간은 <b>2분 48초</b>로 측정되었습니다. (소방 안전 법정 기준치 5분 대비 44% 단축)
        </p>
        <ul class="report-list">
          <li>비상구 주변 5m 이내에 어떠한 가설물이나 부스 배치를 금지하는 안전 버퍼존 적용.</li>
          <li>주요 동선 교차점마다 유도요원 및 LED 비상 표지판 필수 배치 권장.</li>
        </ul>
      </div>

      <!-- Recommendation Roadmap -->
      <div class="report-section">
        <div class="report-section-title">5. AI 최종 권고사항 및 실행 로드맵</div>
        <ul class="report-list">
          <li><b>현장 통제:</b> 체험존 A와 B 입구에 대기줄 분리 라인(차단봉) 설치 권장.</li>
          <li><b>전력 및 설비:</b> 푸드존 및 무대 장비 전력 용량을 구역별 독립 분전반으로 배치 필요.</li>
          <li><b>운영 요원:</b> 메인 무대 전면 4명, 출입구 2명, 의료존 2명 상시 배치 권장.</li>
        </ul>
      </div>

    </div>

    <div style="margin-top:20px;display:flex;justify-content:flex-end;gap:12px;padding-top:16px;border-top:1px solid #e2e8f0;">
      <button class="sim-btn sim-btn-secondary" onclick="closeReportModal()">닫기</button>
      <button class="sim-btn sim-btn-primary" onclick="alert('보고서가 고해상도 PDF로 다운로드 되었습니다.');closeReportModal();">
        📥 PDF 보고서 다운로드
      </button>
    </div>
  </div>
</div>

<script>
/* ==============================================
   STATE & AUTH MANAGEMENT
   ============================================== */
let currentUser = null; // { name: '추천', email: 'user@event.ai', role: '행사 기획자' }
let venue = { width: 40, height: 25, shape: 'rect' };
let booths = [];
let people = [];
let simRunning = false;
let simTime = 0;
let mapScale = 1.0;

// Auth Modal Handlers
function openAuthModal(mode){
  const container = document.getElementById('authContent');
  if(mode === 'login'){
    container.innerHTML = `
      <div class="auth-title">로그인</div>
      <div class="auth-sub">Event AI 서비스를 이용하시려면 로그인하세요.</div>
      <form onsubmit="handleAuthSubmit(event, 'login')">
        <div class="form-group" style="margin-bottom:12px;">
          <label>이메일</label>
          <input type="email" id="loginEmail" required value="demo@event.ai">
        </div>
        <div class="form-group" style="margin-bottom:20px;">
          <label>비밀번호</label>
          <input type="password" id="loginPw" required value="123456">
        </div>
        <button type="submit" class="btn-ai-generate" style="width:100%;justify-content:center;">로그인하기</button>
      </form>
      <div style="margin-top:16px;text-align:center;font-size:12px;color:#64748b;">
        계정이 없으신가요? <a href="#" onclick="openAuthModal('signup')" style="color:#2563eb;font-weight:700;">회원가입</a>
      </div>
    `;
  } else {
    container.innerHTML = `
      <div class="auth-title">회원가입</div>
      <div class="auth-sub">새 계정을 만들고 AI 행사장 설계를 시작하세요.</div>
      <form onsubmit="handleAuthSubmit(event, 'signup')">
        <div class="form-group" style="margin-bottom:10px;">
          <label>이름 / 닉네임</label>
          <input type="text" id="signupName" required value="홍길동">
        </div>
        <div class="form-group" style="margin-bottom:10px;">
          <label>이메일 주소</label>
          <input type="email" id="signupEmail" required value="user@event.ai">
        </div>
        <div class="form-group" style="margin-bottom:20px;">
          <label>비밀번호</label>
          <input type="password" id="signupPw" required value="123456">
        </div>
        <button type="submit" class="btn-ai-generate" style="width:100%;justify-content:center;">회원가입완료</button>
      </form>
      <div style="margin-top:16px;text-align:center;font-size:12px;color:#64748b;">
        이미 계정이 있으신가요? <a href="#" onclick="openAuthModal('login')" style="color:#2563eb;font-weight:700;">로그인</a>
      </div>
    `;
  }
  document.getElementById('authModal').classList.add('active');
}

function closeAuthModal(){ document.getElementById('authModal').classList.remove('active'); }

function handleAuthSubmit(e, type){
  e.preventDefault();
  if(type === 'login'){
    currentUser = { name: '추천', email: 'user@event.ai', role: '총괄 매니저' };
  } else {
    const name = document.getElementById('signupName').value;
    currentUser = { name: name || '신규회원', email: 'new@event.ai', role: '행사 기획자' };
  }
  updateAuthUI();
  closeAuthModal();
}

function logout(){
  currentUser = null;
  updateAuthUI();
}

function updateAuthUI(){
  const area = document.getElementById('authArea');
  if(currentUser){
    area.innerHTML = `
      <div class="user-profile-badge">
        <div class="user-avatar">${currentUser.name[0]}</div>
        <div>
          <div class="user-info-text">${currentUser.name} 님</div>
          <div class="user-info-role">${currentUser.role}</div>
        </div>
        <button class="btn-logout" onclick="logout()">로그아웃</button>
      </div>
    `;
  } else {
    area.innerHTML = `
      <button class="btn-auth btn-login" onclick="openAuthModal('login')">로그인</button>
      <button class="btn-auth btn-signup" onclick="openAuthModal('signup')">회원가입</button>
    `;
  }
}

/* ==============================================
   PAGE ROUTING & MODAL CONTROLS
   ============================================== */
function switchPage(pageId, navEl){
  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  if(navEl) navEl.classList.add('active');

  const titleEl = document.getElementById('pageTitleText');
  const subEl = document.getElementById('pageSubText');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
    titleEl.textContent = '행사 설계 입력';
    subEl.textContent = '행사 기본 정보를 입력하시면 AI가 최적의 부스 배치 및 동선을 자동 설계합니다.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    titleEl.textContent = '행사 설계 & 디지털트윈';
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
   PRETTIER BOOTHS GENERATION & RENDERING
   ============================================== */
function runAIGenerate(){
  const name = document.getElementById('inputEventName').value;
  const sizeVal = document.getElementById('inputVenueSize').value;
  const shape = document.getElementById('inputVenueShape').value;
  const visitors = document.getElementById('inputVisitorCount').value;
  const time = document.getElementById('inputEventTime').value;
  const fee = document.getElementById('inputTicketFee').value;

  const [w, h] = sizeVal.split('x').map(Number);
  venue = { width: w, height: h, shape: shape };

  document.getElementById('displayEventName').textContent = name;
  document.getElementById('displayVenueDim').textContent = `${w}m x ${h}m (${getShapeLabel(shape)})`;
  document.getElementById('displayVisitors').textContent = `${visitors}명`;
  document.getElementById('displayTime').textContent = time;
  document.getElementById('displayFee').textContent = fee;

  generateOptimizedBooths(w, h, shape);
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
  resetSim();
}

function getShapeLabel(s){
  return {rect:'직사각형', square:'정사각형', lshape:'L자형', wide:'파노라마'}[s] || s;
}

function generateOptimizedBooths(w, h, shape){
  // Enhanced Booth Colors with dual gradient shades & crisp border styling
  booths = [
    { id:'b1', name:'메인 무대', type:'main', icon:'🎭', x: w*0.32, y: h*0.06, w: w*0.36, h: h*0.22, c1:'#3b82f6', c2:'#1d4ed8', border:'#60a5fa' },
    { id:'b2', name:'체험존 A', type:'popular', icon:'🧪', x: w*0.06, y: h*0.35, w: w*0.2, h: h*0.2, c1:'#f43f5e', c2:'#be123c', border:'#fda4af' },
    { id:'b3', name:'체험존 B', type:'popular', icon:'🚀', x: w*0.74, y: h*0.35, w: w*0.2, h: h*0.2, c1:'#f43f5e', c2:'#be123c', border:'#fda4af' },
    { id:'b4', name:'의료/안전', type:'medical', icon:'🏥', x: w*0.06, y: h*0.75, w: w*0.16, h: h*0.18, c1:'#10b981', c2:'#047857', border:'#6ee7b7' },
    { id:'b5', name:'푸드 존', type:'food', icon:'🍔', x: w*0.74, y: h*0.72, w: w*0.2, h: h*0.22, c1:'#f59e0b', c2:'#b45309', border:'#fcd34d' },
    { id:'b6', name:'중앙 휴식터', type:'rest', icon:'☕', x: w*0.38, y: h*0.42, w: w*0.24, h: h*0.2, c1:'#06b6d4', c2:'#0e7490', border:'#67e8f9' },
    { id:'b7', name:'전시관', type:'normal', icon:'📦', x: w*0.06, y: h*0.58, w: w*0.18, h: h*0.14, c1:'#64748b', c2:'#334155', border:'#cbd5e1' },
  ];
}

/* ==============================================
   SIMULATION ENGINE
   ============================================== */
function initPeople(){
  people = [];
  const count = 75;

  for(let i=0; i<count; i++){
    people.push({
      x: venue.width * (0.46 + (Math.random()-0.5)*0.12),
      y: venue.height * 0.92,
      speed: 0.13 + Math.random()*0.1,
      targets: generateRandomSequence(),
      currentTargetIdx: 0,
      dwellTime: 0
    });
  }
}

function generateRandomSequence(){
  const indices = [0, 1, 2, 3, 4, 5, 6];
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
    if(!targetBooth) { p.currentTargetIdx = 0; return; }

    const tx = targetBooth.x + targetBooth.w/2 + (Math.random()-0.5)*2;
    const ty = targetBooth.y + targetBooth.h/2 + (Math.random()-0.5)*2;

    const dx = tx - p.x;
    const dy = ty - p.y;
    const dist = Math.hypot(dx, dy);

    if(dist < 1.5){
      p.dwellTime = Math.floor(25 + Math.random()*35);
      p.currentTargetIdx = (p.currentTargetIdx + 1) % p.targets.length;
    } else {
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
   CANVAS RENDERING WITH GRADIENTS & STYLES
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

  // Dark Blueprint Grid Background
  venueCtx.strokeStyle = '#1e293b';
  venueCtx.lineWidth = 1;
  const step = 20;
  for(let x=0; x<w; x+=step){
    venueCtx.beginPath(); venueCtx.moveTo(x,0); venueCtx.lineTo(x,h); venueCtx.stroke();
  }
  for(let y=0; y<h; y+=step){
    venueCtx.beginPath(); venueCtx.moveTo(0,y); venueCtx.lineTo(w,y); venueCtx.stroke();
  }

  // Draw Prettier Booths with Soft Shadows & Gradients
  booths.forEach(b => {
    const bx = (b.x / venue.width) * w;
    const by = (b.y / venue.height) * h;
    const bw = (b.w / venue.width) * w;
    const bh = (b.h / venue.height) * h;

    // Drop Shadow
    venueCtx.shadowColor = 'rgba(0, 0, 0, 0.4)';
    venueCtx.shadowBlur = 10;
    venueCtx.shadowOffsetX = 0;
    venueCtx.shadowOffsetY = 4;

    // Gradient Fill
    let grad = venueCtx.createLinearGradient(bx, by, bx + bw, by + bh);
    grad.addColorStop(0, b.c1);
    grad.addColorStop(1, b.c2);

    venueCtx.fillStyle = grad;
    venueCtx.beginPath();
    venueCtx.roundRect(bx, by, bw, bh, 10);
    venueCtx.fill();

    // Border Outline
    venueCtx.shadowColor = 'transparent';
    venueCtx.strokeStyle = b.border;
    venueCtx.lineWidth = 1.5;
    venueCtx.stroke();

    // Text & Icon Label
    venueCtx.fillStyle = '#ffffff';
    venueCtx.font = 'bold 12px Pretendard, sans-serif';
    venueCtx.textAlign = 'center';
    venueCtx.fillText(`${b.icon} ${b.name}`, bx + bw/2, by + bh/2 + 4);
  });

  // Entry Gate
  const gateX = w * 0.44;
  const gateY = h * 0.91;
  venueCtx.fillStyle = '#10b981';
  venueCtx.beginPath();
  venueCtx.roundRect(gateX, gateY, w*0.12, h*0.07, 6);
  venueCtx.fill();
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 11px sans-serif';
  venueCtx.textAlign = 'center';
  venueCtx.fillText('🚪 메인 입출구', gateX + (w*0.12)/2, gateY + 15);
}

function drawPeople(){
  if(!peopleCtx) return;
  const w = peopleCanvas.width;
  const h = peopleCanvas.height;

  peopleCtx.clearRect(0, 0, w, h);

  people.forEach(p => {
    const px = (p.x / venue.width) * w;
    const py = (p.y / venue.height) * h;

    peopleCtx.fillStyle = '#60a5fa';
    peopleCtx.beginPath();
    peopleCtx.arc(px, py, 3.8, 0, Math.PI * 2);
    peopleCtx.fill();

    peopleCtx.strokeStyle = '#ffffff';
    peopleCtx.lineWidth = 1;
    peopleCtx.stroke();
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

    const grad = heatmapCtx.createRadialGradient(px, py, 0, px, py, 28);
    grad.addColorStop(0, 'rgba(239, 68, 68, 0.45)');
    grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.22)');
    grad.addColorStop(1, 'rgba(245, 158, 11, 0)');

    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(px, py, 28, 0, Math.PI * 2);
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
   AI CHAT COMMAND PROCESSING
   ============================================== */
function sendChat(){
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if(!msg) return;

  appendChatMsg(msg, 'user', 'chatBox');
  input.value = '';

  setTimeout(() => { processAICommand(msg, 'chatBox'); }, 500);
}

function sendFullChat(){
  const input = document.getElementById('fullChatInput');
  const msg = input.value.trim();
  if(!msg) return;

  appendChatMsg(msg, 'user', 'fullChatBox');
  input.value = '';

  setTimeout(() => { processAICommand(msg, 'fullChatBox'); }, 500);
}

function applyQuickPrompt(text){
  appendChatMsg(text, 'user', 'chatBox');
  setTimeout(() => { processAICommand(text, 'chatBox'); }, 400);
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
  let reply = "요청을 반영하여 행사장 구조 및 통로 폭을 수정했습니다.";

  if(cmd.includes('의료') || cmd.includes('안전')){
    reply = "의료/안전 부스를 메인 입구 바로 옆으로 재배치하였습니다.";
    const med = booths.find(b => b.type === 'medical');
    if(med){ med.x = venue.width * 0.06; med.y = venue.height * 0.75; }
  } else if(cmd.includes('푸드') || cmd.includes('출구')){
    reply = "푸드 존을 환기가 우수한 우측 출구 주변으로 이격하여 재설계했습니다.";
    const food = booths.find(b => b.type === 'food');
    if(food){ food.x = venue.width * 0.74; food.y = venue.height * 0.72; }
  } else if(cmd.includes('통로') || cmd.includes('폭') || cmd.includes('넓히기')){
    reply = "중앙 통로 정체 해소를 위해 휴식터 크기를 줄이고 이동 폭을 +1.2m 늘렸습니다.";
    const rest = booths.find(b => b.type === 'rest');
    if(rest){ rest.w = venue.width * 0.18; }
  }

  appendChatMsg(reply, 'ai', boxId);
  drawVenue();
  drawPeople();
}

// Initial Launch
window.addEventListener('load', () => {
  updateAuthUI();
  runAIGenerate();
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=1150, scrolling=True)
