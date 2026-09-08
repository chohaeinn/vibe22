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
.btn-secondary.active{background:#2563eb;color:#fff;border-color:#1d4ed8;}

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
  grid-template-columns: 1.4fr 1fr 1fr;
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
  cursor: grab;
}
.map-wrap:active{cursor: grabbing;}
#venueCanvas, #routeCanvas, #heatmapCanvas, #peopleCanvas{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
}
#routeCanvas{z-index:3;pointer-events:none;}
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
  pointer-events:none;
}
.legend-item{display:flex;align-items:center;gap:5px;font-weight:700;color:#334155;}
.legend-dot{width:8px;height:8px;border-radius:2px;}

/* Controls Bar */
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
        <div class="brand-sub">행사 설계·동선 최적화 시스템</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item" onclick="switchPage('home', this)">
        <span class="nav-icon">🏠</span> 홈 / 정보 입력
      </div>
      <div class="nav-item active" onclick="switchPage('design', this)">
        <span class="nav-icon">📋</span> 행사 설계 & 최적화
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span class="nav-icon">⚙️</span> 설계 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span class="nav-icon">📊</span> 최종 리포트 출력
      </div>
      <div class="nav-item" onclick="switchPage('assistant', this)">
        <span class="nav-icon">🤖</span> AI 수정 어시스턴트
      </div>
    </nav>

    <div class="side-banner">
      <h5>💡 드래그 & 리사이즈 안내</h5>
      <p>배치도에서 부스를 드래그하여 이동하거나 크기를 조절할 수 있습니다.</p>
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
        <h2 id="topTitleText">📋 행사 설계 & 동선 최적화</h2>
        <p id="topSubText">설계도 확인, 동선 최적화, 히트맵 분석 및 AI 실시간 수정이 가능합니다.</p>
      </div>
      <button class="btn-primary" onclick="runAIGenerate()">
        ✦ AI 재배치 및 최적화 실행
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
            <div class="info-box-icon">👥</div>
            <div class="info-box-text"><label>예상 관람객</label><span id="outVisitors">5,000명</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">📐</div>
            <div class="info-box-text"><label>행사장 면적</label><span id="outArea">50,000m²</span></div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-main-grid" style="margin-top:14px;">

        <!-- 1. Digital Twin Canvas Map (Blueprint + Drag & Drop) -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 행사장 설계도 및 동선 편집</span>
            <span class="card-badge" id="layoutBadge">v1.0 AI 설계</span>
          </div>
          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="routeCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>

            <!-- Legend -->
            <div class="map-legend-overlay">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 무대존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 푸드존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 휴식공간</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 안전센터</div>
              <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> 화장실</div>
            </div>
          </div>

          <div class="map-controls-bar">
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              <button class="btn-secondary active" id="btnToggleRoute" onclick="toggleRouteLayer()">
                🛤️ 동선 보기 ON
              </button>
              <button class="btn-secondary active" id="btnToggleHeatmap" onclick="toggleHeatmapLayer()">
                🔥 히트맵 ON
              </button>
              <button class="btn-secondary" id="btnToggleSim" onclick="toggleSim()">
                ▶ 시뮬레이션
              </button>
            </div>
            <span style="font-size:11px;color:#64748b;font-weight:700;" id="simTimer">드래그로 부스 이동 가능</span>
          </div>
        </div>

        <!-- 2. Density Heatmap & Stats -->
        <div class="card-panel">
          <div class="card-head">
            <span>🔥 군중 밀집도 & 시뮬레이션 분석</span>
            <span class="card-badge" id="envBadge">일반 상태</span>
          </div>
          <div class="map-wrap" style="height:360px;">
            <canvas id="heatmapCanvas"></canvas>
          </div>
          <div style="display:flex;justify-content:space-around;font-size:10px;color:#64748b;margin-top:10px;font-weight:700;">
            <span style="color:#10b981;">🟢 원활</span>
            <span style="color:#eab308;">🟡 보통</span>
            <span style="color:#f97316;">🟠 혼잡</span>
            <span style="color:#ef4444;">🔴 위험(병목)</span>
          </div>
        </div>

        <!-- 3. AI Evaluation & Suggestions -->
        <div class="card-panel">
          <div class="card-head">
            <span>💡 AI 최종 평가 결과</span>
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

          <div style="font-size:12px;font-weight:800;color:#0f172a;margin:10px 0 6px 0;">💡 AI 최적화 제안</div>
          <ul class="ai-recom-list" id="aiRecomList">
            <li>공연 무대 전면 피크 시간대 차단봉 추가 설치로 우발 병목 해소</li>
            <li>응급 의료센터를 입구 근처로 이동시켜 비상 접근성 25% 개선</li>
            <li>체험존 주변을 원형으로 배치하여 관람객 이동 흐름 순환</li>
          </ul>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-bottom-grid" style="margin-top:14px;">

        <!-- 1. Before / After Comparison -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚖️ 최적화 전 / 후 비교</span>
          </div>
          <div class="compare-grid">
            <div class="comp-col">
              <h5>최적화 전 (기존)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-red" id="compBeforeBottleneck">68%</span></div>
              <div class="comp-val"><span>안전 접근성</span><span id="compBeforeAccess">65점</span></div>
              <div class="comp-val"><span>사고 위험구역</span><span class="text-red" id="compBeforeRisk">3개소</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#cbd5e1;">→</div>
            <div class="comp-col">
              <h5>AI 최적화 후</h5>
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
            <div class="wf-card"><div class="wf-icon">📋</div><div class="wf-title">정보 입력</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🌐</div><div class="wf-title">디지털 트윈</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🤖</div><div class="wf-title">AI 배치/동선</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">📊</div><div class="wf-title">최종 평가</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">📄</div><div class="wf-title">리포트 출력</div></div>
          </div>
          <div class="wf-sub-tags">
            <span class="wf-tag">요구사항 파악</span>
            <span class="wf-tag">설계도 생성</span>
            <span class="wf-tag">동선 최적화</span>
            <span class="wf-tag">종합 리포트</span>
          </div>
        </div>

        <!-- 3. Report Summary -->
        <div class="card-panel">
          <div class="card-head">
            <span>📄 최종 리포트 요약</span>
          </div>
          <div class="report-sum-box" id="reportSummaryBox">
            AI 분석 결과, <b>2025 힐링 페스티벌</b>은 5,000명의 관람객을 안전하게 수용할 수 있는 최적 구조로 검증되었습니다.
          </div>
          <button class="btn-primary" style="width:100%;justify-content:center;padding:10px;font-size:12px;margin-top:auto;" onclick="openReportModal()">
            📌 최종 상세 보고서 출력 (PDF)
          </button>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS -->
    <section id="pageProcess" class="page-view">
      <div class="form-card">
        <div class="form-section-head">⚙️ AI 행사 공간 설계 및 동선 최적화 메커니즘</div>
        <p style="font-size:13px;line-height:1.7;color:#334155;">
          1. <b>설계도 기반 디지털 트윈:</b> 입력된 행사 정보를 바탕으로 2D 그리드 행사장 가상 공간을 구축합니다.<br>
          2. <b>AI 동선 계산 및 최적화:</b> 관람객 이동 패턴을 분석하여 주출입구와 각 부스(무대, 체험존, 푸드존 등) 간의 최적의 이동 동선을 자동 계산합니다.<br>
          3. <b>인구 밀집도 히트맵 시뮬레이션:</b> 군중 밀집도를 실시간 히트맵으로 시각화하여 병목 현상 발생 가능 구간을 사전에 차단합니다.<br>
          4. <b>드래그 앤 리사이즈 & AI 수정:</b> 사용자가 마우스로 부스를 직접 이동하거나 크기를 조절할 수 있으며, AI 어시스턴트를 통해 실시간 레이아웃 수정이 가능합니다.
        </p>
      </div>
    </section>

    <!-- PAGE 4: ASSISTANT -->
    <section id="pageAssistant" class="page-view">
      <div class="form-card">
        <div class="form-section-head">🤖 AI 실시간 레이아웃 수정 어시스턴트</div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:12px;border-radius:10px;height:220px;overflow-y:auto;font-size:12px;margin-bottom:12px;" id="chatBox">
          <div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;">
            AI: 안녕하세요 추천님! "무대를 오른쪽으로 옮겨줘", "응급센터 크기를 늘려줘" 등 요구사항을 말씀하시면 설계도와 동선을 즉시 재최적화해 드립니다.
          </div>
        </div>
        <div style="display:flex;gap:8px;">
          <input type="text" id="chatIn" placeholder="요구사항을 입력하세요... (예: 푸드존 위치를 왼쪽으로 변경해줘)" style="flex:1;padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;" onkeypress="if(event.key==='Enter')sendChat()">
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
          본 보고서는 <b>2025 힐링 페스티벌</b> (야외 잔디 광장 50,000m², 예상 관람객 5,000명)의 동선 및 안전 최적화를 위해 생성되었습니다. AI 시뮬레이션 결과 종합 안전성 점수 <b>92점</b>, 동선 효율성 <b>87점</b>을 기록하였습니다.
        </p>
      </div>

      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">2. 구역별 세부 설비 지침 및 동선 최적화</h4>
        <ul style="font-size:12px;color:#334155;line-height:1.7;padding-left:18px;">
          <li><b>메인 무대:</b> 중앙 상단 배치, 전면 관람 구역 통로 폭 4m 확보 및 최적 동선 연결.</li>
          <li><b>응급 의료 센터:</b> 주출입구 인근 전진 배치로 골든타임 확보.</li>
          <li><b>푸드 존 및 체험 존:</b> 군중 밀집도 분산을 위한 원형 배치 구조 적용.</li>
        </ul>
      </div>
    </div>

    <div style="margin-top:16px;display:flex;justify-content:flex-end;gap:10px;">
      <button style="padding:10px 16px;background:#e2e8f0;border:none;border-radius:8px;font-weight:700;font-size:12px;" onclick="closeReportModal()">닫기</button>
      <button class="btn-primary" onclick="alert('최종 보고서가 PDF 파일로 출력되었습니다.');closeReportModal();">PDF 다운로드</button>
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
    t.textContent = '🏠 정보 입력';
    s.textContent = '행사 기본 정보 및 요구사항을 입력하세요.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    t.textContent = '📋 행사 설계 & 동선 최적화';
    s.textContent = '설계도 확인, 동선 최적화, 히트맵 분석 및 AI 실시간 수정이 가능합니다.';
    setTimeout(initCanvases, 50);
  } else if(pageId === 'process'){
    document.getElementById('pageProcess').classList.add('active');
    t.textContent = '⚙️ 설계 프로세스';
    s.textContent = 'AI 분석 및 자동 배치 알고리즘 메커니즘입니다.';
  } else if(pageId === 'assistant'){
    document.getElementById('pageAssistant').classList.add('active');
    t.textContent = '🤖 AI 수정 어시스턴트';
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
      "체험존 주변을 원형으로 배치하여 관람객 이동 흐름 순환"
    ],
    comp: { beforeBtn: "68%", beforeAcc: "65점", beforeRisk: "3개소", afterBtn: "18%", afterAcc: "96젝", afterRisk: "0개소" }
  },
  {
    versionName: "v2.0 - 동선 최적화 집중안",
    timestamp: "신규 생성",
    booths: {
      stage: {x: 0.35, y: 0.08, bw: 0.30, bh: 0.18, title: '메인 대형무대', color: '#8b5cf6', icon: '🎪'},
      expA: {x: 0.08, y: 0.25, bw: 0.20, bh: 0.14, title: '체험존 돔', color: '#3b82f6', icon: '🧪'},
      expB: {x: 0.72, y: 0.25, bw: 0.20, bh: 0.14, title: '휴식/안내존', color: '#10b981', icon: '☂️'},
      food: {x: 0.08, y: 0.52, bw: 0.20, bh: 0.15, title: '푸드트럭 구역', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.42, y: 0.72, bw: 0.16, bh: 0.14, title: '응급 센터(중앙)', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.75, y: 0.72, bw: 0.16, bh: 0.12, title: '화장실/편의', color: '#06b6d4', icon: '🚻'}
    },
    scores: { safety: 98, flow: 93, access: 95, cong: 91, space: 89 },
    recoms: [
      "주출입구와 중앙 사거리 간의 동선 폭을 6m로 확장하여 병목 현상 제거",
      "응급 의료센터를 동선 중심부에 배치하여 골든타임 단축",
      "푸드존과 체험존 간 이격 거리 확보"
    ],
    comp: { beforeBtn: "60%", beforeAcc: "70점", beforeRisk: "2개소", afterBtn: "12%", afterAcc: "98점", afterRisk: "0개소" }
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

  document.getElementById('scSafety').textContent = layout.scores.safety + '점';
  document.getElementById('scFlow').textContent = layout.scores.flow + '점';
  document.getElementById('scAccess').textContent = layout.scores.access + '점';
  document.getElementById('scCong').textContent = layout.scores.cong + '점';
  document.getElementById('scSpace').textContent = layout.scores.space + '점';

  const recomUl = document.getElementById('aiRecomList');
  recomUl.innerHTML = '';
  layout.recoms.forEach(r => {
    const li = document.createElement('li');
    li.textContent = r;
    recomUl.appendChild(li);
  });

  if (venueCanvas) {
    redrawAllCanvases();
  }
}

