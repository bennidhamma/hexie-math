import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _plotkit import *

f = PFig(width=900, height=720, margin=100, equal=False)
f.plot(0, 6, 0, 140, xnums=range(0, 7), ynums=[0, 40, 80, 120], yticks=list(range(0, 141, 20)),
       ext=0.5, exty=14, grid=False, label_mode=None, num_size=26)
f.view(0, 7.9, 0, 154)   # room on the right for the axis label
h = lambda t: -16 * t * t + 80 * t + 16
tend = (5 + math.sqrt(29)) / 2
f.seg((0, 80), (4, 80), dashed=True, width=1.6)
f.seg((1, 0), (1, 80), dashed=True, width=1.6)
f.seg((4, 0), (4, 80), dashed=True, width=1.6)
f.curve(h, 0, tend, steps=400)
f.dot((1, 80), 6.5); f.dot((4, 80), 6.5)
f.raw_text((6.5, 0), "t (seconds)", size=28, anchor="start", dx=12, halo=False)
f.raw_text((0, 154), "h (feet)", size=28, anchor="start", dx=-30, dy=-24, halo=False)
f.save("figures/QUAD-06.svg", png="figures/QUAD-06.png")
