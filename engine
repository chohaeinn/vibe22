"""배치·평가 엔진. 모든 지표는 교육용 규칙 기반 추정값이다."""
from __future__ import annotations
import copy
import math
import random
import numpy as np

KINDS = {
    '무대': (18, 10, 5, '#1751D0', 3500000),
    '관람석': (22, 14, 0.8, '#0E9E8F', 1200000),
    '판매 부스': (5, 5, 3, '#E2661E', 180000),
    '체험 부스': (6, 6, 3, '#C08A00', 250000),
    '푸드트럭': (6, 4, 3, '#D95D8F', 300000),
    '휴식 공간': (9, 7, 2.5, '#2E7D32', 200000),
    '화장실': (6, 4, 3, '#9117D0', 400000),
    '안내소': (5, 4, 3, '#1751D0', 150000),
    '응급의료소': (6, 5, 3, '#1751D0', 350000),
    '출입구': (8, 3, 4, '#0E9E8F', 100000),
    '주차장': (18, 12, 0.2, '#505A74', 500000),
    '분리수거장': (4, 3, 2, '#505A74', 80000),
    '음수대': (3, 3, 1.5, '#0E9E8F', 100000),
}
DEFAULT_COUNTS = {'무대': 1, '관람석': 1, '판매 부스': 8, '체험 부스': 5,
                  '푸드트럭': 4, '휴식 공간': 3, '화장실': 2, '안내소': 1,
                  '응급의료소': 1, '출입구': 2, '주차장': 1, '분리수거장': 2, '음수대': 2}
REQUIRED = ['화장실', '안내소', '응급의료소', '출입구', '휴식 공간', '음수대', '분리수거장']

def overlap(a, b, gap=0):
    return (a['x'] < b['x'] + b['w'] + gap and a['x'] + a['w'] + gap > b['x']
            and a['y'] < b['y'] + b['d'] + gap and a['y'] + a['d'] + gap > b['y'])

def corridors(c):
    w, d, k = c['width'], c['depth'], c['aisle']
    return [dict(x=w/2-k/2, y=0, w=k, d=d), dict(x=0, y=d/2-k/2, w=w, d=k)]

def center(b):
    return b['x'] + b['w']/2, b['y'] + b['d']/2

def distance(a, b):
    return math.dist(center(a), center(b))

def errors(layout, c):
    out = []
    for i, b in enumerate(layout):
        if (not all(math.isfinite(float(b[k])) for k in ['x','y','w','d','h'])
                or min(b['w'], b['d'], b['h']) <= 0):
            out.append(f"{b['name']}: 크기 또는 좌표 오류")
            continue
        if b['x'] < 0 or b['y'] < 0 or b['x']+b['w'] > c['width'] or b['y']+b['d'] > c['depth']:
            out.append(f"{b['name']}: 행사장 경계 초과")
        if any(overlap(b, road) for road in corridors(c)):
            out.append(f"{b['name']}: 중앙 통로 침범")
        for other in layout[:i]:
            if overlap(b, other, c.get('gap', 2)):
                out.append(f"{b['name']} / {other['name']}: 겹침 또는 시설 간 여유 부족")
    return out

