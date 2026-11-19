# -*- coding: utf-8 -*-
"""kg.json · refs.json · meta.json 생성 (ai-lab-retrofit 6장 형식)."""
import json, pathlib, re
import data_ko as D
from build import CHREF

PG = "agentic_ai_crash_guide"
OUT = pathlib.Path(__file__).parent / "kg"; OUT.mkdir(exist_ok=True)
nodes, edges = [], []

def node(id, type, ko, en, anchor, level=2, coverage="explained", definition=None, family=None, conf="high", **kw):
    n = {"id": id, "type": type, "label": {"ko": ko, "en": en}, "page": PG, "anchor": anchor, "level": level,
         "status": "known", "confidence": conf, "coverage": coverage, "match": [], "domain": ["ai"]}
    if definition: n["definition"] = {"ko": definition}
    if family: n["family"] = family
    n.update(kw); nodes.append(n); return id

def edge(s, p, o, anchor, conf="high"):
    edges.append({"s": s, "p": "lab:" + p, "o": o, "anchor": anchor, "confidence": conf})

# 장별 핵심 노드: (id, type, ko, en, 정의, family, 뼈대 주제들)
CORE = {
 1: ("lab:concept/bayes-theorem", "Concept", "베이즈 정리", "Bayes' theorem", "처음 짐작에 단서의 무게를 곱해 짐작을 고치는 식.", "math", ["probability-statistics"]),
 2: ("lab:concept/expected-utility", "Concept", "기대효용", "Expected utility", "결과마다 확률 × 만족도를 더해 행동별 점수를 내고 큰 쪽을 고르는 방법.", "math", ["probability-statistics"]),
 3: ("lab:method/constrained-optimization", "Method", "제약 최적화", "Constrained optimization", "넘으면 안 되는 선을 먼저 긋고 그 안에서 점수가 가장 큰 조합을 찾는 방법.", "math", ["calculus-optimization-math"]),
 4: ("lab:method/a-star-search", "Method", "A* 탐색", "A* search", "지금까지 쓴 비용과 남은 비용 어림의 합이 가장 작은 단계부터 펼치는 길 찾기.", None, []),
 5: ("lab:concept/nash-equilibrium", "Concept", "내시 균형", "Nash equilibrium", "서로 상대의 선택을 보고도 혼자 바꿀 이유가 없는 상태.", None, []),
 6: ("lab:concept/state-transition", "Concept", "상태 전이 확률", "State transition probability", "지금 상태와 행동이 정해졌을 때 다음 상태로 갈 확률.", "rl", ["mdp"]),
 7: ("lab:concept/discounted-return", "Concept", "할인 누적 보상", "Discounted return", "늦게 받는 보상일수록 할인율을 곱해 깎아 모두 더한 값.", "rl", ["reward"]),
 8: ("lab:concept/state-value-function", "Concept", "상태가치 함수", "State-value function", "정책을 따를 때 그 상태에서 받을 할인 누적 보상의 평균.", "rl", ["value-function"]),
 9: ("lab:concept/action-value-function", "Concept", "행동가치 함수", "Action-value function", "첫 행동을 정해 두고 그 뒤 정책을 따를 때의 평균 누적 보상.", "rl", ["value-function", "q-learning"]),
 10: ("lab:concept/bellman-equation", "Concept", "벨만 방정식", "Bellman equation", "지금 가치를 바로 받는 보상과 다음 상태 가치의 평균으로 잇는 되풀이 식.", "rl", ["value-function", "mdp"]),
 11: ("lab:method/softmax-policy", "Method", "소프트맥스 정책", "Softmax policy", "행동 점수를 지수로 키운 뒤 합으로 나눠 확률로 바꾸고 그 확률대로 고르는 정책.", "rl", ["policy-gradient", "exploration"]),
 12: ("lab:method/reinforce", "Method", "REINFORCE (정책 경사)", "REINFORCE", "받은 누적 보상만큼 고른 행동의 확률을 올리는 쪽으로 가중치를 고치는 방법.", "rl", ["policy-gradient"]),
 13: ("lab:method/actor-critic", "Method", "행동자·평가자", "Actor-critic", "평가자가 보통 점수를 어림하고 행동자는 보통보다 나은 만큼만 반영해 배우는 방법.", "rl", ["policy-gradient", "value-function"]),
}
EXTRA = [
 ("lab:concept/admissible-heuristic", "Concept", "부풀리지 않은 어림", "Admissible heuristic", 4, "남은 비용 어림이 실제 남은 비용보다 크지 않아야 한다는 조건.", None, []),
 ("lab:concept/mixed-strategy", "Concept", "혼합 전략", "Mixed strategy", 5, "행동을 확률로 섞어 고르는 전략. 순수 전략 균형이 없을 때의 균형.", None, []),
 ("lab:concept/markov-property", "Assumption", "마르코프 가정", "Markov property", 6, "다음 상태는 지금 상태와 행동만 보고 정해진다는 가정.", "rl", ["mdp"]),
 ("lab:concept/discount-factor", "Concept", "할인율 γ", "Discount factor", 7, "늦게 받는 보상을 깎는 0 이상 1 미만의 수.", "rl", ["reward"]),
 ("lab:concept/policy", "Concept", "정책 π", "Policy", 8, "어느 상태에서 무엇을 할지 정한 규칙.", "rl", ["mdp"]),
 ("lab:concept/advantage", "Concept", "이점 A", "Advantage", 13, "받은 점수에서 평가자의 보통 점수 어림을 뺀 값.", "rl", ["policy-gradient"]),
 ("lab:concept/td-target", "Concept", "시간차 목표", "TD target", 10, "바로 받는 보상과 다음 상태 가치 어림을 더한 목표값.", "rl", ["value-function"]),
 ("lab:term/temperature", "Term", "온도", "Temperature", 11, "점수를 나누어 고르기를 날카롭게 또는 고르게 하는 챗봇 설정값.", "language", ["autoregressive-generation"]),
 ("lab:term/rlhf", "Term", "사람 피드백 강화학습", "RLHF", 12, None, "rl", ["policy-gradient"]),
 ("lab:term/ppo", "Term", "PPO", "Proximal policy optimization", 13, None, "rl", ["policy-gradient"]),
 ("lab:term/grpo", "Term", "GRPO", "Group relative policy optimization", 13, None, "rl", ["policy-gradient"]),
 ("lab:concept/llm-output-softmax", "Analogy", "LLM 출력층과 같은 모양", "LLM output layer as softmax policy", 11, "LLM이 다음 낱말을 고르는 마지막 층이 소프트맥스 정책과 같은 모양이라는 대응.", "language", ["pretrained-lm"]),
]
TERMS_MENTIONED = {"lab:term/rlhf", "lab:term/ppo", "lab:term/grpo"}

