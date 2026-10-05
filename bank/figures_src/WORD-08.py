import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=820, height=900, margin=110, equal=False)
f.plot(0, 4, 0, 32, gx=1, gy=2, xnums=range(0, 5), ynums=range(0, 33, 2), ext=0.35, exty=1.8,
       label_mode=None, num_size=24)
f.margin = 110
A = [(0, 18), (2, 24), (4, 30)]
B = [(0, 6), (2, 16), (4, 26)]
f.poly(A, closed=False)
f.poly(B, closed=False, dashed=True)
for p in A:
    f.dot(p, 7)
for p in B:
    f.open_square(p, 7)
f.raw_text((4, 30), "Plan A", size=28, anchor="start", dx=40, halo=False)
f.raw_text((4, 26), "Plan B", size=28, anchor="start", dx=40, halo=False)
f.raw_text((2, 0), "Data (GB)", size=30, dy=66, halo=False)
f.raw_text((0, 16), "Monthly cost ($)", size=30, dx=-72, rotate=-90, halo=False)
f.save("figures/WORD-08.svg", png="figures/WORD-08.png")