def generate(c, counts, seed=42):
    rng = random.Random(seed)
    layout, missing = [], []
    # 큰 시설부터 배치. 요청 수량은 배치하지 못해도 숨기지 않는다.
    order = sorted(counts, key=lambda k: KINDS[k][0]*KINDS[k][1], reverse=True)
    for kind in order:
        w, d, h, color, cost = KINDS[kind]
        for n in range(int(counts[kind])):
            b = dict(id=f'{kind}-{n+1}', name=f'{kind} {n+1}', kind=kind, w=w, d=d, h=h,
                     color=color, cost=cost, x=0., y=0.)
            candidates = []
            for _ in range(220):
                x = rng.uniform(1, max(1, c['width']-w-1))
                y = rng.uniform(1, max(1, c['depth']-d-1))
                candidate = dict(b, x=round(x, 1), y=round(y, 1))
                if errors([candidate], c) or any(overlap(candidate, old, c['gap']) for old in layout):
                    continue
                # 출입구는 경계에 가깝게, 무대는 상단, 관람석은 무대 근처.
                preference = rng.random()*5
                if kind == '출입구':
                    preference += min(x,y,c['width']-x-w,c['depth']-y-d)*8
                    if any(old['kind']=='출입구' and distance(candidate,old)<c['width']*.45 for old in layout):
                        preference += 100
                if kind == '무대': preference += c['depth']-y-d
                if kind == '관람석':
                    stage = next((old for old in layout if old['kind']=='무대'), None)
                    if stage: preference += distance(candidate, stage)
                candidates.append((preference, candidate))
            if candidates:
                layout.append(min(candidates, key=lambda t:t[0])[1])
            else:
                missing.append(b['name'])
    return layout, missing

def assess(layout, c):
    occupied = sum(b['w']*b['d'] for b in layout)
    free = max(1., c['width']*c['depth']-occupied)
    simultaneous = c['visitors']*c['peak_ratio']
    density = simultaneous/free
    entries = [b for b in layout if b['kind']=='출입구']
    distances = [min(distance(b,e) for e in entries) for b in layout] if entries else []
    mean_distance = float(np.mean(distances)) if distances else math.hypot(c['width'], c['depth'])
    near = sum(min((distance(b,r) for r in layout if r['kind']=='휴식 공간'), default=1e6) <= 30 for b in layout)
    coverage = 100*near/max(1,len(layout))
    missing = [kind for kind in REQUIRED if not any(b['kind']==kind for b in layout)]
    violation = errors(layout,c)
    cost = sum(b['cost'] for b in layout)
    # 비교용 점수이며 인증된 안전/접근성 점수가 아니다.
    spacing = max(0,100-12*len(violation)-10*len(missing)-max(0,density-.3)*45)
    access = max(0, min(100,.6*coverage + .4*max(0,100-mean_distance*.7)))
    flow = max(0, min(100,100-mean_distance*.65-max(0,density-.3)*30))
    budget = min(100,100*c['budget']/max(1,cost))
    weights = {'안전 중심':(.5,.2,.2,.1),'접근성 중심':(.2,.5,.2,.1),
               '운영 효율 중심':(.2,.2,.5,.1),'예산 중심':(.2,.2,.1,.5)}[c['goal']]
    score = sum(a*b for a,b in zip(weights,(spacing,access,flow,budget)))
    return dict(score=round(score,1), spacing=round(spacing,1), access=round(access,1),
                flow=round(flow,1), budget_score=round(budget,1), cost=cost, free_area=round(free,1),
                density=round(density,3), simultaneous=round(simultaneous),
                distance=round(mean_distance,1), rest_coverage=round(coverage,1),
                missing=missing, violations=violation)

def optimize(c, counts, trials=30):
    best = None
    for seed in range(trials):
        layout, missing = generate(c, counts, seed=1000+seed)
        value = assess(layout,c)['score'] - 100*len(missing)
        if best is None or value > best[0]:
            best = (value,layout,missing)
    return best[1], best[2]

def heatmap(layout, c, scenario='평상시'):
    """시설 매력도를 가정한 가우시안 분포. 실제 군중 이동 시뮬레이션 아님."""
    x = np.linspace(0,c['width'],65)
    y = np.linspace(0,c['depth'],65)
    X,Y = np.meshgrid(x,y)
    Z = np.ones_like(X)*.15
    for b in layout:
        cx,cy = center(b)
        weight = {'무대':4,'관람석':3,'푸드트럭':2,'출입구':2}.get(b['kind'],.5)
        if scenario == '공연 지연' and b['kind'] in ['무대','관람석']: weight *= 1.6
        sigma = max(5,min(c['width'],c['depth'])*.07)
        Z += weight*np.exp(-((X-cx)**2+(Y-cy)**2)/(2*sigma**2))
    Z *= c['visitors']*c['peak_ratio']/(max(1,Z.sum())*(x[1]-x[0])*(y[1]-y[0]))
    if scenario == '방문객 급증': Z *= 1.5
    if scenario == '우천': Z *= 1.2
    return x,y,Z

