import sys, os, math; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from svgfig import *

f = Fig(width=760, height=700, margin=90)
A, B, C, D = f.pt(0, 8), f.pt(8, 8), f.pt(8, 0), f.pt(0, 0)
O, P = (4, 4), (6, 2)
r = math.dist(O, P)
f.fill_circle(O, r, fill=GRAY)
f.circle(O, r)
f.poly([A, B, C, D])
f.right_angle(D, C, A)
f.seg(A, C, dashed=True)
f.ticks(O, P); f.ticks(P, C)
f.dot(O, 5.5); f.dot(P, 5.5)
f.label_point(O, "O", (1, 1)); f.label_point(P, "P", (-1, -0.15), gap=26)
for p, s, d in [(A, "A", (-1, 1)), (B, "B", (1, 1)), (C, "C", (1, -1)), (D, "D", (-1, -1))]:
    f.label_point(p, s, d)
f.label_seg(D, C, "8 cm", side=-1)
f.save("figures/PROB-10.svg", png="figures/PROB-10.png")
