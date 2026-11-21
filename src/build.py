# -*- coding: utf-8 -*-
"""data_ko.py + engine.js → index.html (단일 파일). 사용: python3 build.py"""
import html, json, re, pathlib
import data_ko as D

ROOT = pathlib.Path(__file__).parent
ASSETS = ROOT.parent / "assets"
M = D.META

# ---------- RPG 아이템(픽셀 스프라이트) ----------
import items as IT
def icon(n, cls="ic"):
    """장 번호 n의 아이템 픽셀 스프라이트."""
    return f'<svg class="spr {cls}" viewBox="0 0 12 12" aria-hidden="true"><use href="#it-{n}"/></svg>'

# ---------- 하루봇: 하루의 표정이 나오는 큰 모니터 (본체 없음) + 아이템 인벤토리 ----------
def _px(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'
def _box(x, y, w, h, line, fill):
    """모서리를 한 픽셀 깎은 픽셀 상자(외곽선 1px)."""
    return (_px(x+1, y, w-2, h, line) + _px(x, y+1, w, h-2, line)
            + _px(x+1, y+1, w-2, h-2, fill))
SLOTS = [(4.5+i*8, 48) for i in range(7)] + [(8.5+i*8, 56.5) for i in range(6)]
FACES = ["smile", "spark", "proud", "think", "shock", "sad", "doubt"]
def harubot_svg(mode="live", mood="smile", cls="", label=None):
    """mode: 'live'(장착 상태를 따라감) · 'full'(13개 모두) · 정수 n(n장 장면: 1~n-1 장착, n 장착 중)."""
    K, O, OL, CR = "#2b2118", "#ea580c", "#fb923c", "#fff7ed"
    p = []
    # 모니터
    p.append(_box(2, 1, 60, 42, K, O) + _px(3, 2, 58, 1, OL) + _px(3, 3, 1, 38, OL))
    p.append(_px(31, 2, 2, 2, K) + _px(31, 2, 1, 1, "#64748b"))  # 카메라
    p.append(_px(53, 38, 3, 2, "#ec4899", ' class="hb-led"') + _px(53, 38, 1, 1, "#f9a8d4"))  # 전원 불빛
    p.append(_px(7, 5, 50, 32, K) + _px(8, 6, 48, 30, "#cfd8e3"))
    p.append(f'<svg x="8" y="6" width="48" height="30" viewBox="0 5.5 48 30" preserveAspectRatio="xMidYMid slice">'
             f'<use class="hb-face" href="#face-{mood}" width="48" height="48"/></svg>')
    p.append(_px(8, 6, 48, 1, "rgba(255,255,255,.35)"))
    # 아이템 인벤토리(모니터 아래 RPG 아이템 창 — 하루봇의 몸이 아님)
    p.append(_box(2, 46, 60, 19, K, "#1f2937") + _px(3, 47, 58, 1, "#334155"))
    for i, (x, y) in enumerate(SLOTS, start=1):
        if mode == "full":
            st = "done"
        elif isinstance(mode, int):
            st = "done" if i < mode else ("now" if i == mode else "")
        else:
            st = ""
        p.append(f'<g class="slot {st}" data-i="{i}">'
                 f'<rect class="sl-bg" x="{x}" y="{y}" width="7" height="7"/>'
                 f'<use class="sl-it" href="#it-{i}" x="{x+0.5}" y="{y+0.5}" width="6" height="6"/></g>')
    data = f' data-mode="{mode}"'
    lab = label or ("하루봇 — 하루의 표정이 나오는 큰 모니터. 아래 아이템 창의 13자리에 아이템을 장착합니다")
    return (f'<svg class="harubot {cls}" viewBox="0 0 64 66" shape-rendering="crispEdges"{data} role="img" '
            f'aria-label="{html.escape(lab, quote=True)}">{"".join(p)}</svg>')

def face_defs():
    out = []
    for m in FACES:
        b = base64.b64encode((ASSETS / "avatar" / f"haru_{m}.webp").read_bytes()).decode()
        out.append(f'<image id="face-{m}" width="48" height="48" preserveAspectRatio="xMidYMid slice" '
                   f'style="image-rendering:pixelated" href="data:image/webp;base64,{b}"/>')
    for n, it in IT.ITEMS.items():
        out.append(f'<symbol id="it-{n}" viewBox="0 0 12 12" shape-rendering="crispEdges">{IT.sprite_rects(it[4])}</symbol>')
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{"".join(out)}</defs></svg>'

def esc(s): return html.escape(s, quote=True)

import base64

AV_USED = set()
def av(who, mood="smile"):
    name, _, col = D.CAST[who]
    AV_USED.add((who, mood))
    return f'<span class="av av-{who}-{mood}" data-who="{who}" data-mood="{mood}" role="img" aria-label="{esc(name)}"></span>'

def av_css():
    out = []
    for who, mood in sorted(AV_USED):
        b = base64.b64encode((ASSETS / "avatar" / f"{who}_{mood}.webp").read_bytes()).decode()
        out.append(f".av-{who}-{mood}{{background-image:url(data:image/webp;base64,{b})}}")
    return "\n".join(out)

def say(who, mood, text):
    return f'<div class="say" data-who="{who}">{av(who, mood)}<div><b>{esc(D.CAST[who][0])}</b> {text}</div></div>'

IMG_WH = {"cover": (1600, 900), "harubot_sheet": (1600, 900)}
def pic(name, alt, cls="pic", eager=False):
    """assets/img/의 픽셀 그림(WebP). 페이지는 저장소 루트의 index.html 기준 경로를 씁니다."""
    w, h = IMG_WH.get(name, (960, 540))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="assets/img/{name}.webp" width="{w}" height="{h}" {load} decoding="async" '
            f'alt="{html.escape(alt, quote=True)}">')

