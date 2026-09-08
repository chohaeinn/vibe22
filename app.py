import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 레이아웃 설정
st.set_page_config(
    page_title="AI 행사장 설계 & 동선 시뮬레이터 Pro",
    page_icon="📐",
    layout="wide"
)

# 전체 시스템 통합 HTML/CSS/JS (파이썬 멀티라인 문자열)
SIMULATOR_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 행사장 스마트 공간 설계 & 동선 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CAD 모눈종이 그리드 배경 */
        .cad-grid {
            background-size: 25px 25px;
            background-image: 
                linear-gradient(to right, rgba(226, 232, 240, 0.8) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(226, 232, 240, 0.8) 1px, transparent 1px);
        }
        /* 줌 캔버스 트랜지션 */
        #canvasViewport {
            transition: transform 0.2s ease-out;
            transform-origin: center center;
        }
        /* 유동 파티클 애니메이션 */
        @keyframes flowDots {
            0% { stroke-dashoffset: 40; }
            100% { stroke-dashoffset: 0; }
        }
        .flow-line {
            stroke-dasharray: 8, 8;
            animation: flowDots 1.2s linear infinite;
        }
    </style>
</head>
<body class="bg-slate-100 text-slate-800 font-sans min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-slate-900 text-white px-6 py-4 shadow-md flex justify-between items-center shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-pink-500 flex items-center justify-center text-white font-bold text-xl">
                <i class="fa-solid fa-drafting-compass"></i>
            </div>
            <div>
                <h1 class="text-xl font-bold tracking-tight">AI 행사장 설계 & 동선 최적화 시스템 <span class="text-xs bg-indigo-500/30 text-indigo-300 border border-indigo-400/30 px-2 py-0.5 rounded ml-2">PRO v3.0</span></h1>
                <p class="text-xs text-slate-400">Barrier-Free 스마트 공간 배치 · 동선 병목 시뮬레이션 · 자동 평가 리포트</p>
            </div>
        </div>
        
        <!-- 단계별 워크플로우 네비게이션 탭 -->
        <div class="flex bg-slate-800 p-1 rounded-xl border border-slate-700">
            <button onclick="switchStep(1)" id="tab-step-1" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 bg-indigo-600 text-white shadow">
                <span class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center text-[10px]">1</span> 공간 설계 & 줌(Zoom)
            </button>
            <button onclick="switchStep(2)" id="tab-step-2" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white">
                <span class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[10px]">2</span> 동선 계산 & 시뮬레이션
            </button>
            <button onclick="switchStep(3)" id="tab-step-3" class="step-tab px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-2 text-slate-400 hover:text-white">
                <span class="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center text-[10px]">3</span> 최종 평가 & AI 리포트
            </button>
        </div>
    </header>

    <!-- Main Content Container -->
    <div class="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 좌측 옵션 & 컨트롤 패널 (4 컬럼) -->
        <section class="lg:col-span-4 bg-white rounded-2xl shadow-sm border border-slate-200 p-5 flex flex-col gap-5 h-fit">
            
            <div class="border-b pb-3 flex justify-between items-center">
                <h2 class="font-bold text-slate-800 flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-indigo-600"></i> 공간 & 환경 옵션
                </h2>
                <span class="text-xs text-slate-400">설정 후 자동 반영</span>
            </div>

            <!-- 공간 기본 프리셋 -->
            <div class="space-y-3">
                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">행사 성격 / 목적</label>
                    <select id="optEventType" onchange="updateDesign()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="exhibition">학술 / 박람회 / 전시 컨퍼런스</option>
                        <option value="popup">체험형 팝업스토어 & 브랜드 존</option>
                        <option value="welfare">주민 & 사회복지 축제</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">주요 타깃 관람객 (약자 배려)</label>
                    <select id="optTarget" onchange="updateDesign()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="barrier_free">휠체어/교통약자 중심 (최고 배리어프리)</option>
                        <option value="senior">고령층 중심 (휴게 공간 확대)</option>
                        <option value="general">전 연령 일반 관람객</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-600 mb-1">동선 루팅 알고리즘</label>
                    <select id="optRouteMode" onchange="updateDesign()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                        <option value="loop">병목 제로 순환형 루프 (Loop)</option>
                        <option value="grid">공간 활용 격자형 (Grid)</option>
                        <option value="radial">중앙 광장 방사형 (Radial)</option>
                    </select>
                </div>
            </div>

            <!-- 약자 배려 옵션 체크박스 -->
            <div class="border-t pt-4 space-y-2">
                <span class="text-xs font-bold text-slate-600 uppercase">사회적 약자 배려 필수 옵션</span>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkAisle" checked onchange="updateDesign()" class="w-4 h-4 text-indigo-600 rounded">
                    통로 폭 최소 2.0m~2.4m 확보 (휠체어 양방향 교행)
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkLowDesk" checked onchange="updateDesign()" class="w-4 h-4 text-indigo-600 rounded">
                    높이 75cm 이하 낮은 안내 데스크 배치
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkQuietZone" checked onchange="updateDesign()" class="w-4 h-4 text-indigo-600 rounded">
                    감각 안심 쉼터 & 수유실/메디컬존 필수 포함
                </label>
            </div>

            <!-- 사용자 직접 부스 추가 -->
            <div class="border-t pt-4 space-y-2">
                <label class="block text-xs font-bold text-slate-600">추가할 맞춤형 부스/시설 직접 입력</label>
                <div class="flex gap-2">
                    <input type="text" id="customBoothInput" placeholder="예: 수어통역 부스, 팝업존" class="flex-1 p-2 bg-slate-50 border border-slate-300 rounded-lg text-xs outline-none focus:ring-2 focus:ring-indigo-500">
                    <button onclick="addCustomBooth()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-2 rounded-lg text-xs font-bold shadow transition">
                        + 추가
                    </button>
                </div>
                <!-- 부스 태그 목록 -->
                <div id="customBoothList" class="flex flex-wrap gap-1.5 mt-2"></div>
            </div>

        </section>

        <!-- 우측 메인 영역 (8 컬럼) -->
        <section class="lg:col-span-8 flex flex-col gap-5">

            <!-- STEP 1: 공간 설계 도면 & 줌(Zoom) 컨트롤 -->
            <div id="step-view-1" class="step-view flex flex-col gap-4">
                
                <!-- 도면 상단 툴바 & 줌 조작 버튼 -->
                <div class="bg-white p-3 rounded-2xl border border-slate-200 shadow-sm flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <span class="font-bold text-slate-800 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-map-location-dot text-indigo-600"></i> CAD 공간 배치 도면
                        </span>
                        <span class="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded font-medium border border-indigo-100">
                            스케일 1:100 (m)
                        </span>
                    </div>

                    <!-- 줌(Zoom) 조작 툴바 -->
                    <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200">
                        <button onclick="zoomCanvas(-0.1)" class="w-8 h-8 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 font-bold transition" title="축소">
                            <i class="fa-solid fa-minus text-xs"></i>
                        </button>
                        <span id="zoomDisplay" class="text-xs font-bold text-slate-700 px-2">100%</span>
                        <button onclick="zoomCanvas(0.1)" class="w-8 h-8 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 font-bold transition" title="확대">
                            <i class="fa-solid fa-plus text-xs"></i>
                        </button>
                        <button onclick="resetZoom()" class="w-8 h-8 rounded-lg bg-white shadow-sm hover:bg-slate-50 flex items-center justify-center text-slate-700 transition ml-1" title="줌 초기화">
                            <i class="fa-solid fa-rotate-left text-xs"></i>
                        </button>
                    </div>
                </div>

                <!-- CAD 캔버스 영역 -->
                <div class="bg-slate-900 rounded-2xl border border-slate-800 p-4 h-[480px] relative overflow-hidden flex items-center justify-center">
                    
                    <!-- 확대/축소 지원 뷰포트 -->
                    <div id="canvasViewport" class="w-full h-full cad-grid bg-slate-900 rounded-xl border border-slate-700/60 p-6 flex flex-col justify-between relative shadow-inner">
                        
                        <!-- 입구 구역 -->
                        <div class="flex justify-between items-center border-b border-indigo-500/30 pb-3">
                            <div class="bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 text-xs font-bold px-3 py-1.5 rounded-lg flex items-center gap-2">
                                <i class="fa-solid fa-door-open text-emerald-400"></i> 주출입구 (경사로 + 점자블록 + 낮은 안내데스크)
                            </div>
                            <span class="text-[11px] text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-2 py-0.5 rounded">
                                메인 통로폭: <b id="dispWidth">2.4m</b>
                            </span>
                        </div>

                        <!-- 중앙 부스 동적 그리드 -->
                        <div id="boothGridCanvas" class="grid grid-cols-3 gap-3 my-auto">
                            <!-- JS 동적 생성 -->
                        </div>

                        <!-- 하단 출구 & 쉼터 구역 -->
                        <div class="flex justify-between items-center border-t border-indigo-500/30 pt-3">
                            <div class="bg-amber-500/20 border border-amber-500/40 text-amber-300 text-xs font-bold px-3 py-1.5 rounded-lg flex items-center gap-2">
                                <i class="fa-solid fa-couch text-amber-400"></i> 배리어프리 안심 쉼터 & 메디컬 존
                            </div>
                            <div class="bg-slate-800 border border-slate-700 text-slate-300 text-xs font-bold px-3 py-1.5 rounded-lg flex items-center gap-1">
                                출구 <i class="fa-solid fa-arrow-right ml-1"></i>
                            </div>
                        </div>

                    </div>

                    <!-- 범례 오버레이 -->
                    <div class="absolute bottom-6 left-6 bg-slate-900/90 backdrop-blur border border-slate-700 p-2.5 rounded-xl text-[11px] text-slate-300 flex gap-3 shadow-lg pointer-events-none">
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>약자배려 존</span>
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-400"></span>메인 부스</span>
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-pink-400"></span>커스텀 부스</span>
                    </div>
                </div>

                <!-- 하단 다음 단계 버튼 -->
                <div class="flex justify-end">
                    <button onclick="switchStep(2)" class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold px-6 py-3 rounded-xl text-sm shadow-md transition flex items-center gap-2">
                        다음: AI 동선 계산 & 시뮬레이션 <i class="fa-solid fa-arrow-right"></i>
                    </button>
                </div>
            </div>


            <!-- STEP 2: AI 동선 계산 & 병목 시뮬레이션 -->
            <div id="step-view-2" class="step-view hidden flex-col gap-4">
                
                <!-- 동선 계산 수치 지표 카드 -->
                <div class="grid grid-cols-3 gap-3">
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">예상 병목 위험도</div>
                        <div id="simBottleneck" class="text-xl font-bold text-emerald-600 mt-1">낮음 (2.1%)</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">순환형 루프로 교차 차단</div>
                    </div>
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">휠체어/유모차 이동 원활성</div>
                        <div id="simAccessibility" class="text-xl font-bold text-indigo-600 mt-1">최상 (96점)</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">통로폭 2.2m 이상 확보</div>
                    </div>
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
                        <div class="text-xs text-slate-500 font-medium">평균 공간 체류 시간</div>
                        <div class="text-xl font-bold text-purple-600 mt-1">38 분</div>
                        <div class="text-[11px] text-slate-400 mt-0.5">쾌적한 관람 동선 유지</div>
                    </div>
                </div>

                <!-- 동선 흐름 시뮬레이션 캔버스 (SVG 파티클 애니메이션) -->
                <div class="bg-slate-900 rounded-2xl border border-slate-800 p-4 h-[400px] relative flex flex-col justify-between">
                    <div class="flex justify-between items-center text-xs text-slate-400 border-b border-slate-800 pb-2">
                        <span class="font-bold text-indigo-400 flex items-center gap-1.5">
                            <i class="fa-solid fa-circle-dot text-emerald-400 animate-pulse"></i> AI 동선 및 관람객 유동 벡터 분석
                        </span>
                        <span>실시간 유동 벡터 시뮬레이션 작동 중</span>
                    </div>

                    <!-- SVG 동선 시각화 -->
                    <svg class="w-full h-full absolute inset-0 p-6 pointer-events-none" viewBox="0 0 600 300">
                        <!-- 주 동선 경로 라인 -->
                        <path d="M 50 40 L 550 40 L 550 260 L 50 260 Z" fill="none" stroke="#6366f1" stroke-width="3" opacity="0.3" />
                        <path d="M 50 40 L 550 40 L 550 260 L 50 260 Z" fill="none" stroke="#10b981" stroke-width="3" class="flow-line" />
                        
                        <!-- 교차 보조 동선 -->
                        <path d="M 300 40 L 300 260" fill="none" stroke="#ec4899" stroke-width="2" class="flow-line" opacity="0.7" />

                        <!-- 노드 포인트 -->
                        <circle cx="50" cy="40" r="8" fill="#10b981" />
                        <circle cx="550" cy="40" r="8" fill="#6366f1" />
                        <circle cx="550" cy="260" r="8" fill="#ec4899" />
                        <circle cx="50" cy="260" r="8" fill="#f59e0b" />
                    </svg>

                    <div class="mt-auto bg-slate-800/80 backdrop-blur p-3 rounded-xl border border-slate-700 text-xs text-slate-300 flex justify-between items-center z-10">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid fa-wand-magic-sparkles text-amber-400"></i>
                            <span><b>AI 해석:</b> 메인 통로와 부스 사이 간격이 넓어 병목 현상 없이 유연하게 관람객이 순환합니다.</span>
                        </div>
                    </div>
                </div>

                <!-- 단계 이동 버튼 -->
                <div class="flex justify-between">
                    <button onclick="switchStep(1)" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">
                        <i class="fa-solid fa-arrow-left"></i> 이전: 공간 설계
                    </button>
                    <button onclick="switchStep(3)" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-6 py-2.5 rounded-xl text-sm shadow-md transition flex items-center gap-2">
                        최종 평가 & AI 리포트 생성 <i class="fa-solid fa-file-contract"></i>
                    </button>
                </div>
            </div>


            <!-- STEP 3: 최종 평가 & 종합 AI 리포트 -->
            <div id="step-view-3" class="step-view hidden flex-col gap-4">
                
                <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
                    
                    <!-- 리포트 헤더 -->
                    <div class="border-b pb-4 flex justify-between items-start">
                        <div>
                            <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider">AI 종합 검토 보고서</span>
                            <h3 class="text-xl font-bold text-slate-900 mt-1">행사장 공간 최적화 & 배리어프리 평가 리포트</h3>
                        </div>
                        <button onclick="window.print()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold px-3 py-2 rounded-lg border border-slate-300 flex items-center gap-1.5 transition">
                            <i class="fa-solid fa-print"></i> 인쇄 / PDF 저장
                        </button>
                    </div>

                    <!-- 점수 요약 -->
                    <div class="grid grid-cols-3 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
                        <div class="text-center">
                            <div class="text-xs text-slate-500 font-semibold">배리어프리 적합성</div>
                            <div id="repScoreBF" class="text-2xl font-black text-emerald-600 mt-1">98점</div>
                        </div>
                        <div class="text-center border-x border-slate-200">
                            <div class="text-xs text-slate-500 font-semibold">동선 효율성</div>
                            <div id="repScoreFlow" class="text-2xl font-black text-indigo-600 mt-1">95점</div>
                        </div>
                        <div class="text-center">
                            <div class="text-xs text-slate-500 font-semibold">안전 및 응급 대처</div>
                            <div class="text-2xl font-black text-purple-600 mt-1">92점</div>
                        </div>
                    </div>

                    <!-- 세부 평가 내용 -->
                    <div class="space-y-4 text-xs md:text-sm text-slate-700">
                        <h4 class="font-bold text-slate-900 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-check-circle text-emerald-500"></i> 항목별 AI 종합 소평
                        </h4>
                        
                        <div class="space-y-2">
                            <div class="p-3 bg-emerald-50 border border-emerald-100 rounded-xl">
                                <strong class="text-emerald-900">1. 사회적 약자 배려 (Barrier-Free)</strong>
                                <p class="text-emerald-800 mt-1 text-xs">
                                    주출입구 점자블록 및 낮은 안내데스크가 완비되었으며, 통로폭이 2.2m 이상 확보되어 휠체어 사용자와 유모차 이동에 지장이 없습니다.
                                </p>
                            </div>

                            <div class="p-3 bg-indigo-50 border border-indigo-100 rounded-xl">
                                <strong class="text-indigo-900">2. 동선 및 병목 방지</strong>
                                <p class="text-indigo-800 mt-1 text-xs">
                                    순환형 루프 알고리즘이 적용되어 입구와 출구의 관람객 교행 충돌을 최소화하였습니다.
                                </p>
                            </div>

                            <div class="p-3 bg-purple-50 border border-purple-100 rounded-xl">
                                <strong class="text-purple-900">3. 맞춤형 부스 수용성</strong>
                                <p class="text-purple-800 mt-1 text-xs" id="repCustomNote">
                                    사용자가 추가한 부스들이 메인 동선의 시야 확보 구역에 적절히 배치되었습니다.
                                </p>
                            </div>
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

    <!-- JavaScript logic -->
    <script>
        let currentStep = 1;
        let zoomLevel = 1.0;
        let customBooths = ['수어통역 안내소', '인터랙티브 포토존'];

        const defaultBooths = [
            { name: '스마트 안내 부스', type: 'bf', icon: 'fa-wheelchair' },
            { name: '메인 전시 부스 A', type: 'main', icon: 'fa-star' },
            { name: '메인 전시 부스 B', type: 'main', icon: 'fa-cube' },
            { name: '배리어프리 휴게존', type: 'bf', icon: 'fa-heart' }
        ];

        window.onload = () => {
            renderCustomTags();
            updateDesign();
        };

        // 1. 단계(Step) 전환 함수
        function switchStep(step) {
            currentStep = step;
            
            // 탭 스타일 변경
            document.querySelectorAll('.step-tab').forEach((tab, idx) => {
                if (idx + 1 === step) {
                    tab.classList.remove('text-slate-400', 'hover:text-white');
                    tab.classList.add('bg-indigo-600', 'text-white', 'shadow');
                } else {
                    tab.classList.remove('bg-indigo-600', 'text-white', 'shadow');
                    tab.classList.add('text-slate-400', 'hover:text-white');
                }
            });

            // 뷰 스위칭
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

        // 2. 도면 확대 / 축소 (Zoom) 함수
        function zoomCanvas(delta) {
            zoomLevel = Math.max(0.6, Math.min(1.8, zoomLevel + delta));
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

        // 3. 커스텀 부스 추가/삭제
        function addCustomBooth() {
            const input = document.getElementById('customBoothInput');
            const val = input.value.trim();
            if (val) {
                customBooths.push(val);
                input.value = '';
                renderCustomTags();
                updateDesign();
            }
        }

        function removeCustomBooth(idx) {
            customBooths.splice(idx, 1);
            renderCustomTags();
            updateDesign();
        }

        function renderCustomTags() {
            const container = document.getElementById('customBoothList');
            container.innerHTML = customBooths.map((b, i) => `
                <span class="bg-pink-50 text-pink-700 border border-pink-200 text-[11px] px-2 py-0.5 rounded-full flex items-center gap-1 font-semibold">
                    ${b}
                    <button onclick="removeCustomBooth(${i})" class="hover:text-pink-900 font-bold ml-1">×</button>
                </span>
            `).join('');
        }

        // 4. 공간 배치 동적 업데이트
        function updateDesign() {
            const chkAisle = document.getElementById('chkAisle').checked;
            document.getElementById('dispWidth').innerText = chkAisle ? '2.4m' : '1.5m';

            const grid = document.getElementById('boothGridCanvas');
            grid.innerHTML = '';

            // 기본 부스
            defaultBooths.forEach(b => {
                const color = b.type === 'bf' ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-300' : 'bg-indigo-950/80 border-indigo-500/50 text-indigo-300';
                grid.innerHTML += `
                    <div class="p-3 rounded-xl border ${color} text-xs font-bold flex flex-col items-center justify-center gap-1.5 text-center shadow">
                        <i class="fa-solid ${b.icon} text-base"></i>
                        ${b.name}
                    </div>
                `;
            });

            // 사용자 지정 부스
            customBooths.forEach(c => {
                grid.innerHTML += `
                    <div class="p-3 rounded-xl border bg-pink-950/80 border-pink-500/50 text-pink-300 text-xs font-bold flex flex-col items-center justify-center gap-1.5 text-center shadow">
                        <i class="fa-solid fa-puzzle-piece text-base"></i>
                        ${c}
                    </div>
                `;
            });

            // 리포트 텍스트 반영
            document.getElementById('repCustomNote').innerText = `총 ${customBooths.length}개의 사용자 추가 부스(${customBooths.join(', ') || '없음'})가 메인 동선의 시야 확보 구역에 성공적으로 배치되었습니다.`;
        }
    </script>
</body>
</html>
"""

# Streamlit 내에 HTML 렌더링 (충분한 높이 확보)
components.html(SIMULATOR_HTML, height=800, scrolling=True)
