# AI 에이전트 공식 속성 가이드 — 하루봇을 만들며 배우는 13장

조수 하루를 닮은 AI 에이전트 챗봇 '하루봇'을 만들며, 에이전트의 수학 공식 13개를 한 장씩 익히는 비전공자용 속성 가이드입니다.

- 페이지: https://adminmrobo.github.io/agentic_ai_crash_guide/
- 원자료: ML Tut 「Agentic AI Math Formulas」 인포그래픽(12개 공식) — 이 페이지에서 바로잡고 벨만 방정식을 더해 13장으로 다시 썼습니다.

## 파일
- index.html — 완성 페이지(단일 파일, 지식 색인·꾸러미 포함)
- IMG_PROMPTS.md — 일러스트 픽셀 그림이 필요할 때 쓰는 프롬프트 v4(16비트 SNES 픽셀 아트, 모니터만 있는 하루봇, RPG 아이템 장착)
- assets/img/og_cover.webp — 공유 미리보기(코드로 그린 픽셀 하루봇). v1 일반 일러스트 그림은 픽셀 방침 위반으로 삭제(2026-11-21)
- assets/avatar/ — 대화칸 캐릭터 얼굴(fruitfly-lab-expressions 정본 픽셀 표정에서 잘라 128px로 줄임)
- src/ — 문구 데이터(data_ko.py), 아이템 데이터·픽셀 스프라이트(items.py), 빌드(build.py), 실험 엔진(engine.js), 아이템 장착 엔진(items.js), 스타일, 검산(verify.py, duel.py)

## 하루봇과 아이템
- 하루봇은 본체 없이 하루의 표정이 나오는 큰 모니터 하나입니다. 아이템 13자리는 모니터 아래의 RPG 아이템 창입니다. 모니터 속 얼굴은 fruitfly-lab-expressions 정본 픽셀 표정을 씁니다.
- 장마다 RPG 아이템 1개(12×12 픽셀 스프라이트)를 줍니다. 퀴즈를 맞히거나 '장착하기'를 누르면 장착됩니다.
- 장착하면 「○○ 기능이 탑재됐습니다! 이제 ○○ 가능합니다」 메시지, LEVEL UP 표시, 8비트 효과음(Web Audio, 파일 없음)이 나옵니다. 13개를 모두 장착하면 Lv.MAX 완성 팡파르.
- 장착 상태와 효과음 켬/끔은 읽는 사람의 브라우저에만 저장됩니다.
- kg/ — kg.json · refs.json · meta.json · check_report.md · retrofit_log.md

## 고치는 법
src/data_ko.py·items.py에서 문구를 고친 뒤 `python3 build.py` → ai-lab-retrofit의 `retrofit.py dist/index.html --kg ../kg/kg.json --refs ../kg/refs.json --meta ../kg/meta.json -o ../index.html` → `python3 postfix.py ../index.html`(금지 표현 점검)

글 · 안상선 (https://adminmrobo.github.io/who_am_i/who_am_i.html) · (주)M-Robo 대표
