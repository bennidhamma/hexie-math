import sys; sys.path.insert(0, '.')
import math
from svgfig import *

# AD = 6, DB = 4, AE = 9 (so EC = 6), DE = 12, BC = 20: triangle ABC has sides 10, 15, 20 to scale.
f = Fig()
B, C = f.pt(0, 0), f.pt(20, 0)
ax = (10**2 - 15**2 + 20**2) / 40
A = f.pt(ax, math.sqrt(10**2 - ax**2))
D = add(A, mul(sub(B, A), 0.6)); E = add(A, mul(sub(C, A), 0.6))
f.poly([A, B, C]); f.seg(D, E)
f.arrow_mark(D, E, at=0.5); f.arrow_mark(B, C, at=0.5)
f.label_seg(A, D, "6", side=-1); f.label_seg(D, B, "4", side=-1); f.label_seg(A, E, "9", side=1)
f.label_point(A, "A", (0, 1)); f.label_point(B, "B", (-1, -0.4)); f.label_point(C, "C", (1, -0.4))
f.label_point(D, "D", (-1, 0.15)); f.label_point(E, "E", (1, 0.3))
f.save("figures/ANG-06.svg", png="figures/ANG-06.png")
