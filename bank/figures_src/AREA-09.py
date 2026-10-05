import sys; sys.path.insert(0, '.')
from svgfig import *

class GridFig(Fig):
    """Adds light grid lines under everything and arrowheads at the positive axis ends."""
    grid, arrows = [], []
    def svg(self):
        out = super().svg()
        T, _ = self._transform()
        g = []
        for a, b in self.grid:
            (x1, y1), (x2, y2) = T(a), T(b)
            g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#cfcfcf" stroke-width="1"/>')
        head = 'font-family="' + FONT + '">'
        out = out.replace(head, head + "\n" + "\n".join(g), 1)
        (ax, ay), (bx, by) = T(self.arrows[0]), T(self.arrows[1])
        arr = (f'<path d="M{ax:.1f},{ay:.1f} l-12,-6 m12,6 l-12,6" stroke-width="2"/>'
               f'<path d="M{bx:.1f},{by:.1f} l-6,12 m6,-12 l6,12" stroke-width="2"/>')
        out = out.replace("</g></svg>", arr + "</g></svg>")
        # white halo behind the axis numbers so lines that cross them stay readable
        import re
        halo = lambda m: m.group(0).replace('fill="#111" stroke="none"', 'fill="white" stroke="white" stroke-width="7"') + m.group(0)
        return re.sub(r'<text [^>]*>[^<]*</text>', halo, out)

f = GridFig(width=820, height=700, margin=30)
f.view(-5.9, 5.9, -3.8, 5.9)
fs = 22
f.grid = [((x, -3), (x, 5)) for x in range(-5, 6)] + [((-5, y), (5, y)) for y in range(-3, 6)]
X1, Y1 = (5.7, 0), (0, 5.7)
f.arrows = [X1, Y1]
f.seg((-5.6, 0), X1, width=2); f.seg((0, -3.6), Y1, width=2)
f.text((5.55, 0.45), "x", italic=True, size=26)
f.text((0.4, 5.6), "y", italic=True, size=26)
A, B, C = (-4, -2), (4, -2), (1, 4)
f.poly([A, B, C])
neg = lambda v: str(v).replace("-", "−")
for x in range(-5, 6):
    if x:
        f.seg((x, -0.1), (x, 0.1), width=1.6); f.text((x, -0.42), neg(x), size=fs)
for y in range(-3, 6):
    if y:
        f.seg((-0.1, y), (0.1, y), width=1.6); f.text((-0.22, y), neg(y), size=fs, anchor="end")
f.text((-0.25, -0.42), "0", size=fs)
for p, s, d in [(A, "A", (-1, -1)), (B, "B", (1, -1)), (C, "C", (1, 0.8))]:
    f.dot(p, 6); f.label_point(p, s, d, gap=14, size=28)
f.save("figures/AREA-09.svg", png="figures/AREA-09.png")