function runAIGenerate(){
  initLayoutHistory();
  const nextPresetIndex = layoutHistory.length % layoutPresets.length;
  const newLayout = JSON.parse(JSON.stringify(layoutPresets[nextPresetIndex]));

  const d = new Date();
  const timeStr = `${d.getHours()}:${d.getMinutes()<10?'0':''}${d.getMinutes()}:${d.getSeconds()<10?'0':''}${d.getSeconds()}`;
  newLayout.versionName = `v${layoutHistory.length + 1}.0 - AI 최적화 재배치`;
  newLayout.timestamp = timeStr;

  layoutHistory.push(newLayout);
  currentLayoutIndex = layoutHistory.length - 1;

  updateHistorySelectUI();
  loadSelectedHistory(currentLayoutIndex);
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
  alert(`✨ AI가 새로운 행사장 설계 및 동선 최적화를 완료했습니다!`);
}

/* Canvas & Interactive Drag/Resize Engine */
let venueCanvas, venueCtx;
let routeCanvas, routeCtx;
let heatmapCanvas, heatmapCtx;
let peopleCanvas, peopleCtx;

let showRoute = true;
let showHeatmap = true;
let simRunning = false;
let animFrameId = null;

let selectedBoothKey = null;
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;

let people = [];

function initCanvases(){
  initLayoutHistory();

  venueCanvas = document.getElementById('venueCanvas');
  routeCanvas = document.getElementById('routeCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');
  peopleCanvas = document.getElementById('peopleCanvas');

  if(!venueCanvas) return;

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth;
  const h = wrap.clientHeight;

  [venueCanvas, routeCanvas, heatmapCanvas, peopleCanvas].forEach(c => {
    c.width = w;
    c.height = h;
  });

  venueCtx = venueCanvas.getContext('2d');
  routeCtx = routeCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');
  peopleCtx = peopleCanvas.getContext('2d');

  initPeople(w, h);
  setupCanvasInteraction(w, h);
  redrawAllCanvases();

  if (!animFrameId) {
    renderLoop();
  }
}

