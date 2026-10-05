import sys; sys.path.insert(0, '.')
from svgfig import *
f = Fig()
r = 12
O = f.pt(0, 0)
f.sector(O, r, 0, 120)
f.circle(O, r)
A, B = polar(r, 0), polar(r, 120)
arc = [polar(r, a) for a in range(0, 121, 2)]
for p, q in zip(arc, arc[1:]): f.seg(p, q, width=4.6)
f.seg(O, A); f.seg(O, B); f.dot(O, 5)
f.angle_arc(O, A, B, r=34, label="120°")
f.label_point(O, "O", (-0.7, -1))
f.label_point(A, "A", (1, 0)); f.label_point(B, "B", unit(B))
f.label_point(polar(r, 60), "8π", polar(1, 60), gap=12, italic=False)
f.save("figures/AREA-08.svg", png="figures/AREA-08.png")
