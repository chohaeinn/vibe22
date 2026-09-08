import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI 이벤트 디자인 워크플로",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SIMULATOR_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 이벤트 디자인 워크플로</title>
<style>
*{box-sizing:border-box}
body{
  margin:0;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR",Arial,sans-serif;
  color:#17233d;
  background:#f7fbff;
}
button,select,input{font:inherit}
button{cursor:pointer}
.app{
  min-height:1120px;
  padding:18px;
  background:
    radial-gradient(circle at 20% 0%,rgba(72,126,255,.08),transparent 30%),
    linear-gradient(135deg,#f8fbff,#eef7ff);
}
.topbar{
  height:86px;
  display:flex;
  align-items:center;
  gap:16px;
  padding:12px 16px;
  border:1px solid #dbe8f7;
  border-radius:22px;
  background:rgba(255,255,255,.94);
  box-shadow:0 10px 30px rgba(50,100,160,.08);
}
.brand{
  width:265px;
  display:flex;
  align-items:center;
  gap:12px;
}
.brandIcon{
  width:45px;height:45px;border-radius:14px;
  display:grid;place-items:center;
  color:white;font-size:24px;font-weight:900;
  background:linear-gradient(135deg,#2563eb,#5b7cff);
  box-shadow:0 8px 18px rgba(37,99,235,.25);
}
.brandTitle{font-weight:900;font-size:20px;letter-spacing:-.7px}
.brandSub{font-size:11px;color:#6c7b91;margin-top:3px}
.topControls{flex:1;display:grid;grid-template-columns:repeat(4,minmax(120px,1fr));gap:10px}
.controlBox{
  min-width:0;padding:7px 12px;border:1px solid #e2eaf4;
  border-radius:14px;background:#fbfdff;
}
.controlBox label{display:block;font-size:10px;color:#78869a;font-weight:800;margin-bottom:3px}
.controlBox select,.controlBox input{
  width:100%;border:0;outline:0;background:transparent;color:#1c2b49;font-weight:800;
}
.aiBtn{
  border:0;border-radius:14px;padding:15px 20px;color:white;font-weight:900;
  background:linear-gradient(135deg,#315ff2,#5d6df8);
  box-shadow:0 9px 18px rgba(49,95,242,.25);
  white-space:nowrap;
}
.layout{
  display:grid;
  grid-template-columns:235px minmax(550px,1fr) 380px;
  gap:14px;
  margin-top:14px;
}
.sidebar,.mainCard,.rightCard,.bottomCard{
  border:1px solid #dbe7f4;
  background:rgba(255,255,255,.95);
  box-shadow:0 8px 24px rgba(44,91,137,.07);
}
.sidebar{border-radius:20px;padding:12px;height:990px}
.navItem{
  display:flex;align-items:center;gap:11px;padding:11px 12px;
  margin-bottom:5px;border-radius:12px;font-weight:800;color:#4b5b73;
}
.navItem.active{color:#2463e9;background:#eaf1ff}
.navIcon{width:26px;text-align:center}
.sideSection{margin-top:14px;border-top:1px solid #e8eef6;padding-top:14px}
.sideTitle{display:flex;justify-content:space-between;align-items:center;font-weight:900;font-size:13px;margin-bottom:9px}
.boothGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.boothBtn{
  border:1px solid #dce7f3;background:#fff;border-radius:10px;
  padding:8px 3px;font-size:10px;font-weight:800;color:#50627a;
}
.boothBtn:hover{border-color:#86a9ff;background:#f3f7ff}
.sideField{margin-bottom:9px}
.sideField label{display:block;font-size:10px;color:#77879d;font-weight:800;margin-bottom:4px}
.sideField select,.sideField input{
  width:100%;padding:9px;border:1px solid #dce6f1;border-radius:10px;background:#fbfdff;
}
.saveBtn{
  width:100%;border:0;border-radius:11px;padding:10px;color:white;
  background:#3473ed;font-weight:900;
}
.mainCard{border-radius:20px;padding:12px;min-width:0}
.tabs{display:flex;gap:6px;margin-bottom:10px}
.tab{
  border:1px solid #e0e9f3;background:#fff;border-radius:11px;
  padding:8px 15px;font-weight:800;color:#61728a;
}
.tab.active{background:#eaf1ff;border-color:#c9d9ff;color:#2862df}
.canvasWrap{
  position:relative;height:760px;border:1px solid #dce8f4;border-radius:17px;
  overflow:hidden;background:#f8fcff;
}
.canvasHeader{
  position:absolute;z-index:50;left:14px;right:14px;top:12px;
  display:flex;justify-content:space-between;pointer-events:none;
}
.canvasBadge{
  pointer-events:auto;padding:8px 11px;border:1px solid #d9e6f2;
  background:rgba(255,255,255,.94);border-radius:11px;font-size:11px;font-weight:900;
  box-shadow:0 5px 12px rgba(50,90,130,.08);
}
.zoomBtns{display:flex;gap:5px;pointer-events:auto}
.zoomBtns button{
  width:34px;height:34px;border:1px solid #dce7f2;background:white;border-radius:10px;
  font-weight:900;
}
#venue{
  position:absolute;left:50%;top:52%;transform:translate(-50%,-50%);
  width:min(90%,900px);height:min(78%,590px);
  border:3px solid #7086a0;border-radius:18px;
  background:#fff;box-shadow:0 18px 38px rgba(55,88,120,.18);
  overflow:hidden;
}
#venue.lshape{border-radius:18px}
#grid{
  position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(81,124,170,.09) 1px,transparent 1px),
    linear-gradient(90deg,rgba(81,124,170,.09) 1px,transparent 1px);
  background-size:24px 24px;
}
#heatmap,#people,#flow{
  position:absolute;inset:0;width:100%;height:100%;pointer-events:none;
}
#heatmap{z-index:5}
#flow{z-index:8}
#people{z-index:12}
#booths{position:absolute;inset:0;z-index:20}
.booth{
  position:absolute;display:flex;align-items:center;justify-content:center;
  flex-direction:column;gap:3px;padding:6px;border-radius:10px;
  border:2px solid rgba(30,63,105,.28);box-shadow:0 5px 12px rgba(40,70,110,.13);
  color:#18304e;user-select:none;cursor:grab;font-weight:900;text-align:center;
  overflow:hidden;
}
.booth:active{cursor:grabbing}
.booth .bname{font-size:11px;line-height:1.1}
.booth .btype{font-size:9px;opacity:.72}
.booth.popular{background:#ffe4e8;border-color:#f29ba8}
.booth.main{background:#dce9ff;border-color:#82a8f4}
.booth.food{background:#fff0cc;border-color:#efc45b}
.booth.medical{background:#e2f7ee;border-color:#79cda8}
.booth.rest{background:#e7f6ff;border-color:#8cc7e8}
.booth.normal{background:#e4f0ff;border-color:#91b8ea}
.booth.selected{outline:3px solid #316ff1;outline-offset:2px}
.resizeHandle{
  position:absolute;right:2px;bottom:2px;width:10px;height:10px;
  border-radius:3px;background:rgba(39,82,140,.35);cursor:nwse-resize;
}
.gate{
  position:absolute;z-index:30;bottom:-1px;padding:7px 12px;border-radius:11px 11px 0 0;
  background:#e9fff6;border:2px solid #35b68b;color:#168362;font-size:11px;font-weight:900;
}
.gate.exit{background:#fff4dc;border-color:#e5aa35;color:#a36b00}
#entranceGate{left:16%}
#exitGate{right:16%}
.simBar{
  display:flex;align-items:center;gap:10px;margin-top:10px;padding:10px;
  border:1px solid #e0e9f2;border-radius:14px;background:#fbfdff;
}
.primary{
  border:0;border-radius:11px;padding:11px 15px;background:#3675ee;color:white;font-weight:900;
}
.secondary{
  border:1px solid #dce7f2;border-radius:11px;padding:10px 12px;background:white;font-weight:900;color:#50627b;
}
.range{flex:1}
.range input{width:100%}
.timeBox{font-size:11px;color:#68798f;min-width:85px;text-align:center}
.speedSelect{padding:8px;border:1px solid #dce7f2;border-radius:9px;background:white}
.rightCol{display:flex;flex-direction:column;gap:14px}
.rightCard{border-radius:20px;padding:14px}
.cardTitle{display:flex;align-items:center;justify-content:space-between;font-weight:900;font-size:14px;margin-bottom:12px}
.live{font-size:10px;color:#15916f;background:#e7fff5;padding:5px 8px;border-radius:20px}
.statGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.stat{
  padding:10px;border:1px solid #e4ebf3;border-radius:11px;background:#fcfdff;
}
.stat small{display:block;color:#7a899d;font-size:9px;font-weight:800}
.stat strong{display:block;font-size:18px;margin-top:3px}
.miniGrid{display:grid;grid-template-columns:repeat(2,1fr);gap:7px;margin-top:7px}
.mini{
  padding:9px;border:1px solid #e4ebf3;border-radius:11px;
}
.mini span{display:block;font-size:9px;color:#77879b;font-weight:800}
.mini b{font-size:15px}
.heatLegend{
  height:10px;border-radius:10px;margin:7px 0;
  background:linear-gradient(90deg,#46c9ff,#6ee7b7,#ffe36b,#ff9d43,#ef4444);
}
.legendLabels{display:flex;justify-content:space-between;font-size:9px;color:#77879b}
.miniMap{
  height:180px;margin-top:8px;border-radius:12px;overflow:hidden;border:1px solid #dce6f0;background:#eff8ff;
}
#miniHeat{width:100%;height:100%}
.compare{display:grid;grid-template-columns:1fr 28px 1fr;align-items:center;gap:5px}
.compareBox{padding:10px;border-radius:12px;background:#f5f8fc;border:1px solid #e1e9f2}
.compareBox h4{margin:0 0 7px;font-size:10px}
.compareRow{display:flex;justify-content:space-between;font-size:10px;padding:3px 0}
.before{color:#e14d59;font-weight:900}
.after{color:#14966f;font-weight:900}
.arrow{font-size:22px;text-align:center;color:#55708f}
.recommend{
  margin-top:9px;padding:9px 10px;border-radius:11px;background:#effbf7;border:1px solid #cdeee3;
  color:#197c64;font-size:10px;font-weight:800;line-height:1.45;
}
.bottomGrid{display:grid;grid-template-columns:1fr 1.25fr 1.05fr;gap:14px;margin-top:14px}
.bottomCard{border-radius:20px;padding:14px;min-height:205px}
.scoreCircle{
  width:105px;height:105px;border-radius:50%;margin:5px auto 8px;
  display:grid;place-items:center;
  background:conic-gradient(#29b997 var(--scoredeg),#e8f0f5 0);
  position:relative;
}
.scoreCircle:after{content:"";position:absolute;inset:10px;background:white;border-radius:50%}
.scoreText{position:relative;z-index:2;text-align:center}
.scoreText b{font-size:25px;display:block}.scoreText span{font-size:9px;color:#74859a}
.metricLine{margin:7px 0}.metricLineTop{display:flex;justify-content:space-between;font-size:9px;font-weight:800}
.bar{height:7px;background:#e9eff5;border-radius:10px;overflow:hidden;margin-top:4px}
.bar i{display:block;height:100%;border-radius:10px;background:#5a9ff5}
#chart{width:100%;height:145px;border:1px solid #e2eaf2;border-radius:12px;background:#fbfdff}
.recItem{display:flex;gap:8px;padding:7px 0;border-bottom:1px solid #edf1f5;font-size:10px;font-weight:800}
.recNum{width:20px;height:20px;border-radius:6px;background:#eaf1ff;color:#2866e7;display:grid;place-items:center}
.smallNote{font-size:9px;color:#8795a7;line-height:1.4;margin-top:8px}
.toast{
  position:fixed;right:20px;bottom:20px;z-index:9999;
  background:#173252;color:white;padding:11px 15px;border-radius:11px;
  opacity:0;transform:translateY(10px);transition:.2s;pointer-events:none;font-size:12px;font-weight:800;
}
.toast.show{opacity:1;transform:translateY(0)}
@media(max-width:1200px){
  .layout{grid-template-columns:190px 1fr}.rightCol{grid-column:1/-1;display:grid;grid-template-columns:repeat(2,1fr)}
}
@media(max-width:850px){
  .topControls{display:none}.layout{grid-template-columns:1fr}.sidebar{height:auto}.rightCol{display:block}
  .bottomGrid{grid-template-columns:1fr}.canvasWrap{height:650px}
}
</style>
</head>
<body>
<div class="app">

  <div class="topbar">
    <div class="brand">
      <div class="brandIcon">✦</div>
      <div>
        <div class="brandTitle">AI 이벤트 디자인 워크플로</div>
        <div class="brandSub">AI가 모두를 위해 안전하고 효율적인 이벤트를 디자인합니다</div>
      </div>
    </div>

    <div class="topControls">
      <div class="controlBox">
        <label>행사장 크기</label>
        <select id="venueSize">
          <option value="20x15">20m × 15m</option>
          <option value="30x20">30m × 20m</option>
          <option value="40x25" selected>40m × 25m</option>
          <option value="50x30">50m × 30m</option>
          <option value="60x40">60m × 40m</option>
        </select>
      </div>
      <div class="controlBox">
        <label>행사장 형태</label>
        <select id="venueShape">
          <option value="rect" selected>직사각형</option>
          <option value="square">정사각형</option>
          <option value="wide">가로형</option>
          <option value="tall">세로형</option>
          <option value="lshape">L자형</option>
        </select>
      </div>
      <div class="controlBox">
        <label>관람객 수</label>
        <select id="visitorCount">
          <option value="100">100명</option>
          <option value="300" selected>300명</option>
          <option value="500">500명</option>
          <option value="800">800명</option>
          <option value="1000">1,000명</option>
        </select>
      </div>
      <div class="controlBox">
        <label>입장 방식</label>
        <select id="entranceMode">
          <option value="bottom" selected>중앙 입구</option>
          <option value="bottom2">양쪽 입구</option>
          <option value="left">좌측 입구</option>
          <option value="right">우측 입구</option>
          <option value="top">상단 입구</option>
        </select>
      </div>
    </div>
    <button class="aiBtn" id="aiBtn">✦ AI 최적화 실행</button>
  </div>

  <div class="layout">
    <aside class="sidebar">
      <div class="navItem active"><span class="navIcon">▦</span>대시보드</div>
      <div class="navItem"><span class="navIcon">⌘</span>이벤트 디자인</div>
      <div class="navItem"><span class="navIcon">▣</span>이벤트 모드</div>
      <div class="navItem"><span class="navIcon">◈</span>디자인 템플릿</div>
      <div class="navItem"><span class="navIcon">◉</span>AI 시뮬레이션</div>
      <div class="navItem"><span class="navIcon">▤</span>AI 보고서</div>
      <div class="navItem"><span class="navIcon">⚙</span>설정</div>

      <div class="sideSection">
        <div class="sideTitle"><span>부스 추가하기</span><span style="color:#2e6be8">＋</span></div>
        <div class="boothGrid">
          <button class="boothBtn" data-add="normal">▦<br>일반</button>
          <button class="boothBtn" data-add="popular">♨<br>체험</button>
          <button class="boothBtn" data-add="food">♨<br>푸드</button>
          <button class="boothBtn" data-add="main">★<br>무대</button>
          <button class="boothBtn" data-add="medical">✚<br>의료</button>
          <button class="boothBtn" data-add="rest">☕<br>휴식</button>
        </div>
        <div class="smallNote">추가한 부스는 AI 최적화 실행 후에도 삭제되지 않습니다.</div>
      </div>

      <div class="sideSection">
        <div class="sideTitle">행사장 설정</div>
        <div class="sideField">
          <label>행사장 크기</label>
          <select id="sideSize">
            <option value="20x15">20m × 15m</option>
            <option value="30x20">30m × 20m</option>
            <option value="40x25" selected>40m × 25m</option>
            <option value="50x30">50m × 30m</option>
            <option value="60x40">60m × 40m</option>
          </select>
        </div>
        <div class="sideField">
          <label>행사장 형태</label>
          <select id="sideShape">
            <option value="rect">직사각형</option>
            <option value="square">정사각형</option>
            <option value="wide">가로형</option>
            <option value="tall">세로형</option>
            <option value="lshape">L자형</option>
          </select>
        </div>
        <div class="sideField">
          <label>관람객 수</label>
          <select id="sideVisitors">
            <option value="100">100명</option>
            <option value="300" selected>300명</option>
            <option value="500">500명</option>
            <option value="800">800명</option>
            <option value="1000">1,000명</option>
          </select>
        </div>
        <div class="sideField">
          <label>입장 방식</label>
          <select id="sideEntrance">
            <option value="bottom">중앙 입구</option>
            <option value="bottom2">양쪽 입구</option>
            <option value="left">좌측 입구</option>
            <option value="right">우측 입구</option>
            <option value="top">상단 입구</option>
          </select>
        </div>
        <button class="saveBtn" id="applySettings">설정 저장</button>
      </div>

      <div class="sideSection">
        <div class="sideTitle">시뮬레이션</div>
        <div class="sideField">
          <label>이동 속도</label>
          <select id="sideSpeed">
            <option value="0.5">0.5×</option>
            <option value="1" selected>1.0×</option>
            <option value="2">2.0×</option>
            <option value="3">3.0×</option>
          </select>
        </div>
        <div class="sideField">
          <label>혼잡 기준</label>
          <select id="densityLimit">
            <option value="2">2명/㎡</option>
            <option value="3" selected>3명/㎡</option>
            <option value="4">4명/㎡</option>
            <option value="5">5명/㎡</option>
          </select>
        </div>
      </div>
    </aside>

    <main class="mainCard">
      <div class="tabs">
        <button class="tab active">▦ 평면도</button>
        <button class="tab">♨ 히트맵</button>
        <button class="tab">⌁ 동선</button>
        <button class="tab">♧ 시뮬레이션</button>
      </div>

      <div class="canvasWrap" id="canvasWrap">
        <div class="canvasHeader">
          <div class="canvasBadge" id="venueLabel">40m × 25m · 직사각형</div>
          <div class="zoomBtns">
            <button id="zoomIn">＋</button><button id="zoomOut">−</button><button id="resetZoom">⌂</button>
          </div>
        </div>

        <div id="venue">
          <div id="grid"></div>
          <canvas id="heatmap"></canvas>
          <svg id="flow"></svg>
          <canvas id="people"></canvas>
          <div id="booths"></div>
          <div class="gate" id="entranceGate">↑ 입구</div>
          <div class="gate exit" id="exitGate">↓ 출구</div>
        </div>
      </div>

      <div class="simBar">
        <button class="primary" id="startSim">▶ 시뮬레이션 시작</button>
        <button class="secondary" id="pauseSim">Ⅱ</button>
        <div class="range"><input id="timeline" type="range" min="0" max="600" value="0"></div>
        <div class="timeBox">경과 시간<br><b id="timeText">00:00 / 10:00</b></div>
        <select class="speedSelect" id="speedSelect">
          <option value="0.5">0.5×</option>
          <option value="1" selected>1.0×</option>
          <option value="2">2.0×</option>
          <option value="3">3.0×</option>
        </select>
      </div>
    </main>

    <aside class="rightCol">
      <section class="rightCard">
        <div class="cardTitle">👥 실시간 시뮬레이션 현황 <span class="live" id="liveState">● 대기 중</span></div>
        <div class="statGrid">
          <div class="stat"><small>현재 관람객</small><strong id="currentPeople">0명</strong></div>
          <div class="stat"><small>행사장 체류</small><strong id="insidePeople">0명</strong></div>
          <div class="stat"><small>평균 이동거리</small><strong id="avgDistance">0.0m</strong></div>
        </div>
        <div class="miniGrid">
          <div class="mini"><span>평균 대기시간</span><b id="waitTime">0초</b></div>
          <div class="mini"><span>최대 밀집도</span><b id="maxDensity">0.0명/㎡</b></div>
          <div class="mini"><span>혼잡 구역</span><b id="crowdZones">0곳</b></div>
          <div class="mini"><span>출구 병목</span><b id="exitRisk">낮음</b></div>
        </div>
      </section>

      <section class="rightCard">
        <div class="cardTitle">♨ 실시간 혼잡도 히트맵</div>
        <div class="heatLegend"></div>
        <div class="legendLabels"><span>원활</span><span>보통</span><span>혼잡</span><span>매우 혼잡</span></div>
        <div class="miniMap"><canvas id="miniHeat"></canvas></div>
      </section>

      <section class="rightCard">
        <div class="cardTitle">✦ AI 최적화 결과</div>
        <div class="compare">
          <div class="compareBox">
            <h4>▣ 최적화 전</h4>
            <div class="compareRow">혼잡도 <span class="before" id="beforeCong">72%</span></div>
            <div class="compareRow">동선 점수 <b id="beforeFlow">61점</b></div>
            <div class="compareRow">병목 구역 <span class="before" id="beforeBottleneck">4곳</span></div>
          </div>
          <div class="arrow">→</div>
          <div class="compareBox">
            <h4>♧ 최적화 후</h4>
            <div class="compareRow">혼잡도 <span class="after" id="afterCong">31%</span></div>
            <div class="compareRow">동선 점수 <span class="after" id="afterFlow">89점</span></div>
            <div class="compareRow">병목 구역 <span class="after" id="afterBottleneck">1곳</span></div>
          </div>
        </div>
        <div class="recommend" id="recommendation">기존 부스와 사용자가 추가한 부스를 모두 유지하면서 이동거리와 부스 간 간격을 기준으로 배치합니다.</div>
      </section>

      <section class="rightCard">
        <div class="cardTitle">⚙ AI 권장 사항</div>
        <div id="recommendList">
          <div class="recItem"><span class="recNum">1</span><span>시뮬레이션을 시작하면 실제 관람객 이동을 계산합니다.</span></div>
          <div class="recItem"><span class="recNum">2</span><span>인기 부스 주변의 통로 폭을 우선 확보합니다.</span></div>
          <div class="recItem"><span class="recNum">3</span><span>푸드존은 입구와 출구 동선을 방해하지 않도록 분산합니다.</span></div>
          <div class="recItem"><span class="recNum">4</span><span>의료·안내 시설은 접근성이 높은 위치를 우선합니다.</span></div>
        </div>
      </section>
    </aside>
  </div>

  <div class="bottomGrid">
    <section class="bottomCard">
      <div class="cardTitle">✦ AI 분석 리포트</div>
      <div class="scoreCircle" id="scoreCircle" style="--scoredeg:330deg">
        <div class="scoreText"><b id="overallScore">91</b><span>종합 만족도</span></div>
      </div>
      <div class="metricLine"><div class="metricLineTop"><span>동선 효율성</span><b id="flowScore">92</b></div><div class="bar"><i id="flowBar" style="width:92%"></i></div></div>
      <div class="metricLine"><div class="metricLineTop"><span>혼잡도 관리</span><b id="densityScore">88</b></div><div class="bar"><i id="densityBar" style="width:88%"></i></div></div>
      <div class="metricLine"><div class="metricLineTop"><span>공간 활용도</span><b id="spaceScore">87</b></div><div class="bar"><i id="spaceBar" style="width:87%"></i></div></div>
      <div class="metricLine"><div class="metricLineTop"><span>안전성</span><b id="safetyScore">95</b></div><div class="bar"><i id="safetyBar" style="width:95%"></i></div></div>
    </section>

    <section class="bottomCard">
      <div class="cardTitle">이벤트 동선 분석</div>
      <canvas id="chart"></canvas>
      <div class="smallNote">시간이 지날수록 누적 이동량과 주요 구역의 통과량을 계산합니다.</div>
    </section>

    <section class="bottomCard">
      <div class="cardTitle">AI 추천 배치안</div>
      <div class="recItem"><span class="recNum">1</span><span>메인 무대 접근 경로 확보</span></div>
      <div class="recItem"><span class="recNum">2</span><span>인기 체험부스 간격 확대</span></div>
      <div class="recItem"><span class="recNum">3</span><span>푸드존을 출구 측으로 분산</span></div>
      <div class="recItem"><span class="recNum">4</span><span>의료·안내 시설을 입구 근처로 이동</span></div>
      <button class="primary" id="applyAI" style="width:100%;margin-top:10px">적용하기</button>
    </section>
  </div>

  <div class="toast" id="toast"></div>
</div>

<script>
/* =========================
   AI 이벤트 시뮬레이터
   ========================= */

const DEFAULT_BOOTHS = [
  {id:"b1",name:"메인 무대",type:"main",x:12,y:2,w:10,h:4.5,icon:"★",manual:false},
  {id:"b2",name:"인기 체험부스",type:"popular",x:4,y:7,w:6.5,h:4.5,icon:"♨",manual:false},
  {id:"b3",name:"IT 전시관",type:"normal",x:12,y:8,w:6.5,h:4.5,icon:"▦",manual:false},
  {id:"b4",name:"의료/안전존",type:"medical",x:29,y:3,w:7,h:4.5,icon:"✚",manual:false},
  {id:"b5",name:"휴식 구역",type:"rest",x:28,y:8,w:7,h:4.5,icon:"☕",manual:false},
  {id:"b6",name:"푸드존",type:"food",x:31,y:14,w:6.5,h:5,icon:"♨",manual:false},
  {id:"b7",name:"체험존",type:"popular",x:5,y:14,w:6.5,h:5,icon:"♨",manual:false},
  {id:"b8",name:"정보센터",type:"normal",x:18,y:14,w:6.5,h:4.5,icon:"i",manual:false},
];

let booths = JSON.parse(JSON.stringify(DEFAULT_BOOTHS));
let selectedBooth = null;
let dragging = null;
let running = false;
let paused = false;
let simTime = 0;
let lastFrame = 0;
let speedMultiplier = 1;
let people = [];
let densityGrid = [];
let routeCache = {};
let totalDistance = 0;
let completedVisitors = 0;
let chartHistory = [];
let zoom = 1;
let venue = {w:40,h:25,shape:"rect"};

const $ = id => document.getElementById(id);
const clamp = (v,a,b) => Math.max(a,Math.min(b,v));
const rand = (a,b) => a + Math.random()*(b-a);

function toast(msg){
  const el=$("toast"); el.textContent=msg; el.classList.add("show");
  setTimeout(()=>el.classList.remove("show"),2200);
}

function typeLabel(t){
  return ({normal:"일반 부스",popular:"체험 부스",food:"푸드존",main:"메인 무대",medical:"의료/안전",rest:"휴식 구역"})[t] || "부스";
}

function syncSelects(){
  $("venueSize").value = $("sideSize").value;
  $("venueShape").value = $("sideShape").value;
  $("visitorCount").value = $("sideVisitors").value;
  $("entranceMode").value = $("sideEntrance").value;
  $("speedSelect").value = $("sideSpeed").value;
}

function parseSize(v){
  const [w,h]=v.split("x").map(Number);
  return {w,h};
}

function applyVenue(){
  const size=parseSize($("sideSize").value);
  venue.w=size.w; venue.h=size.h; venue.shape=$("sideShape").value;
  $("venueLabel").textContent=`${venue.w}m × ${venue.h}m · ${shapeLabel(venue.shape)}`;
  $("venue").classList.toggle("lshape",venue.shape==="lshape");
  syncSelects();
  clampAllBooths();
  renderBooths();
  initCanvases();
  drawHeatmap();
  drawPeople();
  drawFlow();
}

function shapeLabel(s){
  return ({rect:"직사각형",square:"정사각형",wide:"가로형",tall:"세로형",lshape:"L자형"})[s] || s;
}

function pointInsideVenue(x,y,margin=0){
  if(x<margin || y<margin || x>venue.w-margin || y>venue.h-margin) return false;
  if(venue.shape!=="lshape") return true;
  // L자형: 오른쪽 위 모서리를 비운 형태
  const cutX=venue.w*0.58, cutY=venue.h*0.42;
  if(x>cutX && y<cutY) return false;
  return true;
}

function rectInsideVenue(b){
  const pts=[
    [b.x,b.y],[b.x+b.w,b.y],[b.x,b.y+b.h],[b.x+b.w,b.y+b.h]
  ];
  return pts.every(p=>pointInsideVenue(p[0],p[1],.35));
}

function overlaps(a,b,gap=.5){
  return !(a.x+a.w+gap<=b.x || b.x+b.w+gap<=a.x || a.y+a.h+gap<=b.y || b.y+b.h+gap<=a.y);
}

function hasCollision(b,ignoreId=null){
  return booths.some(o=>o.id!==ignoreId && overlaps(b,o,.55));
}

function clampBooth(b){
  b.w=clamp(b.w,3,Math.max(3,venue.w-1));
  b.h=clamp(b.h,2.5,Math.max(2.5,venue.h-1));
  b.x=clamp(b.x,.5,venue.w-b.w-.5);
  b.y=clamp(b.y,.5,venue.h-b.h-.5);
  for(let i=0;i<30 && !rectInsideVenue(b);i++){
    b.x=clamp(b.x+rand(-1,1),.5,venue.w-b.w-.5);
    b.y=clamp(b.y+rand(-1,1),.5,venue.h-b.h-.5);
  }
}

function clampAllBooths(){booths.forEach(clampBooth)}

function renderBooths(){
  const layer=$("booths"); layer.innerHTML="";
  booths.forEach(b=>{
    const el=document.createElement("div");
    el.className=`booth ${b.type}${selectedBooth===b.id?" selected":""}`;
    el.dataset.id=b.id;
    el.style.left=(b.x/venue.w*100)+"%";
    el.style.top=(b.y/venue.h*100)+"%";
    el.style.width=(b.w/venue.w*100)+"%";
    el.style.height=(b.h/venue.h*100)+"%";
    el.innerHTML=`<div style="font-size:16px">${b.icon||"▦"}</div><div class="bname">${b.name}</div><div class="btype">${typeLabel(b.type)}${b.manual?" · 사용자 추가":""}</div><div class="resizeHandle"></div>`;
    el.addEventListener("pointerdown",e=>startBoothDrag(e,b,false));
    el.querySelector(".resizeHandle").addEventListener("pointerdown",e=>startBoothDrag(e,b,true));
    el.addEventListener("click",()=>{selectedBooth=b.id;renderBooths()});
    layer.appendChild(el);
  });
}

function startBoothDrag(e,b,resizing){
  e.preventDefault(); e.stopPropagation();
  selectedBooth=b.id;
  dragging={b,resizing,startX:e.clientX,startY:e.clientY,x:b.x,y:b.y,w:b.w,h:b.h};
  window.addEventListener("pointermove",moveBooth);
  window.addEventListener("pointerup",endBooth);
}
function moveBooth(e){
  if(!dragging)return;
  const rect=$("venue").getBoundingClientRect();
  const dx=(e.clientX-dragging.startX)/rect.width*venue.w;
  const dy=(e.clientY-dragging.startY)/rect.height*venue.h;
  const b=dragging.b;
  if(dragging.resizing){
    b.w=clamp(dragging.w+dx,3,venue.w-b.x-.5);
    b.h=clamp(dragging.h+dy,2.5,venue.h-b.y-.5);
  }else{
    b.x=dragging.x+dx;b.y=dragging.y+dy;clampBooth(b);
  }
  renderBooths();drawFlow();
}
function endBooth(){
  if(dragging){
    const b=dragging.b;
    if(hasCollision(b,b.id)){b.x=dragging.x;b.y=dragging.y;b.w=dragging.w;b.h=dragging.h;toast("다른 부스와 겹칠 수 없습니다.");}
  }
  dragging=null;
  window.removeEventListener("pointermove",moveBooth);
  window.removeEventListener("pointerup",endBooth);
  renderBooths();
}

function addBooth(type){
  const names={
    normal:"새 일반 부스",popular:"새 체험 부스",food:"새 푸드존",
    main:"새 메인 무대",medical:"새 의료/안전존",rest:"새 휴식 구역"
  };
  const icons={normal:"▦",popular:"♨",food:"♨",main:"★",medical:"✚",rest:"☕"};
  const sizes={normal:[5,3.5],popular:[5.5,4],food:[5.5,4],main:[7,4],medical:[5.5,3.5],rest:[5.5,3.5]};
  const [w,h]=sizes[type]||[5,3.5];
  let b={id:"m"+Date.now(),name:names[type],type,x:2,y:2,w,h,icon:icons[type],manual:true};
  let placed=false;
  for(let tries=0;tries<300;tries++){
    b.x=rand(.8,Math.max(.9,venue.w-w-.8));
    b.y=rand(.8,Math.max(.9,venue.h-h-.8));
    if(rectInsideVenue(b)&&!hasCollision(b)){placed=true;break}
  }
  if(!placed){toast("현재 공간에 들어갈 위치가 부족합니다.");return}
  booths.push(b);selectedBooth=b.id;renderBooths();drawFlow();
  toast("사용자 부스가 추가되었습니다. AI 최적화 후에도 유지됩니다.");
}

function deleteSelected(){
  if(!selectedBooth){toast("삭제할 부스를 먼저 선택하세요.");return}
  const b=booths.find(x=>x.id===selectedBooth);
  if(!b)return;
  booths=booths.filter(x=>x.id!==selectedBooth);
  selectedBooth=null;renderBooths();drawFlow();
  toast(`${b.name} 삭제`);
}

function candidateScore(b,placed){
  const centerX=venue.w/2,centerY=venue.h/2;
  const cx=b.x+b.w/2,cy=b.y+b.h/2;
  let score=0;
  const entrance=getEntrancePoint();
  const distEnt=Math.hypot(cx-entrance.x,cy-entrance.y);
  const centerDist=Math.hypot(cx-centerX,cy-centerY);
  score -= distEnt*.06;
  if(b.type==="medical") score -= distEnt*.45;
  if(b.type==="main") score -= centerDist*.35;
  if(b.type==="popular") score -= centerDist*.08;
  if(b.type==="food") score += distEnt*.10;
  placed.forEach(o=>{
    const ox=o.x+o.w/2,oy=o.y+o.h/2;
    const d=Math.hypot(cx-ox,cy-oy);
    score += clamp(d,0,8)*.35;
  });
  // 통로를 만들기 위해 중앙의 과도한 밀집을 약간 억제
  if(b.type!=="main") score -= Math.max(0,2.5-centerDist)*.35;
  return score;
}

function optimizeLayout(){
  // 핵심: booths 배열을 초기화하지 않는다.
  // 즉 사용자가 추가한 manual=true 부스도 그대로 유지된다.
  const before=layoutQuality();
  const original=JSON.parse(JSON.stringify(booths));

  // 사용자 추가 부스는 존재 자체를 보존하고, 위치는 개선할 수 있게 한다.
  const locked=booths.filter(b=>b.locked);
  const movable=booths.filter(b=>!b.locked);
  const placed=[...locked.map(x=>JSON.parse(JSON.stringify(x)))];

  movable.sort((a,b)=>{
    const weight={medical:5,main:4,popular:3,food:2,normal:1,rest:1};
    return (weight[b.type]||1)-(weight[a.type]||1);
  });

  for(const b of movable){
    let best=null,bestScore=-Infinity;
    const candidates=[];
    candidates.push({x:b.x,y:b.y});
    const step=Math.max(1,Math.min(2,venue.w/20));
    for(let x=.8;x<venue.w-b.w-.5;x+=step){
      for(let y=.8;y<venue.h-b.h-.5;y+=step){
        candidates.push({x,y});
      }
    }
    for(let k=0;k<40;k++){
      candidates.push({
        x:clamp(b.x+rand(-5,5),.8,Math.max(.8,venue.w-b.w-.5)),
        y:clamp(b.y+rand(-5,5),.8,Math.max(.8,venue.h-b.h-.5))
      });
    }
    for(const c of candidates){
      const test={...b,x:c.x,y:c.y};
      if(!rectInsideVenue(test))continue;
      if(placed.some(o=>overlaps(test,o,.7)))continue;
      const s=candidateScore(test,placed);
      if(s>bestScore){bestScore=s;best=c}
    }
    if(best){b.x=best.x;b.y=best.y}
    placed.push(JSON.parse(JSON.stringify(b)));
  }

  // 2차 충돌 제거
  for(let pass=0;pass<20;pass++){
    let changed=false;
    for(let i=0;i<booths.length;i++){
      for(let j=i+1;j<booths.length;j++){
        const a=booths[i],b=booths[j];
        if(!overlaps(a,b,.35))continue;
        if(a.locked && b.locked)continue;
        const mover=b.locked?a: b;
        mover.x += mover.x+mover.w/2 < a.x+a.w/2 ? -1 : 1;
        mover.y += mover.y+mover.h/2 < a.y+a.h/2 ? -1 : 1;
        clampBooth(mover);changed=true;
      }
    }
    if(!changed)break;
  }

  renderBooths();drawFlow();
  const after=layoutQuality();
  updateCompare(before,after);
  $("recommendation").textContent=`${booths.length}개 부스를 유지한 채 최적화했습니다. 사용자 추가 부스 ${booths.filter(b=>b.manual).length}개도 보존되었습니다.`;
  updateRecommendations();
  toast("AI 공간 최적화가 완료되었습니다.");
}

function layoutQuality(){
  let overlap=0,avgDist=0,count=0;
  for(let i=0;i<booths.length;i++){
    for(let j=i+1;j<booths.length;j++){
      const a=booths[i],b=booths[j];
      if(overlaps(a,b,0))overlap++;
      const d=Math.hypot((a.x+a.w/2)-(b.x+b.w/2),(a.y+a.h/2)-(b.y+b.h/2));
      avgDist+=d;count++;
    }
  }
  avgDist=count?avgDist/count:0;
  const crowd=clamp(70-overlap*10+avgDist*1.5,10,95);
  const flow=clamp(58+avgDist*2.2-overlap*15,20,96);
  const bottleneck=Math.max(0,overlap+Math.round(Math.max(0,5-avgDist/3)));
  return {crowd,flow,bottleneck};
}

function updateCompare(before,after){
  $("beforeCong").textContent=Math.round(before.crowd)+"%";
  $("beforeFlow").textContent=Math.round(before.flow)+"점";
  $("beforeBottleneck").textContent=before.bottleneck+"곳";
  $("afterCong").textContent=Math.round(after.crowd)+"%";
  $("afterFlow").textContent=Math.round(after.flow)+"점";
  $("afterBottleneck").textContent=after.bottleneck+"곳";
}

function getEntrancePoints(){
  const mode=$("entranceMode").value;
  if(mode==="bottom2")return [{x:venue.w*.25,y:venue.h-.3},{x:venue.w*.75,y:venue.h-.3}];
  if(mode==="left")return [{x:.3,y:venue.h*.55}];
  if(mode==="right")return [{x:venue.w-.3,y:venue.h*.55}];
  if(mode==="top")return [{x:venue.w*.5,y:.3}];
  return [{x:venue.w*.5,y:venue.h-.3}];
}
function getEntrancePoint(){return getEntrancePoints()[0]}
function getExitPoint(){return {x:venue.w*.5,y:venue.h-.3}}

function boothTarget(b){
  const margin=.7;
  const points=[
    {x:b.x+b.w/2,y:b.y-margin},
    {x:b.x+b.w+margin,y:b.y+b.h/2},
    {x:b.x+b.w/2,y:b.y+b.h+margin},
    {x:b.x-margin,y:b.y+b.h/2}
  ];
  return points.find(p=>pointInsideVenue(p.x,p.y,.2)) || {x:b.x+b.w/2,y:b.y+b.h/2};
}

function nearestSafePoint(p){
  if(pointInsideVenue(p.x,p.y,.1))return p;
  return {x:clamp(p.x,.5,venue.w-.5),y:clamp(p.y,.5,venue.h-.5)};
}

/* 간단한 A* 격자 경로 탐색.
   사람마다 새로 계산하지 않고 source/target 조합을 캐시한다. */
function findPath(start,target){
  const step=1;
  const cols=Math.ceil(venue.w/step)+1;
  const rows=Math.ceil(venue.h/step)+1;
  const sx=clamp(Math.round(start.x/step),0,cols-1);
  const sy=clamp(Math.round(start.y/step),0,rows-1);
  const tx=clamp(Math.round(target.x/step),0,cols-1);
  const ty=clamp(Math.round(target.y/step),0,rows-1);
  const key=`${sx},${sy}->${tx},${ty}`;
  if(routeCache[key])return routeCache[key];

  const blocked=(gx,gy)=>{
    const x=gx*step,y=gy*step;
    if(!pointInsideVenue(x,y,.2))return true;
    return booths.some(b=>x>b.x-.55&&x<b.x+b.w+.55&&y>b.y-.55&&y<b.y+b.h+.55);
  };
  const nodeKey=(x,y)=>x+","+y;
  const open=[{x:sx,y:sy,g:0,f:Math.hypot(tx-sx,ty-sy)}];
  const came=new Map(),gScore=new Map([[nodeKey(sx,sy),0]]);
  const dirs=[[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]];
  let found=false;
  let loops=0;
  while(open.length && loops<7000){
    loops++;
    open.sort((a,b)=>a.f-b.f);
    const cur=open.shift();
    if(Math.abs(cur.x-tx)<=1&&Math.abs(cur.y-ty)<=1){found=true;break}
    for(const [dx,dy] of dirs){
      const nx=cur.x+dx,ny=cur.y+dy;
      if(nx<0||ny<0||nx>=cols||ny>=rows||blocked(nx,ny))continue;
      const nk=nodeKey(nx,ny);
      const ng=cur.g+((dx&&dy)?1.414:1);
      if(!gScore.has(nk)||ng<gScore.get(nk)){
        gScore.set(nk,ng);
        came.set(nk,nodeKey(cur.x,cur.y));
        open.push({x:nx,y:ny,g:ng,f:ng+Math.hypot(tx-nx,ty-ny)});
      }
    }
  }
  let path=[];
  if(found){
    let k=nodeKey(tx,ty);
    for(let i=0;i<500 && k;i++){
      const [x,y]=k.split(",").map(Number);
      path.push({x:x*step,y:y*step});
      if(k===nodeKey(sx,sy))break;
      k=came.get(k);
    }
    path.reverse();
  }else{
    path=[nearestSafePoint(target)];
  }
  // 경로 포인트를 줄여 렌더링/이동 비용을 낮춤
  const simplified=[];
  path.forEach((p,i)=>{
    if(i===0||i===path.length-1||i%3===0)simplified.push(p)
  });
  routeCache[key]=simplified;
  return simplified;
}

function weightedBooth(){
  if(!booths.length)return null;
  const weights=booths.map(b=>{
    if(b.type==="popular")return 4;
    if(b.type==="main")return 2.5;
    if(b.type==="food")return 2;
    if(b.type==="medical")return 1;
    if(b.type==="rest")return 1.4;
    return 1.2;
  });
  const total=weights.reduce((a,b)=>a+b,0);
  let r=Math.random()*total;
  for(let i=0;i<booths.length;i++){r-=weights[i];if(r<=0)return booths[i]}
  return booths[booths.length-1];
}

function makePerson(i){
  const gates=getEntrancePoints();
  const gate=gates[i%gates.length];
  const target=weightedBooth();
  const start={x:gate.x+rand(-.7,.7),y:gate.y+rand(-.3,.3)};
  const goal=target?boothTarget(target):getExitPoint();
  return {
    id:i,x:start.x,y:start.y,prevX:start.x,prevY:start.y,
    speed:rand(1.0,1.55),targetId:target?target.id:null,
    path:findPath(start,goal),pathIndex:0,dwell:rand(1.5,5),
    distance:0,done:false,exiting:false,entered:true
  };
}

function resetSimulation(){
  running=false;paused=false;simTime=0;totalDistance=0;completedVisitors=0;chartHistory=[];routeCache={};
  const n=Number($("visitorCount").value);
  people=[];
  // 초기에는 일부만 입장시켜 실제 행사장에 유입되는 모습으로 시작
  const initial=Math.min(n,Math.max(30,Math.round(n*.28)));
  for(let i=0;i<initial;i++)people.push(makePerson(i));
  $("timeline").value=0;
  updateMetrics();
  drawPeople();drawHeatmap();drawChart();
  $("liveState").textContent="● 준비 완료";
}

function spawnPeople(){
  const target=Number($("visitorCount").value);
  const maxInitial=Math.min(target,Math.max(30,Math.round(target*.28)));
  while(people.length<maxInitial)people.push(makePerson(people.length));
}

function chooseNextTarget(p){
  const target=weightedBooth();
  if(!target){p.exiting=true;p.path=findPath({x:p.x,y:p.y},getExitPoint());p.pathIndex=0;return}
  p.targetId=target.id;
  p.path=findPath({x:p.x,y:p.y},boothTarget(target));
  p.pathIndex=0;
}

function updatePeople(dt){
  const targetCount=Number($("visitorCount").value);
  // 시간이 지나면 관람객이 조금씩 입장
  const desired=Math.min(targetCount,Math.max(30,Math.round(30+simTime/600*targetCount)));
  while(people.length<desired)people.push(makePerson(people.length));

  for(const p of people){
    if(p.done)continue;
    if(p.dwell>0 && p.pathIndex>=p.path.length-1){
      p.dwell-=dt;
      if(p.dwell>0)continue;
      if(p.exiting){p.done=true;completedVisitors++;continue}
      if(Math.random()<.16){
        p.exiting=true;
        p.path=findPath({x:p.x,y:p.y},getExitPoint());
        p.pathIndex=0;
      }else{
        chooseNextTarget(p);
      }
    }
    const next=p.path[p.pathIndex+1]||p.path[p.path.length-1];
    if(!next)continue;
    const dx=next.x-p.x,dy=next.y-p.y,d=Math.hypot(dx,dy);
    if(d<.12){
      p.pathIndex++;
      continue;
    }
    const speed=p.speed*speedMultiplier;
    const move=Math.min(d,speed*dt);
    p.prevX=p.x;p.prevY=p.y;
    p.x+=dx/d*move;p.y+=dy/d*move;
    const md=Math.hypot(p.x-p.prevX,p.y-p.prevY);
    p.distance+=md;totalDistance+=md;
  }
}

function updateDensity(){
  const cols=Math.ceil(venue.w),rows=Math.ceil(venue.h);
  densityGrid=new Array(cols*rows).fill(0);
  for(const p of people){
    if(p.done)continue;
    const x=clamp(Math.floor(p.x),0,cols-1);
    const y=clamp(Math.floor(p.y),0,rows-1);
    densityGrid[y*cols+x]++;
  }
}

function densityStats(){
  const limit=Number($("densityLimit").value);
  const max=densityGrid.length?Math.max(...densityGrid):0;
  let zones=0;
  densityGrid.forEach(v=>{if(v>=limit)zones++});
  return {max,zones,limit};
}

function updateMetrics(){
  updateDensity();
  const ds=densityStats();
  const inside=people.filter(p=>!p.done).length;
  const avg=people.length?totalDistance/people.length:0;
  const exitRisk=ds.zones>=5?"높음":ds.zones>=2?"주의":"낮음";
  $("currentPeople").textContent=people.length+"명";
  $("insidePeople").textContent=inside+"명";
  $("avgDistance").textContent=avg.toFixed(1)+"m";
  $("waitTime").textContent=Math.round(ds.max*4)+"초";
  $("maxDensity").textContent=ds.max.toFixed(1)+"명/㎡";
  $("crowdZones").textContent=ds.zones+"곳";
  $("exitRisk").textContent=exitRisk;

  const densityScore=clamp(100-ds.max*10-ds.zones*2,35,98);
  const flowScore=clamp(78+Math.min(20,people.length/50)-ds.zones*1.5,45,98);
  const safetyScore=clamp(98-ds.max*7-ds.zones,40,99);
  const spaceScore=clamp(70+Math.min(25,booths.length*2)-Math.max(0,booths.length-12)*3,45,96);
  const overall=Math.round((densityScore+flowScore+safetyScore+spaceScore)/4);

  $("flowScore").textContent=Math.round(flowScore);
  $("densityScore").textContent=Math.round(densityScore);
  $("safetyScore").textContent=Math.round(safetyScore);
  $("spaceScore").textContent=Math.round(spaceScore);
  $("flowBar").style.width=flowScore+"%";
  $("densityBar").style.width=densityScore+"%";
  $("safetyBar").style.width=safetyScore+"%";
  $("spaceBar").style.width=spaceScore+"%";
  $("overallScore").textContent=overall;
  $("scoreCircle").style.setProperty("--scoredeg",(overall/100*360)+"deg");
}

function drawHeatmap(){
  const c=$("heatmap"),r=$("venue").getBoundingClientRect();
  const dpr=window.devicePixelRatio||1;
  c.width=r.width*dpr;c.height=r.height*dpr;
  const ctx=c.getContext("2d");ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,r.width,r.height);
  if(!densityGrid.length)return;
  const cols=Math.ceil(venue.w),rows=Math.ceil(venue.h);
  const cw=r.width/cols,ch=r.height/rows;
  for(let y=0;y<rows;y++){
    for(let x=0;x<cols;x++){
      const v=densityGrid[y*cols+x]||0;
      if(v<=0)continue;
      const px=(x+.5)*cw,py=(y+.5)*ch;
      const rad=Math.max(cw,ch)*1.8;
      const g=ctx.createRadialGradient(px,py,0,px,py,rad);
      const alpha=clamp(.10+v*.045,.10,.48);
      g.addColorStop(0,`rgba(239,68,68,${alpha})`);
      g.addColorStop(.35,`rgba(255,170,45,${alpha*.8})`);
      g.addColorStop(.7,`rgba(90,210,150,${alpha*.45})`);
      g.addColorStop(1,"rgba(90,210,150,0)");
      ctx.fillStyle=g;ctx.fillRect(px-rad,py-rad,rad*2,rad*2);
    }
  }
  drawMiniHeat();
}

function drawMiniHeat(){
  const c=$("miniHeat"),r=c.getBoundingClientRect(),dpr=window.devicePixelRatio||1;
  c.width=r.width*dpr;c.height=r.height*dpr;
  const ctx=c.getContext("2d");ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,r.width,r.height);
  ctx.fillStyle="#f3f8fc";ctx.fillRect(0,0,r.width,r.height);
  if(!densityGrid.length)return;
  const cols=Math.ceil(venue.w),rows=Math.ceil(venue.h),cw=r.width/cols,ch=r.height/rows;
  for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
    const v=densityGrid[y*cols+x]||0;if(v<=0)continue;
    const a=clamp(.08+v*.06,.08,.75);
    const t=clamp(v/Math.max(4,densityStats().limit*2),0,1);
    const rr=Math.round(40+215*t),gg=Math.round(205-155*t),bb=Math.round(235-195*t);
    ctx.fillStyle=`rgba(${rr},${gg},${bb},${a})`;
    ctx.fillRect(x*cw,y*ch,cw+1,ch+1);
  }
  ctx.strokeStyle="#b6c7d8";ctx.lineWidth=2;ctx.strokeRect(1,1,r.width-2,r.height-2);
}

function drawPeople(){
  const c=$("people"),r=$("venue").getBoundingClientRect(),dpr=window.devicePixelRatio||1;
  c.width=r.width*dpr;c.height=r.height*dpr;
  const ctx=c.getContext("2d");ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,r.width,r.height);
  const sx=r.width/venue.w,sy=r.height/venue.h;
  for(const p of people){
    if(p.done)continue;
    const x=p.x*sx,y=p.y*sy;
    ctx.beginPath();ctx.arc(x,y,2.3,0,Math.PI*2);
    ctx.fillStyle="#1d5fe8";ctx.fill();
  }
}

function drawFlow(){
  const svg=$("flow"),r=$("venue").getBoundingClientRect();
  svg.setAttribute("viewBox",`0 0 ${r.width} ${r.height}`);
  svg.innerHTML="";
  const sx=r.width/venue.w,sy=r.height/venue.h;
  const entrance=getEntrancePoint();
  booths.forEach((b,i)=>{
    const target=boothTarget(b);
    const path=findPath(entrance,target);
    if(!path.length)return;
    let d=`M ${entrance.x*sx} ${entrance.y*sy}`;
    path.forEach(p=>{d+=` L ${p.x*sx} ${p.y*sy}`});
    const el=document.createElementNS("http://www.w3.org/2000/svg","path");
    el.setAttribute("d",d);
    el.setAttribute("fill","none");
    el.setAttribute("stroke","#2f72ed");
    el.setAttribute("stroke-width","1.5");
    el.setAttribute("stroke-dasharray","4 5");
    el.setAttribute("opacity",".48");
    svg.appendChild(el);
  });
}

function drawChart(){
  const c=$("chart"),r=c.getBoundingClientRect(),dpr=window.devicePixelRatio||1;
  c.width=r.width*dpr;c.height=r.height*dpr;
  const ctx=c.getContext("2d");ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,r.width,r.height);
  ctx.strokeStyle="#dfe7f0";ctx.lineWidth=1;
  for(let i=1;i<5;i++){const y=i*r.height/5;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(r.width,y);ctx.stroke()}
  if(chartHistory.length<2)return;
  const max=Math.max(10,...chartHistory);
  ctx.strokeStyle="#4e70ed";ctx.lineWidth=2.5;ctx.beginPath();
  chartHistory.forEach((v,i)=>{
    const x=i/(chartHistory.length-1)*r.width;
    const y=r.height-10-(v/max)*(r.height-25);
    if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
  });
  ctx.stroke();
}

function recordChart(){
  const value=totalDistance;
  chartHistory.push(value);
  if(chartHistory.length>80)chartHistory.shift();
  drawChart();
}

function tick(now){
  if(!lastFrame)lastFrame=now;
  const realDt=Math.min(.05,(now-lastFrame)/1000);
  lastFrame=now;
  if(running&&!paused){
    simTime+=realDt*speedMultiplier;
    updatePeople(realDt);
    updateDensity();
    if(Math.floor(simTime*10)%4===0)recordChart();
    $("timeline").value=Math.round(clamp(simTime,0,600));
    const mm=Math.floor(simTime/60),ss=Math.floor(simTime%60);
    $("timeText").textContent=`${String(mm).padStart(2,"0")}:${String(ss).padStart(2,"0")} / 10:00`;
    if(simTime>=600){running=false;$("liveState").textContent="● 시뮬레이션 완료"}
    updateMetrics();drawHeatmap();drawPeople();
  }
  requestAnimationFrame(tick);
}

function startSimulation(){
  if(!people.length)resetSimulation();
  running=true;paused=false;
  $("liveState").textContent="● 시뮬레이션 진행 중";
  toast("관람객 이동 시뮬레이션을 시작합니다.");
}

function togglePause(){
  if(!running){toast("먼저 시뮬레이션을 시작하세요.");return}
  paused=!paused;
  $("liveState").textContent=paused?"● 일시정지":"● 시뮬레이션 진행 중";
}

function updateRecommendations(){
  const ds=densityStats();
  const list=[
    `${booths.filter(b=>b.type==="popular").length}개 체험 부스의 접근 통로를 우선 확보하세요.`,
    `현재 혼잡 기준은 ${ds.limit}명/㎡이며 ${ds.zones}개 구역이 기준 이상입니다.`,
    `의료/안전 시설은 입구와 중앙 통로에서 빠르게 접근할 수 있도록 유지하세요.`,
    `사용자 추가 부스 ${booths.filter(b=>b.manual).length}개가 현재 레이아웃에 포함되어 있습니다.`
  ];
  $("recommendList").innerHTML=list.map((t,i)=>`<div class="recItem"><span class="recNum">${i+1}</span><span>${t}</span></div>`).join("");
}

function initCanvases(){
  setTimeout(()=>{drawHeatmap();drawPeople();drawFlow();drawChart()},30);
}

function applySettings(){
  applyVenue();
  resetSimulation();
  toast("행사장 설정이 적용되었습니다.");
}

function syncFromTop(){
  $("sideSize").value=$("venueSize").value;
  $("sideShape").value=$("venueShape").value;
  $("sideVisitors").value=$("visitorCount").value;
  $("sideEntrance").value=$("entranceMode").value;
  applyVenue();resetSimulation();
}

$("aiBtn").addEventListener("click",optimizeLayout);
$("applyAI").addEventListener("click",optimizeLayout);
$("applySettings").addEventListener("click",applySettings);
$("startSim").addEventListener("click",startSimulation);
$("pauseSim").addEventListener("click",togglePause);
$("sideSpeed").addEventListener("change",e=>{speedMultiplier=Number(e.target.value);$("speedSelect").value=e.target.value});
$("speedSelect").addEventListener("change",e=>{speedMultiplier=Number(e.target.value);$("sideSpeed").value=e.target.value});
$("timeline").addEventListener("input",e=>{
  const t=Number(e.target.value);
  simTime=t;
  const mm=Math.floor(t/60),ss=Math.floor(t%60);
  $("timeText").textContent=`${String(mm).padStart(2,"0")}:${String(ss).padStart(2,"0")} / 10:00`;
});
$("venueSize").addEventListener("change",syncFromTop);
$("venueShape").addEventListener("change",syncFromTop);
$("visitorCount").addEventListener("change",syncFromTop);
$("entranceMode").addEventListener("change",syncFromTop);
$("densityLimit").addEventListener("change",updateMetrics);

document.querySelectorAll("[data-add]").forEach(btn=>btn.addEventListener("click",()=>addBooth(btn.dataset.add)));

$("zoomIn").addEventListener("click",()=>{$("venue").style.transform=`translate(-50%,-50%) scale(${zoom=clamp(zoom+.1,.8,1.4)})`});
$("zoomOut").addEventListener("click",()=>{$("venue").style.transform=`translate(-50%,-50%) scale(${zoom=clamp(zoom-.1,.8,1.4)})`});
$("resetZoom").addEventListener("click",()=>{zoom=1;$("venue").style.transform="translate(-50%,-50%) scale(1)"});

window.addEventListener("resize",initCanvases);

// 초기화
syncSelects();
applyVenue();
resetSimulation();
renderBooths();
updateRecommendations();
requestAnimationFrame(tick);
</script>
</body>
</html>
"""

components.html(SIMULATOR_HTML, height=1160, scrolling=True)
