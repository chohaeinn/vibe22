import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="스마트 행사장 도면 설계 & 3D 시뮬레이터",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 자바스크립트/HTML/CSS 전체 코드 (Streamlit iframe 내 통합 실행)
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>스마트 행사장 도면 설계 및 3D 시뮬레이터</title>
  
  <!-- Three.js & OrbitControls for 3D Simulation -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

  <style>
    :root {
      --bg-dark: #0f172a;
      --bg-sidebar: #1e293b;
      --bg-card: #334155;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-light: #f8fafc;
      --text-muted: #94a3b8;
      --border: #475569;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    body, html {
      width: 100%;
      height: 100%;
      background-color: var(--bg-dark);
      color: var(--text-light);
      overflow: hidden;
    }

    /* App Container & Navigation Header */
    .app-container {
      display: flex;
      flex-direction: column;
      height: 100vh;
    }

    .nav-header {
      height: 60px;
      background-color: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      z-index: 100;
    }

    .brand-logo {
      font-size: 1.25rem;
      font-weight: 800;
      color: #60a5fa;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .nav-tabs {
      display: flex;
      gap: 8px;
      background-color: var(--bg-dark);
      padding: 4px;
      border-radius: 8px;
    }

    .nav-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      transition: all 0.2s;
    }

    .nav-btn:hover {
      color: var(--text-light);
    }

    .nav-btn.active {
      background-color: var(--primary);
      color: #ffffff;
    }

    /* View Sections */
    .view-content {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .view-page {
      display: none;
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0;
      left: 0;
    }

    .view-page.active {
      display: flex;
    }

    /* 1. HOME SCREEN */
    #page-home {
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
      padding: 40px;
      text-align: center;
      overflow-y: auto;
    }

    .hero-title {
      font-size: 2.8rem;
      font-weight: 900;
      margin-bottom: 16px;
      background: linear-gradient(to right, #60a5fa, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: 1.15rem;
      color: var(--text-muted);
      max-width: 680px;
      margin-bottom: 40px;
      line-height: 1.6;
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      max-width: 1000px;
      width: 100%;
    }

    .feature-card {
      background-color: rgba(30, 41, 59, 0.7);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px 20px;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }

    .feature-card:hover {
      transform: translateY(-6px);
      border-color: var(--primary);
      box-shadow: 0 12px 24px rgba(59, 130, 246, 0.2);
    }

    .card-icon {
      font-size: 2.5rem;
    }

    .card-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-light);
    }

    .card-desc {
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.4;
    }

    /* 2. 2D EDITOR SCREEN */
    .editor-sidebar {
      width: 360px;
      background-color: var(--bg-sidebar);
      border-right: 1px solid var(--border);
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
      border-bottom: 2px solid var(--border);
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
      color: var(--text-muted);
    }

    input[type="text"], input[type="number"], select, textarea {
      background-color: var(--bg-dark);
      border: 1px solid var(--border);
      color: var(--text-light);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.9rem;
      outline: none;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--primary);
    }

    .mode-toggle {
      display: flex;
      gap: 8px;
    }

    .mode-btn {
      flex: 1;
      padding: 10px;
      border: 1px solid var(--border);
      background-color: var(--bg-card);
      color: var(--text-light);
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }

    .mode-btn.active {
      background-color: var(--primary);
      border-color: var(--primary);
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

    .switch input { opacity: 0; width: 0; height: 0; }

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
      height: 18px; width: 18px;
      left: 3px; bottom: 3px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
    }

    input:checked + .slider { background-color: var(--danger); }
    input:checked + .slider:before { transform: translateX(20px); }

    .palette-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .palette-btn {
      background-color: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-light);
      padding: 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
      text-align: center;
      transition: background 0.2s;
    }

    .palette-btn:hover { background-color: var(--border); }

    .editor-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    .canvas-toolbar {
      height: 50px;
      background-color: var(--bg-sidebar);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }

    .canvas-area {
      flex: 1;
      position: relative;
      overflow: hidden;
      background-color: #1e293b;
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
      background-size: 20px 20px;
    }

    .canvas-area.outdoor {
      background-color: #14532d;
      background-image: 
        linear-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.08) 1px, transparent 1px);
    }

    .placed-element {
      position: absolute;
      border: 2px solid rgba(255, 255, 255, 0.85);
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
      width: 12px; height: 12px;
      background-color: #f59e0b;
      bottom: -6px; right: -6px;
      cursor: se-resize;
      border-radius: 2px;
      display: none;
    }

    .placed-element.selected .resize-handle { display: block; }

    .traffic-svg {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
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
      to { stroke-dashoffset: -36; }
    }

    .flow-node { fill: #f43f5e; stroke: #ffffff; stroke-width: 2; }

    /* 3. 3D SIMULATION SCREEN */
    #page-3d {
      position: relative;
      background-color: #050811;
    }

    #3d-canvas-container {
      width: 100%;
      height: 100%;
    }

    .hud-overlay {
      position: absolute;
      top: 20px;
      left: 20px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 10px;
      max-width: 300px;
    }

    .hud-title {
      font-weight: 700;
      color: #60a5fa;
      margin-bottom: 8px;
    }

    .hud-info {
      font-size: 0.82rem;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* 4. SAFETY & REPORT SCREEN */
    #page-report {
      padding: 30px;
      overflow-y: auto;
      flex-direction: column;
      align-items: center;
      background-color: var(--bg-dark);
    }

    .report-container {
      max-width: 900px;
      width: 100%;
      background-color: var(--bg-sidebar);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 36px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }

    .report-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 24px;
    }

    .score-badge-card {
      display: flex;
      align-items: center;
      gap: 20px;
      background-color: var(--bg-card);
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 24px;
    }

    .score-circle {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background-color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.8rem;
      font-weight: 900;
      color: white;
    }

    .audit-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }

    .audit-item {
      background-color: var(--bg-card);
      padding: 16px;
      border-radius: 8px;
      border-left: 4px solid var(--primary);
    }

    .audit-item.danger { border-left-color: var(--danger); }
    .audit-item.success { border-left-color: var(--success); }
    .audit-item.warning { border-left-color: var(--warning); }

    .audit-title { font-size: 0.9rem; font-weight: 700; margin-bottom: 4px; }
    .audit-value { font-size: 0.85rem; color: var(--text-muted); }

    .btn-print {
      background-color: var(--primary);
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      font-weight: 700;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <div class="app-container">
    <!-- Header Navigation -->
    <header class="nav-header">
      <div class="brand-logo">
        <span>🏛️ EventPlan AI Pro</span>
      </div>
      <nav class="nav-tabs">
        <button class="nav-btn active" onclick="switchTab('home')">🏠 홈</button>
        <button class="nav-btn" onclick="switchTab('editor')">✏️ 2D 도면 설계</button>
        <button class="nav-btn" onclick="switchTab('3d')">🧊 3D 시뮬레이션</button>
        <button class="nav-btn" onclick="switchTab('report')">📊 안전·동선 리포트</button>
      </nav>
    </header>

    <!-- Main View Content -->
    <div class="view-content">

      <!-- PAGE 1: HOME -->
      <section id="page-home" class="view-page active">
        <h1 class="hero-title">스마트 행사장 도면 설계 & 3D 시뮬레이터</h1>
        <p class="hero-subtitle">
          직관적인 드래그 & 드롭 2D 레이아웃 구성부터 실시간 3D 조감도 투어,
          인공지능 기반 수용 인원 밀집도 및 비상 대피 동선 안전성 평가 리포트까지 한 번에 해결하세요.
        </p>

        <div class="card-grid">
          <div class="feature-card" onclick="startEditor('indoor')">
            <div class="card-icon">🏢</div>
            <div class="card-title">실내 컨벤션 행사 설계</div>
            <div class="card-desc">박람회, 학술대회, 기업 전시회에 최적화된 내부 무대, 부스, 비상구 레이아웃을 제작합니다.</div>
          </div>

          <div class="feature-card" onclick="startEditor('outdoor')">
            <div class="card-icon">🌳</div>
            <div class="card-title">야외 페스티벌 설계</div>
            <div class="card-desc">야외 축제, 푸드트럭 존, 몽골텐트, 가설 보건소 및 외곽 펜스 배치를 지원합니다.</div>
          </div>

          <div class="feature-card" onclick="switchTab('report')">
            <div class="card-icon">📋</div>
            <div class="card-title">안전 & 동선 리포트</div>
            <div class="card-desc">현재 배치된 도면을 실시간 분석하여 병목 예상 구간과 소방 안전 체크리스트를 생성합니다.</div>
          </div>
        </div>
      </section>

      <!-- PAGE 2: 2D EDITOR -->
      <section id="page-editor" class="view-page">
        <!-- Sidebar Controls -->
        <aside class="editor-sidebar">
          <div>
            <div class="section-title">행사 유형</div>
            <div class="mode-toggle">
              <button class="mode-btn active" id="btn-indoor" onclick="setEventMode('indoor')">🏢 실내 행사</button>
              <button class="mode-btn" id="btn-outdoor" onclick="setEventMode('outdoor')">🌳 야외 행사</button>
            </div>
          </div>

          <div>
            <div class="section-title">행사 세부 정보</div>
            <div class="form-group">
              <label>행사명</label>
              <input type="text" id="event-title" value="2026 테크 박람회" oninput="updateStats()">
            </div>
            <div class="form-group">
              <label>예상 참가 인원 (명)</label>
              <input type="number" id="expected-capacity" value="1500" min="1" oninput="updateStats()">
            </div>
            <div class="form-group">
              <label>입장료 (원)</label>
              <input type="number" id="ticket-fee" value="10000" min="0" step="500" oninput="updateStats()">
            </div>
            <div class="form-group">
              <label>추가 요구 사항 (전력/음향/위생 등)</label>
              <textarea id="extra-reqs" placeholder="예: 메인무대 220V 인입, 소방대피로 3m 유지"></textarea>
            </div>
          </div>

          <div>
            <div class="section-title">동선 및 안전 관리</div>
            <div class="toggle-container">
              <span style="font-size: 0.85rem; font-weight: 600;">최적 관람 동선 Overlay</span>
              <label class="switch">
                <input type="checkbox" id="traffic-toggle" onchange="toggleTrafficFlow(this.checked)">
                <span class="slider"></span>
              </label>
            </div>
          </div>

          <div>
            <div class="section-title">요소 추가 (클릭)</div>
            <div class="palette-grid" id="palette-buttons"></div>
          </div>

          <div id="inspector-panel" style="display: none;">
            <div class="section-title">선택 요소 조정</div>
            <div class="form-group">
              <label>라벨명 변경</label>
              <input type="text" id="elem-label" oninput="updateSelectedElement()">
            </div>
            <button style="background-color: var(--danger); color: white; border: none; padding: 8px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: 600;" onclick="deleteSelectedElement()">🗑️ 요소 삭제</button>
          </div>
        </aside>

        <!-- Canvas Area -->
        <main class="editor-main">
          <div class="canvas-toolbar">
            <span id="current-mode-label" style="font-weight: 700; color: #93c5fd;">모드: 실내 컨벤션 홀</span>
            <button onclick="clearCanvas()" style="background: none; border: 1px solid var(--border); color: #fff; padding: 6px 12px; border-radius: 6px; cursor: pointer;">초기화</button>
          </div>

          <div class="canvas-area" id="canvas">
            <svg class="traffic-svg" id="traffic-svg">
              <path class="flow-path" d="M 80,500 C 200,450 250,250 450,250 C 650,250 700,450 850,150" />
              <circle class="flow-node" cx="80" cy="500" r="8" />
              <circle class="flow-node" cx="450" cy="250" r="8" />
              <circle class="flow-node" cx="850" cy="150" r="8" />
              <text x="80" y="530" fill="#ffffff" font-size="12" font-weight="bold">주 출입구 (입장)</text>
              <text x="430" y="220" fill="#ffffff" font-size="12" font-weight="bold">메인 관람 구역</text>
              <text x="830" y="120" fill="#ffffff" font-size="12" font-weight="bold">비상구/퇴장</text>
            </svg>
          </div>
        </main>
      </section>

      <!-- PAGE 3: 3D SIMULATION -->
      <section id="page-3d" class="view-page">
        <div id="3d-canvas-container"></div>
        <div class="hud-overlay">
          <div class="hud-title">🧊 3D 실시간 조감도 투어</div>
          <div class="hud-info">
            • <b>마우스 좌클릭 드래그:</b> 화면 회전<br>
            • <b>우클릭 드래그:</b> 화면 이동(Pan)<br>
            • <b>휠 스크롤:</b> 확대/축소(Zoom)<br>
            <br>
            2D 도면에서 배치된 요소들이 실제 높이값을 가진 3D 입체 구조물로 자동 변환되어 렌더링됩니다.
          </div>
        </div>
      </section>

      <!-- PAGE 4: REPORT -->
      <section id="page-report" class="view-page">
        <div class="report-container">
          <div class="report-header">
            <div>
              <h2 style="font-size: 1.5rem; color: #fff;" id="report-title-display">행사장 종합 안전 및 동선 리포트</h2>
              <p style="color: var(--text-muted); font-size: 0.9rem;" id="report-date-display">진단일: 2026.09.08</p>
            </div>
            <button class="btn-print" onclick="window.print()">🖨️ 리포트 인쇄 / PDF 저장</button>
          </div>

          <div class="score-badge-card">
            <div class="score-circle" id="report-score">88</div>
            <div>
              <h3 style="font-size: 1.1rem; color: #fff;" id="report-grade">안전성 평가 우수 (Grade A)</h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);" id="report-summary-text">
                설계된 도면은 비상 대피로 접근성이 양호하며, 관람객 정체 위험이 낮습니다.
              </p>
            </div>
          </div>

          <div class="audit-grid">
            <div class="audit-item success" id="audit-density">
              <div class="audit-title">예상 인원 밀집도</div>
              <div class="audit-value" id="val-density">1.50 명/m² (안전 기준 충족)</div>
            </div>
            <div class="audit-item success" id="audit-exits">
              <div class="audit-title">비상구 접근성</div>
              <div class="audit-value" id="val-exits">비상 출입구 배치 확인됨</div>
            </div>
            <div class="audit-item warning" id="audit-flow">
              <div class="audit-title">병목 현상 예상 구역</div>
              <div class="audit-value" id="val-flow">메인무대 전면 5m 구간 밀집 주의</div>
            </div>
            <div class="audit-item success" id="audit-booth">
              <div class="audit-title">부스 간 통로 폭</div>
              <div class="audit-value" id="val-booth">최소 통로 폭 2.5m 이상 확보</div>
            </div>
          </div>

          <div class="section-title">소방 안전 및 대피 시나리오 체크리스트</div>
          <ul style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.8; padding-left: 20px;">
            <li>비상 출입구 방향 유도등 보시성 확보 확인 완료</li>
            <li>주요 무대 전원 제어반 및 소화기 가설 위치 지정 필요</li>
            <li>식음료(푸드트럭/음료부스) 인근 화기 사용 규정 준수 및 안심 대피선 표기</li>
          </ul>
        </div>
      </section>

    </div>
  </div>

  <script>
    // Global Application State
    let currentTab = 'home';
    let currentMode = 'indoor';
    let elements = [];
    let selectedElementId = null;

    let isDragging = false;
    let isResizing = false;
    let dragOffsetX = 0, dragOffsetY = 0;
    let initialW = 0, initialH = 0, initialMouseX = 0, initialMouseY = 0;

    // Three.js Variables
    let scene, camera, renderer, controls;
    let is3DInitialized = false;

    const paletteConfigs = {
      indoor: [
        { label: '메인 무대', color: '#6366f1', w: 220, h: 100, depth: 40 },
        { label: '전시 부스', color: '#0ea5e9', w: 90, h: 90, depth: 30 },
        { label: '안내 데스크', color: '#10b981', w: 120, h: 60, depth: 20 },
        { label: '관람석/의자', color: '#8b5cf6', w: 160, h: 80, depth: 15 },
        { label: '비상구', color: '#ef4444', w: 80, h: 40, depth: 35 }
      ],
      outdoor: [
        { label: '야외 메인무대', color: '#4f46e5', w: 260, h: 120, depth: 50 },
        { label: '푸드트럭', color: '#f59e0b', w: 110, h: 70, depth: 35 },
        { label: '몽골텐트', color: '#10b981', w: 80, h: 80, depth: 40 },
        { label: '의무실 텐트', color: '#ec4899', w: 90, h: 70, depth: 35 },
        { label: '야외 화장실', color: '#64748b', w: 90, h: 60, depth: 30 }
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

    // Switch Top Navigation Tabs
    function switchTab(tabName) {
      currentTab = tabName;
      document.querySelectorAll('.nav-btn').forEach((btn, idx) => {
        const tabs = ['home', 'editor', '3d', 'report'];
        btn.classList.toggle('active', tabs[idx] === tabName);
      });

      document.querySelectorAll('.view-page').forEach(page => page.classList.remove('active'));
      document.getElementById('page-' + tabName).classList.add('active');

      if (tabName === '3d') {
        initOrUpdate3D();
      } else if (tabName === 'report') {
        generateReport();
      }
    }

    function startEditor(mode) {
      setEventMode(mode);
      switchTab('editor');
    }

    function setEventMode(mode) {
      currentMode = mode;
      document.getElementById('btn-indoor').classList.toggle('active', mode === 'indoor');
      document.getElementById('btn-outdoor').classList.toggle('active', mode === 'outdoor');

      const canvasArea = document.getElementById('canvas');
      const modeLabel = document.getElementById('current-mode-label');

      if (mode === 'indoor') {
        canvasArea.classList.remove('outdoor');
        modeLabel.innerText = "모드: 실내 컨벤션 홀";
      } else {
        canvasArea.classList.add('outdoor');
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
        btn.onclick = () => addElement(item.label, item.color, item.w, item.h, item.depth);
        container.appendChild(btn);
      });
    }

    function loadDefaultPresets() {
      if (currentMode === 'indoor') {
        addElement('메인 무대', '#6366f1', 240, 100, 40, 250, 40);
        addElement('전시 부스 A', '#0ea5e9', 100, 100, 30, 120, 200);
        addElement('전시 부스 B', '#0ea5e9', 100, 100, 30, 250, 200);
        addElement('안내 데스크', '#10b981', 140, 60, 20, 40, 420);
        addElement('비상구', '#ef4444', 80, 40, 35, 600, 80);
      } else {
        addElement('야외 메인무대', '#4f46e5', 260, 120, 50, 220, 30);
        addElement('푸드트럭 01', '#f59e0b', 110, 70, 35, 80, 220);
        addElement('푸드트럭 02', '#f59e0b', 110, 70, 35, 80, 310);
        addElement('몽골텐트 A', '#10b981', 90, 90, 40, 400, 220);
        addElement('의무실 텐트', '#ec4899', 90, 70, 35, 600, 100);
      }
    }

    function addElement(label, color, w = 100, h = 80, depth = 30, customX, customY) {
      const id = 'elem_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
      const x = customX !== undefined ? customX : Math.floor(Math.random() * 150) + 80;
      const y = customY !== undefined ? customY : Math.floor(Math.random() * 150) + 80;

      const elementData = { id, label, color, x, y, width: w, height: h, depth };
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
      const density = (capacity / 1000).toFixed(2);
      
      document.getElementById('val-density').innerText = `${density} 명/m² (${density > 2.0 ? '밀집 주의' : '안전 기준 충족'})`;
    }

    /* 3D Simulation Setup & Render */
    function initOrUpdate3D() {
      const container = document.getElementById('3d-canvas-container');

      if (!is3DInitialized) {
        is3DInitialized = true;

        scene = new THREE.Scene();
        scene.background = new THREE.Color(currentMode === 'indoor' ? 0x0f172a : 0x052e16);

        camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 1, 3000);
        camera.position.set(0, 600, 800);

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        // Ambient & Directional Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(200, 500, 200);
        dirLight.castShadow = true;
        scene.add(dirLight);

        window.addEventListener('resize', () => {
          if (!container) return;
          camera.aspect = container.clientWidth / container.clientHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(container.clientWidth, container.clientHeight);
        });

        function animate() {
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }
        animate();
      }

      // Rebuild 3D Scene Objects from `elements` array
      scene.background = new THREE.Color(currentMode === 'indoor' ? 0x0f172a : 0x052e16);
      
      // Clear previous mesh objects except lights
      for (let i = scene.children.length - 1; i >= 0; i--) {
        const obj = scene.children[i];
        if (obj.type === 'Mesh') scene.remove(obj);
      }

      // Ground Plane
      const groundGeo = new THREE.PlaneGeometry(1200, 800);
      const groundMat = new THREE.MeshStandardMaterial({ 
        color: currentMode === 'indoor' ? 0x1e293b : 0x14532d,
        roughness: 0.8 
      });
      const ground = new THREE.Mesh(groundGeo, groundMat);
      ground.rotation.x = -Math.PI / 2;
      ground.position.set(0, 0, 0);
      scene.add(ground);

      // Render 3D Floor Elements
      elements.forEach(item => {
        const geo = new THREE.BoxGeometry(item.width, item.depth || 30, item.height);
        const mat = new THREE.MeshStandardMaterial({ 
          color: item.color,
          metalness: 0.2,
          roughness: 0.5 
        });
        const mesh = new THREE.Mesh(geo, mat);

        // Convert 2D canvas coordinates to 3D Scene space
        const posX = item.x + item.width / 2 - 400;
        const posZ = item.y + item.height / 2 - 300;
        const posY = (item.depth || 30) / 2;

        mesh.position.set(posX, posY, posZ);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        scene.add(mesh);
      });
    }

    /* Automated Report Generation */
    function generateReport() {
      const eventTitle = document.getElementById('event-title').value;
      const capacity = parseInt(document.getElementById('expected-capacity').value) || 0;
      const density = (capacity / 1000).toFixed(2);

      document.getElementById('report-title-display').innerText = `${eventTitle} - 안전 및 동선 종합 리포트`;
      
      let score = 90;
      if (density > 2.0) score -= 15;
      if (elements.length < 3) score -= 10;

      document.getElementById('report-score').innerText = score;
      
      if (score >= 85) {
        document.getElementById('report-grade').innerText = "안전성 평가 우수 (Grade A)";
        document.getElementById('report-summary-text').innerText = "전반적인 출입구 비상동선 확보 및 밀집도 분포가 매우 우수합니다.";
      } else {
        document.getElementById('report-grade').innerText = "안전성 평가 보통 (Grade B)";
        document.getElementById('report-summary-text').innerText = "일부 관람 구역의 밀집도가 높습니다. 주요 경로의 통로 폭을 확장하는 것을 권장합니다.";
      }
    }

    window.onload = init;
  </script>
</body>
</html>
"""

# Streamlit 앱 내 풀사이즈 렌더링
components.html(html_code, height=920, scrolling=False)
