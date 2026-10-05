import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Observers A and B on a straight shoreline, AB = 600 m. Angle A = 48, angle B = 64; boat at C.
f = Fig(width=900, height=640, margin=80)
A, B = f.pt(0, 0), f.pt(600, 0)
AC = 600 * math.sin(math.radians(64)) / math.sin(math.radians(68))
C = f.pt(*polar(AC, 48))
f.seg(f.pt(-110, 0), f.pt(710, 0))          # shoreline
f.seg(A, C); f.seg(B, C)
f.dot(A, 5.5); f.dot(B, 5.5); f.dot(C, 5.5)
f.angle_mark(A, B, C, "48°", r=56)
f.angle_mark(B, C, A, "64°", r=46)
f.label_seg(A, B, "600", side=-1)
f.label_point(A, "A", (-0.5, -1)); f.label_point(B, "B", (0.5, -1)); f.label_point(C, "C", (0, 1))
f.save("figures/LAW-04.svg", png="figures/LAW-04.png")