def thumb(n):
    k, part, who = D.ASSEMBLY[n]
    name = IT.ITEMS[n][1]
    names = " · ".join(D.CAST[w][0] for w in who)
    faces = "".join(av(w, "proud") for w in who)
    lab = f"{n}장 장면: {names}이(가) 하루봇의 {n}번째 자리에 아이템 '{name}'을 장착하려는 모습"
    return (f'<figure class="thumb"><div class="th-stage">{pic(f"thumb_ch{n:02d}", lab)}</div>'
            f'<figcaption><span class="chipn">{n}장 아이템</span><span class="th-it">{icon(n,"ic")}<b>{esc(name)}</b></span>'
            f'<span class="th-who">{faces}<span><b>{esc(names)}</b>이(가) 하루봇에 장착을 도와요</span></span>'
            f'<span class="th-fx">효과 — {esc(IT.ITEMS[n][2])}</span></figcaption></figure>')

def item_card(n):
    key, name, func, can, _ = IT.ITEMS[n]
    return (f'<div class="itemcard" data-item="{n}"><div class="ic-spr">{icon(n,"big")}</div>'
            f'<div class="ic-txt"><p class="ic-k">{n}장 보상 아이템</p><p class="ic-n">{esc(name)}</p>'
            f'<p class="ic-e">장착하면 <b>{esc(func)}</b>이 탑재됩니다. 퀴즈를 맞히면 자동으로 장착돼요.</p></div>'
            f'<button type="button" class="btn equip" data-item="{n}">장착하기 ▶</button></div>')

