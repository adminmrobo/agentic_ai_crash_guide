# -*- coding: utf-8 -*-
"""data_ko.py + engine.js → index.html (단일 파일). 사용: python3 build.py"""
import html, json, re, pathlib
import data_ko as D

ROOT = pathlib.Path(__file__).parent
M = D.META

# ---------- 부품 아이콘 (원본 그림, 48×48) ----------
ICON = {
 "magnifier": '<circle cx="20" cy="20" r="11"/><line x1="28" y1="28" x2="40" y2="40"/>',
 "scale": '<line x1="24" y1="8" x2="24" y2="40"/><line x1="10" y1="14" x2="38" y2="14"/><path d="M10 14 L5 26 H15 Z"/><path d="M38 14 L33 26 H43 Z"/><line x1="16" y1="40" x2="32" y2="40"/>',
 "hourglass": '<path d="M13 7 H35 M13 41 H35 M15 7 C15 18 33 20 33 24 C33 28 15 30 15 41 M33 7 C33 18 15 20 15 24 C15 28 33 30 33 41"/>',
 "compass": '<circle cx="24" cy="24" r="16"/><path d="M24 12 L28 24 L24 36 L20 24 Z"/>',
 "plug": '<rect x="14" y="20" width="20" height="14" rx="3"/><line x1="19" y1="20" x2="19" y2="10"/><line x1="29" y1="20" x2="29" y2="10"/><path d="M24 34 V40 M24 40 H14 M24 40 H34"/>',
 "board": '<rect x="8" y="8" width="32" height="32" rx="3"/><path d="M8 19 H40 M8 29 H40 M19 8 V40 M29 8 V40"/><path d="M13 13 L24 24 L35 35" class="hl"/>',
 "coins": '<ellipse cx="24" cy="38" rx="14" ry="4"/><ellipse cx="24" cy="30" rx="11" ry="3.5"/><ellipse cx="24" cy="23" rx="8" ry="3"/><ellipse cx="24" cy="17" rx="5" ry="2.5"/>',
 "gauge": '<path d="M8 32 A16 16 0 0 1 40 32"/><line x1="24" y1="32" x2="33" y2="20"/><circle cx="24" cy="32" r="2.5"/>',
 "stars": '<path d="M24 8 L28 18 L39 18 L30 25 L33 36 L24 29 L15 36 L18 25 L9 18 L20 18 Z"/>',
 "mirror": '<path d="M12 10 V38 M36 10 V38"/><path d="M16 18 C22 14 26 14 32 18" /><path d="M32 30 C26 34 22 34 16 30"/><path d="M29 15 L32 18 L28 20 M19 33 L16 30 L20 28"/>',
 "speaker": '<path d="M8 19 H15 L24 11 V37 L15 29 H8 Z"/><path d="M30 18 C33 21 33 27 30 30 M34 14 C39 19 39 29 34 34"/>',
 "sticker": '<rect x="10" y="8" width="28" height="32" rx="4"/><path d="M17 24 L22 29 L31 18"/>',
 "monocle": '<circle cx="21" cy="21" r="12"/><circle cx="21" cy="21" r="7"/><path d="M30 30 C34 36 36 40 40 42"/>',
}
def icon(k, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true">{ICON[k]}</svg>'

# ---------- 하루봇 조립 그림(자리표시) ----------
SLOTS = [(52+i*44, 132) for i in range(5)] + [(74+i*44, 176) for i in range(4)] + [(74+i*44, 220) for i in range(4)]
def harubot_svg(n, big=False):
    """n장까지 조립된 하루봇. n=0이면 빈 몸체, 14면 완성."""
    parts = []
    parts.append('<rect x="30" y="96" width="240" height="160" rx="26" class="hb-body"/>'
                 '<path d="M80 256 L64 286 L118 256 Z" class="hb-body"/>'
                 '<rect x="80" y="20" width="140" height="66" rx="18" class="hb-head"/>'
                 '<circle cx="124" cy="52" r="8" class="hb-eye"/><circle cx="176" cy="52" r="8" class="hb-eye"/>'
                 '<path d="M132 70 Q150 80 168 70" class="hb-mouth"/>'
                 '<line x1="150" y1="20" x2="150" y2="6" class="hb-line"/><circle cx="150" cy="5" r="5" class="hb-ant"/>')
    for i, (x, y) in enumerate(SLOTS, start=1):
        k = D.ASSEMBLY[i][0]
        cls = "slot done" if i < n or n == 14 else ("slot now" if i == n else "slot")
        parts.append(f'<g class="{cls}"><rect x="{x-18}" y="{y-18}" width="36" height="36" rx="8"/>'
                     + (f'<g transform="translate({x-14},{y-14}) scale(0.5833)">{ICON[k]}</g>' if (i <= n or n == 14) else "")
                     + '</g>')
    vb = "0 0 300 300"
    return f'<svg class="harubot{" big" if big else ""}" viewBox="{vb}" role="img" aria-label="하루봇 조립 {min(n,13)}/13">{"".join(parts)}</svg>'

def esc(s): return html.escape(s, quote=True)

import base64
IMGDIR = ROOT / "assets" / "img"
PICS = {"cover": "cover.webp", "front": "harubot_front.webp", **{f"ch{n:02d}": f"thumb_ch{n:02d}.webp" for n in range(1, 14)}}
def pic_css():
    out = []
    for k, f in PICS.items():
        b = base64.b64encode((IMGDIR / f).read_bytes()).decode()
        out.append(f".im-{k}{{background-image:url(data:image/webp;base64,{b})}}")
    return "\n".join(out)
ALT = {"cover": "완성된 하루봇 앞에 연구실 식구 아홉 명이 모여 기뻐하는 장면",
       "front": "아직 부품 자리 13곳이 비어 있는 하루봇"}
def pic(k, cls="pic", alt=None):
    a = alt or ALT.get(k, "")
    return f'<div class="{cls} im-{k}" role="img" aria-label="{esc(a)}"></div>'

AV_USED = set()
def av(who, mood="smile"):
    name, _, col = D.CAST[who]
    AV_USED.add((who, mood))
    return f'<span class="av av-{who}-{mood}" data-who="{who}" data-mood="{mood}" role="img" aria-label="{esc(name)}"></span>'

def av_css():
    out = []
    for who, mood in sorted(AV_USED):
        b = base64.b64encode((ROOT / "assets" / "avatar" / f"{who}_{mood}.webp").read_bytes()).decode()
        out.append(f".av-{who}-{mood}{{background-image:url(data:image/webp;base64,{b})}}")
    return "\n".join(out)

def say(who, mood, text):
    return f'<div class="say" data-who="{who}">{av(who, mood)}<div><b>{esc(D.CAST[who][0])}</b> {text}</div></div>'

def thumb(n):
    k, part, who = D.ASSEMBLY[n]
    names = " · ".join(D.CAST[w][0] for w in who)
    alt = f"{names}이(가) 하루봇의 {n}번째 자리에 {part} 부품을 끼우는 장면"
    return (f'<figure class="thumb">{pic(f"ch{n:02d}", "pic", alt)}'
            f'<figcaption><span class="chipn">{n}장</span> {icon(k,"ic sm")} {esc(part)} — <b>{esc(names)}</b>이(가) 끼웁니다</figcaption></figure>')

# ---------- 섹션 ----------
def sec_plain():
    ab = "".join(f'<dt>{k}</dt><dd>{esc(v[0])} — {esc(v[1])}</dd>' for k, v in D.ABBR.items())
    P = D.PLAIN
    return f'''<section id="plain" class="band"><div class="wrap">
<h2>처음 오신 분께 — 이 페이지를 3줄로</h2>
<ol class="three"><li><b>무엇을</b> {esc(P["what"])}</li><li><b>왜 중요한가</b> {esc(P["why"])}</li><li><b>업무에서는</b> {esc(P["work"])}</li></ol>
<p class="nocode">{esc(P["nocode"])}</p>
<details class="abbr"><summary>영어 약어 풀이</summary><dl>{ab}</dl></details></div></section>'''

def sec_cast():
    order = ["dr", "haru", "fly", "aba", "bot", "sia", "moa", "x1", "x2", "x3"]
    cards = "".join(f'<li>{av(k)}<div><b>{esc(D.CAST[k][0])}</b><span>{esc(D.CAST[k][1])}</span></div></li>' for k in order)
    return f'<section id="cast"><div class="wrap"><h2>등장인물</h2><ul class="cast">{cards}</ul></div></section>'

def sec_why():
    ps = "".join(f"<p>{esc(x)}</p>" for x in D.WHY)
    return f'''<section id="why" class="band"><div class="wrap two"><div><h2>왜 이 가이드인가</h2>{ps}
<p class="src">원자료: {esc(M["source"])}. 이 페이지의 그림·예제·실험은 새로 만들었습니다.</p></div>
<div class="center">{pic("front", "pic front")}<p class="cap">아직 비어 있는 하루봇. 13장을 지나며 부품 13개가 하나씩 끼워집니다.</p></div></div></section>'''

def sec_map():
    cols = []
    for title, sub, ns in D.PARTS:
        items = "".join(f'<a href="#lv{n}" class="mapi">{icon(D.ASSEMBLY[n][0],"ic sm")}<span>{n}. {esc(D.CH[n-1]["title"].split(" — ")[0])}</span></a>' for n in ns)
        cols.append(f'<div class="mapcol"><h3>{esc(title)}</h3><p>{esc(sub)}</p><div class="mapl">{items}</div></div>')
    return f'''<section id="map"><div class="wrap"><h2>큰 그림 — 두 묶음</h2><div class="mapw">{cols[0]}<div class="maparrow">→</div>{cols[1]}</div>
<p class="note">1부는 숫자가 주어졌을 때 판단하는 법, 2부는 직접 겪으며 숫자를 배우는 법입니다. 2부는 6장 말판에서 시작해 13장 행동자·평가자에서 한 바퀴를 닫습니다.</p></div></section>'''

def sec_toc():
    cards = "".join(f'<a class="tc" href="#lv{c["n"]}">{pic(f"ch{c['n']:02d}", "pic", f"{c['n']}장 썸네일")}<span><b>{c["n"]}장</b> {esc(c["title"].split(" — ")[0])}</span></a>' for c in D.CH)
    return f'<section id="toc" class="band"><div class="wrap"><h2>목차 — 하루봇 조립 순서</h2><div class="tocg">{cards}<a class="tc" href="#duel">{pic("cover")}<span><b>대결</b> 완성된 하루봇</span></a></div></div></section>'

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
    return f'''<section id="lv{n}" class="level{band}"><div class="wrap stack">
<header class="lvh"><span class="lvn">{n}</span><div><h2>{esc(c["title"])}</h2><p class="tag">{esc(c["tag"])} · {esc(c["orig"])}</p></div></header>
{thumb(n)}
<div class="fx">{c["fx"]}</div>
<div class="easy"><div class="ez-why"><h3>왜 이 방법을 쓰나</h3><p>{esc(why[0])}</p><p>{esc(why[1])}</p><p>{why[2]}</p><p class="ez">쉽게 말하면 — {esc(why[3])}</p></div>
<div class="ez-math"><h3>수학 수식을 어려워하는 조수가 대신 물어봅니다</h3>{say("haru","shock",c["ask"])}
<p class="school">학교 수학으로 보면 — <b>{esc(c["school"])}</b></p><table class="tbl pcs"><tr><th>식 조각</th><th>읽는 법</th></tr>{pieces}</table>
<p class="try"><b>숫자로 한 번 해 보기</b> {c["tryit"]}</p>{say("haru","spark",esc(c["comment"]))}</div></div>
<p class="change"><b>원자료와 다른 점</b> {c["change"]}</p>
<div class="pair"><div><h3>일상으로 치면</h3><p>{esc(c["daily"])}</p></div><div><h3>하루봇에서는</h3><p>{c["bot"]}</p></div></div>
<div class="dialog lvtalk">{talk}</div>
<div class="panel" data-exp="{n}" aria-label="{n}장 실험"><h3>실험 패널</h3></div>
<div class="explain"><h3>풀이</h3><ol>{ex}</ol><p class="lim"><b>이 방법의 한계</b> {esc(c["limit"])}</p>{refline(n)}</div>
<div class="quiz" data-ans="{ans}"><h3>확인 퀴즈</h3><p>{q}</p><div class="opts">{ob}</div><p class="qfb" hidden data-exp="{esc(exp)}"></p></div>
</div></section>'''

def sec_duel():
    d = D.DUEL
    rule = "".join(f"<li>{esc(x)}</li>" for x in d["rule"])
    judges = "".join(say(w, m, esc(t)) for w, m, t in d["judges"])
    return f'''<section id="duel" class="level band"><div class="wrap stack"><h2>{esc(d["title"])}</h2>
<div class="center">{pic("cover", "pic wide")}<p class="cap">13개 부품이 모두 끼워진 하루봇. 이제 하루의 말투를 누가 더 빨리 배우는지 겨룹니다.</p></div>
<ol class="rules">{rule}</ol><div class="dialog lvtalk">{judges}</div>
<div class="panel" data-exp="duel" aria-label="대결 실험"><h3>대결 패널</h3></div>
<p class="note">{esc(d["result"])}</p></div></section>'''

def sec_summary():
    rows = []
    for c in D.CH:
        short = re.split(r"(?<=다)\. ", re.sub("<[^>]+>", "", c["change"]))[0].rstrip(".") + "."
        rows.append(f'<tr><td>{c["n"]}</td><td>{icon(D.ASSEMBLY[c["n"]][0],"ic sm")}</td><td class="fxs">{c["fx"]}</td><td>{esc(c["title"].split(" — ")[0])}</td><td>{esc(short)}</td></tr>')
    return f'''<section id="summary"><div class="wrap"><h2>정리 — 바로잡은 공식 13개</h2><div class="scroll"><table class="tbl sum">
<tr><th>장</th><th>부품</th><th>공식</th><th>한 줄</th><th>원자료와 다른 점</th></tr>{"".join(rows)}</table></div></div></section>'''

def sec_outro():
    return f'<section id="outro" class="band"><div class="wrap"><h2>아웃트로</h2><div class="dialog">{"".join(say(w,m,esc(t)) for w,m,t in D.OUTRO)}</div><p class="next">{esc(D.NEXT)}</p></div></section>'

def sec_refs():
    li = "".join(f'<li id="ref-{r["id"]}">{esc(r["text"])}</li>' for r in D.REFS)
    return f'<section id="refs"><div class="wrap"><h2>참고 문헌</h2><ol class="refs">{li}</ol></div></section>'

CSS = (ROOT / "style.css").read_text(encoding="utf-8")
JS = (ROOT / "engine.js").read_text(encoding="utf-8")

ld = {"@context": "https://schema.org", "@type": "LearningResource", "name": M["title"], "description": M["desc"],
      "inLanguage": "ko", "dateCreated": M["date"], "educationalLevel": "입문",
      "creator": {"@type": "Person", "name": M["author"], "url": M["site"], "affiliation": M["affil"]}}

page = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(M["title"])}</title><meta name="description" content="{esc(M["desc"])}">
<meta property="og:title" content="{esc(M["title"])}"><meta property="og:description" content="{esc(M["desc"])}">
<meta property="og:image" content="https://adminmrobo.github.io/agentic_ai_crash_guide/assets/img/og_cover.webp"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}\n{pic_css()}\n/*AVCSS*/</style></head>
<body><a id="top"></a>
<nav class="topnav"><div class="wrap"><a href="#top">{esc(M["short"])}</a><span><a href="#toc">목차</a><a href="#duel">대결</a><a href="#summary">정리</a></span></div></nav>
<header class="hero" id="hero"><div class="wrap two"><div><p class="kicker">{esc(M["series"])} · {M["number"]}</p>
<h1>AI 에이전트 공식 속성 가이드<br><small>하루봇을 만들며 배우는 13장</small></h1><p class="lead">{esc(M["desc"])}</p>
<div class="dialog">{say("haru","smile","저를 닮은 챗봇을 만든대요. 이름은 하루봇!")}{say("dr","proud","부품 13개를 하나씩 끼우면서, 부품마다 들어 있는 수식을 같이 익혀 보자.")}</div></div>
<div class="center">{pic("cover", "pic wide")}</div></div></header>
{sec_plain()}{sec_cast()}{sec_why()}{sec_map()}{sec_toc()}
{"".join(sec_level(c) for c in D.CH)}
{sec_duel()}{sec_summary()}{sec_outro()}{sec_refs()}
<footer class="foot"><div class="wrap"><p>글 · {esc(M["author"])} (<a href="{M["site"]}">{M["site"]}</a>) · {esc(M["affil"])}</p>
<p class="src">원자료: {esc(M["source"])}. 공식은 이 페이지에서 바로잡아 다시 썼습니다.</p></div></footer>
<script>{JS}</script></body></html>'''

page = page.replace("/*AVCSS*/", av_css())
out = ROOT / "dist" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print("built", out, len(page.encode("utf-8")) // 1024, "KB")
