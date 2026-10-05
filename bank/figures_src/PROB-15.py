import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from svgfig import *

f = Fig(width=700, height=640, margin=50)
O = f.pt(0, 0); R = 10
f.circle(O, R)
r0, r1, r2 = polar(R, 0), polar(R, 120), polar(R, 210)
for q in (r0, r1, r2):
    f.seg(O, q)
f.dot(O, 4)
f.angle_arc(O, r0, r1, r=30, label="120°")
f.right_angle(O, r1, r2, size=20)
f.text(polar(6.4, 60), "Red", size=34)
f.text(polar(6.2, 165), "Blue", size=34)
f.text(polar(6.0, 285), "Green", size=34)
f.save("figures/PROB-15.svg", png="figures/PROB-15.png")
