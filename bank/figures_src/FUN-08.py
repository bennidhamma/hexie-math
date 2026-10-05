import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=900, height=680, margin=50)
f.plot(-5, 6, -2, 5, gx=1, gy=1, xnums=range(-5, 7), ynums=range(-2, 6), ext=0.6)
def dashed(T, k):
    (x0, y), (x1, _) = T((-5, 2)), T((6, 2))
    return f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke-dasharray="10 8" stroke-width="2"/>'
f.under.insert(1, dashed)   # above the grid and axes, below the tick numbers
f.raw_text((5.1, 2.2), "y", italic=True, size=28, anchor="end", dx=-14, dy=-16)
f.raw_text((5.1, 2.2), "= 2", size=28, anchor="start", dx=-6, dy=-16)
p1 = [(-4, 0), (-3, 3), (-1, 2), (0, 4), (1, 2)]
p2 = [(1, -1), (3, 2), (5, -1)]
f.poly(p1, closed=False); f.poly(p2, closed=False)
for p in p1[:-1] + p2:
    f.dot(p, 6)
f.dot((1, 2), 8, open_=True)
f.raw_text((-2.7, 3.2), "f", italic=True, dx=4, dy=-12)
f.save("figures/FUN-08.svg", png="figures/FUN-08.png")
