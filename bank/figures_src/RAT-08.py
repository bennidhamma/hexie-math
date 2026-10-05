import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from svgfig import *

# True proportions: lamp 18 ft high, person 6 ft tall 12 ft from the pole, shadow 6 ft long.
f = Fig(width=900, height=720, margin=70)
f.pt(-3, 0); f.pt(21, 0); f.pt(0, 19)
lamp, head, tip = (0, 18), (12, 6), (18, 0)
f.seg((-2.5, 0), (12, 0)); f.seg((18, 0), (21, 0))
f.seg((12, 0), tip, width=5.5)                  # shadow, slightly heavier
f.seg((0, 0), (0, 17.6))                        # pole
f.circle(lamp, 0.4, fill="white")               # lamp (open circle)
f.right_angle((0, 0), (1, 0), (0, 1), size=18)
# person: small head and a narrow body outline. The head top is at height 6 and the
# dashed ray touches the head there (center shifted left so the ray is tangent).
hr = 0.45
cx = 12 - hr * (2 ** 0.5 - 1)
f.circle((cx, 6 - hr), hr)
body = [(-0.25, 0), (-0.25, 2.9), (-0.4, 2.9), (-0.4, 4.6), (-0.05, 5.1 - 0.1), (0.05, 5.0),
        (0.4, 4.6), (0.4, 2.9), (0.25, 2.9), (0.25, 0)]
body[4] = (-0.05, 5.0)
f.poly([(cx + dx, y) for dx, y in body], closed=False)
f.seg((cx, 0), (cx, 2.9), width=1.6)            # line between the legs
# height guide beside the person (left side, clear of the dashed ray)
g = 10.6
f.seg((g, 0), (g, 6), width=1.6)
f.seg((g - 0.3, 6), (g + 0.3, 6), width=1.6)
f.right_angle((g, 0), (g - 1, 0), (g, 1), size=14)
f.seg(lamp, tip, dashed=True)
f.label_point((0, 9), "18 ft", (-1, 0), gap=14, italic=False)
f.label_point((g, 3), "6 ft", (-1, 0), gap=12, italic=False)
f.dimension((0, 0), (12, 0), "12 ft", offset=-1.6)
f.dimension((12, 0), (18, 0), "x", offset=-1.6, italic=True)
f.save("figures/RAT-08.svg", png="figures/RAT-08.png")
