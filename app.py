import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(
    page_title="인터랙티브 행사장 도면 제작기",
    layout="wide"
)

# HTML/CSS/JS 코드 전체를 문자열로 전달
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>인터랙티브 행사장 도면 제작기</title>
  <style>
    :root {
      --bg-primary: #121826;
      --bg-secondary: #1b2438;
      --bg-card: #243048;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --text-main: #f3f4f6;
      --text-sub: #9ca3af;
      --border-color: #374151;
      --indoor-bg: #1e293b;
      --outdoor-bg: #14532d;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    body {
      background-color: var(--bg-primary);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    .sidebar {
      width: 340px;
      background-color: var(--bg-secondary);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 20px;
      gap: 20px;
    }

    .section-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: #60a5fa;
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 6px;
      margin-bottom: 12px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 12px;
    }

    .form-group label {
      font-size: 0.85rem;
      color: var(--text-sub);
    }

    input[type="text"], input[type="number"], select, textarea {
      background-color: var(--bg-primary);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.9rem;
      outline: none;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--accent);
    }

    textarea {
      resize: vertical;
      min-height: 60px;
    }

    .mode-toggle {
      display: flex;
      gap: 8px;
    }

    .mode-btn {
      flex: 1;
      padding: 10px;
      border: 1px solid var(--border-color);
      background-color: var(--bg-card);
      color: var(--text-main);
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }

    .mode-btn.active {
      background-color: var(--accent);
      border-color: var(--accent);
    }

    .toggle-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background-color: var(--bg-card);
      padding: 12px;
      border-radius: 8px;
    }

    .switch {
      position: relative;
      display: inline-block;
      width: 44px;
      height: 24px;
    }

    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .slider {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: #4b5563;
      transition: .3s;
      border-radius: 24px;
    }

    .slider:before {
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
    }

    input:checked + .slider {
      background-color: #ef4444;
    }

    input:checked + .slider:before {
      transform: translateX(20px);
    }

    .palette-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .palette-btn {
      background-color: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
      text-align: center;
      transition: background 0.2s;
    }

    .palette-btn:hover {
      background-color: var(--border-color);
    }

    .stats-card {
      background-color: var(--bg-card);
      padding: 12px;
      border-radius: 8px;
      font-size: 0.85rem;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .stats-card span {
      font-weight: 700;
      color: #34d399;
    }

    .main-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    .toolbar {
      height: 50px;
      background-color: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }

    .canvas-container {
      flex: 1;
      position: relative;
      overflow: hidden;
      background-color: var(--indoor-bg);
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
      background-size: 20px 20px;
      transition: background-color 0.3s;
    }

    .canvas-container.outdoor {
      background-color: var(--outdoor-bg);
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
    }

    .placed-element {
      position: absolute;
      border: 2px solid rgba(255, 255, 255, 0.8);
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 0.8rem;
      color: #ffffff;
      text-shadow: 0 1px 2px rgba(0,0,0,0.8);
      cursor: move;
      user-select: none;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }

    .placed-element.selected {
      border: 2px dashed #f59e0b;
      box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.3);
    }

    .resize-handle {
      position: absolute;
      width: 12px;
      height: 12px;
      background-color: #f59e0b;
      bottom: -6px;
      right: -6px;
      cursor: se-resize;
      border-radius: 2px;
      display: none;
    }

    .placed-element.selected .resize-handle {
      display: block;
    }

    .traffic-svg {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      display: none;
      z-index: 10;
    }

    .flow-path {
      stroke: #f43f5e;
      stroke-width: 4;
      stroke-dasharray: 10, 8;
      fill: none;
      animation: dash 1.5s linear infinite;
    }

    @keyframes dash {
      to {
        stroke-dashoffset: -36;
      }
    }

    .flow-node {
      fill: #f43f5e;
      stroke: #ffffff;
      stroke-width: 2;
    }
  </style>
