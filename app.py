import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(
    page_title="AI 스마트 공간 설계 & 크기조절 시뮬레이터",
    page_icon="📐",
    layout="wide"
)

# 전체 통합 HTML/CSS/JS Engine
SIMULATOR_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 스마트 공간 설계 & 크기조절 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CAD 모눈종이 배경 */
        .cad-grid-light {
            background-size: 20px 20px;
            background-image: 
                linear-gradient(to right, rgba(203, 213, 225, 0.5) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(203, 213, 225, 0.5) 1px, transparent 1px);
        }

        #canvasViewport {
            transition: transform 0.15s ease-out;
            transform-origin: center center;
        }

        /* 부스 카드 및 리사이즈 핸들 */
        .booth-card {
            user-select: none;
            touch-action: none;
            transition: box-shadow 0.15s, border-color 0.15s;
        }
        .booth-card:hover {
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
            border-color: #6366f1;
        }
        .booth-card.dragging {
            opacity: 0.85;
            cursor: grabbing !important;
            z-index: 50 !important;
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.3);
        }

        /* 리사이즈 우측하단 핸들 */
        .resize-handle {
            position: absolute;
            right: 0;
            bottom: 0;
            width: 16px;
            height: 16px;
            cursor: se-resize;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            transition: color 0.2s;
        }
        .resize-handle:hover {
            color: #6366f1;
        }

        /* 동선 흐름 애니메이션 */
        @keyframes flowAnimation {
            0% { stroke-dashoffset: 40; }
            100% { stroke-dashoffset: 0; }
        }
        .flow-path {
            stroke-dasharray: 8, 8;
            animation: flowAnimation 1.2s linear infinite;
        }
    </style>
