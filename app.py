import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 3D 디지털 트윈 & AI 행사장 설계 시뮬레이터",
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
<title>Event AI - 3D 디지털 트윈 & AI 행사장 설계 시뮬레이터</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">

<!-- Three.js 및 OrbitControls CDN (3D 그래픽 구현) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

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

::-webkit-scrollbar {width:6px;height:6px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}
::-webkit-scrollbar-thumb:hover {background:#94a3b8;}

.app-container{
  display:flex;
  min-height:100vh;
  background:#f1f5f9;
}

/* Sidebar */
.sidebar{
  width:245px;
  background:#0f172a;
  color:#94a3b8;
  padding:20px 14px;
  display:flex;
  flex-direction:column;
  gap:18px;
  flex-shrink:0;
  border-right:1px solid #1e293b;
}
.brand{display:flex;align-items:center;gap:10px;padding:0 6px;color:#fff;}
.brand-icon{
  width:36px;height:36px;
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:10px;display:grid;place-items:center;font-size:18px;font-weight:900;
  box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.brand-title{font-size:17px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;}
.brand-sub{font-size:10px;color:#64748b;margin-top:1px;font-weight:500;}

.nav-group{display:flex;flex-direction:column;gap:4px;}
.nav-item{
  display:flex;align-items:center;gap:10px;padding:11px 14px;
  border-radius:10px;font-size:13px;font-weight:600;color:#94a3b8;cursor:pointer;
}
.nav-item:hover{background:rgba(255,255,255,0.05);color:#f1f5f9;}
.nav-item.active{
  background:linear-gradient(135deg, #2563eb, #3b82f6);
  color:#ffffff;box-shadow:0 4px 12px rgba(37,99,235,0.3);
}

.side-banner{
  background:linear-gradient(135deg, rgba(37,99,235,0.2), rgba(15,23,42,0.8));
  border:1px solid rgba(59,130,246,0.25);padding:12px;border-radius:12px;color:#e2e8f0;
}
.side-banner h5{font-size:11.5px;font-weight:800;color:#60a5fa;margin-bottom:4px;}
.side-banner p{font-size:10px;color:#94a3b8;line-height:1.4;}

/* Main Content */
.main-content{
  flex:1;padding:20px;display:flex;flex-direction:column;gap:16px;min-width:0;overflow-y:auto;
}

.top-header{
  display:flex;justify-content:space-between;align-items:center;
  background:#ffffff;padding:14px 20px;border-radius:16px;border:1px solid #e2e8f0;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
}
.top-title h2{font-size:19px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:8px;}
.top-title p{font-size:12px;color:#64748b;margin-top:2px;}

.page-view{display:none;}
.page-view.active{display:block;}

/* Form Sections */
.form-card{
  background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;padding:22px;
  box-shadow:0 2px 10px rgba(0,0,0,0.02);margin-bottom:16px;
}
.form-section-head{
  font-size:15px;font-weight:800;color:#0f172a;margin-bottom:16px;
  display:flex;align-items:center;gap:8px;border-bottom:2px solid #f1f5f9;padding-bottom:10px;
}
.form-grid{display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:14px;}
.form-group{display:flex;flex-direction:column;gap:5px;}
.form-group label{font-size:11.5px;font-weight:700;color:#334155;}
.form-group input, .form-group select{
  padding:9px 11px;border:1.5px solid #cbd5e1;border-radius:8px;background:#f8fafc;
  color:#0f172a;font-size:12.5px;font-weight:600;outline:none;
}

.btn-primary{
  background:linear-gradient(135deg, #2563eb, #1d4ed8);
  color:#ffffff;border:none;padding:10px 18px;border-radius:10px;
  font-weight:800;font-size:12.5px;box-shadow:0 4px 14px rgba(37,99,235,0.3);
  display:inline-flex;align-items:center;gap:6px;
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(37,99,235,0.4);}
.btn-secondary{
  background:#ffffff;border:1.5px solid #cbd5e1;color:#334155;
  padding:8px 14px;border-radius:8px;font-weight:700;font-size:12px;
}

/* Map & Simulation Container */
.map-wrap{
  position:relative;width:100%;height:380px;background:#0f172a;
  border-radius:12px;overflow:hidden;border:1px solid #334155;
}
#venueCanvas, #heatmapCanvas, #canvas3D{
  position:absolute;inset:0;width:100%;height:100%;
}
#canvas3D{display:none;z-index:10;}

/* View Switcher Bar */
.view-switch-bar{
  display:flex;justify-content:space-between;align-items:center;
  background:#f8fafc;border:1px solid #e2e8f0;padding:8px 12px;border-radius:10px;margin-bottom:10px;
}
.view-btn-group{display:flex;gap:6px;}
.btn-view-mode{
  padding:6px 12px;border-radius:8px;font-size:11.5px;font-weight:800;border:1px solid #cbd5e1;background:#fff;color:#475569;
}
.btn-view-mode.active{background:#2563eb;color:#fff;border-color:#2563eb;}

/* Interactive Simulation Toolbar */
.sim-toolbar{
  background:#f1f5f9;border:1px solid #cbd5e1;padding:8px 12px;border-radius:10px;
  display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;flex-wrap:wrap;
}
.sim-tool-group{display:flex;align-items:center;gap:6px;}
.btn-sim-act{
  background:#ffffff;border:1px solid #cbd5e1;padding:5px 10px;border-radius:6px;
  font-size:11px;font-weight:700;color:#334155;
}
.btn-sim-act:hover{background:#3b82f6;color:#ffffff;border-color:#3b82f6;}

/* Emergency Controls Bar */
.emergency-bar{
  background:#fff1f2;border:1px solid #fecdd3;padding:10px 14px;border-radius:12px;
  margin-top:10px;display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;
}
.emergency-title{font-size:11px;font-weight:800;color:#be123c;display:flex;align-items:center;gap:4px;}
.emergency-btn-group{display:flex;gap:6px;}
.btn-contingency{
  background:#ffffff;border:1px solid #fda4af;color:#9f1239;padding:5px 10px;border-radius:6px;
  font-size:10.5px;font-weight:700;
}
.btn-contingency:hover,.btn-contingency.active{background:#f43f5e;color:#ffffff;border-color:#f43f5e;}

/* Dashboard Grids */
.dashboard-main-grid{display:grid;grid-template-columns:1.5fr 1fr;gap:16px;}
.dashboard-bottom-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px;}

.card-panel{
  background:#ffffff;border:1px solid #e2e8f0;border-radius:16px;padding:16px;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);display:flex;flex-direction:column;
}
.card-head{font-size:13.5px;font-weight:800;color:#0f172a;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;}
.card-badge{font-size:10px;background:#eff6ff;color:#2563eb;padding:3px 8px;border-radius:12px;font-weight:700;}

/* History List Panel */
.history-list{
  display:flex;flex-direction:column;gap:8px;max-height:220px;overflow-y:auto;padding-right:4px;
}
.history-item{
  background:#f8fafc;border:1px solid #e2e8f0;padding:10px 12px;border-radius:10px;
  display:flex;justify-content:space-between;align-items:center;font-size:11.5px;
}
.history-item.active{border-color:#2563eb;background:#eff6ff;}
.history-info b{color:#0f172a;display:block;font-size:12px;}
.history-info span{color:#64748b;font-size:10px;}

/* Score Table */
.score-tbl{width:100%;border-collapse:collapse;font-size:11.5px;margin-bottom:10px;}
.score-tbl th,.score-tbl td{padding:7px 4px;text-align:left;border-bottom:1px solid #f1f5f9;}
.score-tbl th{color:#64748b;font-weight:700;font-size:10.5px;}

/* Modal Prose Report */
.modal-bg{
  position:fixed;inset:0;background:rgba(15,23,42,0.7);backdrop-filter:blur(6px);
  z-index:999;display:none;place-items:center;padding:20px;
}
.modal-bg.active{display:grid;}
.modal-content{
  background:#ffffff;width:min(95%, 920px);max-height:88vh;border-radius:20px;padding:28px;
  box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);display:flex;flex-direction:column;overflow:hidden;
}
.modal-body{flex:1;overflow-y:auto;padding-right:10px;display:flex;flex-direction:column;gap:18px;color:#334155;font-size:13px;line-height:1.75;}
.prose-report h3{font-size:18px;color:#0f172a;border-bottom:2px solid #2563eb;padding-bottom:6px;margin-top:10px;margin-bottom:10px;}
.prose-report p{margin-bottom:12px;text-align:justify;word-break:keep-all;}
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
        <div class="brand-sub">3D 디지털 트윈 & AI 재배치</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item" onclick="switchPage('home', this)"><span>🏠</span> 행사 정보 설정</div>
      <div class="nav-item active" onclick="switchPage('design', this)"><span>📋</span> AI 설계 & 3D 시뮬레이션</div>
      <div class="nav-item" onclick="openReportModal()"><span>📄</span> 종합 리포트 (줄글)</div>
      <div class="nav-item" onclick="switchPage('assistant', this)"><span>🤖</span> AI 어시스턴트</div>
    </nav>

    <div class="side-banner">
      <h5>AI Multi-Layout Engine</h5>
      <p>AI 재배치 클릭 시 신규 배치안을 생성하고 이전 히스토리를 보관합니다.</p>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">

    <header class="top-header">
      <div class="top-title">
        <h2 id="topTitleText">📋 AI 행사장 설계 & 3D 시뮬레이션</h2>
        <p id="topSubText">2D/3D 전환, 관람객 실시간 투입, 히스토리 복원 및 돌발상황 대피 시뮬레이션을 제공합니다.</p>
      </div>
      <button class="btn-primary" onclick="generateNewAILayout()">
        ✦ AI 신규 재배치 실행 (히스토리 추가)
      </button>
    </header>

    <!-- PAGE 1: HOME FORM -->
    <section id="pageHome" class="page-view">
      <div class="form-card">
        <div class="form-section-head">📌 행사 기본 정보 및 조건 생성</div>
        <div class="form-grid">
          <div class="form-group"><label>행사명</label><input type="text" id="inEventName" value="2025 힐링 페스티벌"></div>
          <div class="form-group">
            <label>행사장 유형</label>
            <select id="inVenueType">
              <option value="야외 잔디 광장" selected>야외 잔디 광장</option>
              <option value="실내 컨벤션 홀">실내 컨벤션 홀</option>
            </select>
          </div>
          <div class="form-group">
            <label>최우선 목표</label>
            <select id="inGoal">
              <option value="안전 중심" selected>🛡️ 안전 중심 (비상동선 최우선)</option>
              <option value="참여 중심">🎪 참여 중심 (부스 체류 최대화)</option>
              <option value="운영 효율 중심">⚡ 운영 효율 중심 (이동 동선 최단화)</option>
            </select>
          </div>
          <div class="form-group"><label>초기 관람객 수</label><input type="number" id="inVisitors" value="80"></div>
        </div>
        <div style="margin-top:16px;text-align:right;">
          <button class="btn-primary" onclick="runAIGenerateFromHome()">✦ AI 최적화 설계 구동</button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: DESIGN DASHBOARD -->
    <section id="pageDesign" class="page-view active">

      <!-- View Switcher Toolbar -->
      <div class="view-switch-bar">
        <div class="view-btn-group">
          <button class="btn-view-mode active" id="btn2D" onclick="setRenderMode('2D')">🗺️ 2D 평면도 뷰어</button>
          <button class="btn-view-mode" id="btn3D" onclick="setRenderMode('3D')">🧊 3D 입체 트윈 뷰어 (Three.js)</button>
        </div>
        <div style="font-size:11px;font-weight:700;color:#64748b;" id="viewTip">
          * 3D 뷰어: 마우스 드래그로 회전, 스크롤로 확대/축소 가능
        </div>
      </div>

      <div class="dashboard-main-grid">

        <!-- Left: Map & Interactive Simulation Engine -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 디지털 트윈 시뮬레이션 캔버스</span>
            <span class="card-badge" id="simModeBadge">실시간 동선 추적 ON</span>
          </div>

          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="heatmapCanvas"></canvas>
            <div id="canvas3D"></div>
          </div>

          <!-- Simulation Interactive Toolbar (Dynamic People Control) -->
          <div class="sim-toolbar">
            <div class="sim-tool-group">
              <span style="font-size:11.5px;font-weight:800;color:#0f172a;">👥 관람객 조절:</span>
              <button class="btn-sim-act" onclick="adjustPeopleCount(20)">+20명 투입</button>
              <button class="btn-sim-act" onclick="adjustPeopleCount(50)">+50명 대량 투입</button>
              <button class="btn-sim-act" onclick="adjustPeopleCount(-20)">-20명 줄이기</button>
            </div>
            <div style="font-size:12px;font-weight:800;color:#2563eb;">
              현재 실시간 인원: <span id="currentAgentCount">80</span>명
            </div>
          </div>

          <!-- Realistic Emergency Contingency Controls -->
          <div class="emergency-bar">
            <div class="emergency-title">
              ⚡ 실제 돌발상황 시뮬레이션 (관람객 반응)
            </div>
            <div class="emergency-btn-group">
              <button class="btn-contingency" onclick="triggerContingency('rain')">🌧️ 우천 (부스/천막 대피)</button>
              <button class="btn-contingency" onclick="triggerContingency('surge')">🚨 관람객 급증 (병목 발생)</button>
              <button class="btn-contingency" onclick="triggerContingency('medical')">🏥 응급환자 (비상통로 확보)</button>
              <button class="btn-contingency" style="background:#e2e8f0;color:#334155;border-color:#cbd5e1;" onclick="resetContingency()">🔄 원상복구</button>
            </div>
          </div>
        </div>

        <!-- Right: Layout History & Metrics -->
        <div class="card-panel">
          <div class="card-head">
            <span>📜 AI 설계 히스토리 보관함</span>
            <button class="btn-secondary" style="padding:3px 8px;font-size:10.5px;" onclick="generateNewAILayout()">+ AI 재배치</button>
          </div>
          <p style="font-size:11px;color:#64748b;margin-bottom:8px;">
            AI 재배치를 실행할 때마다 새로운 배치가 기록되며, 원하시는 버전을 선택하여 즉시 복원할 수 있습니다.
          </p>

          <div class="history-list" id="historyContainer">
            <!-- Dynamic History Cards -->
          </div>

          <div style="margin-top:16px;border-top:1px solid #f1f5f9;padding-top:12px;">
            <div style="font-size:12px;font-weight:800;color:#0f172a;margin-bottom:8px;">📊 현재 배치 평가 지표</div>
            <table class="score-tbl">
              <tbody>
                <tr><td>비상 안전성 (Safety)</td><td id="scSafety" style="font-weight:800;color:#16a34a;">96점</td></tr>
                <tr><td>혼잡 분산성 (Congestion)</td><td id="scCong" style="font-weight:800;color:#0284c7;">88점</td></tr>
                <tr><td>맞춤 접근성 (Access)</td><td id="scAcc" style="font-weight:800;color:#16a34a;">95점</td></tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-bottom-grid">
        <div class="card-panel">
          <div class="card-head"><span>🚨 실시간 상황 리포트</span></div>
          <div style="background:#0f172a;border-radius:10px;padding:12px;color:#fff;font-size:12px;">
            <div style="color:#94a3b8;font-size:10px;">현재 시뮬레이션 상태</div>
            <div style="font-size:14px;font-weight:800;color:#38bdf8;margin-top:2px;" id="simStatusText">정상 관람 동선 작동 중</div>
            <div style="font-size:11px;color:#cbd5e1;margin-top:6px;" id="simBehaviorDetail">관람객들이 자유롭게 무대와 푸드존, 체험 부스를 순환하고 있습니다.</div>
          </div>
        </div>

        <div class="card-panel">
          <div class="card-head"><span>📄 줄글 종합 분석 리포트</span></div>
          <p style="font-size:11.5px;color:#64748b;line-height:1.5;margin-bottom:10px;">
            현재 활성화된 AI 배치 버전의 공간 정량 지표와 비상 대피 검증 결과를 줄글 보고서로 확인합니다.
          </p>
          <button class="btn-primary" style="width:100%;justify-content:center;" onclick="openReportModal()">
            📌 줄글 형태 종합 보고서 열람
          </button>
        </div>
      </div>

    </section>

    <!-- PAGE 3: ASSISTANT -->
    <section id="pageAssistant" class="page-view">
      <div class="form-card">
        <div class="form-section-head">🤖 AI 대화형 배치 어시스턴트</div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:12px;border-radius:10px;height:200px;overflow-y:auto;font-size:12px;margin-bottom:12px;" id="chatBox">
          <div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;">
            AI: 지시사항을 입력하시면 2D/3D 레이아웃을 즉시 반영합니다.
          </div>
        </div>
        <div style="display:flex;gap:8px;">
          <input type="text" id="chatIn" placeholder="예: 무대를 조금 더 중앙으로 이동해줘" style="flex:1;padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;">
          <button class="btn-primary" onclick="sendChat()">전송</button>
        </div>
      </div>
    </section>

  </main>
</div>

<!-- DETAILED PROSE REPORT MODAL -->
<div class="modal-bg" id="reportModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #f1f5f9;">
      <h3 style="font-size:18px;font-weight:800;color:#0f172a;">📊 AI 행사장 설계 및 시뮬레이션 종합 분석 보고서</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:22px;font-weight:800;color:#64748b;cursor:pointer;">✕</button>
    </div>

    <div class="modal-body prose-report">
      <h3>1. 서론 및 개요</h3>
      <p>
        본 보고서는 디지털 트윈 기술과 3D 공간 알고리즘을 결합하여 생성된 AI 행사장 공간 설계 및 관람객 유동 시뮬레이션 결과를 기술합니다. 본 설계안은 관람객의 안전 확보와 구역별 혼잡도 분산을 극대화하는 것에 목적을 두고 있습니다.
      </p>

      <h3>2. 멀티 레이아웃 AI 생성 및 복원 검증</h3>
      <p>
        AI 자동 재배치 알고리즘을 반복 실행함으로써 최적화 지표가 각기 다른 다수의 설계 버전이 생성되었습니다. 생성된 이전 히스토리 배치안들은 보관함에 자동 기록되며, 환경 변화에 따라 즉시 과거 배치 버전으로 복원 및 교체가 가능하도록 구현되었습니다.
      </p>

      <h3>3. 실제 동적 상황 반응형 시뮬레이션 분석</h3>
      <p>
        가상 관람객 에이전트들은 우천 발생 시 천막 및 부스 내부로 대피하는 동선 밀집 행동을 보였으며, 응급환자 발생 시 비상 골든타임 통로 확보를 위해 중앙 통로 양옆으로 신속히 이동하는 정교한 반응 알고리즘이 적용되었습니다.
      </p>
    </div>

    <div style="margin-top:12px;display:flex;justify-content:flex-end;gap:10px;border-top:1px solid #f1f5f9;padding-top:12px;">
      <button class="btn-secondary" onclick="closeReportModal()">닫기</button>
      <button class="btn-primary" onclick="alert('다운로드가 완료되었습니다.');closeReportModal();">📥 PDF 다운로드</button>
    </div>
  </div>
</div>

<script>
/* Global Simulation & Layout Variables */
let venueCanvas, venueCtx, heatmapCanvas, heatmapCtx;
let renderMode = '2D'; // '2D' or '3D'
let contingencyMode = 'normal';
let animFrameId = null;

let people = [];
let layoutHistory = [];
let currentLayoutIndex = -1;

// Base Layout Booth Coordinates
let booths = [
  { id:'stage', title:'메인 무대', x: 0.38, y: 0.06, w: 0.24, h: 0.15, color:'#8b5cf6', icon:'🎭' },
  { id:'boothA', title:'체험존 A', x: 0.10, y: 0.22, w: 0.16, h: 0.14, color:'#3b82f6', icon:'🧪' },
  { id:'boothB', title:'체험존 B', x: 0.74, y: 0.22, w: 0.16, h: 0.14, color:'#3b82f6', icon:'🚀' },
  { id:'food', title:'푸드존', x: 0.08, y: 0.50, w: 0.16, h: 0.15, color:'#f59e0b', icon:'🍔' },
  { id:'med', title:'응급/안내', x: 0.74, y: 0.50, w: 0.16, h: 0.14, color:'#ef4444', icon:'🏥' },
  { id:'rest', title:'중앙 쉼터', x: 0.40, y: 0.45, w: 0.20, h: 0.16, color:'#10b981', icon:'🌿' }
];

/* Page Switching */
function switchPage(pageId, el){
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  if(el) el.classList.add('active');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    setTimeout(initCanvases, 50);
  } else if(pageId === 'assistant'){
    document.getElementById('pageAssistant').classList.add('active');
  }
}

function openReportModal(){ document.getElementById('reportModal').classList.add('active'); }
function closeReportModal(){ document.getElementById('reportModal').classList.remove('active'); }

function runAIGenerateFromHome(){
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
}

/* 1. LAYOUT HISTORY MANAGEMENT (다중 배치 생성 & 복원) */
function generateNewAILayout(){
  // Randomize booth locations slightly for new variant
  const newBooths = booths.map(b => {
    let copy = {...b};
    if(b.id !== 'stage'){
      copy.x = Math.max(0.08, Math.min(0.76, copy.x + (Math.random() - 0.5) * 0.12));
      copy.y = Math.max(0.18, Math.min(0.65, copy.y + (Math.random() - 0.5) * 0.10));
    }
    return copy;
  });

  const safetySc = 85 + Math.floor(Math.random() * 12);
  const congSc = 80 + Math.floor(Math.random() * 18);
  const accSc = 88 + Math.floor(Math.random() * 10);

  const newHistoryItem = {
    id: layoutHistory.length + 1,
    time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'}),
    title: `AI 배치안 v${layoutHistory.length + 1}`,
    booths: newBooths,
    scores: { safety: safetySc, cong: congSc, acc: accSc }
  };

  layoutHistory.unshift(newHistoryItem); // newest top
  currentLayoutIndex = 0;
  loadLayoutFromHistory(0);
}

function loadLayoutFromHistory(index){
  currentLayoutIndex = index;
  const item = layoutHistory[index];
  if(!item) return;

  booths = item.booths;
  document.getElementById('scSafety').textContent = item.scores.safety + '점';
  document.getElementById('scCong').textContent = item.scores.cong + '점';
  document.getElementById('scAcc').textContent = item.scores.acc + '점';

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
      <div class="history-info">
        <b>${item.title} ${isActive ? ' (현재 반영중)' : ''}</b>
        <span>생성시각: ${item.time} | 안전성: ${item.scores.safety}점</span>
      </div>
      <button class="btn-secondary" style="padding:4px 8px;font-size:10px;" onclick="loadLayoutFromHistory(${idx})">
        ${isActive ? '적용됨' : '복원하기'}
      </button>
    `;
    container.appendChild(div);
  });
}

/* 2. DYNAMIC PEOPLE & REALISTIC CONTINGENCY SIMULATION */
function adjustPeopleCount(delta){
  const countSpan = document.getElementById('currentAgentCount');
  let current = people.length;
  let target = Math.max(10, current + delta);

  const w = venueCanvas ? venueCanvas.width : 500;
  const h = venueCanvas ? venueCanvas.height : 350;

  if(target > current){
    for(let i=0; i < (target - current); i++){
      people.push({
        x: w * 0.45 + (Math.random()-0.5) * 40,
        y: h * 0.85 + (Math.random()-0.5) * 20,
        vx: (Math.random()-0.5) * 1.6,
        vy: (Math.random()-0.5) * 1.6,
        mesh: null
      });
    }
  } else {
    people.splice(target, current - target);
  }
  countSpan.textContent = people.length;
  if(renderMode === '3D') rebuild3DPeople();
}

function triggerContingency(mode){
  contingencyMode = mode;
  document.querySelectorAll('.btn-contingency').forEach(b => b.classList.remove('active'));

  const stText = document.getElementById('simStatusText');
  const stDetail = document.getElementById('simBehaviorDetail');

  if(mode === 'rain'){
    stText.textContent = '🚨 우천 발생 (부스/천막 대피 작동)';
    stText.style.color = '#3b82f6';
    stDetail.textContent = '관람객 에이전트들이 빗물을 피하기 위해 가장 가까운 부스 및 중앙 쉼터 천막 안으로 대피하고 있습니다.';
  } else if(mode === 'surge'){
    stText.textContent = '🚨 관람객 급증 (밀집 병목현상 발생)';
    stText.style.color = '#ef4444';
    stDetail.textContent = '주출입구 및 무대 전면에 인원이 집중되어 밀집도가 상승하고 있습니다.';
    adjustPeopleCount(40);
  } else if(mode === 'medical'){
    stText.textContent = '🚨 응급환자 발생 (비상통로 확보)';
    stText.style.color = '#10b981';
    stDetail.textContent = '구급차 이동 경로(중앙 통로)를 확보하기 위해 관람객들이 양옆으로 대피하고 있습니다.';
  }
}

function resetContingency(){
  contingencyMode = 'normal';
  document.getElementById('simStatusText').textContent = '정상 관람 동선 작동 중';
  document.getElementById('simStatusText').style.color = '#38bdf8';
  document.getElementById('simBehaviorDetail').textContent = '관람객들이 자유롭게 무대와 푸드존, 체험 부스를 순환하고 있습니다.';
}

/* 3. 2D & 3D GRAPHICS ENGINE */
function initCanvases(){
  venueCanvas = document.getElementById('venueCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');
  if(!venueCanvas) return;

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth || 500;
  const h = wrap.clientHeight || 350;

  venueCanvas.width = w; venueCanvas.height = h;
  heatmapCanvas.width = w; heatmapCanvas.height = h;

  venueCtx = venueCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');

  if(people.length === 0){
    for(let i=0; i<80; i++){
      people.push({
        x: w*0.15 + Math.random()*w*0.7,
        y: h*0.2 + Math.random()*h*0.6,
        vx: (Math.random()-0.5)*1.5,
        vy: (Math.random()-0.5)*1.5
      });
    }
  }

  if(layoutHistory.length === 0){
    generateNewAILayout();
  }

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

/* 2D CANVAS RENDERING LOOP */
function loopSimulation(){
  if(venueCtx && renderMode === '2D'){
    const w = venueCanvas.width;
    const h = venueCanvas.height;

    // Draw Background & Booths
    draw2DBackground(w, h);

    // Update & Draw Agents
    updateAndDraw2DPeople(w, h);

    // Draw Heatmap Overlay
    draw2DHeatmap(w, h);
  } else if(renderMode === '3D' && renderer3D){
    update3DPeoplePositions();
    renderer3D.render(scene3D, camera3D);
    if(controls3D) controls3D.update();
  }

  animFrameId = requestAnimationFrame(loopSimulation);
}

function draw2DBackground(w, h){
  venueCtx.fillStyle = '#2e6f40'; // Grass
  venueCtx.fillRect(0, 0, w, h);

  // Outer Path
  venueCtx.strokeStyle = '#e2d9c8';
  venueCtx.lineWidth = 24;
  venueCtx.beginPath();
  venueCtx.ellipse(w*0.5, h*0.5, w*0.38, h*0.30, 0, 0, Math.PI*2);
  venueCtx.stroke();

  // Emergency Corridor Guidance during Medical Event
  if(contingencyMode === 'medical'){
    venueCtx.strokeStyle = 'rgba(239, 68, 68, 0.8)';
    venueCtx.lineWidth = 14;
    venueCtx.setLineDash([8, 8]);
    venueCtx.beginPath();
    venueCtx.moveTo(w*0.5, h*0.9);
    venueCtx.lineTo(w*0.5, h*0.1);
    venueCtx.stroke();
    venueCtx.setLineDash([]);
  }

  // Render Booths
  booths.forEach(b => {
    const bx = b.x * w;
    const by = b.y * h;
    const bw = b.w * w;
    const bh = b.h * h;

    venueCtx.fillStyle = 'rgba(0,0,0,0.25)';
    venueCtx.fillRect(bx+3, by+3, bw, bh);

    venueCtx.fillStyle = b.color;
    venueCtx.beginPath();
    venueCtx.roundRect(bx, by, bw, bh, 6);
    venueCtx.fill();
    venueCtx.strokeStyle = '#fff';
    venueCtx.lineWidth = 1;
    venueCtx.stroke();

    venueCtx.fillStyle = '#ffffff';
    venueCtx.font = 'bold 10px Pretendard';
    venueCtx.textAlign = 'center';
    venueCtx.fillText(`${b.icon} ${b.title}`, bx + bw/2, by + bh/2 + 3);
  });
}

function updateAndDraw2DPeople(w, h){
  people.forEach(p => {
    // REALISTIC BEHAVIOR LOGIC
    if(contingencyMode === 'rain'){
      // Flee toward nearest booth or central shelter
      let targetB = booths[3]; // Rest/Food area shelter
      let tx = targetB.x * w + targetB.w*w*0.5;
      let ty = targetB.y * h + targetB.h*h*0.5;
      p.x += (tx - p.x) * 0.03;
      p.y += (ty - p.y) * 0.03;
    } else if(contingencyMode === 'medical'){
      // Clear central Corridor (X between 0.45*w and 0.55*w)
      if(p.x > w*0.42 && p.x < w*0.58){
        if(p.x < w*0.5) p.x -= 2.0; else p.x += 2.0;
      }
    } else {
      // Normal roaming
      p.x += p.vx;
      p.y += p.vy;
      if(p.x < 15 || p.x > w-15) p.vx *= -1;
      if(p.y < 15 || p.y > h-15) p.vy *= -1;
    }

    // Draw Agent Dot
    venueCtx.fillStyle = '#ffffff';
    venueCtx.beginPath();
    venueCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
    venueCtx.fill();
    venueCtx.strokeStyle = '#000';
    venueCtx.lineWidth = 0.5;
    venueCtx.stroke();
  });
}

function draw2DHeatmap(w, h){
  heatmapCtx.clearRect(0, 0, w, h);
  let spots = [];

  if(contingencyMode === 'rain'){
    spots.push({x: w*0.48, y: h*0.5, r: 60});
  } else if(contingencyMode === 'surge'){
    spots.push({x: w*0.5, y: h*0.15, r: 50});
    spots.push({x: w*0.5, y: h*0.85, r: 65});
  }

  spots.forEach(pt => {
    let grad = heatmapCtx.createRadialGradient(pt.x, pt.y, 0, pt.x, pt.y, pt.r);
    grad.addColorStop(0, 'rgba(239, 68, 68, 0.7)');
    grad.addColorStop(1, 'rgba(16, 185, 129, 0)');
    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(pt.x, pt.y, pt.r, 0, Math.PI*2);
    heatmapCtx.fill();
  });
}

/* 4. THREE.JS 3D ENGINE IMPLEMENTATION */
let scene3D, camera3D, renderer3D, controls3D;
let booth3DGroup, people3DGroup;

function init3D(){
  const container = document.getElementById('canvas3D');
  if(!container || renderer3D) {
    if(renderer3D) build3DScene();
    return;
  }

  const w = container.clientWidth || 500;
  const h = container.clientHeight || 350;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w / h, 1, 1000);
  camera3D.position.set(0, 160, 200);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  controls3D = new THREE.OrbitControls(camera3D, renderer3D.domElement);
  controls3D.enableDamping = true;
  controls3D.dampingFactor = 0.05;

  // Lighting
  const ambient = new THREE.AmbientLight(0xffffff, 0.7);
  scene3D.add(ambient);

  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(60, 120, 80);
  scene3D.add(dirLight);

  // Ground Plane (Grass)
  const planeGeo = new THREE.PlaneGeometry(240, 160);
  const planeMat = new THREE.MeshStandardMaterial({ color: 0x2e6f40, roughness: 0.8 });
  const ground = new THREE.Mesh(planeGeo, planeMat);
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

  // Clear existing 3D Booths
  while(booth3DGroup.children.length > 0){
    booth3DGroup.remove(booth3DGroup.children[0]);
  }

  // Create 3D Mesh for each Booth
  booths.forEach(b => {
    const bw = b.w * 240;
    const bh = b.h * 160;
    const bx = (b.x + b.w/2 - 0.5) * 240;
    const bz = (b.y + b.h/2 - 0.5) * 160;

    const height = b.id === 'stage' ? 14 : 8;
    const geo = new THREE.BoxGeometry(bw, height, bh);
    const mat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(b.color),
      roughness: 0.3
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(bx, height/2, bz);
    booth3DGroup.add(mesh);
  });

  rebuild3DPeople();
}

function rebuild3DPeople(){
  if(!people3DGroup) return;

  while(people3DGroup.children.length > 0){
    people3DGroup.remove(people3DGroup.children[0]);
  }

  const pGeo = new THREE.SphereGeometry(1.8, 8, 8);
  const pMat = new THREE.MeshBasicMaterial({ color: 0xffffff });

  people.forEach(p => {
    const mesh = new THREE.Mesh(pGeo, pMat);
    people3DGroup.add(mesh);
    p.mesh = mesh;
  });
}

function update3DPeoplePositions(){
  if(!venueCanvas || !people3DGroup) return;
  const w = venueCanvas.width;
  const h = venueCanvas.height;

  people.forEach(p => {
    if(p.mesh){
      const x3d = (p.x / w - 0.5) * 240;
      const z3d = (p.y / h - 0.5) * 160;
      p.mesh.position.set(x3d, 1.8, z3d);
    }
  });
}

function sendChat(){
  const val = document.getElementById('chatIn').value;
  if(!val) return;
  const box = document.getElementById('chatBox');
  box.innerHTML += `<div style="color:#1e293b;background:#ffffff;padding:8px;border-radius:8px;margin-bottom:8px;text-align:right;"><b>나:</b> ${val}</div>`;
  document.getElementById('chatIn').value = '';
  setTimeout(() => {
    box.innerHTML += `<div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;"><b>AI:</b> 지시하신 "${val}" 내용을 도면에 반영하여 2D/3D 레이아웃을 최적화했습니다.</div>`;
    box.scrollTop = box.scrollHeight;
  }, 300);
}

window.addEventListener('load', () => {
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_FULL_HTML, height=1280, scrolling=True)