for n, (id, t, ko, en, df, fam, tops) in CORE.items():
    a = f"#lv{n}"
    node(id, t, ko, en, a, level=1 if n <= 7 else 2, definition=df, family=fam)
    for tp in tops: edge(id, "broader", "lab:topic/" + tp, a)
    if n > 1: edge(CORE[n-1][0], "prerequisiteOf", id, a, "medium" if n in (6,) else "high")
    # 한계
    lid = f"lab:limitation/ch{n:02d}"
    lim = D.CH[n-1]["limit"]
    node(lid, "Limitation", lim.split(". ")[0].rstrip(".") , f"Limitation of chapter {n}", a, level=2, coverage="explained", family=fam)
    edge(id, "hasLimitation", lid, a)
    if tops: edge(lid, "broader", "lab:topic/" + tops[0], a)
    # 시뮬레이션 · 퀴즈
    sid = f"lab:simulation/p1-lv{n}"
    node(sid, "Simulation", f"{n}장 실험 패널", f"Chapter {n} interactive panel", a, level=1)
    edge(id, "demonstratedBy", sid, a)
    qid = f"lab:quiz/p1-lv{n}-1"
    node(qid, "QuizItem", re.sub("<[^>]+>", "", D.CH[n-1]["quiz"][0]), f"Quiz {n}", a, level=1)
    edge(qid, "assesses", id, a)

for id, t, ko, en, ch, df, fam, tops in EXTRA:
    a = f"#lv{ch}"
    node(id, t, ko, en, a, level=2 if id not in TERMS_MENTIONED else 3,
         coverage="mentioned" if id in TERMS_MENTIONED else "explained", definition=df, family=fam)
    for tp in tops: edge(id, "broader", "lab:topic/" + tp, a)

C = lambda n: CORE[n][0]
# 한계 → 다음 방법
for a_, b_ in [(1, 2), (2, 3), (3, 4), (4, 4), (5, 5), (6, 7), (7, 8), (8, 10), (9, 9), (10, 12), (11, 11), (12, 13)]:
    pass
addr = [(1, C(2)), (2, C(3)), (5, "lab:concept/mixed-strategy"), (6, C(1)), (7, C(8)), (8, C(10)), (10, C(12)), (12, C(13)), (13, "lab:term/ppo")]
for ch, tgt in addr: edge(f"lab:limitation/ch{ch:02d}", "addressedBy", tgt, f"#lv{ch}")
# 부품 관계
P = [("lab:concept/admissible-heuristic", "partOf", C(4), "#lv4"), ("lab:concept/mixed-strategy", "partOf", C(5), "#lv5"),
     ("lab:concept/markov-property", "partOf", C(6), "#lv6"), (C(6), "assumes", "lab:concept/markov-property", "#lv6"),
     ("lab:concept/discount-factor", "partOf", C(7), "#lv7"), ("lab:concept/policy", "prerequisiteOf", C(8), "#lv8"),
     ("lab:concept/policy", "prerequisiteOf", C(11), "#lv11"), ("lab:concept/advantage", "partOf", C(13), "#lv13"),
     ("lab:concept/td-target", "derivedFrom", C(10), "#lv10"), ("lab:concept/td-target", "partOf", C(13), "#lv13"),
     ("lab:term/temperature", "partOf", C(11), "#lv11"), ("lab:concept/llm-output-softmax", "analogyOf", C(11), "#lv11"),
     ("lab:term/rlhf", "derivedFrom", C(12), "#lv12"), ("lab:term/ppo", "derivedFrom", C(13), "#lv13"),
     ("lab:term/grpo", "contrastsWith", "lab:term/ppo", "#lv13"), (C(12), "contrastsWith", C(13), "#duel"),
     (C(8), "relatedTo", C(9), "#lv9"), (C(2), "relatedTo", C(9), "#lv9"),
     (C(7), "prerequisiteOf", C(12), "#lv12"), (C(11), "prerequisiteOf", C(12), "#lv12"), (C(10), "prerequisiteOf", C(13), "#lv13")]
