import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 프리미엄 디지털 트윈 & 동선 시뮬레이터",
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
<title>Event AI - 행사 설계 및 디지털 트윈</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">

<!-- Three.js & OrbitControls -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Pretendard Variable", Pretendard, -apple-system, sans-serif;
  color: #1e293b;
  background: #f8fafc;
  overflow-x: hidden;
}
button, input, select { font: inherit; }
button { cursor: pointer; transition: all 0.2s ease; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

/* Dashboard Layout */
.app-layout { display: flex; min-height: 100vh; }

/* Left Sidebar - Deep Navy Theme */
.sidebar {
  width: 230px;
  background: #0f172a;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px 12px;
  flex-shrink: 0;
  border-right: 1px solid #1e293b;
}
.sidebar-top { display: flex; flex-direction: column; gap: 20px; }
.brand-logo {
  display: flex; align-items: center; gap: 10px; color: #fff; padding: 4px 8px;
}
.brand-icon {
  width: 30px; height: 30px; background: #3b82f6; border-radius: 8px;
  display: grid; place-items: center; font-weight: 900; color: #fff; font-size: 14px;
}
.brand-name { font-size: 16px; font-weight: 800; color: #ffffff; letter-spacing: -0.3px; }

.nav-menu { display: flex; flex-direction: column; gap: 4px; list-style: none; }
.nav-item {
  display: flex; align-items: center; gap: 10px; padding: 10px 12px;
  border-radius: 8px; font-size: 13px; font-weight: 600; color: #94a3b8;
  cursor: pointer; transition: 0.15s;
}
.nav-item:hover { background: rgba(255,255,255,0.05); color: #f8fafc; }
.nav-item.active { background: #2563eb; color: #ffffff; font-weight: 700; }

.sidebar-card {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border: 1px solid #334155; border-radius: 12px; padding: 12px; color: #fff;
}
.sidebar-card h4 { font-size: 12px; font-weight: 700; color: #38bdf8; margin-bottom: 4px; }
.sidebar-card p { font-size: 11px; color: #94a3b8; line-height: 1.4; }

/* Main Content Area */
.main-wrapper { flex: 1; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; min-width: 0; }

/* Top Header & Info Card */
.page-header { display: flex; justify-content: space-between; align-items: center; }
.page-title-wrap h1 { font-size: 20px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px; }
.page-title-wrap p { font-size: 12px; color: #64748b; margin-top: 2px; }

.info-summary-card {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 14px 20px; display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03); flex-wrap: wrap; gap: 12px;
}
.info-group { display: flex; align-items: center; gap: 24px; }
.info-item { display: flex; flex-direction: column; gap: 2px; }
.info-label { font-size: 11px; font-weight: 600; color: #64748b; display: flex; align-items: center; gap: 4px; }
.info-val { font-size: 13px; font-weight: 800; color: #0f172a; }

.btn-ai-replan {
  background: linear-gradient(135deg, #4f46e5, #3b82f6); color: #fff; border: none;
  padding: 10px 18px; border-radius: 10px; font-size: 12px; font-weight: 800;
  display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(59,130,246,0.25);
}
.btn-ai-replan:hover { opacity: 0.95; transform: translateY(-1px); }

/* Main Grid Layout (Reference Image Layout) */
.dashboard-grid { display: grid; grid-template-columns: 1.25fr 1fr 0.85fr; gap: 16px; }

.card-box {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px;
  display: flex; flex-direction: column; gap: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { font-size: 14px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 6px; }

/* Canvas Visual Container */
.canvas-container {
  position: relative; width: 100%; height: 380px; background: #1b2838;
  border-radius: 10px; overflow: hidden; border: 1px solid #334155;
}
#venueCanvas, #heatmapCanvas, #vectorCanvas, #canvas3D {
  position: absolute; inset: 0; width: 100%; height: 100%;
}
#canvas3D { display: none; z-index: 10; }

.map-tools {
  position: absolute; top: 10px; right: 10px; z-index: 20;
  display: flex; gap: 4px; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(4px);
  padding: 4px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);
}
.tool-btn {
  background: transparent; border: none; color: #94a3b8; padding: 4px 8px;
  border-radius: 6px; font-size: 11px; font-weight: 700;
}
.tool-btn.active { background: #2563eb; color: #fff; }

/* Timeline Simulator Bar */
.time-control-panel {
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px;
  display: flex; flex-direction: column; gap: 10px;
}
.time-header { display: flex; justify-content: space-between; align-items: center; }
.time-display { font-size: 15px; font-weight: 900; color: #2563eb; }
.timeline-slider-wrap { display: flex; align-items: center; gap: 12px; }
.timeline-slider { flex: 1; accent-color: #2563eb; cursor: pointer; }

.time-presets { display: flex; gap: 6px; }
.preset-btn {
  flex: 1; padding: 6px 4px; border: 1px solid #cbd5e1; background: #fff;
  border-radius: 6px; font-size: 11px; font-weight: 700; color: #475569; text-align: center;
}
.preset-btn.active { background: #eff6ff; border-color: #3b82f6; color: #1d4ed8; }

/* AI Evaluation Scores Table */
.score-list { display: flex; flex-direction: column; gap: 8px; }
.score-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 12px; background: #f8fafc; border-radius: 8px; font-size: 12px;
}
.score-row-title { font-weight: 600; color: #334155; }
.score-value-wrap { display: flex; align-items: center; gap: 8px; }
.score-num { font-weight: 800; color: #0f172a; width: 24px; text-align: right; }
.badge {
  padding: 3px 8px; border-radius: 6px; font-size: 10px; font-weight: 800;
}
.badge-excel { background: #dcfce7; color: #15803d; }
.badge-good { background: #dbeafe; color: #1e40af; }
.badge-warn { background: #fef3c7; color: #b45309; }

/* Bottom Row Section */
.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.comparison-box { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.comp-card {
  background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px;
  display: flex; flex-direction: column; gap: 6px; text-align: center;
}
.comp-card img, .comp-thumb {
  width: 100%; height: 100px; background: #cbd5e1; border-radius: 6px;
  display: grid; place-items: center; font-size: 11px; color: #475569; font-weight: 700;
}

.report-box {
  background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 12px;
  display: flex; flex-direction: column; gap: 6px; font-size: 12px; color: #1e40af;
}
.report-box ul { padding-left: 16px; display: flex; flex-direction: column; gap: 4px; }
</style>
</head>
<body>

<div class="app-layout">

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div class="sidebar-top">
      <div class="brand-logo">
        <div class="brand-icon">E</div>
        <span class="brand-name">Event AI</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item">🏠 홈</li>
        <li class="nav-item active">📐 행사 설계</li>
        <li class="nav-item">⚙️ 설계 프로세스</li>
        <li class="nav-item">📜 설계 이력 관리</li>
        <li class="nav-item">👤 마이페이지</li>
      </ul>
    </div>

    <div class="sidebar-card">
      <h4>AI 컨설턴트</h4>
      <p>부스 간 최소 거리 3m 및 겹침 방지 알고리즘이 실시간 적용 중입니다.</p>
    </div>
  </aside>

  <!-- MAIN WRAPPER -->
  <main class="main-wrapper">

    <!-- TOP TITLE HEADER -->
    <header class="page-header">
      <div class="page-title-wrap">
        <h1>📑 행사 설계 및 디지털 트윈</h1>
        <p>행사 정보를 기반으로 AI가 실시간 최적의 배치와 동선을 계산합니다.</p>
      </div>
    </header>

    <!-- INFO SUMMARY CARD -->
    <div class="info-summary-card">
      <div class="info-group">
        <div class="info-item">
          <span class="info-label">📋 행사명</span>
          <span class="info-val">2026 청동 융합 박람회</span>
        </div>
        <div class="info-item">
          <span class="info-label">🎪 부스 수</span>
          <span class="info-val" id="summaryBoothCount">8개</span>
        </div>
        <div class="info-item">
          <span class="info-label">📐 행사 공간</span>
          <span class="info-val">50m × 35m (야외)</span>
        </div>
        <div class="info-item">
          <span class="info-label">👥 목표 관람객</span>
          <span class="info-val">5,000명</span>
        </div>
        <div class="info-item">
          <span class="info-label">⏰ 운영 시간</span>
          <span class="info-val">10:00 ~ 18:00</span>
        </div>
      </div>
      <button class="btn-ai-replan" onclick="replanAILayout()">
        ✨ AI 매니저 재배치
      </button>
    </div>

    <!-- TIME SIMULATION CONTROL PANEL -->
    <div class="time-control-panel">
      <div class="time-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:13px; font-weight:800; color:#0f172a;">🕒 시간대별 관람객 동선 시뮬레이션</span>
          <span style="font-size:11px; color:#64748b;" id="timeStatusDesc">(12:00 점심시간 - 푸드존 밀집)</span>
        </div>
        <div class="time-display" id="timeText">12:00 PM</div>
      </div>
      <div class="timeline-slider-wrap">
        <span style="font-size:11px; font-weight:700; color:#64748b;">10:00</span>
        <input type="range" class="timeline-slider" id="timeSlider" min="10" max="18" step="0.5" value="12" oninput="onTimeChange(this.value)">
        <span style="font-size:11px; font-weight:700; color:#64748b;">18:00</span>
      </div>
      <div class="time-presets">
        <button class="preset-btn" onclick="setTimePreset(10)">10:00 입장/개막식</button>
        <button class="preset-btn active" id="btnPresetLunch" onclick="setTimePreset(12)">12:00 점심시간 (푸드존)</button>
        <button class="preset-btn" onclick="setTimePreset(14)">14:00 메인 공연 (무대)</button>
        <button class="preset-btn" onclick="setTimePreset(16)">16:00 체험/휴식</button>
        <button class="preset-btn" onclick="setTimePreset(17.5)">17:30 폐막 및 퇴장</button>
      </div>
    </div>

    <!-- MAIN DASHBOARD GRID (3 COLUMNS) -->
    <div class="dashboard-grid">

      <!-- Column 1: Main Digital Twin Canvas -->
      <div class="card-box">
        <div class="card-header">
          <h3>🎪 행사장 배치도 (디지털 트윈)</h3>
          <span style="font-size:11px; color:#10b981; font-weight:700;">🟢 실시간 충돌방지 작동 중</span>
        </div>
        <div class="canvas-container">
          <div class="map-tools">
            <button class="tool-btn active" id="btn2D" onclick="switchView('2D')">2D</button>
            <button class="tool-btn" id="btn3D" onclick="switchView('3D')">3D 입체</button>
          </div>
          <canvas id="venueCanvas"></canvas>
          <canvas id="heatmapCanvas"></canvas>
          <canvas id="vectorCanvas"></canvas>
          <div id="canvas3D"></div>
        </div>
      </div>

      <!-- Column 2: Heatmap View -->
      <div class="card-box">
        <div class="card-header">
          <h3>🔥 혼잡도 Heatmap</h3>
          <span style="font-size:10px; color:#64748b;">실시간 밀집 레이어</span>
        </div>
        <div class="canvas-container" style="height:380px;">
          <canvas id="secondaryHeatmap"></canvas>
        </div>
      </div>

      <!-- Column 3: AI Evaluation Metrics -->
      <div class="card-box">
        <div class="card-header">
          <h3>💡 AI 평가 결과</h3>
        </div>
        <div class="score-list">
          <div class="score-row">
            <span class="score-row-title">안전성</span>
            <div class="score-value-wrap">
              <span class="score-num">92</span>
              <span class="badge badge-excel">매우 우수</span>
            </div>
          </div>
          <div class="score-row">
            <span class="score-row-title">동선 순환성</span>
            <div class="score-value-wrap">
              <span class="score-num">87</span>
              <span class="badge badge-good">우수</span>
            </div>
          </div>
          <div class="score-row">
            <span class="score-row-title">접근성</span>
            <div class="score-value-wrap">
              <span class="score-num">90</span>
              <span class="badge badge-excel">매우 우수</span>
            </div>
          </div>
          <div class="score-row">
            <span class="score-row-title">혼잡도 경감</span>
            <div class="score-value-wrap">
              <span class="score-num">84</span>
              <span class="badge badge-good">우수</span>
            </div>
          </div>
          <div class="score-row">
            <span class="score-row-title">공간 활용성</span>
            <div class="score-value-wrap">
              <span class="score-num">88</span>
              <span class="badge badge-good">우수</span>
            </div>
          </div>
        </div>

        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:10px; font-size:11px; margin-top:4px;">
          <b style="color:#0f172a;">AI 개선 제안</b>
          <p style="color:#64748b; margin-top:4px; line-height:1.4;">
            부스 간 충돌 없이 최적으로 이격되었습니다. 점심시간에는 푸드존 주변 안전 요원 배치를 권장합니다.
          </p>
        </div>
      </div>

    </div>

    <!-- BOTTOM ROW SECTION -->
    <div class="bottom-grid">
      <!-- AI Before / After Comparison -->
      <div class="card-box">
        <div class="card-header">
          <h3>📊 설계 전 / 후 비교</h3>
        </div>
        <div class="comparison-box">
          <div class="comp-card">
            <span style="font-size:11px; font-weight:700; color:#ef4444;">설계 전 (충돌 및 병목 발생)</span>
            <div class="comp-thumb" style="background:#fee2e2; color:#991b1b;">
              ⚠️ 부스 겹침 2건<br>병목 구간 3개 발생
            </div>
          </div>
          <div class="comp-card">
            <span style="font-size:11px; font-weight:700; color:#16a34a;">AI 설계 후 (충돌 방지 최적화)</span>
            <div class="comp-thumb" style="background:#dcfce7; color:#166534;">
              ✅ 충돌 0건<br>동선 순환 효율 +35%
            </div>
          </div>
        </div>
      </div>

      <!-- AI Summary Report -->
      <div class="card-box">
        <div class="card-header">
          <h3>📝 분석 리포트 요약</h3>
        </div>
        <div class="report-box">
          <b>🎯 시간대별 동선 및 공간 배치 최적화 종합 리포트</b>
          <ul>
            <li>자동 겹침 방지(Non-overlapping) 알고리즘으로 안전 통로 규격(3m)을 전면 확보했습니다.</li>
            <li>12:00~13:30 점심시간대 푸드존 동선 분산으로 특정 구간 병목현상을 42% 방지합니다.</li>
            <li>비상 출입구 및 응급의료소 접근 골든타임을 확보하여 대피 안전 등급 '매우 우수'를 기록했습니다.</li>
          </ul>
        </div>
      </div>
    </div>

  </main>
</div>

<script>
/* GLOBAL STATE & VARS */
let currentView = '2D';
let currentTime = 12.0; // Default 12:00 PM (Lunch)

let venueCanvas, venueCtx, heatmapCanvas, heatmapCtx, vectorCanvas, vectorCtx, secHeatmapCanvas, secHeatmapCtx;
let animFrameId = null;

// Booth Definitions
let booths = [
  { id:'stage', title:'메인 무대', x: 0.36, y: 0.06, w: 0.28, h: 0.18, color:'#8b5cf6', icon:'🎭' },
  { id:'boothA', title:'체험존 A', x: 0.08, y: 0.28, w: 0.18, h: 0.15, color:'#3b82f6', icon:'🧪' },
  { id:'boothB', title:'체험존 B', x: 0.74, y: 0.28, w: 0.18, h: 0.15, color:'#3b82f6', icon:'🚀' },
  { id:'food', title:'푸드존', x: 0.08, y: 0.58, w: 0.22, h: 0.18, color:'#f59e0b', icon:'🍔' },
  { id:'med', title:'응급의료소', x: 0.74, y: 0.58, w: 0.16, h: 0.15, color:'#ef4444', icon:'🏥' },
  { id:'rest', title:'중앙 쉼터', x: 0.38, y: 0.48, w: 0.24, h: 0.18, color:'#10b981', icon:'🌿' },
  { id:'gate_in', title:'주 출입구', x: 0.40, y: 0.82, w: 0.20, h: 0.10, color:'#06b6d4', icon:'🚪' },
  { id:'wc', title:'위생시설', x: 0.82, y: 0.82, w: 0.12, h: 0.10, color:'#64748b', icon:'🚻' }
];

let people = [];
const TOTAL_PEOPLE = 110;

/* 1. NON-OVERLAPPING BOOTH ALGORITHM */
function resolveBoothOverlaps() {
  const minPadding = 0.03; // Minimum distance between booths (3% of canvas)
  let iterations = 0;
  let hasOverlap = true;

  while(hasOverlap && iterations < 50) {
    hasOverlap = false;
    iterations++;

    for (let i = 0; i < booths.length; i++) {
      for (let j = i + 1; j < booths.length; j++) {
        let b1 = booths[i];
        let b2 = booths[j];

        // AABB Collision Detection
        if (b1.x < b2.x + b2.w + minPadding &&
            b1.x + b1.w + minPadding > b2.x &&
            b1.y < b2.y + b2.h + minPadding &&
            b1.y + b1.h + minPadding > b2.y) {

          hasOverlap = true;

          // Push b2 away from b1
          let overlapX = (b1.w/2 + b2.w/2 + minPadding) - Math.abs((b1.x + b1.w/2) - (b2.x + b2.w/2));
          let overlapY = (b1.h/2 + b2.h/2 + minPadding) - Math.abs((b1.y + b1.h/2) - (b2.y + b2.h/2));

          if (overlapX < overlapY) {
            if (b2.x > b1.x) b2.x += overlapX * 0.6;
            else b2.x -= overlapX * 0.6;
          } else {
            if (b2.y > b1.y) b2.y += overlapY * 0.6;
            else b2.y -= overlapY * 0.6;
          }

          // Clamp bounds inside Canvas
          b2.x = Math.max(0.04, Math.min(0.96 - b2.w, b2.x));
          b2.y = Math.max(0.04, Math.min(0.92 - b2.h, b2.y));
        }
      }
    }
  }
}

/* 2. TIME-BASED BEHAVIORAL ENGINE */
function onTimeChange(val) {
  currentTime = parseFloat(val);
  const hours = Math.floor(currentTime);
  const mins = (currentTime % 1 === 0) ? '00' : '30';
  document.getElementById('timeText').textContent = `${hours}:${mins} ${hours >= 12 ? 'PM' : 'AM'}`;

  // Update Status Description based on Time
  const descEl = document.getElementById('timeStatusDesc');
  if(currentTime >= 10 && currentTime < 11.5) {
    descEl.textContent = "(10:00~11:30 입장 및 개막식 - 주 출입구 & 메인 무대 밀집)";
  } else if(currentTime >= 11.5 && currentTime <= 13.5) {
    descEl.textContent = "(12:00~13:30 점심시간 - 관람객 70% 푸드존 이동)";
  } else if(currentTime > 13.5 && currentTime <= 15.5) {
    descEl.textContent = "(14:00~15:30 메인 공연시간 - 메인 무대 인원 폭주)";
  } else if(currentTime > 15.5 && currentTime <= 17) {
    descEl.textContent = "(16:00~17:00 자유 관람 - 체험존 및 중앙 쉼터 분산)";
  } else {
    descEl.textContent = "(17:30~18:00 폐막 - 주 출입구 퇴장 동선 형성)";
  }

  // Highlight active preset button UI
  document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
}

function setTimePreset(timeVal) {
  document.getElementById('timeSlider').value = timeVal;
  onTimeChange(timeVal);
}

function getTargetForPerson(index) {
  // Returns target coordinates (x, y) based on current hour
  const w = venueCanvas ? venueCanvas.width : 500;
  const h = venueCanvas ? venueCanvas.height : 380;

  let targetBooth = null;

  if (currentTime >= 10 && currentTime < 11.5) {
    // Entrance / Main Stage
    targetBooth = (index % 3 === 0) ? booths.find(b => b.id === 'gate_in') : booths.find(b => b.id === 'stage');
  } else if (currentTime >= 11.5 && currentTime <= 13.5) {
    // Lunch Time: 70% Food Zone, 30% Rest / Restroom
    if(index % 10 < 7) targetBooth = booths.find(b => b.id === 'food');
    else targetBooth = (index % 2 === 0) ? booths.find(b => b.id === 'rest') : booths.find(b => b.id === 'wc');
  } else if (currentTime > 13.5 && currentTime <= 15.5) {
    // Main Performance: 65% Main Stage, 35% Experience Booths
    if(index % 10 < 6.5) targetBooth = booths.find(b => b.id === 'stage');
    else targetBooth = (index % 2 === 0) ? booths.find(b => b.id === 'boothA') : booths.find(b => b.id === 'boothB');
  } else if (currentTime > 15.5 && currentTime <= 17) {
    // Free Viewing: Distributed across booths
    targetBooth = booths[index % booths.length];
  } else {
    // Exit Time: Head to Exit Gate
    targetBooth = booths.find(b => b.id === 'gate_in');
  }

  if(targetBooth) {
    return {
      x: (targetBooth.x + targetBooth.w * 0.5) * w + (Math.random()-0.5)*40,
      y: (targetBooth.y + targetBooth.h * 0.5) * h + (Math.random()-0.5)*30
    };
  }

  return { x: w*0.5, y: h*0.5 };
}

/* 3. SIMULATION & CANVAS DRAWING */
function initSim() {
  venueCanvas = document.getElementById('venueCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');
  vectorCanvas = document.getElementById('vectorCanvas');
  secHeatmapCanvas = document.getElementById('secondaryHeatmap');

  const wrap = venueCanvas.parentElement;
  const w = wrap.clientWidth || 500;
  const h = wrap.clientHeight || 380;

  [venueCanvas, heatmapCanvas, vectorCanvas, secHeatmapCanvas].forEach(c => {
    c.width = w; c.height = h;
  });

  venueCtx = venueCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');
  vectorCtx = vectorCanvas.getContext('2d');
  secHeatmapCtx = secHeatmapCanvas.getContext('2d');

  // Ensure Booth Overlap is Resolved
  resolveBoothOverlaps();

  // Initialize People
  people = [];
  for(let i=0; i<TOTAL_PEOPLE; i++) {
    people.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: 0, vy: 0
    });
  }

  if(animFrameId) cancelAnimationFrame(animFrameId);
  loop();
}

function loop() {
  if(currentView === '2D') {
    const w = venueCanvas.width;
    const h = venueCanvas.height;

    // Clear
    venueCtx.clearRect(0,0,w,h);
    heatmapCtx.clearRect(0,0,w,h);
    secHeatmapCtx.clearRect(0,0,w,h);

    // Draw Background Grid
    venueCtx.fillStyle = '#1e293b';
    venueCtx.fillRect(0,0,w,h);

    venueCtx.strokeStyle = 'rgba(255,255,255,0.05)';
    venueCtx.lineWidth = 1;
    for(let x=0; x<w; x+=25){ venueCtx.beginPath(); venueCtx.moveTo(x,0); venueCtx.lineTo(x,h); venueCtx.stroke(); }
    for(let y=0; y<h; y+=25){ venueCtx.beginPath(); venueCtx.moveTo(0,y); venueCtx.lineTo(w,y); venueCtx.stroke(); }

    // Draw Booths
    booths.forEach(b => {
      const bx = b.x * w, by = b.y * h, bw = b.w * w, bh = b.h * h;

      // Card Shadow
      venueCtx.fillStyle = 'rgba(0,0,0,0.3)';
      venueCtx.fillRect(bx+3, by+3, bw, bh);

      // Booth Body
      venueCtx.fillStyle = b.color;
      venueCtx.beginPath();
      venueCtx.roundRect(bx, by, bw, bh, 6);
      venueCtx.fill();

      venueCtx.strokeStyle = 'rgba(255,255,255,0.8)';
      venueCtx.lineWidth = 1.5;
      venueCtx.stroke();

      // Label
      venueCtx.fillStyle = '#ffffff';
      venueCtx.font = 'bold 11px Pretendard';
      venueCtx.textAlign = 'center';
      venueCtx.fillText(`${b.icon} ${b.title}`, bx + bw/2, by + bh/2 + 4);
    });

    // Move & Draw People
    people.forEach((p, idx) => {
      const target = getTargetForPerson(idx);
      const dx = target.x - p.x;
      const dy = target.y - p.y;
      const dist = Math.sqrt(dx*dx + dy*dy);

      if(dist > 5) {
        p.vx = (dx / dist) * 1.6;
        p.vy = (dy / dist) * 1.6;
      } else {
        p.vx = (Math.random()-0.5) * 0.5;
        p.vy = (Math.random()-0.5) * 0.5;
      }

      p.x += p.vx;
      p.y += p.vy;

      // Draw Person Dot
      venueCtx.fillStyle = '#38bdf8';
      venueCtx.beginPath();
      venueCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
      venueCtx.fill();

      // Heatmap Effect on Both Canvas & Secondary Heatmap
      [heatmapCtx, secHeatmapCtx].forEach(ctx => {
        let grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 22);
        grad.addColorStop(0, 'rgba(239, 68, 68, 0.28)');
        grad.addColorStop(1, 'rgba(239, 68, 68, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 22, 0, Math.PI*2);
        ctx.fill();
      });
    });
  } else if(currentView === '3D' && renderer3D) {
    update3DPeople();
    renderer3D.render(scene3D, camera3D);
    if(controls3D) controls3D.update();
  }

  animFrameId = requestAnimationFrame(loop);
}

function replanAILayout() {
  // Randomize locations slightly and apply collision-free algorithm
  booths.forEach(b => {
    if(b.id === 'stage' || b.id === 'gate_in') return;
    b.x = 0.08 + Math.random() * 0.68;
    b.y = 0.20 + Math.random() * 0.50;
  });

  resolveBoothOverlaps();
  if(currentView === '3D') build3DScene();
}

/* 4. THREE.JS 3D VIEW ENGINE */
let scene3D, camera3D, renderer3D, controls3D, booth3DGroup, people3DGroup;

function switchView(mode) {
  currentView = mode;
  document.getElementById('btn2D').classList.toggle('active', mode === '2D');
  document.getElementById('btn3D').classList.toggle('active', mode === '3D');

  const canvas3D = document.getElementById('canvas3D');
  if(mode === '3D') {
    canvas3D.style.display = 'block';
    init3D();
  } else {
    canvas3D.style.display = 'none';
  }
}

function init3D() {
  const container = document.getElementById('canvas3D');
  if(renderer3D) return;

  const w = container.clientWidth || 500;
  const h = container.clientHeight || 380;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w/h, 1, 1000);
  camera3D.position.set(0, 140, 160);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  controls3D = new THREE.OrbitControls(camera3D, renderer3D.domElement);
  controls3D.enableDamping = true;

  scene3D.add(new THREE.AmbientLight(0xffffff, 0.8));
  const light = new THREE.DirectionalLight(0xffffff, 0.6);
  light.position.set(40, 100, 40);
  scene3D.add(light);

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(220, 150),
    new THREE.MeshStandardMaterial({ color: 0x1e293b })
  );
  ground.rotation.x = -Math.PI / 2;
  scene3D.add(ground);

  booth3DGroup = new THREE.Group();
  people3DGroup = new THREE.Group();
  scene3D.add(booth3DGroup);
  scene3D.add(people3DGroup);

  build3DScene();
}

function build3DScene() {
  if(!booth3DGroup) return;
  while(booth3DGroup.children.length > 0) booth3DGroup.remove(booth3DGroup.children[0]);

  booths.forEach(b => {
    const bw = b.w * 220, bh = b.h * 150;
    const bx = (b.x + b.w/2 - 0.5) * 220;
    const bz = (b.y + b.h/2 - 0.5) * 150;
    const height = b.id === 'stage' ? 12 : 7;

    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(bw, height, bh),
      new THREE.MeshStandardMaterial({ color: new THREE.Color(b.color) })
    );
    mesh.position.set(bx, height/2, bz);
    booth3DGroup.add(mesh);
  });

  // Rebuild 3D People
  while(people3DGroup.children.length > 0) people3DGroup.remove(people3DGroup.children[0]);
  const geo = new THREE.SphereGeometry(1.5, 8, 8);
  const mat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });

  people.forEach(p => {
    const mesh = new THREE.Mesh(geo, mat);
    people3DGroup.add(mesh);
    p.mesh3D = mesh;
  });
}

function update3DPeople() {
  if(!venueCanvas || !people3DGroup) return;
  const w = venueCanvas.width, h = venueCanvas.height;
  people.forEach(p => {
    if(p.mesh3D) {
      p.mesh3D.position.set((p.x/w - 0.5)*220, 1.5, (p.y/h - 0.5)*150);
    }
  });
}

window.addEventListener('load', () => {
  initSim();
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=1150, scrolling=True)
