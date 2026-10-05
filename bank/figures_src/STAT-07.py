import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Histogram of commute times: [0,10) 4, [10,20) 9, [20,30) 12, [30,40) 10, [40,50) 5 (total 40).
f = PFig(width=900, height=720, margin=40, equal=False)
f.view(-11, 55, -3.2, 15.2)
vals = [4, 9, 12, 10, 5]

def grid(T, k):
    o = []
    for y in range(2, 15, 2):
        (x0, py), (x1, _) = T((0, y)), T((52, y))
        o.append(f'<line x1="{x0:.1f}" y1="{py:.1f}" x2="{x1:.1f}" y2="{py:.1f}" stroke="#9a9a9a" stroke-width="1.2"/>')
    return "\n".join(o)
f.under.append(grid)

for i, v in enumerate(vals):
    box = [(10 * i, 0), (10 * i + 10, 0), (10 * i + 10, v), (10 * i, v)]
    f.fill(box, fill="#c8c8c8"); f.poly(box)
for x in range(0, 51, 10):
    f.seg((x, 0), (x, -0.25), width=1.6)
    f.text((x, -0.95), str(x), size=28)
for y in range(0, 15, 2):
    f.seg((-0.8, y), (0, y), width=1.6)
    f.text((-1.6, y), str(y), size=28, anchor="end")
f.seg((0, 0), (52, 0)); f.seg((0, 0), (0, 14.4))
f.text((26, -2.4), "Commute time (minutes)", size=30)
f.raw_text((-8.2, 7), "Number of employees", size=30, rotate=-90, halo=False)
f.save("figures/STAT-07.svg", png="figures/STAT-07.png")
