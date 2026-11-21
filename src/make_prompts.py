# -*- coding: utf-8 -*-
"""그림 목록·프롬프트 파일 IMG_PROMPTS.md 생성."""
import pathlib
import data_ko as D
import items as IT

LOOK = {
 "dr": "the chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie)",
 "haru": "the girl assistant Haru (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans)",
 "fly": "the anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings)",
 "aba": "the boxy beige retro CRT-monitor robot AbaBot (dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads)",
 "sia": "Sia the maid intern (long straight jet-black hair, calm gray eyes, charcoal-black maid dress, long white frilled apron, large gray bow, no headdress)",
 "moa": "Moa the maid intern (long ash-beige wavy hair, white frilled maid headband, amber-brown eyes, camel cardigan, red and navy plaid bow tie, white apron)",
 "x1": "unrevealed extra X1 (cute solid silhouette filled with flat very dark navy-black #1B1A2E, thin dithered purple rim light, two round white dot eyes, pink blush pixels, pink hair bow, ponytail)",
 "x2": "unrevealed extra X2 (cute solid navy-black silhouette with purple rim light, white dot eyes, teal round glasses, beret)",
 "x3": "unrevealed extra X3 (cute solid navy-black silhouette with purple rim light, white dot eyes, cat-ear hood with two small gold pompoms)",
}
PART_EN = {
 "magnifier": "a magnifying-glass sensor", "scale": "a small balance scale", "hourglass": "an hourglass-shaped battery",
 "compass": "a compass chip with a route line", "plug": "a two-pronged connector plug", "board": "a game-board-like circuit board",
 "coins": "a stack of coins that get smaller toward the top", "gauge": "a dashboard gauge with a needle",
 "stars": "a panel of star-shaped buttons", "mirror": "a coil made of two facing mirrors", "speaker": "a speaker with a dial",
 "sticker": "a card slot holding score stickers (a checkmark sticker, no numbers)", "monocle": "a judge's monocle lens",
}
HARUBOT = ("HaruBot, which is ONLY a large wide monitor (no body, no stand, no base, no wheels, no legs, no arms): a big screen with a thick orange bezel and a small pink power light; "
           "the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) "
           "as a bust-up portrait with a clear facial expression, the same character and design as the attached Haru reference; "
           "right below the monitor floats a separate dark RPG-style inventory bar with thirteen square item slots in two rows (7 on top, 6 below), like a game UI, not part of the monitor")
STYLE = ("Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. "
         "Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). "
         "Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. "
         "No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.")

def eul(w):
    c = ord(w[-1]) - 0xAC00
    return w + ("을" if 0 <= c < 11172 and c % 28 else "를")

def slot_desc(n):
    if n <= 7: return f"inventory slot {n} counting from the left in the top row"
    return f"inventory slot {n-7} counting from the left in the bottom row"

out = ["# 그림 목록과 프롬프트 — AI 에이전트 공식 속성 가이드", "",
       "## 쓰는 법 (v4 — 픽셀 화풍 · 모니터만 있는 하루봇 · RPG 아이템)",
       "v1(2026-11-19) 그림은 화풍 지정이 빠져 일반 일러스트(말풍선 로봇)로 나와 픽셀 방침을 어겼으므로 페이지와 저장소에서 모두 뺐습니다(2026-11-21). 지금 페이지의 하루봇·아이템은 코드로 그린 픽셀 그림이라 그림 파일 없이도 완성돼 있습니다. 아래 프롬프트는 표지·썸네일을 일러스트 픽셀 그림으로 바꾸고 싶을 때 씁니다. 반드시 16비트 SNES 픽셀 아트로 받습니다.",
       "1. 모든 요청에 fruitfly-lab-expressions 저장소의 참고 그림을 함께 올립니다: images/_sheets/lab6_lineup.png(박사·하루·초파리·주판봇·시아·모아), images/_sheets/spares_sheet.png(X1~X3). 하루봇은 **본체 없이 하루의 표정이 나오는 큰 모니터 하나**입니다(받침·바퀴·다리·팔 없음). 아이템 13자리는 모니터 아래 따로 뜬 RPG 아이템 창입니다. 하루봇이 나오는 모든 요청에 images/haru/E01_joy.png(모니터 속 하루 얼굴 기준)도 올립니다. v1의 말풍선 로봇 디자인은 쓰지 않습니다.",
       "2. **00 하루봇 설정 그림을 먼저** 받아 확정합니다. 이후 모든 요청에 이 그림을 참고 이미지로 함께 올립니다.",
       "3. 그다음 01 표지 → 02~14 장별 썸네일 순서로 요청합니다. 한 대화에 3~5장씩, 같은 비율끼리 묶습니다.",
       "4. 받은 그림은 아래 저장 이름으로 돌려주세요. 페이지 반영 때 표지 1600×900, 썸네일 960×540 WebP로 줄입니다(합계 600KB 이하).",
       "", "## 한눈에 보기", "", "| 번호 | 저장 이름 | 장면 | 등장 |", "|---|---|---|---|",
       "| 00 | harubot_sheet.png | 하루봇 설정 그림 — 하루의 표정이 나오는 큰 모니터(앞·옆)와 빈 아이템 창 13자리 | 하루봇 |",
       "| 01 | cover.png | 완성된 하루봇 앞에 아홉 명이 모두 모인 장면 | 전원 |"]
