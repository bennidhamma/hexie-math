import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# AB = 8, AC = 5, angle A = 60 degrees. BC = 7 (not labeled).
f = Fig(width=900, height=620, margin=90)
A, B = f.pt(0, 0), f.pt(8, 0)
C = f.pt(*polar(5, 60))
f.poly([A, B, C])
f.angle_mark(A, B, C, "60°", r=46)
f.label_seg(A, B, "8", side=-1)
f.label_seg(A, C, "5", side=1)
f.label_point(A, "A", (-1, -0.4)); f.label_point(B, "B", (1, -0.4)); f.label_point(C, "C", (0, 1))
f.save("figures/LAW-01.svg", png="figures/LAW-01.png")
