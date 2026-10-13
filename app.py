import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 오늘의집 스타일 행사장 종합 스튜디오",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_STUDIO_ULTIMATE_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI - Ultimate Studio</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<!-- Three.js Library for 3D View -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color:#1e293b;
  background:#f8fafc;
  overflow:hidden;
}
button,input,select,textarea{font:inherit;}
button{cursor:pointer;transition:all 0.2s ease;}

::-webkit-scrollbar {width:6px;height:6px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}

.app-container{
  display:flex;
  height:100vh;
  width:100vw;
  background:#f1f5f9;
}

/* Left Sidebar: Navigation & Catalog */
.left-sidebar{
  width:260px;
  background:#0f172a;
  color:#94a3b8;
  padding:16px;
  display:flex;
  flex-direction:column;
  gap:14px;
  border-right:1px solid #1e293b;
  flex-shrink:0;
  z-index:30;
  overflow-y:auto;
}
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  color:#fff;
  padding-bottom:12px;
  border-bottom:1px solid #1e293b;
}
.brand-icon{
  width:34px;height:34px;
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:10px;
  display:grid;place-items:center;
  font-weight:900;color:#fff;
  box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.brand-title{font-size:16px;font-weight:800;color:#fff;}
.brand-sub{font-size:10px;color:#64748b;}

.nav-group{display:flex;flex-direction:column;gap:4px;}
.nav-item{
  display:flex;align-items:center;gap:10px;
  padding:10px 12px;border-radius:8px;
  font-size:13px;font-weight:600;color:#94a3b8;cursor:pointer;
}
.nav-item:hover{background:rgba(255,255,255,0.05);color:#f1f5f9;}
.nav-item.active{background:linear-gradient(135deg,#2563eb,#3b82f6);color:#fff;}

.catalog-section-title{
  font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;margin:6px 0 4px 0;letter-spacing:0.5px;
}
.catalog-grid{
  display:grid;
  grid-template-columns:repeat(2, 1fr);
  gap:6px;
}
.catalog-item{
  background:#1e293b;
  border:1px solid #334155;
  border-radius:8px;
  padding:8px;
  text-align:center;
  cursor:pointer;
  color:#f8fafc;
  font-size:11.5px;
  font-weight:700;
  display:flex;
  flex-direction:column;
  gap:3px;
}
.catalog-item:hover{background:#2563eb;border-color:#3b82f6;}
.catalog-item span{font-size:16px;}

/* Main Workspace */
.main-workspace{
  flex:1;
  display:flex;
  flex-direction:column;
  position:relative;
  overflow-y:auto;
  padding:16px;
  gap:12px;
}

.top-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  background:#ffffff;
  padding:12px 20px;
  border-radius:14px;
  border:1px solid #e2e8f0;
  box-shadow:0 2px 6px rgba(0,0,0,0.02);
}
.top-title h2{font-size:17px;font-weight:800;color:#0f172a;}
.top-title p{font-size:11.5px;color:#64748b;margin-top:1px;}

.mode-toggle-group{
  display:flex;gap:4px;background:#f1f5f9;padding:4px;border-radius:10px;border:1px solid #cbd5e1;
}
.mode-btn{
  background:transparent;border:none;padding:6px 12px;border-radius:8px;font-size:11.5px;font-weight:700;color:#64748b;cursor:pointer;
}
.mode-btn.active{background:#ffffff;color:#2563eb;box-shadow:0 2px 6px rgba(0,0,0,0.05);}

/* Dashboard Grids */
.dashboard-grid{
  display:grid;
  grid-template-columns: 1.6fr 1fr;
  gap:12px;
}
.card-panel{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:14px;
  padding:14px;
  box-shadow:0 2px 6px rgba(0,0,0,0.02);
  display:flex;
  flex-direction:column;
}
.card-head{
  font-size:13px;font-weight:800;color:#0f172a;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;
}
.card-badge{
  font-size:10px;background:#eff6ff;color:#2563eb;padding:2px 8px;border-radius:10px;font-weight:700;
}

/* Canvas Wrap */
.map-wrap{
  position:relative;
  width:100%;
  height:330px;
  background:#1e293b;
  border-radius:10px;
  overflow:hidden;
  border:1px solid #334155;
}
#floorCanvas, #peopleCanvas, #heatmapCanvas, #container3D{
  position:absolute;inset:0;width:100%;height:100%;
}
#heatmapCanvas{z-index:5;opacity:0.85;pointer-events:none;}
#peopleCanvas{z-index:10;pointer-events:none;}
#container3D{z-index:15;display:none;background:#0f172a;}

/* Sub Toolbar */
.sub-toolbar{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:12px;
  padding:10px 14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  flex-wrap:wrap;
}
.timeline-slider{accent-color:#2563eb;cursor:pointer;flex:1;max-width:220px;}
.time-badge{background:#2563eb;color:#fff;font-weight:800;font-size:11.5px;padding:3px 8px;border-radius:12px;}

.btn-primary{
  background:linear-gradient(135deg, #2563eb, #1d4ed8);
  color:#ffffff;border:none;padding:8px 16px;border-radius:10px;font-weight:800;font-size:12px;
  box-shadow:0 4px 12px rgba(37,99,235,0.3);
}
.btn-secondary{
  background:#f1f5f9;color:#334155;border:1px solid #cbd5e1;padding:5px 10px;border-radius:8px;font-size:11px;font-weight:700;
}
.btn-warning{background:#fef3c7;color:#b45309;border:1px solid #fde68a;padding:5px 10px;border-radius:8px;font-size:11px;font-weight:700;}
.btn-warning.active{background:#f59e0b;color:#fff;}
.btn-danger{background:#fee2e2;color:#b91c1c;border:1px solid #fca5a5;padding:5px 10px;border-radius:8px;font-size:11px;font-weight:700;}
.btn-danger.active{background:#ef4444;color:#fff;}

/* Right Inspector Sidebar */
.right-sidebar{
  width:260px;
  background:#ffffff;
  border-left:1px solid #e2e8f0;
  padding:16px;
  display:flex;
  flex-direction:column;
  gap:12px;
  flex-shrink:0;
  z-index:30;
  box-shadow:-2px 0 10px rgba(0,0,0,0.02);
  overflow-y:auto;
}
.inspector-title{font-size:13px;font-weight:800;color:#0f172a;border-bottom:2px solid #f1f5f9;padding-bottom:6px;}
.prop-group{display:flex;flex-direction:column;gap:4px;margin-bottom:8px;}
.prop-group label{font-size:10.5px;font-weight:700;color:#64748b;}
.prop-group input, .prop-group select, .prop-group textarea{
  padding:6px 8px;border:1px solid #cbd5e1;border-radius:8px;font-size:11.5px;font-weight:600;background:#f8fafc;color:#0f172a;outline:none;
}

/* Modals */
.modal-bg{
  position:fixed;inset:0;background:rgba(15,23,42,0.65);backdrop-filter:blur(4px);z-index:999;display:none;place-items:center;padding:20px;
}
.modal-bg.active{display:grid;}
.modal-content{background:#fff;width:min(90%, 750px);max-height:85vh;border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:14px;overflow-y:auto;}
.form-grid{display:grid;grid-template-columns:repeat(2, 1fr);gap:10px;}
</style>
</head>
<body>

<div class="app-container">

  <!-- LEFT SIDEBAR: NAV & CATALOG -->
  <aside class="left-sidebar">
    <div class="brand">
      <div class="brand-icon">🎪</div>
      <div>
        <div class="brand-title">Event Studio</div>
        <div class="brand-sub">오늘의집 스타일 행사장 설계</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item active"><span>📋</span>행사 설계 대시보드</div>
      <div class="nav-item" onclick="openConditionModal()"><span>⚙️</span>행사 조건 상세 설정</div>
      <div class="nav-item" onclick="openReportModal()"><span>📊</span>종합 분석 리포트</div>
    </nav>

    <div>
      <div class="catalog-section-title">시설물 카탈로그 (클릭 추가)</div>
      <div class="catalog-grid">
        <div class="catalog-item" onclick="addCatalogObject('stage')"><span>🎭</span>메인무대</div>
        <div class="catalog-item" onclick="addCatalogObject('exp')"><span>🧪</span>체험부스</div>
        <div class="catalog-item" onclick="addCatalogObject('food')"><span>🍔</span>푸드트럭</div>
        <div class="catalog-item" onclick="addCatalogObject('rest')"><span>🌳</span>잔디휴식존</div>
        <div class="catalog-item" onclick="addCatalogObject('medical')"><span>🏥</span>응급센터</div>
        <div class="catalog-item" onclick="addCatalogObject('restroom')"><span>🚻</span>화장실</div>
      </div>
    </div>

    <div style="margin-top:auto;background:rgba(255,255,255,0.05);padding:10px;border-radius:10px;font-size:10.5px;line-height:1.4;color:#94a3b8;">
      💡 <b>사용 방법:</b><br>
      • 상단 <b>[행사 조건 상세 설정]</b>에서 조건 변경 가능<br>
      • 카탈로그 클릭 시 캔버스 중앙에 부스 배치<br>
      • 캔버스에서 드래그하여 자유로운 위치 조정
    </div>
  </aside>

  <!-- MAIN WORKSPACE -->
  <main class="main-workspace">
    <header class="top-header">
      <div class="top-title">
        <h2 id="headerEventName">2025 힐링 페스티벌 행사장 설계</h2>
        <p id="headerEventSub">야외 잔디 광장 (50,000m²) · 예상 관람객 5,000명</p>
      </div>
      <div class="mode-toggle-group">
        <button class="mode-btn active" id="btn2D" onclick="switchMode('2d')">2D 도면 편집</button>
        <button class="mode-btn" id="btn3D" onclick="switchMode('3d')">3D 입체 뷰</button>
      </div>
    </header>

    <!-- Sub Toolbar: Timeline & Modes -->
    <div class="sub-toolbar">
      <div style="display:flex;align-items:center;gap:10px;flex:1;">
        <span style="font-size:11.5px;font-weight:800;">⏰ 시간 시뮬:</span>
        <button class="btn-secondary" id="btnTimelinePlay" onclick="toggleTimelinePlay()">▶ 재생</button>
        <input type="range" id="timeSlider" class="timeline-slider" min="10" max="20" step="1" value="14" oninput="updateTimeSimulation(this.value)">
        <div class="time-badge" id="timeDisplay">14:00</div>
      </div>
      <div style="display:flex;gap:6px;">
        <button class="btn-warning" id="btnRain" onclick="toggleRainEnv()">🌧️ 우천모드</button>
        <button class="btn-danger" id="btnEmergency" onclick="triggerEmergencyEnv()">🚨 응급후송</button>
      </div>
    </div>

    <!-- Main Canvas Grid -->
    <div class="dashboard-grid">
      <!-- 2D & 3D Canvas Panel -->
      <div class="card-panel">
        <div class="card-head">
          <span>🗺️ 행사장 디지털 트윈 캔버스</span>
          <span class="card-badge" id="canvasStatusBadge">편집 모드 활성</span>
        </div>
        <div class="map-wrap" id="mapWrap">
          <canvas id="floorCanvas"></canvas>
          <canvas id="peopleCanvas"></canvas>
          <canvas id="heatmapCanvas"></canvas>
          <div id="container3D"></div>
        </div>
      </div>

      <!-- Quick Analysis & Summary Panel -->
      <div class="card-panel">
        <div class="card-head">
          <span>📈 실시간 분석 요약</span>
          <span class="card-badge" style="background:#dcfce7;color:#15803d;">안전도 최적</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;font-size:12px;color:#334155;line-height:1.6;flex:1;">
          <div style="background:#f8fafc;padding:10px;border-radius:10px;border:1px solid #e2e8f0;">
            <b>• 행사 유형:</b> <span id="summaryVenueType" style="color:#2563eb;font-weight:700;">야외 잔디 광장</span>
          </div>
          <div style="background:#f8fafc;padding:10px;border-radius:10px;border:1px solid #e2e8f0;">
            <b>• 병목 발생 예측율:</b> <span style="color:#10b981;font-weight:800;">14% (매우 낮음)</span>
          </div>
          <div style="background:#f8fafc;padding:10px;border-radius:10px;border:1px solid #e2e8f0;">
            <b>• 응급 이송 골든타임:</b> <span style="color:#2563eb;font-weight:800;">1분 12초 확보</span>
          </div>
          <div style="background:#f8fafc;padding:10px;border-radius:10px;border:1px solid #e2e8f0;">
            <b>• 배치된 시설물 수:</b> <span id="totalObjCount" style="font-weight:800;">6개</span>
          </div>
        </div>
        <button class="btn-primary" style="width:100%;text-align:center;margin-top:auto;" onclick="openReportModal()">
          📌 상세 종합 보고서 보기
        </button>
      </div>
    </div>
  </main>

  <!-- RIGHT INSPECTOR SIDEBAR -->
  <aside class="right-sidebar">
    <div class="inspector-title">⚙️ 속성 인스펙터</div>
    <div id="inspectorContent" style="display:flex;flex-direction:column;gap:8px;">
      <p style="font-size:11.5px;color:#64748b;text-align:center;margin-top:50px;">선택된 시설물이 없습니다.<br>도면에서 시설물을 클릭하세요.</p>
    </div>
    <button class="btn-primary" style="margin-top:auto;" onclick="alert('설계안이 저장되었습니다!')">설계안 저장</button>
  </aside>

</div>

<!-- EVENT CONDITION SETTINGS MODAL -->
<div class="modal-bg" id="conditionModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
      <h3 style="font-size:16px;font-weight:800;">⚙️ 행사 조건 상세 설정</h3>
      <button onclick="closeConditionModal()" style="border:none;background:none;font-size:18px;font-weight:800;">✕</button>
    </div>
    <div class="form-grid">
      <div class="prop-group">
        <label>📌 행사명</label>
        <input type="text" id="inEventName" value="2025 힐링 페스티벌">
      </div>
      <div class="prop-group">
        <label>🏞️ 행사장 유형</label>
        <select id="inVenueType">
          <option value="야외 잔디 광장" selected>야외 잔디 광장</option>
          <option value="실내 컨벤션 홀">실내 컨벤션 홀</option>
          <option value="실내 체육관">실내 체육관</option>
          <option value="도심 스트리트/광장">도심 스트리트/광장</option>
        </select>
      </div>
      <div class="prop-group">
        <label>👥 예상 관람객 수</label>
        <select id="inVisitors">
          <option value="1,000명">1,000명</option>
          <option value="3,000명">3,000명</option>
          <option value="5,000명" selected>5,000명</option>
          <option value="10,000명 이상">10,000명 이상</option>
        </select>
      </div>
      <div class="prop-group">
        <label>📐 행사장 면적</label>
        <input type="text" id="inArea" value="50,000m²">
      </div>
      <div class="prop-group">
        <label>⏰ 운영 시간</label>
        <input type="text" id="inTime" value="10시 - 20시">
      </div>
      <div class="prop-group">
        <label>💰 예산 규모</label>
        <input type="text" id="inBudget" value="5,000만원">
      </div>
      <div class="prop-group" style="grid-column: 1 / -1;">
        <label>💬 AI 배치 세부 프롬프트 / 요구사항</label>
        <textarea id="inPrompt" rows="2" style="width:100%;">메인 무대는 상단에 배치하고, 푸드트럭과 체험 부스를 원형 광장 주변으로 배치해주세요.</textarea>
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:10px;">
      <button class="btn-secondary" onclick="closeConditionModal()">취소</button>
      <button class="btn-primary" onclick="saveEventConditions()">조건 적용하기</button>
    </div>
  </div>
</div>

<!-- REPORT MODAL -->
<div class="modal-bg" id="reportModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e2e8f0;padding-bottom:8px;">
      <h3 style="font-size:16px;font-weight:800;">📊 행사장 설계 및 동선 분석 종합 보고서</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:18px;font-weight:800;">✕</button>
    </div>
    <p style="font-size:12px;line-height:1.6;color:#334155;" id="reportDesc">
      본 보고서는 오늘의집 스타일 인터페이스로 구성된 <b>2025 힐링 페스티벌</b>(야외 잔디 광장 50,000m², 예상 관람객 5,000명)의 구역 배치와 실시간 군중 시뮬레이션 결과입니다.
    </p>
    <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:10px;">
      <button class="btn-secondary" onclick="closeReportModal()">닫기</button>
      <button class="btn-primary" onclick="alert('PDF 다운로드가 완료되었습니다.');closeReportModal();">PDF 다운로드</button>
    </div>
  </div>
</div>

<script>
/* APPLICATION STATE & OBJECTS */
let objects = [
  { id: 1, type: 'stage', title: '메인 무대 & 객석', x: 220, y: 30, w: 200, h: 90, color: '#8b5cf6', icon: '🎭' },
  { id: 2, type: 'exp', title: '체험 부스 A', x: 40, y: 150, w: 120, h: 80, color: '#3b82f6', icon: '🧪' },
  { id: 3, type: 'exp', title: '체험 부스 B', x: 480, y: 150, w: 120, h: 80, color: '#3b82f6', icon: '🚀' },
  { id: 4, type: 'food', title: '푸드트럭 구역', x: 40, y: 260, w: 130, h: 80, color: '#f59e0b', icon: '🍔' },
  { id: 5, type: 'medical', title: '응급 의료센터', x: 480, y: 260, w: 120, h: 80, color: '#ef4444', icon: '🏥' },
  { id: 6, type: 'rest', title: '잔디 휴식광장', x: 240, y: 160, w: 160, h: 100, color: '#10b981', icon: '🌳' }
];

let selectedId = null;
let isDragging = false;
let dragOffsetX = 0;
let dragOffsetY = 0;

let currentMode = '2d';
let simRunning = true;
let isRain = false;
let isEmergency = false;
let emergencyPos = null;

let floorCanvas, floorCtx, peopleCanvas, peopleCtx, heatmapCanvas, heatmapCtx;
let crowdAgents = [];
let raindrops = [];

window.addEventListener('load', () => {
  floorCanvas = document.getElementById('floorCanvas');
  peopleCanvas = document.getElementById('peopleCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');

  floorCtx = floorCanvas.getContext('2d');
  peopleCtx = peopleCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');

  resizeCanvases();
  window.addEventListener('resize', resizeCanvases);

  initCrowd();
  initRain();
  setupEvents();
  renderLoop();
});

function resizeCanvases() {
  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth;
  const h = wrap.clientHeight;
  [floorCanvas, peopleCanvas, heatmapCanvas].forEach(c => {
    c.width = w;
    c.height = h;
  });
  redraw2D();
}

/* EVENT CONDITION MODAL */
function openConditionModal() { document.getElementById('conditionModal').classList.add('active'); }
function closeConditionModal() { document.getElementById('conditionModal').classList.remove('active'); }

function saveEventConditions() {
  const name = document.getElementById('inEventName').value;
  const vType = document.getElementById('inVenueType').value;
  const visitors = document.getElementById('inVisitors').value;
  const area = document.getElementById('inArea').value;

  document.getElementById('headerEventName').textContent = name;
  document.getElementById('headerEventSub').textContent = `${vType} (${area}) · 예상 관람객 ${visitors}`;
  document.getElementById('summaryVenueType').textContent = vType;
  document.getElementById('reportDesc').innerHTML = `본 보고서는 오늘의집 스타일 인터페이스로 구성된 <b>${name}</b>(${vType} ${area}, 예상 관람객 ${visitors})의 구역 배치와 실시간 군중 시뮬레이션 결과입니다.`;

  closeConditionModal();
  alert('행사 조건이 성공적으로 반영되었습니다!');
}

/* CATALOG ADD */
function addCatalogObject(type) {
  const meta = {
    stage: { title: '대형 무대', w: 180, h: 85, color: '#8b5cf6', icon: '🎭' },
    exp: { title: '신규 체험부스', w: 110, h: 75, color: '#3b82f6', icon: '🧪' },
    food: { title: '푸드트럭', w: 120, h: 75, color: '#f59e0b', icon: '🍔' },
    rest: { title: '휴식존', w: 140, h: 90, color: '#10b981', icon: '🌳' },
    medical: { title: '응급센터', w: 110, h: 75, color: '#ef4444', icon: '🏥' },
    restroom: { title: '화장실', w: 100, h: 70, color: '#06b6d4', icon: '🚻' }
  }[type];

  const newItem = {
    id: Date.now(),
    type: type,
    title: meta.title,
    x: floorCanvas.width / 2 - meta.w / 2,
    y: floorCanvas.height / 2 - meta.h / 2,
    w: meta.w,
    h: meta.h,
    color: meta.color,
    icon: meta.icon
  };

  objects.push(newItem);
  selectedId = newItem.id;
  updateInspector();
  redraw2D();
  document.getElementById('totalObjCount').textContent = objects.length + '개';
}

/* 2D RENDERING */
function redraw2D() {
  if (!floorCtx) return;
  const w = floorCanvas.width;
  const h = floorCanvas.height;

  floorCtx.fillStyle = isRain ? '#254e2b' : '#3a7d44';
  floorCtx.fillRect(0, 0, w, h);

  // Grid
  floorCtx.strokeStyle = 'rgba(255,255,255,0.06)';
  floorCtx.lineWidth = 1;
  for(let x=0; x<w; x+=35){
    floorCtx.beginPath(); floorCtx.moveTo(x, 0); floorCtx.lineTo(x, h); floorCtx.stroke();
  }
  for(let y=0; y<h; y+=35){
    floorCtx.beginPath(); floorCtx.moveTo(0, y); floorCtx.lineTo(w, y); floorCtx.stroke();
  }

  // Draw Objects
  objects.forEach(obj => {
    floorCtx.fillStyle = 'rgba(0,0,0,0.3)';
    floorCtx.fillRect(obj.x + 3, obj.y + 3, obj.w, obj.h);

    floorCtx.fillStyle = obj.color;
    floorCtx.beginPath();
    floorCtx.roundRect(obj.x, obj.y, obj.w, obj.h, 8);
    floorCtx.fill();

    floorCtx.strokeStyle = (selectedId === obj.id) ? '#ffffff' : 'rgba(255,255,255,0.6)';
    floorCtx.lineWidth = (selectedId === obj.id) ? 3 : 1.5;
    floorCtx.stroke();

    floorCtx.fillStyle = '#ffffff';
    floorCtx.font = 'bold 11.5px Pretendard, sans-serif';
    floorCtx.textAlign = 'center';
    floorCtx.textBaseline = 'middle';
    floorCtx.fillText(`${obj.icon} ${obj.title}`, obj.x + obj.w / 2, obj.y + obj.h / 2);
  });
}

/* MOUSE EVENTS & DRAGGING */
function setupEvents() {
  floorCanvas.onmousedown = (e) => {
    if (currentMode !== '2d') return;
    const rect = floorCanvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    selectedId = null;
    for (let i = objects.length - 1; i >= 0; i--) {
      const obj = objects[i];
      if (mx >= obj.x && mx <= obj.x + obj.w && my >= obj.y && my <= obj.y + obj.h) {
        selectedId = obj.id;
        isDragging = true;
        dragOffsetX = mx - obj.x;
        dragOffsetY = my - obj.y;
        objects.push(objects.splice(i, 1)[0]);
        break;
      }
    }
    updateInspector();
    redraw2D();
  };

  floorCanvas.onmousemove = (e) => {
    if (!isDragging || !selectedId || currentMode !== '2d') return;
    const rect = floorCanvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    const obj = objects.find(o => o.id === selectedId);
    if (obj) {
      obj.x = mx - dragOffsetX;
      obj.y = my - dragOffsetY;
      redraw2D();
    }
  };

  window.onmouseup = () => { isDragging = false; };
}

/* INSPECTOR PANEL */
function updateInspector() {
  const box = document.getElementById('inspectorContent');
  const obj = objects.find(o => o.id === selectedId);

  if (!obj) {
    box.innerHTML = `<p style="font-size:11.5px;color:#64748b;text-align:center;margin-top:50px;">선택된 시설물이 없습니다.<br>도면에서 시설물을 클릭하세요.</p>`;
    return;
  }

  box.innerHTML = `
    <div class="prop-group"><label>시설물 이름</label><input type="text" value="${obj.title}" oninput="updateProp('title', this.value)"></div>
    <div class="prop-group"><label>너비 (Width)</label><input type="number" value="${obj.w}" oninput="updateProp('w', parseInt(this.value)||40)"></div>
    <div class="prop-group"><label>높이 (Height)</label><input type="number" value="${obj.h}" oninput="updateProp('h', parseInt(this.value)||40)"></div>
    <div class="prop-group"><label>X 좌표</label><input type="number" value="${Math.round(obj.x)}" oninput="updateProp('x', parseInt(this.value)||0)"></div>
    <div class="prop-group"><label>Y 좌표</label><input type="number" value="${Math.round(obj.y)}" oninput="updateProp('y', parseInt(this.value)||0)"></div>
    <button class="btn-danger" style="width:100%;margin-top:8px;" onclick="deleteSelected()">시설물 삭제</button>
  `;
}

function updateProp(key, val) {
  const obj = objects.find(o => o.id === selectedId);
  if (obj) {
    obj[key] = val;
    redraw2D();
  }
}

function deleteSelected() {
  if (selectedId) {
    objects = objects.filter(o => o.id !== selectedId);
    selectedId = null;
    updateInspector();
    redraw2D();
    document.getElementById('totalObjCount').textContent = objects.length + '개';
  }
}

/* CROWD SIMULATION & HEATMAP */
function initCrowd() {
  crowdAgents = [];
  for(let i=0; i<65; i++){
    crowdAgents.push({
      x: 50 + Math.random()*500,
      y: 50 + Math.random()*300,
      vx: (Math.random()-0.5)*1.2,
      vy: (Math.random()-0.5)*1.2
    });
  }
}

function initRain() {
  raindrops = [];
  for(let i=0; i<80; i++){
    raindrops.push({ x: Math.random()*700, y: Math.random()*400, len: 10, vy: 5 });
  }
}

function updateSimulation() {
  if (!simRunning || !peopleCtx || !heatmapCtx) return;
  const w = peopleCanvas.width;
  const h = peopleCanvas.height;

  peopleCtx.clearRect(0,0,w,h);
  heatmapCtx.clearRect(0,0,w,h);

  objects.forEach(obj => {
    const cx = obj.x + obj.w / 2;
    const cy = obj.y + obj.h / 2;
    let grad = heatmapCtx.createRadialGradient(cx, cy, 5, cx, cy, 80);
    grad.addColorStop(0, 'rgba(239, 68, 68, 0.4)');
    grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.2)');
    grad.addColorStop(1, 'rgba(16, 185, 129, 0)');
    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath(); heatmapCtx.arc(cx, cy, 80, 0, Math.PI*2); heatmapCtx.fill();
  });

  if (isEmergency && emergencyPos) {
    const med = objects.find(o => o.type === 'medical') || objects[0];
    const mx = med.x + med.w/2;
    const my = med.y + med.h/2;
    peopleCtx.strokeStyle = '#ef4444';
    peopleCtx.lineWidth = 3;
    peopleCtx.setLineDash([6, 4]);
    peopleCtx.beginPath(); peopleCtx.moveTo(emergencyPos.x, emergencyPos.y); peopleCtx.lineTo(mx, my); peopleCtx.stroke();
    peopleCtx.setLineDash([]);

    peopleCtx.fillStyle = '#ef4444';
    peopleCtx.beginPath(); peopleCtx.arc(emergencyPos.x, emergencyPos.y, 8, 0, Math.PI*2); peopleCtx.fill();
  }

  crowdAgents.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    if(p.x < 10 || p.x > w-10) p.vx *= -1;
    if(p.y < 10 || p.y > h-10) p.vy *= -1;

    peopleCtx.fillStyle = isRain ? '#60a5fa' : '#ffffff';
    peopleCtx.beginPath(); peopleCtx.arc(p.x, p.y, 3, 0, Math.PI*2); peopleCtx.fill();
  });

  if (isRain) {
    peopleCtx.strokeStyle = 'rgba(147, 197, 253, 0.6)';
    raindrops.forEach(r => {
      r.y += r.vy;
      if(r.y > h) r.y = 0;
      peopleCtx.beginPath(); peopleCtx.moveTo(r.x, r.y); peopleCtx.lineTo(r.x-1, r.y+r.len); peopleCtx.stroke();
    });
  }
}

function renderLoop() {
  if (currentMode === '2d') {
    updateSimulation();
  }
  requestAnimationFrame(renderLoop);
}

/* CONTROLS */
let timeInterval = null;
let currentTime = 14;
function updateTimeSimulation(val) {
  currentTime = parseInt(val);
  document.getElementById('timeDisplay').textContent = `${currentTime}:00`;
}
function toggleTimelinePlay() {
  const btn = document.getElementById('btnTimelinePlay');
  if (timeInterval) {
    clearInterval(timeInterval); timeInterval = null;
    btn.textContent = '▶ 재생';
  } else {
    btn.textContent = '⏸ 정지';
    timeInterval = setInterval(() => {
      currentTime = currentTime >= 20 ? 10 : currentTime + 1;
      document.getElementById('timeSlider').value = currentTime;
      updateTimeSimulation(currentTime);
    }, 1500);
  }
}
function toggleRainEnv() {
  isRain = !isRain;
  document.getElementById('btnRain').classList.toggle('active', isRain);
  redraw2D();
}
function triggerEmergencyEnv() {
  isEmergency = !isEmergency;
  document.getElementById('btnEmergency').classList.toggle('active', isEmergency);
  emergencyPos = isEmergency ? { x: 150, y: 150 } : null;
}

function openReportModal() { document.getElementById('reportModal').classList.add('active'); }
function closeReportModal() { document.getElementById('reportModal').classList.remove('active'); }

/* MODE SWITCHING & 3D */
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btn2D').classList.toggle('active', mode === '2d');
  document.getElementById('btn3D').classList.toggle('active', mode === '3d');

  const fC = document.getElementById('floorCanvas');
  const pC = document.getElementById('peopleCanvas');
  const hC = document.getElementById('heatmapCanvas');
  const r3 = document.getElementById('container3D');

  if (mode === '3d') {
    fC.style.display = 'none'; pC.style.display = 'none'; hC.style.display = 'none';
    r3.style.display = 'block';
    init3DScene();
  } else {
    fC.style.display = 'block'; pC.style.display = 'block'; hC.style.display = 'block';
    r3.style.display = 'none';
    redraw2D();
  }
}

let scene3D, camera3D, renderer3D;
function init3DScene() {
  const container = document.getElementById('container3D');
  container.innerHTML = '';
  const w = container.clientWidth;
  const h = container.clientHeight;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w / h, 0.1, 2000);
  camera3D.position.set(0, 280, 320);
  camera3D.lookAt(0, 0, 0);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  scene3D.add(new THREE.AmbientLight(0xffffff, 0.7));
  const dir = new THREE.DirectionalLight(0xffffff, 0.8);
  dir.position.set(100, 200, 100);
  scene3D.add(dir);

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(700, 500), new THREE.MeshLambertMaterial({ color: 0x3a7d44 }));
  ground.rotation.x = -Math.PI / 2;
  scene3D.add(ground);

  objects.forEach(obj => {
    const bw = obj.w;
    const bh = obj.h;
    const bx = obj.x - w / 2 + bw / 2;
    const bz = obj.y - h / 2 + bh / 2;
    const height = obj.type === 'stage' ? 22 : 12;

    const mesh = new THREE.Mesh(new THREE.BoxGeometry(bw, height, bh), new THREE.MeshLambertMaterial({ color: parseInt(obj.color.replace('#','0x')) }));
    mesh.position.set(bx, height/2, bz);
    scene3D.add(mesh);
  });

  function animate3D() {
    if (currentMode === '3d') {
      requestAnimationFrame(animate3D);
      scene3D.rotation.y += 0.002;
      renderer3D.render(scene3D, camera3D);
    }
  }
  animate3D();
}
</script>
</body>
</html>
"""

components.html(EVENT_STUDIO_ULTIMATE_HTML, height=850, scrolling=False)
