import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=760, height=900, margin=50)
f.plot(-6, 2, -5, 6, gx=1, gy=1, xnums=range(-6, 3), ynums=range(-5, 7), ext=0.6, yright={-1, -2, -3, -4, -5}, xshift={-4: -22})
q = lambda x: (x + 2) ** 2 - 4
xl, xr = -2 - math.sqrt(10), -2 + math.sqrt(10)   # where the arms reach y = 6
f.curve(q, xl, xr, steps=400)
f.curve_arrow(q, xl, xl + 0.05); f.curve_arrow(q, xr, xr - 0.05)
for p in [(-2, -4), (-4, 0), (0, 0), (-5, 5), (1, 5)]:
    f.dot(p, 6)
f.raw_text((-5.3, 4), "f", italic=True)
f.save("figures/QUAD-03.svg", png="figures/QUAD-03.png")
