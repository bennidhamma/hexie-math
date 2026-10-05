import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Dot plot: number of books read. Each dot is one student (15 students).
counts = {1: 2, 2: 4, 3: 2, 4: 3, 5: 1, 6: 1, 7: 0, 8: 2}
f = PFig(width=900, height=520, margin=60)
f.pt(-0.6, -2.2); f.pt(9.6, 4.4)
f.seg((-0.4, 0), (9.4, 0))
for x in range(0, 10):
    f.seg((x, -0.18), (x, 0.18), width=2)
    f.text((x, -0.75), str(x), size=30)
for x, n in counts.items():
    for i in range(n):
        f.dot((x, 0.62 + 0.78 * i), 15)
f.text((4.5, -1.8), "Number of books", size=32)
f.save("figures/STAT-03.svg", png="figures/STAT-03.png")
