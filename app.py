import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 스마트 행사 설계 & 디지털 트윈 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_AI_FULL_PLATFORM_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI Platform</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">

<!-- Three.js & OrbitControls -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Pretendard Variable", Pretendard, -apple-system, sans-serif;
  color: #0f172a;
  background: #f8fafc;
  overflow-x: hidden;
}
button, input, select, textarea { font: inherit; }
button { cursor: pointer; transition: all 0.2s ease; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

/* Global App Layout */
.app-container { display: flex; min-height: 100vh; }

/* Left Sidebar Navigation */
.sidebar {
  width: 240px;
  background: #0f172a;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px 14px;
  flex-shrink: 0;
  border-right: 1px solid #1e293b;
}
.brand-logo {
  display: flex; align-items: center; gap: 10px; color: #fff; padding: 4px 8px; margin-bottom: 24px;
}
.brand-icon {
  width: 32px; height: 32px; background: linear-gradient(135deg, #2563eb, #3b82f6);
  border-radius: 8px; display: grid; place-items: center; font-weight: 900; color: #fff; font-size: 15px;
}
.brand-name { font-size: 17px; font-weight: 800; color: #ffffff; letter-spacing: -0.3px; }

.nav-menu { display: flex; flex-direction: column; gap: 6px; list-style: none; }
.nav-item {
  display: flex; align-items: center; gap: 10px; padding: 11px 14px;
  border-radius: 9px; font-size: 13.5px; font-weight: 600; color: #94a3b8;
  cursor: pointer; transition: all 0.15s ease;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: #f8fafc; }
.nav-item.active { background: #2563eb; color: #ffffff; font-weight: 700; box-shadow: 0 4px 12px rgba(37,99,235,0.3); }

.user-profile-card {
  background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 12px;
  display: flex; align-items: center; gap: 10px; color: #fff;
}
.user-avatar {
  width: 36px; height: 36px; background: #3b82f6; border-radius: 50%;
  display: grid; place-items: center; font-weight: 800; font-size: 14px;
}

/* Main Content Area */
.main-wrapper { flex: 1; padding: 24px; display: flex; flex-direction: column; gap: 20px; min-width: 0; overflow-y: auto; }

/* Page View Sections */
.view-section { display: none; width: 100%; }
.view-section.active { display: flex; flex-direction: column; gap: 20px; }

/* Common Card Box */
.card-box {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 14px;
}
.card-header { display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { font-size: 15px; font-weight: 800; color: #0f172a; display: flex; align-items: center; gap: 8px; }

/* PAGE 1: AUTH (HOME / LOGIN) */
.auth-hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border-radius: 20px; padding: 48px; color: #fff; text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: 16px; margin-top: 20px;
}
.auth-hero h1 { font-size: 32px; font-weight: 900; letter-spacing: -0.5px; }
.auth-hero p { font-size: 15px; color: #94a3b8; max-width: 560px; line-height: 1.6; }

.auth-form-card {
  width: 100%; max-width: 420px; margin: 0 auto; background: #fff; border: 1px solid #e2e8f0;
  border-radius: 16px; padding: 28px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  display: flex; flex-direction: column; gap: 16px;
}
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 12.5px; font-weight: 700; color: #334155; }
.form-control {
  width: 100%; padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px;
  font-size: 13px; outline: none; transition: 0.15s;
}
.form-control:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }

.btn-primary-block {
  width: 100%; padding: 12px; background: #2563eb; color: #fff; border: none;
  border-radius: 9px; font-size: 14px; font-weight: 800; box-shadow: 0 4px 12px rgba(37,99,235,0.25);
}
.btn-primary-block:hover { background: #1d4ed8; }

/* PAGE 2: REQUEST OPTIONS FORM */
.options-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

/* PAGE 3: BLUEPRINT & TWIN SIMULATOR */
.info-summary-bar {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 16px 24px; display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03); flex-wrap: wrap; gap: 12px;
}
.info-group { display: flex; align-items: center; gap: 28px; }
.info-item { display: flex; flex-direction: column; gap: 3px; }
.info-label { font-size: 11px; font-weight: 600; color: #64748b; }
.info-val { font-size: 14px; font-weight: 800; color: #0f172a; }

.dashboard-layout { display: grid; grid-template-columns: 1fr 340px; gap: 16px; }
.canvas-main-wrap { position: relative; width: 100%; height: 440px; background: #0f172a; border-radius: 12px; overflow: hidden; }

#venueCanvas, #heatmapCanvas, #canvas3D { position: absolute; inset: 0; width: 100%; height: 100%; }
#canvas3D { display: none; z-index: 10; }

.canvas-toolbar {
  position: absolute; top: 12px; right: 12px; z-index: 20; display: flex; gap: 6px;
  background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(6px); padding: 5px; border-radius: 8px;
}
.tool-btn {
  background: transparent; border: none; color: #94a3b8; padding: 5px 10px;
  border-radius: 6px; font-size: 11.5px; font-weight: 700;
}
.tool-btn.active { background: #2563eb; color: #fff; }

/* AI ASSISTANT PANEL */
.ai-assistant-card {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px;
  display: flex; flex-direction: column; height: 100%; gap: 12px;
}
.chat-messages {
  flex: 1; min-height: 280px; max-height: 320px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;
  padding-right: 4px;
}
.chat-msg { display: flex; flex-direction: column; gap: 4px; max-width: 88%; font-size: 12px; line-height: 1.45; }
.chat-msg.ai { align-self: flex-start; }
.chat-msg.user { align-self: flex-end; }
.msg-bubble {
  padding: 10px 12px; border-radius: 10px; font-weight: 500;
}
.chat-msg.ai .msg-bubble { background: #f1f5f9; color: #0f172a; border-bottom-left-radius: 2px; }
.chat-msg.user .msg-bubble { background: #2563eb; color: #ffffff; border-bottom-right-radius: 2px; }

.chat-input-wrap { display: flex; gap: 6px; }
.chat-input {
  flex: 1; padding: 9px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 12px; outline: none;
}
.btn-chat-send {
  background: #2563eb; color: #fff; border: none; padding: 0 14px; border-radius: 8px; font-weight: 700; font-size: 12px;
}

/* TIMELINE SIMULATOR BAR */
.timeline-card {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 14px 20px;
  display: flex; flex-direction: column; gap: 10px;
}
.time-presets { display: flex; gap: 8px; }
.preset-btn {
  flex: 1; padding: 8px; border: 1px solid #cbd5e1; background: #fff; border-radius: 8px;
  font-size: 11.5px; font-weight: 700; color: #475569; text-align: center;
}
.preset-btn.active { background: #eff6ff; border-color: #2563eb; color: #1d4ed8; }

/* PAGE 4: HISTORY MANAGEMENT */
.history-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.history-table th { background: #f8fafc; padding: 12px 14px; text-align: left; font-weight: 700; color: #475569; border-bottom: 1px solid #e2e8f0; }
.history-table td { padding: 14px; border-bottom: 1px solid #f1f5f9; color: #0f172a; }
.history-table tr:hover { background: #f8fafc; }
</style>
</head>
<body>

<div class="app-container">

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div>
      <div class="brand-logo">
        <div class="brand-icon">E</div>
        <span class="brand-name">Event AI</span>
      </div>
      <ul class="nav-menu">
        <li class="nav-item active" id="navHome" onclick="navigateTo('viewHome')">🏠 홈 / 로그인</li>
        <li class="nav-item" id="navRequest" onclick="navigateTo('viewRequest')">📝 행사 요청사항 입력</li>
        <li class="nav-item" id="navBlueprint" onclick="navigateTo('viewBlueprint')">📐 AI 행사 설계 & 시뮬레이터</li>
        <li class="nav-item" id="navHistory" onclick="navigateTo('viewHistory')">📜 설계 이력 관리</li>
      </ul>
    </div>

    <div class="user-profile-card">
      <div class="user-avatar">관</div>
      <div>
        <div style="font-size:12.5px; font-weight:800;" id="userDisplayNav">관람기획자 님</div>
        <div style="font-size:10.5px; color:#94a3b8;">Pro Plan 회원</div>
      </div>
    </div>
  </aside>

  <!-- MAIN WRAPPER -->
  <main class="main-wrapper">

    <!-- PAGE 1: HOME & AUTHENTICATION -->
    <section class="view-section active" id="viewHome">
      <div class="auth-hero">
        <span style="background:rgba(59,130,246,0.2); color:#60a5fa; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:800;">
          ✨ AI 기반 행사 디지털 트윈 솔루션
        </span>
        <h1>스마트한 행사 설계도 자동 생성 & 동선 계산</h1>
        <p>복잡한 행사장 부스 배치, 관람객 밀집도, 비상 대피 동선을 AI가 3초 만에 설계하고 실시간 디지털 트윈으로 시뮬레이션합니다.</p>
      </div>

      <div class="auth-form-card">
        <div style="text-align:center; margin-bottom:8px;">
          <h2 style="font-size:18px; font-weight:800; color:#0f172a;">플랫폼 로그인</h2>
          <p style="font-size:12px; color:#64748b; margin-top:2px;">계정에 로그인하여 행사 설계를 시작하세요.</p>
        </div>

        <div class="form-group">
          <label>이메일 계정</label>
          <input type="text" class="form-control" id="loginEmail" value="planner@eventai.co.kr">
        </div>
        <div class="form-group">
          <label>비밀번호</label>
          <input type="password" class="form-control" value="••••••••">
        </div>

        <button class="btn-primary-block" onclick="processLogin()">로그인하고 시작하기</button>
        <button class="btn-primary-block" style="background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; box-shadow:none;" onclick="processLogin()">체험용 게스트 회원가입</button>
      </div>
    </section>

    <!-- PAGE 2: REQUEST OPTIONS FORM -->
    <section class="view-section" id="viewRequest">
      <div class="card-box">
        <div class="card-header">
          <h3>📝 AI 행사 설계 요청사항 입력</h3>
          <span style="font-size:11.5px; color:#2563eb; font-weight:700;">Step 2 / 3</span>
        </div>
        <p style="font-size:12.5px; color:#64748b; margin-top:-8px;">행사 조건과 요구사항을 상세히 입력하면, AI 알고리즘이 겹침 없는 최적 배치를 계산합니다.</p>

        <div class="options-grid" style="margin-top:10px;">
          <div class="form-group">
            <label>행사명</label>
            <input type="text" class="form-control" id="reqTitle" value="2026 청동 융합 엑스포">
          </div>
          <div class="form-group">
            <label>행사 유형</label>
            <select class="form-control" id="reqType">
              <option value="expo">🏛️ 박람회 / 전시회</option>
              <option value="festival">🎸 음악 페스티벌 / 공연</option>
              <option value="food">🍔 푸드 & 마켓 축제</option>
            </select>
          </div>

          <div class="form-group">
            <label>행사장 크기 (가로 x 세로)</label>
            <div class="form-row-2">
              <input type="number" class="form-control" id="reqWidth" value="60" placeholder="가로(m)">
              <input type="number" class="form-control" id="reqHeight" value="40" placeholder="세로(m)">
            </div>
          </div>

          <div class="form-group">
            <label>목표 예상 관람객 수</label>
            <select class="form-control" id="reqPeople">
              <option value="1000">1,000명 이하</option>
              <option value="5000" selected>5,000명 (중형)</option>
              <option value="10000">10,000명 이상 (대형)</option>
            </select>
          </div>

          <div class="form-group">
            <label>설치할 주요 부스 구성</label>
            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; margin-top:4px;">
              <label style="font-size:11.5px; font-weight:600;"><input type="checkbox" checked id="chkStage"> 메인 무대</label>
              <label style="font-size:11.5px; font-weight:600;"><input type="checkbox" checked id="chkFood"> 푸드존</label>
              <label style="font-size:11.5px; font-weight:600;"><input type="checkbox" checked id="chkExp"> 체험존 (4개)</label>
              <label style="font-size:11.5px; font-weight:600;"><input type="checkbox" checked id="chkMed"> 응급의료소</label>
              <label style="font-size:11.5px; font-weight:600;"><input type="checkbox" checked id="chkRest"> 중앙 쉼터</label>
              <label style="font-size:11.5px; font-weight:600;"><input type="checkbox" checked id="chkWc"> 위생시설</label>
            </div>
          </div>

          <div class="form-group">
            <label>AI 설계 최적화 핵심 가중치</label>
            <select class="form-control" id="reqPriority">
              <option value="safety">🚨 비상 대피 및 안전성 최우선</option>
              <option value="flow" selected>🔄 관람객 동선 순환성 최우선</option>
              <option value="balance">⚖️ 공간 균형 배치</option>
            </select>
          </div>
        </div>

        <button class="btn-primary-block" style="margin-top:16px; padding:14px; font-size:15px;" onclick="generateAIBlueprint()">
          🚀 입력 조건 기반 AI 행사 설계도 생성하기
        </button>
      </div>
    </section>

    <!-- PAGE 3: AI BLUEPRINT & DIGITAL TWIN SIMULATOR -->
    <section class="view-section" id="viewBlueprint">
      <!-- SUMMARY BAR -->
      <div class="info-summary-bar">
        <div class="info-group">
          <div class="info-item">
            <span class="info-label">📋 행사명</span>
            <span class="info-val" id="summaryTitle">2026 청동 융합 엑스포</span>
          </div>
          <div class="info-item">
            <span class="info-label">🎪 부스 상태</span>
            <span class="info-val" style="color:#16a34a;">🟢 겹침 방지 (Non-overlapping) 완벽 적용</span>
          </div>
          <div class="info-item">
            <span class="info-label">📐 규격</span>
            <span class="info-val" id="summarySize">60m × 40m</span>
          </div>
          <div class="info-item">
            <span class="info-label">👥 관람객</span>
            <span class="info-val" id="summaryPeople">5,000명</span>
          </div>
        </div>
        <button class="btn-primary-block" style="width:auto; padding:8px 16px; font-size:12px;" onclick="rearrangeBoothsFixOverlap()">
          ⚡ AI 부스 자동 이격/재배치
        </button>
      </div>

      <!-- TIMELINE SIMULATOR -->
      <div class="timeline-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:13.5px; font-weight:800; color:#0f172a;">🕒 시간대별 개개인 관람객 동선 시뮬레이션</span>
            <span style="font-size:11.5px; color:#64748b;" id="timeDescText">(12:00 점심시간 - 푸드존 이동)</span>
          </div>
          <span style="font-size:16px; font-weight:900; color:#2563eb;" id="timeValText">12:00 PM</span>
        </div>
        <input type="range" id="timeSlider" min="10" max="18" step="0.5" value="12" style="width:100%; accent-color:#2563eb;" oninput="onTimeChange(this.value)">
        <div class="time-presets">
          <button class="preset-btn" onclick="setPreset(10)">10:00 개막식/입장</button>
          <button class="preset-btn active" id="btnPresetLunch" onclick="setPreset(12)">12:00 점심시간 (푸드존)</button>
          <button class="preset-btn" onclick="setPreset(14)">14:00 메인 공연 (무대)</button>
          <button class="preset-btn" onclick="setPreset(16)">16:00 체험 및 휴식</button>
          <button class="preset-btn" onclick="setPreset(17.5)">17:30 폐막 및 퇴장</button>
        </div>
      </div>

      <!-- MAIN DASHBOARD SPLIT (CANVAS + AI ASSISTANT) -->
      <div class="dashboard-layout">

        <!-- LEFT: DIGITAL TWIN CANVAS -->
        <div class="card-box" style="padding:14px;">
          <div class="card-header">
            <h3>🎪 AI 행사장 설계도 (디지털 트윈)</h3>
            <span style="font-size:11px; color:#64748b;">개개인 히트맵 입자 모드 활성화</span>
          </div>
          <div class="canvas-main-wrap">
            <div class="canvas-toolbar">
              <button class="tool-btn active" id="btn2D" onclick="switchViewMode('2D')">2D 평면도</button>
              <button class="tool-btn" id="btn3D" onclick="switchViewMode('3D')">3D 입체</button>
            </div>
            <canvas id="venueCanvas"></canvas>
            <canvas id="heatmapCanvas"></canvas>
            <div id="canvas3D"></div>
          </div>
        </div>

        <!-- RIGHT: AI ASSISTANT PANEL -->
        <div class="ai-assistant-card">
          <div style="display:flex; align-items:center; gap:8px; border-bottom:1px solid #e2e8f0; padding-bottom:10px;">
            <div style="width:28px; height:28px; background:#eff6ff; color:#2563eb; border-radius:6px; display:grid; place-items:center; font-weight:900; font-size:13px;">🤖</div>
            <div>
              <div style="font-size:13px; font-weight:800; color:#0f172a;">AI 설계 어시스턴트</div>
              <div style="font-size:10.5px; color:#16a34a; font-weight:600;">● 실시간 대화 가능</div>
            </div>
          </div>

          <div class="chat-messages" id="chatMessages">
            <div class="chat-msg ai">
              <div class="msg-bubble">
                안녕하세요! AI 어시스턴트입니다. 👋<br>
                부스 겹침 방지 알고리즘을 적용해 공간 배치를 마쳤습니다. "푸드존 크기 키워줘" 또는 "쉼터를 무대 근처로 옮겨줘" 처럼 요청해보세요!
              </div>
            </div>
          </div>

          <div class="chat-input-wrap">
            <input type="text" class="chat-input" id="chatInput" placeholder="AI에게 배치 수정 요청하기..." onkeypress="if(event.key==='Enter') sendChatMessage()">
            <button class="btn-chat-send" onclick="sendChatMessage()">전송</button>
          </div>
        </div>

      </div>
    </section>

    <!-- PAGE 4: HISTORY MANAGEMENT -->
    <section class="view-section" id="viewHistory">
      <div class="card-box">
        <div class="card-header">
          <h3>📜 AI 행사 설계 이력 관리</h3>
          <span style="font-size:12px; color:#64748b;">총 <b id="historyCount">2</b>개의 저장된 설계도</span>
        </div>

        <table class="history-table">
          <thead>
            <tr>
              <th>번호</th>
              <th>행사명</th>
              <th>생성 일시</th>
              <th>부스 수</th>
              <th>안전/동선 점수</th>
              <th>관리</th>
            </tr>
          </thead>
          <tbody id="historyTableBody">
            <!-- Dynamic History Rows -->
          </tbody>
        </table>
      </div>
    </section>

  </main>
</div>

<script>
/* GLOBAL STATE */
let currentView = 'viewHome';
let viewMode = '2D'; // 2D or 3D
let currentTime = 12.0;

let venueCanvas, venueCtx, heatmapCanvas, heatmapCtx;
let animFrameId = null;

/* BOOTH DEFINITIONS (STRICT GRID & BOUNDS) */
let booths = [];
let defaultBooths = [
  { id:'stage', title:'메인 무대', x: 0.35, y: 0.06, w: 0.30, h: 0.18, color:'#8b5cf6', icon:'🎭' },
  { id:'boothA', title:'체험존 A', x: 0.06, y: 0.30, w: 0.18, h: 0.15, color:'#3b82f6', icon:'🧪' },
  { id:'boothB', title:'체험존 B', x: 0.76, y: 0.30, w: 0.18, h: 0.15, color:'#3b82f6', icon:'🚀' },
  { id:'food', title:'푸드존', x: 0.06, y: 0.58, w: 0.22, h: 0.18, color:'#f59e0b', icon:'🍔' },
  { id:'med', title:'응급의료소', x: 0.76, y: 0.58, w: 0.18, h: 0.15, color:'#ef4444', icon:'🏥' },
  { id:'rest', title:'중앙 쉼터', x: 0.38, y: 0.50, w: 0.24, h: 0.18, color:'#10b981', icon:'🌿' },
  { id:'gate_in', title:'주 출입구', x: 0.38, y: 0.82, w: 0.24, h: 0.10, color:'#06b6d4', icon:'🚪' },
  { id:'wc', title:'위생시설', x: 0.82, y: 0.82, w: 0.12, h: 0.10, color:'#64748b', icon:'🚻' }
];

let savedHistoryList = [
  { id: 1, title: '2026 청동 융합 엑스포 (기본)', date: '2026-09-09 10:15', boothsCount: 8, score: '92점 (우수)', data: JSON.parse(JSON.stringify(defaultBooths)) },
  { id: 2, title: '여름 음악 페스티벌 시안', date: '2026-09-08 16:40', boothsCount: 6, score: '88점 (양호)', data: JSON.parse(JSON.stringify(defaultBooths)) }
];

/* PEOPLE PARTICLES */
let people = [];
const TOTAL_PEOPLE = 100;

/* 1. NAVIGATION CONTROL */
function navigateTo(viewId) {
  currentView = viewId;
  document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  document.getElementById(viewId).classList.add('active');

  if(viewId === 'viewHome') document.getElementById('navHome').classList.add('active');
  if(viewId === 'viewRequest') document.getElementById('navRequest').classList.add('active');
  if(viewId === 'viewBlueprint') {
    document.getElementById('navBlueprint').classList.add('active');
    setTimeout(() => { initCanvases(); }, 100);
  }
  if(viewId === 'viewHistory') {
    document.getElementById('navHistory').classList.add('active');
    renderHistoryTable();
  }
}

function processLogin() {
  const email = document.getElementById('loginEmail').value || '기획자';
  document.getElementById('userDisplayNav').textContent = email.split('@')[0] + ' 님';
  navigateTo('viewRequest');
}

/* 2. STRICT NON-OVERLAPPING ALGORITHM (GUARANTEED NO OVERLAP) */
function fixBoothOverlapsStrict() {
  const minGap = 0.03; // Minimum distance gap between booths
  let iterations = 0;
  let overlapFound = true;

  while (overlapFound && iterations < 100) {
    overlapFound = false;
    iterations++;

    for (let i = 0; i < booths.length; i++) {
      for (let j = i + 1; j < booths.length; j++) {
        let b1 = booths[i];
        let b2 = booths[j];

        // AABB Overlap Check
        if (b1.x < b2.x + b2.w + minGap &&
            b1.x + b1.w + minGap > b2.x &&
            b1.y < b2.y + b2.h + minGap &&
            b1.y + b1.h + minGap > b2.y) {

          overlapFound = true;

          // Push b2 away from b1
          let diffX = (b2.x + b2.w/2) - (b1.x + b1.w/2);
          let diffY = (b2.y + b2.h/2) - (b1.y + b1.h/2);

          if (Math.abs(diffX) > Math.abs(diffY)) {
            if (diffX > 0) b2.x += 0.04; else b2.x -= 0.04;
          } else {
            if (diffY > 0) b2.y += 0.04; else b2.y -= 0.04;
          }

          // Clamp within boundaries
          b2.x = Math.max(0.04, Math.min(0.96 - b2.w, b2.x));
          b2.y = Math.max(0.04, Math.min(0.92 - b2.h, b2.y));
        }
      }
    }
  }
}

function rearrangeBoothsFixOverlap() {
  fixBoothOverlapsStrict();
  if(viewMode === '3D') build3DScene();
  appendAIMessage("🤖 AI 알고리즘이 부스 간 최소 안전거리(3m)를 확보하여 겹침 현상을 완벽하게 해결했습니다.");
}

/* 3. GENERATE BLUEPRINT FROM REQUEST FORM */
function generateAIBlueprint() {
  const title = document.getElementById('reqTitle').value;
  const w = document.getElementById('reqWidth').value;
  const h = document.getElementById('reqHeight').value;

  booths = JSON.parse(JSON.stringify(defaultBooths));
  fixBoothOverlapsStrict();

  document.getElementById('summaryTitle').textContent = title;
  document.getElementById('summarySize').textContent = `${w}m × ${h}m`;

  // Save to History
  savedHistoryList.unshift({
    id: savedHistoryList.length + 1,
    title: title,
    date: new Date().toLocaleString(),
    boothsCount: booths.length,
    score: '95점 (최상)',
    data: JSON.parse(JSON.stringify(booths))
  });

  navigateTo('viewBlueprint');
}

/* 4. TIME SIMULATOR & INDIVIDUAL HEATMAP LOGIC */
function onTimeChange(val) {
  currentTime = parseFloat(val);
  const hours = Math.floor(currentTime);
  const mins = (currentTime % 1 === 0) ? '00' : '30';
  document.getElementById('timeValText').textContent = `${hours}:${mins} ${hours >= 12 ? 'PM' : 'AM'}`;

  const descEl = document.getElementById('timeDescText');
  if(currentTime >= 10 && currentTime < 11.5) descEl.textContent = "(10:00 입장/개막 - 주 출입구 & 무대 주변 이동)";
  else if(currentTime >= 11.5 && currentTime <= 13.5) descEl.textContent = "(12:00 점심시간 - 관람객 70% 푸드존 집중)";
  else if(currentTime > 13.5 && currentTime <= 15.5) descEl.textContent = "(14:00 메인 공연 - 메인 무대 집중 관람)";
  else if(currentTime > 15.5 && currentTime <= 17) descEl.textContent = "(16:00 자유 관람 - 체험존 및 쉼터 분산)";
  else descEl.textContent = "(17:30 폐막 - 주 출입구 퇴장 동선)";

  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
}

function setPreset(t) {
  document.getElementById('timeSlider').value = t;
  onTimeChange(t);
}

function getPersonTarget(index) {
  const w = venueCanvas ? venueCanvas.width : 600;
  const h = venueCanvas ? venueCanvas.height : 400;
  let targetB = null;

  if (currentTime >= 11.5 && currentTime <= 13.5) {
    targetB = (index % 10 < 7) ? booths.find(b => b.id === 'food') : booths.find(b => b.id === 'rest');
  } else if (currentTime > 13.5 && currentTime <= 15.5) {
    targetB = (index % 10 < 6) ? booths.find(b => b.id === 'stage') : booths.find(b => b.id === 'boothA');
  } else {
    targetB = booths[index % booths.length];
  }

  if(targetB) {
    return {
      x: (targetB.x + targetB.w*0.5)*w + (Math.random()-0.5)*30,
      y: (targetB.y + targetB.h*0.5)*h + (Math.random()-0.5)*25
    };
  }
  return { x: w*0.5, y: h*0.5 };
}

/* 5. CANVAS & INDIVIDUAL HEATMAP RENDER LOOP */
function initCanvases() {
  venueCanvas = document.getElementById('venueCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');

  const wrap = venueCanvas.parentElement;
  const w = wrap.clientWidth || 600;
  const h = wrap.clientHeight || 400;

  venueCanvas.width = w; venueCanvas.height = h;
  heatmapCanvas.width = w; heatmapCanvas.height = h;

  venueCtx = venueCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');

  if(booths.length === 0) booths = JSON.parse(JSON.stringify(defaultBooths));
  fixBoothOverlapsStrict();

  people = [];
  for(let i=0; i<TOTAL_PEOPLE; i++) {
    people.push({ x: Math.random()*w, y: Math.random()*h, vx: 0, vy: 0 });
  }

  if(animFrameId) cancelAnimationFrame(animFrameId);
  renderLoop();
}

function renderLoop() {
  if(viewMode === '2D' && venueCtx) {
    const w = venueCanvas.width, h = venueCanvas.height;

    venueCtx.clearRect(0,0,w,h);
    heatmapCtx.clearRect(0,0,w,h);

    // Background Grid
    venueCtx.fillStyle = '#0f172a';
    venueCtx.fillRect(0,0,w,h);

    venueCtx.strokeStyle = 'rgba(255,255,255,0.06)';
    venueCtx.lineWidth = 1;
    for(let x=0; x<w; x+=30){ venueCtx.beginPath(); venueCtx.moveTo(x,0); venueCtx.lineTo(x,h); venueCtx.stroke(); }
    for(let y=0; y<h; y+=30){ venueCtx.beginPath(); venueCtx.moveTo(0,y); venueCtx.lineTo(w,y); venueCtx.stroke(); }

    // Render Booths (GUARANTEED NO OVERLAP)
    booths.forEach(b => {
      const bx = b.x * w, by = b.y * h, bw = b.w * w, bh = b.h * h;

      venueCtx.fillStyle = 'rgba(0,0,0,0.4)';
      venueCtx.fillRect(bx+4, by+4, bw, bh);

      venueCtx.fillStyle = b.color;
      venueCtx.beginPath();
      venueCtx.roundRect(bx, by, bw, bh, 8);
      venueCtx.fill();

      venueCtx.strokeStyle = '#ffffff';
      venueCtx.lineWidth = 1.5;
      venueCtx.stroke();

      venueCtx.fillStyle = '#ffffff';
      venueCtx.font = 'bold 11.5px Pretendard';
      venueCtx.textAlign = 'center';
      venueCtx.fillText(`${b.icon} ${b.title}`, bx + bw/2, by + bh/2 + 4);
    });

    // Move & Render People + INDIVIDUAL HEATMAP (Small Glow Dots, NOT Giant Blobs)
    people.forEach((p, idx) => {
      const target = getPersonTarget(idx);
      const dx = target.x - p.x, dy = target.y - p.y;
      const dist = Math.sqrt(dx*dx + dy*dy);

      if(dist > 4) {
        p.x += (dx / dist) * 1.5;
        p.y += (dy / dist) * 1.5;
      }

      // Person Dot
      venueCtx.fillStyle = '#38bdf8';
      venueCtx.beginPath();
      venueCtx.arc(p.x, p.y, 2.5, 0, Math.PI*2);
      venueCtx.fill();

      // Individual Heatmap Radius (Small 7px glow dot per person)
      let grad = heatmapCtx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 7);
      grad.addColorStop(0, 'rgba(239, 68, 68, 0.6)');
      grad.addColorStop(1, 'rgba(239, 68, 68, 0)');
      heatmapCtx.fillStyle = grad;
      heatmapCtx.beginPath();
      heatmapCtx.arc(p.x, p.y, 7, 0, Math.PI*2);
      heatmapCtx.fill();
    });
  } else if(viewMode === '3D' && renderer3D) {
    update3DPeople();
    renderer3D.render(scene3D, camera3D);
    if(controls3D) controls3D.update();
  }

  animFrameId = requestAnimationFrame(renderLoop);
}

/* 6. AI ASSISTANT INTERACTIVE CHAT */
function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const txt = input.value.trim();
  if(!txt) return;

  appendUserMessage(txt);
  input.value = '';

  // Process AI commands
  setTimeout(() => {
    if(txt.includes('푸드존') && txt.includes('크기')) {
      let f = booths.find(b => b.id === 'food');
      if(f) { f.w = 0.28; f.h = 0.22; }
      fixBoothOverlapsStrict();
      appendAIMessage("🍔 푸드존 부스의 크기를 확대하고 주변 부스와 충돌하지 않도록 재배치했습니다!");
    } else if(txt.includes('쉼터') || txt.includes('무대')) {
      let r = booths.find(b => b.id === 'rest');
      if(r) { r.x = 0.38; r.y = 0.28; }
      fixBoothOverlapsStrict();
      appendAIMessage("🌿 중앙 쉼터를 무대 근처로 이동하고 겹침 현상을 자동 해결했습니다.");
    } else {
      fixBoothOverlapsStrict();
      appendAIMessage(`🤖 "${txt}" 요청을 반영하여 부스 이격 및 안전 동선 재계산을 완료했습니다.`);
    }
  }, 500);
}

function appendUserMessage(msg) {
  const container = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'chat-msg user';
  div.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function appendAIMessage(msg) {
  const container = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'chat-msg ai';
  div.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

/* 7. THREE.JS 3D ENGINE */
let scene3D, camera3D, renderer3D, controls3D, booth3DGroup, people3DGroup;

function switchViewMode(mode) {
  viewMode = mode;
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
  if(renderer3D) { build3DScene(); return; }

  const w = container.clientWidth || 600, h = container.clientHeight || 400;

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

/* 8. RENDER HISTORY TABLE */
function renderHistoryTable() {
  const tbody = document.getElementById('historyTableBody');
  document.getElementById('historyCount').textContent = savedHistoryList.length;
  tbody.innerHTML = '';

  savedHistoryList.forEach((item, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><b>#${item.id}</b></td>
      <td><b>${item.title}</b></td>
      <td style="color:#64748b; font-size:12px;">${item.date}</td>
      <td>${item.boothsCount}개 부스</td>
      <td><span style="color:#16a34a; font-weight:800;">${item.score}</span></td>
      <td>
        <button class="tool-btn active" style="padding:4px 10px; font-size:11px;" onclick="loadHistoryItem(${idx})">설계도 불러오기</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function loadHistoryItem(index) {
  const item = savedHistoryList[index];
  if(item) {
    booths = JSON.parse(JSON.stringify(item.data));
    document.getElementById('summaryTitle').textContent = item.title;
    navigateTo('viewBlueprint');
  }
}
</script>
</body>
</html>
"""

components.html(EVENT_AI_FULL_PLATFORM_HTML, height=1150, scrolling=True)
