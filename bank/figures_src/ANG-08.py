import sys; sys.path.insert(0, '.')
import math
from svgfig import *

# BC = 6 and angle CAB = 30, so AB = 6*sqrt(3): drawn to scale.
f = Fig()
w = 6 * math.sqrt(3)
A, B, C, D = f.pt(0, 0), f.pt(w, 0), f.pt(w, 6), f.pt(0, 6)
f.poly([A, B, C, D]); f.seg(A, C)
f.right_angle(B, A, C); f.right_angle(D, A, C)
f.angle_mark(A, B, C, "30°", r=60, at=0.45)
f.label_seg(B, C, "6", side=-1)
f.label_point(A, "A", (-1, -0.6)); f.label_point(B, "B", (1, -0.6))
f.label_point(C, "C", (1, 0.6)); f.label_point(D, "D", (-1, 0.6))
f.save("figures/ANG-08.svg", png="figures/ANG-08.png")
