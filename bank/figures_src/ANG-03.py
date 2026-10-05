import sys; sys.path.insert(0, '.')
import math
from svgfig import *

# Interior angles: A = 52 (2x+4), C = 72 (3x), B = 56; exterior angle at B = 124. x = 24.
f = Fig()
A, B = f.pt(0, 0), f.pt(12, 0)
AC = 12 * math.sin(math.radians(56)) / math.sin(math.radians(72))
C = f.pt(*polar(AC, 52))
D = f.pt(17, 0)
f.poly([A, B, C]); f.seg(B, D)
f.angle_mark(A, B, C, var("(2x+4)°"), r=40)
f.angle_mark(C, A, B, var("(3x)°"), r=34)
f.angle_mark(B, C, D, "124°", r=34)
f.point(A, "A", (-1, -0.5), dot=False); f.point(B, "B", (0, -1), dot=False)
f.point(C, "C", (0, 1), dot=False); f.point(D, "D", (0.4, -1), dot=False)
f.save("figures/ANG-03.svg", png="figures/ANG-03.png")
