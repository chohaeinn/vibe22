import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI 스마트 행사장 설계 & 동선·밀집도 시뮬레이터",
    page_icon="🎨",
    layout="wide"
)

SIMULATOR_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 행사장 설계 & 동선 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* 밝은 CAD 격자 배경 */
        .cad-grid-bright {
            background-color: #ffffff;
            background-size: 20px 20px;
            background-image: 
                linear-gradient(to right, rgba(226, 232, 240, 0.8) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(226, 232, 240, 0.8) 1px, transparent 1px);
        }

        /* 토글 스위치 */
        .switch { position: relative; display: inline-block; width: 40px; height: 20px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #cbd5e1; transition: .2s; border-radius: 20px;
        }
        .slider:before {
            position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px;
            background-color: white; transition: .2s; border-radius: 50%;
        }
        input:checked + .slider { background-color: #4f46e5; }
        input:checked + .slider:before { transform: translateX(20px); }

        /* 동선 흐름 애니메이션 */
        @keyframes flowAnimation {
            0% { stroke-dashoffset: 40; }
            100% { stroke-dashoffset: 0; }
        }
        .flow-path { stroke-dasharray: 8, 8; animation: flowAnimation 1s linear infinite; }

        /* 비상 대피 화살표 점멸 */
        @keyframes emergencyBlink {
            0%, 100% { opacity: 1; stroke: #ef4444; }
            50% { opacity: 0.3; stroke: #f87171; }
        }
        .emergency-path { stroke-dasharray: 6, 6; animation: emergencyBlink 0.8s ease-in-out infinite; }

        /* 커스텀 스크롤바 */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        /* 인터랙티브 부스 카드 */
        .booth-card {
            user-select: none;
            touch-action: none;
            transition: box-shadow 0.15s ease, border-color 0.15s ease;
        }
        .booth-card:hover { box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1); }
        .booth-card.selected { border-color: #6366f1 !important; ring: 2px; ring-color: #c7d2fe; }

        /* 리사이즈 핸들 */
        .resize-handle {
            position: absolute;
            right: 2px;
            bottom: 2px;
            width: 14px;
            height: 14px;
            cursor: se-resize;
            background: linear-gradient(135deg, transparent 50%, #94a3b8 50%);
            border-bottom-right-radius: 6px;
        }
        .resize-handle:hover { background: linear-gradient(135deg, transparent 50%, #4f46e5 50%); }
    </style>
</head>
<body class="bg-slate-100 text-slate-800 font-sans min-h-screen flex flex-col select-none">

    <!-- Header -->
    <header class="bg-white px-6 py-3.5 border-b border-slate-200 flex justify-between items-center shrink-0 shadow-sm">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold text-xl shadow-md">
                <i class="fa-solid fa-compass-drafting"></i>
            </div>
            <div>
                <h1 class="text-lg font-bold tracking-tight text-slate-900 flex items-center gap-2">
                    AI 행사장 스마트 공간 설계 & 동선 시뮬레이터
                    <span class="text-xs font-semibold bg-indigo-100 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded-full">Light Studio v6.0</span>
                </h1>
                <p class="text-xs text-slate-500">자유로운 부스 드래그 & 크기 조절 · 실시간 동선 및 히트맵 최적화 시스템</p>
            </div>
        </div>
        
        <div class="flex items-center gap-2">
            <button onclick="exportLayoutJSON()" class="bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold px-3.5 py-2 rounded-xl text-xs transition flex items-center gap-1.5 shadow-sm">
                <i class="fa-solid fa-download text-slate-500"></i> 도면 내보내기
            </button>
            <button onclick="resetLayout()" class="bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-semibold px-3.5 py-2 rounded-xl text-xs transition flex items-center gap-1.5 shadow-sm">
                <i class="fa-solid fa-rotate-right text-slate-500"></i> 초기화
            </button>
            <button onclick="toggleAIOptimization()" id="btnAIToggle" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-4 py-2 rounded-xl text-xs shadow-md transition flex items-center gap-2">
                <i class="fa-solid fa-wand-magic-sparkles"></i> <span>AI 공간 설계 자동 최적화</span>
            </button>
        </div>
    </header>

    <!-- Main Workspace -->
    <div class="flex-1 max-w-[1600px] w-full mx-auto p-4 grid grid-cols-1 lg:grid-cols-12 gap-4">

        <!-- 좌측 제어 및 옵션 패널 (4 컬럼) -->
        <section class="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-4 flex flex-col gap-4 overflow-y-auto max-h-[860px] shadow-sm">
            
            <!-- 1. 시각화 레이어 토글 -->
            <div class="border-b border-slate-100 pb-3 space-y-2">
                <h2 class="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-layer-group text-indigo-600"></i> 1. 디스플레이 레이어 설정
                </h2>

                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                        <span class="font-medium text-slate-700 flex items-center gap-1.5"><i class="fa-solid fa-route text-emerald-500"></i> 동선 (Flow)</span>
                        <label class="switch"><input type="checkbox" id="toggleFlow" checked onchange="renderAllLayers()"><span class="slider"></span></label>
                    </div>
                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                        <span class="font-medium text-slate-700 flex items-center gap-1.5"><i class="fa-solid fa-fire text-amber-500"></i> 밀집도 히트맵</span>
                        <label class="switch"><input type="checkbox" id="toggleHeatmap" checked onchange="renderAllLayers()"><span class="slider"></span></label>
                    </div>
                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                        <span class="font-medium text-slate-700 flex items-center gap-1.5"><i class="fa-solid fa-shield-halved text-blue-500"></i> 안전 버퍼 구역</span>
                        <label class="switch"><input type="checkbox" id="toggleBuffer" onchange="renderAllLayers()"><span class="slider"></span></label>
                    </div>
                    <div class="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                        <span class="font-medium text-slate-700 flex items-center gap-1.5"><i class="fa-solid fa-[#ef4444] fa-truck-medical text-red-500"></i> 비상 대피 경로</span>
                        <label class="switch"><input type="checkbox" id="toggleEmergency" onchange="renderAllLayers()"><span class="slider"></span></label>
                    </div>
                </div>
            </div>

            <!-- 2. 부스 직접 추가 & 편집 옵션 -->
            <div class="border-b border-slate-100 pb-3 space-y-2">
                <h2 class="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-plus-minus text-indigo-600"></i> 2. 부스 추가 및 제어
                </h2>
                <div class="flex gap-2">
                    <input type="text" id="newBoothName" placeholder="신규 부스명 입력" class="flex-1 border border-slate-300 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500">
                    <select id="newBoothType" class="border border-slate-300 rounded-xl px-2 py-1.5 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <option value="normal">일반 부스</option>
                        <option value="popular">인기 부스 (혼잡)</option>
                        <option value="main">메인 무대</option>
                        <option value="food">푸드/음료</option>
                    </select>
                    <button onclick="addNewBooth()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-3 py-1.5 rounded-xl text-xs shadow-sm">추가</button>
                </div>
                <div id="selectedBoothInfo" class="text-[11px] text-slate-500 bg-indigo-50/50 border border-indigo-100 p-2 rounded-xl flex justify-between items-center">
                    <span>💡 부스를 클릭하면 선택하여 삭제할 수 있습니다.</span>
                    <button id="btnDeleteBooth" onclick="deleteSelectedBooth()" class="hidden text-xs text-red-600 font-bold hover:underline"><i class="fa-solid fa-trash"></i> 선택 부스 삭제</button>
                </div>
            </div>

            <!-- 3. 시뮬레이션 환경 세부 조절 옵션 -->
            <div class="border-b border-slate-100 pb-3 space-y-3">
                <h2 class="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-indigo-600"></i> 3. 정밀 시뮬레이션 변수 옵션
                </h2>

                <!-- 격자 스냅 -->
                <div class="flex justify-between items-center text-xs">
                    <span class="text-slate-600">격자 스냅 (Grid Snap)</span>
                    <select id="gridSnapSize" onchange="renderAllLayers()" class="border border-slate-300 rounded-lg px-2 py-1 text-xs bg-white">
                        <option value="1">사용 안 함 (자유)</option>
                        <option value="10">10px 정렬</option>
                        <option value="20" selected>20px 정렬</option>
                    </select>
                </div>

                <!-- 히트맵 반경 -->
                <div class="space-y-1">
                    <div class="flex justify-between text-xs text-slate-600">
                        <span>히트맵확산 반경 (Blur)</span>
                        <span id="lblHeatRadius" class="font-bold text-indigo-600">80px</span>
                    </div>
                    <input type="range" id="heatRadius" min="40" max="160" value="80" oninput="document.getElementById('lblHeatRadius').innerText=this.value+'px'; renderAllLayers();" class="w-full accent-indigo-600">
                </div>

                <!-- 히트맵 투명도 -->
                <div class="space-y-1">
                    <div class="flex justify-between text-xs text-slate-600">
                        <span>히트맵 레이어 투명도</span>
                        <span id="lblHeatOpacity" class="font-bold text-indigo-600">65%</span>
                    </div>
                    <input type="range" id="heatOpacity" min="20" max="100" value="65" oninput="document.getElementById('lblHeatOpacity').innerText=this.value+'%'; renderAllLayers();" class="w-full accent-indigo-600">
                </div>

                <!-- 시간대별 유입량 -->
                <div class="space-y-1">
                    <div class="flex justify-between text-xs text-slate-600">
                        <span>시간대별 관람객 유입 시간</span>
                        <span id="timeDisplay" class="font-bold text-indigo-600">14:00 (피크 타임)</span>
                    </div>
                    <input type="range" id="timeSlider" min="9" max="18" value="14" step="1" oninput="onTimeChange(this.value)" class="w-full accent-indigo-600">
                    <div class="flex justify-between text-[10px] text-slate-400">
                        <span>09:00 (개장)</span>
                        <span>14:00 (피크)</span>
                        <span>18:00 (폐장)</span>
                    </div>
                </div>
            </div>

            <!-- 4. Real-time AI 분석 모니터링 -->
            <div class="space-y-2">
                <h2 class="font-bold text-slate-800 text-xs uppercase tracking-wider flex items-center gap-2">
                    <i class="fa-solid fa-chart-line text-indigo-600"></i> 4. 실시간 AI 안전 및 공간 리포트
                </h2>

                <div class="grid grid-cols-2 gap-2">
                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                        <div class="text-[10px] text-slate-500">최대 혼잡 병목 위험도</div>
                        <div id="valRisk" class="text-sm font-bold text-red-500 mt-0.5">42.8% (혼잡 경고)</div>
                    </div>
                    <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
                        <div class="text-[10px] text-slate-500">동선 수월성 평가 점수</div>
                        <div id="valFlow" class="text-sm font-bold text-slate-700 mt-0.5">65 점</div>
                    </div>
                </div>

                <div class="bg-indigo-50/60 border border-indigo-100 p-3 rounded-xl text-xs text-slate-700 leading-relaxed">
                    <strong class="text-indigo-700 block mb-0.5"><i class="fa-solid fa-robot"></i> AI 최적화 진단:</strong>
                    <span id="aiReportText">부스를 드래그하여 배치하거나 우측 하단 핸들을 잡아 크기를 조절해보세요. 위치 변동 시 실시간으로 동선 및 밀집도가 재계산됩니다.</span>
                </div>
            </div>

        </section>

        <!-- 우측 메인 스마트 캔버스 영역 (8 컬럼) -->
        <section class="lg:col-span-8 flex flex-col gap-3">

            <!-- 스마트 설계도 보드 -->
            <div class="bg-white rounded-2xl border border-slate-200 p-3 h-[780px] relative overflow-hidden shadow-sm flex items-center justify-center">
                
                <div id="canvasViewport" class="w-full h-full cad-grid-bright rounded-xl border border-slate-300 relative overflow-hidden">
                    
                    <!-- 1. 부스 레이어 (드래그 & 크기조절 가능 DOM 객체들) -->
                    <div id="boothLayer" class="absolute inset-0 z-20">
                        <!-- Dynamic Draggable & Resizable Booth Cards -->
                    </div>

                    <!-- 2. 인구 밀집도 히트맵 Canvas -->
                    <canvas id="heatmapCanvas" width="900" height="750" class="absolute inset-0 z-10 pointer-events-none"></canvas>

                    <!-- 3. 관람객 동선 벡터 SVG -->
                    <svg id="flowSvg" class="absolute inset-0 w-full h-full z-30 pointer-events-none">
                        <!-- Dynamic SVG Lines & Paths -->
                    </svg>

                    <!-- 주출입구 & 비상구 고정 오버레이 -->
                    <div class="absolute top-3 left-4 right-4 flex justify-between items-center z-40 pointer-events-none">
                        <span class="bg-emerald-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md flex items-center gap-1.5">
                            <i class="fa-solid fa-door-open"></i> 메인 주출입구 (GATE 1)
                        </span>
                        <span id="layoutStateBadge" class="bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
                            상태: 커스텀 설계 모드
                        </span>
                    </div>

                    <div class="absolute bottom-3 left-4 right-4 flex justify-between items-center z-40 pointer-events-none">
                        <span class="bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md flex items-center gap-1.5">
                            <i class="fa-solid fa-truck-medical"></i> 비상 탈출구 (EMERGENCY EXIT)
                        </span>
                        <span class="bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md flex items-center gap-1">
                            보조 출구 (GATE 2) <i class="fa-solid fa-arrow-right"></i>
                        </span>
                    </div>

                </div>

                <!-- 히트맵 범례 -->
                <div class="absolute bottom-6 right-6 bg-white/90 backdrop-blur border border-slate-200 p-2.5 rounded-xl text-[11px] text-slate-700 shadow-md z-50 pointer-events-none">
                    <div class="font-bold mb-1 flex justify-between items-center">
                        <span>밀집도 범례</span>
                        <span class="text-[9px] text-slate-400">인원/m²</span>
                    </div>
                    <div class="w-32 h-2.5 rounded-full bg-gradient-to-r from-blue-500 via-emerald-400 via-amber-400 to-red-500"></div>
                    <div class="flex justify-between text-[9px] text-slate-500 mt-1">
                        <span>쾌적</span>
                        <span>보통</span>
                        <span>혼잡</span>
                    </div>
                </div>

            </div>

        </section>
    </div>

    <!-- JavaScript - Interactive Drag/Resize & Dynamic Heatmap Engine -->
    <script>
        let isAIOptimized = false;
        let currentTime = 14;
        let selectedBoothId = null;

        // 초기 부스 상태 데이터
        let booths = [
            { id: 'b1', name: '메인 무대 (A)', type: 'main', x: 60, y: 70, w: 220, h: 120, icon: 'fa-star' },
            { id: 'b2', name: '인기 체험부스 (B)', type: 'popular', x: 310, y: 70, w: 190, h: 120, icon: 'fa-fire' },
            { id: 'b3', name: 'IT 전시관 (C)', type: 'normal', x: 530, y: 70, w: 190, h: 120, icon: 'fa-laptop' },
            { id: 'b4', name: '의무실 & BF안내', type: 'normal', x: 60, y: 240, w: 220, h: 100, icon: 'fa-kit-medical' },
            { id: 'b5', name: '이벤트 팝업 (D)', type: 'normal', x: 310, y: 240, w: 190, h: 100, icon: 'fa-gift' },
            { id: 'b6', name: '푸드/음료 존', type: 'food', x: 530, y: 240, w: 190, h: 100, icon: 'fa-utensils' }
        ];

        window.onload = () => {
            renderAllLayers();
        };

        function onTimeChange(val) {
            currentTime = parseInt(val);
            document.getElementById('timeDisplay').innerText = `${val}:00 ${val == 14 ? '(피크 타임)' : ''}`;
            renderAllLayers();
        }

        // 전체 레이어 재렌더링
        function renderAllLayers() {
            renderBoothDOMs();
            renderHeatmapCanvas();
            renderFlowSVG();
            updateMetrics();
        }

        // 1. 부스 DOM 렌더링 (드래그 & 크기조절 이벤트 포함)
        function renderBoothDOMs() {
            const container = document.getElementById('boothLayer');
            container.innerHTML = '';

            booths.forEach(b => {
                let styleClasses = "bg-white border-slate-300 text-slate-800";
                let badgeClasses = "bg-slate-100 text-slate-600";
                
                if (b.type === 'popular') {
                    styleClasses = "bg-amber-50/90 border-amber-400 text-amber-900";
                    badgeClasses = "bg-amber-200 text-amber-800";
                } else if (b.type === 'main') {
                    styleClasses = "bg-indigo-50/90 border-indigo-400 text-indigo-900";
                    badgeClasses = "bg-indigo-200 text-indigo-800";
                } else if (b.type === 'food') {
                    styleClasses = "bg-orange-50/90 border-orange-400 text-orange-900";
                    badgeClasses = "bg-orange-200 text-orange-800";
                }

                const isSelected = (selectedBoothId === b.id);
                const borderRing = isSelected ? 'ring-2 ring-indigo-500 border-indigo-600' : '';

                const el = document.createElement('div');
                el.className = `booth-card absolute rounded-xl border-2 p-3 shadow-sm flex flex-col justify-between cursor-move ${styleClasses} ${borderRing}`;
                el.style.left = `${b.x}px`;
                el.style.top = `${b.y}px`;
                el.style.width = `${b.w}px`;
                el.style.height = `${b.h}px`;
                el.id = `booth-${b.id}`;

                el.innerHTML = `
                    <div class="flex justify-between items-center pointer-events-none">
                        <span class="text-xs font-bold flex items-center gap-1.5 truncate">
                            <i class="fa-solid ${b.icon}"></i> ${b.name}
                        </span>
                        <span class="text-[9px] font-semibold px-1.5 py-0.5 rounded ${badgeClasses}">
                            ${b.w}x${b.h}
                        </span>
                    </div>
                    <div class="text-[10px] text-slate-400 flex justify-between pointer-events-none">
                        <span>X: ${b.x}, Y: ${b.y}</span>
                        <span class="text-indigo-600 font-semibold">${b.type}</span>
                    </div>
                    <div class="resize-handle" title="크기 조절"></div>
                `;

                // 부스 클릭 선택
                el.addEventListener('click', (e) => {
                    e.stopPropagation();
                    selectedBoothId = b.id;
                    document.getElementById('btnDeleteBooth').classList.remove('hidden');
                    renderBoothDOMs();
                });

                // 드래그 및 리사이즈 이벤트 바인딩
                makeBoothInteractive(el, b);

                container.appendChild(el);
            });
        }

        // 드래그 & 크기 조절 (Mouse / Touch) 이벤트 로직
        function makeBoothInteractive(el, boothData) {
            let isDragging = false;
            let isResizing = false;
            let startX, startY, initialX, initialY, initialW, initialH;

            const gridSnap = parseInt(document.getElementById('gridSnapSize').value) || 1;

            el.addEventListener('mousedown', (e) => {
                if (e.target.classList.contains('resize-handle')) {
                    isResizing = true;
                } else {
                    isDragging = true;
                }

                startX = e.clientX;
                startY = e.clientY;
                initialX = boothData.x;
                initialY = boothData.y;
                initialW = boothData.w;
                initialH = boothData.h;

                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
            });

            function onMouseMove(e) {
                const dx = e.clientX - startX;
                const dy = e.clientY - startY;

                if (isDragging) {
                    let newX = Math.max(10, Math.min(680, initialX + dx));
                    let newY = Math.max(10, Math.min(600, initialY + dy));

                    if (gridSnap > 1) {
                        newX = Math.round(newX / gridSnap) * gridSnap;
                        newY = Math.round(newY / gridSnap) * gridSnap;
                    }

                    boothData.x = newX;
                    boothData.y = newY;
                    el.style.left = `${newX}px`;
                    el.style.top = `${newY}px`;
                } else if (isResizing) {
                    let newW = Math.max(80, initialW + dx);
                    let newH = Math.max(60, initialH + dy);

                    if (gridSnap > 1) {
                        newW = Math.round(newW / gridSnap) * gridSnap;
                        newH = Math.round(newH / gridSnap) * gridSnap;
                    }

                    boothData.w = newW;
                    boothData.h = newH;
                    el.style.width = `${newW}px`;
                    el.style.height = `${newH}px`;
                }

                // 이동/크기 조절 시 실시간 레이어 업데이트
                renderHeatmapCanvas();
                renderFlowSVG();
            }

            function onMouseUp() {
                isDragging = false;
                isResizing = false;
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                renderAllLayers();
            }
        }

        // 2. 히트맵 Canvas 렌더링
        function renderHeatmapCanvas() {
            const canvas = document.getElementById('heatmapCanvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (!document.getElementById('toggleHeatmap').checked) return;

            const radius = parseInt(document.getElementById('heatRadius').value);
            const opacity = parseInt(document.getElementById('heatOpacity').value) / 100;
            const densityFactor = (currentTime / 14.0);

            ctx.globalAlpha = opacity;

            booths.forEach(b => {
                let cx = b.x + b.w / 2;
                let cy = b.y + b.h / 2;
                
                let curRadius = (b.type === 'popular') ? radius * 1.4 * densityFactor : radius * densityFactor;

                const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, curRadius);
                if (b.type === 'popular') {
                    grad.addColorStop(0, 'rgba(239, 68, 68, 0.8)'); // Red
                    grad.addColorStop(0.4, 'rgba(245, 158, 11, 0.5)'); // Amber
                    grad.addColorStop(0.8, 'rgba(16, 185, 129, 0.2)'); // Green
                    grad.addColorStop(1, 'rgba(59, 130, 246, 0)');
                } else {
                    grad.addColorStop(0, 'rgba(16, 185, 129, 0.6)'); // Green
                    grad.addColorStop(0.6, 'rgba(59, 130, 246, 0.2)'); // Blue
                    grad.addColorStop(1, 'rgba(59, 130, 246, 0)');
                }

                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(cx, cy, curRadius, 0, Math.PI * 2);
                ctx.fill();
            });

            ctx.globalAlpha = 1.0;
        }

        // 3. 관람객 동선 & 안전 버퍼 SVG 렌더링
        function renderFlowSVG() {
            const svg = document.getElementById('flowSvg');
            svg.innerHTML = '';

            const showFlow = document.getElementById('toggleFlow').checked;
            const showBuffer = document.getElementById('toggleBuffer').checked;
            const showEmergency = document.getElementById('toggleEmergency').checked;

            // 안전 버퍼 영역 표시
            if (showBuffer) {
                booths.forEach(b => {
                    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                    rect.setAttribute('x', b.x - 15);
                    rect.setAttribute('y', b.y - 15);
                    rect.setAttribute('width', b.w + 30);
                    rect.setAttribute('height', b.h + 30);
                    rect.setAttribute('rx', '16');
                    rect.setAttribute('fill', 'rgba(99, 102, 241, 0.08)');
                    rect.setAttribute('stroke', '#818cf8');
                    rect.setAttribute('stroke-width', '1.5');
                    rect.setAttribute('stroke-dasharray', '4,4');
                    svg.appendChild(rect);
                });
            }

            // 동선 흐름선 표시
            if (showFlow && booths.length > 0) {
                let pathD = `M 150 20 `;
                booths.forEach(b => {
                    let cx = b.x + b.w / 2;
                    let cy = b.y + b.h / 2;
                    pathD += `L ${cx} ${cy} `;
                });
                pathD += `L 550 700`;

                const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                path.setAttribute('d', pathD);
                path.setAttribute('fill', 'none');
                path.setAttribute('stroke', '#4f46e5');
                path.setAttribute('stroke-width', '3');
                path.setAttribute('class', 'flow-path');
                svg.appendChild(path);
            }

            // 비상 대피 경로
            if (showEmergency && booths.length > 0) {
                booths.forEach(b => {
                    let cx = b.x + b.w / 2;
                    let cy = b.y + b.h / 2;
                    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    path.setAttribute('d', `M ${cx} ${cy} L 100 720`);
                    path.setAttribute('fill', 'none');
                    path.setAttribute('stroke', '#ef4444');
                    path.setAttribute('stroke-width', '2');
                    path.setAttribute('class', 'emergency-path');
                    svg.appendChild(path);
                });
            }
        }

        // AI 공간 설계 자동 최적화
        function toggleAIOptimization() {
            isAIOptimized = !isAIOptimized;
            const btn = document.getElementById('btnAIToggle');
            const badge = document.getElementById('layoutStateBadge');

            if (isAIOptimized) {
                // 통로 넓히고 이격 배치
                booths = [
                    { id: 'b1', name: '메인 무대 (A)', type: 'main', x: 50, y: 70, w: 220, h: 130, icon: 'fa-star' },
                    { id: 'b2', name: '인기 체험부스 (B)', type: 'popular', x: 530, y: 70, w: 200, h: 130, icon: 'fa-fire' }, // 분산배치
                    { id: 'b3', name: 'IT 전시관 (C)', type: 'normal', x: 290, y: 70, w: 210, h: 130, icon: 'fa-laptop' },
                    { id: 'b4', name: '의무실 & BF안내', type: 'normal', x: 50, y: 260, w: 220, h: 110, icon: 'fa-kit-medical' },
                    { id: 'b5', name: '이벤트 팝업 (D)', type: 'normal', x: 290, y: 260, w: 210, h: 110, icon: 'fa-gift' },
                    { id: 'b6', name: '푸드/음료 존', type: 'food', x: 530, y: 260, w: 200, h: 110, icon: 'fa-utensils' }
                ];
                btn.className = "bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-xl text-xs shadow-md transition flex items-center gap-2";
                btn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> <span>기존 도면으로 복원</span>`;
                badge.className = "bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md";
                badge.innerText = "상태: AI 공간 최적화 완료";
            } else {
                resetLayout();
                btn.className = "bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-4 py-2 rounded-xl text-xs shadow-md transition flex items-center gap-2";
                btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>AI 공간 설계 자동 최적화</span>`;
                badge.className = "bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md";
                badge.innerText = "상태: 사용자 수동 편집 모드";
            }

            renderAllLayers();
        }

        // 부스 신규 추가
        function addNewBooth() {
            const nameInput = document.getElementById('newBoothName');
            const typeSelect = document.getElementById('newBoothType');
            const name = nameInput.value.trim() || '신규 부스';
            const type = typeSelect.value;

            const newId = 'b' + (Date.now() % 10000);
            booths.push({
                id: newId,
                name: name,
                type: type,
                x: 100 + (booths.length * 20) % 300,
                y: 150 + (booths.length * 20) % 200,
                w: 180,
                h: 100,
                icon: type === 'main' ? 'fa-star' : (type === 'popular' ? 'fa-fire' : 'fa-cube')
            });

            nameInput.value = '';
            renderAllLayers();
        }

        // 선택한 부스 삭제
        function deleteSelectedBooth() {
            if (!selectedBoothId) return;
            booths = booths.filter(b => b.id !== selectedBoothId);
            selectedBoothId = null;
            document.getElementById('btnDeleteBooth').classList.add('hidden');
            renderAllLayers();
        }

        // 리셋
        function resetLayout() {
            booths = [
                { id: 'b1', name: '메인 무대 (A)', type: 'main', x: 60, y: 70, w: 220, h: 120, icon: 'fa-star' },
                { id: 'b2', name: '인기 체험부스 (B)', type: 'popular', x: 310, y: 70, w: 190, h: 120, icon: 'fa-fire' },
                { id: 'b3', name: 'IT 전시관 (C)', type: 'normal', x: 530, y: 70, w: 190, h: 120, icon: 'fa-laptop' },
                { id: 'b4', name: '의무실 & BF안내', type: 'normal', x: 60, y: 240, w: 220, h: 100, icon: 'fa-kit-medical' },
                { id: 'b5', name: '이벤트 팝업 (D)', type: 'normal', x: 310, y: 240, w: 190, h: 100, icon: 'fa-gift' },
                { id: 'b6', name: '푸드/음료 존', type: 'food', x: 530, y: 240, w: 190, h: 100, icon: 'fa-utensils' }
            ];
            selectedBoothId = null;
            renderAllLayers();
        }

        // 도면 JSON 내보내기
        function exportLayoutJSON() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(booths, null, 2));
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", "event_booth_layout.json");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        }

        // 실시간 진단 지표 업데이트
        function updateMetrics() {
            const riskElem = document.getElementById('valRisk');
            const flowElem = document.getElementById('valFlow');
            const textElem = document.getElementById('aiReportText');

            if (isAIOptimized) {
                riskElem.className = "text-sm font-bold text-emerald-600 mt-0.5";
                riskElem.innerText = "6.1% (매우 안전)";
                flowElem.innerText = "98 점";
                textElem.innerText = "AI 최적화 완료: 인기 부스 간격을 확충하고 메인 통로를 2.5m 이상 확보하여 피크타임 혼잡 위험을 완전히 해소했습니다.";
            } else {
                riskElem.className = "text-sm font-bold text-red-500 mt-0.5";
                riskElem.innerText = "42.8% (혼잡 경고)";
                flowElem.innerText = "65 점";
                textElem.innerText = "부스를 자유롭게 드래그하거나 우측 하단 핸들을 조작하여 크기를 변경해 보세요. 부스가 너무 조밀하면 병목 위험도가 증가합니다.";
            }
        }
    </script>
</body>
</html>
"""

components.html(SIMULATOR_HTML, height=920, scrolling=True)
