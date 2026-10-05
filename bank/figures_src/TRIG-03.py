import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Right triangle: right angle at C, angle A = 32 degrees, AC = 15. BC = 15 tan 32 (not labeled).
f = Fig(width=900, height=620, margin=90)
A, C = f.pt(0, 0), f.pt(15, 0)
B = f.pt(15, 15 * math.tan(math.radians(32)))
f.poly([A, C, B])
f.right_angle(C, A, B, size=20)
f.angle_mark(A, C, B, "32°", r=60)
f.label_seg(A, C, "15", side=-1)
f.label_point(A, "A", (-1, -0.4)); f.label_point(C, "C", (1, -0.4)); f.label_point(B, "B", (0.4, 1))
f.save("figures/TRIG-03.svg", png="figures/TRIG-03.png")
