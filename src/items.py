# -*- coding: utf-8 -*-
"""하루봇 RPG 아이템 — 장마다 하나씩 장착한다.
스프라이트는 12×12 픽셀 그림(연구실 픽셀아트 방침). 문자 하나 = 픽셀 하나, '.'은 투명."""

PAL = {
    "k": "#2b2118",  # 외곽선
    "o": "#ea580c", "O": "#fb923c",  # 주황
    "y": "#f5b301", "Y": "#fde68a",  # 금색
    "w": "#ffffff", "c": "#7dd3fc", "b": "#2563eb", "B": "#1e3a8a",
    "g": "#94a3b8", "d": "#475569", "r": "#dc2626", "p": "#ec4899", "P": "#f9a8d4",
    "n": "#92400e", "N": "#d97706", "G": "#16a34a", "L": "#86efac", "t": "#0f766e", "v": "#7c3aed",
}

# 장 번호 → (키, 아이템 이름, 탑재 기능('~기능이 탑재됐습니다'), 가능해진 일('이제 ~ 가능합니다'), 스프라이트)
ITEMS = {
1: ("magnifier", "단서 돋보기", "말뜻 짐작(베이즈) 기능",
    "단서로 사용자의 속뜻을 확률로 짐작하기가", [
    "...kkkk.....",
    "..kyyyyk....",
    ".kycwccyk...",
    ".kywccccyk..",
    ".kycccccyk..",
    ".kycccccyk..",
    "..kyccccyk..",
    "...kyyyyk...",
    "....kkkkNn..",
    "........kNn.",
    ".........kNn",
    "..........kk"]),
2: ("scale", "판단의 저울", "기대효용 계산 기능",
    "바로 답할지 되물을지 손익 따지기가", [
    ".....yy.....",
    "kkkkkyykkkkk",
    "kYk..yy..kYk",
    "kYk..yy..kYk",
    "kYk..yy..kYk",
    "kyyk.yy.kyyk",
    "kkkk.yy.kkkk",
    ".....yy.....",
    ".....yy.....",
    "....kyyk....",
    "..kkyyyykk..",
    "..kkkkkkkk.."]),
3: ("hourglass", "모래시계 배터리", "시간 예산 관리 기능",
    "10초 예산 안에서 가장 좋은 계획 고르기가", [
    "kkkkkkkkkkkk",
    "knnnnnnnnnnk",
    ".kcYYYYYYck.",
    "..kcYYYYck..",
    "...kcYYck...",
    "....kcck....",
    "....kcck....",
    "...kccYck...",
    "..kccYYYck..",
    ".kcYYYYYYck.",
    "knnnnnnnnnnk",
    "kkkkkkkkkkkk"]),
4: ("compass", "길찾기 나침반", "A* 경로 탐색 기능",
    "할 일을 가장 빨리 끝내는 순서 찾기가", [
    "...kkkkkk...",
    "..kyyyyyyk..",
    ".kywwwrwwyk.",
    "kywwwrrwwwyk",
    "kywwwrrwwwyk",
    "kywwwkkwwwyk",
    "kywwwbbwwwyk",
    "kywwwbbwwwyk",
    ".kywwbwwwyk.",
    "..kyyyyyyk..",
    "...kkkkkk...",
    "............"]),
5: ("plug", "협업 플러그", "역할 나누기(내시 균형) 기능",
    "주판봇과 서로 손해 없는 일 나누기가", [
    "..kk....kk..",
    "..kg....kg..",
    "..kg....kg..",
    ".kkkkkkkkkk.",
    ".kGGGGGGGGk.",
    ".kGLLGGGGGk.",
    ".kGGGGGGGGk.",
    "..kGGGGGGk..",
    "...kkddkk...",
    ".....dd.....",
    ".....dd.....",
    "....kkkk...."]),
6: ("board", "말판 회로 기판", "상태 전이 지도 기능",
    "대화가 다음에 어디로 갈지 확률로 내다보기가", [
    "kkkkkkkkkkkk",
    "kGGGGGGGGGGk",
    "kGyykGGkyyGk",
    "kGyykGGkyyGk",
    "kGkkGGGGkkGk",
    "kGGGGpGGGGGk",
    "kGGGGGpGGGGk",
    "kGkkGGGGkkGk",
    "kGyykGGkyyGk",
    "kGyykGGkyyGk",
    "kGGGGGGGGGGk",
    "kkkkkkkkkkkk"]),
7: ("coins", "줄어드는 동전탑", "미래 보상 할인 기능",
    "먼 훗날의 점수를 지금 값으로 바꿔 세기가", [
    "............",
    ".....kk.....",
    "....kYyk....",
    "....kkkk....",
    "...kYyyyk...",
    "...kkkkkk...",
    "..kYyyyyyk..",
    "..kkkkkkkk..",
    ".kYyyyyyyyk.",
    ".kNNNNNNNNk.",
    "kYyyyyyyyyyk",
    "kkkkkkkkkkkk"]),
8: ("gauge", "가치 계기판", "상태가치(V) 측정 기능",
    "지금 대화가 몇 점짜리인지 재기가", [
    "............",
    "...kkkkkk...",
    "..kwwwwwwk..",
    ".kwGwwwwrwk.",
    "kwGwwwwwwrwk",
    "kwwwwwwkwwwk",
    "kwwwwwkwwwwk",
    "kwwwwkkwwwwk",
    "kwwwwkkwwwwk",
    "kddddddddddk",
    "kkkkkkkkkkkk",
    "............"]),
9: ("stars", "별점 버튼판", "행동가치(Q) 채점 기능",
    "상황마다 답의 점수 매기기가", [
    ".....kk.....",
    ".....ky.....",
    "....kyyk....",
    "kkkkkyykkkkk",
    "kYyyyyyyyyyk",
    ".kYyyyyyyyk.",
    "..kyyyyyyk..",
    "..kyyyyyyk..",
    ".kyyykkyyyk.",
    ".kyyk..kyyk.",
    "kyyk....kyyk",
    "kkk......kkk"]),
10: ("mirror", "되비춤 거울 코일", "벨만 되풀이 계산 기능",
    "다음 걸음의 값으로 지금 값 고쳐 세기가", [
    "kk........kk",
    "kck......kck",
    "kwck....kcwk",
    "kcck.vv.kcck",
    "kcckvvvvkcck",
    "kwck....kcwk",
    "kcck....kcck",
    "kcckvvvvkcck",
    "kwck.vv.kcck",
    "kcck....kcwk",
    "kck......kck",
    "kk........kk"]),
11: ("speaker", "말투 다이얼 스피커", "말투 고르기(소프트맥스) 기능",
    "점수에 따라 말투를 확률로 골라 말하기가", [
    "......k.....",
    ".....kk..k..",
    "....kgk...k.",
    "kkkkggk.k..k",
    "kggggg..k..k",
    "kgdddg...k.k",
    "kgdddg...k.k",
    "kggggg..k..k",
    "kkkkggk.k..k",
    "....kgk...k.",
    ".....kk..k..",
    "......k....."]),
12: ("sticker", "점수 스티커 카드", "정책 경사 학습 기능",
    "하루가 준 점수로 말투를 스스로 고치기가", [
    "kkkkkkkkkk..",
    "kwwwwwwwwk..",
    "kwppwwppwk..",
    "kwpppppwwk..",
    "kwwpppwwwk..",
    "kwwwpwwwwk..",
    "kwwwwwwwGkk.",
    "kwggggwGGk..",
    "kwwwwwGGwk..",
    "kwgggGGwwk..",
    "kwwwwGwwwk..",
    "kkkkkkkkkk.."]),
13: ("monocle", "평가자의 외눈 렌즈", "행동자·평가자 학습 기능",
    "박사의 평가를 받으며 훨씬 빨리 배우기가", [
    "....kkkk....",
    "..kkddddkk..",
    ".kddcccwddk.",
    ".kdcccwccdk.",
    "kdcccwccccdk",
    "kdccbcccccdk",
    "kdcbccccccdk",
    ".kdbcccccdk.",
    ".kddccccddk.",
    "y.kkddddkk..",
    ".y..kkkk....",
    "..yy.y.y.y.y"]),
}


def sprite_rects(grid, x0=0.0, y0=0.0, px=1.0):
    """스프라이트를 SVG rect 문자열로. 같은 색이 가로로 이어지면 한 rect로 묶는다."""
    out = []
    for j, row in enumerate(grid):
        i = 0
        while i < len(row):
            ch = row[i]
            if ch == ".":
                i += 1; continue
            k = i
            while k < len(row) and row[k] == ch:
                k += 1
            out.append(f'<rect x="{x0+i*px:g}" y="{y0+j*px:g}" width="{(k-i)*px:g}" height="{px:g}" fill="{PAL[ch]}"/>')
            i = k
    return "".join(out)


def sprite_svg(n, cls="spr"):
    return (f'<svg class="{cls}" viewBox="0 0 12 12" shape-rendering="crispEdges" aria-hidden="true">'
            f'{sprite_rects(ITEMS[n][4])}</svg>')


for _n, _it in ITEMS.items():
    assert len(_it[4]) == 12 and all(len(r) == 12 for r in _it[4]), (_n, [len(r) for r in _it[4]])
    assert all(ch in PAL or ch == "." for r in _it[4] for ch in r), _n
