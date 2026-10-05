import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=700, height=900, margin=50)
f.plot(-1, 5, -6, 4, gx=1, gy=1, xnums=range(-1, 6), ynums=range(-6, 5), ext=0.6, yright={-6})
g = lambda x: -2 * (x - 2) ** 2 + 3
xl, xr = 2 - math.sqrt(4.5), 2 + math.sqrt(4.5)   # where the arms reach y = -6
f.curve(g, xl, xr, steps=400)
f.curve_arrow(g, xl, xl + 0.05); f.curve_arrow(g, xr, xr - 0.05)
for p in [(2, 3), (0, -5), (1, 1), (3, 1), (4, -5)]:
    f.dot(p, 6)
f.raw_text((4, -3), "g", italic=True, dx=10)
f.save("figures/FUN-04.svg", png="figures/FUN-04.png")
