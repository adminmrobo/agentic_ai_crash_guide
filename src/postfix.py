# -*- coding: utf-8 -*-
"""retrofit.py 결과(kgx.js 포함)에서 금지 표현('사다리'·'관통'·'칸')을 바꾼다. 사용: python3 postfix.py ../index.html"""
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding="utf-8")
for a, b in [("사다리 경로", "선행 개념 경로"), ("사다리 사슬", "선행 개념 사슬"), ("// 사다리", "// 선행 개념"),
             ("빈칸으로", "빈 값으로"), ("loc 칸이", "loc 열이"), ("// 칸 수", "// 항목 수")]:
    s = s.replace(a, b)
bad = [w for w in ("칸", "사다리", "관통") if w in s]
p.write_text(s, encoding="utf-8")
print("postfix:", "남은 금지 표현 " + ", ".join(bad) if bad else "금지 표현 없음")