# ---------- 섹션 ----------
def sec_plain():
    ab = "".join(f'<dt>{k}</dt><dd>{esc(v[0])} — {esc(v[1])}</dd>' for k, v in D.ABBR.items())
    P = D.PLAIN
    sy = "".join(f'<tr><td class="fxp">{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td><td><a href="#lv{n}">{n}장</a></td></tr>' for a, b, c, n in D.SYMBOLS)
    return f'''<section id="plain" class="band"><div class="wrap">
<h2>처음 오신 분께 — 이 페이지를 3줄로</h2>
<ol class="three"><li><b>무엇을</b> {esc(P["what"])}</li><li><b>왜 중요한가</b> {esc(P["why"])}</li><li><b>업무에서는</b> {esc(P["work"])}</li></ol>
<p class="nocode">{esc(P["nocode"])}</p>
<details class="abbr"><summary>영어 약어 풀이</summary><dl>{ab}</dl></details>
<details class="abbr syms"><summary>기호 사전 — 이 페이지에 나오는 기호 15개 (막히면 여기로)</summary>
<table class="tbl symt"><tr><th>기호</th><th>읽는 법</th><th>뜻</th><th>처음 나오는 장</th></tr>{sy}</table></details></div></section>'''

def sec_cast():
    order = ["dr", "haru", "fly", "aba", "bot", "sia", "moa", "x1", "x2", "x3"]
    cards = "".join(f'<li>{av(k)}<div><b>{esc(D.CAST[k][0])}</b><span>{esc(D.CAST[k][1])}</span></div></li>' for k in order)
    return (f'<section id="cast"><div class="wrap"><h2>등장인물</h2><ul class="cast">{cards}</ul>'
            f'<figure class="sheet">{pic("harubot_sheet", "하루봇 설정 그림: 본체 없이 하루의 얼굴이 나오는 주황 테두리 큰 모니터(앞·옆 모습)와 그 아래 비어 있는 아이템 창 13자리")}'
            f'<figcaption>하루봇 설정 그림 — 본체 없이 큰 모니터 하나, 그 아래 아이템 창(위 7자리 · 아래 6자리)</figcaption></figure></div></section>')

def sec_why():
    ps = "".join(f"<p>{esc(x)}</p>" for x in D.WHY)
    return f'''<section id="why" class="band"><div class="wrap two"><div><h2>왜 이 가이드인가</h2>{ps}
<p class="src">원자료: {esc(M["source"])}. 이 페이지의 그림·예제·실험은 새로 만들었습니다.</p></div>
<div class="center inv">{harubot_svg("live", "smile", "big")}<p class="lvline"><b class="hb-lv">Lv.1</b> · 아이템 <b class="hb-cnt">0</b>/13</p>
<p class="cap">하루의 표정이 나오는 큰 모니터, 하루봇입니다. 아래는 하루봇의 아이템 창입니다. 장마다 아이템을 하나씩 장착하면 레벨이 오르고 새 기능이 탑재됩니다.</p>
<button type="button" class="btn ghost hb-reset">아이템 모두 빼고 처음부터</button></div></div></section>'''

def sec_map():
    cols = []
    for title, sub, ns in D.PARTS:
        items = "".join(f'<a href="#lv{n}" class="mapi">{icon(n,"sm")}<span>{n}. {esc(D.CH[n-1]["title"].split(" — ")[0])}</span></a>' for n in ns)
        cols.append(f'<div class="mapcol"><h3>{esc(title)}</h3><p>{esc(sub)}</p><div class="mapl">{items}</div></div>')
    return f'''<section id="map"><div class="wrap"><h2>큰 그림 — 두 묶음</h2><div class="mapw">{cols[0]}<div class="maparrow">→</div>{cols[1]}</div>
<p class="note">1부는 숫자가 주어졌을 때 판단하는 법, 2부는 직접 겪으며 숫자를 배우는 법입니다. 2부는 6장 말판에서 시작해 13장 행동자·평가자에서 한 바퀴를 닫습니다.</p></div></section>'''

def sec_toc():
    cards = "".join(f'<a class="tc" href="#lv{c["n"]}"><span class="tc-spr">{icon(c["n"],"big")}</span><span class="tc-it">{esc(IT.ITEMS[c["n"]][1])}</span><span><b>{c["n"]}장</b> {esc(c["title"].split(" — ")[0])}</span></a>' for c in D.CH)
    return f'<section id="toc" class="band"><div class="wrap"><h2>목차 — 하루봇 아이템 장착 순서</h2><div class="tocg">{cards}<a class="tc" href="#duel"><span class="tc-bot">{harubot_svg("full", "proud", "mini", "아이템 13개를 모두 장착한 하루봇")}</span><span><b>대결</b> 완성된 하루봇</span></a></div></div></section>'

