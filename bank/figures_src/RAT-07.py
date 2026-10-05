import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from svgfig import *

f = Fig(width=800, height=560, margin=90)
P = [f.pt(0, 0), f.pt(5, 0), f.pt(5, 3), f.pt(0, 3)]
f.poly(P)
f.pt(-1.0, 1.5); f.pt(6.0, 1.5)   # room for the side label
for i in range(4):
    f.right_angle(P[i], P[(i + 1) % 4], P[i - 1], size=18)
f.label_seg(P[3], P[2], "5 cm", side=1)      # above the top side
f.label_seg(P[1], P[2], "3 cm", side=-1)      # right of the right side
f.save("figures/RAT-07.svg", png="figures/RAT-07.png")
