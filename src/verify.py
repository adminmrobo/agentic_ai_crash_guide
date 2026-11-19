"""13장 '숫자로 한 번 해 보기' 값 검산."""
import math, heapq, itertools, random

print("== 1 베이즈")
pA, pBA, pBn = 0.3, 0.8, 0.1
pB = pBA * pA + pBn * (1 - pA)
post = pBA * pA / pB
print("P(B)=", round(pB, 4), "P(A|B)=", round(post, 4))

print("== 2 기대효용")
p = round(post, 2)  # 0.77
eu_ans = p * 10 + (1 - p) * (-20)
print("p=", p, "EU(답하기)=", round(eu_ans, 2), "EU(되묻기)=4", "분기점 p=", 24 / 30)

print("== 3 제약 최적화")
tools = {"웹 검색": (5, 6), "일정 조회": (2, 5), "문서 요약": (8, 7), "이모티콘": (1, 2)}
best = None
for r in range(len(tools) + 1):
    for c in itertools.combinations(tools, r):
        t = sum(tools[k][0] for k in c); u = sum(tools[k][1] for k in c)
        if t <= 10 and (best is None or u > best[0]):
            best = (u, t, c)
print(best)
for r in range(len(tools) + 1):
    for c in itertools.combinations(tools, r):
        t = sum(tools[k][0] for k in c); u = sum(tools[k][1] for k in c)
        if t <= 10 and u >= 12: print("  후보", c, t, u)

print("== 4 A*")
E = {"S": {"M": 2, "W": 4}, "M": {"K": 3, "D": 6}, "W": {"D": 3, "T": 5},
     "K": {"D": 4}, "D": {"R": 4, "G": 7}, "T": {"R": 3}, "R": {"G": 2}, "G": {}}
H = {"S": 10, "M": 9, "K": 8, "W": 7, "D": 5, "T": 4, "R": 2, "G": 0}

def true_cost(n):
    dist = {n: 0}; pq = [(0, n)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == "G": return d
        for v, w in E[u].items():
            if d + w < dist.get(v, 1e9): dist[v] = d + w; heapq.heappush(pq, (d + w, v))
for n in E: print(n, "실제 남은", true_cost(n), "h", H[n])

def astar(w):
    openl = [(w * H["S"], 0, "S", ["S"])]; closed = set(); order = []
    while openl:
        f, g, u, path = heapq.heappop(openl)
        if u in closed: continue
        closed.add(u); order.append(u)
        if u == "G": return path, g, order
        for v, c in E[u].items():
            if v not in closed: heapq.heappush(openl, (g + c + w * H[v], g + c, v, path + [v]))
for w in (0, 1, 2, 3):
    print("배수", w, astar(w))

print("== 5 내시")
games = {"협력": {("W","W"):(2,0),("W","C"):(5,5),("C","W"):(1,1),("C","C"):(0,3)},
         "숨바꼭질": {("W","W"):(1,-1),("W","C"):(-1,1),("C","W"):(-1,1),("C","C"):(1,-1)}}
for name, g in games.items():
    ne = []
    for a, b in g:
        u1, u2 = g[(a, b)]
        br1 = all(u1 >= g[(x, b)][0] for x in "WC"); br2 = all(u2 >= g[(a, y)][1] for y in "WC")
        if br1 and br2: ne.append((a, b))
    print(name, ne)

print("== 6~10 MDP")
gam = 0.9
# P[s][a] = [(s', p, r)]
P = {"C": {"ans": [("D", .3, 10), ("C", .7, -2)], "ask": [("U", .9, -1), ("C", .1, -3)]},
     "U": {"ans": [("D", .9, 10), ("C", .1, -2)], "ask": [("U", 1.0, -1)]}}
pol = {"C": "ask", "U": "ans"}
V = {"C": 0, "U": 0, "D": 0}
for _ in range(2000):
    V = {**V, **{s: sum(p * (r + gam * V[n]) for n, p, r in P[s][pol[s]]) for s in P}}
print("7 G 예: -1 + 0.9*10 =", -1 + 0.9 * 10)
print("8 V^pi", {k: round(v, 3) for k, v in V.items()})
Q = {(s, a): sum(p * (r + gam * V[n]) for n, p, r in P[s][a]) for s in P for a in P[s]}
print("9 Q^pi", {k: round(v, 3) for k, v in Q.items()})
# 손계산식 보이기
print("   Q(C,ans)=0.3*10+0.7*(-2+0.9*V(C)) =", round(.3 * 10 + .7 * (-2 + .9 * V["C"]), 3))
# 몬테카를로
random.seed(1)
def episode(s="C"):
    G, disc = 0, 1
    while s != "D":
        x = random.random(); acc = 0
        for n, p, r in P[s][pol[s]]:
            acc += p
            if x < acc: break
        G += disc * r; disc *= gam; s = n
    return G
mc = sum(episode() for _ in range(20000)) / 20000
print("   MC V(C) 20000판", round(mc, 3))
# 가치 반복
V2 = {"C": 0, "U": 0, "D": 0}
for it in range(1, 8):
    V2 = {**V2, **{s: max(sum(p * (r + gam * V2[n]) for n, p, r in P[s][a]) for a in P[s]) for s in P}}
    print("10 반복", it, {k: round(v, 3) for k, v in V2.items()})
for _ in range(500):
    V2 = {**V2, **{s: max(sum(p * (r + gam * V2[n]) for n, p, r in P[s][a]) for a in P[s]) for s in P}}
print("   V* 수렴", {k: round(v, 3) for k, v in V2.items()})
# 답하기 성공확률 분기점 (C에서)
for pc in [x / 100 for x in range(0, 101, 5)]:
    Pc = {**P, "C": {**P["C"], "ans": [("D", pc, 10), ("C", 1 - pc, -2)]}}
    Vv = {"C": 0, "U": 0, "D": 0}
    for _ in range(3000):
        Vv = {**Vv, **{s: max(sum(p * (r + gam * Vv[n]) for n, p, r in Pc[s][a]) for a in Pc[s]) for s in Pc}}
    qa = sum(p * (r + gam * Vv[n]) for n, p, r in Pc["C"]["ans"]); qk = sum(p * (r + gam * Vv[n]) for n, p, r in Pc["C"]["ask"])
    print("   p_c", pc, "Q*ans", round(qa, 2), "Q*ask", round(qk, 2), "ans" if qa > qk else "ask")

print("== 11 소프트맥스")
z = [2.0, 1.0, 0.1]; ez = [math.exp(v) for v in z]; s = sum(ez)
print([round(v, 3) for v in ez], round(s, 3), [round(v / s, 3) for v in ez])

print("== 12 REINFORCE 한 걸음")
th = [0, 0, 0]; pi = [1 / 3] * 3; a, G, lr = 0, 1, 0.5
th = [t + lr * G * ((1 if i == a else 0) - pi[i]) for i, t in enumerate(th)]
ez = [math.exp(v) for v in th]; s = sum(ez)
print([round(t, 4) for t in th], [round(v / s, 3) for v in ez])

print("== 13 critic")
Vb, beta = 7, 0.1
for G in (9, 6): print("G", G, "A", G - Vb, "손실", (G - Vb) ** 2)
print("V 새 값", Vb + beta * (9 - Vb))
