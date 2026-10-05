import sys; sys.path.insert(0, '.')
import math
from svgfig import *

# AB = AC, base angles 65, apex 50. Angle BAD = 20, so angle ADB = 95 and angle ADC = 85.
f = Fig()
B, C = f.pt(0, 0), f.pt(10, 0)
A = f.pt(5, 5 * math.tan(math.radians(65)))
AB = length(sub(A, B))
BD = AB * math.sin(math.radians(20)) / math.sin(math.radians(95))
D = f.pt(BD, 0)
f.poly([A, B, C]); f.seg(A, D)
f.ticks(A, B); f.ticks(A, C)
f.angle_mark(A, B, D, "20°", r=285)
f.angle_mark(D, A, C, "85°", r=32)
f.point(A, "A", (0, 1), dot=False); f.point(B, "B", (-1, -0.5), dot=False)
f.point(C, "C", (1, -0.5), dot=False); f.point(D, "D", (0, -1), dot=False)
f.save("figures/ANG-04.svg", png="figures/ANG-04.png")
