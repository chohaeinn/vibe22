<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 행사장 설계 최적화 & 동선·밀집도 시뮬레이터</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }
        body { display: flex; height: 100vh; background-color: #1a1d24; color: #fff; }
        
        /* 사이드바 컨트롤 패널 */
        #sidebar {
            width: 340px;
            background: #222631;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            border-right: 1px solid #333a4d;
            box-shadow: 4px 0 15px rgba(0,0,0,0.3);
            z-index: 10;
        }
        h2 { font-size: 1.1rem; color: #4da6ff; margin-bottom: 5px; }
        .control-group { background: #2a2f3d; padding: 15px; border-radius: 8px; }
        .control-group h3 { font-size: 0.95rem; margin-bottom: 12px; color: #e1e6f0; }

        /* 토글 스위치 디자인 */
        .toggle-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .toggle-item:last-child { margin-bottom: 0; }
        .switch { position: relative; display: inline-block; width: 46px; height: 24px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #444c60; transition: .3s; border-radius: 24px; }
        .slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 3px; bottom: 3px; background-color: white; transition: .3s; border-radius: 50%; }
        input:checked + .slider { background-color: #007bff; }
        input:checked + .slider:before { transform: translateX(22px); }

        /* 버튼 및 슬라이더 */
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        .btn-ai { background: linear-gradient(135deg, #007bff, #6610f2); color: white; margin-top: 5px; }
        .btn-ai:hover { opacity: 0.9; }
        .timeline { width: 100%; margin-top: 8px; }

        /* 지표 모니터링 */
        .metric-card { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.85rem; color: #a0aec0; }
        .metric-value { font-weight: bold; color: #00e676; }

        /* 메인 시각화 영역 */
        #main-view { flex: 1; position: relative; background: #12141a; display: flex; justify-content: center; align-items: center; overflow: hidden; }
        .canvas-container { position: relative; width: 800px; height: 600px; border: 2px solid #333a4d; border-radius: 10px; overflow: hidden; background: #1a1d2a; }
        canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }

        /* 래전드 */
        .legend { position: absolute; bottom: 20px; right: 20px; background: rgba(34, 38, 49, 0.9); padding: 12px 16px; border-radius: 8px; font-size: 0.8rem; border: 1px solid #333a4d; }
        .legend-bar { width: 120px; height: 10px; background: linear-gradient(to right, blue, cyan, green, yellow, red); border-radius: 5px; margin-top: 5px; }
    </style>
</head>
<body>

    <!-- 사이드바 패널 -->
    <div id="sidebar">
        <h2>🏛️ AI 행사장 관제 시스템</h2>

        <!-- 도면 모드 변경 -->
        <div class="control-group">
            <h3>1. 도면 상태 선택</h3>
            <button class="btn btn-ai" id="btn-toggle-layout" onclick="toggleLayout()">AI 최적화 도면 적용하기</button>
        </div>

        <!-- 온/오프 토글 시스템 -->
        <div class="control-group">
            <h3>2. 오버레이 레이어 ON/OFF</h3>
            <div class="toggle-item">
                <span>관람객 동선 (Flow)</span>
                <label class="switch">
                    <input type="checkbox" id="toggle-flow" checked onchange="draw()">
                    <span class="slider"></span>
                </label>
            </div>
            <div class="toggle-item">
                <span>인구 밀집도 히트맵</span>
                <label class="switch">
                    <input type="checkbox" id="toggle-heatmap" checked onchange="draw()">
                    <span class="slider"></span>
                </label>
            </div>
        </div>

        <!-- 시간 시뮬레이션 -->
        <div class="control-group">
            <h3>3. 시간대별 인구 변동</h3>
            <span id="time-display" style="font-weight:bold; color:#4da6ff;">14:00 (최고 혼잡시간)</span>
            <input type="range" id="time-slider" class="timeline" min="9" max="18" value="14" oninput="updateTime(this.value)">
        </div>

        <!-- 분석 리포트 -->
        <div class="control-group">
            <h3>4. AI 분석 데이터</h3>
            <div class="metric-card">
                <span>평균 동선 효율성:</span>
                <span class="metric-value" id="val-efficiency">62% (기존)</span>
            </div>
            <div class="metric-card">
                <span>병목 정체 위험도:</span>
                <span class="metric-value" id="val-risk" style="color:#ff5252;">높음 (기존)</span>
            </div>
            <div class="metric-card">
                <span>예상 안전 지수:</span>
                <span class="metric-value" id="val-safety">71점</span>
            </div>
        </div>
    </div>

    <!-- 메인 시각화 화면 -->
    <div id="main-view">
        <div class="canvas-container">
            <!-- 레이어 1: 설계도 (기존 / AI 최적화) -->
            <canvas id="layoutCanvas" width="800" height="600"></canvas>
            <!-- 레이어 2: 밀집도 히트맵 -->
            <canvas id="heatmapCanvas" width="800" height="600"></canvas>
            <!-- 레이어 3: 관람객 동선 벡터 -->
            <canvas id="flowCanvas" width="800" height="600"></canvas>
        </div>

        <!-- 범례 -->
        <div class="legend">
            <div>인구 밀집도 (Density)</div>
            <div class="legend-bar"></div>
            <div style="display:flex; justify-content:space-between; margin-top:2px; color:#aaa; font-size:0.7rem;">
                <span>쾌적</span><span>원활</span><span>혼잡</span>
            </div>
        </div>
    </div>

    <script>
        const layoutCanvas = document.getElementById('layoutCanvas');
        const heatmapCanvas = document.getElementById('heatmapCanvas');
        const flowCanvas = document.getElementById('flowCanvas');

        const ctxLayout = layoutCanvas.getContext('2d');
        const ctxHeatmap = heatmapCanvas.getContext('2d');
        const ctxFlow = flowCanvas.getContext('2d');

        let isAIOptimized = false;
        let currentTime = 14;

        // 부스 데이터 (기존 vs AI 최적화)
        const originalBooths = [
            { x: 150, y: 150, w: 120, h: 220, name: "메인 무대 (A)" },
            { x: 290, y: 150, w: 100, h: 220, name: "인기 부스 (B)" }, // 정체 유발구역
            { x: 410, y: 150, w: 100, h: 220, name: "전시 부스 (C)" },
            { x: 550, y: 150, w: 120, h: 100, name: "체험존 (D)" },
            { x: 550, y: 270, w: 120, h: 100, name: "푸드존 (E)" }
        ];

        const aiOptimizedBooths = [
            { x: 100, y: 100, w: 140, h: 180, name: "메인 무대 (A)" },
            { x: 560, y: 100, w: 140, h: 180, name: "인기 부스 (B)" }, // 간격 분산 배치
            { x: 330, y: 100, w: 140, h: 120, name: "전시 부스 (C)" },
            { x: 180, y: 380, w: 180, h: 120, name: "체험존 (D)" },
            { x: 440, y: 380, w: 180, h: 120, name: "푸드존 (E)" }
        ];

        // 관람객 에이전트 생성 (시뮬레이션용 데이터)
        function generateAgents() {
            const count = Math.floor((currentTime / 18) * 120) + 30; 
            const agents = [];
            const booths = isAIOptimized ? aiOptimizedBooths : originalBooths;

            for (let i = 0; i < count; i++) {
                // 특정 인기 부스 주변 밀집도 생성
                let target = booths[i % booths.length];
                let scatter = isAIOptimized ? 90 : 40; // AI 최적화시 공간이 넓어져 밀집도 분산
                agents.push({
                    x: target.x + target.w / 2 + (Math.random() - 0.5) * scatter * 2,
                    y: target.y + target.h / 2 + (Math.random() - 0.5) * scatter * 2,
                    vx: (Math.random() - 0.5) * 3,
                    vy: (Math.random() - 0.5) * 3
                });
            }
            return agents;
        }

        // 1. 설계도 그리기
        function drawLayout() {
            ctxLayout.clearRect(0, 0, 800, 600);
            const booths = isAIOptimized ? aiOptimizedBooths : originalBooths;

            // 외벽
            ctxLayout.strokeStyle = "#4da6ff";
            ctxLayout.lineWidth = 4;
            ctxLayout.strokeRect(20, 20, 760, 560);

            // 출입구 표시
            ctxLayout.fillStyle = "#00e676";
            ctxLayout.fillRect(360, 570, 80, 10); // 입구
            ctxLayout.fillStyle = "#fff";
            ctxLayout.font = "12px sans-serif";
            ctxLayout.fillText("주 출입구", 375, 560);

            // 부스 그리드
            booths.forEach(b => {
                ctxLayout.fillStyle = isAIOptimized ? "rgba(0, 123, 255, 0.25)" : "rgba(255, 255, 255, 0.08)";
                ctxLayout.strokeStyle = isAIOptimized ? "#007bff" : "#666";
                ctxLayout.lineWidth = 2;
                ctxLayout.fillRect(b.x, b.y, b.w, b.h);
                ctxLayout.strokeRect(b.x, b.y, b.w, b.h);

                ctxLayout.fillStyle = "#ffffff";
                ctxLayout.font = "bold 13px sans-serif";
                ctxLayout.fillText(b.name, b.x + 10, b.y + 25);
            });
        }

        // 2. 인구 밀집도 히트맵 그리기
        function drawHeatmap(agents) {
            ctxHeatmap.clearRect(0, 0, 800, 600);
            if (!document.getElementById('toggle-heatmap').checked) return;

            agents.forEach(agent => {
                const radius = isAIOptimized ? 45 : 35;
                const gradient = ctxHeatmap.createRadialGradient(agent.x, agent.y, 0, agent.x, agent.y, radius);
                
                gradient.addColorStop(0, 'rgba(255, 0, 0, 0.35)');
                gradient.addColorStop(0.4, 'rgba(255, 255, 0, 0.2)');
                gradient.addColorStop(0.8, 'rgba(0, 255, 0, 0.08)');
                gradient.addColorStop(1, 'rgba(0, 0, 255, 0)');

                ctxHeatmap.fillStyle = gradient;
                ctxHeatmap.beginPath();
                ctxHeatmap.arc(agent.x, agent.y, radius, 0, Math.PI * 2);
                ctxHeatmap.fill();
            });
        }

        // 3. 관람객 동선 벡터 그리기
        function drawFlow(agents) {
            ctxFlow.clearRect(0, 0, 800, 600);
            if (!document.getElementById('toggle-flow').checked) return;

            ctxFlow.strokeStyle = "rgba(0, 230, 118, 0.6)";
            ctxFlow.lineWidth = 1.5;

            agents.forEach(agent => {
                ctxFlow.beginPath();
                ctxFlow.moveTo(agent.x, agent.y);
                // 이동 경로 및 방향 화살표
                ctxFlow.lineTo(agent.x + agent.vx * 8, agent.y + agent.vy * 8);
                ctxFlow.stroke();

                // 에이전트 위치 점
                ctxFlow.fillStyle = "#00e676";
                ctxFlow.beginPath();
                ctxFlow.arc(agent.x, agent.y, 2, 0, Math.PI * 2);
                ctxFlow.fill();
            });
        }

        // 전체 화면 업데이트 메인 루틴
        function draw() {
            const agents = generateAgents();
            drawLayout();
            drawHeatmap(agents);
            drawFlow(agents);
        }

        // AI 최적화 도면 토글
        function toggleLayout() {
            isAIOptimized = !isAIOptimized;
            const btn = document.getElementById('btn-toggle-layout');
            
            if (isAIOptimized) {
                btn.innerText = "기존 도면으로 돌아가기";
                btn.style.background = "#28a745";
                document.getElementById('val-efficiency').innerText = "91% (최적화됨)";
                document.getElementById('val-efficiency').style.color = "#00e676";
                document.getElementById('val-risk').innerText = "낮음 (안전)";
                document.getElementById('val-risk').style.color = "#00e676";
                document.getElementById('val-safety').innerText = "95점";
            } else {
                btn.innerText = "AI 최적화 도면 적용하기";
                btn.style.background = "linear-gradient(135deg, #007bff, #6610f2)";
                document.getElementById('val-efficiency').innerText = "62% (기존)";
                document.getElementById('val-efficiency').style.color = "#a0aec0";
                document.getElementById('val-risk').innerText = "높음 (기존)";
                document.getElementById('val-risk').style.color = "#ff5252";
                document.getElementById('val-safety').innerText = "71점";
            }
            draw();
        }

        // 시간대 업데이트
        function updateTime(val) {
            currentTime = val;
            document.getElementById('time-display').innerText = `${val}:00 ${val == 14 ? '(최고 혼잡시간)' : ''}`;
            draw();
        }

        // 최초 실행
        draw();
    </script>
</body>
</html>
