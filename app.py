import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Event AI - 디지털 트윈 기반 AI 행사장 설계 및 돌발상황 시뮬레이터",
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
<title>Event AI - AI 행사장 자동 설계 및 시뮬레이션 시스템</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
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

/* Scrollbar Style */
::-webkit-scrollbar {width:6px;height:6px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}
::-webkit-scrollbar-thumb:hover {background:#94a3b8;}

.app-container{
  display:flex;
  min-height:100vh;
  background:#f1f5f9;
}

/* Sidebar - Deep Navy Theme */
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
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  padding:0 6px;
  color:#fff;
}
.brand-icon{
  width:36px;
  height:36px;
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:10px;
  display:grid;
  place-items:center;
  font-size:18px;
  font-weight:900;
  box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.brand-title{font-size:17px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;}
.brand-sub{font-size:10px;color:#64748b;margin-top:1px;font-weight:500;}

.nav-group{display:flex;flex-direction:column;gap:4px;}
.nav-item{
  display:flex;
  align-items:center;
  gap:10px;
  padding:11px 14px;
  border-radius:10px;
  font-size:13px;
  font-weight:600;
  color:#94a3b8;
  cursor:pointer;
}
.nav-item:hover{background:rgba(255,255,255,0.05);color:#f1f5f9;}
.nav-item.active{
  background:linear-gradient(135deg, #2563eb, #3b82f6);
  color:#ffffff;
  box-shadow:0 4px 12px rgba(37,99,235,0.3);
}

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
  background:#3b82f6;
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

.side-banner{
  background:linear-gradient(135deg, rgba(37,99,235,0.2), rgba(15,23,42,0.8));
  border:1px solid rgba(59,130,246,0.25);
  padding:12px;
  border-radius:12px;
  color:#e2e8f0;
}
.side-banner h5{font-size:11.5px;font-weight:800;color:#60a5fa;margin-bottom:4px;}
.side-banner p{font-size:10px;color:#94a3b8;line-height:1.4;}

/* Main Container */
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
.top-title h2{font-size:19px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:8px;}
.top-title p{font-size:12px;color:#64748b;margin-top:2px;}

/* Page Views */
.page-view{display:none;}
.page-view.active{display:block;}

/* Form Sections */
.form-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:22px;
  box-shadow:0 2px 10px rgba(0,0,0,0.02);
  margin-bottom:16px;
}
.form-section-head{
  font-size:15px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:16px;
  display:flex;
  align-items:center;
  gap:8px;
  border-bottom:2px solid #f1f5f9;
  padding-bottom:10px;
}
.form-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));
  gap:14px;
}
.form-group{
  display:flex;
  flex-direction:column;
  gap:5px;
}
.form-group label{
  font-size:11.5px;
  font-weight:700;
  color:#334155;
  display:flex;
  align-items:center;
  gap:4px;
}
.form-group input, .form-group select, .form-group textarea{
  padding:9px 11px;
  border:1.5px solid #cbd5e1;
  border-radius:8px;
  background:#f8fafc;
  color:#0f172a;
  font-size:12.5px;
  font-weight:600;
  outline:none;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus{
  border-color:#2563eb;
  background:#ffffff;
  box-shadow:0 0 0 3px rgba(37,99,235,0.1);
}

.btn-primary{
  background:linear-gradient(135deg, #2563eb, #1d4ed8);
  color:#ffffff;
  border:none;
  padding:10px 20px;
  border-radius:10px;
  font-weight:800;
  font-size:13px;
  box-shadow:0 4px 14px rgba(37,99,235,0.3);
  display:inline-flex;
  align-items:center;
  gap:6px;
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(37,99,235,0.4);}

.btn-secondary{
  background:#ffffff;
  border:1.5px solid #cbd5e1;
  color:#334155;
  padding:8px 14px;
  border-radius:8px;
  font-weight:700;
  font-size:12px;
}
.btn-secondary:hover{background:#f8fafc;border-color:#94a3b8;}

/* Dashboard Info Strip */
.info-strip{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:12px 18px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  flex-wrap:wrap;
  gap:10px;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
}
.info-strip-group{
  display:flex;
  align-items:center;
  gap:14px;
  flex-wrap:wrap;
}
.info-box{
  display:flex;
  align-items:center;
  gap:8px;
  padding-right:10px;
  border-right:1px solid #f1f5f9;
}
.info-box:last-child{border-right:none;}
.info-box-icon{
  width:30px;
  height:30px;
  border-radius:8px;
  background:#eff6ff;
  color:#2563eb;
  display:grid;
  place-items:center;
  font-size:13px;
}
.info-box-text label{display:block;font-size:9.5px;color:#64748b;font-weight:700;}
.info-box-text span{font-size:12px;font-weight:800;color:#0f172a;}

/* Main Dashboard Grids */
.dashboard-main-grid{
  display:grid;
  grid-template-columns: 1.4fr 1fr 0.9fr;
  gap:16px;
}
.dashboard-bottom-grid{
  display:grid;
  grid-template-columns: 1fr 1.2fr 0.9fr;
  gap:16px;
}

/* Card Panels */
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
  font-size:13.5px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:12px;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.card-badge{
  font-size:10px;
  background:#eff6ff;
  color:#2563eb;
  padding:3px 8px;
  border-radius:12px;
  font-weight:700;
}

/* Canvas Wrap */
.map-wrap{
  position:relative;
  width:100%;
  height:350px;
  background:#1e293b;
  border-radius:12px;
  overflow:hidden;
  border:1px solid #334155;
}
#venueCanvas, #heatmapCanvas{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
}

/* Legend Overlay */
.map-legend-overlay{
  position:absolute;
  left:10px;
  bottom:10px;
  z-index:20;
  background:rgba(255,255,255,0.92);
  backdrop-filter:blur(6px);
  padding:8px 10px;
  border-radius:10px;
  font-size:10px;
  border:1px solid #e2e8f0;
  box-shadow:0 4px 12px rgba(0,0,0,0.1);
  display:grid;
  grid-template-columns:repeat(2, 1fr);
  gap:4px 8px;
}
.legend-item{display:flex;align-items:center;gap:4px;font-weight:700;color:#334155;}
.legend-dot{width:8px;height:8px;border-radius:2px;}

/* Emergency Controls Bar */
.emergency-bar{
  background:#fff1f2;
  border:1px solid #fecdd3;
  padding:10px 14px;
  border-radius:12px;
  margin-top:10px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:8px;
  flex-wrap:wrap;
}
.emergency-title{font-size:11px;font-weight:800;color:#be123c;display:flex;align-items:center;gap:4px;}
.emergency-btn-group{display:flex;gap:6px;}
.btn-contingency{
  background:#ffffff;
  border:1px solid #fda4af;
  color:#9f1239;
  padding:5px 10px;
  border-radius:6px;
  font-size:10.5px;
  font-weight:700;
}
.btn-contingency:hover,.btn-contingency.active{
  background:#f43f5e;
  color:#ffffff;
  border-color:#f43f5e;
}

/* Score Table */
.score-tbl{width:100%;border-collapse:collapse;font-size:11.5px;margin-bottom:10px;}
.score-tbl th,.score-tbl td{padding:7px 4px;text-align:left;border-bottom:1px solid #f1f5f9;}
.score-tbl th{color:#64748b;font-weight:700;font-size:10.5px;}
.grade-badge{
  padding:2px 7px;
  border-radius:8px;
  font-weight:800;
  font-size:10px;
  display:inline-block;
}
.gb-excel{background:#dcfce7;color:#15803d;}
.gb-good{background:#e0f2fe;color:#0369a1;}

/* AI Recommendations List */
.ai-recom-list{
  list-style:none;
  display:flex;
  flex-direction:column;
  gap:6px;
  font-size:11px;
  color:#334155;
}
.ai-recom-list li{
  display:flex;
  align-items:flex-start;
  gap:5px;
  line-height:1.4;
  background:#f8fafc;
  padding:7px 9px;
  border-radius:8px;
  border:1px solid #f1f5f9;
}
.ai-recom-list li::before{content:"✔";color:#10b981;font-weight:900;}

/* Compare Grid */
.compare-grid{
  display:grid;
  grid-template-columns:1fr 20px 1fr;
  align-items:center;
  gap:8px;
  background:#f8fafc;
  padding:10px;
  border-radius:12px;
  border:1px solid #e2e8f0;
}
.comp-col h5{font-size:10.5px;color:#64748b;margin-bottom:6px;font-weight:700;}
.comp-val{display:flex;justify-content:space-between;font-size:11px;font-weight:700;margin-bottom:4px;}
.text-red{color:#ef4444;}
.text-green{color:#10b981;}

/* Workflow Steps */
.wf-container{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:4px;
  margin-top:4px;
}
.wf-card{
  flex:1;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 4px;
  border-radius:8px;
  text-align:center;
}
.wf-card .wf-icon{font-size:13px;margin-bottom:2px;}
.wf-card .wf-title{font-size:9.5px;font-weight:800;color:#1e293b;}
.wf-arrow{color:#cbd5e1;font-weight:900;font-size:10px;}

.wf-sub-tags{
  display:flex;
  justify-content:space-between;
  gap:4px;
  margin-top:8px;
}
.wf-tag{
  flex:1;
  background:#eff6ff;
  color:#2563eb;
  font-size:9px;
  font-weight:700;
  text-align:center;
  padding:4px 2px;
  border-radius:6px;
}

/* Modal for Comprehensive Prose Report */
.modal-bg{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,0.7);
  backdrop-filter:blur(6px);
  z-index:999;
  display:none;
  place-items:center;
  padding:20px;
}
.modal-bg.active{display:grid;}
.modal-content{
  background:#ffffff;
  width:min(95%, 920px);
  max-height:88vh;
  border-radius:20px;
  padding:28px;
  box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.modal-body{
  flex:1;
  overflow-y:auto;
  padding-right:10px;
  display:flex;
  flex-direction:column;
  gap:20px;
  color:#334155;
  font-size:13px;
  line-height:1.75;
}

/* Prose Report Style Inside Modal */
.prose-report h3{font-size:18px;color:#0f172a;border-bottom:2px solid #2563eb;padding-bottom:6px;margin-top:10px;margin-bottom:10px;}
.prose-report h4{font-size:15px;color:#1e293b;margin-top:14px;margin-bottom:6px;font-weight:800;}
.prose-report p{margin-bottom:12px;text-align:justify;word-break:keep-all;}
.prose-highlight{background:#f1f5f9;padding:12px 16px;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;margin:12px 0;font-weight:500;}
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
        <div class="brand-sub">디지털 트윈 & AI 행사 최적화</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item" onclick="switchPage('home', this)">
        <span>🏠</span> 행사 정보 및 목표 설정
      </div>
      <div class="nav-item active" onclick="switchPage('design', this)">
        <span>📋</span> AI 행사장 설계 & 디지털 트윈
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span>⚙️</span> 유전 알고리즘 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span>📄</span> 종합 분석 리포트 (줄글)
      </div>
      <div class="nav-item" onclick="switchPage('assistant', this)">
        <span>🤖</span> AI 어시스턴트 수정
      </div>
    </nav>

    <div class="side-banner">
      <h5>AI Re-Optimization Engine</h5>
      <p>돌발상황 발생 시 AI 유전 알고리즘이 0.3초 내 실시간 재배치를 도출합니다.</p>
    </div>

    <div class="side-profile">
      <div class="side-avatar">추</div>
      <div class="side-user-info">
        <div class="side-user-name">추천님 (총괄 총괄기획)</div>
        <button class="side-user-btn">로그아웃</button>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">

    <!-- Top Header -->
    <header class="top-header">
      <div class="top-title">
        <h2 id="topTitleText">📋 AI 행사장 설계 및 디지털 트윈 시뮬레이션</h2>
        <p id="topSubText">입력된 조건과 AI 목표 우선순위에 따라 유전 알고리즘 최적화를 수행합니다.</p>
      </div>
      <button class="btn-primary" onclick="runAIGenerate()">
        ✦ AI 재배치 & 시뮬레이션 실행
      </button>
    </header>

    <!-- PAGE 1: HOME FORM (ALL IMAGE REQUIREMENTS) -->
    <section id="pageHome" class="page-view">
      
      <!-- 1. 행사 기본 정보 & 설계 조건 생성 -->
      <div class="form-card">
        <div class="form-section-head">📌 1. 행사 기본 정보 및 AI 설계 조건 생성</div>
        <div class="form-grid">
          <div class="form-group">
            <label>행사명</label>
            <input type="text" id="inEventName" value="2025 힐링 페스티벌">
          </div>
          <div class="form-group">
            <label>행사장 유형</label>
            <select id="inVenueType">
              <option value="야외 잔디 광장" selected>야외 잔디 광장</option>
              <option value="실내 컨벤션 홀">실내 컨벤션 홀</option>
              <option value="실내 체육관">실내 체육관</option>
              <option value="도심 스트리트/광장">도심 스트리트 / 광장</option>
            </select>
          </div>
          <div class="form-group">
            <label>행사장 위치</label>
            <input type="text" id="inLocation" value="야외 종합 운동장 & 잔디 광장">
          </div>
          <div class="form-group">
            <label>예상 방문객 수</label>
            <select id="inVisitors">
              <option value="1,000명">1,000명</option>
              <option value="3,000명">3,000명</option>
              <option value="5,000명" selected>5,000명</option>
              <option value="10,000명 이상">10,000명 이상</option>
            </select>
          </div>
          <div class="form-group">
            <label>행사장 면적</label>
            <input type="text" id="inArea" value="50,000m²">
          </div>
          <div class="form-group">
            <label>행사 시간</label>
            <input type="text" id="inTime" value="10:00 - 20:00">
          </div>
          <div class="form-group">
            <label>입장료 / 예산</label>
            <input type="text" id="inBudget" value="무료 / 예산 5,000만원">
          </div>
        </div>
      </div>

      <!-- 2. 행사 목적 기반 AI 최적화 설정 -->
      <div class="form-card">
        <div class="form-section-head">🎯 2. 행사 목적 기반 AI 최적화 가중치 설정 (이미지 반영)</div>
        <div class="form-grid">
          <div class="form-group">
            <label>최우선 목표 선택</label>
            <select id="inGoal" onchange="updateGoalDescription()">
              <option value="안전 중심" selected>🛡️ 안전 중심 (병목 최소화, 비상 동선 최우선)</option>
              <option value="참여 중심">🎪 참여성 중심 (체험/부스 순환 및 체류시간 최대화)</option>
              <option value="운영 효율 중심">⚡ 운영 효율 중심 (설비 가동률 및 인력 동선 최소화)</option>
              <option value="예산 중심">💰 예산 효율 중심 (설치비 및 자원 배치 최적화)</option>
            </select>
          </div>
          <div class="form-group" style="grid-column: span 2;">
            <label>목적별 AI 알고리즘 적용 지침</label>
            <input type="text" id="goalDesc" value="안전 중심: 관람객 간 격리 통로 확보, 메인 출입구 인근 응급부스 전진 배치, 피크 타임 혼잡도 제어." readonly style="background:#f1f5f9;color:#64748b;">
          </div>
        </div>
      </div>

      <!-- 3. 시설 및 부스 구성 자동 배치 제약조건 -->
      <div class="form-card">
        <div class="form-section-head">🎪 3. 부스 종류 및 개수 설정 (자동 배치 제약조건)</div>
        <div class="form-grid">
          <div class="form-group">
            <label>메인 공연장 / 무대</label>
            <input type="number" id="cntStage" value="1">
          </div>
          <div class="form-group">
            <label>체험 & 플리마켓 부스</label>
            <input type="number" id="cntExbooth" value="14">
          </div>
          <div class="form-group">
            <label>푸드존 / 푸드트럭</label>
            <input type="number" id="cntFood" value="8">
          </div>
          <div class="form-group">
            <label>휴게공간 / 쉼터</label>
            <input type="number" id="cntRest" value="4">
          </div>
          <div class="form-group">
            <label>화장실 & 편의시설</label>
            <input type="number" id="cntToilet" value="3">
          </div>
          <div class="form-group">
            <label>안내소 & 응급 의료부스</label>
            <input type="number" id="cntMed" value="2">
          </div>
        </div>
      </div>

      <!-- 4. 이용자 맞춤형 접근성 분석 설정 -->
      <div class="form-card">
        <div class="form-section-head">♿ 4. AI 기반 이용자 맞춤형 접근성 옵션 (이미지 반영)</div>
        <div style="display:flex;gap:20px;flex-wrap:wrap;">
          <label style="font-size:12.5px;font-weight:700;display:flex;align-items:center;gap:6px;">
            <input type="checkbox" id="chkWheelchair" checked> 휠체어 / 유모차 무장애(Barrier-Free) 전용 동선 확보
          </label>
          <label style="font-size:12.5px;font-weight:700;display:flex;align-items:center;gap:6px;">
            <input type="checkbox" id="chkSenior" checked> 어린이 / 노약자 전용 안심 쉼터 zone 배치
          </label>
          <label style="font-size:12.5px;font-weight:700;display:flex;align-items:center;gap:6px;">
            <input type="checkbox" id="chkForeigner" checked> 외국인 방문객 다국어 안내 및 이정표 스팟 자동 설계
          </label>
        </div>
        <div style="margin-top:16px;text-align:right;">
          <button class="btn-primary" onclick="runAIGenerate()">
            ✦ 조건 입력 완료 및 AI 최적화 알고리즘 구동
          </button>
        </div>
      </div>

    </section>

    <!-- PAGE 2: DESIGN DASHBOARD (ACTIVE CANVAS + CONTINGENCY) -->
    <section id="pageDesign" class="page-view active">

      <!-- Top Header Strip "행사 기본 정보" -->
      <div class="info-strip">
        <div class="info-strip-group">
          <div class="info-box">
            <div class="info-box-icon">📌</div>
            <div class="info-box-text"><label>행사명</label><span id="outEventName">2025 힐링 페스티벌</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🎯</div>
            <div class="info-box-text"><label>최적화 목표</label><span id="outGoal" style="color:#2563eb;">안전 중심</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">📍</div>
            <div class="info-box-text"><label>위치/유형</label><span id="outVenueType">야외 잔디 광장</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">👥</div>
            <div class="info-box-text"><label>예상 방문객</label><span id="outVisitors">5,000명</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">♿</div>
            <div class="info-box-text"><label>접근성 설계</label><span id="outAccess">무장애 동선 적용</span></div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-main-grid" style="margin-top:14px;">

        <!-- 1. Digital Twin Canvas Map -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 디지털 트윈 기반 행사장 3D/2D 레이아웃</span>
            <span class="card-badge" id="simModeBadge">실시간 동선 시뮬레이션 ON</span>
          </div>
          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="heatmapCanvas"></canvas>

            <!-- Overlay Legend -->
            <div class="map-legend-overlay">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 무대존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험/플리마켓</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 푸드존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 휴식공간</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 응급/안내</div>
              <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> 화장실</div>
              <div class="legend-item" style="grid-column:span 2;"><span class="legend-dot" style="background:#ffffff;border:1px solid #000;"></span> ⚪ 실시간 관람객 에이전트</div>
            </div>
          </div>

          <!-- Real-Time Contingency Trigger Controls (Image Feature) -->
          <div class="emergency-bar">
            <div class="emergency-title">
              ⚡ 디지털 트윈 돌발상황 시뮬레이션 & Re-Optimization
            </div>
            <div class="emergency-btn-group">
              <button class="btn-contingency" onclick="triggerContingency('rain')">🌧️ 우천 발생</button>
              <button class="btn-contingency" onclick="triggerContingency('surge')">🚨 관람객 급증 (200%)</button>
              <button class="btn-contingency" onclick="triggerContingency('delay')">🎭 공연 지연</button>
              <button class="btn-contingency" onclick="triggerContingency('medical')">🏥 응급환자 발생</button>
              <button class="btn-contingency" style="background:#e2e8f0;color:#334155;border-color:#cbd5e1;" onclick="resetContingency()">🔄 원상복구</button>
            </div>
          </div>
        </div>

        <!-- 2. Congestion Heatmap & Realtime Metrics -->
        <div class="card-panel">
          <div class="card-head">
            <span>🔥 시간대별 혼잡도 Heatmap</span>
            <span class="card-badge">AI 실시간 감지</span>
          </div>
          <div style="background:#0f172a;border-radius:12px;padding:12px;color:#fff;margin-bottom:10px;">
            <div style="font-size:11px;color:#94a3b8;font-weight:700;">현재 최대 병목구역 밀집도</div>
            <div style="font-size:22px;font-weight:900;color:#f43f5e;" id="densityVal">1.2 명/m² (안전)</div>
            <div style="font-size:10px;color:#cbd5e1;margin-top:2px;" id="contingencyStatus">상태: 정상 시뮬레이션 가동 중</div>
          </div>
          <div style="font-size:11.5px;font-weight:800;color:#0f172a;margin-bottom:6px;">📍 구역별 예상 대기시간</div>
          <div style="display:flex;flex-direction:column;gap:6px;font-size:11px;">
            <div style="display:flex;justify-size:space-between;justify-content:space-between;"><span>메인 무대 앞:</span><b id="waitStage" style="color:#2563eb;">3분</b></div>
            <div style="display:flex;justify-content:space-between;"><span>푸드트럭 존:</span><b id="waitFood" style="color:#2563eb;">7분</b></div>
            <div style="display:flex;justify-content:space-between;"><span>주 화장실:</span><b id="waitToilet" style="color:#2563eb;">2분</b></div>
            <div style="display:flex;justify-content:space-between;"><span>응급/비상 통로:</span><b id="waitEmg" style="color:#10b981;">0분 (원활)</b></div>
          </div>
        </div>

        <!-- 3. AI Evaluation Scores -->
        <div class="card-panel">
          <div class="card-head">
            <span>💡 AI 설계 결과 분석 평가</span>
          </div>
          <table class="score-tbl">
            <thead>
              <tr><th>평가 지표</th><th>점수</th><th>등급</th></tr>
            </thead>
            <tbody>
              <tr><td>비상 안전성 (Safety)</td><td id="scSafety">96점</td><td><span class="grade-badge gb-excel">매우 우수</span></td></tr>
              <tr><td>혼잡도 분산 (Congestion)</td><td id="scCong">88점</td><td><span class="grade-badge gb-good">우수</span></td></tr>
              <tr><td>맞춤 접근성 (Access)</td><td id="scAcc">95점</td><td><span class="grade-badge gb-excel">매우 우수</span></td></tr>
              <tr><td>참여/순환성 (Flow)</td><td id="scFlow">91점</td><td><span class="grade-badge gb-excel">매우 우수</span></td></tr>
              <tr><td>운영/예산 (Efficiency)</td><td id="scEff">89점</td><td><span class="grade-badge gb-good">우수</span></td></tr>
            </tbody>
          </table>

          <div style="font-size:11.5px;font-weight:800;color:#0f172a;margin:8px 0 4px 0;">💡 AI 설계 이유 및 개선 효과</div>
          <ul class="ai-recom-list" id="recomList">
            <li>선택하신 '안전 중심' 목표에 따라 비상 출입구와 응급센터 간 직결 통로 확보</li>
            <li>휠체어 및 유모차 이용자를 위해 경사도 3% 이하의 무장애 순환 경로 배치</li>
            <li>푸드존과 무대 사이 15m 완충지대를 두어 병목현상 사전 차단</li>
          </ul>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-bottom-grid" style="margin-top:14px;">

        <!-- 1. Before / After Comparison -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚖️ 변경 전 / 후 정량적 비교</span>
          </div>
          <div class="compare-grid">
            <div class="comp-col">
              <h5>AI 설계 전 (기존 수동)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-red">68%</span></div>
              <div class="comp-val"><span>비상 대피시간</span><span class="text-red">6분 30초</span></div>
              <div class="comp-val"><span>약자 접근성</span><span>62점</span></div>
              <div class="comp-val"><span>사고 위험구역</span><span class="text-red">4개소</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#cbd5e1;">→</div>
            <div class="comp-col">
              <h5>AI 설계 후 (최적화)</h5>
              <div class="comp-val"><span>병목 발생율</span><span class="text-green">12%</span></div>
              <div class="comp-val"><span>비상 대피시간</span><span class="text-green">2분 10초</span></div>
              <div class="comp-val"><span>약자 접근성</span><span class="text-green">95점</span></div>
              <div class="comp-val"><span>사고 위험구역</span><span class="text-green">0개소</span></div>
            </div>
          </div>
        </div>

        <!-- 2. AI Workflow Process -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚙️ AI 행사 설계 & 시뮬레이션 Workflow</span>
          </div>
          <div class="wf-container">
            <div class="wf-card"><div class="wf-icon">📋</div><div class="wf-title">조건/목표 입력</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🧬</div><div class="wf-title">유전 알고리즘</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🌐</div><div class="wf-title">디지털 트윈</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">⚡</div><div class="wf-title">Re-optimization</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">📄</div><div class="wf-title">종합 리포트</div></div>
          </div>
          <div class="wf-sub-tags">
            <span class="wf-tag">입력데이터 분석</span>
            <span class="wf-tag">수천가지 배치 생성</span>
            <span class="wf-tag">시간대 동선 추적</span>
            <span class="wf-tag">돌발변수 수시반영</span>
          </div>
        </div>

        <!-- 3. Report Output Trigger -->
        <div class="card-panel">
          <div class="card-head">
            <span>📄 최종 결과물 및 줄글 리포트</span>
          </div>
          <p style="font-size:11px;color:#64748b;line-height:1.5;margin-bottom:12px;">
            3D 공간 배치 좌표 데이터, 혼잡도 Heatmap, 접근성 검증 결과가 모두 포함된 긴 줄글 형태의 공식 분석 보고서를 열람합니다.
          </p>
          <button class="btn-primary" style="width:100%;justify-content:center;padding:11px;font-size:12.5px;margin-top:auto;" onclick="openReportModal()">
            📌 줄글 형태의 종합 리포트 생성 및 열람
          </button>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS EXPLANATION -->
    <section id="pageProcess" class="page-view">
      <div class="form-card">
        <div class="form-section-head">⚙️ 유전 알고리즘(Genetic Algorithm) 및 디지털 트윈 알고리즘 메커니즘</div>
        <p style="font-size:12.5px;line-height:1.8;color:#334155;">
          <b>1. 제약조건 및 염색체 인코딩 (Chromosome Encoding):</b><br>
          입력된 부스 종류, 개수, 행사 면적, 출입구 위치를 기반으로 유전자의 위치 좌표(X, Y, Orientation)를 벡터로 변환합니다.<br><br>
          <b>2. 적합도 함수 (Fitness Function) 계산:</b><br>
          설정된 목표(안전/참여/운영/예산)에 맞춰 $Fitness = w_1 \cdot Safety + w_2 \cdot Accessibility - w_3 \cdot Congestion$ 수식을 적용, 수천 개의 가상 레이아웃을 탐색합니다.<br><br>
          <b>3. Re-optimization (실시간 재배치):</b><br>
          우천, 관람객 급증, 공연 지연 등 돌발상황 발생 시 디지털 트윈 센서 파라미터가 변경되며, 변형된 유전 알고리즘이 0.3초 이내에 보조 동선 및 안전 구역을 재배치합니다.
        </p>
      </div>
    </section>

    <!-- PAGE 4: MYPAGE / ASSISTANT -->
    <section id="pageAssistant" class="page-view">
      <div class="form-card">
        <div class="form-section-head">🤖 AI 대화형 배치 어시스턴트</div>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:12px;border-radius:10px;height:220px;overflow-y:auto;font-size:12px;margin-bottom:12px;" id="chatBox">
          <div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;">
            AI: 안녕하세요! "응급의료부스를 주출입구에 더 가깝게 옮겨줘" 또는 "휠체어 통로 폭을 넓혀줘" 와 같은 명령어를 입력하시면 디지털 트윈 캔버스에 바로 반영합니다.
          </div>
        </div>
        <div style="display:flex;gap:8px;">
          <input type="text" id="chatIn" placeholder="자연어로 지시사항을 입력하세요..." style="flex:1;padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;">
          <button class="btn-primary" onclick="sendChat()">전송</button>
        </div>
      </div>
    </section>

  </main>
</div>

<!-- DETAILED LONG PROSE REPORT MODAL (줄글 방식 보고서) -->
<div class="modal-bg" id="reportModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #f1f5f9;margin-bottom:12px;">
      <h3 style="font-size:18px;font-weight:800;color:#0f172a;">📊 AI 행사장 자동 설계 및 디지털 트윈 검증 종합 리포트</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:22px;font-weight:800;color:#64748b;cursor:pointer;">✕</button>
    </div>

    <div class="modal-body prose-report">
      
      <h3>1. 서론 및 행사 개요</h3>
      <p>
        본 보고서는 최신 디지털 트윈(Digital Twin) 기술과 유전 알고리즘(Genetic Algorithm) 기반의 공간 최적화 AI 모델을 활용하여 수립된 <b>'[신규] 2025 힐링 페스티벌'</b>의 행사장 자동 설계 및 동선 검증 결과를 서술합니다. 본 행사는 50,000m² 규모의 야외 잔디 광장에서 약 5,000명 이상의 관람객을 수용하는 대규모 야외 문화 행사로 기획되었습니다. 운영 주최측이 설정한 최우선 목적 지표인 <b>'안전 중심(Safety-First)'</b>에 맞추어, 관람객 이동 동선의 병목현상 방지, 비상시 골든타임 확보, 그리고 모든 이용자(휠체어, 유모차, 노약자, 외국인 포함)를 위한 무장애 접근성을 완벽히 구현하는 것에 중점을 두었습니다.
      </p>

      <h3>2. AI 공간 배치 전략 및 시설물 제약조건 분석</h3>
      <p>
        AI 자동 설계 엔진은 공간 내 주요 설비 간의 상호작용 및 관람객 유동 패턴을 수식화하여 최적의 위치 좌표를 도출하였습니다. 
        메인 공연장(무대)은 잔디 광장 상단 중앙에 배치하여 시야각과 음향 전달 범위를 극대화하였으며, 무대 전면에는 피크 타임 시 밀집도를 완화할 수 있는 15m 규격의 완충 구역(Buffer Zone)을 조성하였습니다. 
        체험 부스 및 플리마켓(14개소)과 푸드트럭(8개소)은 중앙 잔디 휴게공간(Central Lawn)을 원형으로 둘러싸는 루프(Loop)형 동선으로 배치되었습니다. 이러한 원형 배치는 특정 구역에 인원이 쏠리는 현상을 방지하고 관람객이 자연스럽게 전체 행사장을 순환하도록 유도합니다.
      </p>

      <div class="prose-highlight">
        <b>주요 시설 배치 좌표 요약:</b><br>
        • 메인 무대: 중앙 상단 (상대좌표 X: 0.50, Y: 0.12) / 전면 완충 공간 15m 확보<br>
        • 응급 의료센터 & 종합 안내소: 주 출입구 바로 우측 (X: 0.72, Y: 0.85) 전진 배치로 비상 진출입로 연결<br>
        • 휠체어/유모차 전용 램프 동선: 경사도 3% 이하, 최소 폭 2.5m 완충 통로 전체 구간 적용
      </div>

      <h3>3. AI 기반 이용자 맞춤형 접근성 분석 (Accessibility Evaluation)</h3>
      <p>
        본 시스템은 어린이, 노약자, 휠체어 이용자, 유모차 동반 가족, 외국인 등 다양한 관람객의 이동 특성을 고려한 접근성 분석 알고리즘을 구동하였습니다. 휠체어 및 유모차 이용자의 이동 편의성을 위해 행사장 전체 주 동선의 단차를 제거하고 경사도 3% 이하의 무장애(Barrier-Free) 특화 통로를 설계에 반영하였습니다. 또한 노약자와 어린이를 위한 안심 쉼터를 잔디 광장 중앙과 외곽 4개 지점에 분산 배치하였으며, 외국인 방문객을 위해 주요 동선 교차로마다 다국어 스마트 안내 스팟을 자동 배치함으로써 누구나 안전하고 편리하게 행사에 참여할 수 있도록 구현하였습니다.
      </p>

      <h3>4. 디지털 트윈 시뮬레이션 및 돌발상황(Contingency) 대응 검증</h3>
      <p>
        디지털 트윈 환경에서 5,000명의 가상 관람객(Agent)을 대상으로 시간대별 이동 패턴 및 대기시간을 시뮬레이션한 결과, 평균 이동 효율성은 기존 수동 설계 대비 <b>34% 향상</b>되었습니다. 
        특히 우천, 관람객 200% 급증, 공연 지연, 응급환자 발생 등 4가지 대표 돌발상황을 가정한 시뮬레이션 테스트에서 AI의 <b>Re-optimization(실시간 재배치)</b> 기능이 성공적으로 작동하였습니다. 응급환자 발생 신호 수신 즉시 비상 골든타임 통로가 0.3초 만에 확보되었으며, 관람객 급증 시에도 보조 출입구가 가동되어 최대 병목 밀집도가 1.2명/m² 이하로 안전하게 유지됨을 확인하였습니다.
      </p>

      <h3>5. 정량적 전·후 성과 비교 및 최종 제언</h3>
      <p>
        기존의 수동 배치 방식과 AI 최적화 설계안을 정량적으로 비교한 결과, 병목 발생 위험률은 <b>68%에서 12%로 대폭 감소</b>하였으며, 비상 상황 발생 시 전체 관람객의 대피 완료 시간은 <b>6분 30초에서 2분 10초로 약 67% 단축</b>되었습니다. 
        결론적으로 본 AI 자동 설계안은 안전성(96점), 접근성(95점), 순환성(91점) 등 전 지표에서 '매우 우수' 등급을 달성하였으므로, 본 행사의 최종 공간 배치안으로 확정할 것을 강력히 권장합니다.
      </p>

    </div>

    <div style="margin-top:14px;display:flex;justify-content:flex-end;gap:10px;border-top:1px solid #f1f5f9;padding-top:12px;">
      <button class="btn-secondary" onclick="closeReportModal()">닫기</button>
      <button class="btn-primary" onclick="alert('보고서 및 3D 좌표 데이터가 PDF로 다운로드 되었습니다.');closeReportModal();">
        📥 PDF 및 3D 좌표 데이터 다운로드
      </button>
    </div>
  </div>
</div>

<script>
/* Global Simulation Variables */
let venueCanvas, venueCtx, heatmapCanvas, heatmapCtx;
let simRunning = true;
let animFrameId = null;
let people = [];
let contingencyMode = 'normal'; // 'normal', 'rain', 'surge', 'delay', 'medical'

function switchPage(pageId, el){
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  if(el) el.classList.add('active');

  const t = document.getElementById('topTitleText');
  const s = document.getElementById('topSubText');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
    t.textContent = '📝 행사 정보 및 AI 목표 설정';
    s.textContent = '기본 정보와 최적화 목적을 선택하면 AI가 제약조건을 생성합니다.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    t.textContent = '📋 AI 행사장 설계 & 디지털 트윈';
    s.textContent = '실시간 동선 시뮬레이션 및 돌발상황 대응 테스트를 수행합니다.';
    setTimeout(initCanvases, 50);
  } else if(pageId === 'process'){
    document.getElementById('pageProcess').classList.add('active');
    t.textContent = '⚙️ 유전 알고리즘 프로세스';
    s.textContent = '수천 가지 배치 시나리오 자동 생성 및 최적화 메커니즘입니다.';
  } else if(pageId === 'assistant'){
    document.getElementById('pageAssistant').classList.add('active');
    t.textContent = '🤖 AI 대화형 어시스턴트';
    s.textContent = '자연어 명령으로 배치 및 동선을 실시간 수정합니다.';
  }
}

function updateGoalDescription(){
  const g = document.getElementById('inGoal').value;
  const desc = document.getElementById('goalDesc');
  if(g === '안전 중심'){
    desc.value = '안전 중심: 관람객 간 격리 통로 확보, 메인 출입구 인근 응급부스 전진 배치, 피크 타임 혼잡도 제어.';
  } else if(g === '참여 중심'){
    desc.value = '참여 중심: 체험부스 순환동선 배치, 관람객 체류 시간 및 부스 접근율 최대화.';
  } else if(g === '운영 효율 중심'){
    desc.value = '운영 효율 중심: 안내소 및 스태프 이동선 최소화, 화장실/편의시설 균등 분산.';
  } else if(g === '예산 중심'){
    desc.value = '예산 중심: 무대 및 대형 전력 시설물 집중 배치로 인프라 음영 최소화 및 설치비 절감.';
  }
}

function openReportModal(){ document.getElementById('reportModal').classList.add('active'); }
function closeReportModal(){ document.getElementById('reportModal').classList.remove('active'); }

function runAIGenerate(){
  const name = document.getElementById('inEventName').value;
  const vtype = document.getElementById('inVenueType').value;
  const vis = document.getElementById('inVisitors').value;
  const goal = document.getElementById('inGoal').value;

  document.getElementById('outEventName').textContent = name;
  document.getElementById('outVenueType').textContent = vtype;
  document.getElementById('outVisitors').textContent = vis;
  document.getElementById('outGoal').textContent = goal;

  const chkW = document.getElementById('chkWheelchair').checked;
  document.getElementById('outAccess').textContent = chkW ? '무장애 동선 적용' : '일반 동선';

  switchPage('design', document.querySelectorAll('.nav-item')[1]);
}

/* Contingency Simulation Function (Image Requirement) */
function triggerContingency(mode){
  contingencyMode = mode;
  document.querySelectorAll('.btn-contingency').forEach(b => b.classList.remove('active'));

  const status = document.getElementById('contingencyStatus');
  const dVal = document.getElementById('densityVal');
  const wStage = document.getElementById('waitStage');
  const wFood = document.getElementById('waitFood');

  if(mode === 'rain'){
    status.textContent = '🚨 돌발상황: [우천 발생] -> 천막/휴게공간으로 대피 동선 Re-optimization 가동!';
    status.style.color = '#3b82f6';
    dVal.textContent = '2.1 명/m² (대피 우천 대응)';
    wStage.textContent = '1분 (대피중)';
    wFood.textContent = '2분';
  } else if(mode === 'surge'){
    status.textContent = '🚨 돌발상황: [방문객 200% 급증] -> 보조 출입구 자동 개방 및 동선 즉시 분산!';
    status.style.color = '#ef4444';
    dVal.textContent = '3.4 명/m² (주의)';
    wStage.textContent = '12분';
    wFood.textContent = '15분';
  } else if(mode === 'delay'){
    status.textContent = '🚨 돌발상황: [공연 지연] -> 무대 전면 병목 경보, 우회 통로 자동 개설!';
    status.style.color = '#f59e0b';
    dVal.textContent = '2.8 명/m² (경계)';
    wStage.textContent = '20분 (정체)';
  } else if(mode === 'medical'){
    status.textContent = '🚨 돌발상황: [응급환자 발생] -> 비상 골든타임 통로 즉시 클리어 및 앰뷸런스 경로 확보!';
    status.style.color = '#10b981';
    dVal.textContent = '1.0 명/m² (골든타임 확보)';
  }
}

function resetContingency(){
  contingencyMode = 'normal';
  document.getElementById('contingencyStatus').textContent = '상태: 정상 시뮬레이션 가동 중';
  document.getElementById('contingencyStatus').style.color = '#cbd5e1';
  document.getElementById('densityVal').textContent = '1.2 명/m² (안전)';
  document.getElementById('waitStage').textContent = '3분';
  document.getElementById('waitFood').textContent = '7분';
}

/* REALTIME ANIMATED SIMULATION ENGINE (requestAnimationFrame) */
function initCanvases(){
  venueCanvas = document.getElementById('venueCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');
  if(!venueCanvas) return;

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth || 500;
  const h = wrap.clientHeight || 350;

  venueCanvas.width = w;
  venueCanvas.height = h;
  heatmapCanvas.width = w;
  heatmapCanvas.height = h;

  venueCtx = venueCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');

  initPeopleData(w, h);

  if(animFrameId) cancelAnimationFrame(animFrameId);
  loopSimulation();
}

function initPeopleData(w, h){
  people = [];
  const count = 70;
  for(let i=0; i<count; i++){
    people.push({
      x: w*0.15 + Math.random()*w*0.7,
      y: h*0.2 + Math.random()*h*0.6,
      vx: (Math.random()-0.5) * 1.5,
      vy: (Math.random()-0.5) * 1.5,
      targetX: w*0.5,
      targetY: h*0.5,
      color: '#ffffff'
    });
  }
}

function loopSimulation(){
  if(!venueCtx) return;

  const w = venueCanvas.width;
  const h = venueCanvas.height;

  // 1. Draw Base Venue Layout
  drawVenueBackground(w, h);

  // 2. Update and Draw People Agents
  updateAndDrawPeople(w, h);

  // 3. Draw Dynamic Heatmap
  drawHeatmapLayer(w, h);

  animFrameId = requestAnimationFrame(loopSimulation);
}

function drawVenueBackground(w, h){
  // Grass Background
  venueCtx.fillStyle = '#2e6f40';
  venueCtx.fillRect(0, 0, w, h);

  // Outer Path Loop
  venueCtx.strokeStyle = '#e2d9c8';
  venueCtx.lineWidth = 28;
  venueCtx.lineCap = 'round';
  venueCtx.beginPath();
  venueCtx.ellipse(w*0.5, h*0.5, w*0.38, h*0.3, 0, 0, Math.PI*2);
  venueCtx.stroke();

  // Emergency Golden Route Overlay if Medical Contingency
  if(contingencyMode === 'medical'){
    venueCtx.strokeStyle = 'rgba(239, 68, 68, 0.8)';
    venueCtx.lineWidth = 10;
    venueCtx.setLineDash([8, 8]);
    venueCtx.beginPath();
    venueCtx.moveTo(w*0.5, h*0.9);
    venueCtx.lineTo(w*0.72, h*0.5);
    venueCtx.stroke();
    venueCtx.setLineDash([]);
  }

  // Central Lawn
  venueCtx.fillStyle = '#3d8b4f';
  venueCtx.beginPath();
  venueCtx.ellipse(w*0.5, h*0.5, w*0.2, h*0.16, 0, 0, Math.PI*2);
  venueCtx.fill();

  // Booth Structures
  drawBooth(venueCtx, w*0.38, h*0.06, w*0.24, h*0.15, '메인 무대', '#8b5cf6', '🎭');
  drawBooth(venueCtx, w*0.10, h*0.20, w*0.16, h*0.14, '체험존 A', '#3b82f6', '🧪');
  drawBooth(venueCtx, w*0.74, h*0.20, w*0.16, h*0.14, '체험존 B', '#3b82f6', '🚀');
  drawBooth(venueCtx, w*0.08, h*0.48, w*0.16, h*0.15, '푸드존', '#f59e0b', '🍔');
  drawBooth(venueCtx, w*0.74, h*0.48, w*0.16, h*0.14, '응급/안내센터', '#ef4444', '🏥');
  drawBooth(venueCtx, w*0.74, h*0.70, w*0.14, h*0.12, '화장실', '#06b6d4', '🚻');

  // Main Entry Gate
  venueCtx.fillStyle = '#0f172a';
  venueCtx.fillRect(w*0.42, h*0.88, w*0.16, h*0.08);
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 10px Pretendard';
  venueCtx.textAlign = 'center';
  venueCtx.fillText('🚪 주출입구 (비상문)', w*0.5, h*0.93);
}

function drawBooth(ctx, x, y, bw, bh, title, color, icon){
  ctx.fillStyle = 'rgba(0,0,0,0.3)';
  ctx.fillRect(x+2, y+2, bw, bh);

  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, bw, bh, 6);
  ctx.fill();
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 1.2;
  ctx.stroke();

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 10px Pretendard';
  ctx.textAlign = 'center';
  ctx.fillText(`${icon} ${title}`, x + bw/2, y + bh/2 + 3);
}

function updateAndDrawPeople(w, h){
  people.forEach(p => {
    // Behavior based on contingency mode
    if(contingencyMode === 'rain'){
      p.targetX = w*0.5; p.targetY = h*0.5; // Rush to shelter
    } else if(contingencyMode === 'delay'){
      p.targetX = w*0.5; p.targetY = h*0.15; // Crowd around stage
    } else if(contingencyMode === 'medical'){
      if(p.x > w*0.5 && p.x < w*0.8) p.x -= 2; // Clear emergency path
    }

    // Movement Physics
    p.x += p.vx + (Math.random()-0.5)*0.8;
    p.y += p.vy + (Math.random()-0.5)*0.8;

    // Boundaries Bounce
    if(p.x < 15 || p.x > w-15) p.vx *= -1;
    if(p.y < 15 || p.y > h-15) p.vy *= -1;

    // Render Dot
    venueCtx.fillStyle = '#ffffff';
    venueCtx.beginPath();
    venueCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
    venueCtx.fill();
    venueCtx.strokeStyle = '#0f172a';
    venueCtx.lineWidth = 0.5;
    venueCtx.stroke();
  });
}

function drawHeatmapLayer(w, h){
  if(!heatmapCtx) return;
  heatmapCtx.clearRect(0, 0, w, h);

  let spots = [
    {x: w*0.5, y: h*0.15, r: 40},
    {x: w*0.16, y: h*0.55, r: 35}
  ];

  if(contingencyMode === 'surge'){
    spots.push({x: w*0.5, y: h*0.85, r: 65});
    spots.push({x: w*0.5, y: h*0.5, r: 50});
  }

  spots.forEach(pt => {
    let grad = heatmapCtx.createRadialGradient(pt.x, pt.y, 0, pt.x, pt.y, pt.r);
    grad.addColorStop(0, 'rgba(239, 68, 68, 0.7)');
    grad.addColorStop(0.5, 'rgba(245, 158, 11, 0.3)');
    grad.addColorStop(1, 'rgba(16, 185, 129, 0)');

    heatmapCtx.fillStyle = grad;
    heatmapCtx.beginPath();
    heatmapCtx.arc(pt.x, pt.y, pt.r, 0, Math.PI*2);
    heatmapCtx.fill();
  });
}

function sendChat(){
  const val = document.getElementById('chatIn').value;
  if(!val) return;
  const box = document.getElementById('chatBox');
  box.innerHTML += `<div style="color:#1e293b;background:#ffffff;padding:8px;border-radius:8px;margin-bottom:8px;text-align:right;"><b>나:</b> ${val}</div>`;
  document.getElementById('chatIn').value = '';
  setTimeout(() => {
    box.innerHTML += `<div style="color:#0369a1;background:#e0f2fe;padding:8px;border-radius:8px;margin-bottom:8px;"><b>AI:</b> 지시하신 "${val}" 명령을 수용하여 디지털 트윈 레이아웃 좌표 및 동선 알고리즘을 재배치했습니다.</div>`;
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
