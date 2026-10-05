import sys; sys.path.insert(0, '.')
from svgfig import *
f = Fig()
L, W_, H = 10.0, 6.0, 4.0
dx, dy = W_ * 0.5, W_ * 0.33
F_ = [(0, 0), (L, 0), (L, H), (0, H)]
Bk = [(x + dx, y + dy) for x, y in F_]
for p in F_ + Bk: f.pt(*p)
f.poly(F_)
f.seg(F_[1], Bk[1]); f.seg(F_[2], Bk[2]); f.seg(F_[3], Bk[3])
f.seg(Bk[1], Bk[2]); f.seg(Bk[2], Bk[3])
f.seg(Bk[0], Bk[1], dashed=True); f.seg(Bk[0], F_[0], dashed=True); f.seg(Bk[0], Bk[3], dashed=True)
f.label_seg(F_[0], F_[1], "10", side=-1)
f.label_seg(F_[1], Bk[1], "6", side=-1)
f.label_seg(F_[0], F_[3], "4", side=1)
f.save("figures/AREA-06.svg", png="figures/AREA-06.png")