CHREF = {1: "russell2021artificial", 2: "russell2021artificial", 3: "russell2021artificial", 4: "hart1968formal", 5: "nash1950equilibrium",
         6: "sutton2018reinforcement", 7: "sutton2018reinforcement", 8: "sutton2018reinforcement", 9: "sutton2018reinforcement",
         10: "bellman1957dynamic", 11: "sutton2018reinforcement", 12: "williams1992simple", 13: "sutton2018reinforcement"}
def refline(n):
    r = next(x for x in D.REFS if x["id"] == CHREF[n])
    au = r["author"]; names = " · ".join(a[0] for a in au[:2]) + (" 외" if len(au) > 2 else "")
    return f'<p class="note">더 읽기: <a href="#ref-{r["id"]}">{esc(names)} ({r["year"]}), {esc(r["title"])}</a></p>'

def sec_level(c):
    n = c["n"]
    why = c["why"]
    pieces = "".join(f'<tr><td class="fxp">{a}</td><td>{esc(b)}</td></tr>' for a, b in c["pieces"])
    talk = "".join(say(w, m, esc(t)) for w, m, t in c["talk"])
    ex = "".join(f"<li>{esc(x)}</li>" for x in c["explain"])
    q, opts, ans, exp = c["quiz"]
    ob = "".join(f'<button type="button" class="opt">{o}</button>' for o in opts)
    band = " band" if n % 2 == 0 else ""
    E = D.EASY2[n]
    fxl = c["fx"].split("<br>")
    fx_more = (f'<details class="fxmore"><summary>식 더 보기 (몰라도 됩니다)</summary><div class="fx sub">{"<br>".join(fxl[1:])}</div></details>'
               if len(fxl) > 1 else "")
    names = {x["n"]: x["title"].split("—")[-1].replace("(새로 더한 장)", "").strip() for x in D.CH}
    prev = f'<a href="#lv{n-1}">{n-1}장 {esc(names[n-1])}</a>' if n > 1 else "출발"
    nxt = f'<a href="#lv{n+1}">{n+1}장 {esc(names[n+1])}</a>' if n < 13 else '<a href="#duel">대결</a>'
    claim, cq, ca = E["ai"]
    return f'''<section id="lv{n}" class="level{band}"><div class="wrap stack">
<header class="lvh"><span class="lvn">{n}</span><div><h2>{esc(c["title"])}</h2><p class="tag">{esc(c["tag"])} · {esc(c["orig"])}</p></div></header>
{thumb(n)}
<p class="route">앞에서 {prev} → <b>이번 {n}장 {esc(names[n])}</b> → 다음 {nxt}</p>
<div class="dialog lvopen">{say("dr", "smile", esc(E["open"]))}</div>
<div class="words"><p class="w-k">먼저 말로 쓴 식</p><p class="w-f">{E["words"]}</p></div>
<div class="fxbox"><p class="fx-k">같은 내용을 기호로 쓰면 — 기호는 아래 조수 상자와 <a href="#plain">기호 사전</a>에서 하나씩 풀어 줍니다</p>
<div class="fx">{fxl[0]}</div>{fx_more}</div>
<div class="easy"><div class="ez-why"><h3>왜 이 방법을 쓰나</h3><p>{esc(why[0])}</p><p>{esc(why[1])}</p><p>{why[2]}</p><p class="ez">쉽게 말하면 — {esc(why[3])}</p></div>
<div class="ez-math"><h3>수학 수식을 어려워하는 조수가 대신 물어봅니다</h3>{say("haru","shock",c["ask"])}
<p class="school">학교 수학으로 보면 — <b>{esc(c["school"])}</b></p><table class="tbl pcs"><tr><th>식 조각</th><th>읽는 법</th></tr>{pieces}</table>
<p class="try"><b>숫자로 한 번 해 보기</b> {c["tryit"]}</p>{say("haru","spark",esc(c["comment"]))}</div></div>
<p class="change"><b>원자료와 다른 점</b> {c["change"]}</p>
<div class="pair"><div><h3>일상으로 치면</h3><p>{esc(c["daily"])}</p></div><div><h3>하루봇에서는</h3><p>{c["bot"]}</p></div></div>
<div class="dialog lvtalk">{talk}</div>
<div class="panel" data-exp="{n}" aria-label="{n}장 실험"><h3>실험 패널</h3></div>
<div class="aichk"><h3>AI가 이렇게 답한다면? — 그대로 믿지 말고 확인하기</h3>
<p class="ai-say"><span class="ai-tag">AI</span> “{esc(claim)}”</p><p class="ai-q"><b>확인 질문</b> {esc(cq)}</p>
<details><summary>확인 결과 보기</summary><p>{ca}</p></details></div>
<div class="explain"><h3>풀이</h3><ol>{ex}</ol><p class="lim"><b>이 방법의 한계</b> {esc(c["limit"])}</p>{refline(n)}</div>
<div class="quiz" data-ans="{ans}" data-ch="{n}"><h3>확인 퀴즈</h3><p>{q}</p><div class="opts">{ob}</div><p class="qfb" hidden data-exp="{esc(exp)}"></p></div>
{item_card(n)}
</div></section>'''

