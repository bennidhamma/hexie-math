import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Line y = -3/4 x + 3 through (0, 3) and (4, 0).
X0, X1, Y0, Y1 = -3, 6, -3, 5
f = PFig(width=840, height=820, margin=50)
f.plot(X0, X1, Y0, Y1, gx=1, gy=1, xnums=range(X0, X1 + 1), ynums=range(Y0, Y1 + 1), ext=0.6)
line = lambda x: -0.75 * x + 3
xa, xb = -8 / 3, 6          # where the line meets the grid edges (y = 5 and x = 6)
f.seg((xa, line(xa)), (xb, line(xb)))
f.curve_arrow(line, xa, xa + 0.05); f.curve_arrow(line, xb, xb - 0.05)
for p in [(0, 3), (4, 0)]:
    f.dot(p, 6)
f.save("figures/COORD-05.svg", png="figures/COORD-05.png")
