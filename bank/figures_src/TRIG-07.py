import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Unit circle with P at 150 degrees. The coordinates of P are not shown.
f = PFig(width=820, height=800, margin=60)
R = 1
f.view(-1.45, 1.55, -1.4, 1.5)
f.pt(-1.45, -1.4); f.pt(1.55, 1.5)
O = (0, 0)

def axes(T, k):
    o = []
    (x0, y), (x1, _) = T((-1.4, 0)), T((1.45, 0))
    (x, y0), (_, y1) = T((0, -1.35)), T((0, 1.4))
    o.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke-width="2"/>')
    o.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" stroke-width="2"/>')
    o.append(chevron((x1, y), (1, 0))); o.append(chevron((x0, y), (-1, 0)))
    o.append(chevron((x, y1), (0, -1))); o.append(chevron((x, y0), (0, 1)))
    o.append(T_text(x1 - 4, y - 24, "x", f.font * 0.9, italic=True))
    o.append(T_text(x + 22, y1 + 8, "y", f.font * 0.9, italic=True))
    return "\n".join(o)
f.under.append(axes)

f.circle(O, R)
P = polar(R, 150)
f.seg(O, P)
f.dot(O, 5.5); f.dot(P, 6.5)
f.angle_arc(O, (1, 0), P, r=44)
f.text_px(O, "150°", dx=66, dy=62, size=30)
f.label_point(P, "P", (-0.6, 1), gap=16)
f.text_px(O, "O", dx=20, dy=-24, italic=True)
for p, s, dx, dy in [((1, 0), "1", 18, -22), ((0, 1), "1", -20, 22), ((-1, 0), "−1", -28, -22), ((0, -1), "−1", -28, -22)]:
    f.text_px(p, s, dx=dx, dy=dy, size=28)
f.save("figures/TRIG-07.svg", png="figures/TRIG-07.png")
