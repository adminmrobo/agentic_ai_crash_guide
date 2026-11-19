# AI 에이전트 공식 속성 가이드 — 하루봇을 만들며 배우는 13장

조수 하루를 닮은 AI 에이전트 챗봇 '하루봇'을 만들며, 에이전트의 수학 공식 13개를 한 장씩 익히는 비전공자용 속성 가이드입니다.

- 페이지: https://adminmrobo.github.io/agentic_ai_crash_guide/
- 원자료: ML Tut 「Agentic AI Math Formulas」 인포그래픽(12개 공식) — 이 페이지에서 바로잡고 벨만 방정식을 더해 13장으로 다시 썼습니다.

## 파일
- index.html — 완성 페이지(단일 파일, 지식 색인·꾸러미 포함)
- IMG_PROMPTS.md — 그림 15장 프롬프트 v2(16비트 SNES 픽셀 아트, 정본 캐릭터 참고 그림 지정)
- assets/img/ — 페이지용 그림(표지 1600×900, 썸네일 720×405 WebP, 공유 미리보기 og_cover.webp)과 하루봇 설정 그림 원본(harubot_sheet.png)
- assets/avatar/ — 대화칸 캐릭터 얼굴(fruitfly-lab-expressions 정본 픽셀 표정에서 잘라 128px로 줄임)
- src/ — 문구 데이터(data_ko.py), 빌드(build.py), 실험 엔진(engine.js), 스타일, 검산(verify.py, duel.py)
- kg/ — kg.json · refs.json · meta.json · check_report.md · retrofit_log.md

## 고치는 법
src/data_ko.py에서 문구를 고친 뒤 python3 build.py (그림은 assets/img/에서 읽어 페이지에 넣음) → ai-lab-retrofit의 retrofit.py로 꼬리표를 다시 답니다.

글 · 안상선 (https://adminmrobo.github.io/who_am_i/who_am_i.html) · (주)M-Robo 대표