def recommendations(layout,c):
    a=assess(layout,c)
    notes=[]
    if a['missing']: notes.append('빠진 필수시설: '+', '.join(a['missing']))
    if a['violations']: notes.append('경계·간격·통로 오류를 먼저 수정한다.')
    if a['cost']>c['budget']: notes.append('입력 예산보다 가상 설치비가 높다. 수량이나 시설 규격을 조정한다.')
    if a['density']>.5: notes.append('가정한 동시 체류 인원에 비해 여유면적이 작다. 입장 시간 분산과 장소 확대를 검토한다.')
    if a['rest_coverage']<80: notes.append('시설 중심 기준 30m 안에 휴식 공간이 없는 구역이 있다. 휴식 공간을 분산한다.')
    if sum(b['kind']=='출입구' for b in layout)<2: notes.append('출입구를 두 곳 이상 두고 분산 배치하는 방안을 검토한다.')
    notes.append('화장실·출입구·의료소의 실제 접근 경로, 경사, 지면 상태와 유효 폭은 현장에서 따로 확인한다.')
    return notes

def validate_project(raw):
    if not isinstance(raw,dict) or raw.get('version') != 1: raise ValueError('지원하지 않는 프로젝트 형식')
    c=raw['config']; layout=raw['layout']; counts=raw['counts']
    for k,lo,hi in [('width',60,500),('depth',60,500),('aisle',4,16),('gap',0,6),
                    ('visitors',1,100000),('peak_ratio',.05,1),('budget',100000,1000000000)]:
        v=c[k]
        if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or not lo<=v<=hi:
            raise ValueError(f'잘못된 설정: {k}')
    if c['goal'] not in ['안전 중심','접근성 중심','운영 효율 중심','예산 중심']: raise ValueError('설계 목표 오류')
    if not isinstance(c['name'],str) or len(c['name'])>100: raise ValueError('행사명 오류')
    if not isinstance(layout,list) or len(layout)>250: raise ValueError('시설은 250개 이하만 불러올 수 있다')
    if not isinstance(counts,dict) or any(k not in KINDS or type(v)!=int or not 0<=v<=60 for k,v in counts.items()):
        raise ValueError('시설 수량 오류')
    if sum(counts.values())>250: raise ValueError('총 요청 수량 초과')
    ids=set()
    for b in layout:
        if b['kind'] not in KINDS or not isinstance(b['name'],str) or len(b['name'])>100: raise ValueError('시설 정보 오류')
        if not isinstance(b['id'],str) or b['id'] in ids: raise ValueError('시설 ID 오류')
        ids.add(b['id'])
        for k in ['x','y','w','d','h','cost']:
            if type(b[k]) not in (int,float) or not math.isfinite(b[k]) or not 0<=b[k]<=1e9: raise ValueError('좌표·비용 오류')
        if b['w']<1 or b['d']<1 or not .1<=b['h']<=30: raise ValueError('시설 크기 범위 오류')
        b['color']=KINDS[b['kind']][3]
    if any(sum(b['kind']==k for b in layout)>60 for k in KINDS): raise ValueError('종류별 시설 수량 초과')
    if any(counts.get(k,0)<sum(b['kind']==k for b in layout) for k in KINDS): raise ValueError('요청 수량과 시설 목록 불일치')
    problems=errors(layout,c)
    if problems: raise ValueError(problems[0])
    return copy.deepcopy(c),copy.deepcopy(layout),copy.deepcopy(counts)