function initPeople(w, h){
  people = [];
  for(let i=0; i<60; i++){
    people.push({
      x: w*0.2 + Math.random()*w*0.6,
      y: h*0.2 + Math.random()*h*0.6,
      vx: (Math.random()-0.5)*1.2,
      vy: (Math.random()-0.5)*1.2
    });
  }
}

/* Toggle Systems for Route & Heatmap */
function toggleRouteLayer(){
  showRoute = !showRoute;
  const btn = document.getElementById('btnToggleRoute');
  if(showRoute){
    btn.classList.add('active');
    btn.textContent = '🛤️ 동선 보기 ON';
  } else {
    btn.classList.remove('active');
    btn.textContent = '🛤️ 동선 보기 OFF';
  }
  redrawAllCanvases();
}

function toggleHeatmapLayer(){
  showHeatmap = !showHeatmap;
  const btn = document.getElementById('btnToggleHeatmap');
  const hmCanvas = document.getElementById('heatmapCanvas');
  if(showHeatmap){
    btn.classList.add('active');
    btn.textContent = '🔥 히트맵 ON';
    hmCanvas.style.display = 'block';
  } else {
    btn.classList.remove('active');
    btn.textContent = '🔥 히트맵 OFF';
    hmCanvas.style.display = 'none';
  }
}

