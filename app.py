<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event AI - 스마트 행사장 설계 및 동선 최적화 시스템</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #0f172a; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    </style>
</head>
<body class="bg-[#0b0f19] text-slate-100 font-sans min-h-screen flex">

    <!-- 좌측 사이드바 -->
    <aside class="w-64 bg-[#111827] border-r border-slate-800 flex flex-col justify-between hidden md:flex shrink-0">
        <div>
            <!-- 로고 영역 -->
            <div class="p-5 flex items-center space-x-3 border-b border-slate-800">
                <div class="bg-indigo-600 p-2 rounded-xl text-white font-bold flex items-center justify-center shadow-lg shadow-indigo-500/30">AI</div>
                <div>
                    <h1 class="font-bold text-base tracking-tight text-white">Event AI</h1>
                    <p class="text-xs text-slate-400">AI 기반 행사 기획 및 동선 분석</p>
                </div>
            </div>
            <!-- 네비게이션 메뉴 -->
            <nav class="p-4 space-y-1.5 text-sm">
                <a href="#" class="flex items-center space-x-3 px-3 py-2.5 rounded-lg bg-indigo-600 text-white font-medium shadow-md shadow-indigo-600/20"><span class="text-lg">📊</span><span>행사 설계</span></a>
                <a href="#" class="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 transition"><span class="text-lg">⚙️</span><span>설계 프로세스</span></a>
                <a href="#" class="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 transition"><span class="text-lg">🗺️</span><span>부스 상세 관리</span></a>
                <a href="#" class="flex items-center space-x-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 transition"><span class="text-lg">👤</span><span>마이페이지</span></a>
            </nav>
        </div>
        <!-- 하단 유저 프로필 -->
        <div class="p-4 border-t border-slate-800">
            <div class="bg-slate-800/50 p-3 rounded-xl flex items-center space-x-3 border border-slate-700/50">
                <div class="w-9 h-9 rounded-full bg-indigo-500 flex items-center justify-center font-bold text-white text-sm shadow">주</div>
                <div class="overflow-hidden">
                    <p class="text-sm font-medium text-white truncate">주현님</p>
                    <p class="text-xs text-indigo-400 truncate">로그인됨</p>
                </div>
            </div>
        </div>
    </aside>

    <!-- 메인 콘텐츠 영역 -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
        
        <!-- 상단 헤더 -->
        <header class="bg-[#111827] border-b border-slate-800 px-6 py-4 flex justify-between items-center shadow-sm">
            <div class="flex items-center space-x-4">
                <h2 class="text-lg font-bold text-white">행사 설계</h2>
                <span class="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">행사 정보를 입력하여 AI 최적의 행사장을 설계해드립니다.</span>
            </div>
            <div class="flex items-center space-x-3">
                <span id="clock-display" class="bg-indigo-950/60 text-indigo-300 border border-indigo-800/60 px-3 py-1.5 rounded-lg font-mono text-xs font-bold">시간: 09:00</span>
                <button onclick="triggerAiRedesign()" class="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3.5 py-2 rounded-lg font-medium transition shadow-lg shadow-indigo-600/20 flex items-center space-x-1.5">
                    <span>✨ AI 행사장 설계하기</span>
                </button>
            </div>
        </header>

        <!-- 스크롤 가능한 대시보드 본문 -->
        <main class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
            
            <!-- 1. 행사 기본 정보 바 -->
            <div class="bg-[#111827] border border-slate-800 rounded-xl p-4 shadow-sm grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-4 text-center divide-y sm:divide-y-0 sm:divide-x divide-slate-800">
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">행사명</p><p class="text-xs font-bold text-white mt-1">2026 통합 엑스포</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">홀 규모</p><p class="text-xs font-bold text-white mt-1">4홀</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">행사 형태</p><p class="text-xs font-bold text-white mt-1">야외 겸 실내형 & 청년 소통</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">목표 인원</p><p class="text-xs font-bold text-white mt-1">5,000명</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">소요 시간</p><p class="text-xs font-bold text-white mt-1">9시간</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">예산 규모</p><p class="text-xs font-bold text-white mt-1">5,000만원</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">핵심 공간</p><p class="text-xs font-bold text-white mt-1">메인 스테이지</p></div>
                <div class="pt-2 sm:pt-0"><p class="text-[11px] text-slate-400">종합 평가</p><p class="text-xs font-bold text-emerald-400 mt-1">매우 우수</p></div>
            </div>

            <!-- 2. 행사장 배치도 및 히트맵 뷰 (2열 구조) -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                
                <!-- 행사장 배치도 (시뮬레이터 연동) -->
                <div class="bg-[#111827] border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col">
                    <div class="flex justify-between items-center mb-4 pb-2 border-b border-slate-800">
                        <div class="flex items-center space-x-2">
                            <span class="text-base">🗺️</span>
                            <h3 class="font-bold text-sm text-white">행사장 배치도 (디지털 조감 커스텀)</h3>
                        </div>
                        <div class="flex items-center space-x-2">
                            <button onclick="toggleSimState()" id="sim-control-btn" class="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1.5 rounded-md font-medium transition shadow">시뮬레이션 시작</button>
                            <span class="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">드래그 이동 가능</span>
                        </div>
                    </div>
                    <div class="relative flex-1 flex items-center justify-center bg-[#090d16] rounded-lg border border-slate-800/80 p-2 overflow-hidden min-h-[360px]">
                        <canvas id="simCanvas" width="560" height="340" class="rounded shadow-inner cursor-crosshair w-full h-auto max-w-full"></canvas>
                        <!-- 실시간 범례 오버레이 -->
                        <div class="absolute bottom-3 left-3 bg-slate-900/90 backdrop-blur border border-slate-700/60 p-2 rounded-lg text-[10px] space-y-1">
                            <div class="flex items-center space-x-2"><span class="w-2.5 h-2.5 bg-blue-500 rounded-full"></span><span class="text-slate-300">일반 관람객</span></div>
                            <div class="flex items-center space-x-2"><span class="w-2.5 h-2.5 bg-amber-500 rounded-full"></span><span class="text-slate-300">VIP 관람객</span></div>
                            <div class="flex items-center space-x-2"><span class="w-2.5 h-2.5 bg-rose-500 rounded-full"></span><span class="text-slate-300">혼잡 밀집 구역</span></div>
                        </div>
                    </div>
                </div>

                <!-- 히트맵 뷰 (실시간 동기화) -->
                <div class="bg-[#111827] border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col">
                    <div class="flex justify-between items-center mb-4 pb-2 border-b border-slate-800">
                        <div class="flex items-center space-x-2">
                            <span class="text-base">🔥</span>
                            <h3 class="font-bold text-sm text-white">혼잡도 Heatmap</h3>
                        </div>
                        <div class="flex items-center space-x-3 text-xs text-slate-400">
                            <span class="flex items-center space-x-1"><span class="w-2 h-2 rounded-full bg-blue-500"></span><span>여유</span></span>
                            <span class="flex items-center space-x-1"><span class="w-2 h-2 rounded-full bg-yellow-500"></span><span>보통</span></span>
                            <span class="flex items-center space-x-1"><span class="w-2 h-2 rounded-full bg-red-500"></span><span>혼잡</span></span>
                        </div>
                    </div>
                    <div class="relative flex-1 flex items-center justify-center bg-[#090d16] rounded-lg border border-slate-800/80 p-2 overflow-hidden min-h-[360px]">
                        <canvas id="heatmapCanvas" width="560" height="340" class="rounded shadow-inner w-full h-auto max-w-full"></canvas>
                        <div class="absolute bottom-3 right-3 bg-slate-900/90 backdrop-blur border border-slate-700/60 px-3 py-1.5 rounded-lg text-[11px] text-indigo-300 font-mono" id="heatmap-status-text">
                            상태: 시뮬레이션 대기 중 (동기화됨)
                        </div>
                    </div>
                </div>

            </div>

            <!-- 3. AI 평가 결과 및 개선사항 패널 -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- AI 평가 점수 -->
                <div class="bg-[#111827] border border-slate-800 rounded-xl p-5 shadow-sm">
                    <h3 class="font-bold text-sm text-white mb-4 pb-2 border-b border-slate-800 flex items-center space-x-2">
                        <span>💡</span><span>AI 평가 결과</span>
                    </h3>
                    <div class="space-y-3 text-xs">
                        <div class="flex justify-between items-center bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                            <span class="text-slate-300">안전성</span>
                            <div class="flex items-center space-x-3"><span class="font-bold text-white">92점</span><span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">매우 우수</span></div>
                        </div>
                        <div class="flex justify-between items-center bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                            <span class="text-slate-300">동선 효율성</span>
                            <div class="flex items-center space-x-3"><span class="font-bold text-white" id="score-efficiency">87점</span><span class="bg-indigo-950 text-indigo-400 border border-indigo-800 px-2 py-0.5 rounded text-[10px]">우수</span></div>
                        </div>
                        <div class="flex justify-between items-center bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                            <span class="text-slate-300">접근성</span>
                            <div class="flex items-center space-x-3"><span class="font-bold text-white">94점</span><span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">매우 우수</span></div>
                        </div>
                        <div class="flex justify-between items-center bg-slate-800/40 p-2.5 rounded-lg border border-slate-700/40">
                            <span class="text-slate-300">조밀도 최적화</span>
                            <div class="flex items-center space-x-3"><span class="font-bold text-white">84점</span><span class="bg-indigo-950 text-indigo-400 border border-indigo-800 px-2 py-0.5 rounded text-[10px]">우수</span></div>
                        </div>
                    </div>
                </div>

                <!-- AI 개선 맞춤 제안 -->
                <div class="lg:col-span-2 bg-[#111827] border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between">
                    <div>
                        <h3 class="font-bold text-sm text-white mb-4 pb-2 border-b border-slate-800 flex items-center space-x-2">
                            <span>🛠️</span><span>AI 개선 맞춤사항</span>
                        </h3>
                        <ul class="space-y-2.5 text-xs text-slate-300" id="ai-suggestions-list">
                            <li class="flex items-start space-x-2"><span class="text-emerald-400 font-bold">•</span><span>공간 배치 최적화: 시뮬레이션 시간대별 이동 동선과 부스 유입율이 정확히 일치하도록 동기화되었습니다.</span></li>
                            <li class="flex items-start space-x-2"><span class="text-emerald-400 font-bold">•</span><span>오전 개막 러시 타임(10:00)에는 메인 스테이지 주변 집중도가 가중됩니다.</span></li>
                            <li class="flex items-start space-x-2"><span class="text-emerald-400 font-bold">•</span><span>점심 시간(12:00~13:00)에는 식음료 및 휴게 부스로 관람객 이동이 쏠리는 현상이 시뮬에 반영됩니다.</span></li>
                            <li class="flex items-start space-x-2"><span class="text-emerald-400 font-bold">•</span><span>오후 피크(14:00 이후) 신기술 체험존의 병목 현상에 대비해 우회 통로 확보를 권장합니다.</span></li>
                        </ul>
                    </div>
                    <div class="mt-4 pt-3 border-t border-slate-800/60 flex justify-between items-center text-[11px] text-slate-400">
                        <span>💡 실시간 시뮬레이션 피드백이 완벽 동기화 적용 중입니다.</span>
                        <button onclick="addAiLog()" class="text-indigo-400 hover:text-indigo-300 font-medium underline">수동 리포트 갱신</button>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <!-- 스크립트: 시뮬레이션 및 히트맵 동기화 로직 -->
    <script>
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const heatCanvas = document.getElementById('heatmapCanvas');
        const heatCtx = heatCanvas.getContext('2d');

        let isRunning = false;
        let simTime = 9 * 60; // 09:00 (분 단위)
        let visitors = [];

        // 행사장 부스 객체 (시뮬레이션과 히트맵 좌표 공유)
        let booths = [
            { id: 1, name: '메인 스테이지', x: 180, y: 30, width: 200, height: 70, color: '#4f46e5' },
            { id: 2, name: '기업 홍보관 A', x: 40, y: 130, width: 120, height: 90, color: '#0ea5e9' },
            { id: 3, name: '신기술 체험존', x: 400, y: 130, width: 130, height: 90, color: '#10b981' },
            { id: 4, name: '스타트업 파빌리온', x: 40, y: 240, width: 200, height: 70, color: '#f59e0b' },
            { id: 5, name: '휴게 및 식음료', x: 300, y: 240, width: 230, height: 70, color: '#ec4899' }
        ];

        let selectedBooth = null;
        let isDragging = false;
        let dragOffsetX = 0;
        let dragOffsetY = 0;

        // 드래그 앤 드롭 이벤트 처리
        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const mouseX = (e.clientX - rect.left) * scaleX;
            const mouseY = (e.clientY - rect.top) * scaleY;

            booths.forEach(b => {
                if (mouseX >= b.x && mouseX <= b.x + b.width && mouseY >= b.y && mouseY <= b.y + b.height) {
                    selectedBooth = b;
                    isDragging = true;
                    dragOffsetX = mouseX - b.x;
                    dragOffsetY = mouseY - b.y;
                }
            });
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!isDragging || !selectedBooth) return;
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            selectedBooth.x = (e.clientX - rect.left) * scaleX - dragOffsetX;
            selectedBooth.y = (e.clientY - rect.top) * scaleY - dragOffsetY;
        });

        window.addEventListener('mouseup', () => {
            isDragging = false;
            selectedBooth = null;
        });

        function toggleSimState() {
            isRunning = !isRunning;
            const btn = document.getElementById('sim-control-btn');
            if (isRunning) {
                btn.innerText = '시뮬레이션 중지';
                btn.className = 'bg-amber-600 hover:bg-amber-500 text-white text-xs px-3 py-1.5 rounded-md font-medium transition shadow';
            } else {
                btn.innerText = '시뮬레이션 시작';
                btn.className = 'bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1.5 rounded-md font-medium transition shadow';
            }
        }

        function triggerAiRedesign() {
            simTime = 9 * 60;
            visitors = [];
            // 무작위 재배치 애니메이션 효과
            booths.forEach(b => {
                b.x = Math.max(20, Math.min(350, b.x + (Math.random() * 40 - 20)));
                b.y = Math.max(20, Math.min(220, b.y + (Math.random() * 40 - 20)));
            });
            document.getElementById('heatmap-status-text').innerText = '상태: AI가 행사장 배치를 재최적화했습니다.';
        }

        function addAiLog() {
            const list = document.getElementById('ai-suggestions-list');
            const item = document.createElement('li');
            item.className = 'flex items-start space-x-2';
            item.innerHTML = `<span class="text-indigo-400 font-bold">•</span><span>실시간 동기화 업데이트: 현재 시각(${Math.floor(simTime/60)}:${String(simTime%60).padStart(2,'0')}) 기준 병목 위험 구간이 해소되었습니다.</span>`;
            list.prepend(item);
        }

        // 관람객 생성 로직 (시간대별 변수와 공간 동기화)
        function updateVisitors() {
            if (!isRunning) return;

            simTime += 2; // 시뮬레이션 배속
            if (simTime >= 18 * 60) simTime = 9 * 60; // 반복 루프

            let h = Math.floor(simTime / 60);
            let m = simTime % 60;
            document.getElementById('clock-display').innerText = `시간: ${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
            document.getElementById('heatmap-status-text').innerText = `동기화 시간: ${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;

            // 시간대별 특정 부스로의 쏠림 현상(가중치) 설정
            let targetBooth = booths[0]; // 기본 메인스테이지
            if (h >= 10 && h < 12) {
                targetBooth = booths[2]; // 신기술 체험존 집중
            } else if (h >= 12 && h < 13) {
                targetBooth = booths[4]; // 휴게 및 식음료 집중
            } else if (h >= 14) {
                targetBooth = booths[1]; // 기업 홍보관 집중
            } else {
                targetBooth = booths[Math.floor(Math.random() * booths.length)];
            }

            // 관람객 스폰
            if (visitors.length < 100 && Math.random() < 0.6) {
                visitors.push({
                    x: 280 + (Math.random() * 40 - 20),
                    y: 330,
                    targetBooth: targetBooth,
                    speed: Math.random() * 1.2 + 0.8,
                    type: Math.random() > 0.15 ? 'normal' : 'vip'
                });
            }

            // 이동 업데이트
            visitors.forEach(v => {
                // 실시간으로 변경된 부스 위치로 타겟 좌표 갱신
                let tx = v.targetBooth.x + v.targetBooth.width / 2;
                let ty = v.targetBooth.y + v.targetBooth.height / 2;

                let dx = tx - v.x;
                let dy = ty - v.y;
                let dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 5) {
                    // 도착 후 다른 부스로 변경
                    v.targetBooth = booths[Math.floor(Math.random() * booths.length)];
                } else {
                    v.x += (dx / dist) * v.speed;
                    v.y += (dy / dist) * v.speed;
                }
            });
        }

        // 렌더링 루프 (시뮬레이션 캔버스 & 히트맵 캔버스 동시 드로잉)
        function drawScene() {
            // 1. 시뮬레이션 캔버스 드로잉
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 바닥 그리드 및 통로 가이드라인
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
            ctx.lineWidth = 1;
            for (let i = 0; i < canvas.width; i += 30) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
            }
            for (let j = 0; j < canvas.height; j += 30) {
                ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(canvas.width, j); ctx.stroke();
            }

            // 출입구 표시
            ctx.fillStyle = '#64748b';
            ctx.fillRect(250, 320, 60, 20);
            ctx.fillStyle = '#ffffff';
            ctx.font = '10px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('입출구', 280, 334);

            // 부스 렌더링
            booths.forEach(b => {
                ctx.fillStyle = b.color;
                ctx.fillRect(b.x, b.y, b.width, b.height);
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.strokeRect(b.x, b.y, b.width, b.height);

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 11px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(b.name, b.x + b.width / 2, b.y + b.height / 2 + 4);
            });

            // 관람객 렌더링
            visitors.forEach(v => {
                ctx.fillStyle = v.type === 'vip' ? '#f59e0b' : '#3b82f6';
                ctx.beginPath();
                ctx.arc(v.x, v.y, 3.5, 0, Math.PI * 2);
                ctx.fill();
            });

            // 2. 히트맵 캔버스 동기화 드로잉
            heatCtx.clearRect(0, 0, heatCanvas.width, heatCanvas.height);
            
            // 히트맵 배경 부스 배치 복사
            booths.forEach(b => {
                heatCtx.fillStyle = '#1e293b';
                heatCtx.fillRect(b.x, b.y, b.width, b.height);
                heatCtx.strokeStyle = '#334155';
                heatCtx.strokeRect(b.x, b.y, b.width, b.height);
                heatCtx.fillStyle = '#94a3b8';
                heatCtx.font = '10px sans-serif';
                heatCtx.textAlign = 'center';
                heatCtx.fillText(b.name, b.x + b.width / 2, b.y + b.height / 2 + 4);
            });

            // 관람객 위치 기반 밀집도 히트맵 방사형 그라데이션 적용
            visitors.forEach(v => {
                let gradient = heatCtx.createRadialGradient(v.x, v.y, 2, v.x, v.y, 30);
                gradient.addColorStop(0, 'rgba(239, 68, 68, 0.25)'); // 중심 밀집 고온
                gradient.addColorStop(0.5, 'rgba(234, 179, 8, 0.1)'); // 중간 온도
                gradient.addColorStop(1, 'rgba(239, 68, 68, 0)');
                heatCtx.fillStyle = gradient;
                heatCtx.beginPath();
                heatCtx.arc(v.x, v.y, 30, 0, Math.PI * 2);
                heatCtx.fill();
            });
        }

        function loop() {
            updateVisitors();
            drawScene();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
