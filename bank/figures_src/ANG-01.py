import sys; sys.path.insert(0, '.')
import math
from svgfig import *

f = Fig()
t = 70  # transversal makes 70 degrees with the parallel lines: 3x+10 = 70, 5x+10 = 110
d = polar(1, t)
q0, q1 = f.pt(0, 0), f.pt(16, 0)
p0, p1 = f.pt(0, 5), f.pt(16, 5)
f.seg(q0, q1); f.seg(p0, p1)
f.arrow_mark(q0, q1, at=0.1); f.arrow_mark(p0, p1, at=0.1)
L = (6, 0); U = add(L, mul(d, 5 / d[1]))
f.seg(add(L, mul(d, -2.4)), add(U, mul(d, 2.4)))
f.label_point(p1, "p", (1, 0)); f.label_point(q1, "q", (1, 0))
f.angle_mark(U, p1, add(U, d), var("(3x+10)°"), r=36, at=0.3)
f.angle_mark(L, q0, add(L, d), var("(5x+10)°"), r=36)
f.save("figures/ANG-01.svg", png="figures/ANG-01.png")
