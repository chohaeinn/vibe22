<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 배리어프리 공간 & 동선 최적화 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen font-sans">

    <!-- Header -->
    <header class="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white p-6 shadow-lg">
        <div class="max-w-7xl mx-mx-auto flex justify-between items-center px-4">
            <div>
                <h1 class="text-2xl font-bold flex items-center gap-2">
                    <i class="fa-solid fa-wand-magic-sparkles text-yellow-300"></i> AI 공간 & 동선 최적화 시뮬레이터
                </h1>
                <p class="text-indigo-100 text-sm mt-1">사회적 약자 배려(Barrier-Free) 및 병목 제로 순환 동선 설계 시스템</p>
            </div>
            <span class="bg-white/20 px-3 py-1 rounded-full text-xs font-semibold backdrop-blur-md">v2.4 Smart Optimizer</span>
        </div>
    </header>

    <main class="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 1. 좌측 설정 옵션 패널 (12컬럼 중 4) -->
        <section class="lg:col-span-4 bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-col gap-5">
            <h2 class="text-lg font-bold text-slate-800 border-b pb-3 flex items-center gap-2">
                <i class="fa-solid fa-sliders text-indigo-500"></i> 시뮬레이션 옵션 설정
            </h2>

            <!-- 행사 유형 -->
            <div>
                <label class="block text-xs font-bold text-slate-600 uppercase mb-2">행사 / 공간 성격</label>
                <select id="eventType" onchange="updateSimulation()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 outline-none">
                    <option value="popup">팝업 스토어 & 체험존</option>
                    <option value="exhibition">학술 / 전시 컨퍼런스</option>
                    <option value="festival">주민 & 복지 축제</option>
                    <option value="jobfair">박람회 / 채용 설명회</option>
                </select>
            </div>

            <!-- 관람객 타깃 -->
            <div>
                <label class="block text-xs font-bold text-slate-600 uppercase mb-2">주요 방문객 타깃</label>
                <select id="targetAudience" onchange="updateSimulation()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 outline-none">
                    <option value="all">전 연령층 (가족 단위)</option>
                    <option value="accessible">장애인 & 교통약자 중심 (High Barrier-Free)</option>
                    <option value="senior">고령층 중심 (휴게존 확장)</option>
                    <option value="youth">학생 & 청년층</option>
                </select>
            </div>

            <!-- 동선 모드 -->
            <div>
                <label class="block text-xs font-bold text-slate-600 uppercase mb-2">동선 설계 알고리즘</label>
                <div class="grid grid-cols-3 gap-2">
                    <button onclick="setRoute('loop')" id="btn-loop" class="route-btn active p-2 border rounded-xl text-xs font-medium bg-indigo-50 border-indigo-500 text-indigo-700 flex flex-col items-center gap-1">
                        <i class="fa-solid fa-arrows-spin text-base"></i> 순환형 (Loop)
                    </button>
                    <button onclick="setRoute('grid')" id="btn-grid" class="route-btn p-2 border rounded-xl text-xs font-medium bg-slate-50 border-slate-200 text-slate-600 flex flex-col items-center gap-1">
                        <i class="fa-solid fa-border-all text-base"></i> 격자형 (Grid)
                    </button>
                    <button onclick="setRoute('radial')" id="btn-radial" class="route-btn p-2 border rounded-xl text-xs font-medium bg-slate-50 border-slate-200 text-slate-600 flex flex-col items-center gap-1">
                        <i class="fa-solid fa-sun text-base"></i> 방사형 (Radial)
                    </button>
                </div>
            </div>

            <!-- 사용자 커스텀 부스 추가 입력 -->
            <div class="border-t pt-4">
                <label class="block text-xs font-bold text-slate-600 uppercase mb-2">직접 추가할 부스/시설</label>
                <div class="flex gap-2">
                    <input type="text" id="customBoothInput" placeholder="예: 수어통역 부스, 팝업존" class="flex-1 p-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm outline-none focus:ring-2 focus:ring-indigo-500">
                    <button onclick="addCustomBooth()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl text-sm font-bold shadow-md transition">
                        추가
                    </button>
                </div>
                <!-- 추가된 부스 태그 목록 -->
                <div id="boothTags" class="flex flex-wrap gap-2 mt-3">
                    <!-- Dynamic Tags -->
                </div>
            </div>

            <!-- 배리어프리 특별 옵션 체크박스 -->
            <div class="border-t pt-4 flex flex-col gap-2">
                <span class="text-xs font-bold text-slate-600 uppercase">약자 배려 세부 설정</span>
                <label class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkPathWidth" checked onchange="updateSimulation()" class="w-4 h-4 text-indigo-600 rounded">
                    통로 폭 최소 2.0m 이상 확보 (휠체어 교행)
                </label>
                <label class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
                    <input type="checkbox" id="chkBraille" checked onchange="updateSimulation()" class="w-4 h-4 text-indigo-600 rounded">
                    점자/음성 안내선 및 낮은 데스크 적용
                </label>
            </div>
        </section>


        <!-- 2. 우측 시뮬레이션 & 시각화 영역 (12컬럼 중 8) -->
        <section class="lg:col-span-8 flex flex-col gap-6">

            <!-- 실시간 메트릭 카드 -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center text-lg"><i class="fa-solid fa-universal-access"></i></div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">배리어프리 지수</div>
                        <div id="metricBF" class="text-xl font-bold text-emerald-600">98 / 100</div>
                    </div>
                </div>

                <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center text-lg"><i class="fa-solid fa-person-walking"></i></div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">동선 효율성</div>
                        <div id="metricFlow" class="text-xl font-bold text-indigo-600">원활 (순환)</div>
                    </div>
                </div>

                <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center text-lg"><i class="fa-solid fa-ruler-horizontal"></i></div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">최소 통로 폭</div>
                        <div id="metricWidth" class="text-xl font-bold text-amber-600">2.2 m</div>
                    </div>
                </div>

                <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center text-lg"><i class="fa-solid fa-store"></i></div>
                    <div>
                        <div class="text-xs text-slate-500 font-medium">총 배치 부스</div>
                        <div id="metricCount" class="text-xl font-bold text-purple-600">7 개</div>
                    </div>
                </div>
            </div>

            <!-- 공간 레이아웃 도면 캔버스 / 시뮬레이터 -->
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 relative">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="font-bold text-slate-800 flex items-center gap-2">
                        <i class="fa-solid fa-map text-indigo-500"></i> AI 배치 2D 시뮬레이션 맵
                    </h3>
                    <div class="flex gap-2 text-xs">
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span> 배리어프리존</span>
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-indigo-500 inline-block"></span> 메인부스</span>
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-pink-500 inline-block"></span> 사용자부스</span>
                    </div>
                </div>

                <!-- 2D 시각화 구역 (Grid) -->
                <div id="layoutMap" class="w-full h-80 bg-slate-100 rounded-xl border-2 border-dashed border-slate-300 p-4 relative overflow-hidden flex flex-col justify-between">
                    
                    <!-- 입구 영역 -->
                    <div class="flex justify-between items-center border-b border-slate-300 pb-2">
                        <span class="bg-emerald-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                            <i class="fa-solid fa-door-open"></i> 주출입구 (경사로 & 낮은 안내데스크)
                        </span>
                        <span class="text-xs text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                            통로 2.4m 확보
                        </span>
                    </div>

                    <!-- 중앙 배치 부스들 (Dynamically Rendered) -->
                    <div id="boothGrid" class="grid grid-cols-2 md:grid-cols-4 gap-3 my-auto">
                        <!-- JS로 부스 카드들이 생성됨 -->
                    </div>

                    <!-- 출구 & 쉼터 영역 -->
                    <div class="flex justify-between items-center border-t border-slate-300 pt-2">
                        <span class="bg-amber-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                            <i class="fa-solid fa-couch"></i> 감각 안심 쉼터 & 응급 메디컬존
                        </span>
                        <span class="bg-slate-700 text-white text-xs font-bold px-3 py-1 rounded-full shadow flex items-center gap-1">
                            출구 <i class="fa-solid fa-arrow-right"></i>
                        </span>
                    </div>

                    <!-- 동선 화살표 오버레이 (순환형 표시) -->
                    <div class="absolute inset-0 pointer-events-none opacity-20 flex items-center justify-center">
                        <i class="fa-solid fa-arrows-spin text-9xl text-indigo-600 animate-spin-slow"></i>
                    </div>
                </div>
            </div>

            <!-- 시뮬레이션 설명 요약 리포트 -->
            <div class="bg-indigo-50/50 border border-indigo-100 rounded-2xl p-5 text-sm">
                <h4 class="font-bold text-indigo-900 mb-2 flex items-center gap-2">
                    <i class="fa-solid fa-lightbulb text-indigo-600"></i> AI 최적화 포인트 요약
                </h4>
                <ul class="list-disc list-inside text-indigo-950 space-y-1 text-xs md:text-sm">
                    <li><strong>병목 제로 순환 구조:</strong> 입구 ➔ 스마트 안내 ➔ 메인/체험 부스 ➔ 약자 쉼터 ➔ 출구 순으로 일방통행 흐름을 유도합니다.</li>
                    <li><strong>Barrier-Free 스펙 적용:</strong> 단차(턱)를 완전히 제거하고 휠체어 반경(1.5m) 이상의 수회전 공간을 확보했습니다.</li>
                    <li><strong>사용자 맞춤 부스 동적 배치:</strong> 추가 입력된 부스는 접근성이 가장 높은 중앙 메인 동선에 자동 정렬됩니다.</li>
                </ul>
            </div>
        </section>
    </main>

    <!-- JavaScript Logic -->
    <script>
        // 초기 상태
        let currentRoute = 'loop';
        let customBooths = ['스마트 안내 & 휠체어 대여', '인터랙티브 포토존'];

        // 기본 추천 부스 데이터
        const defaultBooths = [
            { name: '스마트 안내 부스', type: 'bf', icon: 'fa-wheelchair' },
            { name: '메인 체험 부스 A', type: 'main', icon: 'fa-star' },
            { name: '메인 체험 부스 B', type: 'main', icon: 'fa-cube' },
            { name: '감각 안심 휴게존', type: 'bf', icon: 'fa-heart' },
        ];

        // 초기화
        window.onload = () => {
            renderBoothTags();
            updateSimulation();
        };

        // 동선 버튼 변경
        function setRoute(mode) {
            currentRoute = mode;
            document.querySelectorAll('.route-btn').forEach(btn => {
                btn.classList.remove('bg-indigo-50', 'border-indigo-500', 'text-indigo-700');
                btn.classList.add('bg-slate-50', 'border-slate-200', 'text-slate-600');
            });
            const activeBtn = document.getElementById(`btn-${mode}`);
            activeBtn.classList.remove('bg-slate-50', 'border-slate-200', 'text-slate-600');
            activeBtn.classList.add('bg-indigo-50', 'border-indigo-500', 'text-indigo-700');
            
            updateSimulation();
        }

        // 커스텀 부스 추가
        function addCustomBooth() {
            const input = document.getElementById('customBoothInput');
            const value = input.value.trim();
            if (value) {
                customBooths.push(value);
                input.value = '';
                renderBoothTags();
                updateSimulation();
            }
        }

        // 커스텀 부스 삭제
        function removeCustomBooth(index) {
            customBooths.splice(index, 1);
            renderBoothTags();
            updateSimulation();
        }

        // 부스 태그 렌더링
        function renderBoothTags() {
            const container = document.getElementById('boothTags');
            container.innerHTML = customBooths.map((booth, idx) => `
                <span class="bg-pink-50 border border-pink-200 text-pink-700 text-xs px-2.5 py-1 rounded-full flex items-center gap-1 shadow-sm">
                    ${booth}
                    <button onclick="removeCustomBooth(${idx})" class="hover:text-pink-900 font-bold ml-1">×</button>
                </span>
            `).join('');
        }

        // 시뮬레이션 계산 및 뷰 업데이트
        function updateSimulation() {
            const target = document.getElementById('targetAudience').value;
            const chkWidth = document.getElementById('chkPathWidth').checked;

            // 1. 메트릭 업데이트
            let bfScore = 90;
            if (target === 'accessible') bfScore += 8;
            if (chkWidth) bfScore += 2;
            document.getElementById('metricBF').innerText = `${bfScore} / 100`;

            document.getElementById('metricWidth').innerText = chkWidth ? '2.2 m' : '1.5 m';

            let flowText = '순환형 (원활)';
            if (currentRoute === 'grid') flowText = '격자형 (보통)';
            if (currentRoute === 'radial') flowText = '방사형 (집중)';
            document.getElementById('metricFlow').innerText = flowText;

            const totalBoothsCount = defaultBooths.length + customBooths.length;
            document.getElementById('metricCount').innerText = `${totalBoothsCount} 개`;

            // 2. 맵 캔버스 부스 카드 렌더링
            const gridContainer = document.getElementById('boothGrid');
            gridContainer.innerHTML = '';

            // 기본 부스 출력
            defaultBooths.forEach(b => {
                const color = b.type === 'bf' ? 'bg-emerald-50 border-emerald-300 text-emerald-800' : 'bg-indigo-50 border-indigo-300 text-indigo-800';
                gridContainer.innerHTML += `
                    <div class="p-3 rounded-xl border ${color} text-xs font-bold flex flex-col items-center justify-center gap-1 shadow-sm text-center">
                        <i class="fa-solid ${b.icon} text-base"></i>
                        ${b.name}
                    </div>
                `;
            });

            // 커스텀 부스 출력
            customBooths.forEach(cName => {
                gridContainer.innerHTML += `
                    <div class="p-3 rounded-xl border bg-pink-50 border-pink-300 text-pink-800 text-xs font-bold flex flex-col items-center justify-center gap-1 shadow-sm text-center">
                        <i class="fa-solid fa-puzzle-piece text-base"></i>
                        ${cName}
                    </div>
                `;
            });
        }
    </script>
</body>
</html>
