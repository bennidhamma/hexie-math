import sys, math; sys.path.insert(0, '.')
from svgfig import *
f = Fig(height=650)
r, h, e = 5, 12, 1.6   # radius, height, ellipse half-height (perspective)
def ell(cy, a0, a1):
    return [(r * math.cos(math.radians(t)), cy + e * math.sin(math.radians(t))) for t in range(a0, a1 + 1, 3)]
for p in [(-r, 0), (r, 0), (0, -e), (0, h + e), (-r, h), (r, h)]: f.pt(*p)
f.poly(ell(h, 0, 360), closed=True)
f.poly(ell(0, 180, 360), closed=False)
f.poly(ell(0, 0, 180), closed=False, dashed=True)
f.seg((-r, 0), (-r, h)); f.seg((r, 0), (r, h))
f.seg((-r, h), (r, h)); f.dot((0, h), 4.5)
f.label_point((0, h), "10", (0, 1), gap=12, italic=False)
f.label_seg((r, 0), (r, h), "12", side=-1)
f.save("figures/AREA-03.svg", png="figures/AREA-03.png")