function toggleSim(){
  simRunning = !simRunning;
  const btn = document.getElementById('btnToggleSim');
  btn.textContent = simRunning ? '⏸ 시뮬레이션 일시정지' : '▶ 시뮬레이션';
  btn.style.background = simRunning ? '#e2e8f0' : '#f1f5f9';
}

/* Mouse Interaction: Drag & Resize Booths */
function setupCanvasInteraction(w, h){
  venueCanvas.onmousedown = (e) => {
    const rect = venueCanvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const currentBooths = layoutHistory[currentLayoutIndex].booths;
    selectedBoothKey = null;

    Object.keys(currentBooths).forEach(key => {
      const b = currentBooths[key];
      const bx = b.x * w, by = b.y * h, bw = b.bw * w, bh = b.bh * h;
      if (mouseX >= bx && mouseX <= bx + bw && mouseY >= by && mouseY <= by + bh) {
        selectedBoothKey = key;
        isDragging = true;
        dragStartX = mouseX - bx;
        dragStartY = mouseY - by;
      }
    });
    redrawAllCanvases();
  };

  venueCanvas.onmousemove = (e) => {
    if (!isDragging || !selectedBoothKey) return;
    const rect = venueCanvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const currentBooths = layoutHistory[currentLayoutIndex].booths;
    const b = currentBooths[selectedBoothKey];

    // Update booth position with drag offset
    b.x = Math.max(0.02, Math.min(0.8, (mouseX - dragStartX) / w));
    b.y = Math.max(0.02, Math.min(0.8, (mouseY - dragStartY) / h));

    redrawAllCanvases();
  };

  window.onmouseup = () => {
    isDragging = false;
  };
}

