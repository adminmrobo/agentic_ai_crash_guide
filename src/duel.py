"""대결 검산: REINFORCE 하루봇 vs 평가자(critic) 붙은 하루봇. JS와 같은 난수기(mulberry32)."""
import math, sys

def mulberry32(a):
    a &= 0xFFFFFFFF
    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r

MEAN = [9, 7, 6]

def run(seed, critic, alpha=0.02, beta=0.1, rounds=300):
    rnd = mulberry32(seed)
    th = [0.0, 0.0, 0.0]; b = 0.0; hist = []; hit = None
    for t in range(rounds):
        m = max(th); e = [math.exp(x - m) for x in th]; s = sum(e); pi = [x / s for x in e]
        u = rnd(); a = 0 if u < pi[0] else (1 if u < pi[0] + pi[1] else 2)
        u1 = max(rnd(), 1e-12); u2 = rnd()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        G = min(10, max(1, MEAN[a] + z))
        adv = G - b if critic else G
        th = [th[i] + alpha * adv * ((1 if i == a else 0) - pi[i]) for i in range(3)]
        if critic: b += beta * (G - b)
        hist.append(pi[0])
        if hit is None and pi[0] >= 0.9: hit = t + 1
    return hit or rounds, hist

if __name__ == "__main__":
    for alpha in (0.01, 0.02, 0.03):
        rf = [run(s, False, alpha)[0] for s in range(1, 31)]
        ac = [run(s, True, alpha)[0] for s in range(1, 31)]
        wins = sum(1 for x, y in zip(rf, ac) if y < x)
        print(alpha, "REINFORCE 평균", sum(rf) / 30, "critic 평균", sum(ac) / 30, "critic 승", wins, "/30",
              "REINFORCE 300 미달", sum(1 for x in rf if x >= 300))
    print("seed1 첫 3라운드 pi0", [round(x, 4) for x in run(1, False, 0.02)[1][:3]])
