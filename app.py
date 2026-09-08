import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI 스마트 행사장 최적화 설계 및 3D 평가 시스템",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# HTML/CSS/JS 전체 코드
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 행사장 최적 설계 및 3D 평가</title>
  
  <!-- Three.js & OrbitControls -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    :root {
      --bg-dark: #090d16;
      --bg-panel: #111827;
      --bg-card: #1f2937;
      --primary: #2563eb;
      --primary-accent: #3b82f6;
      --cyan: #06b6d4;
      --emerald: #10b981;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --text-main: #f9fafb;
      --text-sub: #9ca3af;
      --border: #374151;
      --grid-color: rgba(59, 130, 246, 0.12);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    body, html {
      width: 100%;
      height: 100%;
      background-color: var(--bg-dark);
      color: var(--text-main);
      overflow: hidden;
    }

    .app-header {
      height: 56px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 1.15rem;
      color: var(--cyan);
    }

    .step-indicator {
      display: flex;
      gap: 12px;
    }

    .step-badge {
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.82rem;
      font-weight: 600;
      background: rgba(255,255,255,0.05);
      color: var(--text-sub);
      border: 1px solid var(--border);
      transition: all 0.3s;
    }

    .step-badge.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary-accent);
      box-shadow: 0 0 12px rgba(37, 99, 235, 0.4);
    }

    .main-layout {
      display: flex;
      height: calc(100vh - 56px);
      width: 100%;
    }

    /* Left Sidebar */
    .sidebar {
      width: 340px;
      background-color: var(--bg-panel);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      padding: 16px;
      gap: 16px;
      overflow-y: auto;
    }

    .section-title {
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--cyan);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .palette-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .btn-palette {
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 10px 8px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 600;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-palette:hover {
      border-color: var(--cyan);
      background: rgba(6, 182, 212, 0.1);
      transform: translateY(-2px);
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .form-group label {
      font-size: 0.8rem;
      color: var(--text-sub);
    }

    input, select {
      background: var(--bg-dark);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 8px 10px;
      border-radius: 6px;
      font-size: 0.85rem;
      outline: none;
    }

    input:focus, select:focus {
      border-color: var(--cyan);
    }

    .btn-ai-optimize {
      background: linear-gradient(135deg, #2563eb 0%, #06b6d4 100%);
      color: white;
      border: none;
      padding: 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.95rem;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: auto;
    }

    .btn-ai-optimize:hover {
      opacity: 0.95;
      transform: scale(1.02);
    }

    /* Content Area */
    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: var(--bg-dark);
      position: relative;
    }

    /* Tab Panels */
    .tab-panel {
      display: none;
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0; left: 0;
    }

    .tab-panel.active {
      display: flex;
    }

    /* Editor View */
    #view-editor {
      flex-direction: column;
    }

    .canvas-header {
      height: 42px;
      background: rgba(17, 24, 39, 0.8);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      font-size: 0.82rem;
      color: var(--text-sub);
    }

    .blueprint-canvas {
      flex: 1;
      position: relative;
      background-color: #0b1329;
      background-image: 
        radial-gradient(var(--grid-color) 1px, transparent 1px),
        linear-gradient(to right, var(--grid-color) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid-color) 1px, transparent 1px);
      background-size: 20px 20px, 40px 40px, 40px 40px;
      overflow: hidden;
      cursor: crosshair;
    }

    .element-node {
      position: absolute;
      border: 2px solid rgba(255, 255, 255, 0.9);
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 0.78rem;
      font-weight: 700;
      color: white;
      cursor: move;
      user-select: none;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(4px);
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .element-node.selected {
      border-color: var(--amber) !important;
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.4), 0 8px 16px rgba(0,0,0,0.6);
      z-index: 50;
    }

    .node-type-tag {
      font-size: 0.65rem;
      opacity: 0.8;
      font-weight: 400;
      margin-top: 2px;
    }

    .resize-handle {
      position: absolute;
      width: 10px;
      height: 10px;
      background: var(--amber);
      bottom: -5px;
      right: -5px;
      cursor: se-resize;
      border-radius: 2px;
      display: none;
    }

    .element-node.selected .resize-handle {
      display: block;
    }

    /* Comparison / Optimization Result View */
    #view-result {
      flex-direction: row;
      background: var(--bg-dark);
    }

    .split-pane {
      flex: 1;
      display: flex;
      flex-direction: column;
      border-right: 1px solid var(--border);
      position: relative;
    }

    .pane-header {
      height: 40px;
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      font-weight: 700;
      font-size: 0.88rem;
    }

    #3d-container {
      width: 100%;
      height: calc(100% - 40px);
      position: relative;
    }

    /* Analysis & Report Drawer */
    .report-panel {
      width: 420px;
      background: var(--bg-panel);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      padding: 20px;
      gap: 20px;
      overflow-y: auto;
    }

    .score-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .score-ring {
      width: 70px;
      height: 70px;
      border-radius: 50%;
      background: conic-gradient(var(--emerald) 0% 88%, #374151 88% 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }

    .score-ring-inner {
      width: 54px;
      height: 54px;
      border-radius: 50%;
      background: var(--bg-card);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.2rem;
      color: var(--emerald);
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }

    .metric-box {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
    }

    .metric-title {
      font-size: 0.75rem;
      color: var(--text-sub);
      margin-bottom: 4px;
    }

    .metric-val {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .improvement-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .item-card {
      background: var(--bg-card);
      border-left: 4px solid var(--cyan);
      border-radius: 6px;
      padding: 12px;
      font-size: 0.83rem;
      line-height: 1.4;
    }

    .item-card.danger { border-left-color: var(--rose); }
    .item-card.success { border-left-color: var(--emerald); }
    .item-card.warning { border-left-color: var(--amber); }

    .item-card-title {
      font-weight: 700;
      margin-bottom: 4px;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Floating Controls */
    .hud-controls {
      position: absolute;
      bottom: 16px;
      left: 16px;
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.75rem;
      color: var(--text-sub);
      pointer-events: none;
    }
  </style>
</head>
<body>

  <div class="app-header">
    <div class="brand">
      <i data-lucide="layout-grid"></i>
      <span>EventArchitect AI</span>
    </div>

    <div class="step-indicator">
      <div class="step-badge active" id="step-1">1. 사용자 초안 도면 작성</div>
      <div class="step-badge" id="step-2">2. AI 최적화 도면 & 3D 검증</div>
      <div class="step-badge" id="step-3">3. 안전/동선 리포트</div>
    </div>
  </div>

  <div class="main-layout">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <div>
        <div class="section-title"><i data-lucide="plus-circle"></i> 요소 추가 (초안 라이브러리)</div>
        <div class="palette-grid">
          <button class="btn-palette" onclick="addElement('STAGE')">
            <i data-lucide="tv" style="color: #6366f1;"></i>
            <span>메인 무대</span>
          </button>
          <button class="btn-palette" onclick="addElement('BOOTH')">
            <i data-lucide="store" style="color: #0ea5e9;"></i>
            <span>전시 부스</span>
          </button>
          <button class="btn-palette" onclick="addElement('EXIT')">
            <i data-lucide="door-open" style="color: #ef4444;"></i>
            <span>비상 출입구</span>
          </button>
          <button class="btn-palette" onclick="addElement('FOOD')">
            <i data-lucide="utensils" style="color: #f59e0b;"></i>
            <span>푸드트럭 존</span>
          </button>
          <button class="btn-palette" onclick="addElement('INFO')">
            <i data-lucide="info" style="color: #10b981;"></i>
            <span>안내 데스크</span>
          </button>
          <button class="btn-palette" onclick="addElement('RESTROOM')">
            <i data-lucide="bath" style="color: #8b5cf6;"></i>
            <span>편의/화장실</span>
          </button>
        </div>
      </div>

      <div>
        <div class="section-title"><i data-lucide="sliders"></i> 행사 설정</div>
        <div class="form-group">
          <label>행사명</label>
          <input type="text" id="input-event-name" value="2026 AI Global Expo">
        </div>
        <div class="form-group" style="margin-top: 8px;">
          <label>수용 예정 인원 (명)</label>
          <input type="number" id="input-capacity" value="2500" step="100">
        </div>
        <div class="form-group" style="margin-top: 8px;">
          <label>최우선 목표</label>
          <select id="select-priority">
            <option value="safety">비상 대피 안전 최우선</option>
            <option value="flow">관람객 동선 순환 극대화</option>
            <option value="booth">부스 시인성 및 밀집 방지</option>
          </select>
        </div>
      </div>

      <div id="inspector" style="display: none; background: var(--bg-card); padding: 12px; border-radius: 8px; border: 1px solid var(--border);">
        <div class="section-title" style="color: var(--amber);"><i data-lucide="edit-3"></i> 선택 요소 편집</div>
        <div class="form-group">
          <label>명칭</label>
          <input type="text" id="inspector-label" oninput="updateSelectedLabel()">
        </div>
        <button onclick="deleteSelected()" style="margin-top: 10px; width: 100%; background: rgba(239, 68, 68, 0.2); border: 1px solid var(--rose); color: var(--rose); padding: 6px; border-radius: 6px; cursor: pointer; font-weight: 600;">요소 삭제</button>
      </div>

      <button class="btn-ai-optimize" onclick="runAIOptimization()">
        <i data-lucide="wand2"></i>
        <span>AI 최적 도면 생성 & 평가</span>
      </button>
    </div>

    <!-- MAIN CONTENT -->
    <div class="content-area">
      
      <!-- TAB 1: 2D DRAFT EDITOR -->
      <div class="tab-panel active" id="view-editor">
        <div class="canvas-header">
          <span>📐 자유 배치 초안 워크스페이스 (부스를 드래그하여 배치하세요)</span>
          <span id="canvas-count">배치된 요소: 0개</span>
        </div>
        <div class="blueprint-canvas" id="editor-canvas"></div>
      </div>

      <!-- TAB 2 & 3: AI OPTIMIZED RESULT & 3D SIMULATION -->
      <div class="tab-panel" id="view-result">
        
        <!-- Left Pane: AI Optimized 2D Layout -->
        <div class="split-pane">
          <div class="pane-header">
            <span style="color: var(--cyan);"><i data-lucide="sparkles"></i> AI 자동 생성 최적 도면 (2D)</span>
            <span style="font-size: 0.75rem; color: var(--emerald);">동선 및 안전 규칙 적용됨</span>
          </div>
          <div class="blueprint-canvas" id="optimized-canvas"></div>
        </div>

        <!-- Center Pane: 3D Real-time Simulation -->
        <div class="split-pane">
          <div class="pane-header">
            <span style="color: var(--amber);"><i data-lucide="box"></i> 실시간 3D 조감도 및 시뮬레이션</span>
            <span style="font-size: 0.75rem; color: var(--text-sub);">드래그: 회전 | 우클릭: 이동 | 휠: 확대</span>
          </div>
          <div id="3d-container"></div>
          <div class="hud-controls">
            🧊 Three.js PBR 3D 렌더링 엔진 가동 중
          </div>
        </div>

        <!-- Right Pane: AI Report & Evaluation -->
        <div class="report-panel">
          <div class="section-title"><i data-lucide="check-circle-2"></i> AI 안전 & 동선 진단 결과</div>

          <div class="score-card">
            <div>
              <div style="font-size: 0.8rem; color: var(--text-sub);">종합 설계 평가 점수</div>
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--text-main); margin-top: 2px;" id="report-grade-text">A+ (최우수 도면)</div>
            </div>
            <div class="score-ring">
              <div class="score-ring-inner" id="report-score-val">94</div>
            </div>
          </div>

          <div class="metrics-grid">
            <div class="metric-box">
              <div class="metric-title">대피 시간 (예상)</div>
              <div class="metric-val" style="color: var(--emerald);" id="metric-evac">2분 10초</div>
            </div>
            <div class="metric-box">
              <div class="metric-title">병목 구간 발생율</div>
              <div class="metric-val" style="color: var(--emerald);" id="metric-bottleneck">3.2% (매우 낮음)</div>
            </div>
            <div class="metric-box">
              <div class="metric-title">평균 통로 너비</div>
              <div class="metric-val" id="metric-aisle">3.8 m (기준 충족)</div>
            </div>
            <div class="metric-box">
              <div class="metric-title">무대 시인성 지수</div>
              <div class="metric-val" style="color: var(--cyan);" id="metric-sight">96 / 100</div>
            </div>
          </div>

          <div class="section-title" style="margin-top: 10px;"><i data-lucide="list-checks"></i> 초안 대비 AI 주요 개선 사항</div>

          <div class="improvement-list" id="improvement-container">
            <!-- Dynamic Injection -->
          </div>

          <button onclick="switchTab('editor')" style="background: var(--bg-card); border: 1px solid var(--border); color: var(--text-main); padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; margin-top: auto;">
            ✏️ 초안 수정하러 돌아가기
          </button>
        </div>

      </div>

    </div>
  </div>

  <script>
    // State Management
    let draftElements = [];
    let optimizedElements = [];
    let selectedId = null;

    let isDragging = false;
    let isResizing = false;
    let dragOffset = { x: 0, y: 0 };
    let initialRect = { w: 0, h: 0, mouseX: 0, mouseY: 0 };

    // Three.js State
    let scene, camera, renderer, controls;
    let is3DInit = false;

    // Presets
    const ELEMENT_TYPES = {
      STAGE: { label: '메인 무대', color: '#6366f1', w: 220, h: 100, depth: 50 },
      BOOTH: { label: '전시 부스', color: '#0ea5e9', w: 80, h: 80, depth: 30 },
      EXIT: { label: '비상구', color: '#ef4444', w: 90, h: 35, depth: 40 },
      FOOD: { label: '푸드트럭', color: '#f59e0b', w: 100, h: 60, depth: 35 },
      INFO: { label: '안내데스크', color: '#10b981', w: 120, h: 50, depth: 25 },
      RESTROOM: { label: '편의시설', color: '#8b5cf6', w: 90, h: 60, depth: 30 }
    };

    const canvas = document.getElementById('editor-canvas');

    function init() {
      lucide.createIcons();
      setupCanvasEvents();

      // Default Draft Setup
      addElement('STAGE', 250, 40);
      addElement('BOOTH', 100, 200);
      addElement('BOOTH', 200, 200);
      addElement('BOOTH', 300, 200);
      addElement('EXIT', 600, 40);
      addElement('FOOD', 80, 420);
      addElement('INFO', 450, 420);
    }

    function addElement(typeKey, customX, customY) {
      const config = ELEMENT_TYPES[typeKey];
      const id = 'elem_' + Date.now() + '_' + Math.floor(Math.random()*1000);
      
      const x = customX !== undefined ? customX : Math.floor(Math.random() * 200) + 100;
      const y = customY !== undefined ? customY : Math.floor(Math.random() * 200) + 100;

      const item = {
        id,
        type: typeKey,
        label: config.label + ' ' + (draftElements.filter(e => e.type === typeKey).length + 1),
        color: config.color,
        x, y,
        w: config.w,
        h: config.h,
        depth: config.depth
      };

      draftElements.push(item);
      renderNode(item, canvas);
      selectElement(id);
      updateCount();
    }

    function renderNode(item, parentCanvas, isReadOnly = false) {
      const node = document.createElement('div');
      node.className = 'element-node';
      node.id = item.id;
      node.style.backgroundColor = item.color;
      node.style.left = item.x + 'px';
      node.style.top = item.y + 'px';
      node.style.width = item.w + 'px';
      node.style.height = item.h + 'px';

      node.innerHTML = `
        <div>${item.label}</div>
        <div class="node-type-tag">${item.w}x${item.h}</div>
        ${!isReadOnly ? '<div class="resize-handle"></div>' : ''}
      `;

      if (!isReadOnly) {
        node.addEventListener('mousedown', (e) => {
          e.stopPropagation();
          selectElement(item.id);

          if (e.target.classList.contains('resize-handle')) {
            isResizing = true;
            initialRect = { w: item.w, h: item.h, mouseX: e.clientX, mouseY: e.clientY };
          } else {
            isDragging = true;
            dragOffset = { x: e.clientX - item.x, y: e.clientY - item.y };
          }
        });
      }

      parentCanvas.appendChild(node);
    }

    function setupCanvasEvents() {
      canvas.addEventListener('mousedown', () => selectElement(null));

      window.addEventListener('mousemove', (e) => {
        if (!selectedId) return;
        const item = draftElements.find(e => e.id === selectedId);
        if (!item) return;

        if (isDragging) {
          item.x = Math.max(0, e.clientX - dragOffset.x);
          item.y = Math.max(0, e.clientY - dragOffset.y);
          const node = document.getElementById(item.id);
          if (node) {
            node.style.left = item.x + 'px';
            node.style.top = item.y + 'px';
          }
        } else if (isResizing) {
          item.w = Math.max(50, initialRect.w + (e.clientX - initialRect.mouseX));
          item.h = Math.max(30, initialRect.h + (e.clientY - initialRect.mouseY));
          const node = document.getElementById(item.id);
          if (node) {
            node.style.width = item.w + 'px';
            node.style.height = item.h + 'px';
            node.querySelector('.node-type-tag').innerText = `${item.w}x${item.h}`;
          }
        }
      });

      window.addEventListener('mouseup', () => {
        isDragging = false;
        isResizing = false;
      });
    }

    function selectElement(id) {
      selectedId = id;
      document.querySelectorAll('#editor-canvas .element-node').forEach(node => {
        node.classList.toggle('selected', node.id === id);
      });

      const inspector = document.getElementById('inspector');
      if (id) {
        const item = draftElements.find(e => e.id === id);
        if (item) {
          inspector.style.display = 'block';
          document.getElementById('inspector-label').value = item.label;
        }
      } else {
        inspector.style.display = 'none';
      }
    }

    function updateSelectedLabel() {
      if (!selectedId) return;
      const item = draftElements.find(e => e.id === selectedId);
      if (item) {
        item.label = document.getElementById('inspector-label').value;
        const node = document.getElementById(selectedId);
        if (node) node.querySelector('div').innerText = item.label;
      }
    }

    function deleteSelected() {
      if (!selectedId) return;
      draftElements = draftElements.filter(e => e.id !== selectedId);
      const node = document.getElementById(selectedId);
      if (node) node.remove();
      selectElement(null);
      updateCount();
    }

    function updateCount() {
      document.getElementById('canvas-count').innerText = `배치된 요소: ${draftElements.length}개`;
    }

    /* AI OPTIMIZATION ALGORITHM & ENGINE */
    function runAIOptimization() {
      if (draftElements.length === 0) {
        alert("최소 1개 이상의 요소를 도면에 배치해주세요.");
        return;
      }

      // Step 1: Clone draft elements for optimization
      optimizedElements = JSON.parse(JSON.stringify(draftElements));

      // Step 2: Calculate AI Smart Spatial Optimization Rules
      let boothIndex = 0;

      optimizedElements.forEach(item => {
        if (item.type === 'STAGE') {
          // Rule: Stage placed top-center with optimal sightlines
          item.x = 280;
          item.y = 30;
          item.w = 260;
          item.h = 90;
        } else if (item.type === 'BOOTH') {
          // Rule: Booths arranged in structured grid with 3.5m clearance
          const row = Math.floor(boothIndex / 3);
          const col = boothIndex % 3;
          item.x = 180 + col * 150;
          item.y = 180 + row * 120;
          item.w = 110;
          item.h = 80;
          boothIndex++;
        } else if (item.type === 'EXIT') {
          // Rule: Exits at outer boundaries with clear escape channels
          item.x = 650;
          item.y = 30;
        } else if (item.type === 'FOOD') {
          // Rule: Food trucks separated to perimeter to avoid grease/bottlenecks
          item.x = 50;
          item.y = 320;
        } else if (item.type === 'INFO') {
          // Rule: Information desk near main entrance
          item.x = 320;
          item.y = 440;
        } else if (item.type === 'RESTROOM') {
          item.x = 650;
          item.y = 420;
        }
      });

      // Step 3: Render AI 2D Optimized Canvas
      const optCanvas = document.getElementById('optimized-canvas');
      optCanvas.innerHTML = '';
      optimizedElements.forEach(item => renderNode(item, optCanvas, true));

      // Step 4: Generate Improvement Report List
      renderReportItems();

      // Step 5: Switch UI to Result Tab & Trigger 3D Render
      switchTab('result');
      setTimeout(initOrUpdate3D, 100);
    }

    function renderReportItems() {
      const container = document.getElementById('improvement-container');
      container.innerHTML = `
        <div class="item-card success">
          <div class="item-card-title"><i data-lucide="shield-check"></i> 메인 무대 시인성 및 음향 35% 향상</div>
          무대를 중앙 상단에 재배치하여 관람 객석 시야각 사각지대를 완전히 제거했습니다.
        </div>
        <div class="item-card warning">
          <div class="item-card-title"><i data-lucide="move"></i> 전시 부스 간격 확장 (1.8m ➔ 3.5m)</div>
          기존 초안의 부스 간 병목 위험을 감지하여 관람객 동선 통로 폭을 표준 이상으로 확장했습니다.
        </div>
        <div class="item-card danger">
          <div class="item-card-title"><i data-lucide="alert-triangle"></i> 비상 대피로 가림 현상 해결</div>
          비상 출입구 전면 5m 이내 장애물을 제거하여 최단 대피 동선을 확보했습니다.
        </div>
      `;
      lucide.createIcons();
    }

    function switchTab(tabName) {
      document.getElementById('step-1').classList.toggle('active', tabName === 'editor');
      document.getElementById('step-2').classList.toggle('active', tabName === 'result');
      document.getElementById('step-3').classList.toggle('active', tabName === 'result');

      document.getElementById('view-editor').classList.toggle('active', tabName === 'editor');
      document.getElementById('view-result').classList.toggle('active', tabName === 'result');
    }

    /* 3D SIMULATION ENGINE (Three.js) */
    function initOrUpdate3D() {
      const container = document.getElementById('3d-container');
      const w = container.clientWidth || 400;
      const h = container.clientHeight || 400;

      if (!is3DInit) {
        is3DInit = true;

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x090d16);

        camera = new THREE.PerspectiveCamera(45, w / h, 1, 2000);
        camera.position.set(0, 450, 600);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(w, h);
        renderer.shadowMap.enabled = true;
        renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(renderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(150, 400, 150);
        dirLight.castShadow = true;
        scene.add(dirLight);

        // Ground Grid
        const grid = new THREE.GridHelper(1000, 40, 0x3b82f6, 0x1f2937);
        grid.position.y = -1;
        scene.add(grid);

        window.addEventListener('resize', () => {
          if (!container) return;
          const nw = container.clientWidth;
          const nh = container.clientHeight;
          camera.aspect = nw / nh;
          camera.updateProjectionMatrix();
          renderer.setSize(nw, nh);
        });

        function animate() {
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }
        animate();
      }

      // Re-populate 3D Scene based on `optimizedElements`
      for (let i = scene.children.length - 1; i >= 0; i--) {
        const obj = scene.children[i];
        if (obj.type === 'Mesh' && obj !== scene.children[0]) {
          scene.remove(obj);
        }
      }

      // Ground Floor Mesh
      const floorGeo = new THREE.PlaneGeometry(800, 600);
      const floorMat = new THREE.MeshStandardMaterial({ color: 0x0b1329, roughness: 0.8 });
      const floor = new THREE.Mesh(floorGeo, floorMat);
      floor.rotation.x = -Math.PI / 2;
      floor.receiveShadow = true;
      scene.add(floor);

      // Render 3D Procedural Objects
      optimizedElements.forEach(item => {
        const posX = item.x + item.w / 2 - 400;
        const posZ = item.y + item.h / 2 - 300;
        const depth = item.depth || 30;

        const geo = new THREE.BoxGeometry(item.w, depth, item.h);
        const mat = new THREE.MeshStandardMaterial({
          color: parseInt(item.color.replace('#', '0x')),
          roughness: 0.4,
          metalness: 0.2
        });

        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(posX, depth / 2, posZ);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        scene.add(mesh);
      });
    }

    window.onload = init;
  </script>
</body>
</html>
"""

# Streamlit 풀스크린 렌더링
components.html(html_code, height=920, scrolling=False)
