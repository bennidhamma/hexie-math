"""Ten test figures in ACT style, to judge hand-built SVG figures. Writes svg-tests/*.svg and *.png."""
import math
from svgfig import *

OUT = "svg-tests/"

# 1. Triangle 13-14-15 with an altitude (same figure as the Codex image test)
f = Fig()
A, B, C, D = f.pt(0, 0), f.pt(14, 0), f.pt(9, 12), f.pt(9, 0)
f.poly([A, B, C])
f.seg(C, D, dashed=True); f.right_angle(D, B, C)
for p, s, d in [(A, "A", (-1, -0.6)), (B, "B", (1, -0.6)), (C, "C", (0, 1)), (D, "D", (0, -1))]:
    f.label_point(p, s, d)
f.label_seg(A, C, "15"); f.label_seg(C, B, "13"); f.dimension(A, B, "14", offset=-2.2)
f.margin = 95
f.save(OUT + "01-triangle-altitude.svg", png=OUT + "01-triangle-altitude.png")

# 2. Parallel lines cut by two transversals that meet above the top line
f = Fig()
L1a, L1b, L2a, L2b = f.pt(-1, 0), f.pt(15, 0), f.pt(-1, 5), f.pt(15, 5)
f.seg(L1a, L1b); f.seg(L2a, L2b)
f.arrow_mark(L1a, L1b, at=0.93); f.arrow_mark(L2a, L2b, at=0.93)
P, Q, R = (3, 0), (11, 0), (7, 8.5)
t1, t2 = (P[0] - (R[0] - P[0]) * 0.2, -1.7), (Q[0] + (Q[0] - R[0]) * 0.2, -1.7)
f.seg(t1, add(R, mul(sub(R, P), 0.12))); f.seg(t2, add(R, mul(sub(R, Q), 0.12)))
S = (P[0] + (R[0] - P[0]) * 5 / 8.5, 5); T_ = (Q[0] + (R[0] - Q[0]) * 5 / 8.5, 5)
f.angle_arc(P, L1a, R, r=30, label="115°")
f.angle_arc(Q, R, L1b, r=30, label="120°")
f.angle_arc(R, S, T_, r=30, label="x°", italic=True)
f.label_point(L2b, "ℓ", (1, 0), italic=True); f.label_point(L1b, "m", (1, 0), italic=True)
f.save(OUT + "02-parallel-transversals.svg", png=OUT + "02-parallel-transversals.png")

# 3. Circle with a shaded sector and central angle
f = Fig()
O = f.pt(0, 0); f.circle(O, 10)
f.sector(O, 10, 20, 92)
A_, B_ = polar(10, 20), polar(10, 92)
f.circle(O, 10)
f.seg(O, A_); f.seg(O, B_); f.dot(O, 4)
f.angle_arc(O, A_, B_, r=36, label="72°")
f.label_point(O, "O", (0.3, -1)); f.label_point(A_, "A", unit(A_)); f.label_point(B_, "B", unit(B_))
f.label_seg(O, A_, "10", side=-1)
f.save(OUT + "03-circle-sector.svg", png=OUT + "03-circle-sector.png")

# 4. Square with an inscribed circle; the corners are shaded
f = Fig()
sq = [f.pt(0, 0), f.pt(8, 0), f.pt(8, 8), f.pt(0, 8)]
f.fill(sq); f.fill_circle((4, 4), 4); f.poly(sq); f.circle((4, 4), 4)
f.label_seg((0, 0), (8, 0), "8 cm", side=-1)
f.save(OUT + "04-square-inscribed-circle.svg", png=OUT + "04-square-inscribed-circle.png")

# 5. Parabola on a grid
f = Fig(width=800, height=700, margin=40)
f.view(-3, 7, -3, 11)
f.axes(ticks_every=1, number_every=2)
f.curve(lambda x: -(x - 2) ** 2 + 9, -3, 7)
f.save(OUT + "05-parabola-graph.svg", png=OUT + "05-parabola-graph.png")

# 6. Bar graph
f = Fig(width=900, height=620, margin=80, equal=False)
years, vals = ["2019", "2020", "2021", "2022", "2023"], [40, 55, 50, 70, 84]
f.view(-1.3, 10.4, -12, 100)
for i, v in enumerate(vals):
    x = 1 + 2 * i
    f.fill([(x - 0.6, 0), (x + 0.6, 0), (x + 0.6, v), (x - 0.6, v)], fill="#bdbdbd")
    f.poly([(x - 0.6, 0), (x + 0.6, 0), (x + 0.6, v), (x - 0.6, v)])
    f.text((x, -6), years[i], size=24)
