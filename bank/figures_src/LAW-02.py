import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# AB = 12, angle A = 40, angle B = 75, so angle C = 65 (not marked).
f = Fig(width=900, height=640, margin=90)
A, B = f.pt(0, 0), f.pt(12, 0)
AC = 12 * math.sin(math.radians(75)) / math.sin(math.radians(65))
C = f.pt(*polar(AC, 40))
f.poly([A, B, C])
f.angle_mark(A, B, C, "40°", r=56)
f.angle_mark(B, C, A, "75°", r=46)
f.label_seg(A, B, "12", side=-1)
f.label_point(A, "A", (-1, -0.4)); f.label_point(B, "B", (1, -0.4)); f.label_point(C, "C", (0, 1))
f.save("figures/LAW-02.svg", png="figures/LAW-02.png")
