# 그림 목록과 프롬프트 — AI 에이전트 공식 속성 가이드

## 쓰는 법 (v2 — 픽셀 화풍)
v1(2026-11-19)은 화풍 지정이 빠져 일반 일러스트로 나왔습니다. v2는 연구실 정본과 같은 16비트 SNES 픽셀 아트로 지정합니다.
1. 모든 요청에 fruitfly-lab-expressions 저장소의 참고 그림을 함께 올립니다: images/_sheets/lab6_lineup.png(박사·하루·초파리·주판봇·시아·모아), images/_sheets/spares_sheet.png(X1~X3). 하루봇은 **하루가 모니터에 나오는 일체형 PC**입니다(다리·팔 없음). 하루봇이 나오는 모든 요청에 images/haru/E01_joy.png(모니터 속 하루 얼굴 기준)도 올립니다. v1의 말풍선 로봇 디자인은 쓰지 않습니다.
2. **00 하루봇 설정 그림을 먼저** 받아 확정합니다. 이후 모든 요청에 이 그림을 참고 이미지로 함께 올립니다.
3. 그다음 01 표지 → 02~14 장별 썸네일 순서로 요청합니다. 한 대화에 3~5장씩, 같은 비율끼리 묶습니다.
4. 받은 그림은 아래 저장 이름으로 돌려주세요. 페이지 반영 때 표지 1600×900, 썸네일 960×540 WebP로 줄입니다(합계 600KB 이하).

## 한눈에 보기

| 번호 | 저장 이름 | 장면 | 등장 |
|---|---|---|---|
| 00 | harubot_sheet.png | 하루봇 설정 그림 — 하루가 모니터에 나오는 일체형 PC(앞·옆, 받침대의 빈 부품 자리 13곳) | 하루봇 |
| 01 | cover.png | 완성된 하루봇 앞에 아홉 명이 모두 모인 장면 | 전원 |
| 02 | thumb_ch01.png | 1장: 단서를 읽는 돋보기 센서를 끼움 (자리 1) | 초파리 연구원 |
| 03 | thumb_ch02.png | 2장: 저울을 끼움 (자리 2) | 모아 |
| 04 | thumb_ch03.png | 3장: 모래시계 모양 예산 배터리를 끼움 (자리 3) | 시아 |
| 05 | thumb_ch04.png | 4장: 나침반·경로 칩을 끼움 (자리 4) | X1 |
| 06 | thumb_ch05.png | 5장: 두 갈래 협업 플러그를 끼움 (자리 5) | 주판봇 |
| 07 | thumb_ch06.png | 6장: 말판 모양 회로 기판을 끼움 (자리 6) | X2 |
| 08 | thumb_ch07.png | 7장: 점점 작아지는 동전탑을 끼움 (자리 7) | X3 |
| 09 | thumb_ch08.png | 8장: 계기판 게이지를 끼움 (자리 8) | 시아 · 모아 |
| 10 | thumb_ch09.png | 9장: 별점 버튼판을 끼움 (자리 9) | X1 · X2 · X3 |
| 11 | thumb_ch10.png | 10장: 마주 보는 거울 코일을 끼움 (자리 10) | 초파리 연구원 |
| 12 | thumb_ch11.png | 11장: 말투 다이얼 스피커를 끼움 (자리 11) | 조수(하루) |
| 13 | thumb_ch12.png | 12장: 점수 스티커 카드 슬롯을 끼움 (자리 12) | 조수(하루) |
| 14 | thumb_ch13.png | 13장: 심사용 외눈 렌즈를 끼움 (자리 13) | 박사 |

## 00 하루봇 설정 그림

```
Character reference sheet, 16:9, white background.
Design an original character: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot.
Show a front view and a three-quarter side view. All thirteen base slots are EMPTY (dashed outlines). Haru on the screen smiles (same face as the attached Haru E01_joy expression).
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, same pixel density as the attached lab character lineup; the PC is about as tall as the scientist character.
Plain flat light gray background. No anime illustration style, no smooth gradients. No text, no letters, no numbers, no logos.
```

## 01 표지

```
Website top cover illustration, wide 16:9, width 1920px or more.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Center: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot, now COMPLETE: every base slot holds its part (magnifier, scale, hourglass, compass, plug, circuit board, coin stack, gauge, star buttons, mirror coil, speaker, sticker card, monocle).
Around it, all nine characters celebrate together: the chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie); the girl assistant Haru (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans); the anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings); the boxy beige retro CRT-monitor robot AbaBot (dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads); Sia the maid intern (long straight jet-black hair, calm gray eyes, charcoal-black maid dress, long white frilled apron, large gray bow, no headdress); Moa the maid intern (long ash-beige wavy hair, white frilled maid headband, amber-brown eyes, camel cardigan, red and navy plaid bow tie, white apron); unrevealed extra X1 (cute solid silhouette filled with flat very dark navy-black #1B1A2E, thin dithered purple rim light, two round white dot eyes, pink blush pixels, pink hair bow, ponytail); unrevealed extra X2 (cute solid navy-black silhouette with purple rim light, white dot eyes, teal round glasses, beret); unrevealed extra X3 (cute solid navy-black silhouette with purple rim light, white dot eyes, cat-ear hood with two small gold pompoms).
The fruit fly is on the left facing right, AbaBot on the right facing left, the scientist at the back center.
Keep faces and hands inside the central safe area (12% margin left and right, 10% top, 18% bottom); keep the bottom-left corner plain and simple.
Mood: proud, cheerful, the moment the robot is finished.
```

