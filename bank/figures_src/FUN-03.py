import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=900, height=760, margin=50)
f.plot(-5, 5, -4, 4, gx=1, gy=1, xnums=range(-5, 6), ynums=range(-4, 5), ext=0.6)
pts = [(-4, -1), (-2, 3), (0, 1), (2, -3), (4, 1)]
f.poly(pts, closed=False)
for p in pts:
    f.dot(p, 6)
f.raw_text((3.5, 0.5), "f", italic=True, dx=-14, dy=-14)
f.save("figures/FUN-03.svg", png="figures/FUN-03.png")
