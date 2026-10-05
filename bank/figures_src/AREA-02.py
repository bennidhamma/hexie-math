import sys, math; sys.path.insert(0, '.')
from svgfig import *
f = Fig()
s = 16 / math.sqrt(2)
sq = [f.pt(0, 0), f.pt(s, 0), f.pt(s, s), f.pt(0, s)]
c = (s / 2, s / 2)
f.fill(sq); f.fill_circle(c, s / 2)
f.poly(sq); f.circle(c, s / 2)
f.seg(sq[0], sq[2], dashed=True)
f.label_point(c, "16", (-1, 1), gap=10, italic=False)
f.save("figures/AREA-02.svg", png="figures/AREA-02.png")