대체 글: 완성된 하루봇 앞에 연구실 식구 아홉 명이 모여 기뻐하는 장면.

## 02 1장 썸네일 — 단서를 읽는 돋보기 센서 (초파리 연구원)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. All slots are still empty; the remaining slots are empty with dashed outlines.
the anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings) is carefully inserting a magnifying-glass sensor into slot 1 counting from the left in the top row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 초파리 연구원이(가) 하루봇의 1번째 자리에 단서를 읽는 돋보기 센서를 끼우는 장면.

## 03 2장 썸네일 — 저울 (모아)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 1 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor); the remaining slots are empty with dashed outlines.
Moa the maid intern (long ash-beige wavy hair, white frilled maid headband, amber-brown eyes, camel cardigan, red and navy plaid bow tie, white apron) is carefully inserting a small balance scale into slot 2 counting from the left in the top row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 모아이(가) 하루봇의 2번째 자리에 저울을 끼우는 장면.

## 04 3장 썸네일 — 모래시계 모양 예산 배터리 (시아)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 2 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale); the remaining slots are empty with dashed outlines.
Sia the maid intern (long straight jet-black hair, calm gray eyes, charcoal-black maid dress, long white frilled apron, large gray bow, no headdress) is carefully inserting an hourglass-shaped battery into slot 3 counting from the left in the top row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 시아이(가) 하루봇의 3번째 자리에 모래시계 모양 예산 배터리를 끼우는 장면.

## 05 4장 썸네일 — 나침반·경로 칩 (X1)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 3 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery); the remaining slots are empty with dashed outlines.
unrevealed extra X1 (cute solid silhouette filled with flat very dark navy-black #1B1A2E, thin dithered purple rim light, two round white dot eyes, pink blush pixels, pink hair bow, ponytail) is carefully inserting a compass chip with a route line into slot 4 counting from the left in the top row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: X1이(가) 하루봇의 4번째 자리에 나침반·경로 칩을 끼우는 장면.

## 06 5장 썸네일 — 두 갈래 협업 플러그 (주판봇)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 4 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line); the remaining slots are empty with dashed outlines.
the boxy beige retro CRT-monitor robot AbaBot (dark green screen face with mint pixel eyes, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads) is carefully inserting a two-pronged connector plug into slot 5 counting from the left in the top row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 주판봇이(가) 하루봇의 5번째 자리에 두 갈래 협업 플러그를 끼우는 장면.

## 07 6장 썸네일 — 말판 모양 회로 기판 (X2)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 5 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug); the remaining slots are empty with dashed outlines.
unrevealed extra X2 (cute solid navy-black silhouette with purple rim light, white dot eyes, teal round glasses, beret) is carefully inserting a game-board-like circuit board into slot 1 counting from the left in the middle row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: X2이(가) 하루봇의 6번째 자리에 말판 모양 회로 기판을 끼우는 장면.

## 08 7장 썸네일 — 점점 작아지는 동전탑 (X3)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 6 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board); the remaining slots are empty with dashed outlines.
unrevealed extra X3 (cute solid navy-black silhouette with purple rim light, white dot eyes, cat-ear hood with two small gold pompoms) is carefully inserting a stack of coins that get smaller toward the top into slot 2 counting from the left in the middle row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: X3이(가) 하루봇의 7번째 자리에 점점 작아지는 동전탑을 끼우는 장면.

## 09 8장 썸네일 — 계기판 게이지 (시아 · 모아)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 7 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board, slot 7: a stack of coins that get smaller toward the top); the remaining slots are empty with dashed outlines.
Sia the maid intern (long straight jet-black hair, calm gray eyes, charcoal-black maid dress, long white frilled apron, large gray bow, no headdress); Moa the maid intern (long ash-beige wavy hair, white frilled maid headband, amber-brown eyes, camel cardigan, red and navy plaid bow tie, white apron) are carefully inserting a dashboard gauge with a needle into slot 3 counting from the left in the middle row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 시아 · 모아이(가) 하루봇의 8번째 자리에 계기판 게이지를 끼우는 장면.

## 10 9장 썸네일 — 별점 버튼판 (X1 · X2 · X3)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 8 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board, slot 7: a stack of coins that get smaller toward the top, slot 8: a dashboard gauge with a needle); the remaining slots are empty with dashed outlines.
unrevealed extra X1 (cute solid silhouette filled with flat very dark navy-black #1B1A2E, thin dithered purple rim light, two round white dot eyes, pink blush pixels, pink hair bow, ponytail); unrevealed extra X2 (cute solid navy-black silhouette with purple rim light, white dot eyes, teal round glasses, beret); unrevealed extra X3 (cute solid navy-black silhouette with purple rim light, white dot eyes, cat-ear hood with two small gold pompoms) are carefully inserting a panel of star-shaped buttons into slot 4 counting from the left in the middle row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: X1 · X2 · X3이(가) 하루봇의 9번째 자리에 별점 버튼판을 끼우는 장면.

## 11 10장 썸네일 — 마주 보는 거울 코일 (초파리 연구원)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 9 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board, slot 7: a stack of coins that get smaller toward the top, slot 8: a dashboard gauge with a needle, slot 9: a panel of star-shaped buttons); the remaining slots are empty with dashed outlines.
the anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings) is carefully inserting a coil made of two facing mirrors into slot 1 counting from the left in the bottom row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 초파리 연구원이(가) 하루봇의 10번째 자리에 마주 보는 거울 코일을 끼우는 장면.

## 12 11장 썸네일 — 말투 다이얼 스피커 (조수(하루))

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 10 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board, slot 7: a stack of coins that get smaller toward the top, slot 8: a dashboard gauge with a needle, slot 9: a panel of star-shaped buttons, slot 10: a coil made of two facing mirrors); the remaining slots are empty with dashed outlines.
the girl assistant Haru (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans) is carefully inserting a speaker with a dial into slot 2 counting from the left in the bottom row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 조수(하루)이(가) 하루봇의 11번째 자리에 말투 다이얼 스피커를 끼우는 장면.