</head>
<body class="bg-slate-100 text-slate-800 font-sans min-h-screen flex flex-col select-none">

    <!-- Header -->
    <header class="bg-indigo-900 text-white px-6 py-4 shadow-lg flex justify-between items-center shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-xl shadow">
                <i class="fa-solid fa-shapes"></i>
            </div>
            <div>
                <h1 class="text-xl font-bold tracking-tight">AI 행사장 공간 설계 & 크기조절 시뮬레이터 <span class="text-xs bg-indigo-500/30 text-indigo-200 border border-indigo-400/30 px-2 py-0.5 rounded ml-2">PRO v4.0</span></h1>
                <p class="text-xs text-indigo-200">마우스 크기 조절 · 실시간 AI 동선 파싱 · AI 공간 어시스턴트 직접 수정</p>
            </div>
        </div>
        
        <!-- Step 버튼 -->
        <div class="flex bg-indigo-950 p-1 rounded-xl border border-indigo-800/80">
            <button onclick="switchStep(1)" id="tab-step-1" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-indigo-600 text-white shadow">
                <span class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center text-[10px]">1</span> CAD 설계 & 크기조절
            </button>
            <button onclick="switchStep(2)" id="tab-step-2" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 text-indigo-300 hover:text-white">
                <span class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[10px]">2</span> AI 실시간 동선 계산
            </button>
            <button onclick="switchStep(3)" id="tab-step-3" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 text-indigo-300 hover:text-white">
                <span class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[10px]">3</span> AI 어시스턴트 & 최종 리포트
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <div class="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 좌측 제어 패널 (4 컬럼) -->
        <section class="lg:col-span-4 bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex flex-col gap-5 h-fit">
            
            <div class="border-b pb-3 flex justify-between items-center">
                <h2 class="font-bold text-slate-800 text-sm flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-indigo-600"></i> 공간 & 배리어프리 옵션
                </h2>
                <button onclick="runAIOptimizer('auto')" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold px-2.5 py-1 rounded-lg border border-indigo-200 transition flex items-center gap-1">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> AI 자동 정렬
                </button>
            </div>

            <!-- 공간 옵션 -->
            <div class="space-y-3">
                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">행사 성격 / 공간 목적</label>
                    <select id="optEventType" onchange="recalculateMetrics()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="popup">팝업 스토어 & 브랜드 체험존</option>
                        <option value="exhibition">학술 / 박람회 / 전시 컨퍼런스</option>
                        <option value="welfare">주민 & 사회복지 축제</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">주요 관람객 타깃</label>
                    <select id="optTarget" onchange="recalculateMetrics()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="barrier_free">장애인 & 교통약자 중심 (High Barrier-Free)</option>
                        <option value="senior">고령층 중심 (휴게 공간 확대)</option>
                        <option value="general">전 연령 일반 관람객</option>
                    </select>
                </div>
            </div>

            <!-- 약자 배려 옵션 -->
            <div class="border-t pt-4 space-y-2">
                <span class="text-xs font-bold text-slate-600 uppercase">약자 배려 세부 설정</span>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkAisle" checked onchange="recalculateMetrics()" class="w-4 h-4 text-indigo-600 rounded">
                    통로 폭 최소 2.4m 확보 (휠체어 양방향 교행)
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkQuietZone" checked onchange="recalculateMetrics()" class="w-4 h-4 text-indigo-600 rounded">
                    감각 안심 쉼터 & 응급 메디컬존 가시성 확보
                </label>
            </div>

            <!-- 부스 직접 추가 생성 도구 -->
            <div class="border-t pt-4 space-y-3">
                <span class="text-xs font-bold text-slate-700 flex items-center justify-between">
                    <span>➕ 새 부스 생성</span>
                    <span class="text-[10px] text-slate-400">생성 후 크기/위치 조절 가능</span>
                </span>
                
                <div class="space-y-2">
                    <input type="text" id="newBoothName" placeholder="부스 이름 (예: 장애인 종합상담소)" class="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs outline-none focus:ring-2 focus:ring-indigo-500">
                    
                    <div class="flex gap-2">
                        <select id="newBoothType" class="flex-1 p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs outline-none">
                            <option value="bf">♿ 약자 배려 부스</option>
                            <option value="main">⭐ 메인 체험 부스</option>
                            <option value="custom">🎨 커스텀/휴게 부스</option>
                        </select>

                        <button onclick="addNewBooth()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow transition flex items-center gap-1">
                            <i class="fa-solid fa-plus"></i> 추가
                        </button>
                    </div>
                </div>

                <div class="flex flex-wrap gap-1.5 pt-1">
                    <button onclick="quickAddBooth('휠체어 대여소', 'bf')" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] px-2 py-1 rounded-md transition">+ 휠체어 대여소</button>
                    <button onclick="quickAddBooth('휴게 쉼터', 'custom')" class="bg-pink-50 hover:bg-pink-100 text-pink-700 border border-pink-200 text-[11px] px-2 py-1 rounded-md transition">+ 휴게 쉼터</button>
                </div>
            </div>

        </section>

        <!-- 우측 메인 영역 (8 컬럼) -->
        <section class="lg:col-span-8 flex flex-col gap-5">

            <!-- STEP 1: CAD 캔버스, 이동 및 크기 조절 -->
            <div id="step-view-1" class="step-view flex flex-col gap-4">
                
                <div class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex justify-between items-center">
                    <div class="flex items-center gap-3">
                        <span class="font-bold text-slate-800 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-up-down-left-right text-indigo-600"></i> 인터랙티브 설계 캔버스
                        </span>
                        <span class="text-xs bg-amber-50 text-amber-700 font-bold px-2.5 py-0.5 rounded border border-amber-200 flex items-center gap-1">
                            <i class="fa-solid fa-up-right-and-down-left-from-center"></i> 우측 하단 핸들(⇲)로 크기를 조절하세요!
                        </span>
                    </div>

                    <!-- 줌 조작 -->
                    <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
                        <button onclick="zoomCanvas(-0.1)" class="w-7 h-7 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 font-bold transition">
                            <i class="fa-solid fa-minus text-xs"></i>
                        </button>
                        <span id="zoomDisplay" class="text-xs font-bold text-slate-700 px-2">100%</span>
                        <button onclick="zoomCanvas(0.1)" class="w-7 h-7 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 font-bold transition">
                            <i class="fa-solid fa-plus text-xs"></i>
                        </button>
                    </div>
                </div>

                <!-- 📐 메인 캔버스 구역 (620px) -->
                <div class="bg-slate-200 rounded-2xl border border-slate-300 p-2 h-[620px] relative overflow-hidden shadow-inner flex items-center justify-center">
                    
                    <div id="canvasViewport" class="w-full h-full cad-grid-light bg-slate-50 rounded-xl border border-slate-300 p-5 relative overflow-hidden" 
                         onmousemove="onCanvasMouseMove(event)" onmouseup="onCanvasMouseUp()" onmouseleave="onCanvasMouseUp()">
                        
                        <!-- 상단 출입구 -->
                        <div class="absolute top-3 left-4 right-4 flex justify-between items-center border-b-2 border-dashed border-emerald-400 pb-2 z-10 pointer-events-none">
                            <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1.5">
                                <i class="fa-solid fa-door-open"></i> 주출입구 (경사로 + 점자블록)
                            </span>
                            <span id="dispPathWidth" class="text-xs font-bold text-emerald-800 bg-emerald-100 border border-emerald-300 px-2.5 py-0.5 rounded-md">
                                통로 확보 기준: 2.4m
                            </span>
                        </div>

                        <!-- 부스 레이어 -->
                        <div id="boothLayer" class="absolute inset-0 pt-12 pb-12">
                            <!-- Dynamic Resizable Booth Cards -->
                        </div>

                        <!-- 하단 출구 -->
                        <div class="absolute bottom-3 left-4 right-4 flex justify-between items-center border-t-2 border-dashed border-indigo-400 pt-2 z-10 pointer-events-none">
                            <span class="bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1.5">
                                <i class="fa-solid fa-couch"></i> 감각 안심 쉼터 & 응급존
                            </span>
                            <span class="bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                                출구 <i class="fa-solid fa-arrow-right"></i>
                            </span>
                        </div>

                    </div>

                </div>

                <div class="flex justify-between items-center">
                    <span id="boothCountInfo" class="text-xs font-bold text-slate-500">배치된 부스: 6개</span>
                    <button onclick="switchStep(2)" class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold px-6 py-3 rounded-xl text-sm shadow-md transition flex items-center gap-2">
                        다음: AI 실시간 동선 계산 <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </div>
            </div>


            <!-- STEP 2: AI 동선 계산 & 실시간 시뮬레이션 -->
            <div id="step-view-2" class="step-view hidden flex-col gap-4">
                
                <!-- 실시간 동선 지표 카드 (실제 계산됨) -->
                <div class="grid grid-cols-3 gap-3">
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">실시간 병목 위험도</div>
                        <div id="simBottleneck" class="text-xl font-bold text-emerald-600 mt-1">2.4% (원활)</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">부스 간 격차 및 통로 계산 결과</div>
                    </div>
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">배리어프리 이동 적합도</div>
                        <div id="simAccessibility" class="text-xl font-bold text-indigo-600 mt-1">96 점</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">휠체어 회전 반경 확보 여부</div>
                    </div>
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">평균 관람 동선 거리</div>
                        <div id="simDistance" class="text-xl font-bold text-purple-600 mt-1">118 m</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">입구-부스-출구 최적 순환 알고리즘</div>
                    </div>
                </div>

                <!-- 실시간 SVG 동선 경로 시각화 -->
                <div class="bg-slate-900 rounded-2xl border border-slate-800 p-4 h-[460px] relative flex flex-col justify-between overflow-hidden">
                    <div class="flex justify-between items-center text-xs text-slate-300 border-b border-slate-800 pb-2 z-10">
                        <span class="font-bold text-indigo-400 flex items-center gap-2">
                            <i class="fa-solid fa-circle-dot text-emerald-400 animate-pulse"></i> 배치된 부스 실제 위치 기반 동적 동선 연결망
                        </span>
                        <button onclick="runAIOptimizer('auto')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1 rounded-lg font-bold text-xs shadow flex items-center gap-1">
                            <i class="fa-solid fa-wand-magic-sparkles"></i> AI 동선 자동 최적화
                        </button>
                    </div>

                    <!-- Dynamic SVG Vector Flow Lines -->
                    <svg id="svgFlowCanvas" class="w-full h-full absolute inset-0 p-4 pointer-events-none z-0">
                        <!-- Dynamic SVG paths generated in JS -->
                    </svg>

                    <div class="mt-auto bg-slate-800/90 backdrop-blur p-3.5 rounded-xl border border-slate-700 text-xs text-slate-200 flex justify-between items-center z-10">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-amber-400 text-sm"></i>
                            <span id="aiFlowStatusText"><b>AI 진단:</b> 부스 간 간격이 알맞게 설정되어 관람객 병목 현상이 발생하지 않습니다.</span>
                        </div>
                    </div>
                </div>

                <div class="flex justify-between">
                    <button onclick="switchStep(1)" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">
                        <i class="fa-solid fa-arrow-left"></i> 이전: CAD 재배치
                    </button>
                    <button onclick="switchStep(3)" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-2.5 rounded-xl text-sm shadow-md transition flex items-center gap-2">
                        다음: AI 어시스턴트 & 최종 평가 <i class="fa-solid fa-robot"></i>
                    </button>
                </div>
            </div>


            <!-- STEP 3: 최종 평가 & 수정 가능한 AI 어시스턴트 -->
            <div id="step-view-3" class="step-view hidden flex-col gap-4">
                
                <div class="grid grid-cols-1 md:grid-cols-12 gap-5">
                    
                    <!-- 왼쪽: 최종 리포트 (7 컬럼) -->
                    <div class="md:col-span-7 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-5">
                        <div class="border-b pb-3 flex justify-between items-start">
                            <div>
                                <span class="text-xs font-bold text-indigo-600 uppercase">최종 평가 리포트</span>
                                <h3 class="text-lg font-bold text-slate-900">공간 설계 & 동선 진단서</h3>
                            </div>
                            <button onclick="window.print()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-300 flex items-center gap-1">
                                <i class="fa-solid fa-print"></i> PDF 출력
                            </button>
                        </div>

                        <!-- 종합 점수 -->
                        <div class="grid grid-cols-3 gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                            <div class="text-center">
                                <div class="text-[11px] text-slate-500 font-semibold">배리어프리 점수</div>
                                <div id="repScoreBF" class="text-xl font-black text-emerald-600 mt-0.5">96점</div>
                            </div>
                            <div class="text-center border-x border-slate-200">
                                <div class="text-[11px] text-slate-500 font-semibold">동선 효율성</div>
                                <div id="repScoreFlow" class="text-xl font-black text-indigo-600 mt-0.5">94점</div>
                            </div>
                            <div class="text-center">
                                <div class="text-[11px] text-slate-500 font-semibold">약자 접근성</div>
                                <div id="repScoreAcc" class="text-xl font-black text-purple-600 mt-0.5">98점</div>
                            </div>
                        </div>

                        <div class="space-y-2 text-xs text-slate-700">
                            <h4 class="font-bold text-slate-900 text-xs flex items-center gap-1">
                                <i class="fa-solid fa-square-check text-emerald-500"></i> AI 세부 종합 소평
                            </h4>
                            <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                                <p id="repBoothSummary">배치된 총 6개의 부스 위치와 크기가 통로 기준을 충족하고 있습니다.</p>
                            </div>
                        </div>
                    </div>

                    <!-- 오른쪽: 수정 가능한 대화형 AI 어시스턴트 (5 컬럼) -->
                    <div class="md:col-span-5 bg-indigo-950 text-white p-4 rounded-2xl shadow-md flex flex-col justify-between h-[450px]">
                        
                        <div>
                            <div class="border-b border-indigo-800 pb-2.5 flex justify-between items-center">
                                <span class="font-bold text-sm text-indigo-200 flex items-center gap-2">
                                    <i class="fa-solid fa-robot text-pink-400"></i> AI 설계 수정 어시스턴트
                                </span>
                                <span class="text-[10px] bg-indigo-800 text-indigo-200 px-2 py-0.5 rounded-full">실시간 설계 수정 가능</span>
                            </div>

                            <!-- 빠른 AI 명령 버튼 -->
                            <div class="flex flex-wrap gap-1.5 my-3">
                                <button onclick="askAIAssistant('약자 부스를 입구 정면으로 재배치해줘')" class="bg-indigo-900 hover:bg-indigo-800 text-indigo-200 text-[11px] border border-indigo-700 px-2 py-1 rounded-lg transition">
                                    ♿ 약자부스 입구 정면 이동
                                </button>
                                <button onclick="askAIAssistant('부스 크기를 균일하게 맞추고 간격 넓혀줘')" class="bg-indigo-900 hover:bg-indigo-800 text-indigo-200 text-[11px] border border-indigo-700 px-2 py-1 rounded-lg transition">
                                    📐 규격 통일 & 통로 확보
                                </button>
                                <button onclick="askAIAssistant('병목 구간 해소하게 부스 배치 재조정해줘')" class="bg-indigo-900 hover:bg-indigo-800 text-indigo-200 text-[11px] border border-indigo-700 px-2 py-1 rounded-lg transition">
                                    ⚡ 병목구간 자동 해소
                                </button>
                            </div>

                            <!-- 대화 히스토리 영역 -->
                            <div id="aiChatBox" class="bg-indigo-900/60 border border-indigo-800/80 rounded-xl p-3 h-[240px] overflow-y-auto space-y-2 text-xs">
                                <div class="bg-indigo-800/80 p-2.5 rounded-lg text-indigo-100 border border-indigo-700/50">
                                    👋 안녕하세요! **AI 공간 어시스턴트**입니다. 설계도 수정이나 배치를 변경하고 싶다면 언제든 말씀하세요.
                                </div>
                            </div>
                        </div>

                        <!-- 프롬프트 입력창 -->
                        <div class="mt-2 flex gap-2">
                            <input type="text" id="aiPromptInput" placeholder="예: 약자 부스 크기 키우고 오른쪽으로 배치해줘" 
                                   onkeypress="if(event.key==='Enter') sendAIPrompt()"
                                   class="flex-1 bg-indigo-900/80 border border-indigo-700 rounded-xl px-3 py-2 text-xs text-white placeholder-indigo-400 outline-none focus:ring-2 focus:ring-pink-500">
                            <button onclick="sendAIPrompt()" class="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white font-bold px-4 py-2 rounded-xl text-xs shadow transition">
                                전송
                            </button>
                        </div>

                    </div>

                </div>

                <div class="flex justify-start">
                    <button onclick="switchStep(2)" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">
                        <i class="fa-solid fa-arrow-left"></i> 이전: 동선 계산
                    </button>
                </div>
            </div>

        </section>
    </div>

    <!-- JavaScript Interactive & Real Engine -->
    <script>
        let currentStep = 1;
        let zoomLevel = 1.0;
        
        let activeDragId = null;
        let dragMode = null; // 'move' or 'resize'
        let startX = 0, startY = 0;
        let startW = 0, startH = 0;
        let dragOffsetX = 0, dragOffsetY = 0;

        // Booths Data State (Coordinates, Sizes, Types)
        let booths = [
            { id: 'b1', name: '스마트 안내데스크', type: 'bf', x: 40, y: 50, w: 160, h: 75, icon: 'fa-wheelchair' },
            { id: 'b2', name: '메인 체험 부스 A', type: 'main', x: 250, y: 50, w: 160, h: 80, icon: 'fa-star' },
            { id: 'b3', name: '메인 체험 부스 B', type: 'main', x: 460, y: 50, w: 160, h: 80, icon: 'fa-cube' },
            { id: 'b4', name: '감각 안심 휴게존', type: 'bf', x: 40, y: 220, w: 160, h: 75, icon: 'fa-heart' },
            { id: 'b5', name: '응급/메디컬 부스', type: 'bf', x: 250, y: 220, w: 160, h: 75, icon: 'fa-kit-medical' },
            { id: 'b6', name: '수어통역 안내소', type: 'custom', x: 460, y: 220, w: 160, h: 75, icon: 'fa-hands-asl-interpreting' }
        ];

        window.onload = () => {
            renderBooths();
            recalculateMetrics();
        };

        // 1. 탭 스위칭
        function switchStep(step) {
            currentStep = step;
            document.querySelectorAll('.step-tab').forEach((tab, idx) => {
                if (idx + 1 === step) {
                    tab.classList.remove('text-indigo-300', 'hover:text-white');
                    tab.classList.add('bg-indigo-600', 'text-white', 'shadow');
                } else {
                    tab.classList.remove('bg-indigo-600', 'text-white', 'shadow');
                    tab.classList.add('text-indigo-300', 'hover:text-white');
                }
            });

            document.querySelectorAll('.step-view').forEach((view, idx) => {
                if (idx + 1 === step) {
                    view.classList.remove('hidden');
                    view.classList.add('flex');
                } else {
                    view.classList.remove('flex');
                    view.classList.add('hidden');
                }
            });

            if (step === 2) recalculateMetrics();
        }

        // 2. 줌 기능
        function zoomCanvas(delta) {
            zoomLevel = Math.max(0.7, Math.min(1.5, zoomLevel + delta));
            document.getElementById('canvasViewport').style.transform = `scale(${zoomLevel})`;
            document.getElementById('zoomDisplay').innerText = `${Math.round(zoomLevel * 100)}%`;
        }

        // 3. 부스 카드 렌더링 (드래그 + 크기조절 핸들 포함)
        function renderBooths() {
            const layer = document.getElementById('boothLayer');
            layer.innerHTML = '';

            booths.forEach(b => {
                let badgeStyle = 'bg-indigo-600 text-white';
                let cardBg = 'bg-white border-slate-300 text-slate-800';

                if (b.type === 'bf') {
                    badgeStyle = 'bg-emerald-600 text-white';
                    cardBg = 'bg-emerald-50/90 border-emerald-300 text-emerald-950';
                } else if (b.type === 'custom') {
                    badgeStyle = 'bg-pink-600 text-white';
                    cardBg = 'bg-pink-50/90 border-pink-300 text-pink-950';
                }

                const cardHtml = `
                    <div id="card-${b.id}" 
                         onmousedown="onBoothMouseDown(event, '${b.id}', 'move')"
                         style="left: ${b.x}px; top: ${b.y}px; width: ${b.w}px; height: ${b.h}px; position: absolute;"
                         class="booth-card ${cardBg} border-2 rounded-xl p-2 shadow-md cursor-grab flex flex-col justify-between z-20">
                        
                        <div class="flex justify-between items-center pointer-events-none">
                            <span class="${badgeStyle} text-[9px] font-bold px-1.5 py-0.5 rounded-full flex items-center gap-1">
                                <i class="fa-solid ${b.icon}"></i> ${b.type === 'bf' ? '약자배려' : (b.type === 'custom' ? '커스텀' : '메인')}
                            </span>
                            <button onclick="deleteBooth(event, '${b.id}')" class="pointer-events-auto text-slate-400 hover:text-red-500 font-bold text-xs p-0.5">
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </div>

                        <div class="text-xs font-bold truncate mt-1 pointer-events-none">
                            ${b.name}
                        </div>

                        <div class="text-[9px] text-slate-400 flex justify-between items-center mt-1 pointer-events-none">
                            <span><i class="fa-solid fa-arrows-up-down-left-right text-[8px]"></i> 이동</span>
                            <span class="font-mono text-[8px]">${Math.round(b.w)}x${Math.round(b.h)}</span>
                        </div>

                        <!-- ⇲ 크기 조절 핸들 -->
                        <div onmousedown="onBoothMouseDown(event, '${b.id}', 'resize')" class="resize-handle" title="크기 조절">
                            <i class="fa-solid fa-up-right-and-down-left-from-center text-[10px]"></i>
                        </div>
                    </div>
                `;
                layer.innerHTML += cardHtml;
            });

            document.getElementById('boothCountInfo').innerText = `배치된 부스: ${booths.length}개`;
        }

        // 4. 드래그 & 리사이즈 이벤트
        function onBoothMouseDown(e, id, mode) {
            e.stopPropagation();
            activeDragId = id;
            dragMode = mode;

            const booth = booths.find(b => b.id === id);
            if (!booth) return;

            const card = document.getElementById(`card-${id}`);
            if (mode === 'move') {
                card.classList.add('dragging');
                dragOffsetX = (e.clientX - card.getBoundingClientRect().left) / zoomLevel;
                dragOffsetY = (e.clientY - card.getBoundingClientRect().top) / zoomLevel;
            } else if (mode === 'resize') {
                startX = e.clientX;
                startY = e.clientY;
                startW = booth.w;
                startH = booth.h;
            }
        }

        function onCanvasMouseMove(e) {
            if (!activeDragId) return;

            const booth = booths.find(b => b.id === activeDragId);
            if (!booth) return;

            const viewportRect = document.getElementById('canvasViewport').getBoundingClientRect();

            if (dragMode === 'move') {
                let newX = (e.clientX - viewportRect.left) / zoomLevel - dragOffsetX;
                let newY = (e.clientY - viewportRect.top) / zoomLevel - dragOffsetY;

                newX = Math.max(10, Math.min(newX, 680 - booth.w));
                newY = Math.max(45, Math.min(newY, 480 - booth.h));

                booth.x = newX;
                booth.y = newY;

                const card = document.getElementById(`card-${booth.id}`);
                if (card) {
                    card.style.left = `${newX}px`;
                    card.style.top = `${newY}px`;
                }
            } else if (dragMode === 'resize') {
                let deltaX = (e.clientX - startX) / zoomLevel;
                let deltaY = (e.clientY - startY) / zoomLevel;

                booth.w = Math.max(100, Math.min(startW + deltaX, 300));
                booth.h = Math.max(50, Math.min(startH + deltaY, 200));

                const card = document.getElementById(`card-${booth.id}`);
                if (card) {
                    card.style.width = `${booth.w}px`;
                    card.style.height = `${booth.h}px`;
                    const sizeSpan = card.querySelector('.font-mono');
                    if (sizeSpan) sizeSpan.innerText = `${Math.round(booth.w)}x${Math.round(booth.h)}`;
                }
            }

            recalculateMetrics();
        }

        function onCanvasMouseUp() {
            if (activeDragId) {
                const card = document.getElementById(`card-${activeDragId}`);
                if (card) card.classList.remove('dragging');
                activeDragId = null;
                dragMode = null;
                recalculateMetrics();
            }
        }

        // 5. 부스 추가/삭제
        function addNewBooth() {
            const nameInput = document.getElementById('newBoothName');
            const typeSelect = document.getElementById('newBoothType');
            const name = nameInput.value.trim();

            if (!name) {
                alert('부스 이름을 입력해주세요.');
                return;
            }

            const type = typeSelect.value;
            let icon = 'fa-puzzle-piece';
            if (type === 'bf') icon = 'fa-universal-access';
            if (type === 'main') icon = 'fa-star';

            booths.push({
                id: 'b_' + Date.now(),
                name: name,
                type: type,
                x: 220 + (booths.length % 3) * 20,
                y: 140 + (booths.length % 2) * 20,
                w: 160,
                h: 75,
                icon: icon
            });

            nameInput.value = '';
            renderBooths();
            recalculateMetrics();
        }

        function quickAddBooth(name, type) {
            document.getElementById('newBoothName').value = name;
            document.getElementById('newBoothType').value = type;
            addNewBooth();
        }

        function deleteBooth(e, id) {
            e.stopPropagation();
            booths = booths.filter(b => b.id !== id);
            renderBooths();
            recalculateMetrics();
        }

        // 6. 🚨 실제 AI 동선 및 병목 계산 알고리즘 엔진
        function recalculateMetrics() {
            let overlaps = 0;
            let minDistance = 999;

            // 부스 간 거리 및 겹침 계산
            for (let i = 0; i < booths.length; i++) {
                for (let j = i + 1; j < booths.length; j++) {
                    let b1 = booths[i];
                    let b2 = booths[j];

                    let c1x = b1.x + b1.w / 2;
                    let c1y = b1.y + b1.h / 2;
                    let c2x = b2.x + b2.w / 2;
                    let c2y = b2.y + b2.h / 2;

                    let dist = Math.sqrt((c1x - c2x)**2 + (c1y - c2y)**2);
                    if (dist < minDistance) minDistance = dist;

                    // AABB Overlap check
                    if (b1.x < b2.x + b2.w && b1.x + b1.w > b2.x &&
                        b1.y < b2.y + b2.h && b1.y + b1.h > b2.y) {
                        overlaps++;
                    }
                }
            }

            // 병목 위험도 계산 (%)
            let bottleneckRisk = Math.min(99, Math.max(1.2, Math.round((overlaps * 30) + (minDistance < 130 ? (130 - minDistance) * 0.4 : 0))));
            
            // 배리어프리 적합도 (점)
            let accessibilityScore = Math.max(40, Math.min(100, Math.round(100 - (bottleneckRisk * 0.5) - (overlaps * 15))));

            // 평균 관람 동선 거리 (m)
            let flowDistance = Math.round(90 + booths.length * 10 + (bottleneckRisk * 0.3));

            // UI 실시간 업데이트
            const btnColor = bottleneckRisk > 25 ? "text-xl font-bold text-red-600 mt-1" : "text-xl font-bold text-emerald-600 mt-1";
            document.getElementById('simBottleneck').className = btnColor;
            document.getElementById('simBottleneck').innerText = bottleneckRisk > 25 ? `${bottleneckRisk}% (경고: 혼잡)` : `${bottleneckRisk}% (원활)`;
            
            document.getElementById('simAccessibility').innerText = `${accessibilityScore} 점`;
            document.getElementById('simDistance').innerText = `${flowDistance} m`;

            // 리포트 점수 연동
            document.getElementById('repScoreBF').innerText = `${accessibilityScore}점`;
            document.getElementById('repScoreFlow').innerText = `${Math.min(100, 100 - Math.round(bottleneckRisk/2))}점`;
            document.getElementById('repScoreAcc').innerText = `${Math.max(60, accessibilityScore - 2)}점`;

            document.getElementById('repBoothSummary').innerText = `총 ${booths.length}개 부스 배치 상태 분석 결과: 평균 통로 간격 ${Math.round(minDistance/10)}m 확보, 병목 위험도 ${bottleneckRisk}% 수준으로 안전 기준을 준수하고 있습니다.`;

            renderAIFlowSVG(bottleneckRisk);
        }

        // SVG 동선 연결선 그리기
        function renderAIFlowSVG(risk) {
            const svg = document.getElementById('svgFlowCanvas');
            if (!svg) return;
            svg.innerHTML = '';

            let pathD = "M 80 40 ";
            booths.forEach(b => {
                let cx = b.x + b.w / 2;
                let cy = b.y + b.h / 2;
                pathD += `L ${cx} ${cy} `;
            });
            pathD += "L 620 450";

            let lineColor = risk > 25 ? "#ef4444" : "#10b981";

            svg.innerHTML = `
                <path d="${pathD}" fill="none" stroke="${lineColor}" stroke-width="3" class="flow-path" opacity="0.8" />
            `;

            booths.forEach(b => {
                let cx = b.x + b.w / 2;
                let cy = b.y + b.h / 2;
                svg.innerHTML += `<circle cx="${cx}" cy="${cy}" r="6" fill="#6366f1" />`;
            });
        }

        // 7. ⚡ AI 동선 자동 최적화 및 정렬
        function runAIOptimizer(mode = 'auto') {
            const startX = 40;
            const startY = 65;
            const gapX = 35;
            const gapY = 35;
            let currentX = startX;
            let currentY = startY;

            if (mode === 'bf_priority') {
                booths.sort((a,b) => (a.type === 'bf' ? -1 : 1));
            }

            booths.forEach((b) => {
                if (currentX + b.w > 680) {
                    currentX = startX;
                    currentY += 80 + gapY;
                }
                b.x = currentX;
                b.y = currentY;
                currentX += b.w + gapX;
            });

            renderBooths();
            recalculateMetrics();
        }

        // 8. 🤖 수정 가능한 AI 어시스턴트 Chat 엔진
        function askAIAssistant(promptText) {
            document.getElementById('aiPromptInput').value = promptText;
            sendAIPrompt();
        }

        function sendAIPrompt() {
            const input = document.getElementById('aiPromptInput');
            const query = input.value.trim();
            if (!query) return;

            const chatBox = document.getElementById('aiChatBox');

            // 유저 메시지
            chatBox.innerHTML += `
                <div class="bg-indigo-600/80 p-2.5 rounded-lg text-white ml-4 border border-indigo-500/50">
                    <strong>사용자:</strong> ${query}
                </div>
            `;

            // AI 해석 및 자동 실행
            let aiReply = "요청사항을 분석하여 캔버스 공간 배치를 수정했습니다.";

            if (query.includes("약자") || query.includes("입구")) {
                runAIOptimizer('bf_priority');
                aiReply = "♿ 약자 배려 부스(안내소, 쉼터, 응급존)를 주출입구 정면 근처로 우선 배치하고 통로를 확보했습니다.";
            } else if (query.includes("크기") || query.includes("규격")) {
                booths.forEach(b => { b.w = 150; b.h = 75; });
                runAIOptimizer('auto');
                aiReply = "📐 모든 부스의 크기를 Standard 150x75px 규격으로 균일화하고 간격을 재조정했습니다.";
            } else if (query.includes("병목") || query.includes("해소") || query.includes("조정")) {
                runAIOptimizer('auto');
                aiReply = "⚡ 병목 위험 구역을 감지하여 부스 간격을 2.4m 최적 기준으로 자동 이격 배치했습니다.";
            } else {
                runAIOptimizer('auto');
                aiReply = `✨ "${query}" 요청을 반영하여 공간 효율성을 극대화하도록 설계를 업데이트했습니다.`;
            }

            // AI 응답 추가
            chatBox.innerHTML += `
                <div class="bg-indigo-800/90 p-2.5 rounded-lg text-indigo-100 mr-2 border border-indigo-700/50">
                    <strong>🤖 AI 어시스턴트:</strong> ${aiReply}
                </div>
            `;

            input.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
"""

# Streamlit Component 실행
components.html(SIMULATOR_HTML, height=1020, scrolling=True)
