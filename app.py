import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 커스텀 행사장 설계 & 3D 시뮬레이터",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_AI_FULL_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI - 디지털 트윈 시뮬레이터</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">

<!-- Three.js & OrbitControls -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, sans-serif;
  color:#0f172a;
  background:#f1f5f9;
  overflow-x:hidden;
}
button,input,select,textarea{font:inherit;}
button{cursor:pointer;transition:all 0.15s ease;}

::-webkit-scrollbar {width:5px;height:5px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}

.app-container{display:flex;min-height:100vh;}

/* Sidebar Controls */
.sidebar{
  width:310px;
  background:#0f172a;
  color:#94a3b8;
  padding:16px;
  display:flex;
  flex-direction:column;
  gap:14px;
  flex-shrink:0;
  border-right:1px solid #1e293b;
  max-height:100vh;
  overflow-y:auto;
}
.brand{display:flex;align-items:center;gap:10px;padding:4px 2px;color:#fff;}
.brand-icon{
  width:32px;height:32px;
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:8px;display:grid;place-items:center;font-size:16px;font-weight:900;
}
.brand-title{font-size:16px;font-weight:800;color:#ffffff;}

.opt-group-title{
  font-size:11px;font-weight:800;color:#38bdf8;letter-spacing:0.5px;
  margin-top:6px;margin-bottom:6px;display:flex;align-items:center;gap:6px;
  border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:4px;
}
.opt-card{
  background:#1e293b;border:1px solid #334155;border-radius:10px;padding:10px;
  display:flex;flex-direction:column;gap:8px;
}
.opt-row{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:11px;}
.opt-row label{color:#cbd5e1;font-weight:600;}
.opt-row input[type="range"]{flex:1;accent-color:#3b82f6;}
.opt-row select, .opt-row input[type="text"], .opt-row input[type="number"]{
  background:#0f172a;border:1px solid #475569;color:#fff;padding:4px 8px;border-radius:6px;font-size:11px;outline:none;
}

/* Main Content */
.main-content{
  flex:1;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0;overflow-y:auto;
}

.top-header{
  display:flex;justify-content:space-between;align-items:center;
  background:#ffffff;padding:12px 18px;border-radius:12px;border:1px solid #e2e8f0;
}
.top-title h2{font-size:17px;font-weight:800;color:#0f172a;}
.top-title p{font-size:11px;color:#64748b;}

/* View Switcher & Toolbar */
.control-bar{
  display:flex;justify-content:space-between;align-items:center;
  background:#ffffff;border:1px solid #e2e8f0;padding:8px 12px;border-radius:10px;flex-wrap:wrap;gap:8px;
}
.btn-group{display:flex;gap:4px;align-items:center;}
.btn-ui{
  padding:6px 10px;border-radius:6px;font-size:11px;font-weight:700;
  border:1px solid #cbd5e1;background:#fff;color:#334155;
}
.btn-ui.active{background:#2563eb;color:#fff;border-color:#2563eb;}
.btn-ui-primary{
  background:linear-gradient(135deg, #2563eb, #1d4ed8);
  color:#ffffff;border:none;padding:7px 12px;border-radius:6px;font-weight:800;font-size:11.5px;
}
.btn-ui-danger{
  background:#ef4444;color:#ffffff;border:none;padding:5px 9px;border-radius:6px;font-weight:700;font-size:10.5px;
}

/* Map Canvas Container */
.map-wrap{
  position:relative;width:100%;height:460px;background:#0f172a;
  border-radius:12px;overflow:hidden;border:1px solid #334155;
}
#venueCanvas, #heatmapCanvas, #vectorCanvas, #canvas3D{
  position:absolute;inset:0;width:100%;height:100%;
}
#canvas3D{display:none;z-index:10;}

/* Bottom Grids */
.grid-2col{display:grid;grid-template-columns:1.2fr 1fr;gap:12px;}
.card-panel{
  background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:14px;
  display:flex;flex-direction:column;gap:10px;
}
.card-head{font-size:13px;font-weight:800;color:#0f172a;display:flex;justify-content:space-between;align-items:center;}

.history-list{display:flex;flex-direction:column;gap:6px;max-height:160px;overflow-y:auto;}
.history-item{
  background:#f8fafc;border:1px solid #e2e8f0;padding:8px 10px;border-radius:8px;
  display:flex;justify-content:space-between;align-items:center;font-size:11px;
}
.history-item.active{border-color:#2563eb;background:#eff6ff;}

.score-badge{font-size:10px;padding:2px 6px;border-radius:4px;font-weight:800;}
</style>
</head>
<body>

<div class="app-container">

  <!-- LEFT CONTROL PANEL (옵션 상세 제어) -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon">⚙️</div>
      <div>
        <div class="brand-title">Event AI Options</div>
      </div>
    </div>

    <!-- 1. AI 알고리즘 가중치 & 패턴 옵션 -->
    <div class="opt-group-title">🧠 AI 재배치 알고리즘 옵션</div>
    <div class="opt-card">
      <div class="opt-row">
        <label>비상 안전 가중치</label>
        <input type="range" id="wSafety" min="0" max="100" value="80" oninput="updateWeightLabel()">
        <span id="lblSafety" style="color:#fff;width:24px;">80</span>
      </div>
      <div class="opt-row">
        <label>동선 효율 가중치</label>
        <input type="range" id="wFlow" min="0" max="100" value="60" oninput="updateWeightLabel()">
        <span id="lblFlow" style="color:#fff;width:24px;">60</span>
      </div>
      <div class="opt-row">
        <label>체류 분산 가중치</label>
        <input type="range" id="wDist" min="0" max="100" value="70" oninput="updateWeightLabel()">
        <span id="lblDist" style="color:#fff;width:24px;">70</span>
      </div>
      <div class="opt-row">
        <label>배치 기본 패턴</label>
        <select id="optPattern">
          <option value="ai">✦ AI 자율 최적화</option>
          <option value="grid">▦ 격자 분산형 (Grid)</option>
          <option value="stage">🎭 메인무대 중심형</option>
          <option value="perimeter">🔲 외각 둘레형</option>
        </select>
      </div>
      <button class="btn-ui-primary" style="width:100%;margin-top:4px;" onclick="generateNewAILayout()">
        ⚡ 설정값 반영 신규 AI 재배치
      </button>
    </div>

    <!-- 2. 부스 커스텀 편집 및 추가 옵션 -->
    <div class="opt-group-title">🛠️ 부스 수동 제어 & 크기 조절</div>
    <div class="opt-card">
      <div class="opt-row">
        <label>신규 부스 추가</label>
        <select id="newBoothType">
          <option value="체험존">🧪 체험존</option>
          <option value="푸드존">🍔 푸드존</option>
          <option value="응급의료">🏥 응급의료소</option>
          <option value="쉼터/천막">🌿 쉼터/천막</option>
          <option value="화장실">🚻 위생시설</option>
        </select>
      </div>
      <button class="btn-ui" style="width:100%;" onclick="addCustomBooth()">+ 선택 부스 추가하기</button>
      
      <div style="border-top:1px solid #334155;padding-top:6px;margin-top:4px;">
        <label style="font-size:10px;color:#94a3b8;display:block;margin-bottom:4px;">선택 부스 크기(Width / Height) 변경</label>
        <div class="opt-row">
          <select id="selectBoothToResize" onchange="onBoothSelectChange()"></select>
        </div>
        <div class="opt-row" style="margin-top:4px;">
          <label>가로(W)</label>
          <input type="range" id="boothW" min="5" max="35" value="15" oninput="updateBoothSize()">
          <label>세로(H)</label>
          <input type="range" id="boothH" min="5" max="35" value="15" oninput="updateBoothSize()">
        </div>
        <button class="btn-ui-danger" style="width:100%;margin-top:6px;" onclick="deleteSelectedBooth()">🗑️ 선택 부스 삭제</button>
      </div>
    </div>

    <!-- 3. 환경, 기상 & 돌발 상황 시뮬레이션 옵션 -->
    <div class="opt-group-title">🌧️ 환경 & 돌발 상황 시뮬레이션</div>
    <div class="opt-card">
      <div class="opt-row">
        <label>기상/환경 조건</label>
        <select id="optWeather" onchange="changeEnvironment()">
          <option value="sunny">☀️ 맑음 (평시)</option>
          <option value="rain">🌧️ 우천 (부스/천막 대피)</option>
          <option value="night">🌙 야간 모드 (조명 작동)</option>
          <option value="heat">🔥 폭염 (쉼터/음수대 밀집)</option>
        </select>
      </div>
      <div class="opt-row">
        <label>돌발 시나리오</label>
        <select id="optEmergency" onchange="changeContingency()">
          <option value="normal">✅ 정상 관람 상태</option>
          <option value="surge">🚨 관람객 갑작스런 폭주</option>
          <option value="medical">🏥 응급환자 골든타임 통로</option>
          <option value="fire">🔥 비상 탈출/대피 시뮬레이션</option>
          <option value="vip">👑 VIP/아티스트 동선 이동</option>
        </select>
      </div>
    </div>

    <!-- 4. 시뮬레이션 속도 & 관람객 제어 -->
    <div class="opt-group-title">👥 관람객 & 시뮬레이션 제어</div>
    <div class="opt-card">
      <div class="opt-row">
        <label>총 관람객 수</label>
        <input type="range" id="optPeopleCount" min="10" max="250" value="80" oninput="onPeopleCountChange()">
        <span id="lblPeopleCount" style="color:#fff;">80</span>
      </div>
      <div class="opt-row">
        <label>이동 속도</label>
        <input type="range" id="optSpeed" min="1" max="5" value="2" oninput="onSpeedChange()">
        <span id="lblSpeed" style="color:#fff;">2x</span>
      </div>
      <div class="opt-row">
        <label>시뮬레이션</label>
        <button class="btn-ui" id="btnPause" onclick="togglePause()">⏸️ 일시정지</button>
      </div>
    </div>

  </aside>

  <!-- MAIN VIEW PANEL -->
  <main class="main-content">

    <header class="top-header">
      <div class="top-title">
        <h2>🎪 Event AI - 통합 행사장 3D 디지털 트윈</h2>
        <p>상세 옵션 및 변수를 자유롭게 조정하여 실시간 동선과 대피 시뮬레이션을 수행합니다.</p>
      </div>
      <div class="btn-group">
        <button class="btn-ui" onclick="exportJSON()">📥 배치 데이터 JSON 내보내기</button>
      </div>
    </header>

    <!-- CONTROL BAR & OVERLAY SWITCHES -->
    <div class="control-bar">
      <!-- 2D / 3D Mode -->
      <div class="btn-group">
        <button class="btn-ui active" id="btn2D" onclick="setRenderMode('2D')">🗺️ 2D 평면도</button>
        <button class="btn-ui" id="btn3D" onclick="setRenderMode('3D')">🧊 3D 입체 트윈 (Three.js)</button>
      </div>

      <!-- Layer Overlays -->
      <div class="btn-group">
        <button class="btn-ui active" id="toggleHeatmap" onclick="toggleOverlay('heatmap')">🔥 히트맵 켜기</button>
        <button class="btn-ui active" id="toggleVectors" onclick="toggleOverlay('vectors')">🔀 동선 벡터 표시</button>
        <button class="btn-ui active" id="toggleLabels" onclick="toggleOverlay('labels')">🏷️ 부스 라벨 표시</button>
        <button class="btn-ui active" id="toggleGrid" onclick="toggleOverlay('grid')">📐 그리드 표시</button>
      </div>
    </div>

    <!-- CANVAS VIEW AREA -->
    <div class="map-wrap" id="mapWrap">
      <canvas id="venueCanvas"></canvas>
      <canvas id="heatmapCanvas"></canvas>
      <canvas id="vectorCanvas"></canvas>
      <div id="canvas3D"></div>
    </div>

    <!-- BOTTOM PANELS -->
    <div class="grid-2col">

      <!-- Left: History & Version Control -->
      <div class="card-panel">
        <div class="card-head">
          <span>📜 AI 배치 기록 히스토리</span>
          <span style="font-size:10px;color:#64748b;">이전 기록 클릭 시 복원</span>
        </div>
        <div class="history-list" id="historyContainer"></div>
      </div>

      <!-- Right: Live Metrics & Report -->
      <div class="card-panel">
        <div class="card-head">📊 실시간 평가 지표 & 상태 리포트</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;text-align:center;">
          <div style="background:#f8fafc;padding:8px;border-radius:8px;border:1px solid #e2e8f0;">
            <div style="font-size:10px;color:#64748b;">비상 안전성</div>
            <div id="scSafety" style="font-size:16px;font-weight:900;color:#16a34a;">92점</div>
          </div>
          <div style="background:#f8fafc;padding:8px;border-radius:8px;border:1px solid #e2e8f0;">
            <div style="font-size:10px;color:#64748b;">동선 순환성</div>
            <div id="scCong" style="font-size:16px;font-weight:900;color:#0284c7;">85점</div>
          </div>
          <div style="background:#f8fafc;padding:8px;border-radius:8px;border:1px solid #e2e8f0;">
            <div style="font-size:10px;color:#64748b;">공간 균형성</div>
            <div id="scAcc" style="font-size:16px;font-weight:900;color:#8b5cf6;">89점</div>
          </div>
        </div>
        <div style="background:#0f172a;color:#fff;padding:10px;border-radius:8px;font-size:11px;margin-top:4px;">
          <div style="color:#38bdf8;font-weight:800;" id="simStatusText">✅ 정상 상태 작동 중</div>
          <div style="color:#cbd5e1;margin-top:3px;" id="simDetailText">관람객이 설정된 AI 동선을 따라 원활히 이동하고 있습니다.</div>
        </div>
      </div>

    </div>

  </main>
</div>

<script>
/* GLOBAL STATE & PARAMETERS */
let renderMode = '2D';
let isPaused = false;
let overlays = { heatmap: true, vectors: true, labels: true, grid: true };
let envMode = 'sunny';
let contingencyMode = 'normal';
let simSpeed = 2;

let venueCanvas, venueCtx, heatmapCanvas, heatmapCtx, vectorCanvas, vectorCtx;
let animFrameId = null;

let people = [];
let layoutHistory = [];
let currentLayoutIndex = -1;

// Default Booth List
let booths = [
  { id:'stage', title:'메인 무대', x: 0.38, y: 0.05, w: 0.24, h: 0.16, color:'#8b5cf6', icon:'🎭' },
  { id:'boothA', title:'체험존 A', x: 0.10, y: 0.24, w: 0.16, h: 0.14, color:'#3b82f6', icon:'🧪' },
  { id:'boothB', title:'체험존 B', x: 0.74, y: 0.24, w: 0.16, h: 0.14, color:'#3b82f6', icon:'🚀' },
  { id:'food', title:'푸드존', x: 0.08, y: 0.52, w: 0.18, h: 0.15, color:'#f59e0b', icon:'🍔' },
  { id:'med', title:'응급의료', x: 0.74, y: 0.52, w: 0.16, h: 0.14, color:'#ef4444', icon:'🏥' },
  { id:'rest', title:'중앙 쉼터', x: 0.40, y: 0.46, w: 0.20, h: 0.16, color:'#10b981', icon:'🌿' }
];

/* 1. INITIALIZATION & UI UPDATES */
function updateWeightLabel(){
  document.getElementById('lblSafety').textContent = document.getElementById('wSafety').value;
  document.getElementById('lblFlow').textContent = document.getElementById('wFlow').value;
  document.getElementById('lblDist').textContent = document.getElementById('wDist').value;
}

function updateBoothSelectOptions(){
  const sel = document.getElementById('selectBoothToResize');
  sel.innerHTML = '';
  booths.forEach((b, i) => {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = `${b.icon} ${b.title}`;
    sel.appendChild(opt);
  });
}

function onBoothSelectChange(){
  const idx = document.getElementById('selectBoothToResize').value;
  if(booths[idx]){
    document.getElementById('boothW').value = Math.round(booths[idx].w * 100);
    document.getElementById('boothH').value = Math.round(booths[idx].h * 100);
  }
}

function updateBoothSize(){
  const idx = document.getElementById('selectBoothToResize').value;
  if(booths[idx]){
    booths[idx].w = parseInt(document.getElementById('boothW').value) / 100;
    booths[idx].h = parseInt(document.getElementById('boothH').value) / 100;
    if(renderMode === '3D') build3DScene();
  }
}

function addCustomBooth(){
  const type = document.getElementById('newBoothType').value;
  const id = 'custom_' + Date.now();
  let color = '#3b82f6', icon = '🎪';
  if(type === '푸드존'){ color='#f59e0b'; icon='🍔'; }
  else if(type === '응급의료'){ color='#ef4444'; icon='🏥'; }
  else if(type === '쉼터/천막'){ color='#10b981'; icon='🌿'; }
  else if(type === '화장실'){ color='#06b6d4'; icon='🚻'; }

  booths.push({
    id: id,
    title: type,
    x: 0.2 + Math.random()*0.5,
    y: 0.2 + Math.random()*0.5,
    w: 0.12,
    h: 0.12,
    color: color,
    icon: icon
  });

  updateBoothSelectOptions();
  if(renderMode === '3D') build3DScene();
}

function deleteSelectedBooth(){
  const idx = document.getElementById('selectBoothToResize').value;
  if(booths.length <= 1){ alert("최소 1개 이상의 부스가 필요합니다."); return; }
  booths.splice(idx, 1);
  updateBoothSelectOptions();
  if(renderMode === '3D') build3DScene();
}

/* 2. AI GENERATION & HISTORY */
function generateNewAILayout(){
  const pattern = document.getElementById('optPattern').value;
  const wSafety = parseInt(document.getElementById('wSafety').value);
  const wFlow = parseInt(document.getElementById('wFlow').value);

  // Apply positioning based on pattern option
  booths.forEach((b, idx) => {
    if(b.id === 'stage') return;
    if(pattern === 'grid'){
      b.x = 0.1 + (idx % 3) * 0.28;
      b.y = 0.25 + Math.floor(idx / 3) * 0.25;
    } else if(pattern === 'perimeter'){
      const angle = (idx / booths.length) * Math.PI * 2;
      b.x = 0.45 + Math.cos(angle) * 0.32 - b.w/2;
      b.y = 0.45 + Math.sin(angle) * 0.25 - b.h/2;
    } else {
      b.x = Math.max(0.05, Math.min(0.78, b.x + (Math.random()-0.5)*0.16));
      b.y = Math.max(0.18, Math.min(0.70, b.y + (Math.random()-0.5)*0.14));
    }
  });

  const scS = Math.min(99, Math.max(70, Math.floor(wSafety * 0.9 + Math.random()*10)));
  const scF = Math.min(99, Math.max(70, Math.floor(wFlow * 0.9 + Math.random()*10)));
  const scA = 80 + Math.floor(Math.random()*18);

  const newItem = {
    id: layoutHistory.length + 1,
    time: new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', second:'2-digit'}),
    title: `AI 배치 v${layoutHistory.length + 1} (${pattern.toUpperCase()})`,
    booths: JSON.parse(JSON.stringify(booths)),
    scores: { safety: scS, flow: scF, acc: scA }
  };

  layoutHistory.unshift(newItem);
  currentLayoutIndex = 0;
  loadLayoutFromHistory(0);
}

function loadLayoutFromHistory(index){
  currentLayoutIndex = index;
  const item = layoutHistory[index];
  if(!item) return;

  booths = JSON.parse(JSON.stringify(item.booths));
  document.getElementById('scSafety').textContent = item.scores.safety + '점';
  document.getElementById('scCong').textContent = item.scores.flow + '점';
  document.getElementById('scAcc').textContent = item.scores.acc + '점';

  updateBoothSelectOptions();
  renderHistoryUI();
  if(renderMode === '3D') build3DScene();
}

function renderHistoryUI(){
  const container = document.getElementById('historyContainer');
  container.innerHTML = '';
  layoutHistory.forEach((item, idx) => {
    const isActive = idx === currentLayoutIndex;
    const div = document.createElement('div');
    div.className = `history-item ${isActive ? 'active' : ''}`;
    div.innerHTML = `
      <div>
        <b>${item.title}</b>
        <span style="color:#64748b;font-size:10px;display:block;">${item.time} | 안전: ${item.scores.safety}점</span>
      </div>
      <button class="btn-ui" style="padding:2px 6px;font-size:10px;" onclick="loadLayoutFromHistory(${idx})">
        ${isActive ? '적용중' : '복원'}
      </button>
    `;
    container.appendChild(div);
  });
}

/* 3. SIMULATION CONTROLS & ENVIRONMENT */
function changeEnvironment(){
  envMode = document.getElementById('optWeather').value;
  if(renderMode === '3D' && scene3D){
    if(envMode === 'night') scene3D.background = new THREE.Color(0x030712);
    else scene3D.background = new THREE.Color(0x0f172a);
  }
}

function changeContingency(){
  contingencyMode = document.getElementById('optEmergency').value;
  const stText = document.getElementById('simStatusText');
  const stDetail = document.getElementById('simDetailText');

  if(contingencyMode === 'surge'){
    stText.textContent = '🚨 관람객 밀집 폭주 발생';
    stDetail.textContent = '메인 무대 주변 밀집도가 수용 한계를 초과하고 있습니다.';
  } else if(contingencyMode === 'medical'){
    stText.textContent = '🏥 응급환자 골든타임 통로 확보';
    stDetail.textContent = '중앙 통로를 비우고 양옆으로 관람객을 안내하고 있습니다.';
  } else if(contingencyMode === 'fire'){
    stText.textContent = '🔥 화재 대피 비상령 작동';
    stDetail.textContent = '모든 관람객이 외곽 비상구 방향으로 긴급 대피 중입니다.';
  } else if(contingencyMode === 'vip'){
    stText.textContent = '👑 VIP / 아티스트 전용 동선';
    stDetail.textContent = 'VIP 차량 진입에 따른 보안 경호 구역 통제가 이루어집니다.';
  } else {
    stText.textContent = '✅ 정상 상태 작동 중';
    stDetail.textContent = '관람객이 설정된 AI 동선을 따라 원활히 이동하고 있습니다.';
  }
}

function onPeopleCountChange(){
  const val = parseInt(document.getElementById('optPeopleCount').value);
  document.getElementById('lblPeopleCount').textContent = val;
  adjustPeople(val);
}

function onSpeedChange(){
  simSpeed = parseInt(document.getElementById('optSpeed').value);
  document.getElementById('lblSpeed').textContent = simSpeed + 'x';
}

function togglePause(){
  isPaused = !isPaused;
  document.getElementById('btnPause').textContent = isPaused ? '▶️ 재개' : '⏸️ 일시정지';
}

function toggleOverlay(layer){
  overlays[layer] = !overlays[layer];
  const btn = document.getElementById('toggle' + layer.charAt(0).toUpperCase() + layer.slice(1));
  if(btn) btn.classList.toggle('active', overlays[layer]);
}

function adjustPeople(targetCount){
  const w = venueCanvas ? venueCanvas.width : 500;
  const h = venueCanvas ? venueCanvas.height : 350;
  while(people.length < targetCount){
    people.push({
      x: w*0.1 + Math.random()*w*0.8,
      y: h*0.2 + Math.random()*h*0.6,
      vx: (Math.random()-0.5)*1.5,
      vy: (Math.random()-0.5)*1.5,
      mesh: null
    });
  }
  if(people.length > targetCount){
    people.splice(targetCount);
  }
  if(renderMode === '3D') rebuild3DPeople();
}

/* 4. CANVAS 2D RENDERING LOOP */
function initCanvases(){
  venueCanvas = document.getElementById('venueCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');
  vectorCanvas = document.getElementById('vectorCanvas');

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth || 600;
  const h = wrap.clientHeight || 400;

  [venueCanvas, heatmapCanvas, vectorCanvas].forEach(c => {
    c.width = w; c.height = h;
  });

  venueCtx = venueCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');
  vectorCtx = vectorCanvas.getContext('2d');

  adjustPeople(parseInt(document.getElementById('optPeopleCount').value));
  updateBoothSelectOptions();

  if(layoutHistory.length === 0) generateNewAILayout();

  if(animFrameId) cancelAnimationFrame(animFrameId);
  loopSimulation();
}

function setRenderMode(mode){
  renderMode = mode;
  document.getElementById('btn2D').classList.toggle('active', mode === '2D');
  document.getElementById('btn3D').classList.toggle('active', mode === '3D');

  const canvas3D = document.getElementById('canvas3D');
  if(mode === '3D'){
    canvas3D.style.display = 'block';
    init3D();
  } else {
    canvas3D.style.display = 'none';
  }
}

function loopSimulation(){
  if(!isPaused){
    if(renderMode === '2D' && venueCtx){
      const w = venueCanvas.width;
      const h = venueCanvas.height;
      draw2DBackground(w, h);
      updateAndDraw2DPeople(w, h);
      draw2DOverlays(w, h);
    } else if(renderMode === '3D' && renderer3D){
      update3DPeoplePositions();
      renderer3D.render(scene3D, camera3D);
      if(controls3D) controls3D.update();
    }
  }
  animFrameId = requestAnimationFrame(loopSimulation);
}

function draw2DBackground(w, h){
  // Environment Color
  if(envMode === 'night') venueCtx.fillStyle = '#0f172a';
  else if(envMode === 'rain') venueCtx.fillStyle = '#334155';
  else venueCtx.fillStyle = '#1e3a29'; // Grass
  venueCtx.fillRect(0, 0, w, h);

  // Grid
  if(overlays.grid){
    venueCtx.strokeStyle = 'rgba(255,255,255,0.08)';
    venueCtx.lineWidth = 1;
    for(let x=0; x<w; x+=30){ venueCtx.beginPath(); venueCtx.moveTo(x,0); venueCtx.lineTo(x,h); venueCtx.stroke(); }
    for(let y=0; y<h; y+=30){ venueCtx.beginPath(); venueCtx.moveTo(0,y); venueCtx.lineTo(w,y); venueCtx.stroke(); }
  }

  // Draw Booths
  booths.forEach(b => {
    const bx = b.x * w, by = b.y * h, bw = b.w * w, bh = b.h * h;

    venueCtx.fillStyle = 'rgba(0,0,0,0.3)';
    venueCtx.fillRect(bx+4, by+4, bw, bh);

    venueCtx.fillStyle = b.color;
    venueCtx.beginPath();
    venueCtx.roundRect(bx, by, bw, bh, 6);
    venueCtx.fill();
    venueCtx.strokeStyle = '#ffffff';
    venueCtx.lineWidth = 1.5;
    venueCtx.stroke();

    if(overlays.labels){
      venueCtx.fillStyle = '#ffffff';
      venueCtx.font = 'bold 11px Pretendard';
      venueCtx.textAlign = 'center';
      venueCtx.fillText(`${b.icon} ${b.title}`, bx + bw/2, by + bh/2 + 4);
    }
  });
}

function updateAndDraw2DPeople(w, h){
  people.forEach(p => {
    // Movement Logic
    if(contingencyMode === 'fire'){
      // Flee to outer boundaries
      p.x += (p.x < w/2 ? -2 : 2) * simSpeed;
      p.y += (p.y < h/2 ? -2 : 2) * simSpeed;
    } else if(contingencyMode === 'medical'){
      // Clear central corridor
      if(p.x > w*0.42 && p.x < w*0.58){
        p.x += (p.x < w*0.5 ? -3 : 3) * simSpeed;
      }
    } else if(envMode === 'rain'){
      // Gather in center shelter
      const targetB = booths[0];
      const tx = targetB.x * w + targetB.w*w*0.5;
      const ty = targetB.y * h + targetB.h*h*0.5;
      p.x += (tx - p.x) * 0.02 * simSpeed;
      p.y += (ty - p.y) * 0.02 * simSpeed;
    } else {
      p.x += p.vx * simSpeed * 0.6;
      p.y += p.vy * simSpeed * 0.6;
      if(p.x < 10 || p.x > w-10) p.vx *= -1;
      if(p.y < 10 || p.y > h-10) p.vy *= -1;
    }

    // Render Dot
    venueCtx.fillStyle = envMode === 'night' ? '#38bdf8' : '#ffffff';
    venueCtx.beginPath();
    venueCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
    venueCtx.fill();
  });
}

function draw2DOverlays(w, h){
  heatmapCtx.clearRect(0,0,w,h);
  vectorCtx.clearRect(0,0,w,h);

  if(overlays.heatmap){
    people.forEach(p => {
      let grad = heatmapCtx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 18);
      grad.addColorStop(0, 'rgba(239, 68, 68, 0.25)');
      grad.addColorStop(1, 'rgba(239, 68, 68, 0)');
      heatmapCtx.fillStyle = grad;
      heatmapCtx.beginPath();
      heatmapCtx.arc(p.x, p.y, 18, 0, Math.PI*2);
      heatmapCtx.fill();
    });
  }

  if(overlays.vectors){
    vectorCtx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
    vectorCtx.lineWidth = 1;
    people.forEach(p => {
      vectorCtx.beginPath();
      vectorCtx.moveTo(p.x, p.y);
      vectorCtx.lineTo(p.x + p.vx*12, p.y + p.vy*12);
      vectorCtx.stroke();
    });
  }
}

/* 5. THREE.JS 3D ENGINE */
let scene3D, camera3D, renderer3D, controls3D, booth3DGroup, people3DGroup;

function init3D(){
  const container = document.getElementById('canvas3D');
  if(!container || renderer3D){
    if(renderer3D) build3DScene();
    return;
  }

  const w = container.clientWidth || 600;
  const h = container.clientHeight || 400;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w/h, 1, 1000);
  camera3D.position.set(0, 150, 180);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  controls3D = new THREE.OrbitControls(camera3D, renderer3D.domElement);
  controls3D.enableDamping = true;

  const ambient = new THREE.AmbientLight(0xffffff, 0.8);
  scene3D.add(ambient);

  const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
  dirLight.position.set(50, 100, 50);
  scene3D.add(dirLight);

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(240, 160),
    new THREE.MeshStandardMaterial({ color: 0x1e3a29 })
  );
  ground.rotation.x = -Math.PI / 2;
  scene3D.add(ground);

  booth3DGroup = new THREE.Group();
  people3DGroup = new THREE.Group();
  scene3D.add(booth3DGroup);
  scene3D.add(people3DGroup);

  build3DScene();
}

function build3DScene(){
  if(!booth3DGroup) return;
  while(booth3DGroup.children.length > 0) booth3DGroup.remove(booth3DGroup.children[0]);

  booths.forEach(b => {
    const bw = b.w * 240, bh = b.h * 160;
    const bx = (b.x + b.w/2 - 0.5) * 240;
    const bz = (b.y + b.h/2 - 0.5) * 160;
    const h = b.id === 'stage' ? 14 : 8;

    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(bw, h, bh),
      new THREE.MeshStandardMaterial({ color: new THREE.Color(b.color) })
    );
    mesh.position.set(bx, h/2, bz);
    booth3DGroup.add(mesh);
  });

  rebuild3DPeople();
}

function rebuild3DPeople(){
  if(!people3DGroup) return;
  while(people3DGroup.children.length > 0) people3DGroup.remove(people3DGroup.children[0]);

  const geo = new THREE.SphereGeometry(1.6, 8, 8);
  const mat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

  people.forEach(p => {
    const mesh = new THREE.Mesh(geo, mat);
    people3DGroup.add(mesh);
    p.mesh = mesh;
  });
}

function update3DPeoplePositions(){
  if(!venueCanvas || !people3DGroup) return;
  const w = venueCanvas.width, h = venueCanvas.height;
  people.forEach(p => {
    if(p.mesh){
      p.mesh.position.set((p.x/w - 0.5)*240, 1.6, (p.y/h - 0.5)*160);
    }
  });
}

function exportJSON(){
  const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(booths, null, 2));
  const dlAnchor = document.createElement('a');
  dlAnchor.setAttribute("href", dataStr);
  dlAnchor.setAttribute("download", "event_ai_layout.json");
  document.body.appendChild(dlAnchor);
  dlAnchor.click();
  dlAnchor.remove();
}

window.addEventListener('load', () => {
  initCanvases();
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_FULL_HTML, height=1100, scrolling=True)