## 13 12장 썸네일 — 점수 스티커 카드 슬롯 (조수(하루))

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 11 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board, slot 7: a stack of coins that get smaller toward the top, slot 8: a dashboard gauge with a needle, slot 9: a panel of star-shaped buttons, slot 10: a coil made of two facing mirrors, slot 11: a speaker with a dial); the remaining slots are empty with dashed outlines.
the girl assistant Haru (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans) is carefully inserting a card slot holding score stickers (a checkmark sticker, no numbers) into slot 3 counting from the left in the bottom row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 조수(하루)이(가) 하루봇의 12번째 자리에 점수 스티커 카드 슬롯을 끼우는 장면.

## 14 13장 썸네일 — 심사용 외눈 렌즈 (박사)

```
Chapter thumbnail, 16:9.
Detailed 16-bit SNES-era pixel art, limited palette, crisp pixels, dithering shading, thick dark outlines, cheerful comedy mood. Match the pixel art style, proportions, head size and colors of the attached reference images exactly (same characters, identical design). Bright daytime pixel-art laboratory, white walls, daylight from windows, light teal and orange accents. No anime illustration style, no soft painting, no smooth gradients. No text, no letters, no numbers, no logos, no watermark.
Scene: HaruBot, an all-in-one desktop PC: a wide cream-white monitor with a thick orange bezel on a short neck stand; the screen shows the pixel-art girl Haru (long pink hair in two round buns with a navy streak, blue eyes, white lab coat over a lavender hoodie) as a bust-up portrait, the same character and design as the attached Haru reference; the stand's base is a wide low cream box with thirteen square part slots on its front, arranged in three rows (5 on top, 4 in the middle, 4 at the bottom); a small pink power light on the bezel; no legs, no arms, it is a computer, not a walking robot sits on a lab desk, center-right. Slots 1 to 12 already hold exactly these parts, each as a small pixel icon (slot 1: a magnifying-glass sensor, slot 2: a small balance scale, slot 3: an hourglass-shaped battery, slot 4: a compass chip with a route line, slot 5: a two-pronged connector plug, slot 6: a game-board-like circuit board, slot 7: a stack of coins that get smaller toward the top, slot 8: a dashboard gauge with a needle, slot 9: a panel of star-shaped buttons, slot 10: a coil made of two facing mirrors, slot 11: a speaker with a dial, slot 12: a card slot holding score stickers (a checkmark sticker, no numbers)); the remaining slots are empty with dashed outlines.
the chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie) is carefully inserting a judge's monocle lens into slot 4 counting from the left in the bottom row, which glows softly.
Haru on the HaruBot screen looks happy and curious. Faces and hands stay inside the central safe area; bottom-left corner plain.
```

대체 글: 박사이(가) 하루봇의 13번째 자리에 심사용 외눈 렌즈를 끼우는 장면.

## 고칠 때(같은 대화에서)

```
Same characters, same art style and composition. Change only: {고칠 점}. Still no text.
```