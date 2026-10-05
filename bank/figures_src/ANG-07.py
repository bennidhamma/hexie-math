import sys; sys.path.insert(0, '.')
from svgfig import *

# Legs 5 and 12, hypotenuse 13, drawn to scale.
f = Fig()
P, Q, R = f.pt(0, 0), f.pt(12, 0), f.pt(0, 5)
f.poly([P, Q, R])
f.right_angle(P, Q, R)
f.label_seg(P, R, "5", side=1)
f.label_seg(P, Q, "x", side=-1, italic=True)
f.label_seg(R, Q, "13", side=1)
f.save("figures/ANG-07.svg", png="figures/ANG-07.png")
