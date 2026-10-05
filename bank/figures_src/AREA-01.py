import sys; sys.path.insert(0, '.')
from svgfig import *
f = Fig()
A, B, C, D = f.pt(0, 0), f.pt(12, 0), f.pt(12, 8), f.pt(0, 8)
f.pt(16, 4)
arc = [add((12, 4), polar(4, a)) for a in range(-90, 91, 2)]
f.poly([D, A, B], closed=False)
f.poly(arc, closed=False)
f.seg(D, C)
f.seg(B, C, dashed=True)
f.label_seg(A, B, "12", side=-1)
f.label_seg(A, D, "8", side=1)
f.save("figures/AREA-01.svg", png="figures/AREA-01.png")