def sec_duel():
    d = D.DUEL
    rule = "".join(f"<li>{esc(x)}</li>" for x in d["rule"])
    judges = "".join(say(w, m, esc(t)) for w, m, t in d["judges"])
    return f'''<section id="duel" class="level band"><div class="wrap stack"><h2>{esc(d["title"])}</h2>
<div class="center">{pic("cover", "아이템 13개를 모두 장착한 하루봇 앞에 박사·하루·초파리 연구원·주판봇·시아·모아·X1~X3가 모인 장면", "pic wide")}<p class="cap">아이템 13개를 모두 장착한 하루봇(Lv.MAX). 이제 하루의 말투를 누가 더 빨리 배우는지 겨룹니다.</p></div>
<ol class="rules">{rule}</ol><div class="dialog lvtalk">{judges}</div>
<div class="panel" data-exp="duel" aria-label="대결 실험"><h3>대결 패널</h3></div>
<p class="note">{esc(d["result"])}</p></div></section>'''

def sec_summary():
    rows = []
    for c in D.CH:
        short = re.split(r"(?<=다)\. ", re.sub("<[^>]+>", "", c["change"]))[0].rstrip(".") + "."
        rows.append(f'<tr><td>{c["n"]}</td><td>{icon(c["n"],"sm")}</td><td class="fxs">{c["fx"]}</td><td>{esc(c["title"].split(" — ")[0])}</td><td>{esc(short)}</td></tr>')
    return f'''<section id="summary"><div class="wrap"><h2>정리 — 바로잡은 공식 13개</h2><div class="scroll"><table class="tbl sum">
<tr><th>장</th><th>아이템</th><th>공식</th><th>한 줄</th><th>원자료와 다른 점</th></tr>{"".join(rows)}</table></div></div></section>'''

def sec_outro():
    return f'<section id="outro" class="band"><div class="wrap"><h2>아웃트로</h2><div class="dialog">{"".join(say(w,m,esc(t)) for w,m,t in D.OUTRO)}</div><p class="next">{esc(D.NEXT)}</p></div></section>'

def sec_refs():
    li = "".join(f'<li id="ref-{r["id"]}">{esc(r["text"])}</li>' for r in D.REFS)
    return f'<section id="refs"><div class="wrap"><h2>참고 문헌</h2><ol class="refs">{li}</ol></div></section>'