for y in range(0, 101, 20):
    f.seg((0, y), (10, y), width=0.8) if y else None
    f.text((-0.45, y), str(y), size=22, anchor="end")
f.seg((0, 0), (10, 0)); f.seg((0, 0), (0, 100))
f.text((5, 106), "Chess club members by year", size=26, weight="bold")
f.save(OUT + "06-bar-graph.svg", png=OUT + "06-bar-graph.png")

# 7. Angle of elevation to the top of a building
f = Fig()
G0, G1 = f.pt(-2, 0), f.pt(26, 0)
f.seg(G0, G1)
bld = [(18, 0), (24, 0), (24, 14), (18, 14)]
f.poly(bld)
for wy in (3, 7, 11):
    for wx in (19.3, 21.6):
        f.poly([(wx, wy), (wx + 1.1, wy), (wx + 1.1, wy + 1.6), (wx, wy + 1.6)], )
E, Top = f.pt(0, 0), (18, 14)
f.seg(E, Top, dashed=True); f.dot(E, 5)
f.angle_arc(E, (5, 0), Top, r=60, label="38°")
f.label_seg(E, (18, 0), "80 ft", side=-1)
f.label_point((18, 7), "h", (-1, 0), italic=True)
f.right_angle((18, 0), (0, 0), Top)
f.save(OUT + "07-angle-of-elevation.svg", png=OUT + "07-angle-of-elevation.png")

# 8. Rectangular box with hidden edges dashed
f = Fig()
L, W_, H = 6.0, 4.0, 3.0
dx, dy = W_ * 0.55, W_ * 0.38
F_ = [(0, 0), (L, 0), (L, H), (0, H)]
Bk = [(x + dx, y + dy) for x, y in F_]
for p in F_ + Bk: f.pt(*p)
f.poly(F_)
f.seg(F_[1], Bk[1]); f.seg(F_[2], Bk[2]); f.seg(F_[3], Bk[3]); f.seg(Bk[1], Bk[2]); f.seg(Bk[2], Bk[3])
f.seg(F_[0], Bk[0], dashed=True); f.seg(Bk[0], Bk[1], dashed=True); f.seg(Bk[0], Bk[3], dashed=True)
f.label_seg(F_[0], F_[1], "6 in", side=-1); f.label_seg(F_[1], Bk[1], "4 in", side=-1); f.label_seg(F_[0], F_[3], "3 in", side=-1)
f.save(OUT + "08-rectangular-box.svg", png=OUT + "08-rectangular-box.png")

# 9. Venn diagram
f = Fig(width=900, height=560)
f.poly([f.pt(-9, -6), f.pt(9, -6), f.pt(9, 6.5), f.pt(-9, 6.5)])
f.circle((-2.6, 0), 4.6); f.circle((2.6, 0), 4.6)
f.text((-4.2, 5.4), "Band", size=28); f.text((4.2, 5.4), "Choir", size=28)
f.text((-4.4, -0.4), "18"); f.text((0, -0.4), "7"); f.text((4.4, -0.4), "12"); f.text((7.6, -5), "13")
f.save(OUT + "09-venn.svg", png=OUT + "09-venn.png")

# 10. Triangle with a segment parallel to its base (similar triangles)
f = Fig()
A, B, C = f.pt(4, 9), f.pt(0, 0), f.pt(12, 0)
D, E = add(A, mul(sub(B, A), 0.4)), add(A, mul(sub(C, A), 0.4))
f.poly([A, B, C]); f.seg(D, E)
f.arrow_mark(D, E, at=0.6); f.arrow_mark(B, C, at=0.6)
for p, s, d in [(A, "A", (0, 1)), (B, "B", (-1, -0.5)), (C, "C", (1, -0.5)), (D, "D", (-1, 0.2)), (E, "E", (1, 0.3))]:
    f.label_point(p, s, d)
f.label_seg(A, D, "4", side=-1); f.label_seg(D, B, "6", side=-1); f.label_seg(D, E, "5", side=-1, gap=14); f.label_seg(B, C, "?", side=-1)
f.save(OUT + "10-similar-triangles.svg", png=OUT + "10-similar-triangles.png")
print("ok")
