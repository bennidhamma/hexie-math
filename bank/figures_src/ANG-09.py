import sys; sys.path.insert(0, '.')
from svgfig import *

# x = 20: angle AOB = angle COD = 100, so the line BD makes 80 degrees with AC (angle BOC = 80).
f = Fig()
O = f.pt(0, 0)
A, C = f.pt(-6, 0), f.pt(6, 0)
B, D = polar(5.2, 80), polar(5.2, 260)
f.seg(f.pt(-8, 0), f.pt(8, 0))
f.seg(f.pt(*polar(6.8, 260)), f.pt(*polar(6.8, 80)))
for p in (A, B, C, D, O):
    f.dot(p, 5.5)
f.angle_mark(O, A, B, var("(x+80)°"), r=44, at=0.25)
f.angle_mark(O, C, D, var("(3x+40)°"), r=44, at=0.22)
f.label_point(A, "A", (0, 1)); f.label_point(C, "C", (0, 1))
f.label_point(B, "B", (1, 0)); f.label_point(D, "D", (-1, 0))
f.text_px(O, "O", dx=-30, dy=-28, italic=True)
f.save("figures/ANG-09.svg", png="figures/ANG-09.png")