for s, p, o, a in P: edge(s, p, o, a)
# 대결
node("lab:simulation/p1-duel", "Simulation", "대결: 평가자 없음 vs 박사 평가자", "Duel: REINFORCE vs actor-critic", "#duel", level=2)
edge(C(12), "demonstratedBy", "lab:simulation/p1-duel", "#duel"); edge(C(13), "demonstratedBy", "lab:simulation/p1-duel", "#duel")
node("lab:metric/rounds-to-90", "Metric", "90%에 닿기까지 횟수", "Rounds to 90% preference", "#duel", level=2)
edge(C(12), "evaluatedBy", "lab:metric/rounds-to-90", "#duel"); edge(C(13), "evaluatedBy", "lab:metric/rounds-to-90", "#duel")
node("lab:question/rlhf-next", "Question", "하루봇의 두뇌를 실제 LLM으로 바꾸면(RLHF·PPO·GRPO)?", "Next: RLHF with a real LLM", "#outro", level=4, coverage="mentioned")
edge(C(13), "raises", "lab:question/rlhf-next", "#outro")

# 문헌·주장
refs = []
for r in D.REFS:
    wid = "lab:work/" + r["id"]
    node(wid, "Work", r["title"], r["title"], "#export", level=1, coverage="mentioned")
    auth = [{"literal": r["author"]}] if isinstance(r["author"], str) else [{"family": f, "given": g} for f, g in r["author"]]
    item = {"id": r["id"], "type": r["type"], "title": r["title"], "author": auth}
    if r["year"]: item["issued"] = {"date-parts": [[r["year"]]]}
    if r.get("container"): item["container-title" if r["type"] != "book" else "publisher"] = r["container"]
    item["lab"] = {"work": wid, "role": r["role"], "supports": [], "locs": [],
                   "verified": {"title": True, "author": True, "year": bool(r["year"]), "container": bool(r.get("container")), "pages": False, "doi": False},
                   "checkedBy": "페이지 참고문헌 목록에서 옮김 (외부 대조 안 함)", "checkedSource": "page"}
    refs.append(item)
CLAIMS = [("orig-12-formulas", "원자료 인포그래픽은 에이전트의 수학 공식 12개를 제시한다", "#why", "mltut-agentic", C(1))]
for n, rid in CHREF.items():
    CLAIMS.append((f"ch{n:02d}-basis", f"{CORE[n][2]}의 정의는 표준 문헌을 따른다", f"#lv{n}", rid, C(n)))
for cid, ko, a, rid, tgt in CLAIMS:
    i = "lab:claim/" + cid
    node(i, "Claim", ko, ko, a, level=2, coverage="explained", source=[{"ref": rid, "loc": ""}])
    edge(i, "supports", tgt, a); edge(i, "assertedIn", "lab:work/" + rid, a)
    next(x for x in refs if x["id"] == rid)["lab"]["supports"].append(i)

kg = {"version": "1.0", "page": PG, "nodes": nodes, "edges": edges}
meta = {"title": D.META["title"], "number": D.META["number"], "series": D.META["series"],
        "about": [C(1), C(6), C(10), C(11), C(13)], "basedOn": ["mltut-agentic"], "educationalLevel": "입문",
        "creator": [{"name": D.META["author"], "role": "author", "url": D.META["site"]}],
        "contributor": [{"name": "AI 보조 제작", "role": "assistant"}], "date": D.META["date"], "version": "1.0",
        "language": ["ko"], "license": "", "url": "https://adminmrobo.github.io/agentic_ai_crash_guide/", "registry": "KG_00_registry 0.2", "domain": ["ai"],
        "learningResourceType": "interactive explainer", "seeAlso": "",
        "suggestedCitation": f'{D.META["author"]} (2026). {D.META["title"]}. {D.META["series"]} {D.META["number"]}, v1.0.'}
for name, obj in (("kg", kg), ("refs", refs), ("meta", meta)):
    (OUT / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
print("nodes", len(nodes), "edges", len(edges))