for n in range(1, 14):
    k, part, who = D.ASSEMBLY[n]
    out.append(f"| {n+1:02d} | thumb_ch{n:02d}.png | {n}장: 아이템 「{IT.ITEMS[n][1]}」 장착 (자리 {n}) | {' · '.join(D.CAST[w][0] for w in who)} |")

out += ["", "## 00 하루봇 설정 그림", "", "```",
        "Character reference sheet, 16:9, white background.",
        f"Design an original character: {HARUBOT}.",
        "Show a front view and a three-quarter side view of the monitor, with the inventory bar below the front view. All thirteen inventory slots are EMPTY (dashed outlines). Haru on the screen smiles (same face as the attached Haru E01_joy expression).",
        "Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, same pixel density as the attached lab character lineup; the monitor is about as wide as the scientist character is tall.",
        "Plain flat white background. No anime illustration style, no smooth gradients. No text, no letters, no numbers, no logos.", "```", "",
        "## 01 표지", "", "```", "Website top cover illustration, wide 16:9, width 1920px or more.", STYLE,
        f"Center: {HARUBOT}, now fully equipped like a max-level RPG hero: every item slot holds its glowing item (magnifier, scale, hourglass, compass, plug, circuit board, coin stack, gauge, star, mirror coil, speaker, sticker card, monocle); Haru on the screen beams proudly.",
        "Around it, all nine characters celebrate together: " + "; ".join(LOOK[k] for k in ["dr", "haru", "fly", "aba", "sia", "moa", "x1", "x2", "x3"]) + ".",
        "The fruit fly is on the left facing right, AbaBot on the right facing left, the scientist at the back center.",
        "Keep faces and hands inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain and simple.",
        "Mood: proud, cheerful, a level-up celebration with small pixel sparkles.", "```", "", "대체 글: 완성된 하루봇 앞에 연구실 식구 아홉 명이 모여 기뻐하는 장면.", ""]
for n in range(1, 14):
    k, part, who = D.ASSEMBLY[n]
    names = " · ".join(D.CAST[w][0] for w in who)
    if n > 1:
        held = ", ".join(f"slot {i}: {PART_EN[D.ASSEMBLY[i][0]]}" for i in range(1, n))
        done = f"Item slots 1 to {n-1} already hold exactly these items, each as a small pixel icon ({held}); "
    else:
        done = "All item slots are still empty; "
    out += [f"## {n+1:02d} {n}장 썸네일 — 아이템 「{IT.ITEMS[n][1]}」 ({names})", "", "```",
            "Chapter thumbnail, 16:9.", STYLE,
            f"Scene: {HARUBOT} floats in the lab, center-right. {done}the remaining slots are empty with dashed outlines.",
            f"{'; '.join(LOOK[w] for w in who)} {'is' if len(who)==1 else 'are'} handing over {PART_EN[k]}, like an RPG item drop, and it is being equipped into {slot_desc(n)}, which shines with a small pixel level-up sparkle.",
            "Haru on the HaruBot screen shows an excited, sparkling-eyes expression. Faces and hands stay inside the central safe area; bottom-left corner plain.",
            "```", "", f"대체 글: {names}이(가) 하루봇의 {n}번째 자리에 아이템 「{IT.ITEMS[n][1]}」을(를) 장착하는 장면.", ""]
out += ["## 고칠 때(같은 대화에서)", "", "```", "Same characters, same art style and composition. Change only: {고칠 점}. Still no text.", "```"]
pathlib.Path(__file__).with_name("IMG_PROMPTS.md").write_text("\n".join(out), encoding="utf-8")
print("ok", len(out))
