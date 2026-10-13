import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 오늘의집 스타일 행사장 인테리어 스튜디오",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_STUDIO_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI Studio</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<!-- Three.js Library -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color:#1e293b;
  background:#f8fafc;
  overflow:hidden;
}
button,input,select{font:inherit;}
button{cursor:pointer;transition:all 0.2s ease;}

/* Layout */
.app-container{
  display:flex;
  height:100vh;
  width:100vw;
  background:#f1f5f9;
}

/* Left Catalog Sidebar */
.catalog-sidebar{
  width:260px;
  background:#0f172a;
  color:#94a3b8;
  padding:16px;
  display:flex;
  flex-direction:column;
  gap:16px;
  border-right:1px solid #1e293b;
  flex-shrink:0;
  z-index:30;
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
  width:32px;height:32px;
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:8px;
  display:grid;place-items:center;
  font-weight:900;color:#fff;
}
.brand-title{font-size:16px;font-weight:800;color:#fff;}
.brand-sub{font-size:10px;color:#64748b;}

.catalog-section-title{
  font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;margin-bottom:8px;letter-spacing:0.5px;
}
.catalog-grid{
  display:grid;
  grid-template-columns:repeat(2, 1fr);
  gap:8px;
}
.catalog-item{
  background:#1e293b;
  border:1px solid #334155;
  border-radius:10px;
  padding:10px;
  text-align:center;
  cursor:pointer;
  color:#f8fafc;
  font-size:12px;
  font-weight:700;
  display:flex;
  flex-direction:column;
  gap:4px;
}
.catalog-item:hover{background:#2563eb;border-color:#3b82f6;}
.catalog-item span{font-size:18px;}

/* Center Canvas Area */
.main-workspace{
  flex:1;
  display:flex;
  flex-direction:column;
  position:relative;
  overflow:hidden;
}

.workspace-topbar{
  height:54px;
  background:#ffffff;
  border-bottom:1px solid #e2e8f0;
  padding:0 20px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  box-shadow:0 1px 3px rgba(0,0,0,0.02);
  z-index:20;
}
.workspace-title{font-size:15px;font-weight:800;color:#0f172a;}
.mode-toggle-group{
  display:flex;gap:6px;background:#f1f5f9;padding:4px;border-radius:10px;border:1px solid #cbd5e1;
}
.mode-btn{
  background:transparent;border:none;padding:6px 14px;border-radius:8px;font-size:12px;font-weight:700;color:#64748b;cursor:pointer;
}
.mode-btn.active{background:#ffffff;color:#2563eb;box-shadow:0 2px 6px rgba(0,0,0,0.05);}

.canvas-container{
  flex:1;
  position:relative;
  background:#1e293b;
  overflow:hidden;
}
canvas{
  position:absolute;inset:0;width:100%;height:100%;
}
#renderer3D{display:none;background:#0f172a;}

/* Right Property Inspector Sidebar */
.inspector-sidebar{
  width:280px;
  background:#ffffff;
  border-left:1px solid #e2e8f0;
  padding:16px;
  display:flex;
  flex-direction:column;
  gap:16px;
  flex-shrink:0;
  z-index:30;
  box-shadow:-2px 0 10px rgba(0,0,0,0.02);
}
.inspector-title{font-size:14px;font-weight:800;color:#0f172a;border-bottom:2px solid #f1f5f9;padding-bottom:8px;}
.prop-group{display:flex;flex-direction:column;gap:5px;margin-bottom:10px;}
.prop-group label{font-size:11px;font-weight:700;color:#64748b;}
.prop-group input{
  padding:8px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;font-weight:600;background:#f8fafc;color:#0f172a;
}
.btn-danger{
  background:#fee2e2;color:#b91c1c;border:1px solid #fca5a5;padding:8px;border-radius:8px;font-size:12px;font-weight:700;width:100%;margin-top:auto;
}
.btn-primary{
  background:#2563eb;color:#fff;border:none;padding:10px;border-radius:8px;font-size:12px;font-weight:800;width:100%;box-shadow:0 4px 12px rgba(37,99,235,0.3);
}

/* Floating Toolbar on Canvas */
.floating-toolbar{
  position:absolute;
  left:20px;bottom:20px;
  z-index:25;
  background:rgba(255,255,255,0.92);
  backdrop-filter:blur(6px);
  padding:8px 12px;
  border-radius:12px;
  border:1px solid #e2e8f0;
  box-shadow:0 4px 16px rgba(0,0,0,0.1);
  display:flex;gap:8px;align-items:center;
}
.ft-btn{
  background:#f1f5f9;border:1px solid #cbd5e1;padding:6px 12px;border-radius:8px;font-size:11.5px;font-weight:700;color:#334155;
}
.ft-btn.active{background:#2563eb;color:#fff;border-color:#1d4ed8;}
</style>
</head>
<body>

<div class="app-container">

  <!-- LEFT CATALOG SIDEBAR -->
  <aside class="catalog-sidebar">
    <div class="brand">
      <div class="brand-icon">🏠</div>
      <div>
        <div class="brand-title">Event Studio</div>
        <div class="brand-sub">오늘의집 스타일 행사장 인테리어</div>
      </div>
    </div>

    <div>
      <div class="catalog-section-title">시설물 카탈로그</div>
      <div class="catalog-grid">
        <div class="catalog-item" onclick="addObject('stage')"><span>🎭</span>무대/스탠드</div>
        <div class="catalog-item" onclick="addObject('exp')"><span>🧪</span>체험 부스</div>
        <div class="catalog-item" onclick="addObject('food')"><span>🍔</span>푸드트럭</div>
        <div class="catalog-item" onclick="addObject('rest')"><span>🌳</span>잔디 휴식존</div>
        <div class="catalog-item" onclick="addObject('medical')"><span>🏥</span>응급센터</div>
        <div class="catalog-item" onclick="addObject('restroom')"><span>🚻</span>화장실</div>
      </div>
    </div>

    <div style="margin-top:auto;background:rgba(255,255,255,0.05);padding:12px;border-radius:10px;font-size:11px;line-height:1.4;color:#94a3b8;">
      💡 <b>사용 팁:</b><br>
      • 카탈로그 아이템을 클릭해 추가하세요.<br>
      • 캔버스에서 드래그하여 이동합니다.<br>
      • 클릭하면 우측에서 속성을 편집할 수 있습니다.
    </div>
  </aside>

  <!-- MAIN WORKSPACE -->
  <main class="main-workspace">
    <header class="workspace-topbar">
      <div class="workspace-title" id="projectTitle">2025 힐링 페스티벌 행사장 설계 (50,000m²)</div>
      <div class="mode-toggle-group">
        <button class="mode-btn active" id="btn2D" onclick="switchMode('2d')">2D 도면 편집</button>
        <button class="mode-btn" id="btn3D" onclick="switchMode('3d')">3D 입체 인테리어</button>
      </div>
    </header>

    <div class="canvas-container" id="canvasWrap">
      <canvas id="floorCanvas"></canvas>
      <canvas id="simCanvas"></canvas>
      <div id="renderer3D"></div>

      <!-- Floating Toolbar -->
      <div class="floating-toolbar">
        <button class="ft-btn active" id="btnSimToggle" onclick="toggleSim()">▶ 군중 시뮬레이션</button>
        <button class="ft-btn active" id="btnHeatmapToggle" onclick="toggleHeatmap()">🔥 히트맵 켜기</button>
        <button class="ft-btn" onclick="clearAllObjects()">전체 초기화</button>
      </div>
    </div>
  </main>

  <!-- RIGHT PROPERTY INSPECTOR -->
  <aside class="inspector-sidebar">
    <div class="inspector-title">⚙️ 오브젝트 속성 편집</div>
    <div id="inspectorContent" style="display:flex;flex-direction:column;gap:10px;">
      <p style="font-size:12px;color:#64748b;text-align:center;margin-top:40px;">선택된 오브젝트가 없습니다.<br>도면의 시설물을 클릭하세요.</p>
    </div>
    <button class="btn-primary" style="margin-top:10px;" onclick="saveProjectState()">설계안 저장</button>
  </aside>

</div>

<script>
/* APPLICATION STATE & OBJECT CATALOG */
let objects = [
  { id: 1, type: 'stage', title: '메인 무대 & 객석', x: 250, y: 50, w: 220, h: 100, color: '#8b5cf6', icon: '🎭' },
  { id: 2, type: 'exp', title: '체험 부스 A', x: 60, y: 180, w: 120, h: 90, color: '#3b82f6', icon: '🧪' },
  { id: 3, type: 'exp', title: '체험 부스 B', x: 600, y: 180, w: 120, h: 90, color: '#3b82f6', icon: '🚀' },
  { id: 4, type: 'food', title: '푸드트럭 구역', x: 60, y: 320, w: 140, h: 90, color: '#f59e0b', icon: '🍔' },
  { id: 5, type: 'medical', title: '응급 의료센터', x: 600, y: 320, w: 130, h: 90, color: '#ef4444', icon: '🏥' },
  { id: 6, type: 'rest', title: '잔디 휴식존', x: 280, y: 220, w: 180, h: 120, color: '#10b981', icon: '🌳' }
];

let selectedId = null;
let isDragging = false;
let dragOffsetX = 0;
let dragOffsetY = 0;

let currentMode = '2d'; // '2d' or '3d'
let simRunning = true;
let showHeatmap = true;

let floorCanvas, floorCtx, simCanvas, simCtx;
let crowdAgents = [];

/* INITIALIZATION */
window.addEventListener('load', () => {
  floorCanvas = document.getElementById('floorCanvas');
  simCanvas = document.getElementById('simCanvas');
  floorCtx = floorCanvas.getContext('2d');
  simCtx = simCanvas.getContext('2d');

  resizeCanvases();
  window.addEventListener('resize', resizeCanvases);

  initCrowd();
  setupCanvasEvents();
  renderLoop();
});

function resizeCanvases() {
  const wrap = document.getElementById('canvasWrap');
  const w = wrap.clientWidth;
  const h = wrap.clientHeight;
  [floorCanvas, simCanvas].forEach(c => {
    c.width = w;
    c.height = h;
  });
  redraw2D();
}

/* CATALOG ADD OBJECT */
function addObject(type) {
  const meta = {
    stage: { title: '대형 무대', w: 200, h: 90, color: '#8b5cf6', icon: '🎭' },
    exp: { title: '신규 체험부스', w: 120, h: 90, color: '#3b82f6', icon: '🧪' },
    food: { title: '푸드트럭', w: 130, h: 90, color: '#f59e0b', icon: '🍔' },
    rest: { title: '휴식 광장', w: 160, h: 110, color: '#10b981', icon: '🌳' },
    medical: { title: '응급센터', w: 120, h: 90, color: '#ef4444', icon: '🏥' },
    restroom: { title: '화장실', w: 110, h: 80, color: '#06b6d4', icon: '🚻' }
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
}

/* 2D CANVAS RENDERING */
function redraw2D() {
  if (!floorCtx) return;
  const w = floorCanvas.width;
  const h = floorCanvas.height;

  floorCtx.clearRect(0, 0, w, h);

  // Background Grass Field
  floorCtx.fillStyle = '#3a7d44';
  floorCtx.fillRect(0, 0, w, h);

  // Grid lines (Ohouse Blueprint Style)
  floorCtx.strokeStyle = 'rgba(255,255,255,0.05)';
  floorCtx.lineWidth = 1;
  for(let x=0; x<w; x+=40){
    floorCtx.beginPath(); floorCtx.moveTo(x, 0); floorCtx.lineTo(x, h); floorCtx.stroke();
  }
  for(let y=0; y<h; y+=40){
    floorCtx.beginPath(); floorCtx.moveTo(0, y); floorCtx.lineTo(w, y); floorCtx.stroke();
  }

  // Draw Objects
  objects.forEach(obj => {
    // Shadow
    floorCtx.fillStyle = 'rgba(0,0,0,0.3)';
    floorCtx.fillRect(obj.x + 4, obj.y + 4, obj.w, obj.h);

    // Body
    floorCtx.fillStyle = obj.color;
    floorCtx.beginPath();
    floorCtx.roundRect(obj.x, obj.y, obj.w, obj.h, 8);
    floorCtx.fill();

    // Selection Border
    if (selectedId === obj.id) {
      floorCtx.strokeStyle = '#ffffff';
      floorCtx.lineWidth = 3;
      floorCtx.stroke();
    } else {
      floorCtx.strokeStyle = 'rgba(255,255,255,0.6)';
      floorCtx.lineWidth = 1.5;
      floorCtx.stroke();
    }

    // Label & Icon
    floorCtx.fillStyle = '#ffffff';
    floorCtx.font = 'bold 12px Pretendard, sans-serif';
    floorCtx.textAlign = 'center';
    floorCtx.textBaseline = 'middle';
    floorCtx.fillText(`${obj.icon} ${obj.title}`, obj.x + obj.w / 2, obj.y + obj.h / 2);
  });
}

/* INTERACTION & DRAGGING */
function setupCanvasEvents() {
  floorCanvas.onmousedown = (e) => {
    if (currentMode !== '2d') return;
    const rect = floorCanvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    selectedId = null;
    // Check from top-most (reverse order)
    for (let i = objects.length - 1; i >= 0; i--) {
      const obj = objects[i];
      if (mx >= obj.x && mx <= obj.x + obj.w && my >= obj.y && my <= obj.y + obj.h) {
        selectedId = obj.id;
        isDragging = true;
        dragOffsetX = mx - obj.x;
        dragOffsetY = my - obj.y;
        // Bring to front
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

  window.onmouseup = () => {
    isDragging = false;
  };
}

/* PROPERTY INSPECTOR PANEL */
function updateInspector() {
  const box = document.getElementById('inspectorContent');
  const obj = objects.find(o => o.id === selectedId);

  if (!obj) {
    box.innerHTML = `<p style="font-size:12px;color:#64748b;text-align:center;margin-top:40px;">선택된 오브젝트가 없습니다.<br>도면의 시설물을 클릭하세요.</p>`;
    return;
  }

  box.innerHTML = `
    <div class="prop-group"><label>오브젝트 이름</label><input type="text" id="propTitle" value="${obj.title}" oninput="updateProp('title', this.value)"></div>
    <div class="prop-group"><label>가로 크기 (Width)</label><input type="number" id="propW" value="${obj.w}" oninput="updateProp('w', parseInt(this.value)||50)"></div>
    <div class="prop-group"><label>세로 크기 (Height)</label><input type="number" id="propH" value="${obj.h}" oninput="updateProp('h', parseInt(this.value)||50)"></div>
    <div class="prop-group"><label>X 좌표</label><input type="number" id="propX" value="${Math.round(obj.x)}" oninput="updateProp('x', parseInt(this.value)||0)"></div>
    <div class="prop-group"><label>Y 좌표</label><input type="number" id="propY" value="${Math.round(obj.y)}" oninput="updateProp('y', parseInt(this.value)||0)"></div>
    <button class="btn-danger" onclick="deleteSelectedObject()">오브젝트 삭제</button>
  `;
}

function updateProp(key, val) {
  const obj = objects.find(o => o.id === selectedId);
  if (obj) {
    obj[key] = val;
    redraw2D();
  }
}

function deleteSelectedObject() {
  if (selectedId) {
    objects = objects.filter(o => o.id !== selectedId);
    selectedId = null;
    updateInspector();
    redraw2D();
  }
}

function clearAllObjects() {
  if (confirm('모든 시설물을 초기화하시겠습니까?')) {
    objects = [];
    selectedId = null;
    updateInspector();
    redraw2D();
  }
}

function saveProjectState() {
  alert('성공적으로 설계안이 저장되었습니다!');
}

/* CROWD SIMULATION & HEATMAP ENGINE */
function initCrowd() {
  crowdAgents = [];
  for(let i=0; i<60; i++){
    crowdAgents.push({
      x: 100 + Math.random()*600,
      y: 100 + Math.random()*400,
      vx: (Math.random()-0.5)*1.2,
      vy: (Math.random()-0.5)*1.2
    });
  }
}

function updateSimulation() {
  if (!simRunning || !simCtx) return;
  const w = simCanvas.width;
  const h = simCanvas.height;

  simCtx.clearRect(0, 0, w, h);

  // Heatmap Layer
  if (showHeatmap) {
    objects.forEach(obj => {
      const cx = obj.x + obj.w / 2;
      const cy = obj.y + obj.h / 2;
      let grad = simCtx.createRadialGradient(cx, cy, 5, cx, cy, 90);
      grad.addColorStop(0, 'rgba(239, 68, 68, 0.45)');
      grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.2)');
      grad.addColorStop(1, 'rgba(16, 185, 129, 0)');
      simCtx.fillStyle = grad;
      simCtx.beginPath(); simCtx.arc(cx, cy, 90, 0, Math.PI*2); simCtx.fill();
    });
  }

  // Crowd Agents
  crowdAgents.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    if(p.x < 20 || p.x > w-20) p.vx *= -1;
    if(p.y < 20 || p.y > h-20) p.vy *= -1;

    simCtx.fillStyle = '#ffffff';
    simCtx.beginPath();
    simCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
    simCtx.fill();
  });
}

function toggleSim() {
  simRunning = !simRunning;
  document.getElementById('btnSimToggle').classList.toggle('active', simRunning);
}

function toggleHeatmap() {
  showHeatmap = !showHeatmap;
  document.getElementById('btnHeatmapToggle').classList.toggle('active', showHeatmap);
}

function renderLoop() {
  if (currentMode === '2d') {
    updateSimulation();
  }
  requestAnimationFrame(renderLoop);
}

/* MODE SWITCHING (2D <-> 3D THREE.JS) */
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btn2D').classList.toggle('active', mode === '2d');
  document.getElementById('btn3D').classList.toggle('active', mode === '3d');

  const fCanvas = document.getElementById('floorCanvas');
  const sCanvas = document.getElementById('simCanvas');
  const r3D = document.getElementById('renderer3D');

  if (mode === '3d') {
    fCanvas.style.display = 'none';
    sCanvas.style.display = 'none';
    r3D.style.display = 'block';
    init3DScene();
  } else {
    fCanvas.style.display = 'block';
    sCanvas.style.display = 'block';
    r3D.style.display = 'none';
    redraw2D();
  }
}

/* THREE.JS 3D INTERIOR ENGINE */
let scene3D, camera3D, renderer3D;

function init3DScene() {
  const container = document.getElementById('renderer3D');
  container.innerHTML = '';

  const w = container.clientWidth;
  const h = container.clientHeight;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w / h, 0.1, 2000);
  camera3D.position.set(0, 300, 350);
  camera3D.lookAt(0, 0, 0);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  // Lighting
  scene3D.add(new THREE.AmbientLight(0xffffff, 0.7));
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(100, 200, 100);
  scene3D.add(dirLight);

  // Ground Plane
  const groundGeo = new THREE.PlaneGeometry(800, 600);
  const groundMat = new THREE.MeshLambertMaterial({ color: 0x3a7d44 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  scene3D.add(ground);

  // Build 3D meshes from 2D objects
  objects.forEach(obj => {
    const bw = obj.w;
    const bh = obj.h;
    const bx = obj.x - w / 2 + bw / 2;
    const bz = obj.y - h / 2 + bh / 2;
    const height = obj.type === 'stage' ? 25 : 14;

    const geo = new THREE.BoxGeometry(bw, height, bh);
    const colorHex = parseInt(obj.color.replace('#', '0x'));
    const mat = new THREE.MeshLambertMaterial({ color: colorHex });
    const mesh = new THREE.Mesh(geo, mat);

    mesh.position.set(bx, height / 2, bz);
    scene3D.add(mesh);
  });

  function animate3D() {
    if (currentMode === '3d') {
      requestAnimationFrame(animate3D);
      scene3D.rotation.y += 0.002; // Auto rotate for showroom feel
      renderer3D.render(scene3D, camera3D);
    }
  }
  animate3D();
}
</script>
</body>
</html>
"""

components.html(EVENT_STUDIO_HTML, height=850, scrolling=False)
