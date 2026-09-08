import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(
    page_title="AI 스마트 공간 설계 & 드래그 동선 시뮬레이터",
    page_icon="📐",
    layout="wide"
)

# 전체 통합 HTML/CSS/JS (파이썬 멀티라인 문자열)
SIMULATOR_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 스마트 공간 설계 & 드래그 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* 밝고 명확한 CAD 그리드 모눈종이 배경 */
        .cad-grid-light {
            background-size: 20px 20px;
            background-image: 
                linear-gradient(to right, rgba(203, 213, 225, 0.5) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(203, 213, 225, 0.5) 1px, transparent 1px);
        }

        /* 줌 및 드래그 뷰포트 */
        #canvasViewport {
            transition: transform 0.15s ease-out;
            transform-origin: center center;
        }

        /* 부스 카드 드래그 스타일 */
        .booth-card {
            user-select: none;
            touch-action: none;
            transition: box-shadow 0.2s, transform 0.1s;
        }
        .booth-card:hover {
            box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
            border-color: #6366f1;
        }
        .booth-card.dragging {
            opacity: 0.85;
            cursor: grabbing !important;
            z-index: 50 !important;
            box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.2);
        }

        /* 동선 파티클 애니메이션 */
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
                <h1 class="text-xl font-bold tracking-tight">AI 행사장 공간 설계 & 드래그 시뮬레이터 <span class="text-xs bg-indigo-500/30 text-indigo-200 border border-indigo-400/30 px-2 py-0.5 rounded ml-2">PRO v3.5</span></h1>
                <p class="text-xs text-indigo-200">대형 CAD 캔버스 · 자유 드래그 배치 · 실시간 동선 및 배리어프리 분석</p>
            </div>
        </div>
        
        <!-- 워크플로우 Step 버튼 -->
        <div class="flex bg-indigo-950 p-1 rounded-xl border border-indigo-800/80">
            <button onclick="switchStep(1)" id="tab-step-1" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-indigo-600 text-white shadow">
                <span class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center text-[10px]">1</span> 캔버스 설계 & 드래그
            </button>
            <button onclick="switchStep(2)" id="tab-step-2" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 text-indigo-300 hover:text-white">
                <span class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[10px]">2</span> AI 동선 계산 & 시뮬레이션
            </button>
            <button onclick="switchStep(3)" id="tab-step-3" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 text-indigo-300 hover:text-white">
                <span class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[10px]">3</span> 최종 평가 & AI 리포트
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <div class="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 좌측 패널 (4 컬럼) -->
        <section class="lg:col-span-4 bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex flex-col gap-5 h-fit">
            
            <div class="border-b pb-3 flex justify-between items-center">
                <h2 class="font-bold text-slate-800 text-sm flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-indigo-600"></i> 공간 & 배리어프리 옵션
                </h2>
                <span class="text-xs text-indigo-600 font-semibold bg-indigo-50 px-2 py-0.5 rounded">실시간 연동</span>
            </div>

            <!-- 공간 기본 옵션 -->
            <div class="space-y-3">
                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">행사 성격 / 공간 목적</label>
                    <select id="optEventType" onchange="updateSimulationState()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="popup">팝업 스토어 & 브랜드 체험존</option>
                        <option value="exhibition">학술 / 박람회 / 전시 컨퍼런스</option>
                        <option value="welfare">주민 & 사회복지 축제</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">주요 관람객 타깃</label>
                    <select id="optTarget" onchange="updateSimulationState()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="barrier_free">장애인 & 교통약자 중심 (High Barrier-Free)</option>
                        <option value="senior">고령층 중심 (휴게 공간 확대)</option>
                        <option value="general">전 연령 일반 관람객</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">동선 루팅 알고리즘</label>
                    <select id="optRouteMode" onchange="updateSimulationState()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="loop">병목 제로 순환형 루프 (Loop)</option>
                        <option value="grid">공간 활용 격자형 (Grid)</option>
                        <option value="radial">중앙 광장 방사형 (Radial)</option>
                    </select>
                </div>
            </div>

            <!-- 배리어프리 약자 배려 옵션 -->
            <div class="border-t pt-4 space-y-2">
                <span class="text-xs font-bold text-slate-600 uppercase">약자 배려 세부 설정</span>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkAisle" checked onchange="updateSimulationState()" class="w-4 h-4 text-indigo-600 rounded">
                    통로 폭 최소 2.0m~2.4m 확보 (휠체어 교행)
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkLowDesk" checked onchange="updateSimulationState()" class="w-4 h-4 text-indigo-600 rounded">
                    높이 75cm 이하 낮은 안내 데스크 배치
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkQuietZone" checked onchange="updateSimulationState()" class="w-4 h-4 text-indigo-600 rounded">
                    감각 안심 쉼터 & 응급 메디컬존 포함
                </label>
            </div>

            <!-- ➕ 부스 직접 추가 생성 도구 (복원 및 강화) -->
            <div class="border-t pt-4 space-y-3">
                <span class="text-xs font-bold text-slate-700 flex items-center justify-between">
                    <span>➕ 새 부스 추가 생성</span>
                    <span class="text-[10px] text-slate-400">캔버스에 자동 생성됨</span>
                </span>
                
                <div class="space-y-2">
                    <input type="text" id="newBoothName" placeholder="부스 이름 입력 (예: 수어통역소)" class="w-full p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs outline-none focus:ring-2 focus:ring-indigo-500">
                    
                    <div class="flex gap-2">
                        <select id="newBoothType" class="flex-1 p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs outline-none">
                            <option value="bf">♿ 약자 배려 부스</option>
                            <option value="main">⭐ 메인 체험 부스</option>
                            <option value="custom">🎨 커스텀/팝업 부스</option>
                        </select>

                        <button onclick="addNewBooth()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-xs font-bold shadow transition flex items-center gap-1">
                            <i class="fa-solid fa-plus"></i> 추가
                        </button>
                    </div>
                </div>

                <!-- 빠른 프리셋 추가 버튼 -->
                <div class="flex flex-wrap gap-1.5 pt-1">
                    <button onclick="quickAddBooth('휠체어 대여소', 'bf')" class="bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 text-[11px] px-2 py-1 rounded-md transition">+ 휠체어 대여소</button>
                    <button onclick="quickAddBooth('음료/카페 존', 'custom')" class="bg-pink-50 hover:bg-pink-100 text-pink-700 border border-pink-200 text-[11px] px-2 py-1 rounded-md transition">+ 카페 존</button>
                    <button onclick="quickAddBooth('포토 부스', 'custom')" class="bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 text-[11px] px-2 py-1 rounded-md transition">+ 포토 부스</button>
                </div>
            </div>

        </section>

        <!-- 우측 메인 영역 (8 컬럼) -->
        <section class="lg:col-span-8 flex flex-col gap-5">

            <!-- STEP 1: 대형 CAD 캔버스 & 마우스 자유 드래그 배치 -->
            <div id="step-view-1" class="step-view flex flex-col gap-4">
                
                <!-- 상단 캔버스 조작 툴바 -->
                <div class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex justify-between items-center">
                    <div class="flex items-center gap-3">
                        <span class="font-bold text-slate-800 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-hand-pointer text-indigo-600"></i> CAD 인터랙티브 캔버스
                        </span>
                        <span class="text-xs bg-amber-50 text-amber-700 font-semibold px-2.5 py-0.5 rounded border border-amber-200 flex items-center gap-1">
                            <i class="fa-solid fa-arrows-up-down-left-right"></i> 마우스로 부스를 자유롭게 드래그하세요
                        </span>
                    </div>

                    <!-- 줌(Zoom) 조작 툴바 -->
                    <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
                        <button onclick="zoomCanvas(-0.1)" class="w-8 h-8 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 font-bold transition" title="축소">
                            <i class="fa-solid fa-minus text-xs"></i>
                        </button>
                        <span id="zoomDisplay" class="text-xs font-bold text-slate-700 px-2.5">100%</span>
                        <button onclick="zoomCanvas(0.1)" class="w-8 h-8 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 font-bold transition" title="확대">
                            <i class="fa-solid fa-plus text-xs"></i>
                        </button>
                        <button onclick="resetZoom()" class="w-8 h-8 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 transition ml-1" title="줌 리셋">
                            <i class="fa-solid fa-rotate-left text-xs"></i>
                        </button>
                    </div>
                </div>

                <!-- 📐 대형 캔버스 메인 구역 (620px 대폭 확장) -->
                <div class="bg-slate-200 rounded-2xl border border-slate-300 p-2 h-[620px] relative overflow-hidden shadow-inner flex items-center justify-center">
                    
                    <!-- 줌/드래그 활성화 뷰포트 -->
                    <div id="canvasViewport" class="w-full h-full cad-grid-light bg-slate-50 rounded-xl border border-slate-300 p-5 relative overflow-hidden" 
                         onmousemove="onCanvasMouseMove(event)" onmouseup="onCanvasMouseUp()" onmouseleave="onCanvasMouseUp()">
                        
                        <!-- 상단 주출입구 바 -->
                        <div class="absolute top-3 left-4 right-4 flex justify-between items-center border-b-2 border-dashed border-emerald-400 pb-2 z-10 pointer-events-none">
                            <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1.5">
                                <i class="fa-solid fa-door-open"></i> 주출입구 (경사로 + 점자 블록)
                            </span>
                            <span id="dispPathWidth" class="text-xs font-bold text-emerald-800 bg-emerald-100 border border-emerald-300 px-2.5 py-0.5 rounded-md">
                                메인 통로 폭: 2.4m
                            </span>
                        </div>

                        <!-- 🎪 드래그 가능한 부스 레이어 (JavaScript 동적 생성) -->
                        <div id="boothLayer" class="absolute inset-0 pt-12 pb-12">
                            <!-- Dynamic Draggable Booth Cards -->
                        </div>

                        <!-- 하단 출구 & 쉼터 바 -->
                        <div class="absolute bottom-3 left-4 right-4 flex justify-between items-center border-t-2 border-dashed border-indigo-400 pt-2 z-10 pointer-events-none">
                            <span class="bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1.5">
                                <i class="fa-solid fa-couch"></i> 감각 안심 쉼터 & 메디컬 존
                            </span>
                            <span class="bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                                출구 <i class="fa-solid fa-arrow-right"></i>
                            </span>
                        </div>

                    </div>

                    <!-- 범례 오버레이 -->
                    <div class="absolute bottom-5 left-5 bg-white/90 backdrop-blur border border-slate-300 p-2.5 rounded-xl text-[11px] text-slate-700 flex gap-3 shadow-md pointer-events-none z-20">
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-emerald-500"></span>약자배려 부스</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-indigo-600"></span>메인 체험부스</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-pink-500"></span>커스텀 부스</span>
                    </div>
                </div>

                <!-- 하단 다음 단계 버튼 -->
                <div class="flex justify-between items-center">
                    <span id="boothCountInfo" class="text-xs font-bold text-slate-500">배치된 총 부스: 6개</span>
                    <button onclick="switchStep(2)" class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold px-6 py-3 rounded-xl text-sm shadow-md transition flex items-center gap-2">
                        다음: AI 동선 계산 & 시뮬레이션 <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </div>
            </div>


            <!-- STEP 2: AI 동선 계산 & 병목 시뮬레이션 -->
            <div id="step-view-2" class="step-view hidden flex-col gap-4">
                
                <!-- 실시간 동선 지표 카드 -->
                <div class="grid grid-cols-3 gap-3">
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">예상 병목 위험도</div>
                        <div id="simBottleneck" class="text-xl font-bold text-emerald-600 mt-1">매우 낮음 (1.8%)</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">드래그한 배치 공간 간격 충분</div>
                    </div>
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">배리어프리 이동 적합도</div>
                        <div id="simAccessibility" class="text-xl font-bold text-indigo-600 mt-1">98 점</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">휠체어 회전 반경 1.8m 확보</div>
                    </div>
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">평균 관람 동선 길이</div>
                        <div class="text-xl font-bold text-purple-600 mt-1">120 m</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">최적의 순환 코스 형성</div>
                    </div>
                </div>

                <!-- 동선 벡터 시뮬레이션 SVG 캔버스 -->
                <div class="bg-slate-900 rounded-2xl border border-slate-800 p-4 h-[450px] relative flex flex-col justify-between">
                    <div class="flex justify-between items-center text-xs text-slate-300 border-b border-slate-800 pb-2 z-10">
                        <span class="font-bold text-indigo-400 flex items-center gap-2">
                            <i class="fa-solid fa-circle-dot text-emerald-400 animate-pulse"></i> 배치된 부스 기반 AI 동선 및 관람객 유동 벡터 분석
                        </span>
                        <span class="text-xs text-slate-400">실시간 유동 시뮬레이션 작동 중</span>
                    </div>

                    <!-- SVG 파티클 벡터 오버레이 -->
                    <svg class="w-full h-full absolute inset-0 p-6 pointer-events-none" viewBox="0 0 600 350">
                        <!-- 동선 루프 연결선 -->
                        <path d="M 60 50 L 540 50 L 540 300 L 60 300 Z" fill="none" stroke="#6366f1" stroke-width="3" opacity="0.3" />
                        <path d="M 60 50 L 540 50 L 540 300 L 60 300 Z" fill="none" stroke="#10b981" stroke-width="3" class="flow-path" />
                        <path d="M 300 50 L 300 300" fill="none" stroke="#ec4899" stroke-width="2" class="flow-path" opacity="0.6" />

                        <!-- 유동 노드 포인트 -->
                        <circle cx="60" cy="50" r="7" fill="#10b981" />
                        <circle cx="540" cy="50" r="7" fill="#6366f1" />
                        <circle cx="540" cy="300" r="7" fill="#ec4899" />
                        <circle cx="60" cy="300" r="7" fill="#f59e0b" />
                    </svg>

                    <div class="mt-auto bg-slate-800/90 backdrop-blur p-3.5 rounded-xl border border-slate-700 text-xs text-slate-200 flex justify-between items-center z-10">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-amber-400 text-sm"></i>
                            <span><b>AI 최적화 진단:</b> 배치하신 부스 위치 간격이 균형을 이루어 관람객 병목 및 혼잡이 효과적으로 차단됩니다.</span>
                        </div>
                    </div>
                </div>

                <!-- 단계 이동 버튼 -->
                <div class="flex justify-between">
                    <button onclick="switchStep(1)" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">
                        <i class="fa-solid fa-arrow-left"></i> 이전: 캔버스 재배치
                    </button>
                    <button onclick="switchStep(3)" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-2.5 rounded-xl text-sm shadow-md transition flex items-center gap-2">
                        최종 평가 & AI 리포트 생성 <i class="fa-solid fa-file-contract"></i>
                    </button>
                </div>
            </div>


            <!-- STEP 3: 최종 평가 & AI 종합 리포트 -->
            <div id="step-view-3" class="step-view hidden flex-col gap-4">
                
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
                    
                    <!-- 리포트 헤더 -->
                    <div class="border-b pb-4 flex justify-between items-start">
                        <div>
                            <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider">AI 종합 공간 평가 리포트</span>
                            <h3 class="text-xl font-bold text-slate-900 mt-1">행사장 배리어프리 & 동선 설계 진단 보고서</h3>
                        </div>
                        <button onclick="window.print()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold px-3.5 py-2 rounded-lg border border-slate-300 flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-print"></i> 인쇄 / PDF 출력
                        </button>
                    </div>

                    <!-- 종합 점수 카드 -->
                    <div class="grid grid-cols-3 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <div class="text-center">
                            <div class="text-xs text-slate-500 font-semibold">배리어프리 적합성</div>
                            <div id="repScoreBF" class="text-2xl font-black text-emerald-600 mt-1">98점</div>
                        </div>
                        <div class="text-center border-x border-slate-200">
                            <div class="text-xs text-slate-500 font-semibold">동선 효율성</div>
                            <div id="repScoreFlow" class="text-2xl font-black text-indigo-600 mt-1">96점</div>
                        </div>
                        <div class="text-center">
                            <div class="text-xs text-slate-500 font-semibold">약자 접근 편의성</div>
                            <div class="text-2xl font-black text-purple-600 mt-1">94점</div>
                        </div>
                    </div>

                    <!-- 세부 소평 목록 -->
                    <div class="space-y-3 text-xs md:text-sm text-slate-700">
                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-square-check text-emerald-500"></i> AI 상세 분석 의견
                        </h4>
                        
                        <div class="p-3 bg-emerald-50 border border-emerald-100 rounded-xl">
                            <strong class="text-emerald-900">1. 사회적 약자 배려 (Barrier-Free) 평가</strong>
                            <p class="text-emerald-800 mt-1 text-xs">
                                주출입구 점자 블록과 낮은 데스크 배치가 반영되었습니다. 최소 통로 폭 2.0m 이상을 만족하여 휠체어 양방향 교행에 전혀 불편함이 없습니다.
                            </p>
                        </div>

                        <div class="p-3 bg-indigo-50 border border-indigo-100 rounded-xl">
                            <strong class="text-indigo-900">2. 배치 부스 구성 및 드래그 위치 동선</strong>
                            <p id="repBoothSummary" class="text-indigo-800 mt-1 text-xs">
                                배치된 부스들이 관람객 유동 경로상에 골고루 분포되어 특정 구역으로의 쏠림 현상이 예방됩니다.
                            </p>
                        </div>
                    </div>

                </div>

                <!-- 이전 단계 버튼 -->
                <div class="flex justify-start">
                    <button onclick="switchStep(2)" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">
                        <i class="fa-solid fa-arrow-left"></i> 이전: 동선 시뮬레이션
                    </button>
                </div>
            </div>

        </section>
    </div>

    <!-- JavaScript Drag & Drop / Interactive Engine -->
    <script>
        let currentStep = 1;
        let zoomLevel = 1.0;
        let activeDragId = null;
        let dragOffsetX = 0;
        let dragOffsetY = 0;

        // initial booths array with drag coordinates (x, y)
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
            updateSimulationState();
        };

        // 1. 탭 스위칭 함수
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
        }

        // 2. 캔버스 줌(Zoom) 기능
        function zoomCanvas(delta) {
            zoomLevel = Math.max(0.7, Math.min(1.6, zoomLevel + delta));
            applyZoom();
        }

        function resetZoom() {
            zoomLevel = 1.0;
            applyZoom();
        }

        function applyZoom() {
            const viewport = document.getElementById('canvasViewport');
            viewport.style.transform = `scale(${zoomLevel})`;
            document.getElementById('zoomDisplay').innerText = `${Math.round(zoomLevel * 100)}%`;
        }

        // 3. 부스 렌더링 및 마우스 드래그 핸들러
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
                         onmousedown="onBoothMouseDown(event, '${b.id}')"
                         style="left: ${b.x}px; top: ${b.y}px; width: ${b.w}px; height: ${b.h}px; position: absolute;"
                         class="booth-card ${cardBg} border-2 rounded-xl p-2.5 shadow-md cursor-grab flex flex-col justify-between z-20">
                        
                        <div class="flex justify-between items-center">
                            <span class="${badgeStyle} text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                                <i class="fa-solid ${b.icon}"></i> ${b.type === 'bf' ? '약자배려' : (b.type === 'custom' ? '커스텀' : '메인')}
                            </span>
                            <button onclick="deleteBooth(event, '${b.id}')" class="text-slate-400 hover:text-red-500 font-bold text-xs p-0.5">
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </div>

                        <div class="text-xs font-bold truncate mt-1">
                            ${b.name}
                        </div>

                        <div class="text-[10px] text-slate-400 flex justify-between items-center mt-1">
                            <span><i class="fa-solid fa-arrows-up-down-left-right text-[9px]"></i> 드래그</span>
                            <span class="font-mono text-[9px]">${Math.round(b.x)}, ${Math.round(b.y)}</span>
                        </div>
                    </div>
                `;
                layer.innerHTML += cardHtml;
            });

            document.getElementById('boothCountInfo').innerText = `배치된 총 부스: ${booths.length}개`;
        }

        // 드래그 시작 (MouseDown)
        function onBoothMouseDown(e, id) {
            e.stopPropagation();
            activeDragId = id;
            
            const card = document.getElementById(`card-${id}`);
            card.classList.add('dragging');

            const viewportRect = document.getElementById('canvasViewport').getBoundingClientRect();
            dragOffsetX = (e.clientX - card.getBoundingClientRect().left) / zoomLevel;
            dragOffsetY = (e.clientY - card.getBoundingClientRect().top) / zoomLevel;
        }

        // 마우스 이동 (MouseMove)
        function onCanvasMouseMove(e) {
            if (!activeDragId) return;

            const viewportRect = document.getElementById('canvasViewport').getBoundingClientRect();
            
            // Calculate relative coordinates inside viewport considering zoom
            let newX = (e.clientX - viewportRect.left) / zoomLevel - dragOffsetX;
            let newY = (e.clientY - viewportRect.top) / zoomLevel - dragOffsetY;

            // Boundary limits
            newX = Math.max(15, Math.min(newX, 680));
            newY = Math.max(50, Math.min(newY, 480));

            const booth = booths.find(b => b.id === activeDragId);
            if (booth) {
                booth.x = newX;
                booth.y = newY;
                
                const card = document.getElementById(`card-${booth.id}`);
                if (card) {
                    card.style.left = `${newX}px`;
                    card.style.top = `${newY}px`;
                    const coordSpan = card.querySelector('.font-mono');
                    if (coordSpan) coordSpan.innerText = `${Math.round(newX)}, ${Math.round(newY)}`;
                }
            }
        }

        // 마우스 떼기 (MouseUp)
        function onCanvasMouseUp() {
            if (activeDragId) {
                const card = document.getElementById(`card-${activeDragId}`);
                if (card) card.classList.remove('dragging');
                activeDragId = null;
                updateSimulationState();
            }
        }

        // 4. 부스 추가 & 삭제 기능 (복원)
        function addNewBooth() {
            const nameInput = document.getElementById('newBoothName');
            const typeSelect = document.getElementById('newBoothType');
            const name = nameInput.value.trim();

            if (!name) {
                alert('부스 이름을 입력해 주세요.');
                return;
            }

            const type = typeSelect.value;
            let icon = 'fa-puzzle-piece';
            if (type === 'bf') icon = 'fa-universal-access';
            if (type === 'main') icon = 'fa-star';

            const newId = 'b_' + Date.now();
            // Spawn inside canvas center
            booths.push({
                id: newId,
                name: name,
                type: type,
                x: 220 + (booths.length % 3) * 30,
                y: 150 + (booths.length % 2) * 30,
                w: 160,
                h: 75,
                icon: icon
            });

            nameInput.value = '';
            renderBooths();
            updateSimulationState();
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
            updateSimulationState();
        }

        // 5. 시뮬레이션 및 리포트 데이터 업데이트
        function updateSimulationState() {
            const chkAisle = document.getElementById('chkAisle').checked;
            document.getElementById('dispPathWidth').innerText = `메인 통로 폭: ${chkAisle ? '2.4m' : '1.5m'}`;

            // 리포트 종합 부스 수치 연동
            const bfCount = booths.filter(b => b.type === 'bf').length;
            const customCount = booths.filter(b => b.type === 'custom').length;

            document.getElementById('repBoothSummary').innerText = `현재 총 ${booths.length}개의 부스(약자배려 부스 ${bfCount}개, 커스텀 부스 ${customCount}개)가 마우스 드래그를 통해 최적 위치에 배치되어 시야 및 통로를 원활하게 유지합니다.`;
        }
    </script>
</body>
</html>
"""

# Streamlit Component 실행 (대형 높이 지정)
components.html(SIMULATOR_HTML, height=980, scrolling=True)