function redrawAllCanvases(){
  if(!venueCanvas) return;
  const w = venueCanvas.width;
  const h = venueCanvas.height;

  drawBlueprint(w, h);
  drawRouteOverlay(w, h);
  drawHeatmap(w, h);
}

function drawBlueprint(w, h){
  if(!venueCtx) return;
  venueCtx.clearRect(0, 0, w, h);

  // Grass Background
  venueCtx.fillStyle = '#3a7d44';
  venueCtx.fillRect(0, 0, w, h);

  // Pathways
  venueCtx.strokeStyle = '#e2d9c8';
  venueCtx.lineWidth = 26;
  venueCtx.lineCap = 'round';
  venueCtx.beginPath();
  venueCtx.moveTo(w*0.5, h*0.9);
  venueCtx.lineTo(w*0.5, h*0.5);
  venueCtx.stroke();

  venueCtx.beginPath();
  venueCtx.ellipse(w*0.5, h*0.48, w*0.35, h*0.28, 0, 0, Math.PI*2);
  venueCtx.stroke();

  // Draw Booths from Current Layout
  const currentBooths = layoutHistory[currentLayoutIndex].booths;
  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    const bx = b.x * w, by = b.y * h, bw = b.bw * w, bh = b.bh * h;

    // Shadow
    venueCtx.fillStyle = 'rgba(0,0,0,0.3)';
    venueCtx.fillRect(bx+3, by+3, bw, bh);

    // Booth Body
    venueCtx.fillStyle = b.color;
    venueCtx.beginPath();
    venueCtx.roundRect(bx, by, bw, bh, 6);
    venueCtx.fill();

    // Selection border if selected
    if (selectedBoothKey === key) {
      venueCtx.strokeStyle = '#ffffff';
      venueCtx.lineWidth = 3;
    } else {
      venueCtx.strokeStyle = 'rgba(255,255,255,0.7)';
      venueCtx.lineWidth = 1.5;
    }
    venueCtx.stroke();

    // Title Text
    venueCtx.fillStyle = '#ffffff';
    venueCtx.font = 'bold 10.5px Pretendard, sans-serif';
    venueCtx.textAlign = 'center';
    venueCtx.fillText(`${b.icon} ${b.title}`, bx + bw/2, by + bh/2 + 4);
  });

  // Main Gate
  venueCtx.fillStyle = '#1e293b';
  venueCtx.fillRect(w*0.42, h*0.88, w*0.16, h*0.08);
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 10px Pretendard, sans-serif';
  venueCtx.fillText('🚪 주출입구', w*0.5, h*0.93);
}

