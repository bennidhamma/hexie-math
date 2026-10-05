import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from svgfig import *

f = Fig(width=900, height=560)
f.poly([f.pt(-9.5, -6), f.pt(9.5, -6), f.pt(9.5, 6.5), f.pt(-9.5, 6.5)])
f.circle((-2.6, 0.3), 4.8); f.circle((2.6, 0.3), 4.8)
f.text((-4.6, 3.1), "Art", size=30); f.text((4.6, 3.1), "Music", size=30)
f.text((-4.6, 0.0), "14"); f.text((0, 0.0), "10"); f.text((4.6, 0.0), "18")
f.text((8.0, -5.0), "18")
f.save("figures/PROB-05.svg", png="figures/PROB-05.png")