CSS = (ROOT / "style.css").read_text(encoding="utf-8")
JS = (ROOT / "engine.js").read_text(encoding="utf-8")
IJS = (ROOT / "items.js").read_text(encoding="utf-8")
def items_json():
    return json.dumps([{"n": n, "name": it[1], "func": it[2], "can": it[3], "svg": icon(n, "pop")} for n, it in IT.ITEMS.items()],
                      ensure_ascii=False).replace("</", "<\\/")
def popup_html():
    return (f'<div class="hbpop" hidden role="dialog" aria-modal="true" aria-labelledby="hbpop-t"><div class="hbwin">'
            f'<p class="hbp-k" id="hbpop-t">✦ 아이템 획득 ✦</p><div class="hbp-row"><div class="hbp-spr"></div>'
            f'<div class="hbp-bot">{harubot_svg("live", "spark", "pop", "아이템을 장착한 하루봇")}</div></div>'
            f'<p class="hbp-n"></p><p class="hbp-m"></p><p class="hbp-lv"></p>'
            f'<button type="button" class="btn hbp-ok">확인 ▶</button></div></div>'
            f'<a class="hbhud" href="#why" aria-label="하루봇 상태 보기"><span class="hud-face"><svg viewBox="0 0 48 48"><use href="#face-smile" class="hb-face"/></svg></span>'
            f'<span><b class="hb-lv">Lv.1</b><small><span class="hb-cnt">0</span>/13</small></span></a>')

ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": M["title"], "description": M["desc"],
      "inLanguage": "ko", "dateCreated": M["date"], "educationalLevel": "입문",
      "creator": {"@type": "Person", "name": M["author"], "url": M["site"], "affiliation": M["affil"]}}

page = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(M["title"])}</title><meta name="description" content="{esc(M["desc"])}">
<meta property="og:title" content="{esc(M["title"])}"><meta property="og:description" content="{esc(M["desc"])}">
<meta property="og:image" content="https://adminmrobo.github.io/agentic_ai_crash_guide/assets/img/og_cover.webp"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}\n/*AVCSS*/</style></head>
<body><a id="top"></a>{face_defs()}
<nav class="topnav"><div class="wrap"><a href="#top">{esc(M["short"])}</a><span><button type="button" class="sndbtn" aria-pressed="true">♪ 효과음 켬</button><a href="#toc">목차</a><a href="#duel">대결</a><a href="#summary">정리</a></span></div></nav>
<header class="hero" id="hero"><div class="wrap two"><div><p class="kicker">{esc(M["series"])} · {M["number"]}</p>
<h1>AI 에이전트 공식 속성 가이드<br><small>하루봇을 만들며 배우는 13장</small></h1><p class="lead">{esc(M["desc"])}</p>
<div class="dialog">{say("haru","smile","저를 닮은 챗봇을 만든대요. 이름은 하루봇!")}{say("dr","proud","장마다 아이템을 하나씩 장착하면서, 아이템마다 들어 있는 수식을 같이 익혀 보자. 장착할 때마다 하루봇의 레벨이 올라.")}</div></div>
<div class="center hero-bot">{pic("cover", "표지: 하루의 얼굴이 나오는 큰 모니터 하루봇과 그 아래 아이템 창, 둘레에 모인 연구실 식구들", "pic wide", True)}</div></div></header>
{sec_plain()}{sec_cast()}{sec_why()}{sec_map()}{sec_toc()}
{"".join(sec_level(c) for c in D.CH)}
{sec_duel()}{sec_summary()}{sec_outro()}{sec_refs()}
<footer class="foot"><div class="wrap"><p>글 · {esc(M["author"])} (<a href="{M["site"]}">{M["site"]}</a>) · {esc(M["affil"])}</p>
<p class="src">원자료: {esc(M["source"])}. 공식은 이 페이지에서 바로잡아 다시 썼습니다.</p></div></footer>
{popup_html()}<script>window.HB_ITEMS={items_json()};{JS}\n{IJS}</script></body></html>'''

page = page.replace("/*AVCSS*/", av_css())
out = ROOT / "dist" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print("built", out, len(page.encode("utf-8")) // 1024, "KB")