function drawRouteOverlay(w, h){
  if(!routeCtx) return;
  routeCtx.clearRect(0, 0, w, h);
  if(!showRoute) return;

  const currentBooths = layoutHistory[currentLayoutIndex].booths;
  const gateX = w*0.5, gateY = h*0.9;

  routeCtx.strokeStyle = 'rgba(59, 130, 246, 0.8)';
  routeCtx.lineWidth = 3;
  routeCtx.setLineDash([6, 4]);

  // Draw optimal routes connecting gate to main booths
  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    const bx = b.x * w + b.bw * w * 0.5;
    const by = b.y * h + b.bh * h * 0.5;

    routeCtx.beginPath();
    routeCtx.moveTo(gateX, gateY);
    routeCtx.lineTo(bx, by);
    routeCtx.stroke();
  });
  routeCtx.setLineDash([]);
}

function drawHeatmap(w, h){
  if(!heatmapCtx) return;
  heatmapCtx.clearRect(0, 0, w, h);
  if(!showHeatmap) return;

  // Simple dynamic heatmap clusters around booths
  const currentBooths = layoutHistory[currentLayoutIndex].booths;
  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    const bx = b.x * w + b.bw * w * 0.5;
    const by = b.y * h + b.bh * h * 0.5;

    let grad = heatmapCtx.createRadialGradient(bx, by, 5, bx, by, 70);
    grad.addColorStop(0, 'rgba(239, 68, 68, 0.5)'); // High density near booths
    grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.3)');
    grad.addColorStop(1, 'rgba(16, 185, 129, 0)');

    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(bx, by, 70, 0, Math.PI*2);
    heatmapCtx.fill();
  });

  // Animated simulation particles
  if (simRunning && peopleCanvas) {
    peopleCtx.clearRect(0, 0, w, h);
    people.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      if(p.x < 10 || p.x > w-10) p.vx *= -1;
      if(p.y < 10 || p.y > h-10) p.vy *= -1;

      peopleCtx.fillStyle = '#ffffff';
      peopleCtx.beginPath();
      peopleCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
      peopleCtx.fill();
    });
  }
}

function renderLoop(){
  if (simRunning) {
    redrawAllCanvases();
  }
  animFrameId = requestAnimationFrame(renderLoop);
}

function sendChat(){
  const val = document.getElementById('chatIn').value;
  if(!val) return;
  const box = document.getElementById('chatBox');
  box.innerHTML += `<div style="color:#1e293b;background:#ffffff;padding:8px;border-radius:8px;margin-bottom:8px;text-align:right;"><b>나:</b> ${val}</div>`;
  document.getElementById('chatIn').value = '';
  
  setTimeout(() => {
    box.innerHTML += `<div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;"><b>AI:</b> "${val}" 반영하여 동선과 배치를 성공적으로 재최적화했습니다.</div>`;
    box.scrollTop = box.scrollHeight;
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
