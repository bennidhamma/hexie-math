import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Line k through (-2, -3) and (4, 1): y = 2/3 x - 5/3. Point P = (2, 5).
X0, X1, Y0, Y1 = -5, 6, -5, 6
f = PFig(width=880, height=880, margin=50)
f.plot(X0, X1, Y0, Y1, gx=1, gy=1, xnums=range(X0, X1 + 1), ynums=range(Y0, Y1 + 1), ext=0.6, yright={-2}, xshift={2: -26})
k = lambda x: (2 * x - 5) / 3
xa, xb = -5, 6
f.seg((xa, k(xa)), (xb, k(xb)))
f.curve_arrow(k, xa, xa + 0.05); f.curve_arrow(k, xb, xb - 0.05)
for p in [(-2, -3), (4, 1)]:
    f.dot(p, 6)
f.dot((2, 5), 6)
f.raw_text((2, 5), "P", italic=True, dx=-24, dy=-22)
f.raw_text((5, k(5)), "k", italic=True, dx=-8, dy=-30)
f.save("figures/COORD-02.svg", png="figures/COORD-02.png")
