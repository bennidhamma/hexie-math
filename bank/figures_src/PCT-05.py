import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=900, height=680, margin=40, equal=False)
f.view(-2.3, 7.2, -15, 92)
months, vals = ["April", "May", "June"], [40, 50, 70]

def grid(T, k):  # thin gray grid lines behind the bars
    o = []
    for y in range(10, 81, 10):
        (x0, py), (x1, _) = T((0, y)), T((7, y))
        o.append(f'<line x1="{x0:.1f}" y1="{py:.1f}" x2="{x1:.1f}" y2="{py:.1f}" stroke="#9a9a9a" stroke-width="1.2"/>')
    return "\n".join(o)
f.under.append(grid)

for i, v in enumerate(vals):
    x = 1.25 + 2.25 * i
    box = [(x - 0.65, 0), (x + 0.65, 0), (x + 0.65, v), (x - 0.65, v)]
    f.fill(box, fill="#c8c8c8"); f.poly(box)
    f.text((x, -5), months[i], size=28)
for y in range(0, 81, 10):
    f.seg((-0.12, y), (0, y), width=1.6)
    f.text((-0.25, y), str(y), size=26, anchor="end")
f.seg((0, 0), (7, 0)); f.seg((0, 0), (0, 80))
f.text((3.5, -11.5), "Month", size=30)
f.raw_text((-1.25, 40), "Number of bicycles", size=30, rotate=-90, halo=False)
f.text((3.5, 87.5), "Bicycles sold", size=32, weight="bold")
f.save("figures/PCT-05.svg", png="figures/PCT-05.png")
