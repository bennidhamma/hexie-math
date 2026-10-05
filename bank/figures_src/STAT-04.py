import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Scatterplot of hours studied vs. test score, with the line of best fit y = 4x + 55
# through (0, 55) and (10, 95). The point (7, 70) is the student in the question.
f = PFig(width=860, height=860, margin=110, equal=False)
f.plot(0, 10, 50, 100, gx=1, gy=5, xnums=range(0, 11), ynums=range(50, 101, 10),
       yticks=range(50, 101, 5), ext=0.5, exty=3, label_mode=None, origin=None, num_size=26)
f.margin = 110
pts = [(1, 62), (2, 60), (2, 66), (3, 70), (4, 68), (4, 74), (5, 78), (6, 76), (6, 82),
       (7, 70), (8, 90), (9, 88), (9, 94), (10, 92)]
f.seg((0, 55), (10, 95))
for p in pts:
    f.dot(p, 7)
f.raw_text((0, 50), "50", size=26, anchor="end", dx=-12)
f.raw_text((0, 50), "0", size=26, dy=21)
f.raw_text((5, 50), "Hours studied", size=30, dy=68, halo=False)
f.raw_text((0, 75), "Test score (points)", size=30, dx=-80, rotate=-90, halo=False)
f.save("figures/STAT-04.svg", png="figures/STAT-04.png")
