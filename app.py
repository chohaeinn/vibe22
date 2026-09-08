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

/* Main Dashboard Grids */
.dashboard-main-grid{
  display:grid;
  grid-template-columns: 1.5fr 0.9fr 1fr;
  gap:16px;
}
.dashboard-bottom-grid{
  display:grid;
  grid-template-columns: 1fr 1.2fr 0.9fr;
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
  height:360px;
  background:#1e293b;
  border-radius:12px;
  overflow:hidden;
  border:1px solid #334155;
}
#venueCanvas, #heatmapCanvas, #peopleCanvas{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
}
#heatmapCanvas{z-index:5;opacity:0.85;pointer-events:none;}
#peopleCanvas{z-index:10;pointer-events:none;}

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

/* Score Table */
.score-tbl{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:12px;}
.score-tbl th,.score-tbl td{padding:8px 6px;text-align:left;border-bottom:1px solid #f1f5f9;}
.score-tbl th{color:#64748b;font-weight:700;font-size:11px;}
.grade-badge{
  padding:2px 8px;
  border-radius:10px;
  font-weight:800;
  font-size:10.5px;
  display:inline-block;
}
.gb-excel{background:#dcfce7;color:#15803d;}
.gb-good{background:#e0f2fe;color:#0369a1;}
.gb-warn{background:#fef3c7;color:#b45309;}

/* AI Recommendations list */
.ai-recom-list{
  list-style:none;
  display:flex;
  flex-direction:column;
  gap:8px;
  font-size:11.5px;
  color:#334155;
}
.ai-recom-list li{
  display:flex;
  align-items:flex-start;
  gap:6px;
  line-height:1.4;
  background:#f8fafc;
  padding:8px 10px;
  border-radius:8px;
  border:1px solid #f1f5f9;
}
.ai-recom-list li::before{
  content:"✔";
  color:#10b981;
  font-weight:900;
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
      <div class="nav-item" onclick="switchPage('home', this)">
        <span class="nav-icon">🏠</span> 홈
      </div>
      <div class="nav-item active" onclick="switchPage('design', this)">
        <span class="nav-icon">📋</span> 행사 설계
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span class="nav-icon">⚙️</span> 설계 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span class="nav-icon">📊</span> 비전 설계 리포트
      </div>
      <div class="nav-item" onclick="switchPage('assistant', this)">
        <span class="nav-icon">🤖</span> 마이페이지 / AI
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
        <h2 id="topTitleText">📋 행사 설계</h2>
        <p id="topSubText">행사 정보를 입력하시면 AI가 최적의 행사장을 설계해드립니다.</p>
      </div>
      <button class="btn-primary" onclick="runAIGenerate()">
        ✦ AI 재배치 실행하기
      </button>
    </header>

    <!-- PAGE 1: HOME -->
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
            <textarea id="inPrompt" rows="3">메인 무대는 중앙 상단에 배치하고, Central Lawn(잔디 휴식존) 주변으로 푸드트럭과 체험 부스를 원형으로 둘러싸 배치해주세요. 응급 의료센터는 메인 출입구 인근에 놓아 병목을 방지하세요.</textarea>
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn-primary" onclick="runAIGenerate()">
            ✦ 입력 정보 기반 AI 설계 생성
          </button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: DESIGN DASHBOARD -->
    <section id="pageDesign" class="page-view active">

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
          <div class="info-box">
            <div class="info-box-icon">🎫</div>
            <div class="info-box-text"><label>입장료</label><span id="outTicket">무료</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">💰</div>
            <div class="info-box-text"><label>예산</label><span id="outBudget">5,000만원</span></div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-main-grid" style="margin-top:14px;">

        <!-- 1. Digital Twin Canvas Map -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 행사장 배치도 (디지털 트윈 렌더링)</span>
            <span class="card-badge" id="layoutBadge">v1.0 AI 설계</span>
          </div>
          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>

            <!-- Legend -->
            <div class="map-legend-overlay">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 무대존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 푸드존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 휴식공간</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 안전센터</div>
              <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> 화장실/편의</div>
              <div class="legend-item"><span class="legend-dot" style="background:#64748b;"></span> 출입구</div>
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
                🚨 응급환자 발생
              </button>
            </div>
            <span style="font-size:11px;color:#64748b;font-weight:700;" id="simTimer">상태: 대기중</span>
          </div>
        </div>

        <!-- 2. Density Heatmap -->
        <div class="card-panel">
          <div class="card-head">
            <span>🔥 실시간 군중 밀집도 Heatmap</span>
            <span class="card-badge" id="envBadge">일반 상태</span>
          </div>
          <div class="map-wrap">
            <canvas id="heatmapCanvas"></canvas>
          </div>
          <div style="display:flex;justify-content:space-around;font-size:10px;color:#64748b;margin-top:10px;font-weight:700;">
            <span style="color:#10b981;">🟢 원활</span>
            <span style="color:#eab308;">🟡 보통</span>
            <span style="color:#f97316;">🟠 혼잡</span>
            <span style="color:#ef4444;">🔴 위험</span>
          </div>
        </div>

        <!-- 3. AI Evaluation & Suggestions -->
        <div class="card-panel">
          <div class="card-head">
            <span>💡 AI 평가 결과</span>
          </div>
          <table class="score-tbl">
            <thead>
              <tr><th>평가 항목</th><th>점수</th><th>등급</th></tr>
            </thead>
            <tbody id="evalScoreTable">
              <tr><td>비상 안전성</td><td id="scSafety">92점</td><td><span class="grade-badge gb-excel" id="gbSafety">매우 우수</span></td></tr>
              <tr><td>동선 효율성</td><td id="scFlow">87점</td><td><span class="grade-badge gb-good" id="gbFlow">우수</span></td></tr>
              <tr><td>접근성</td><td id="scAccess">96점</td><td><span class="grade-badge gb-excel" id="gbAccess">매우 우수</span></td></tr>
              <tr><td>혼잡도 분산</td><td id="scCong">84점</td><td><span class="grade-badge gb-good" id="gbCong">우수</span></td></tr>
              <tr><td>공간 활용성</td><td id="scSpace">88점</td><td><span class="grade-badge gb-good" id="gbSpace">우수</span></td></tr>
            </tbody>
          </table>

          <div style="font-size:12px;font-weight:800;color:#0f172a;margin:10px 0 6px 0;">💡 AI 개선 및 맞춤 제안</div>
          <ul class="ai-recom-list" id="aiRecomList">
            <li>공연 무대 전면 피크 시간대 차단봉 추가 설치로 우발 병목 해소</li>
            <li>응급 의료센터를 입구 근처로 이동시켜 비상 접근성 25% 개선</li>
            <li>체험존 주변을 원형으로 배치하여 관람객 이동 흐름 순환</li>
            <li>화장실 수를 2개 추가 배치하여 대기 시간을 줄일 수 있습니다.</li>
          </ul>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-bottom-grid" style="margin-top:14px;">

        <!-- 1. Before / After Comparison -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚖️ 설계 전 / 후 비교</span>
          </div>
          <div class="compare-grid">
            <div class="comp-col">
              <h5>AI 설계 전 (기존)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-red" id="compBeforeBottleneck">68%</span></div>
              <div class="comp-val"><span>안전 접근성</span><span id="compBeforeAccess">65점</span></div>
              <div class="comp-val"><span>사고 위험구역</span><span class="text-red" id="compBeforeRisk">3개소</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#cbd5e1;">→</div>
            <div class="comp-col">
              <h5>AI 설계 후 (최적화)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-green" id="compAfterBottleneck">18%</span></div>
              <div class="comp-val"><span>안전 접근성</span><span class="text-green" id="compAfterAccess">96점</span></div>
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
            <div class="wf-card"><div class="wf-icon">📋</div><div class="wf-title">행사 정보 입력</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🌐</div><div class="wf-title">디지털 트윈 생성</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🤖</div><div class="wf-title">AI 기반 배치 생성</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">📊</div><div class="wf-title">군중 이동 시뮬레이션</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">📄</div><div class="wf-title">리포트 출력</div></div>
          </div>
          <div class="wf-sub-tags">
            <span class="wf-tag">목적/요구사항 선택</span>
            <span class="wf-tag">AI 레이아웃 제시</span>
            <span class="wf-tag">병목 + 안전 분석</span>
            <span class="wf-tag">최적 설계안 확정</span>
          </div>
        </div>

        <!-- 3. Report Summary -->
        <div class="card-panel">
          <div class="card-head">
            <span>📄 분석 리포트 요약</span>
          </div>
          <div class="report-sum-box" id="reportSummaryBox">
            AI 분석 결과, <b>2025 힐링 페스티벌</b>은 5,000명의 관람객을 안전하게 수용할 수 있는 최적 구조입니다.
          </div>
          <button class="btn-primary" style="width:100%;justify-content:center;padding:10px;font-size:12px;margin-top:auto;" onclick="openReportModal()">
            📌 이 설계안을 기반으로 상세 보고서 생성 (PDF)
          </button>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS -->
    <section id="pageProcess" class="page-view">
      <div class="form-card">
        <div class="form-section-head">⚙️ AI 행사 공간 설계 및 시뮬레이션 메커니즘</div>
        <p style="font-size:13px;line-height:1.7;color:#334155;">
          1. <b>공간 파라미터 생성:</b> 입출구, 무대, 푸드존 등의 위치 데이터를 2D/3D 메시 그리드로 변환합니다.<br>
          2. <b>다방향 군중 에이전트 시뮬레이션:</b> 관람객 5,000명의 목적지(공연 관람, 음식 구매, 휴식 등)에 따른 유동 경로를 실시간 물리 엔진으로 연산합니다.<br>
          3. <b>돌발 상황 및 우천 시뮬레이션:</b> 강우 시 피난 이동 속도 증가 및 응급환자 발생 시 골든타임 동선 확보 경로를 동적으로 검증합니다.<br>
          4. <b>자동 히스토리 관리:</b> AI 재배치 시 이전의 설계를 자동으로 저장하여 언제든 버전별 비교가 가능합니다.
        </p>
      </div>
    </section>

    <!-- PAGE 4: MYPAGE / ASSISTANT -->
    <section id="pageAssistant" class="page-view">
      <div class="form-card">
        <div class="form-section-head">🤖 AI 실시간 레이아웃 대화형 어시스턴트</div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:12px;border-radius:10px;height:200px;overflow-y:auto;font-size:12px;margin-bottom:12px;" id="chatBox">
          <div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;">
            AI: 안녕하세요 추천님! "무대를 오른쪽으로 이동해줘", "우천 대비용 천막 추가해줘" 와 같은 명령을 내려주시면 즉시 배치도를 재생성하고 이전 기록에 저장합니다.
          </div>
        </div>
        <div style="display:flex;gap:8px;">
          <input type="text" id="chatIn" placeholder="요구사항을 입력하세요... (예: 응급센터 통로를 확장해줘)" style="flex:1;padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;">
          <button class="btn-primary" onclick="sendChat()">전송</button>
        </div>
      </div>
    </section>

  </main>
</div>

<!-- DETAILED PDF REPORT MODAL -->
<div class="modal-bg" id="reportModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #f1f5f9;margin-bottom:16px;">
      <h3 style="font-size:18px;font-weight:800;color:#0f172a;">📊 AI 행사장 종합 최적화 상세 보고서</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:20px;font-weight:800;color:#64748b;">✕</button>
    </div>

    <div class="modal-body">
      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">1. 종합 평가 요약</h4>
        <p style="font-size:12.5px;color:#334155;line-height:1.6;" id="modalSummaryText">
          본 보고서는 <b>2025 힐링 페스티벌</b> (야외 잔디 광장 50,000m², 예상 관람객 5,000명)의 안전 및 동선 최적화를 위해 생성되었습니다. AI 시뮬레이션 결과 종합 안전성 점수 <b>92점</b>, 동선 효율성 <b>87점</b>을 기록하였습니다.
        </p>
      </div>

      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">2. 구역별 세부 설비 지침</h4>
        <ul style="font-size:12px;color:#334155;line-height:1.7;padding-left:18px;" id="modalDetailList">
          <li><b>메인 무대:</b> 배치 구역 상단 잔디면, 전면 관람 구역 통로 폭 4m 확보.</li>
          <li><b>응급 의료 센터:</b> 주출입구 인근 전진 배치, 앰뷸런스 전용 진출입로 확보.</li>
          <li><b>Central Lawn (휴식존):</b> 파라솔 및 파라솔 테이블 40개소 배치로 관람객 머무름 시간 분산.</li>
          <li><b>푸드 존:</b> 잔디광장 외곽 통풍 구역에 푸드트럭 일렬 배치.</li>
        </ul>
      </div>

      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">3. 비상 대피 및 우천/응급 대응 시뮬레이션 분석</h4>
        <p style="font-size:12px;color:#334155;line-height:1.6;">
          비상 및 응급 상황 발생 시 출입구를 통해 관람객 전원이 <b>2분 10초</b> 이내 대피 가능하며, 응급구조대의 현장 도달 골든타임(3분 이내)이 100% 확보됩니다.
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
/* Navigation Switching */
function switchPage(pageId, el){
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  if(el) el.classList.add('active');

  const t = document.getElementById('topTitleText');
  const s = document.getElementById('topSubText');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
    t.textContent = '📝 행사 정보 입력';
    s.textContent = '상세 기본 정보 및 요구사항을 입력하시면 AI가 자동 설계합니다.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    t.textContent = '📋 행사 설계';
    s.textContent = '행사 정보를 입력하시면 AI가 최적의 행사장을 설계해드립니다.';
    setTimeout(initCanvases, 50);
  } else if(pageId === 'process'){
    document.getElementById('pageProcess').classList.add('active');
    t.textContent = '⚙️ 설계 프로세스';
    s.textContent = 'AI 분석 및 자동 배치 알고리즘 메커니즘입니다.';
  } else if(pageId === 'assistant'){
    document.getElementById('pageAssistant').classList.add('active');
    t.textContent = '🤖 마이페이지 / AI';
    s.textContent = '실시간 대화로 행사장을 수정합니다.';
  }
}

function openReportModal(){ document.getElementById('reportModal').classList.add('active'); }
function closeReportModal(){ document.getElementById('reportModal').classList.remove('active'); }
function openAuthModal(){ alert('로그아웃 되었습니다.'); }

/* APP STATE & BLUEPRINT HISTORY SYSTEM */
let layoutHistory = [];
let currentLayoutIndex = -1;

// Default Base Layout Config
const layoutPresets = [
  {
    versionName: "v1.0 - 기본 최적안",
    timestamp: "방금 전",
    booths: {
      stage: {x: 0.38, y: 0.08, bw: 0.24, bh: 0.16, title: '메인 무대', color: '#8b5cf6', icon: '🎭'},
      expA: {x: 0.12, y: 0.22, bw: 0.16, bh: 0.14, title: '체험존 A', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.72, y: 0.22, bw: 0.16, bh: 0.14, title: '체험존 B', color: '#3b82f6', icon: '🚀'},
      food: {x: 0.10, y: 0.48, bw: 0.16, bh: 0.15, title: '푸드존', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.72, y: 0.48, bw: 0.16, bh: 0.14, title: '응급 의료센터', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.72, y: 0.70, bw: 0.14, bh: 0.12, title: '화장실', color: '#06b6d4', icon: '🚻'}
    },
    scores: { safety: 92, flow: 87, access: 96, cong: 84, space: 88 },
    recoms: [
      "공연 무대 전면 피크 시간대 차단봉 추가 설치로 우발 병목 해소",
      "응급 의료센터를 입구 근처로 이동시켜 비상 접근성 25% 개선",
      "체험존 주변을 원형으로 배치하여 관람객 이동 흐름 순환",
      "화장실 수를 2개 추가 배치하여 대기 시간을 줄일 수 있습니다."
    ],
    comp: { beforeBtn: "68%", beforeAcc: "65점", beforeRisk: "3개소", afterBtn: "18%", afterAcc: "96점", afterRisk: "0개소" }
  },
  {
    versionName: "v2.0 - 우천/골든타임 특화 안",
    timestamp: "신규 생성",
    booths: {
      stage: {x: 0.35, y: 0.08, bw: 0.30, bh: 0.18, title: '메인 대형무대 (캐노피)', color: '#8b5cf6', icon: '🎪'},
      expA: {x: 0.08, y: 0.25, bw: 0.20, bh: 0.14, title: '체험존 (실내 돔)', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.72, y: 0.25, bw: 0.20, bh: 0.14, title: '휴식/우비 배포존', color: '#10b981', icon: '☂️'},
      food: {x: 0.08, y: 0.52, bw: 0.20, bh: 0.15, title: '실내 푸드존', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.42, y: 0.72, bw: 0.16, bh: 0.14, title: '응급 의료센터 (중앙)', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.75, y: 0.72, bw: 0.16, bh: 0.12, title: '화장실/편의', color: '#06b6d4', icon: '🚻'}
    },
    scores: { safety: 98, flow: 91, access: 94, cong: 90, space: 85 },
    recoms: [
      "응급 의료센터를 주 출입로 및 중앙 사거리 전진 배치하여 접근성 극대화",
      "우천 대비 우수 관로 확보 및 방수 캐노피 천막 확장 설치",
      "중앙 통로 폭을 6m로 넓혀 비상 차량 전용 차선 통행 보장",
      "배수 시설 근접 구역으로 푸드존 이동"
    ],
    comp: { beforeBtn: "55%", beforeAcc: "70점", beforeRisk: "2개소", afterBtn: "8%", afterAcc: "98점", afterRisk: "0개소" }
  },
  {
    versionName: "v3.0 - 대형 관람객 군중 분산 안",
    timestamp: "신규 생성",
    booths: {
      stage: {x: 0.38, y: 0.05, bw: 0.24, bh: 0.15, title: '메인 무대', color: '#8b5cf6', icon: '🎭'},
      expA: {x: 0.05, y: 0.18, bw: 0.18, bh: 0.14, title: '체험존 A', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.77, y: 0.18, bw: 0.18, bh: 0.14, title: '체험존 B', color: '#3b82f6', icon: '🚀'},
      food: {x: 0.05, y: 0.65, bw: 0.18, bh: 0.15, title: '분산 푸드존 A', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.77, y: 0.65, bw: 0.18, bh: 0.14, title: '응급 의료센터', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.41, y: 0.72, bw: 0.18, bh: 0.12, title: '화장실 (중앙)', color: '#06b6d4', icon: '🚻'}
    },
    scores: { safety: 95, flow: 94, access: 92, cong: 95, space: 91 },
    recoms: [
      "외곽으로 주요 부스 분산 배치하여 중앙 광장 병목 현상 완벽 방지",
      "화장실을 중앙에 배치하여 동서남북 어디서나 1분 이내 이용 가능",
      "비상 대피로 4개 사방 통로 전면 개방 유지"
    ],
    comp: { beforeBtn: "40%", beforeAcc: "78점", beforeRisk: "1개소", afterBtn: "5%", afterAcc: "95점", afterRisk: "0개소" }
  }
];

// Initialize history on start
function initLayoutHistory() {
  if (layoutHistory.length === 0) {
    // Add default v1
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

  // Update UI Elements with history item data
  document.getElementById('layoutBadge').textContent = layout.versionName;
  document.getElementById('historyStatusBadge').textContent = `현재 버전: ${layout.versionName}`;

  // Scores
  document.getElementById('scSafety').textContent = layout.scores.safety + '점';
  document.getElementById('scFlow').textContent = layout.scores.flow + '점';
  document.getElementById('scAccess').textContent = layout.scores.access + '점';
  document.getElementById('scCong').textContent = layout.scores.cong + '점';
  document.getElementById('scSpace').textContent = layout.scores.space + '점';

  // Recommendations
  const recomUl = document.getElementById('aiRecomList');
  recomUl.innerHTML = '';
  layout.recoms.forEach(r => {
    const li = document.createElement('li');
    li.textContent = r;
    recomUl.appendChild(li);
  });

  // Comparisons
  document.getElementById('compBeforeBottleneck').textContent = layout.comp.beforeBtn;
  document.getElementById('compBeforeAccess').textContent = layout.comp.beforeAcc;
  document.getElementById('compBeforeRisk').textContent = layout.comp.beforeRisk;
  document.getElementById('compAfterBottleneck').textContent = layout.comp.afterBtn;
  document.getElementById('compAfterAccess').textContent = layout.comp.afterAcc;
  document.getElementById('compAfterRisk').textContent = layout.comp.afterRisk;

  // Re-draw map canvas with loaded layout
  if (venueCanvas) {
    drawDetailedOutdoorVenue(venueCanvas.width, venueCanvas.height);
  }
}

/* AI Re-layout Trigger */
function runAIGenerate(){
  initLayoutHistory();

  // Create a new version by selecting next preset or creating variation
  const nextPresetIndex = layoutHistory.length % layoutPresets.length;
  const newLayout = JSON.parse(JSON.stringify(layoutPresets[nextPresetIndex]));

  const d = new Date();
  const timeStr = `${d.getHours()}:${d.getMinutes() < 10 ? '0' : ''}${d.getMinutes()}:${d.getSeconds() < 10 ? '0' : ''}${d.getSeconds()}`;
  newLayout.versionName = `v${layoutHistory.length + 1}.0 - AI 최적 재배치안`;
  newLayout.timestamp = timeStr;

  // Push into history stack (Saving previous blueprints!)
  layoutHistory.push(newLayout);
  currentLayoutIndex = layoutHistory.length - 1;

  updateHistorySelectUI();
  loadSelectedHistory(currentLayoutIndex);

  switchPage('design', document.querySelectorAll('.nav-item')[1]);
  alert(`✨ 새 AI 설계도가 생성되었습니다! 이전 설계도는 상단 '설계 히스토리' 기록에 안전하게 보관되었습니다.`);
}

/* Update Dashboard with Form Inputs */
function updateDashboardInputs(){
  const name = document.getElementById('inEventName').value;
  const vtype = document.getElementById('inVenueType').value;
  const loc = document.getElementById('inLocation').value;
  const vis = document.getElementById('inVisitors').value;
  const area = document.getElementById('inArea').value;
  const time = document.getElementById('inTime').value;
  const age = document.getElementById('inTargetAge').value;
  const cat = document.getElementById('inCategory').value;
  const ticket = document.getElementById('inTicket').value;
  const budget = document.getElementById('inBudget').value;

  document.getElementById('outEventName').textContent = name;
  document.getElementById('outVenueType').textContent = vtype;
  document.getElementById('outLocation').textContent = loc;
  document.getElementById('outVisitors').textContent = vis;
  document.getElementById('outArea').textContent = area;
  document.getElementById('outTime').textContent = time;
  document.getElementById('outAge').textContent = age;
  document.getElementById('outCategory').textContent = cat;
  document.getElementById('outTicket').textContent = ticket;
  document.getElementById('outBudget').textContent = budget;
}

/* Canvas & Real-time Active Simulation Engine */
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
let medicalAgents = [];

function initCanvases(){
  initLayoutHistory();
  updateDashboardInputs();

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

  // Start Animation Render Loop
  if (!animFrameId) {
    renderLoop();
  }
}

function initPeopleData(w, h){
  people = [];
  const count = 90; // Agent particles
  for(let i=0; i<count; i++){
    people.push({
      x: w*0.1 + Math.random()*w*0.8,
      y: h*0.15 + Math.random()*h*0.7,
      vx: (Math.random()-0.5)*1.5,
      vy: (Math.random()-0.5)*1.5,
      targetX: Math.random()*w,
      targetY: Math.random()*h,
      speed: 0.8 + Math.random()*0.8,
      color: '#ffffff'
    });
  }
}

function initRainData(w, h){
  raindrops = [];
  for(let i=0; i<120; i++){
    raindrops.push({
      x: Math.random()*w,
      y: Math.random()*h,
      len: 8 + Math.random()*12,
      vy: 6 + Math.random()*6
    });
  }
}

/* Simulation Physics & Agent Movement Update */
function updateSimulationLogic(){
  if(!venueCanvas) return;
  const w = venueCanvas.width;
  const h = venueCanvas.height;

  const currentBooths = layoutHistory[currentLayoutIndex].booths;

  // 1. Update People Behavior
  people.forEach(p => {
    // If Rain mode active: move faster towards stage canopy or gates/restrooms
    if (isRain) {
      const stage = currentBooths.stage;
      const targetX = stage.x * w + stage.bw * w * 0.5;
      const targetY = stage.y * h + stage.bh * h * 0.5;
      p.vx += (targetX - p.x) * 0.0005;
      p.vy += (targetY - p.y) * 0.0005;
      p.speed = 2.2; // Move faster in rain
    } 
    // If Emergency mode active: evade emergency position
    else if (isEmergency && emergencyPos) {
      const dx = p.x - emergencyPos.x;
      const dy = p.y - emergencyPos.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < 100 && dist > 0) {
        p.vx += (dx / dist) * 0.4; // Repelled from emergency
        p.vy += (dy / dist) * 0.4;
      }
    } 
    // Normal Wander Movement
    else {
      p.speed = 1.0;
      if (Math.random() < 0.02) {
        p.targetX = Math.random() * w;
        p.targetY = Math.random() * h;
      }
      p.vx += (p.targetX - p.x) * 0.0002;
      p.vy += (p.targetY - p.y) * 0.0002;
    }

    // Velocity Limit & Friction
    const maxSpeed = p.speed;
    const currentSpeed = Math.sqrt(p.vx*p.vx + p.vy*p.vy);
    if(currentSpeed > maxSpeed){
      p.vx = (p.vx / currentSpeed) * maxSpeed;
      p.vy = (p.vy / currentSpeed) * maxSpeed;
    }

    p.x += p.vx;
    p.y += p.vy;

    // Boundaries bounce
    if(p.x < 15) { p.x = 15; p.vx *= -1; }
    if(p.x > w-15) { p.x = w-15; p.vx *= -1; }
    if(p.y < 15) { p.y = 15; p.vy *= -1; }
    if(p.y > h-15) { p.y = h-15; p.vy *= -1; }
  });

  // 2. Update Medical Agents when emergency active
  if (isEmergency && emergencyPos && currentBooths.medical) {
    const medX = currentBooths.medical.x * w + currentBooths.medical.bw * w * 0.5;
    const medY = currentBooths.medical.y * h + currentBooths.medical.bh * h * 0.5;

    if (medicalAgents.length === 0) {
      medicalAgents = [
        {x: medX, y: medY, vx: 0, vy: 0},
        {x: medX + 10, y: medY + 10, vx: 0, vy: 0}
      ];
    }

    medicalAgents.forEach(m => {
      const dx = emergencyPos.x - m.x;
      const dy = emergencyPos.y - m.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist > 5) {
        m.x += (dx / dist) * 3.5; // High speed ambulance / medics
        m.y += (dy / dist) * 3.5;
      }
    });
  }

  // 3. Update Raindrops
  if (isRain) {
    raindrops.forEach(r => {
      r.y += r.vy;
      r.x -= 1;
      if (r.y > h) { r.y = 0; r.x = Math.random() * w; }
    });
  }
}

/* Master Animation Render Loop */
function renderLoop(){
  if (simRunning) {
    updateSimulationLogic();
  }

  if (peopleCanvas && venueCanvas) {
    const w = venueCanvas.width;
    const h = venueCanvas.height;

    // Render Layers
    drawPeople(w, h);
    drawDynamicHeatmap(w, h);
  }

  animFrameId = requestAnimationFrame(renderLoop);
}

function drawDetailedOutdoorVenue(w, h){
  if(!venueCtx || currentLayoutIndex < 0) return;

  const currentBooths = layoutHistory[currentLayoutIndex].booths;

  // Background Grass Lawn Texture
  venueCtx.fillStyle = isRain ? '#254e2b' : '#3a7d44'; // Darker grass if raining
  venueCtx.fillRect(0, 0, w, h);

  // Boundary Trees
  venueCtx.fillStyle = '#2d6135';
  for(let x=5; x<w; x+=25){
    venueCtx.beginPath(); venueCtx.arc(x, 8, 12, 0, Math.PI*2); venueCtx.fill();
    venueCtx.beginPath(); venueCtx.arc(x, h-8, 12, 0, Math.PI*2); venueCtx.fill();
  }
  for(let y=5; y<h; y+=25){
    venueCtx.beginPath(); venueCtx.arc(8, y, 12, 0, Math.PI*2); venueCtx.fill();
    venueCtx.beginPath(); venueCtx.arc(w-8, y, 12, 0, Math.PI*2); venueCtx.fill();
  }

  // Pedestrian Pathways
  venueCtx.strokeStyle = isRain ? '#b0a898' : '#e2d9c8';
  venueCtx.lineWidth = 30;
  venueCtx.lineCap = 'round';

  venueCtx.beginPath();
  venueCtx.moveTo(w*0.5, h*0.88);
  venueCtx.lineTo(w*0.5, h*0.55);
  venueCtx.stroke();

  venueCtx.beginPath();
  venueCtx.ellipse(w*0.5, h*0.5, w*0.38, h*0.3, 0, 0, Math.PI*2);
  venueCtx.stroke();

  // Central Lawn Rest Zone
  venueCtx.fillStyle = isRain ? '#377341' : '#4fa15a';
  venueCtx.beginPath();
  venueCtx.ellipse(w*0.5, h*0.5, w*0.22, h*0.18, 0, 0, Math.PI*2);
  venueCtx.fill();

  // Umbrellas / Tents
  const umbrellaPositions = [
    {x: w*0.42, y: h*0.45}, {x: w*0.58, y: h*0.45},
    {x: w*0.45, y: h*0.55}, {x: w*0.55, y: h*0.55},
    {x: w*0.50, y: h*0.48}
  ];
  umbrellaPositions.forEach(u => {
    venueCtx.fillStyle = '#f59e0b';
    venueCtx.beginPath(); venueCtx.arc(u.x, u.y, 8, 0, Math.PI*2); venueCtx.fill();
    venueCtx.fillStyle = '#ffffff';
    venueCtx.beginPath(); venueCtx.arc(u.x, u.y, 2.5, 0, Math.PI*2); venueCtx.fill();
  });

  // Render Layout Booths Dynamically from Active Blueprint
  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    drawGraphicBooth(venueCtx, b.x*w, b.y*h, b.bw*w, b.bh*h, b.title, b.color, b.icon);
  });

  // Gates
  venueCtx.fillStyle = '#1e293b';
  venueCtx.fillRect(w*0.42, h*0.86, w*0.16, h*0.08);
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 10px Pretendard, sans-serif';
  venueCtx.textAlign = 'center';
  venueCtx.fillText('🚪 주출입구', w*0.5, h*0.91);
}

function drawGraphicBooth(ctx, x, y, bw, bh, title, color, icon){
  ctx.fillStyle = 'rgba(0,0,0,0.25)';
  ctx.fillRect(x+3, y+3, bw, bh);

  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, bw, bh, 6);
  ctx.fill();

  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 10.5px Pretendard, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(`${icon} ${title}`, x + bw/2, y + bh/2 + 4);
}

function drawPeople(w, h){
  if(!peopleCtx) return;
  peopleCtx.clearRect(0,0,w,h);

  // Draw People Agents
  people.forEach(p => {
    peopleCtx.fillStyle = isRain ? '#60a5fa' : '#ffffff';
    peopleCtx.beginPath();
    peopleCtx.arc(p.x, p.y, 3.5, 0, Math.PI*2);
    peopleCtx.fill();
    peopleCtx.strokeStyle = 'rgba(0,0,0,0.3)';
    peopleCtx.lineWidth = 0.8;
    peopleCtx.stroke();
  });

  // Draw Emergency Effects & Medics
  if (isEmergency && emergencyPos) {
    // Red Flashing Beacon at Emergency Site
    const time = Date.now() * 0.005;
    const pulseR = 15 + Math.sin(time) * 10;
    
    peopleCtx.fillStyle = 'rgba(239, 68, 68, 0.4)';
    peopleCtx.beginPath();
    peopleCtx.arc(emergencyPos.x, emergencyPos.y, pulseR + 10, 0, Math.PI*2);
    peopleCtx.fill();

    peopleCtx.fillStyle = '#ef4444';
    peopleCtx.beginPath();
    peopleCtx.arc(emergencyPos.x, emergencyPos.y, 8, 0, Math.PI*2);
    peopleCtx.fill();

    peopleCtx.fillStyle = '#ffffff';
    peopleCtx.font = 'bold 10px Pretendard';
    peopleCtx.textAlign = 'center';
    peopleCtx.fillText('🚨 환자발생', emergencyPos.x, emergencyPos.y - 12);

    // Draw Responding Medical Agents (Yellow/Red Crosses)
    medicalAgents.forEach(m => {
      peopleCtx.fillStyle = '#facc15';
      peopleCtx.beginPath();
      peopleCtx.arc(m.x, m.y, 6, 0, Math.PI*2);
      peopleCtx.fill();
      peopleCtx.fillStyle = '#000000';
      peopleCtx.font = 'bold 8px Pretendard';
      peopleCtx.fillText('🚑', m.x, m.y + 3);
    });
  }

  // Draw Rain Effect Filter Overlay
  if (isRain) {
    peopleCtx.strokeStyle = 'rgba(147, 197, 253, 0.5)';
    peopleCtx.lineWidth = 1.2;
    raindrops.forEach(r => {
      peopleCtx.beginPath();
      peopleCtx.moveTo(r.x, r.y);
      peopleCtx.lineTo(r.x - 2, r.y + r.len);
      peopleCtx.stroke();
    });
  }
}

function drawDynamicHeatmap(w, h){
  if(!heatmapCtx) return;
  heatmapCtx.clearRect(0,0,w,h);

  // Compute Grid Density from Particle Coordinates dynamically
  const grid = {};
  const gridSize = 40;

  people.forEach(p => {
    const gx = Math.floor(p.x / gridSize);
    const gy = Math.floor(p.y / gridSize);
    const key = `${gx}_${gy}`;
    grid[key] = (grid[key] || 0) + 1;
  });

  // Render Hotspots based on Real-time Particle Cluster Density
  Object.keys(grid).forEach(key => {
    const [gx, gy] = key.split('_').map(Number);
    const count = grid[key];
    const cx = gx * gridSize + gridSize/2;
    const cy = gy * gridSize + gridSize/2;

    if (count >= 2) {
      let radius = count * 12;
      let alpha = Math.min(0.8, count * 0.15);

      let grad = heatmapCtx.createRadialGradient(cx, cy, 0, cx, cy, radius);
      if (count >= 6) {
        grad.addColorStop(0, `rgba(239, 68, 68, ${alpha})`); // High Density Red
        grad.addColorStop(0.5, `rgba(245, 158, 11, ${alpha*0.6})`);
      } else {
        grad.addColorStop(0, `rgba(245, 158, 11, ${alpha})`); // Medium Yellow
        grad.addColorStop(0.5, `rgba(16, 185, 129, ${alpha*0.4})`);
      }
      grad.addColorStop(1, 'rgba(16, 185, 129, 0)');

      heatmapCtx.fillStyle = grad;
      heatmapCtx.beginPath();
      heatmapCtx.arc(cx, cy, radius, 0, Math.PI*2);
      heatmapCtx.fill();
    }
  });

  // Highlight Emergency Hotspot
  if (isEmergency && emergencyPos) {
    let grad = heatmapCtx.createRadialGradient(emergencyPos.x, emergencyPos.y, 0, emergencyPos.x, emergencyPos.y, 60);
    grad.addColorStop(0, 'rgba(225, 29, 72, 0.9)');
    grad.addColorStop(1, 'rgba(225, 29, 72, 0)');
    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(emergencyPos.x, emergencyPos.y, 60, 0, Math.PI*2);
    heatmapCtx.fill();
  }
}

/* Simulation Control Handlers */
function toggleSim(){
  simRunning = !simRunning;
  const btn = document.getElementById('btnToggleSim');
  const timer = document.getElementById('simTimer');

  if (simRunning) {
    btn.textContent = '⏸ 시뮬레이션 일시정지';
    btn.style.background = '#e2e8f0';
    timer.textContent = '상태: 실시간 군중 시뮬레이션 연산 중 ▶';
  } else {
    btn.textContent = '▶ 시뮬레이션 시작';
    btn.style.background = '#f1f5f9';
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
    badge.textContent = '🌧️ 기상변수: 강우 발생';
    badge.style.background = '#fef3c7';
    badge.style.color = '#b45309';
  } else {
    btn.classList.remove('active');
    btn.textContent = '🌧️ 우천 모드';
    if(!isEmergency) {
      badge.textContent = '일반 상태';
      badge.style.background = '#eff6ff';
      badge.style.color = '#2563eb';
    }
  }

  if (venueCanvas) {
    drawDetailedOutdoorVenue(venueCanvas.width, venueCanvas.height);
  }
}

function triggerEmergencyEnv(){
  isEmergency = !isEmergency;
  const btn = document.getElementById('btnEmergency');
  const badge = document.getElementById('envBadge');

  if (isEmergency) {
    btn.classList.add('active');
    btn.textContent = '🚨 응급상황 해제';
    badge.textContent = '🚨 긴급변수: 응급환자 발생!';
    badge.style.background = '#fee2e2';
    badge.style.color = '#b91c1c';

    // Set emergency position in crowd area
    const currentBooths = layoutHistory[currentLayoutIndex].booths;
    const w = venueCanvas.width;
    const h = venueCanvas.height;
    emergencyPos = {
      x: currentBooths.expA.x * w + 20,
      y: currentBooths.expA.y * h + 30
    };

    // Auto start simulation to view emergency response
    if(!simRunning) toggleSim();
  } else {
    btn.classList.remove('active');
    btn.textContent = '🚨 응급환자 발생';
    emergencyPos = null;
    medicalAgents = [];
    if(!isRain) {
      badge.textContent = '일반 상태';
      badge.style.background = '#eff6ff';
      badge.style.color = '#2563eb';
    }
  }
}

function sendChat(){
  const val = document.getElementById('chatIn').value;
  if(!val) return;
  const box = document.getElementById('chatBox');
  box.innerHTML += `<div style="color:#1e293b;background:#ffffff;padding:8px;border-radius:8px;margin-bottom:8px;text-align:right;"><b>나:</b> ${val}</div>`;
  document.getElementById('chatIn').value = '';
  
  setTimeout(() => {
    box.innerHTML += `<div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;"><b>AI:</b> "${val}" 요구사항을 분석하여 설계안을 새로 구성했습니다. 상단 '설계 히스토리'에 반영되었습니다.</div>`;
    box.scrollTop = box.scrollHeight;
    
    // Automatically trigger layout rebuild on custom AI chat requests
    runAIGenerate();
  }, 500);
}

window.addEventListener('load', () => {
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=1250, scrolling=True)
