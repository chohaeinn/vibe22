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
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<!-- Three.js Library for 3D View Engine -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color:#1e293b;
  background:#f8fafc;
  overflow-x:hidden;
}
button,input,select,textarea{font:inherit;}
button{cursor:pointer;transition:all 0.2s ease;}

/* Custom Scrollbar */
::-webkit-scrollbar {width:6px;height:6px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}
::-webkit-scrollbar-thumb:hover {background:#94a3b8;}

/* App Layout */
.app-container{
  display:flex;
  min-height:100vh;
  background:#f1f5f9;
}

/* Sidebar */
.sidebar{
  width:240px;
  background:#0f172a;
  color:#94a3b8;
  padding:20px 14px;
  display:flex;
  flex-direction:column;
  gap:20px;
  flex-shrink:0;
  border-right:1px solid #1e293b;
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
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:10px;
  display:grid;
  place-items:center;
  font-size:18px;
  font-weight:900;
  box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.brand-title{font-size:18px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;}
.brand-sub{font-size:10px;color:#64748b;margin-top:1px;font-weight:500;}

.nav-group{display:flex;flex-direction:column;gap:4px;}
.nav-item{
  display:flex;
  align-items:center;
  gap:10px;
  padding:11px 14px;
  border-radius:10px;
  font-size:13.5px;
  font-weight:600;
  color:#94a3b8;
  cursor:pointer;
}
.nav-item:hover{background:rgba(255,255,255,0.05);color:#f1f5f9;}
.nav-item.active{
  background:linear-gradient(135deg, #2563eb, #3b82f6);
  color:#ffffff;
  box-shadow:0 4px 12px rgba(37,99,235,0.3);
}
.nav-icon{font-size:15px;width:18px;text-align:center;}

.side-profile{
  margin-top:auto;
  background:#1e293b;
  border-radius:12px;
  padding:12px;
  display:flex;
  align-items:center;
  gap:10px;
}
.side-avatar{
  width:32px;
  height:32px;
  background:#3b82f6;
  border-radius:50%;
  color:#fff;
  display:grid;
  place-items:center;
  font-weight:700;
  font-size:12px;
}
.side-user-info{flex:1;}
.side-user-name{font-size:12px;font-weight:700;color:#f8fafc;}
.side-user-btn{font-size:10px;color:#94a3b8;background:none;border:none;padding:0;margin-top:2px;cursor:pointer;}

.side-banner{
  background:linear-gradient(135deg, rgba(37,99,235,0.2), rgba(15,23,42,0.8));
  border:1px solid rgba(59,130,246,0.25);
  padding:14px;
  border-radius:12px;
  color:#e2e8f0;
}
.side-banner h5{font-size:12px;font-weight:800;color:#60a5fa;margin-bottom:4px;}
.side-banner p{font-size:10.5px;color:#94a3b8;line-height:1.4;}

/* Main Area */
.main-content{
  flex:1;
  padding:20px;
  display:flex;
  flex-direction:column;
  gap:16px;
  min-width:0;
  overflow-y:auto;
}

/* Header */
.top-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  background:#ffffff;
  padding:14px 20px;
  border-radius:16px;
  border:1px solid #e2e8f0;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
}
.top-title h2{font-size:20px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:8px;}
.top-title p{font-size:12px;color:#64748b;margin-top:2px;}

/* Page Views */
.page-view{display:none;}
.page-view.active{display:block;}

/* Form Card */
.form-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:24px;
  box-shadow:0 2px 10px rgba(0,0,0,0.02);
}
.form-section-head{
  font-size:16px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:18px;
  display:flex;
  align-items:center;
  gap:8px;
}
.form-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(210px, 1fr));
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
  font-weight:700;
  color:#334155;
  display:flex;
  align-items:center;
  gap:4px;
}
.form-group input, .form-group select, .form-group textarea{
  padding:10px 12px;
  border:1.5px solid #cbd5e1;
  border-radius:10px;
  background:#f8fafc;
  color:#0f172a;
  font-size:13px;
  font-weight:600;
  outline:none;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus{
  border-color:#2563eb;
  background:#ffffff;
  box-shadow:0 0 0 3px rgba(37,99,235,0.1);
}

.btn-primary{
  background:linear-gradient(135deg, #2563eb, #1d4ed8);
  color:#ffffff;
  border:none;
  padding:12px 24px;
  border-radius:12px;
  font-weight:800;
  font-size:13.5px;
  box-shadow:0 4px 14px rgba(37,99,235,0.3);
  display:inline-flex;
  align-items:center;
  gap:8px;
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(37,99,235,0.4);}

.btn-secondary{
  background:#f1f5f9;
  color:#334155;
  border:1px solid #cbd5e1;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
  display:inline-flex;
  align-items:center;
  gap:4px;
}
.btn-secondary:hover{background:#e2e8f0;}

.btn-warning{
  background:#fef3c7;
  color:#b45309;
  border:1px solid #fde68a;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
}
.btn-warning.active{background:#f59e0b;color:#fff;border-color:#d97706;}

.btn-danger{
  background:#fee2e2;
  color:#b91c1c;
  border:1px solid #fca5a5;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
}
.btn-danger.active{background:#ef4444;color:#fff;border-color:#dc2626;animation:pulse 1s infinite;}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

/* Info Strip */
.info-strip{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:12px;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
}
.info-strip-group{
  display:flex;
  align-items:center;
  gap:16px;
  flex-wrap:wrap;
}
.info-box{
  display:flex;
  align-items:center;
  gap:8px;
  padding-right:12px;
  border-right:1px solid #f1f5f9;
}
.info-box:last-child{border-right:none;}
.info-box-icon{
  width:32px;
  height:32px;
  border-radius:8px;
  background:#eff6ff;
  color:#2563eb;
  display:grid;
  place-items:center;
  font-size:14px;
}
.info-box-text label{display:block;font-size:10px;color:#64748b;font-weight:700;}
.info-box-text span{font-size:12.5px;font-weight:800;color:#0f172a;}

/* Main Dashboard Grids (Adjusted since AI evaluation card is removed) */
.dashboard-main-grid{
  display:grid;
  grid-template-columns: 1.6fr 1fr;
  gap:16px;
}
.dashboard-bottom-grid{
  display:grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap:16px;
}

/* Cards */
.card-panel{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:16px;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
  display:flex;
  flex-direction:column;
}
.card-head{
  font-size:14px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:12px;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.card-badge{
  font-size:10.5px;
  background:#eff6ff;
  color:#2563eb;
  padding:3px 8px;
  border-radius:12px;
  font-weight:700;
}

/* Canvas Wrap */
.map-wrap{
  position:relative;
  width:100%;
  height:380px;
  background:#1e293b;
  border-radius:12px;
  overflow:hidden;
  border:1px solid #334155;
}
#venueCanvas, #heatmapCanvas, #peopleCanvas, #container3D{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
}
#heatmapCanvas{z-index:5;opacity:0.9;pointer-events:none;}
#peopleCanvas{z-index:10;pointer-events:none;}
#container3D{z-index:15;display:none;background:#0f172a;}

/* Map Overlay Legend */
.map-legend-overlay{
  position:absolute;
  left:10px;
  bottom:10px;
  z-index:20;
  background:rgba(255,255,255,0.92);
  backdrop-filter:blur(6px);
  padding:8px 12px;
  border-radius:10px;
  font-size:10.5px;
  border:1px solid #e2e8f0;
  box-shadow:0 4px 12px rgba(0,0,0,0.1);
  display:grid;
  grid-template-columns:repeat(2, 1fr);
  gap:4px 10px;
}
.legend-item{display:flex;align-items:center;gap:5px;font-weight:700;color:#334155;}
.legend-dot{width:8px;height:8px;border-radius:2px;}

/* Controls Bar above/below Map */
.map-controls-bar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top:10px;
  gap:8px;
  flex-wrap:wrap;
}

/* Timeline Controls */
.timeline-container{
  background:#f8fafc;
  border:1px solid #e2e8f0;
  border-radius:12px;
  padding:10px 14px;
  margin-bottom:12px;
  display:flex;
  align-items:center;
  gap:12px;
}
.timeline-slider{
  flex:1;
  accent-color:#2563eb;
  cursor:pointer;
}
.time-badge{
  background:#2563eb;
  color:#fff;
  font-weight:800;
  font-size:12px;
  padding:4px 10px;
  border-radius:20px;
  min-width:70px;
  text-align:center;
}

/* History Toolbar */
.history-bar{
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 12px;
  border-radius:10px;
  margin-bottom:12px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  font-size:12px;
}
.history-select{
  padding:4px 8px;
  border:1px solid #cbd5e1;
  border-radius:6px;
  font-size:11.5px;
  font-weight:700;
  background:#fff;
  color:#0f172a;
}

/* Compare Box */
.compare-grid{
  display:grid;
  grid-template-columns:1fr 20px 1fr;
  align-items:center;
  gap:8px;
  background:#f8fafc;
  padding:12px;
  border-radius:12px;
  border:1px solid #e2e8f0;
}
.comp-col h5{font-size:11px;color:#64748b;margin-bottom:6px;font-weight:700;}
.comp-val{display:flex;justify-content:space-between;font-size:11.5px;font-weight:700;margin-bottom:4px;}
.text-red{color:#ef4444;}
.text-green{color:#10b981;}

/* Main Dashboard Inline AI Assistant Box */
.main-ai-assistant{
  background:linear-gradient(135deg, #f8fafc, #eff6ff);
  border:1.5px solid #bfdbfe;
  border-radius:16px;
  padding:16px;
  margin-bottom:16px;
  box-shadow:0 2px 8px rgba(37,99,235,0.05);
}
.main-ai-header{
  display:flex;
  align-items:center;
  gap:8px;
  font-size:14px;
  font-weight:800;
  color:#1e3a8a;
  margin-bottom:10px;
}
.main-ai-chatbox{
  background:#ffffff;
  border:1px solid #cbd5e1;
  border-radius:10px;
  padding:10px 12px;
  height:100px;
  overflow-y:auto;
  font-size:12px;
  margin-bottom:10px;
  display:flex;
  flex-direction:column;
  gap:6px;
}
.chat-msg-ai{
  background:#eff6ff;
  color:#1e40af;
  padding:6px 10px;
  border-radius:8px;
  align-self:flex-start;
  max-width:85%;
  line-height:1.4;
}
.chat-msg-user{
  background:#2563eb;
  color:#ffffff;
  padding:6px 10px;
  border-radius:8px;
  align-self:flex-end;
  max-width:85%;
  line-height:1.4;
}
.main-ai-inputgroup{
  display:flex;
  gap:8px;
}
.main-ai-inputgroup input{
  flex:1;
  padding:8px 12px;
  border:1px solid #cbd5e1;
  border-radius:8px;
  font-size:12px;
  outline:none;
}
.main-ai-inputgroup input:focus{
  border-color:#2563eb;
  box-shadow:0 0 0 2px rgba(37,99,235,0.15);
}

/* Workflow Steps */
.wf-container{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:4px;
  margin-top:6px;
}
.wf-card{
  flex:1;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 4px;
  border-radius:8px;
  text-align:center;
}
.wf-card .wf-icon{font-size:14px;margin-bottom:2px;}
.wf-card .wf-title{font-size:10px;font-weight:800;color:#1e293b;}
.wf-arrow{color:#cbd5e1;font-weight:900;font-size:11px;}

.wf-sub-tags{
  display:flex;
  justify-content:space-between;
  gap:4px;
  margin-top:8px;
}
.wf-tag{
  flex:1;
  background:#eff6ff;
  color:#2563eb;
  font-size:9.5px;
  font-weight:700;
  text-align:center;
  padding:4px 2px;
  border-radius:6px;
}

/* Report Summary Panel */
.report-sum-box{
  background:#eff6ff;
  border:1px solid #bfdbfe;
  border-radius:10px;
  padding:10px;
  font-size:11.5px;
  color:#1e3a8a;
  line-height:1.4;
  margin-bottom:10px;
}

/* Modals */
.modal-bg{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,0.65);
  backdrop-filter:blur(5px);
  z-index:999;
  display:none;
  place-items:center;
  padding:20px;
}
.modal-bg.active{display:grid;}
.modal-content{
  background:#ffffff;
  width:min(95%, 880px);
  max-height:85vh;
  border-radius:20px;
  padding:28px;
  box-shadow:0 20px 40px rgba(0,0,0,0.2);
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.modal-body{flex:1;overflow-y:auto;padding-right:6px;display:flex;flex-direction:column;gap:18px;}
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
        <div class="brand-sub">AI 기반 행사 설계·분석 시스템</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item active" onclick="switchPage('design', this)">
        <span class="nav-icon">📋</span> 행사 설계 메인 (대시보드)
      </div>
      <div class="nav-item" onclick="switchPage('home', this)">
        <span class="nav-icon">🏠</span> 조건 입력 설정
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span class="nav-icon">⚙️</span> 설계 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span class="nav-icon">📊</span> 비전 설계 리포트
      </div>
    </nav>

    <div class="side-banner">
      <h5>AI 지도 생성기</h5>
      <p>AI가 만든 지도, 더 빠르고 효율적인 행사 운영을 지원합니다.</p>
    </div>

    <div class="side-profile">
      <div class="side-avatar">추</div>
      <div class="side-user-info">
        <div class="side-user-name" id="sideUserName">추천님</div>
        <button class="side-user-btn" onclick="openAuthModal()">로그아웃</button>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">

    <!-- Top Header -->
    <header class="top-header">
      <div class="top-title">
        <h2 id="topTitleText">📋 행사 설계 메인</h2>
        <p id="topSubText">실시간 AI 지능형 행사장 최적화 및 동선 분석 시스템입니다.</p>
      </div>
      <button class="btn-primary" onclick="runAIGenerate()">
        ✦ AI 재배치 실행하기
      </button>
    </header>

    <!-- PAGE 1: HOME / FORM -->
    <section id="pageHome" class="page-view">
      <div class="form-card">
        <div class="form-section-head">📝 행사 기본 정보 및 상세 요구사항 설정</div>
        <div class="form-grid">
          <div class="form-group">
            <label>📌 행사명</label>
            <input type="text" id="inEventName" value="2025 힐링 페스티벌">
          </div>
          <div class="form-group">
            <label>🏞️ 행사장 유형</label>
            <select id="inVenueType">
              <option value="야외" selected>야외 잔디 광장</option>
              <option value="실내 컨벤션">실내 컨벤션 홀</option>
              <option value="체육관">실내 체육관</option>
              <option value="도심 거리">도심 스트리트/광장</option>
            </select>
          </div>
          <div class="form-group">
            <label>📍 행사장 위치</label>
            <input type="text" id="inLocation" value="야외 종합 운동장 & 잔디 광장">
          </div>
          <div class="form-group">
            <label>👥 예상 관람객 수</label>
            <select id="inVisitors">
              <option value="1,000명">1,000명</option>
              <option value="3,000명">3,000명</option>
              <option value="5,000명" selected>5,000명</option>
              <option value="10,000명">10,000명 이상</option>
            </select>
          </div>
          <div class="form-group">
            <label>📐 행사장 면적</label>
            <input type="text" id="inArea" value="50,000m²">
          </div>
          <div class="form-group">
            <label>⏰ 운영 시간</label>
            <input type="text" id="inTime" value="10시 - 20시">
          </div>
          <div class="form-group">
            <label>🎯 주 타겟 연령대</label>
            <select id="inTargetAge">
              <option value="올댓/전 연령층" selected>올댓 / 전 연령층</option>
              <option value="10~20대 청소년">10~20대 청소년 및 대학생</option>
              <option value="30~40대 가족">30~40대 가족 단위</option>
              <option value="50대 이상">50대 이상 시니어</option>
            </select>
          </div>
          <div class="form-group">
            <label>🎪 행사 성격 / 컨셉</label>
            <select id="inCategory">
              <option value="휴식/힐링" selected>휴식 & 힐링 페스티벌</option>
              <option value="학술/박람회">학술 & 산업 박람회</option>
              <option value="음악/공연">음악 & 대형 공연</option>
              <option value="플리마켓/체험">체험 & 플리마켓</option>
            </select>
          </div>
          <div class="form-group">
            <label>🎫 입장료 정책</label>
            <input type="text" id="inTicket" value="무료">
          </div>
          <div class="form-group">
            <label>💰 예산 규모</label>
            <input type="text" id="inBudget" value="5,000만원">
          </div>
          <div class="form-group">
            <label>🚪 출입구 / 비상구 수</label>
            <select id="inGates">
              <option value="2개 (주출입구+비상구)">2개 (주출입구 + 비상구)</option>
              <option value="4개 (동서남북)" selected>4개 (동서남북 사방 출입)</option>
              <option value="6개 이상">6개 이상 (대형 관람객용)</option>
            </select>
          </div>
          <div class="form-group">
            <label>🏥 필수 안전/의료 구역</label>
            <select id="inSafetyReq">
              <option value="입구 근처 전진배치" selected>입구 근처 전진 배치 (골든타임 확보)</option>
              <option value="중앙 분산 배치">중앙 분산 배치</option>
              <option value="음향/무대 주변">무대 및 메인 관람구역 집중</option>
            </select>
          </div>
          <div class="form-group" style="grid-column:1 / -1;">
            <label>💬 AI 공간 배치 세부 프롬프트 / 요구사항</label>
            <textarea id="inPrompt" rows="3">메인 무대는 중앙 상단에 배치하고, Central Lawn(잔디 휴식존) 주변으로 푸드트럭과 체험 부스를 원형으로 둘러싸 배치해주세요. 응급 의료센터는 접근성이 좋은 위치에 배치하여 비상시 이송을 최적화하세요.</textarea>
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn-primary" onclick="runAIGenerate()">
            ✦ 입력 정보 기반 AI 설계 생성
          </button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: DESIGN DASHBOARD (MAIN PAGE - DEFAULT ON LOAD) -->
    <section id="pageDesign" class="page-view active">

      <!-- MAIN PAGE INLINE AI ASSISTANT PANEL -->
      <div class="main-ai-assistant">
        <div class="main-ai-header">
          <span>🤖 AI 메인 어시스턴트 (실시간 레이아웃 제어)</span>
          <span style="font-size:11px;color:#3b82f6;font-weight:600;">— 실시간 명령어를 통해 배치도를 즉시 재구성할 수 있습니다.</span>
        </div>
        <div class="main-ai-chatbox" id="mainAiChatBox">
          <div class="chat-msg-ai">
            안녕하세요 추천님! 원하시는 배치 수정 사항이나 추가 설비를 말씀해 주시면 즉시 반영하여 새로운 최적안을 설계합니다.
          </div>
        </div>
        <div class="main-ai-inputgroup">
          <input type="text" id="mainAiInput" placeholder="예: 무대를 우측으로 옮기고 응급 부스를 중앙 통로 근처로 배치해줘" onkeypress="if(event.key==='Enter') sendMainAiMsg()">
          <button class="btn-primary" style="padding:8px 16px;font-size:12px;" onclick="sendMainAiMsg()">보내기</button>
        </div>
      </div>

      <!-- History Bar -->
      <div class="history-bar">
        <div style="display:flex;align-items:center;gap:8px;">
          <span>📜 <b>설계 히스토리 (기록):</b></span>
          <select id="historySelect" class="history-select" onchange="loadSelectedHistory(this.value)">
            <!-- Dynamic Options -->
          </select>
        </div>
        <span id="historyStatusBadge" style="font-size:11px;color:#2563eb;font-weight:700;">현재 버전: v1 (기본 설계안)</span>
      </div>

      <!-- Time-based Simulation Controller -->
      <div class="timeline-container">
        <span style="font-size:12px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:4px;">
          ⏰ <b>시간별 관람객 시뮬레이션:</b>
        </span>
        <button class="btn-secondary" id="btnTimelinePlay" onclick="toggleTimelinePlay()">▶ 시간 재생</button>
        <input type="range" id="timeSlider" class="timeline-slider" min="10" max="20" step="1" value="14" oninput="updateTimeSimulation(this.value)">
        <div class="time-badge" id="timeDisplay">14:00</div>
        <span style="font-size:11px;color:#64748b;font-weight:600;" id="timeDesc">관람 인원 피크 타임 (공연 및 체험)</span>
      </div>

      <!-- Top Header Strip -->
      <div class="info-strip">
        <div class="info-strip-group">
          <div class="info-box">
            <div class="info-box-icon">📌</div>
            <div class="info-box-text"><label>행사명</label><span id="outEventName">2025 힐링 페스티벌</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🏞️</div>
            <div class="info-box-text"><label>행사장 유형</label><span id="outVenueType">야외</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">📍</div>
            <div class="info-box-text"><label>행사장 위치</label><span id="outLocation">야외 종합 운동장 & 잔디 광장</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">👥</div>
            <div class="info-box-text"><label>예상 관람객</label><span id="outVisitors">5,000명</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">📐</div>
            <div class="info-box-text"><label>행사장 면적</label><span id="outArea">50,000m²</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">⏰</div>
            <div class="info-box-text"><label>운영 시간</label><span id="outTime">10시 - 20시</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🎯</div>
            <div class="info-box-text"><label>관람객 연령대</label><span id="outAge">올댓 / 전 연령층</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🎪</div>
            <div class="info-box-text"><label>행사 성격</label><span id="outCategory">휴식</span></div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Grid (2 columns: 1.6fr venue map, 1fr heatmap) - AI score card removed -->
      <div class="dashboard-main-grid" style="margin-top:14px;">

        <!-- 1. Digital Twin Canvas Map (2D & 3D Supported with Detailed Venue Rendering) -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 행사장 구체화 배치도 (디지털 트윈)</span>
            <div style="display:flex;gap:6px;align-items:center;">
              <button class="btn-secondary" id="btnToggle3D" onclick="toggle3DView()">🧊 3D 입체뷰 보기</button>
              <span class="card-badge" id="layoutBadge">v1.0 AI 설계</span>
            </div>
          </div>

          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>
            <div id="container3D"></div>

            <!-- Legend -->
            <div class="map-legend-overlay">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 메인무대/객석</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 푸드트럭존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 잔디휴식광장</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 응급의료센터</div>
              <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> 화장실/편의</div>
            </div>
          </div>

          <div class="map-controls-bar">
            <div style="display:flex;gap:6px;">
              <button class="btn-secondary" id="btnToggleSim" onclick="toggleSim()">
                ▶ 시뮬레이션 시작
              </button>
              <button class="btn-warning" id="btnRain" onclick="toggleRainEnv()">
                🌧️ 우천 모드
              </button>
              <button class="btn-danger" id="btnEmergency" onclick="triggerEmergencyEnv()">
                🚨 응급환자 발생 (최단 후송)
              </button>
            </div>
            <span style="font-size:11px;color:#64748b;font-weight:700;" id="simTimer">상태: 대기중</span>
          </div>
        </div>

        <!-- 2. Detailed Heatmap Card -->
        <div class="card-panel">
          <div class="card-head">
            <span>🔥 실시간 유동인구 군중 밀집도 Heatmap</span>
            <span class="card-badge" id="envBadge">실시간 동기화</span>
          </div>
          <div class="map-wrap">
            <canvas id="heatmapCanvas"></canvas>
          </div>
          <div style="display:flex;justify-content:space-around;font-size:10px;color:#64748b;margin-top:10px;font-weight:700;">
            <span style="color:#10b981;">🟢 여유 (0~10명)</span>
            <span style="color:#eab308;">🟡 보통 (11~25명)</span>
            <span style="color:#f97316;">🟠 혼잡 (26~45명)</span>
            <span style="color:#ef4444;">🔴 고위험/병목 (46명+)</span>
          </div>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-bottom-grid" style="margin-top:14px;">

        <!-- 1. Before / After Comparison -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚖️ 설계 전 / 후 비교 검증</span>
          </div>
          <div class="compare-grid">
            <div class="comp-col">
              <h5>AI 설계 전 (기존)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-red" id="compBeforeBottleneck">68%</span></div>
              <div class="comp-val"><span>응급 이송시간</span><span id="compBeforeAccess">4분 30초</span></div>
              <div class="comp-val"><span>사고 위험구역</span><span class="text-red" id="compBeforeRisk">3개소</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#cbd5e1;">→</div>
            <div class="comp-col">
              <h5>AI 설계 후 (최적화)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-green" id="compAfterBottleneck">18%</span></div>
              <div class="comp-val"><span>응급 이송시간</span><span class="text-green" id="compAfterAccess">1분 15초</span></div>
              <div class="comp-val"><span>사고 위험구역</span><span class="text-green" id="compAfterRisk">0개소</span></div>
            </div>
          </div>
        </div>

        <!-- 2. AI Workflow Process -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚙️ AI 행사 설계 프로세스 (Workflow)</span>
          </div>
          <div class="wf-container">
            <div class="wf-card"><div class="wf-icon">📋</div><div class="wf-title">정보 입력</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🌐</div><div class="wf-title">2D/3D 트윈</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🤖</div><div class="wf-title">시간별 시뮬</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🚑</div><div class="wf-title">응급 최단경로</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">📄</div><div class="wf-title">리포트</div></div>
          </div>
          <div class="wf-sub-tags">
            <span class="wf-tag">조건 설정</span>
            <span class="wf-tag">입체 시각화</span>
            <span class="wf-tag">군중 흐름</span>
            <span class="wf-tag">골든타임 사수</span>
          </div>
        </div>

        <!-- 3. Report Summary -->
        <div class="card-panel">
          <div class="card-head">
            <span>📄 분석 리포트 요약</span>
          </div>
          <div class="report-sum-box" id="reportSummaryBox">
            AI 분석 결과, <b>2025 힐링 페스티벌</b>은 구체화된 구역 설계와 정교한 군중 시뮬레이션을 통해 모든 시간대에 걸쳐 완벽한 안전성과 최적의 동선을 제공합니다.
          </div>
          <button class="btn-primary" style="width:100%;justify-content:center;padding:10px;font-size:12px;margin-top:auto;" onclick="openReportModal()">
            📌 상세 종합 보고서 출력 (PDF)
          </button>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS -->
    <section id="pageProcess" class="page-view">
      <div class="form-card">
        <div class="form-section-head">⚙️ AI 행사 공간 설계 및 실시간 시뮬레이션 메커니즘</div>
        <p style="font-size:13px;line-height:1.7;color:#334155;">
          1. <b>구체화된 행사장 레이아웃:</b> 메인 무대와 스탠드 객석, 원형 잔디 휴식 광장, 외곽 푸드트럭 구역 및 응급 의료센터를 정밀하게 배치합니다.<br>
          2. <b>정교한 군중 시뮬레이션 및 히트맵:</b> 시간에 따른 유동 인구 변화를 입자 물리 엔진 기반으로 연산하여 밀집도를 고해상도 히트맵으로 시각화합니다.<br>
          3. <b>동적 응급 후송 경로 (Dynamic Pathfinding):</b> 응급 상황 발생 시 부스 위치에 관계없이 최단 의료 후송로를 실시간으로 탐색합니다.<br>
          4. <b>Three.js 기반 3D 입체 뷰:</b> 평면 설계를 넘어 3D 공간 상에서 조망과 시설물 간섭 여부를 즉시 검증할 수 있습니다.
        </p>
      </div>
    </section>

  </main>
</div>

<!-- DETAILED PDF REPORT MODAL -->
<div class="modal-bg" id="reportModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #f1f5f9;margin-bottom:16px;">
      <h3 style="font-size:18px;font-weight:800;color:#0f172a;">📊 AI 행사장 구체화 설계 및 동선 분석 종합 보고서</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:20px;font-weight:800;color:#64748b;">✕</button>
    </div>

    <div class="modal-body">
      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">1. 종합 개요</h4>
        <p style="font-size:12.5px;color:#334155;line-height:1.6;">
          본 보고서는 <b>2025 힐링 페스티벌</b> (야외 잔디 광장 50,000m², 예상 관람객 5,000명)의 구체화된 구역 배치와 실시간 시뮬레이션 검증 결과를 담고 있습니다.
        </p>
      </div>

      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">2. 구역별 상세 설계 및 히트맵 분석 결과</h4>
        <ul style="font-size:12px;color:#334155;line-height:1.7;padding-left:18px;">
          <li><b>메인 무대 & 객석:</b> 북측 상단에 넓은 관람 스탠드를 확보하여 대규모 인원 집중 시 분산 유도.</li>
          <li><b>푸드트럭 & 체험존:</b> 중앙 잔디 휴식 광장을 중심으로 원형 외곽 루프형 배치를 통해 병목 현상 최소화.</li>
          <li><b>응급 의료센터:</b> 중앙 접근성 극대화 및 비상 앰뷸런스 전용 진출입로 연계.</li>
        </ul>
      </div>

      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">3. 비상 대피 및 골든타임 사수 검증</h4>
        <p style="font-size:12px;color:#334155;line-height:1.6;">
          응급 환자 발생 시 실시간 최단 후송 경로 알고리즘을 통해 이송 시간이 평균 <b>1분 15초</b>로 단축되며, 비상시 전원 대피 골든타임(2분 이내)이 완벽히 검증되었습니다.
        </p>
      </div>
    </div>

    <div style="margin-top:16px;display:flex;justify-content:flex-end;gap:10px;">
      <button style="padding:10px 16px;background:#e2e8f0;border:none;border-radius:8px;font-weight:700;font-size:12px;" onclick="closeReportModal()">닫기</button>
      <button class="btn-primary" onclick="alert('보고서가 PDF 파일로 출력되었습니다.');closeReportModal();">PDF 다운로드</button>
    </div>
  </div>
</div>

<script>
/* Navigation Switching (Default to Design Dashboard on Load) */
function switchPage(pageId, el){
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  if(el) {
    el.classList.add('active');
  } else {
    const navItems = document.querySelectorAll('.nav-item');
    if(pageId === 'design' && navItems[0]) navItems[0].classList.add('active');
    if(pageId === 'home' && navItems[1]) navItems[1].classList.add('active');
    if(pageId === 'process' && navItems[2]) navItems[2].classList.add('active');
  }

  const t = document.getElementById('topTitleText');
  const s = document.getElementById('topSubText');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
    t.textContent = '📝 행사 조건 입력';
    s.textContent = '상세 기본 정보 및 요구사항을 입력하시면 AI가 자동 설계합니다.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    t.textContent = '📋 행사 설계 메인';
    s.textContent = '실시간 AI 지능형 행사장 최적화 및 동선 분석 시스템입니다.';
    setTimeout(initCanvases, 50);
  } else if(pageId === 'process'){
    document.getElementById('pageProcess').classList.add('active');
    t.textContent = '⚙️ 설계 프로세스';
    s.textContent = 'AI 시간별 분석, 3D 입체 시뮬레이션 및 응급 경로 추적 메커니즘입니다.';
  }
}

function openReportModal(){ document.getElementById('reportModal').classList.add('active'); }
function closeReportModal(){ document.getElementById('reportModal').classList.remove('active'); }
function openAuthModal(){ alert('로그아웃 되었습니다.'); }

/* APP STATE & BLUEPRINT HISTORY SYSTEM */
let layoutHistory = [];
let currentLayoutIndex = -1;

const layoutPresets = [
  {
    versionName: "v1.0 - 구체화된 기본 최적안",
    timestamp: "기본",
    booths: {
      stage: {x: 0.35, y: 0.06, bw: 0.30, bh: 0.18, title: '메인 무대 & 객석', color: '#8b5cf6', icon: '🎭'},
      expA: {x: 0.10, y: 0.28, bw: 0.18, bh: 0.14, title: '체험존 A', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.72, y: 0.28, bw: 0.18, bh: 0.14, title: '체험존 B', color: '#3b82f6', icon: '🚀'},
      food: {x: 0.10, y: 0.52, bw: 0.18, bh: 0.15, title: '푸드트럭 구역', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.72, y: 0.52, bw: 0.18, bh: 0.14, title: '응급 의료센터', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.72, y: 0.72, bw: 0.16, bh: 0.12, title: '화장실 / 편의', color: '#06b6d4', icon: '🚻'}
    }
  },
  {
    versionName: "v2.0 - 응급 의료센터 중앙 전진안",
    timestamp: "AI 추천",
    booths: {
      stage: {x: 0.35, y: 0.06, bw: 0.30, bh: 0.18, title: '메인 무대 & 객석', color: '#8b5cf6', icon: '🎪'},
      expA: {x: 0.08, y: 0.28, bw: 0.20, bh: 0.14, title: '체험존 A', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.72, y: 0.28, bw: 0.20, bh: 0.14, title: '체험존 B', color: '#3b82f6', icon: '🚀'},
      food: {x: 0.08, y: 0.55, bw: 0.20, bh: 0.15, title: '푸드트럭 구역', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.42, y: 0.52, bw: 0.16, bh: 0.14, title: '응급 의료센터 (중앙)', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.75, y: 0.72, bw: 0.16, bh: 0.12, title: '화장실', color: '#06b6d4', icon: '🚻'}
    }
  },
  {
    versionName: "v3.0 - 우측 무대 특화안",
    timestamp: "AI 추천",
    booths: {
      stage: {x: 0.62, y: 0.08, bw: 0.30, bh: 0.18, title: '메인 무대 (우측)', color: '#8b5cf6', icon: '🎭'},
      expA: {x: 0.08, y: 0.22, bw: 0.20, bh: 0.14, title: '체험존 A', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.35, y: 0.22, bw: 0.20, bh: 0.14, title: '체험존 B', color: '#3b82f6', icon: '🚀'},
      food: {x: 0.08, y: 0.52, bw: 0.20, bh: 0.15, title: '푸드트럭 구역', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.40, y: 0.72, bw: 0.18, bh: 0.14, title: '응급 의료센터 (하단)', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.75, y: 0.72, bw: 0.16, bh: 0.12, title: '화장실', color: '#06b6d4', icon: '🚻'}
    }
  }
];

function initLayoutHistory() {
  if (layoutHistory.length === 0) {
    layoutHistory.push(JSON.parse(JSON.stringify(layoutPresets[0])));
    currentLayoutIndex = 0;
    updateHistorySelectUI();
  }
}

function updateHistorySelectUI() {
  const sel = document.getElementById('historySelect');
  if(!sel) return;
  sel.innerHTML = '';
  layoutHistory.forEach((ly, idx) => {
    const opt = document.createElement('option');
    opt.value = idx;
    opt.textContent = `${ly.versionName} (${ly.timestamp})`;
    if (idx === currentLayoutIndex) opt.selected = true;
    sel.appendChild(opt);
  });
  document.getElementById('historyStatusBadge').textContent = `현재 버전: ${layoutHistory[currentLayoutIndex].versionName}`;
}

function loadSelectedHistory(index) {
  currentLayoutIndex = parseInt(index);
  const layout = layoutHistory[currentLayoutIndex];

  document.getElementById('layoutBadge').textContent = layout.versionName;
  document.getElementById('historyStatusBadge').textContent = `현재 버전: ${layout.versionName}`;

  if (venueCanvas) {
    drawDetailedOutdoorVenue(venueCanvas.width, venueCanvas.height);
  }
  if (is3DActive) {
    update3DScene();
  }
}

function runAIGenerate(customTitle){
  initLayoutHistory();

  const nextPresetIndex = layoutHistory.length % layoutPresets.length;
  const newLayout = JSON.parse(JSON.stringify(layoutPresets[nextPresetIndex]));

  const d = new Date();
  const timeStr = `${d.getHours()}:${d.getMinutes() < 10 ? '0' : ''}${d.getMinutes()}:${d.getSeconds() < 10 ? '0' : ''}${d.getSeconds()}`;
  newLayout.versionName = customTitle || `v${layoutHistory.length + 1}.0 - AI 최적화 재배치안`;
  newLayout.timestamp = timeStr;

  layoutHistory.push(newLayout);
  currentLayoutIndex = layoutHistory.length - 1;

  updateHistorySelectUI();
  loadSelectedHistory(currentLayoutIndex);
}

/* MAIN PAGE AI CHAT ASSISTANT */
function sendMainAiMsg(){
  const input = document.getElementById('mainAiInput');
  const txt = input.value.trim();
  if(!txt) return;

  const chatBox = document.getElementById('mainAiChatBox');
  chatBox.innerHTML += `<div class="chat-msg-user"><b>나:</b> ${txt}</div>`;
  input.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  setTimeout(() => {
    chatBox.innerHTML += `<div class="chat-msg-ai"><b>AI:</b> 요청하신 "${txt}" 조건을 반영하여 행사장 구성을 정밀 재배치했습니다. 시뮬레이션 및 응급 후송 동선이 즉시 동기화되었습니다.</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
    runAIGenerate(`v${layoutHistory.length + 1}.0 - 사용자 맞춤 재배치`);
  }, 600);
}

/* TIME-BASED REALISTIC SIMULATION SYSTEM */
let timeInterval = null;
let currentTime = 14;

function updateTimeSimulation(timeVal) {
  currentTime = parseInt(timeVal);
  document.getElementById('timeDisplay').textContent = `${currentTime}:00`;

  const desc = document.getElementById('timeDesc');
  if (currentTime >= 10 && currentTime < 12) {
    desc.textContent = '개장 및 입장 시간대 - 관람객 순차 유입 (여유)';
    setCrowdDensityFactor(0.6);
  } else if (currentTime >= 12 && currentTime < 15) {
    desc.textContent = '점심 및 피크 타임 - 푸드트럭 및 메인 무대 집중 (혼잡)';
    setCrowdDensityFactor(1.6);
  } else if (currentTime >= 15 && currentTime < 18) {
    desc.textContent = '오후 프로그램 시간 - 체험존 및 잔디광장 고른 분산';
    setCrowdDensityFactor(1.1);
  } else {
    desc.textContent = '야간 폐장 전 - 메인 무대 집중 및 출구 이동';
    setCrowdDensityFactor(1.3);
  }
}

function setCrowdDensityFactor(factor) {
  if(!venueCanvas) return;
  const targetCount = Math.floor(80 * factor);
  const w = venueCanvas.width;
  const h = venueCanvas.height;
  if (people.length < targetCount) {
    for(let i = people.length; i < targetCount; i++){
      people.push({
        x: w*0.15 + Math.random()*w*0.7,
        y: h*0.2 + Math.random()*h*0.6,
        vx: (Math.random()-0.5)*1.4,
        vy: (Math.random()-0.5)*1.4,
        targetX: Math.random()*w,
        targetY: Math.random()*h,
        speed: 0.7 + Math.random()*0.8
      });
    }
  } else if (people.length > targetCount) {
    people = people.slice(0, targetCount);
  }
}

function toggleTimelinePlay() {
  const btn = document.getElementById('btnTimelinePlay');
  if (timeInterval) {
    clearInterval(timeInterval);
    timeInterval = null;
    btn.textContent = '▶ 시간 재생';
  } else {
    btn.textContent = '⏸ 일시정지';
    timeInterval = setInterval(() => {
      let nextTime = currentTime + 1;
      if (nextTime > 20) nextTime = 10;
      document.getElementById('timeSlider').value = nextTime;
      updateTimeSimulation(nextTime);
    }, 2000);
  }
}

/* 2D CANVAS & REALISTIC SIMULATION ENGINE */
let venueCanvas, venueCtx;
let peopleCanvas, peopleCtx;
let heatmapCanvas, heatmapCtx;

let simRunning = false;
let animFrameId = null;

let isRain = false;
let isEmergency = false;
let emergencyPos = null;

let people = [];
let raindrops = [];

function initCanvases(){
  initLayoutHistory();

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

  initPeopleData(w, h);
  initRainData(w, h);

  loadSelectedHistory(currentLayoutIndex);

  if (!animFrameId) {
    renderLoop();
  }
}

function initPeopleData(w, h){
  people = [];
  for(let i=0; i<75; i++){
    people.push({
      x: w*0.15 + Math.random()*w*0.7,
      y: h*0.2 + Math.random()*h*0.6,
      vx: (Math.random()-0.5)*1.4,
      vy: (Math.random()-0.5)*1.4,
      targetX: Math.random()*w,
      targetY: Math.random()*h,
      speed: 0.7 + Math.random()*0.8
    });
  }
}

function initRainData(w, h){
  raindrops = [];
  for(let i=0; i<110; i++){
    raindrops.push({
      x: Math.random()*w,
      y: Math.random()*h,
      len: 8 + Math.random()*12,
      vy: 6 + Math.random()*6
    });
  }
}

function updateSimulationLogic(){
  if(!venueCanvas) return;
  const w = venueCanvas.width;
  const h = venueCanvas.height;

  const currentBooths = layoutHistory[currentLayoutIndex].booths;
  const med = currentBooths.medical;
  const medCenterX = med.x * w + med.bw * w * 0.5;
  const medCenterY = med.y * h + med.bh * h * 0.5;

  if (isEmergency && emergencyPos) {
    const dx = medCenterX - emergencyPos.x;
    const dy = medCenterY - emergencyPos.y;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > 8) {
      emergencyPos.x += (dx / dist) * 3.0;
      emergencyPos.y += (dy / dist) * 3.0;
    }
  }

  people.forEach(p => {
    if (isRain) {
      const stage = currentBooths.stage;
      const targetX = stage.x * w + stage.bw * w * 0.5;
      const targetY = stage.y * h + stage.bh * h * 0.5;
      p.vx += (targetX - p.x) * 0.0006;
      p.vy += (targetY - p.y) * 0.0006;
      p.speed = 2.2;
    } else if (isEmergency && emergencyPos) {
      const dx = p.x - emergencyPos.x;
      const dy = p.y - emergencyPos.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 90 && dist > 0) {
        p.vx += (dx / dist) * 0.6;
        p.vy += (dy / dist) * 0.6;
      }
    } else {
      p.speed = 0.9;
      if (Math.random() < 0.025) {
        p.targetX = Math.random() * w;
        p.targetY = Math.random() * h;
      }
      p.vx += (p.targetX - p.x) * 0.00025;
      p.vy += (p.targetY - p.y) * 0.00025;
    }

    const currentSpeed = Math.sqrt(p.vx*p.vx + p.vy*p.vy);
    if(currentSpeed > p.speed){
      p.vx = (p.vx / currentSpeed) * p.speed;
      p.vy = (p.vy / currentSpeed) * p.speed;
    }

    p.x += p.vx;
    p.y += p.vy;

    if(p.x < 15) { p.x = 15; p.vx *= -1; }
    if(p.x > w-15) { p.x = w-15; p.vx *= -1; }
    if(p.y < 15) { p.y = 15; p.vy *= -1; }
    if(p.y > h-15) { p.y = h-15; p.vy *= -1; }
  });

  if (isRain) {
    raindrops.forEach(r => {
      r.y += r.vy;
      r.x -= 1;
      if (r.y > h) { r.y = 0; r.x = Math.random() * w; }
    });
  }
}

function renderLoop(){
  if (simRunning) {
    updateSimulationLogic();
  }

  if (peopleCanvas && venueCanvas) {
    const w = venueCanvas.width;
    const h = venueCanvas.height;
    drawPeople(w, h);
    drawRealtimeHeatmap(w, h);
  }

  animFrameId = requestAnimationFrame(renderLoop);
}

/* DETAILED CONCRETE VENUE DRAWING */
function drawDetailedOutdoorVenue(w, h){
  if(!venueCtx || currentLayoutIndex < 0) return;
  const currentBooths = layoutHistory[currentLayoutIndex].booths;

  // Background Grass Field
  venueCtx.fillStyle = isRain ? '#254e2b' : '#3a7d44';
  venueCtx.fillRect(0, 0, w, h);

  // Decorative Trees around boundaries
  venueCtx.fillStyle = '#2d6135';
  for(let x=10; x<w; x+=30){
    venueCtx.beginPath(); venueCtx.arc(x, 10, 14, 0, Math.PI*2); venueCtx.fill();
    venueCtx.beginPath(); venueCtx.arc(x, h-10, 14, 0, Math.PI*2); venueCtx.fill();
  }
  for(let y=10; y<h; y+=30){
    venueCtx.beginPath(); venueCtx.arc(10, y, 14, 0, Math.PI*2); venueCtx.fill();
    venueCtx.beginPath(); venueCtx.arc(w-10, y, 14, 0, Math.PI*2); venueCtx.fill();
  }

  // Paved Main Walkways (Cross roads & Loops)
  venueCtx.strokeStyle = isRain ? '#9ca3af' : '#e2d9c8';
  venueCtx.lineWidth = 32;
  venueCtx.lineCap = 'round';
  
  // Vertical Main Avenue
  venueCtx.beginPath();
  venueCtx.moveTo(w*0.5, h*0.9);
  venueCtx.lineTo(w*0.5, h*0.48);
  venueCtx.stroke();

  // Central Circular Plaza Walkway
  venueCtx.beginPath();
  venueCtx.arc(w*0.5, h*0.52, w*0.28, 0, Math.PI*2);
  venueCtx.stroke();

  // Central Lawn Area Inside Circle
  venueCtx.fillStyle = isRain ? '#377341' : '#4fa15a';
  venueCtx.beginPath();
  venueCtx.arc(w*0.5, h*0.52, w*0.22, 0, Math.PI*2);
  venueCtx.fill();

  // Draw Picnic Benches / Parasols in Lawn
  const picnicSpots = [
    {x: w*0.44, y: h*0.48}, {x: w*0.56, y: h*0.48},
    {x: w*0.46, y: h*0.58}, {x: w*0.54, y: h*0.58}
  ];
  picnicSpots.forEach(pt => {
    venueCtx.fillStyle = '#f59e0b';
    venueCtx.beginPath(); venueCtx.arc(pt.x, pt.y, 9, 0, Math.PI*2); venueCtx.fill();
    venueCtx.fillStyle = '#ffffff';
    venueCtx.beginPath(); venueCtx.arc(pt.x, pt.y, 3, 0, Math.PI*2); venueCtx.fill();
  });

  // Render Concrete Booths
  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    drawConcreteBooth(venueCtx, b.x*w, b.y*h, b.bw*w, b.bh*h, b.title, b.color, b.icon);
  });

  // Main Entrance Gate Plaza
  venueCtx.fillStyle = '#334155';
  venueCtx.fillRect(w*0.40, h*0.87, w*0.20, h*0.09);
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 11px Pretendard, sans-serif';
  venueCtx.textAlign = 'center';
  venueCtx.fillText('🚪 종합 주출입구 (Gate A)', w*0.5, h*0.92);
}

function drawConcreteBooth(ctx, x, y, bw, bh, title, color, icon){
  // Drop shadow
  ctx.fillStyle = 'rgba(0,0,0,0.35)';
  ctx.fillRect(x+4, y+4, bw, bh);

  // Main Body with Rounded Corners
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, bw, bh, 8);
  ctx.fill();

  // Border Stroke
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Inner Canopy Effect Line
  ctx.strokeStyle = 'rgba(255,255,255,0.4)';
  ctx.lineWidth = 1;
  ctx.strokeRect(x+4, y+4, bw-8, bh-8);

  // Title & Icon
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 11px Pretendard, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(`${icon} ${title}`, x + bw/2, y + bh/2 + 4);
}

function drawPeople(w, h){
  if(!peopleCtx) return;
  peopleCtx.clearRect(0,0,w,h);

  // Draw Crowd Agents
  people.forEach(p => {
    peopleCtx.fillStyle = isRain ? '#60a5fa' : '#ffffff';
    peopleCtx.beginPath();
    peopleCtx.arc(p.x, p.y, 3.5, 0, Math.PI*2);
    peopleCtx.fill();
    peopleCtx.strokeStyle = 'rgba(0,0,0,0.3)';
    peopleCtx.lineWidth = 0.8;
    peopleCtx.stroke();
  });

  // Emergency Patient Transfer Route & Animation
  if (isEmergency && emergencyPos) {
    const currentBooths = layoutHistory[currentLayoutIndex].booths;
    const med = currentBooths.medical;
    const medCenterX = med.x * w + med.bw * w * 0.5;
    const medCenterY = med.y * h + med.bh * h * 0.5;

    // Dashed Red Emergency Route Line
    peopleCtx.strokeStyle = '#ef4444';
    peopleCtx.lineWidth = 3.5;
    peopleCtx.setLineDash([8, 6]);
    peopleCtx.beginPath();
    peopleCtx.moveTo(emergencyPos.x, emergencyPos.y);
    peopleCtx.lineTo(medCenterX, medCenterY);
    peopleCtx.stroke();
    peopleCtx.setLineDash([]);

    // Emergency Patient Pulsing Beacon
    peopleCtx.fillStyle = '#ef4444';
    peopleCtx.beginPath();
    peopleCtx.arc(emergencyPos.x, emergencyPos.y, 9, 0, Math.PI*2);
    peopleCtx.fill();

    peopleCtx.fillStyle = '#ffffff';
    peopleCtx.font = 'bold 10px Pretendard';
    peopleCtx.textAlign = 'center';
    peopleCtx.fillText('🚨 응급환자 후송중', emergencyPos.x, emergencyPos.y - 12);
  }

  // Raindrops Overlay
  if (isRain) {
    peopleCtx.strokeStyle = 'rgba(147, 197, 253, 0.6)';
    peopleCtx.lineWidth = 1.3;
    raindrops.forEach(r => {
      peopleCtx.beginPath();
      peopleCtx.moveTo(r.x, r.y);
      peopleCtx.lineTo(r.x - 2, r.y + r.len);
      peopleCtx.stroke();
    });
  }
}

/* REALISTIC HIGH-PERFORMANCE HEATMAP */
function drawRealtimeHeatmap(w, h){
  if(!heatmapCtx) return;
  heatmapCtx.clearRect(0,0,w,h);

  const grid = {};
  const gridSize = 36;

  people.forEach(p => {
    const gx = Math.floor(p.x / gridSize);
    const gy = Math.floor(p.y / gridSize);
    const key = `${gx}_${gy}`;
    grid[key] = (grid[key] || 0) + 1;
  });

  Object.keys(grid).forEach(key => {
    const [gx, gy] = key.split('_').map(Number);
    const count = grid[key];
    const cx = gx * gridSize + gridSize/2;
    const cy = gy * gridSize + gridSize/2;

    if (count >= 1) {
      let radius = count * 14;
      let alpha = Math.min(0.85, count * 0.12);

      let grad = heatmapCtx.createRadialGradient(cx, cy, 0, cx, cy, radius);
      if (count >= 6) {
        grad.addColorStop(0, `rgba(239, 68, 68, ${alpha})`); // Red (High Risk / Bottleneck)
        grad.addColorStop(0.5, `rgba(245, 158, 11, ${alpha*0.7})`); // Orange
      } else if (count >= 3) {
        grad.addColorStop(0, `rgba(245, 158, 11, ${alpha})`); // Orange/Yellow
        grad.addColorStop(0.5, `rgba(234, 179, 8, ${alpha*0.5})`);
      } else {
        grad.addColorStop(0, `rgba(16, 185, 129, ${alpha*0.8})`); // Green (Smooth)
      }
      grad.addColorStop(1, 'rgba(16, 185, 129, 0)');

      heatmapCtx.fillStyle = grad;
      heatmapCtx.beginPath();
      heatmapCtx.arc(cx, cy, radius, 0, Math.PI*2);
      heatmapCtx.fill();
    }
  });

  // Highlight Emergency Heatmap Zone
  if (isEmergency && emergencyPos) {
    let grad = heatmapCtx.createRadialGradient(emergencyPos.x, emergencyPos.y, 0, emergencyPos.x, emergencyPos.y, 70);
    grad.addColorStop(0, 'rgba(225, 29, 72, 0.95)');
    grad.addColorStop(1, 'rgba(225, 29, 72, 0)');
    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(emergencyPos.x, emergencyPos.y, 70, 0, Math.PI*2);
    heatmapCtx.fill();
  }
}

function toggleSim(){
  simRunning = !simRunning;
  const btn = document.getElementById('btnToggleSim');
  const timer = document.getElementById('simTimer');

  if (simRunning) {
    btn.textContent = '⏸ 시뮬레이션 일시정지';
    timer.textContent = '상태: 실시간 군중 물리 에이전트 연산 중 ▶';
  } else {
    btn.textContent = '▶ 시뮬레이션 시작';
    timer.textContent = '상태: 대기중';
  }
}

function toggleRainEnv(){
  isRain = !isRain;
  const btn = document.getElementById('btnRain');
  const badge = document.getElementById('envBadge');

  if (isRain) {
    btn.classList.add('active');
    btn.textContent = '🌧️ 우천 모드 (ON)';
    badge.textContent = '🌧️ 강우 기상변수 적용됨';
  } else {
    btn.classList.remove('active');
    btn.textContent = '🌧️ 우천 모드';
    if(!isEmergency) badge.textContent = '실시간 동기화';
  }
  if (venueCanvas) drawDetailedOutdoorVenue(venueCanvas.width, venueCanvas.height);
}

function triggerEmergencyEnv(){
  isEmergency = !isEmergency;
  const btn = document.getElementById('btnEmergency');
  const badge = document.getElementById('envBadge');

  if (isEmergency) {
    btn.classList.add('active');
    btn.textContent = '🚨 응급상황 해제';
    badge.textContent = '🚨 응급환자 발생! 최단 후송 경로 가동';

    const w = venueCanvas.width;
    const h = venueCanvas.height;
    emergencyPos = { x: w * 0.2, y: h * 0.35 };

    if(!simRunning) toggleSim();
  } else {
    btn.classList.remove('active');
    btn.textContent = '🚨 응급환자 발생 (최단 후송)';
    emergencyPos = null;
    if(!isRain) badge.textContent = '실시간 동기화';
  }
}

/* THREE.JS 3D VIEW ENGINE */
let is3DActive = false;
let scene3D, camera3D, renderer3D;

function toggle3DView(){
  is3DActive = !is3DActive;
  const container3D = document.getElementById('container3D');
  const btn = document.getElementById('btnToggle3D');

  if (is3DActive) {
    container3D.style.display = 'block';
    btn.textContent = '🗺️ 2D 평면도 보기';
    init3DScene();
  } else {
    container3D.style.display = 'none';
    btn.textContent = '🧊 3D 입체뷰 보기';
  }
}

function init3DScene(){
  const container = document.getElementById('container3D');
  container.innerHTML = '';

  const w = container.clientWidth;
  const h = container.clientHeight;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
  camera3D.position.set(0, 160, 190);
  camera3D.lookAt(0, 0, 0);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
  scene3D.add(ambientLight);

  const dirLight = new THREE.DirectionalLight(0xffffff, 0.85);
  dirLight.position.set(50, 120, 50);
  scene3D.add(dirLight);

  const groundGeo = new THREE.PlaneGeometry(210, 150);
  const groundMat = new THREE.MeshLambertMaterial({ color: 0x2e7d32 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  scene3D.add(ground);

  update3DScene();

  function animate3D() {
    if (is3DActive) {
      requestAnimationFrame(animate3D);
      scene3D.rotation.y += 0.0025;
      renderer3D.render(scene3D, camera3D);
    }
  }
  animate3D();
}

function update3DScene(){
  if (!scene3D) return;

  for(let i = scene3D.children.length - 1; i >= 0; i--) {
    if(scene3D.children[i].userData.isBooth) {
      scene3D.remove(scene3D.children[i]);
    }
  }

  const currentBooths = layoutHistory[currentLayoutIndex].booths;

  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    const bw = b.bw * 210;
    const bh = b.bh * 150;
    const bx = (b.x - 0.5) * 210 + bw/2;
    const bz = (b.y - 0.5) * 150 + bh/2;

    const height = key === 'stage' ? 20 : 12;
    const geo = new THREE.BoxGeometry(bw, height, bh);
    const colorHex = parseInt(b.color.replace('#', '0x'));
    const mat = new THREE.MeshLambertMaterial({ color: colorHex });

    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(bx, height/2, bz);
    mesh.userData.isBooth = true;
    scene3D.add(mesh);
  });
}

/* INITIAL LOAD: DEFAULT TO DESIGN DASHBOARD */
window.addEventListener('load', () => {
  switchPage('design', null);
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=1300, scrolling=True)
