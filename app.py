<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 행사장 설계 및 동선 시뮬레이터</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        canvas { background-color: #f8fafc; border-radius: 0.5rem; }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col">

    <!-- 상단 헤더 -->
    <header class="bg-slate-800 border-b border-slate-700 px-6 py-4 flex justify-between items-center shadow-md">
        <div class="flex items-center space-x-3">
            <div class="bg-indigo-600 p-2 rounded-lg text-white font-bold">AI</div>
            <h1 class="text-xl font-bold tracking-tight">스마트 행사장 설계 및 동선 최적화 시스템</h1>
        </div>
        <div class="flex items-center space-x-4 text-sm">
            <span id="clock-display" class="bg-slate-700 px-3 py-1.5 rounded-md font-mono text-indigo-400 font-semibold">시간: 09:00</span>
            <span id="status-display" class="bg-emerald-900/50 text-emerald-300 border border-emerald-700 px-3 py-1.5 rounded-md">상태: 대기 중</span>
        </div>
    </header>

    <!-- 메인 대시보드 컨테이너 -->
    <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-4 gap-6 max-w-[1600px] mx-auto w-full">
        
        <!-- 좌측 제어 및 AI 어시스턴트 패널 (1칸) -->
        <section class="lg:col-span-1 flex flex-col space-y-6">
            <!-- 제어판 -->
            <div class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg">
                <h2 class="text-base font-semibold mb-4 text-indigo-300 border-b border-slate-700 pb-2">시뮬레이션 컨트롤</h2>
                <div class="space-y-4">
                    <div>
                        <label class="block text-xs text-slate-400 mb-1">시뮬레이션 속도</label>
                        <input id="speed-range" type="range" min="1" max="5" value="2" class="w-full accent-indigo-500">
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <button id="start-btn" onclick="startSimulation()" class="bg-indigo-600 hover:bg-indigo-500 text-white py-2 px-4 rounded-lg font-medium transition text-sm shadow">시뮬레이션 시작</button>
                        <button id="reset-btn" onclick="resetSimulation()" class="bg-slate-700 hover:bg-slate-600 text-slate-200 py-2 px-4 rounded-lg font-medium transition text-sm">초기화</button>
                    </div>
                </div>
            </div>

            <!-- 레이어 오버프 토글 -->
            <div class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg">
                <h2 class="text-base font-semibold mb-4 text-indigo-300 border-b border-slate-700 pb-2">온오프 레이어 시스템</h2>
                <div class="space-y-3 text-sm">
                    <label class="flex items-center justify-between cursor-pointer">
                        <span>동선 시각화 (Path)</span>
                        <input type="checkbox" id="toggle-path" checked onchange="toggleLayer('path')" class="w-4 h-4 accent-indigo-600 rounded">
                    </label>
                    <label class="flex items-center justify-between cursor-pointer">
                        <span>인구 밀집도 히트맵</span>
                        <input type="checkbox" id="toggle-heatmap" checked onchange="toggleLayer('heatmap')" class="w-4 h-4 accent-indigo-600 rounded">
                    </label>
                    <label class="flex items-center justify-between cursor-pointer">
                        <span>AI 최적화 가이드라인</span>
                        <input type="checkbox" id="toggle-ai-guide" checked onchange="toggleLayer('aiGuide')" class="w-4 h-4 accent-indigo-600 rounded">
                    </label>
                </div>
            </div>

            <!-- AI 어시스턴트 리포트 -->
            <div class="bg-slate-800 border border-slate-700 rounded-xl p-5 shadow-lg flex-1 flex flex-col">
                <h2 class="text-base font-semibold mb-3 text-indigo-300 border-b border-slate-700 pb-2">AI 실시간 피드백 및 리포트</h2>
                <div id="ai-report-box" class="flex-1 bg-slate-900/70 border border-slate-700/60 rounded-lg p-3 text-xs text-slate-300 overflow-y-auto space-y-2 font-mono">
                    <p class="text-indigo-400">[09:00] 시스템 초기화 완료. 행사장 배치가 최적화 상태입니다.</p>
                </div>
            </div>
        </section>

        <!-- 우측 캔버스 및 시각화 영역 (3칸) -->
        <section class="lg:col-span-3 flex flex-col space-y-4">
            <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 shadow-lg flex justify-between items-center">
                <div class="text-sm text-slate-300">
                    💡 <span class="font-medium text-white">가이드:</span> 부스는 드래그하여 이동할 수 있으며, 시간 흐름에 따른 관람객 밀집도와 병목 현상을 실시간으로 분석합니다.
                </div>
                <div class="flex items-center space-x-4 text-xs">
                    <div class="flex items-center space-x-1"><span class="w-3 h-3 bg-blue-500 rounded-full inline-block"></span><span>일반 관람객</span></div>
                    <div class="flex items-center space-x-1"><span class="w-3 h-3 bg-amber-500 rounded-full inline-block"></span><span>VIP 관람객</span></div>
                    <div class="flex items-center space-x-1"><span class="w-3 h-3 bg-rose-500 rounded-full inline-block"></span><span>혼잡 구역</span></div>
                </div>
            </div>

            <!-- 캔버스 영역 -->
            <div class="bg-slate-800 border border-slate-700 rounded-xl p-4 shadow-lg flex justify-center items-center relative overflow-hidden">
                <canvas id="simCanvas" width="900" height="600" class="shadow-inner cursor-crosshair"></canvas>
            </div>
        </section>

    </main>

    <!-- 자바스크립트 시뮬레이션 로직 -->
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');

        // 상태 변수
        let isRunning = false;
        let simTime = 9 * 60; // 09:00 분 단위 표현 (540분)
        let visitors = [];
        let booths = [
            { id: 1, name: '메인 스테이지', x: 100, y: 100, width: 180, height: 100, color: '#4f46e5' },
            { id: 2, name: '기업 홍보관 A', x: 350, y: 100, width: 140, height: 100, color: '#0ea5e9' },
            { id: 3, name: '신기술 체험존', x: 550, y: 100, width: 220, height: 100, color: '#10b981' },
            { id: 4, name: '스타트업 파빌리온', x: 100, y: 350, width: 280, height: 120, color: '#f59e0b' },
            { id: 5, name: '휴게 및 식음료', x: 450, y: 350, width: 320, height: 120, color: '#ec4899' }
        ];

        let layers = {
            path: true,
            heatmap: true,
            aiGuide: true
        };

        let selectedBooth = null;
        let isDragging = false;
        let dragOffsetX = 0;
        let dragOffsetY = 0;

        // 레이어 토글 함수
        function toggleLayer(layerName) {
            layers[layerName] = document.getElementById(`toggle-${layerName}`).checked;
        }

        // 마우스 이벤트 (부스 드래그 앤 드롭 구현)
        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            booths.forEach(booth => {
                if (mouseX >= booth.x && mouseX <= booth.x + booth.width &&
                    mouseY >= booth.y && mouseY <= booth.y + booth.height) {
                    selectedBooth = booth;
                    isDragging = true;
                    dragOffsetX = mouseX - booth.x;
                    dragOffsetY = mouseY - booth.y;
                }
            });
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging || !selectedBooth) return;
            const rect = canvas.getBoundingClientRect();
            selectedBooth.x = e.clientX - rect.left - dragOffsetX;
            selectedBooth.y = e.clientY - rect.top - dragOffsetY;
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
            selectedBooth = null;
        });

        // 관람객 생성 함수 (시간대별 변수 반영)
        function spawnVisitors() {
            // 시간대별 유입 인원 조절 (점심시간 12:00~13:00 감소, 오후 14:00 피크)
            let hour = simTime / 60;
            let spawnRate = 0.5;
            if (hour >= 10 && hour <= 11) spawnRate = 1.5;
            if (hour >= 12 && hour < 13) spawnRate = 0.2; // 점심 시간
            if (hour >= 13 && hour <= 15) spawnRate = 2.0; // 오후 피크

            if (Math.random() < spawnRate && visitors.size < 150) {
                let targetBooth = booths[Math.floor(Math.random() * booths.length)];
                visitors.push({
                    x: Math.random() * 50 + 20,
                    y: Math.random() * 50 + 500,
                    targetX: targetBooth.x + targetBooth.width / 2,
                    targetY: targetBooth.y + targetBooth.height / 2,
                    speed: Math.random() * 1.5 + 1,
                    type: Math.random() > 0.2 ? 'normal' : 'vip',
                    pathHistory: []
                });
            }
        }

        // 시뮬레이션 루프 업데이트
        function updateSimulation() {
            if (!isRunning) return;

            // 시간 증가 (속도 슬라이더 연동)
            let speedVal = parseInt(document.getElementById('speed-range').value);
            simTime += speedVal;

            if (simTime >= 18 * 60) {
                isRunning = false;
                document.getElementById('status-display').innerText = '상태: 시뮬레이션 종료';
                document.getElementById('status-display').className = 'bg-amber-900/50 text-amber-300 border border-amber-700 px-3 py-1.5 rounded-md';
                addLog('시뮬레이션이 종료되었습니다. 하루 동안의 누적 동선 데이터가 산출되었습니다.');
                return;
            }

            // 시간 표시 갱신
            let h = Math.floor(simTime / 60);
            let m = simTime % 60;
            document.getElementById('clock-display').innerText = `시간: ${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;

            spawnVisitors();

            // 관람객 이동 업데이트
            visitors.forEach((v, index) => {
                let dx = v.targetX - v.x;
                let dy = v.targetY - v.y;
                let dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 5) {
                    // 목적지 도착 시 다른 부스로 재설정 혹은 퇴장
                    let nextBooth = booths[Math.floor(Math.random() * booths.length)];
                    v.targetX = nextBooth.x + nextBooth.width / 2;
                    v.targetY = nextBooth.y + nextBooth.height / 2;
                } else {
                    v.x += (dx / dist) * v.speed;
                    v.y += (dy / dist) * v.speed;
                }

                // 동선 기록 저장 (최근 20개)
                if (layers.path) {
                    v.pathHistory.push({x: v.x, y: v.y});
                    if (v.pathHistory.length > 20) v.pathHistory.shift();
                }
            });

            // 주기적인 AI 분석 리포트 추가
            if (simTime === 11 * 60) addLog('[11:00] 오전 피크 타임 진입: 신기술 체험존 주변 병목 현상 감지.');
            if (simTime === 13 * 60) addLog('[13:00] 점심 시간대: 휴게 및 식음료 구역 집중도 급증.');
            if (simTime === 14 * 30) addLog('[14:30] AI 최적화 제안: 메인 스테이지 통로 폭을 15% 확장 권장.');
        }

        function addLog(text) {
            const box = document.getElementById('ai-report-box');
            box.innerHTML += `<p class="text-slate-300">${text}</p>`;
            box.scrollTop = box.scrollHeight;
        }

        // 렌더링 함수
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. 히트맵 레이어 렌더링
            if (layers.heatmap) {
                visitors.forEach(v => {
                    let gradient = ctx.createRadialGradient(v.x, v.y, 2, v.x, v.y, 25);
                    gradient.addColorStop(0, 'rgba(239, 68, 68, 0.15)');
                    gradient.addColorStop(1, 'rgba(239, 68, 68, 0)');
                    ctx.fillStyle = gradient;
                    ctx.beginPath();
                    ctx.arc(v.x, v.y, 25, 0, Math.PI * 2);
                    ctx.fill();
                });
            }

            // 2. 동선(Path) 레이어 렌더링
            if (layers.path) {
                ctx.lineWidth = 1;
                visitors.forEach(v => {
                    if (v.pathHistory.length > 1) {
                        ctx.beginPath();
                        ctx.moveTo(v.pathHistory[0].x, v.pathHistory[0].y);
                        for (let i = 1; i < v.pathHistory.length; i++) {
                            ctx.lineTo(v.pathHistory[i].x, v.pathHistory[i].y);
                        }
                        ctx.strokeStyle = 'rgba(99, 102, 241, 0.15)';
                        ctx.stroke();
                    }
                });
            }

            // 3. AI 최적화 가이드라인 렌더링
            if (layers.aiGuide) {
                ctx.strokeStyle = 'rgba(16, 185, 129, 0.4)';
                ctx.setLineDash([5, 5]);
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(50, 300);
                ctx.lineTo(850, 300);
                ctx.stroke();
                ctx.setLineDash([]); // 리셋
            }

            // 4. 부스 렌더링
            booths.forEach(booth => {
                ctx.fillStyle = booth.color;
                ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
                ctx.shadowBlur = 10;
                ctx.fillRect(booth.x, booth.y, booth.width, booth.height);
                ctx.shadowBlur = 0; // 섀도우 초기화

                // 부스 테두리
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.strokeRect(booth.x, booth.y, booth.width, booth.height);

                // 부스 텍스트
                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 13px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(booth.name, booth.x + booth.width / 2, booth.y + booth.height / 2 + 5);
            });

            // 5. 관람객 입자 렌더링
            visitors.forEach(v => {
                ctx.fillStyle = v.type === 'vip' ? '#f59e0b' : '#3b82f6';
                ctx.beginPath();
                ctx.arc(v.x, v.y, 4, 0, Math.PI * 2);
                ctx.fill();
            });
        }

        // 제어 버튼 액션
        function startSimulation() {
            isRunning = true;
            document.getElementById('status-display').innerText = '상태: 시뮬레이션 구동 중';
            document.getElementById('status-display').className = 'bg-emerald-900/50 text-emerald-300 border border-emerald-700 px-3 py-1.5 rounded-md';
        }

        function resetSimulation() {
            isRunning = false;
            simTime = 9 * 60;
            visitors = [];
            document.getElementById('clock-display').innerText = '시간: 09:00';
            document.getElementById('status-display').innerText = '상태: 대기 중';
            document.getElementById('status-display').className = 'bg-slate-700 text-slate-300 px-3 py-1.5 rounded-md';
            document.getElementById('ai-report-box').innerHTML = '<p class="text-indigo-400">[09:00] 시스템 초기화 완료. 행사장 배치가 최적화 상태입니다.</p>';
        }

        // 애니메이션 루프 실행
        function loop() {
            updateSimulation();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
