# -*- coding: utf-8 -*-
"""그림 목록·프롬프트 파일 IMG_PROMPTS.md 생성."""
import pathlib
import data_ko as D

LOOK = {
 "dr": "the chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie)",
 "haru": "the girl assistant Haru (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans)",
 "fly": "the anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings)",
 "aba": "the boxy beige retro CRT-monitor robot AbaBot (dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads)",
 "in1": "intern 1 (maid-style uniform, black hair)",
 "in2": "intern 2 (maid-style uniform, beige hair)",
 "x1": "extra X1 (small cute character drawn as a solid black silhouette with round white eyes)",
 "x2": "extra X2 (small cute character drawn as a solid black silhouette with round white eyes, slightly taller)",
 "x3": "extra X3 (small cute character drawn as a solid black silhouette with round white eyes, slightly rounder)",
}
PART_EN = {
 "magnifier": "a magnifying-glass sensor", "scale": "a small balance scale", "hourglass": "an hourglass-shaped battery",
 "compass": "a compass chip with a route line", "plug": "a two-pronged connector plug", "board": "a game-board-like circuit board",
 "coins": "a stack of coins that get smaller toward the top", "gauge": "a dashboard gauge with a needle",
 "stars": "a panel of star-shaped buttons", "mirror": "a coil made of two facing mirrors", "speaker": "a speaker with a dial",
 "sticker": "a card slot holding score stickers (a checkmark sticker, no numbers)", "monocle": "a judge's monocle lens",
}
HARUBOT = ("HaruBot, a large friendly robot whose body is shaped like a chat speech bubble (cream body, thick orange outline, "
           "speech-bubble tail at the lower left), with a separate rounded monitor head showing two pink dot eyes and a small smile, "
           "a short antenna with a pink ball, and thirteen square slots on its chest arranged in three rows (5 on top, 4 in the middle, 4 at the bottom)")
STYLE = ("Match the art style, proportions and colors of the attached reference images exactly. "
         "Bright daytime laboratory, white walls, soft daylight, light teal and orange accents, clean and friendly. "
         "No text, no letters, no numbers, no logos, no real brands.")

def eul(w):
    c = ord(w[-1]) - 0xAC00
    return w + ("을" if 0 <= c < 11172 and c % 28 else "를")

def slot_desc(n):
    if n <= 5: return f"slot {n} counting from the left in the top row"
    if n <= 9: return f"slot {n-5} counting from the left in the middle row"
    return f"slot {n-9} counting from the left in the bottom row"

out = ["# 그림 목록과 프롬프트 — AI 에이전트 공식 속성 가이드", "",
       "## 쓰는 법",
       "1. 참고 이미지로 캐릭터 기본 그림(fruitfly-lab-expressions 저장소: 박사·조수·초파리 연구원·주판봇·인턴1·인턴2·X1~X3)을 함께 올립니다.",
       "2. **00 하루봇 설정 그림을 먼저** 받아 확정합니다. 이후 모든 요청에 이 그림을 참고 이미지로 함께 올립니다.",
       "3. 그다음 01 표지 → 02~14 장별 썸네일 순서로 요청합니다. 한 대화에 3~5장씩, 같은 비율끼리 묶습니다.",
       "4. 받은 그림은 아래 저장 이름으로 돌려주세요. 페이지 반영 때 표지 1600×900, 썸네일 960×540 WebP로 줄입니다(합계 600KB 이하).",
       "", "## 한눈에 보기", "", "| 번호 | 저장 이름 | 장면 | 등장 |", "|---|---|---|---|",
       "| 00 | harubot_sheet.png | 하루봇 설정 그림(앞·옆, 빈 부품 자리 13곳) | 하루봇 |",
       "| 01 | cover.png | 완성된 하루봇 앞에 아홉 명이 모두 모인 장면 | 전원 |"]
for n in range(1, 14):
    k, part, who = D.ASSEMBLY[n]
    out.append(f"| {n+1:02d} | thumb_ch{n:02d}.png | {n}장: {eul(part)} 끼움 (자리 {n}) | {' · '.join(D.CAST[w][0] for w in who)} |")

out += ["", "## 00 하루봇 설정 그림", "", "```",
        "Character reference sheet, 16:9, white background.",
        f"Design a new original character: {HARUBOT}.",
        "Show a front view and a three-quarter side view. All thirteen chest slots are EMPTY (dashed outlines).",
        "Simple, cute, toy-like, thick clean outlines. No text, no letters, no numbers, no logos.", "```", "",
        "## 01 표지", "", "```", "Website top cover illustration, wide 16:9, width 1920px or more.", STYLE,
        f"Center: {HARUBOT}, now COMPLETE: every slot holds its part (magnifier, scale, hourglass, compass, plug, circuit board, coin stack, gauge, star buttons, mirror coil, speaker, sticker card, monocle).",
        "Around it, all nine characters celebrate together: " + "; ".join(LOOK[k] for k in ["dr", "haru", "fly", "aba", "in1", "in2", "x1", "x2", "x3"]) + ".",
        "The fruit fly is on the left facing right, AbaBot on the right facing left, the scientist at the back center.",
        "Keep faces and hands inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain and simple.",
        "Mood: proud, cheerful, the moment the robot is finished.", "```", "", "대체 글: 완성된 하루봇 앞에 연구실 식구 아홉 명이 모여 기뻐하는 장면.", ""]
for n in range(1, 14):
    k, part, who = D.ASSEMBLY[n]
    names = " · ".join(D.CAST[w][0] for w in who)
    done = "Slots 1 to %d already hold their parts; " % (n - 1) if n > 1 else "All slots are still empty; "
    out += [f"## {n+1:02d} {n}장 썸네일 — {part} ({names})", "", "```",
            "Chapter thumbnail, 16:9.", STYLE,
            f"Scene: {HARUBOT} stands center-right. {done}the remaining slots are empty with dashed outlines.",
            f"{'; '.join(LOOK[w] for w in who)} {'is' if len(who)==1 else 'are'} carefully inserting {PART_EN[k]} into {slot_desc(n)}, which glows softly.",
            "HaruBot looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.",
            "```", "", f"대체 글: {names}이(가) 하루봇의 {n}번째 자리에 {eul(part)} 끼우는 장면.", ""]
out += ["## 고칠 때(같은 대화에서)", "", "```", "Same characters, same art style and composition. Change only: {고칠 점}. Still no text.", "```"]
pathlib.Path(__file__).with_name("IMG_PROMPTS.md").write_text("\n".join(out), encoding="utf-8")
print("ok", len(out))
