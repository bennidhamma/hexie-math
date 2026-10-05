import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

# Instrument 5 ft tall, 120 ft from the tower; elevation 38 degrees to the top.
# Tower height = 5 + 120 tan 38 (about 98.8 ft), not labeled.
# The instrument is drawn taller than true scale (h0 = 14 units) so the 5 ft label is readable;
# the 38 degree angle and the 120 ft distance are exact.
D, h0, ang = 120, 14, 38
H = h0 + D * math.tan(math.radians(ang))
f = Fig(width=900, height=760, margin=70)
G0, G1 = f.pt(-22, 0), f.pt(D + 26, 0)
f.seg(G0, G1)
P = f.pt(0, h0)
f.seg((0, 0), P, width=3.6)                       # instrument post
f.seg((-4, 0), (0, 5)); f.seg((4, 0), (0, 5))           # tripod legs
f.dot(P, 6)
tw = 12                                             # tower width
f.poly([(D, 0), (D + tw, 0), (D + tw, H), (D, H)])
top = (D, H)
f.seg(P, top)                                       # line of sight
f.seg(P, (D, h0), dashed=True)                      # level line
f.right_angle((D, h0), P, top, size=18)
f.angle_mark(P, (D, h0), top, "38°", r=70)
f.dimension((0, 0), (D, 0), "120", offset=-9)
f.dimension((0, 0), (0, h0), "5", offset=9)
f.save("figures/TRIG-04.svg", png="figures/TRIG-04.png")