</head>
<body>

  <div class="sidebar">
    <h2 style="font-size: 1.1rem; font-weight: 800; color: #fff;">🏛️ 행사장 도면 제작기</h2>

    <div>
      <div class="section-title">행사 유형 선택</div>
      <div class="mode-toggle">
        <button class="mode-btn active" id="btn-indoor" onclick="setEventMode('indoor')">🏢 실내 행사</button>
        <button class="mode-btn" id="btn-outdoor" onclick="setEventMode('outdoor')">🌳 야외 행사</button>
      </div>
    </div>

    <div>
      <div class="section-title">행사 기본 정보</div>
      <div class="form-group">
        <label for="event-title">행사명</label>
        <input type="text" id="event-title" value="2026 테크 박람회" oninput="updateStats()">
      </div>
      <div class="form-group">
        <label for="expected-capacity">예상 참가 인원 (명)</label>
        <input type="number" id="expected-capacity" value="1500" min="1" oninput="updateStats()">
      </div>
      <div class="form-group">
        <label for="ticket-fee">입장료 (원)</label>
        <input type="number" id="ticket-fee" value="10000" min="0" step="500" oninput="updateStats()">
      </div>
      <div class="form-group">
        <label for="extra-reqs">추가 요구 사항</label>
        <textarea id="extra-reqs" placeholder="예: 메인무대 220V 전원 인입, 비상구 경로 확보"></textarea>
      </div>
    </div>

    <div>
      <div class="section-title">동선 및 안전 관리</div>
      <div class="toggle-container">
        <span style="font-size: 0.85rem; font-weight: 600;">최적 이동 경로 표시</span>
        <label class="switch">
          <input type="checkbox" id="traffic-toggle" onchange="toggleTrafficFlow(this.checked)">
          <span class="slider"></span>
        </label>
      </div>
    </div>

    <div>
      <div class="section-title">요소 추가</div>
      <div class="palette-grid" id="palette-buttons"></div>
    </div>

    <div id="inspector-panel" style="display: none;">
      <div class="section-title">선택된 요소 설정</div>
      <div class="form-group">
        <label for="elem-label">라벨명</label>
        <input type="text" id="elem-label" oninput="updateSelectedElement()">
      </div>
      <button style="background-color: #ef4444; color: white; border: none; padding: 8px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: 600;" onclick="deleteSelectedElement()">🗑️ 삭제하기</button>
    </div>

    <div>
      <div class="section-title">실시간 산출 정보</div>
      <div class="stats-card">
        <div>예상 총 매출: <span id="stat-revenue">0 원</span></div>
        <div>밀집도 예상: <span id="stat-density">0 명/m²</span></div>
        <div>총 요소 개수: <span id="stat-count">0 개</span></div>
      </div>
    </div>
  </div>

  <div class="main-area">
    <div class="toolbar">
      <span id="current-mode-label" style="font-weight: 700; color: #93c5fd;">모드: 실내 컨벤션 홀</span>
      <button onclick="clearCanvas()" style="background: none; border: 1px solid var(--border-color); color: #fff; padding: 6px 12px; border-radius: 6px; cursor: pointer;">초기화</button>
    </div>

    <div class="canvas-container" id="canvas">
      <svg class="traffic-svg" id="traffic-svg">
        <path class="flow-path" id="flow-path-1" d="M 80,500 C 200,450 250,250 450,250 C 650,250 700,450 850,150" />
        <circle class="flow-node" cx="80" cy="500" r="8" />
        <circle class="flow-node" cx="450" cy="250" r="8" />
        <circle class="flow-node" cx="850" cy="150" r="8" />
        <text x="80" y="530" fill="#ffffff" font-size="12" font-weight="bold">주 출입구 (입장)</text>
        <text x="430" y="220" fill="#ffffff" font-size="12" font-weight="bold">메인 관람 구역</text>
        <text x="830" y="120" fill="#ffffff" font-size="12" font-weight="bold">비상구/퇴장</text>
      </svg>
    </div>
  </div>

  <script>
    let currentMode = 'indoor';
    let elements = [];
    let selectedElementId = null;
    let isDragging = false;
    let isResizing = false;
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    let initialW = 0;
    let initialH = 0;
    let initialMouseX = 0;
    let initialMouseY = 0;

    const paletteConfigs = {
      indoor: [
        { label: '메인 무대', color: '#6366f1', w: 220, h: 100 },
        { label: '전시 부스', color: '#0ea5e9', w: 90, h: 90 },
        { label: '안내 데스크', color: '#10b981', w: 120, h: 60 },
        { label: '관람석/의자', color: '#8b5cf6', w: 160, h: 80 },
        { label: '비상구', color: '#ef4444', w: 80, h: 40 }
      ],
      outdoor: [
        { label: '야외 메인무대', color: '#4f46e5', w: 260, h: 120 },
        { label: '푸드트럭', color: '#f59e0b', w: 110, h: 70 },
        { label: '몽골텐트', color: '#10b981', w: 80, h: 80 },
        { label: '의무실 텐트', color: '#ec4899', w: 90, h: 70 },
        { label: '야외 화장실', color: '#64748b', w: 90, h: 60 }
      ]
    };

    const canvas = document.getElementById('canvas');

    function init() {
      renderPalette();
      loadDefaultPresets();
      updateStats();

      canvas.addEventListener('mousedown', (e) => {
        if (e.target === canvas || e.target.id === 'traffic-svg') {
          selectElement(null);
        }
      });

      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }

    function setEventMode(mode) {
      currentMode = mode;
      document.getElementById('btn-indoor').classList.toggle('active', mode === 'indoor');
      document.getElementById('btn-outdoor').classList.toggle('active', mode === 'outdoor');
      
      const canvasContainer = document.getElementById('canvas');
      const modeLabel = document.getElementById('current-mode-label');

      if (mode === 'indoor') {
        canvasContainer.classList.remove('outdoor');
        modeLabel.innerText = "모드: 실내 컨벤션 홀";
      } else {
        canvasContainer.classList.add('outdoor');
        modeLabel.innerText = "모드: 야외 페스티벌 광장";
      }

      renderPalette();
      clearCanvas();
      loadDefaultPresets();
    }

    function renderPalette() {
      const container = document.getElementById('palette-buttons');
      container.innerHTML = '';
      
      paletteConfigs[currentMode].forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'palette-btn';
        btn.innerText = `+ ${item.label}`;
        btn.onclick = () => addElement(item.label, item.color, item.w, item.h);
        container.appendChild(btn);
      });
    }

    function loadDefaultPresets() {
      if (currentMode === 'indoor') {
        addElement('메인 무대', '#6366f1', 240, 100, 250, 40);
        addElement('전시 부스 A', '#0ea5e9', 100, 100, 120, 200);
        addElement('전시 부스 B', '#0ea5e9', 100, 100, 250, 200);
        addElement('안내 데스크', '#10b981', 140, 60, 40, 420);
        addElement('비상구', '#ef4444', 80, 40, 600, 80);
      } else {
        addElement('야외 메인무대', '#4f46e5', 260, 120, 220, 30);
        addElement('푸드트럭 01', '#f59e0b', 110, 70, 80, 220);
        addElement('푸드트럭 02', '#f59e0b', 110, 70, 80, 310);
        addElement('몽골텐트 A', '#10b981', 90, 90, 400, 220);
        addElement('의무실 텐트', '#ec4899', 90, 70, 600, 100);
      }
    }

    function addElement(label, color, w = 100, h = 80, customX, customY) {
      const id = 'elem_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
      const x = customX !== undefined ? customX : Math.floor(Math.random() * 150) + 80;
      const y = customY !== undefined ? customY : Math.floor(Math.random() * 150) + 80;

      const elementData = { id, label, color, x, y, width: w, height: h };
      elements.push(elementData);

      renderElementNode(elementData);
      selectElement(id);
      updateStats();
    }

    function renderElementNode(data) {
      const node = document.createElement('div');
      node.className = 'placed-element';
      node.id = data.id;
      node.style.backgroundColor = data.color;
      node.style.left = data.x + 'px';
      node.style.top = data.y + 'px';
      node.style.width = data.width + 'px';
      node.style.height = data.height + 'px';

      const labelSpan = document.createElement('span');
      labelSpan.className = 'node-label';
      labelSpan.innerText = data.label;
      node.appendChild(labelSpan);

      const handle = document.createElement('div');
      handle.className = 'resize-handle';
      node.appendChild(handle);

      node.addEventListener('mousedown', (e) => {
        e.stopPropagation();
        selectElement(data.id);

        if (e.target === handle) {
          isResizing = true;
          initialW = data.width;
          initialH = data.height;
          initialMouseX = e.clientX;
          initialMouseY = e.clientY;
        } else {
          isDragging = true;
          dragOffsetX = e.clientX - data.x;
          dragOffsetY = e.clientY - data.y;
        }
      });

      canvas.appendChild(node);
    }

    function handleMouseMove(e) {
      if (!selectedElementId) return;
      const elemData = elements.find(el => el.id === selectedElementId);
      if (!elemData) return;

      if (isDragging) {
        let newX = e.clientX - dragOffsetX;
        let newY = e.clientY - dragOffsetY;

        const canvasRect = canvas.getBoundingClientRect();
        newX = Math.max(0, Math.min(newX, canvasRect.width - elemData.width));
        newY = Math.max(0, Math.min(newY, canvasRect.height - elemData.height));

        elemData.x = newX;
        elemData.y = newY;

        const node = document.getElementById(elemData.id);
        node.style.left = newX + 'px';
        node.style.top = newY + 'px';
      } else if (isResizing) {
        const deltaX = e.clientX - initialMouseX;
        const deltaY = e.clientY - initialMouseY;

        const newW = Math.max(40, initialW + deltaX);
        const newH = Math.max(30, initialH + deltaY);

        elemData.width = newW;
        elemData.height = newH;

        const node = document.getElementById(elemData.id);
        node.style.width = newW + 'px';
        node.style.height = newH + 'px';
      }
    }

    function handleMouseUp() {
      isDragging = false;
      isResizing = false;
    }

    function selectElement(id) {
      selectedElementId = id;
      document.querySelectorAll('.placed-element').forEach(el => {
        el.classList.toggle('selected', el.id === id);
      });

      const inspector = document.getElementById('inspector-panel');
      if (id) {
        const elemData = elements.find(el => el.id === id);
        if (elemData) {
          inspector.style.display = 'block';
          document.getElementById('elem-label').value = elemData.label;
        }
      } else {
        inspector.style.display = 'none';
      }
    }

    function updateSelectedElement() {
      if (!selectedElementId) return;
      const elemData = elements.find(el => el.id === selectedElementId);
      if (elemData) {
        const newLabel = document.getElementById('elem-label').value;
        elemData.label = newLabel;
        const node = document.getElementById(selectedElementId);
        if (node) {
          node.querySelector('.node-label').innerText = newLabel;
        }
      }
    }

    function deleteSelectedElement() {
      if (!selectedElementId) return;
      elements = elements.filter(el => el.id !== selectedElementId);
      const node = document.getElementById(selectedElementId);
      if (node) node.remove();
      selectElement(null);
      updateStats();
    }

    function clearCanvas() {
      elements = [];
      document.querySelectorAll('.placed-element').forEach(node => node.remove());
      selectElement(null);
      updateStats();
    }

    function toggleTrafficFlow(show) {
      const svg = document.getElementById('traffic-svg');
      svg.style.display = show ? 'block' : 'none';
    }

    function updateStats() {
      const capacity = parseInt(document.getElementById('expected-capacity').value) || 0;
      const fee = parseInt(document.getElementById('ticket-fee').value) || 0;

      const totalRevenue = capacity * fee;
      document.getElementById('stat-revenue').innerText = totalRevenue.toLocaleString() + ' 원';

      const density = (capacity / 1000).toFixed(2);
      document.getElementById('stat-density').innerText = density + ' 명/m²';
      document.getElementById('stat-count').innerText = elements.length + ' 개';
    }

    window.onload = init;
  </script>
</body>
</html>
"""

# Streamlit 내부에 렌더링
components.html(html_code, height=850, scrolling=False)
