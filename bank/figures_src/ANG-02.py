import sys; sys.path.insert(0, '.')
import math
from svgfig import *

# Angle BAC = 56 (exterior 124 at A), angle at C to B = 38, so angle ACB = 86 = x.
f = Fig()
h = 5
A = (0, h)
C = (h / math.tan(math.radians(56)), 0)
B = (C[0] + h / math.tan(math.radians(38)), h)
x0, x1 = -5, 15
p0, p1 = f.pt(x0, h), f.pt(x1, h)
q0, q1 = f.pt(x0, 0), f.pt(x1, 0)
f.seg(p0, p1); f.seg(q0, q1)
f.arrow_mark(p0, p1, at=0.08); f.arrow_mark(q0, q1, at=0.08)
f.label_point(p1, "p", (1, 0)); f.label_point(q1, "q", (1, 0))
uAC = unit(sub(C, A)); uBC = unit(sub(C, B))
f.seg(sub(A, mul(uAC, 1.6)), add(C, mul(uAC, 3.0)))
f.seg(sub(B, mul(uBC, 1.6)), add(C, mul(uBC, 3.0)))
f.angle_mark(A, p0, C, "124°", r=34)
f.angle_mark(C, q1, B, "38°", r=46)
f.angle_mark(C, add(C, uAC), add(C, uBC), var("x°"), r=34)
f.label_point(A, "A", (0.6, 1)); f.label_point(B, "B", (-0.6, 1)); f.text_px(C, "C", dx=-58, dy=30, italic=True)
f.save("figures/ANG-02.svg", png="figures/ANG-02.png")
