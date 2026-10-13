import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 건축 설계도 및 시간대별 동선 시뮬레이터",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_AI_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI - 건축 및 행사장 설계 시스템</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color:#1e293b;
  background:#f1f5f9;
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
  background:linear-gradient(135deg,#0284c7,#0ea5e9);
  border-radius:10px;
  display:grid;
  place-items:center;
  font-size:18px;
  font-weight:900;
  box-shadow:0 4px 12px rgba(14,165,233,0.4);
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
  background:linear-gradient(135deg, #0284c7, #0ea5e9);
  color:#ffffff;
  box-shadow:0 4px 12px rgba(14,165,233,0.3);
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
  background:#0ea5e9;
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

.btn-primary{
  background:linear-gradient(135deg, #0284c7, #0369a1);
  color:#ffffff;
  border:none;
  padding:12px 24px;
  border-radius:12px;
  font-weight:800;
  font-size:13.5px;
  box-shadow:0 4px 14px rgba(2,132,199,0.3);
  display:inline-flex;
  align-items:center;
  gap:8px;
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(2,132,199,0.4);}

.btn-secondary{
  background:#f1f5f9;
  color:#334155;
  border:1px solid #cbd5e1;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
}
.btn-secondary:hover{background:#e2e8f0;}
.btn-secondary.active{background:#0284c7;color:#fff;border-color:#0369a1;}

/* Timeband Controls Bar */
.timeband-bar{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:14px;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  flex-wrap:wrap;
  box-shadow:0 2px 6px rgba(0,0,0,0.02);
}
.timeband-btns{display:flex;gap:6px;flex-wrap:wrap;}

/* Zone Manager Panel */
.zone-manager-box{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:14px;
  padding:16px;
  margin-top:14px;
  box-shadow:0 2px 6px rgba(0,0,0,0.02);
}
.zone-list{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin-top:10px;
}
.zone-chip{
  background:#f1f5f9;
  border:1px solid #cbd5e1;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
  display:flex;
  align-items:center;
  gap:6px;
}
.zone-chip button{background:none;border:none;color:#ef4444;font-weight:900;cursor:pointer;}

/* Main Grids */
.dashboard-main-grid{
  display:grid;
  grid-template-columns: 1.5fr 1fr;
  gap:16px;
}

/* Cards & Canvas */
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
  background:#e0f2fe;
  color:#0284c7;
  padding:3px 8px;
  border-radius:12px;
  font-weight:700;
}

/* Architectural Blueprint Canvas Wrap */
.map-wrap{
  position:relative;
  width:100%;
  height:420px;
  background:#0f172a; /* CAD Blueprint Dark Grid Theme */
  border-radius:12px;
  overflow:hidden;
  border:2px solid #334155;
}
#blueprintCanvas, #heatmapCanvas, #agentCanvas{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
}
#heatmapCanvas{z-index:5;opacity:0.85;pointer-events:none;}
#agentCanvas{z-index:10;pointer-events:none;}

.map-legend{
  position:absolute;
  left:10px;
  bottom:10px;
  z-index:20;
  background:rgba(15,23,42,0.85);
  backdrop-filter:blur(6px);
  padding:8px 12px;
  border-radius:10px;
  font-size:10.5px;
  border:1px solid #334155;
  color:#f8fafc;
  display:grid;
  grid-template-columns:repeat(2, 1fr);
  gap:4px 10px;
}
.legend-item{display:flex;align-items:center;gap:5px;font-weight:600;}
.legend-dot{width:8px;height:8px;border-radius:2px;}
</style>
</head>
<body>

<div class="app-container">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon">📐</div>
      <div>
        <div class="brand-title">Event AI</div>
        <div class="brand-sub">건축 설계 & 동선 시뮬레이터</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item active" onclick="switchPage('design', this)">
        <span class="nav-icon">🗺️</span> 설계도 및 시뮬레이션
      </div>
      <div class="nav-item" onclick="switchPage('home', this)">
        <span class="nav-icon">📝</span> 기본 설정 입력
      </div>
    </nav>

    <div class="side-banner" style="background:rgba(14,165,233,0.1); border:1px solid rgba(14,165,233,0.25); padding:12px; border-radius:10px; color:#e2e8f0; font-size:11px; line-height:1.4;">
      <b style="color:#38bdf8;">💡 설계도 가이드</b><br>
      캐드 스타일의 평면 설계도에서 체험존을 직접 생성하고 시간대별 분포를 확인하세요.
    </div>

    <div class="side-profile">
      <div class="side-avatar">추</div>
      <div class="side-user-info">
        <div class="side-user-name">추천님</div>
        <button class="side-user-btn" onclick="alert('로그아웃 되었습니다.')">로그아웃</button>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">

    <!-- Top Header -->
    <header class="top-header">
      <div class="top-title">
        <h2 id="topTitleText">🗺️ 건축 설계도 및 시간대별 동선 시뮬레이터</h2>
        <p id="topSubText">건축 도면 스타일의 레이아웃과 시간대별 인구 분포를 실시간으로 제어합니다.</p>
      </div>
      <button class="btn-primary" onclick="resetBlueprint()">
        ↺ 설계도 초기화
      </button>
    </header>

    <!-- PAGE 1: CONFIG -->
    <section id="pageHome" class="page-view">
      <div class="form-card">
        <div class="form-section-head">📝 기본 건축 및 행사 설정</div>
        <div class="form-grid">
          <div class="form-group">
            <label>📌 프로젝트명</label>
            <input type="text" id="inEventName" value="2025 복합 문화 컨벤션 센터">
          </div>
          <div class="form-group">
            <label>📐 도면 규격</label>
            <select id="inVenueType">
              <option value="컨벤션 홀 A" selected>대형 컨벤션 홀 (실내)</option>
              <option value="종합 전시장">종합 전시장 (복합)</option>
            </select>
          </div>
          <div class="form-group">
            <label>👥 최대 수용 인원</label>
            <input type="text" id="inVisitors" value="5,000명">
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn-primary" onclick="switchPage('design', document.querySelectorAll('.nav-item')[0])">
            설계도로 이동하기 →
          </button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: MAIN DESIGN & SIMULATION -->
    <section id="pageDesign" class="page-view active">

      <!-- Timeband Selector Bar -->
      <div class="timeband-bar">
        <div style="display:flex;align-items:center;gap:8px;font-size:13px;font-weight:800;color:#0f172a;">
          <span>⏰ <b>시간대별 인구 분포 조절:</b></span>
        </div>
        <div class="timeband-btns">
          <button class="btn-secondary" id="btnTimeEntry" onclick="setTimeband('entry')">🚪 입·퇴장 시간대 (09:00)</button>
          <button class="btn-secondary" id="btnTimeLunch" onclick="setTimeband('lunch')">🍱 점심 시간대 (12:30)</button>
          <button class="btn-secondary active" id="btnTimePeak" onclick="setTimeband('peak')">🔥 오후 피크타임 (15:00)</button>
        </div>
        <span id="timeDesc" style="font-size:11.5px;color:#0284c7;font-weight:700;">현재: 체험존 및 메인홀 고르게 분산</span>
      </div>

      <!-- Experience Zone Creator / Manager Panel -->
      <div class="zone-manager-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <span style="font-size:13px;font-weight:800;color:#0f172a;">🛠️ 체험존 구역 관리 및 신규 생성</span>
          <span style="font-size:11px;color:#64748b;">원하는 이름의 체험존을 추가하여 설계도에 즉시 반영하세요.</span>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <input type="text" id="newZoneName" placeholder="새로운 체험존 이름 (예: VR 체험관)" style="padding:7px 12px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;width:240px;">
          <select id="newZoneColor" style="padding:7px 12px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;">
            <option value="#3b82f6">블루톤 (체험존)</option>
            <option value="#10b981">그린톤 (휴게존)</option>
            <option value="#f59e0b">오렌지톤 (이벤트존)</option>
            <option value="#ec4899">핑크톤 (포토존)</option>
          </select>
          <button class="btn-primary" style="padding:7px 16px;font-size:12px;" onclick="addNewExperienceZone()">+ 체험존 생성</button>
        </div>
        <div class="zone-list" id="zoneChipsContainer">
          <!-- Dynamic Zone Chips -->
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-main-grid" style="margin-top:14px;">

        <!-- 1. Architectural Blueprint Canvas -->
        <div class="card-panel">
          <div class="card-head">
            <span>📐 건축 평면 설계도 (CAD Blueprint 스타일)</span>
            <span class="card-badge" id="blueprintBadge">구역 편집 모드</span>
          </div>

          <div class="map-wrap" id="mapWrap">
            <canvas id="blueprintCanvas"></canvas>
            <canvas id="agentCanvas"></canvas>

            <!-- Legend -->
            <div class="map-legend">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 메인홀/무대</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 식음/푸드존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 휴게공간</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 응급센터</div>
              <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> 출입구</div>
            </div>
          </div>

          <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;">
            <span style="font-size:11px;color:#94a3b8;" id="canvasStatusMsg">💡 도면 내 구역을 클릭하거나 드래그하여 배치할 수 있습니다.</span>
            <button class="btn-secondary" onclick="toggleSimAnimation()" id="btnSimToggle">▶ 군중 동선 시뮬레이션 시작</button>
          </div>
        </div>

        <!-- 2. Heatmap Density Distribution -->
        <div class="card-panel">
          <div class="card-head">
            <span>🔥 시간대별 인구 밀집도 Heatmap</span>
            <span class="card-badge" id="heatmapStatusBadge">실시간 분포 연동</span>
          </div>

          <div class="map-wrap">
            <canvas id="heatmapCanvas"></canvas>
          </div>

          <div style="display:flex;justify-content:space-around;font-size:10px;color:#94a3b8;margin-top:10px;font-weight:700;">
            <span style="color:#10b981;">🟢 여유 (원활)</span>
            <span style="color:#eab308;">🟡 보통 (일반)</span>
            <span style="color:#f97316;">🟠 혼잡 (주의)</span>
            <span style="color:#ef4444;">🔴 과밀 (병목 구간)</span>
          </div>
        </div>

      </div>

    </section>

  </main>
</div>

<script>
/* Navigation Switching */
function switchPage(pageId, el){
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  if(el) el.classList.add('active');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    setTimeout(initBlueprintSystem, 50);
  }
}

/* BLUEPRINT & ZONE STATE MANAGEMENT */
let blueprintCanvas, bpCtx;
let agentCanvas, agentCtx;
let heatmapCanvas, hmCtx;

let currentTimeband = 'peak'; // entry, lunch, peak
let isSimRunning = false;
let animId = null;

// Initial Blueprint Zones (Exhibitions, Experience Zones, Hall)
let blueprintZones = [
  { id: 'stage', name: '메인 컨벤션 홀', x: 0.35, y: 0.08, w: 0.30, h: 0.20, color: '#8b5cf6', type: 'stage' },
  { id: 'exp1', name: 'AI 기술 체험존', x: 0.10, y: 0.32, w: 0.20, h: 0.16, color: '#3b82f6', type: 'exp' },
  { id: 'exp2', name: '디지털 아트 체험존', x: 0.70, y: 0.32, w: 0.20, h: 0.16, color: '#3b82f6', type: 'exp' },
  { id: 'food', name: '푸드 & 다이닝 존', x: 0.10, y: 0.55, w: 0.22, h: 0.16, color: '#f59e0b', type: 'food' },
  { id: 'rest', name: '중앙 잔디 휴게존', x: 0.40, y: 0.55, w: 0.20, h: 0.16, color: '#10b981', type: 'rest' },
  { id: 'medical', name: '응급 의료센터', x: 0.70, y: 0.55, w: 0.20, h: 0.16, color: '#ef4444', type: 'medical' }
];

let agents = [];

function initBlueprintSystem(){
  blueprintCanvas = document.getElementById('blueprintCanvas');
  agentCanvas = document.getElementById('agentCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');

  if(!blueprintCanvas) return;

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth;
  const h = wrap.clientHeight;

  [blueprintCanvas, agentCanvas, heatmapCanvas].forEach(c => {
    c.width = w;
    c.height = h;
  });

  bpCtx = blueprintCanvas.getContext('2d');
  agentCtx = agentCanvas.getContext('2d');
  hmCtx = heatmapCanvas.getContext('2d');

  renderZoneChips();
  setTimeband('peak');
  redrawBlueprint();

  if(!animId){
    simulationLoop();
  }
}

/* TIMEBAND POPULATION DISTRIBUTION CONTROL */
function setTimeband(band){
  currentTimeband = band;
  document.querySelectorAll('.timeband-btns button').forEach(b => b.classList.remove('active'));

  const desc = document.getElementById('timeDesc');
  if(band === 'entry'){
    document.getElementById('btnTimeEntry').classList.add('active');
    desc.textContent = '입·퇴장 시간대: 출입구 및 로비 주변 인구 밀집도 급증';
    setAgentDensity(40, 'entry');
  } else if(band === 'lunch'){
    document.getElementById('btnTimeLunch').classList.add('active');
    desc.textContent = '점심 시간대: 푸드 & 다이닝 존으로 인구 집중';
    setAgentDensity(90, 'lunch');
  } else {
    document.getElementById('btnTimePeak').classList.add('active');
    desc.textContent = '오후 피크타임: 메인홀 및 각 체험존 고르게 분산';
    setAgentDensity(75, 'peak');
  }
  redrawBlueprint();
}

function setAgentDensity(count, mode){
  agents = [];
  const w = blueprintCanvas.width;
  const h = blueprintCanvas.height;

  for(let i=0; i<count; i++){
    let startX = w * 0.5, startY = h * 0.9; // Default near gate
    if(mode === 'entry'){
      startX = w * (0.4 + Math.random()*0.2);
      startY = h * (0.8 + Math.random()*0.15);
    } else if(mode === 'lunch'){
      startX = w * 0.2 + Math.random() * w * 0.2;
      startY = h * 0.55 + Math.random() * h * 0.15;
    } else {
      startX = w * 0.2 + Math.random() * w * 0.6;
      startY = h * 0.2 + Math.random() * h * 0.6;
    }
    agents.push({
      x: startX, y: startY,
      vx: (Math.random()-0.5)*1.2,
      vy: (Math.random()-0.5)*1.2,
      mode: mode
    });
  }
}

/* ADD & EDIT EXPERIENCE ZONES */
function addNewExperienceZone(){
  const nameInput = document.getElementById('newZoneName');
  const colorSelect = document.getElementById('newZoneColor');
  const name = nameInput.value.trim();
  if(!name){ alert('체험존 이름을 입력해주세요.'); return; }

  const newId = 'custom_' + Date.now();
  blueprintZones.push({
    id: newId,
    name: name,
    x: 0.4 + (Math.random()*0.2),
    y: 0.35 + (Math.random()*0.1),
    w: 0.18,
    h: 0.14,
    color: colorSelect.value,
    type: 'exp'
  });

  nameInput.value = '';
  renderZoneChips();
  redrawBlueprint();
  alert(`새로운 체험존 「${name}」이(가) 설계도에 생성되었습니다!`);
}

function removeZone(id){
  blueprintZones = blueprintZones.filter(z => z.id !== id);
  renderZoneChips();
  redrawBlueprint();
}

function renderZoneChips(){
  const container = document.getElementById('zoneChipsContainer');
  container.innerHTML = '';
  blueprintZones.forEach(z => {
    const chip = document.createElement('div');
    chip.className = 'zone-chip';
    chip.innerHTML = `<span style="width:8px;height:8px;background:${z.color};border-radius:2px;"></span> ${z.name} <button onclick="removeZone('${z.id}')">✕</button>`;
    container.appendChild(chip);
  });
}

/* CAD ARCHITECTURAL BLUEPRINT RENDERING */
function redrawBlueprint(){
  if(!bpCtx) return;
  const w = blueprintCanvas.width;
  const h = blueprintCanvas.height;

  // CAD Blueprint Dark Background (#0f172a)
  bpCtx.fillStyle = '#0f172a';
  bpCtx.fillRect(0, 0, w, h);

  // Architectural Grid Lines
  bpCtx.strokeStyle = 'rgba(51, 65, 85, 0.5)';
  bpCtx.lineWidth = 1;
  for(let x=0; x<w; x+=30){
    bpCtx.beginPath(); bpCtx.moveTo(x, 0); bpCtx.lineTo(x, h); bpCtx.stroke();
  }
  for(let y=0; y<h; y+=30){
    bpCtx.beginPath(); bpCtx.moveTo(0, y); bpCtx.lineTo(w, y); bpCtx.stroke();
  }

  // Outer Building Walls (Architectural Double Stroke)
  bpCtx.strokeStyle = '#38bdf8';
  bpCtx.lineWidth = 4;
  bpCtx.strokeRect(30, 20, w - 60, h - 40);

  bpCtx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
  bpCtx.lineWidth = 1;
  bpCtx.strokeRect(34, 24, w - 68, h - 48);

  // Entrance Gate Marker
  bpCtx.fillStyle = '#64748b';
  bpCtx.fillRect(w*0.42, h - 24, w*0.16, 10);
  bpCtx.fillStyle = '#f8fafc';
  bpCtx.font = 'bold 10px Pretendard';
  bpCtx.textAlign = 'center';
  bpCtx.fillText('MAIN GATE (출입구)', w*0.5, h - 30);

  // Render Blueprint Zones (Rooms/Booths with architectural borders)
  blueprintZones.forEach(z => {
    const bx = z.x * w, by = z.y * h, bw = z.w * w, bh = z.h * h;

    // Room Fill
    bpCtx.fillStyle = z.color + '33'; // Semi-transparent
    bpCtx.fillRect(bx, by, bw, bh);

    // Room Border
    bpCtx.strokeStyle = z.color;
    bpCtx.lineWidth = 2;
    bpCtx.strokeRect(bx, by, bw, bh);

    // Inner Room Label Tag
    bpCtx.fillStyle = 'rgba(15, 23, 42, 0.8)';
    bpCtx.fillRect(bx + 4, by + 4, bw - 8, 20);

    bpCtx.fillStyle = '#ffffff';
    bpCtx.font = 'bold 11px Pretendard';
    bpCtx.textAlign = 'center';
    bpCtx.fillText(z.name, bx + bw/2, by + 18);
  });
}

/* SIMULATION & HEATMAP LOOP */
function toggleSimAnimation(){
  isSimRunning = !isSimRunning;
  const btn = document.getElementById('btnSimToggle');
  btn.textContent = isSimRunning ? '⏸ 시뮬레이션 일시정지' : '▶ 군중 동선 시뮬레이션 시작';
  btn.className = isSimRunning ? 'btn-secondary active' : 'btn-secondary';
}

function simulationLoop(){
  if(isSimRunning && blueprintCanvas){
    updateAgents();
    drawAgents();
    drawHeatmap();
  }
  animId = requestAnimationFrame(simulationLoop);
}

function updateAgents(){
  const w = blueprintCanvas.width;
  const h = blueprintCanvas.height;

  agents.forEach(a => {
    // Timeband specific attraction vectors
    let targetX = w * 0.5, targetY = h * 0.5;
    if(currentTimeband === 'entry'){
      targetX = w * 0.5; targetY = h * 0.7;
    } else if(currentTimeband === 'lunch'){
      targetX = w * 0.2; targetY = h * 0.63; // Food zone attraction
    } else {
      targetX = w * 0.5; targetY = h * 0.4; // General distributed
    }

    a.vx += (targetX - a.x) * 0.0002;
    a.vy += (targetY - a.y) * 0.0002;

    a.x += a.vx;
    a.y += a.vy;

    if(a.x < 40) { a.x = 40; a.vx *= -1; }
    if(a.x > w-40) { a.x = w-40; a.vx *= -1; }
    if(a.y < 30) { a.y = 30; a.vy *= -1; }
    if(a.y > h-30) { a.y = h-30; a.vy *= -1; }
  });
}

function drawAgents(){
  if(!agentCtx) return;
  const w = agentCanvas.width;
  const h = agentCanvas.height;
  agentCtx.clearRect(0, 0, w, h);

  agents.forEach(a => {
    agentCtx.fillStyle = '#38bdf8';
    agentCtx.beginPath();
    agentCtx.arc(a.x, a.y, 3, 0, Math.PI*2);
    agentCtx.fill();
  });
}

function drawHeatmap(){
  if(!hmCtx) return;
  const w = heatmapCanvas.width;
  const h = heatmapCanvas.height;
  hmCtx.clearRect(0, 0, w, h);

  // CAD Blueprint Theme for Heatmap Background
  hmCtx.fillStyle = '#0f172a';
  hmCtx.fillRect(0, 0, w, h);

  const grid = {};
  const gridSize = 35;

  agents.forEach(a => {
    const gx = Math.floor(a.x / gridSize);
    const gy = Math.floor(a.y / gridSize);
    const key = `${gx}_${gy}`;
    grid[key] = (grid[key] || 0) + 1;
  });

  Object.keys(grid).forEach(key => {
    const [gx, gy] = key.split('_').map(Number);
    const count = grid[key];
    const cx = gx * gridSize + gridSize/2;
    const cy = gy * gridSize + gridSize/2;

    if(count >= 1){
      let radius = count * 14;
      let alpha = Math.min(0.85, count * 0.18);
      let grad = hmCtx.createRadialGradient(cx, cy, 0, cx, cy, radius);

      if(currentTimeband === 'lunch' && gx <= 3){
        grad.addColorStop(0, `rgba(239, 68, 68, ${alpha})`); // High density in lunch zone
      } else {
        grad.addColorStop(0, `rgba(245, 158, 11, ${alpha})`);
      }
      grad.addColorStop(1, 'rgba(16, 185, 129, 0)');

      hmCtx.fillStyle = grad;
      hmCtx.beginPath();
      hmCtx.arc(cx, cy, radius, 0, Math.PI*2);
      hmCtx.fill();
    }
  });
}

function resetBlueprint(){
  initBlueprintSystem();
  alert('설계도가 초기화되었습니다.');
}

window.addEventListener('load', () => {
  switchPage('design', document.querySelectorAll('.nav-item')[0]);
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=920, scrolling=True)
