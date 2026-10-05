import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Line m: y = -x + 4 through (0, 4) and (4, 0). Line n: y = 2x - 1 through (0, -1) and (2, 3).
X0, X1, Y0, Y1 = -2, 6, -3, 6
f = PFig(width=820, height=860, margin=50)
f.plot(X0, X1, Y0, Y1, gx=1, gy=1, xnums=range(X0, X1 + 1), ynums=range(Y0, Y1 + 1), ext=0.6, yright={-2})
m_ = lambda x: -x + 4
n_ = lambda x: 2 * x - 1
f.seg((-2, m_(-2)), (6, m_(6)))
f.curve_arrow(m_, -2, -1.95); f.curve_arrow(m_, 6, 5.95)
f.seg((-1, n_(-1)), (3.5, n_(3.5)))
f.curve_arrow(n_, -1, -0.95); f.curve_arrow(n_, 3.5, 3.45)
for p in [(0, 4), (4, 0), (0, -1), (2, 3)]:
    f.dot(p, 6)
f.raw_text((-1.2, m_(-1.2)), "m", italic=True, dx=-26, dy=26)
f.raw_text((3.2, n_(3.2)), "n", italic=True, dx=26, dy=6)
f.save("figures/COORD-08.svg", png="figures/COORD-08.png")
