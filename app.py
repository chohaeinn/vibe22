import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(
    page_title="AI 행사장 설계 & 동선·밀집도 히트맵 시뮬레이터",
    page_icon="📐",
    layout="wide"
)

# HTML/CSS/JS 통합 파이썬 문자열
SIMULATOR_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 행사장 설계 & 동선·밀집도 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CAD 모눈종이 배경 */
        .cad-grid-light {
            background-size: 20px 20px;
            background-image: 
                linear-gradient(to right, rgba(203, 213, 225, 0.4) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(203, 213, 225, 0.4) 1px, transparent 1px);
        }

        /* 토글 스위치 스타일 */
        .switch {
            position: relative;
            display: inline-block;
            width: 44px;
            height: 22px;
        }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #cbd5e1; transition: .3s; border-radius: 22px;
        }
        .slider:before {
            position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px;
            background-color: white; transition: .3s; border-radius: 50%;
        }
        input:checked + .slider { background-color: #4f46e5; }
        input:checked + .slider:before { transform: translateX(22px); }

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
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col select-none">

    <!-- Header -->
    <header class="bg-slate-950 px-6 py-4 border-b border-slate-800 flex justify-between items-center shrink-0 shadow-md">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-xl shadow">
                <i class="fa-solid fa-layer-group"></i>
            </div>
            <div>
                <h1 class="text-lg font-bold tracking-tight text-white">AI 행사장 공간 최적화 & 동선·밀집도 시뮬레이터 <span class="text-xs bg-indigo-500/30 text-indigo-300 border border-indigo-400/30 px-2 py-0.5 rounded ml-2">PRO v5.0</span></h1>
                <p class="text-xs text-slate-400">설계도 기반 AI 배치 최적화 · 실시간 밀집도 히트맵 · 동선 레이어 ON/OFF 시스템</p>
            </div>
        </div>
        
        <button onclick="toggleAIOptimization()" id="btnAIToggle" class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold px-5 py-2.5 rounded-xl text-xs shadow-lg transition flex items-center gap-2">
            <i class="fa-solid fa-wand-magic-sparkles"></i> <span>AI 공간 설계 자동 최적화 적용</span>
        </button>
    </header>

    <!-- Main Container -->
    <div class="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 좌측 제어 패널 (4 컬럼) -->
        <section class="lg:col-span-4 bg-slate-950 rounded-2xl border border-slate-800 p-5 flex flex-col gap-5 h-fit shadow-lg">
            
            <!-- 레이어 ON/OFF 토글 시스템 -->
            <div class="border-b border-slate-800 pb-4 space-y-3">
                <h2 class="font-bold text-indigo-400 text-sm flex items-center gap-2">
                    <i class="fa-solid fa-toggle-on"></i> 시각화 레이어 ON / OFF
                </h2>

                <div class="flex justify-between items-center bg-slate-900 p-3 rounded-xl border border-slate-800">
                    <span class="text-xs font-semibold text-slate-200 flex items-center gap-2">
                        <i class="fa-solid fa-route text-emerald-400"></i> 관람객 이동 동선 (Flow)
                    </span>
                    <label class="switch">
                        <input type="checkbox" id="toggleFlow" checked onchange="renderAllLayers()">
                        <span class="slider"></span>
                    </label>
                </div>

                <div class="flex justify-between items-center bg-slate-900 p-3 rounded-xl border border-slate-800">
                    <span class="text-xs font-semibold text-slate-200 flex items-center gap-2">
                        <i class="fa-solid fa-fire text-amber-500"></i> 인구 밀집도 히트맵 (Heatmap)
                    </span>
                    <label class="switch">
                        <input type="checkbox" id="toggleHeatmap" checked onchange="renderAllLayers()">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <!-- 시간대별 인구 변동 슬라이더 -->
            <div class="border-b border-slate-800 pb-4 space-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-xs font-bold text-slate-300">시간대별 인구 유입 변동</span>
                    <span id="timeDisplay" class="text-xs font-bold text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-800">14:00 (최고 피크 타임)</span>
                </div>
                <input type="range" id="timeSlider" min="9" max="18" value="14" step="1" oninput="onTimeChange(this.value)" class="w-full accent-indigo-500 cursor-pointer">
                <div class="flex justify-between text-[10px] text-slate-500">
                    <span>09:00 (개장)</span>
                    <span>14:00 (피크)</span>
                    <span>18:00 (폐장)</span>
                </div>
            </div>

            <!-- AI 분석 리포트 지표 -->
            <div class="space-y-3">
                <h2 class="font-bold text-slate-300 text-sm flex items-center gap-2">
                    <i class="fa-solid fa-chart-pie text-indigo-400"></i> 실시간 AI 공간 진단
                </h2>

                <div class="grid grid-cols-2 gap-2">
                    <div class="bg-slate-900 p-3 rounded-xl border border-slate-800">
                        <div class="text-[11px] text-slate-400">예상 병목 위험도</div>
                        <div id="valRisk" class="text-base font-bold text-red-400 mt-1">42.5% (혼잡 경고)</div>
                    </div>
                    <div class="bg-slate-900 p-3 rounded-xl border border-slate-800">
                        <div class="text-[11px] text-slate-400">동선 원활성 지수</div>
                        <div id="valFlow" class="text-base font-bold text-slate-300 mt-1">68 점</div>
                    </div>
                </div>

                <div class="bg-slate-900 p-3.5 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed">
                    <strong class="text-indigo-400 block mb-1">🤖 AI 진단 리포트:</strong>
                    <span id="aiReportText">현재 배치 상태는 인기 부스 주변에 관람객이 집중되어 좁은 통로에서 병목 현상이 발생하고 있습니다. 상단의 'AI 공간 설계 자동 최적화' 버튼을 눌러 부스 배치를 재조정하세요.</span>
                </div>
            </div>

        </section>

        <!-- 우측 메인 캔버스 영역 (8 컬럼) -->
        <section class="lg:col-span-8 flex flex-col gap-4">

            <!-- 설계도 & 레이어 시각화 화면 -->
            <div class="bg-slate-950 rounded-2xl border border-slate-800 p-3 h-[620px] relative overflow-hidden shadow-2xl flex items-center justify-center">
                
                <div id="canvasViewport" class="w-full h-full cad-grid-light bg-slate-900 rounded-xl border border-slate-800 relative overflow-hidden">
                    
                    <!-- 1. 설계도 레이어 (기존 / AI 최적화 부스) -->
                    <div id="layoutLayer" class="absolute inset-0 z-10 pointer-events-none">
                        <!-- Dynamic Booth Canvas -->
                    </div>

                    <!-- 2. 인구 밀집도 히트맵 레이어 Canvas -->
                    <canvas id="heatmapCanvas" width="750" height="580" class="absolute inset-0 z-20 pointer-events-none opacity-80"></canvas>

                    <!-- 3. 관람객 동선 벡터 레이어 SVG -->
                    <svg id="flowSvg" class="absolute inset-0 w-full h-full z-30 pointer-events-none">
                        <!-- Dynamic SVG Paths -->
                    </svg>

                    <!-- 주출입구 / 출구 바 -->
                    <div class="absolute top-3 left-4 right-4 flex justify-between items-center z-40 pointer-events-none">
                        <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-door-open"></i> 주출입구
                        </span>
                        <span id="layoutStateBadge" class="bg-slate-800 text-slate-300 border border-slate-700 text-xs font-bold px-3 py-1 rounded-full shadow">
                            상태: 기존 설계도
                        </span>
                    </div>

                    <div class="absolute bottom-3 left-4 right-4 flex justify-between items-center z-40 pointer-events-none">
                        <span class="bg-amber-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1.5">
                            <i class="fa-solid fa-couch"></i> 휴게존 & 응급 메디컬
                        </span>
                        <span class="bg-slate-800 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                            주출구 <i class="fa-solid fa-arrow-right"></i>
                        </span>
                    </div>

                </div>

                <!-- 히트맵 범례 -->
                <div class="absolute bottom-6 right-6 bg-slate-900/90 backdrop-blur border border-slate-700 p-2.5 rounded-xl text-[11px] text-slate-300 shadow-xl z-50 pointer-events-none">
                    <div class="font-bold mb-1">인구 밀집도 (Density)</div>
                    <div class="w-32 h-2.5 rounded-full bg-gradient-to-r from-blue-500 via-green-400 via-yellow-400 to-red-500"></div>
                    <div class="flex justify-between text-[9px] text-slate-400 mt-1">
                        <span>쾌적</span>
                        <span>원활</span>
                        <span>혼잡</span>
                    </div>
                </div>

            </div>

        </section>
    </div>

    <!-- JavaScript Real Simulation Engine -->
    <script>
        let isAIOptimized = false;
        let currentTime = 14;

        // 1. 기존 부스 위치 설계도
        const originalBooths = [
            { id: 'b1', name: '메인 무대 (A)', type: 'main', x: 50, y: 60, w: 200, h: 100, icon: 'fa-star' },
            { id: 'b2', name: '인기 체험부스 (B)', type: 'popular', x: 270, y: 60, w: 180, h: 100, icon: 'fa-fire' }, // 병목 유발
            { id: 'b3', name: '전시 부스 (C)', type: 'normal', x: 470, y: 60, w: 180, h: 100, icon: 'fa-cube' },
            { id: 'b4', name: '약자 안내소', type: 'bf', x: 50, y: 220, w: 200, h: 90, icon: 'fa-wheelchair' },
            { id: 'b5', name: '이벤트 부스 (D)', type: 'normal', x: 270, y: 220, w: 180, h: 90, icon: 'fa-gift' },
            { id: 'b6', name: '푸드/카페 존', type: 'normal', x: 470, y: 220, w: 180, h: 90, icon: 'fa-utensils' }
        ];

        // 2. AI가 최적화한 부스 위치 설계도 (통로 확충 및 분산 배치)
        const aiOptimizedBooths = [
            { id: 'b1', name: '메인 무대 (A)', type: 'main', x: 40, y: 60, w: 200, h: 110, icon: 'fa-star' },
            { id: 'b2', name: '인기 체험부스 (B)', type: 'popular', x: 480, y: 60, w: 200, h: 110, icon: 'fa-fire' }, // 분산 이격 배치
            { id: 'b3', name: '전시 부스 (C)', type: 'normal', x: 260, y: 60, w: 200, h: 110, icon: 'fa-cube' },
            { id: 'b4', name: '약자 안내소', type: 'bf', x: 40, y: 240, w: 200, h: 100, icon: 'fa-wheelchair' },
            { id: 'b5', name: '이벤트 부스 (D)', type: 'normal', x: 260, y: 240, w: 200, h: 100, icon: 'fa-gift' },
            { id: 'b6', name: '푸드/카페 존', type: 'normal', x: 480, y: 240, w: 200, h: 100, icon: 'fa-utensils' }
        ];

        window.onload = () => {
            renderAllLayers();
        };

        function onTimeChange(val) {
            currentTime = parseInt(val);
            document.getElementById('timeDisplay').innerText = `${val}:00 ${val == 14 ? '(최고 피크 타임)' : ''}`;
            renderAllLayers();
        }

        // AI 공간 설계 토글 버튼
        function toggleAIOptimization() {
            isAIOptimized = !isAIOptimized;
            const btn = document.getElementById('btnAIToggle');
            const badge = document.getElementById('layoutStateBadge');

            if (isAIOptimized) {
                btn.className = "bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-5 py-2.5 rounded-xl text-xs shadow-lg transition flex items-center gap-2";
                btn.innerHTML = `<i class="fa-solid fa-rotate-left"></i> <span>기존 설계도로 복원</span>`;
                badge.className = "bg-emerald-950 text-emerald-300 border border-emerald-800 text-xs font-bold px-3 py-1 rounded-full shadow";
                badge.innerText = "상태: AI 최적화 설계도 적용됨";
            } else {
                btn.className = "bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold px-5 py-2.5 rounded-xl text-xs shadow-lg transition flex items-center gap-2";
                btn.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> <span>AI 공간 설계 자동 최적화 적용</span>`;
                badge.className = "bg-slate-800 text-slate-300 border border-slate-700 text-xs font-bold px-3 py-1 rounded-full shadow";
                badge.innerText = "상태: 기존 설계도";
            }

            renderAllLayers();
        }

        // 전체 레이어 통합 렌더링
        function renderAllLayers() {
            const currentBooths = isAIOptimized ? aiOptimizedBooths : originalBooths;
            
            renderLayoutLayer(currentBooths);
            renderHeatmapLayer(currentBooths);
            renderFlowLayer(currentBooths);
            updateMetrics();
        }

        // 1. 설계도 레이어 렌더링
        function renderLayoutLayer(booths) {
            const layer = document.getElementById('layoutLayer');
            layer.innerHTML = '';

            booths.forEach(b => {
                let cardStyle = "bg-slate-800/90 border-slate-600 text-slate-200";
                if (b.type === 'popular') cardStyle = "bg-amber-950/80 border-amber-500 text-amber-200";
                if (b.type === 'bf') cardStyle = "bg-emerald-950/80 border-emerald-500 text-emerald-200";

                layer.innerHTML += `
                    <div style="left: ${b.x}px; top: ${b.y}px; width: ${b.w}px; height: ${b.h}px; position: absolute;"
                         class="${cardStyle} border-2 rounded-xl p-3 shadow-lg flex flex-col justify-between">
                        <div class="flex justify-between items-center">
                            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-white/10 flex items-center gap-1">
                                <i class="fa-solid ${b.icon}"></i> ${b.name}
                            </span>
                        </div>
                        <div class="text-[10px] opacity-60">규격: ${b.w}x${b.h}</div>
                    </div>
                `;
            });
        }

        // 2. 인구 밀집도 히트맵 레이어 (Canvas 2D)
        function renderHeatmapLayer(booths) {
            const canvas = document.getElementById('heatmapCanvas');
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (!document.getElementById('toggleHeatmap').checked) return;

            // 시간대별 관람객 수 가중치
            const densityFactor = (currentTime / 14.0);

            booths.forEach(b => {
                let cx = b.x + b.w / 2;
                let cy = b.y + b.h / 2;
                
                let radius = (b.type === 'popular' && !isAIOptimized) ? 140 * densityFactor : 80 * densityFactor;
                let intensity = (b.type === 'popular' && !isAIOptimized) ? 0.7 : 0.4;

                const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
                if (b.type === 'popular' && !isAIOptimized) {
                    grad.addColorStop(0, `rgba(239, 68, 68, ${intensity})`); // Red (혼잡)
                    grad.addColorStop(0.5, `rgba(245, 158, 11, ${intensity * 0.6})`); // Yellow
                    grad.addColorStop(1, 'rgba(59, 130, 246, 0)');
                } else {
                    grad.addColorStop(0, `rgba(16, 185, 129, ${intensity})`); // Green (원활)
                    grad.addColorStop(0.6, `rgba(59, 130, 246, ${intensity * 0.4})`);
                    grad.addColorStop(1, 'rgba(59, 130, 246, 0)');
                }

                ctx.fillStyle = grad;
                ctx.beginPath();
                ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        // 3. 관람객 동선 레이어 (SVG)
        function renderFlowLayer(booths) {
            const svg = document.getElementById('flowSvg');
            svg.innerHTML = '';

            if (!document.getElementById('toggleFlow').checked) return;

            let pathD = `M 150 20 `;
            booths.forEach(b => {
                let cx = b.x + b.w / 2;
                let cy = b.y + b.h / 2;
                pathD += `L ${cx} ${cy} `;
            });
            pathD += `L 570 500`;

            const strokeColor = isAIOptimized ? "#10b981" : "#f59e0b";

            svg.innerHTML = `
                <path d="${pathD}" fill="none" stroke="${strokeColor}" stroke-width="3" class="flow-path" opacity="0.8" />
            `;

            booths.forEach(b => {
                let cx = b.x + b.w / 2;
                let cy = b.y + b.h / 2;
                svg.innerHTML += `<circle cx="${cx}" cy="${cy}" r="5" fill="${strokeColor}" />`;
            });
        }

        // 지표 업데이트
        function updateMetrics() {
            const riskElem = document.getElementById('valRisk');
            const flowElem = document.getElementById('valFlow');
            const textElem = document.getElementById('aiReportText');

            if (isAIOptimized) {
                riskElem.className = "text-base font-bold text-emerald-400 mt-1";
                riskElem.innerText = "8.2% (원활 및 안전)";
                flowElem.innerText = "96 점";
                textElem.innerText = "AI 최적화 배치가 적용되었습니다. 인기 부스의 거리가 이격되고 메인 통로 폭이 넓어져 병목 및 혼잡 위험이 해소되었습니다.";
            } else {
                riskElem.className = "text-base font-bold text-red-400 mt-1";
                riskElem.innerText = "42.5% (혼잡 경고)";
                flowElem.innerText = "68 점";
                textElem.innerText = "현재 배치 상태는 인기 부스 주변에 관람객이 집중되어 좁은 통로에서 병목 현상이 발생하고 있습니다. 상단의 'AI 공간 설계 자동 최적화' 버튼을 눌러 부스 배치를 재조정하세요.";
            }
        }
    </script>
</body>
</html>
"""

# Streamlit Component 실행
components.html(SIMULATOR_HTML, height=1000, scrolling=True)
