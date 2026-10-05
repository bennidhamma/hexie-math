import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=900, height=760, margin=110, equal=False)
f.plot(0, 12, 0, 16, gx=2, gy=2, xnums=range(0, 13, 2), ynums=range(0, 17, 2), ext=0.7, exty=0.95,
       label_mode=None, num_size=26)
pts = [(0, 0), (2, 6), (6, 6), (10, 14), (12, 14)]
f.poly(pts, closed=False)
for p in pts:
    f.dot(p, 6.5)
f.raw_text((6, 0), "Time (hr)", size=30, dy=66, halo=False)
f.raw_text((0, 8), "Total distance (mi)", size=30, dx=-72, rotate=-90, halo=False)
f.save("figures/WORD-03.svg", png="figures/WORD-03.png")
