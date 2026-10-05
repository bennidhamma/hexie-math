"""Helpers for coordinate graphs and charts on top of svgfig.Fig.

PFig adds raw SVG layers (under / over the normal items), real minus signs in numbers,
and plot() draws a grid, axes with arrowheads, and tick numbers for a set data range.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from svgfig import *  # noqa: F401,F403
from svgfig import Fig, FONT, INK, unit, sub, add, mul, fmt

GRID = "#cfcfcf"


def T_text(x, y, s, size, anchor="middle", italic=False, rotate=None, weight="normal", halo=False):
    style = "italic" if italic else "normal"
    rot = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate is not None else ""
    base = (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-style="{style}" font-weight="{weight}" '
            f'text-anchor="{anchor}" dominant-baseline="central"{rot} ')
    out = base + f'fill="{INK}" stroke="none">{s}</text>'
    if halo:  # white outline copy underneath (cairosvg ignores paint-order)
        out = base + f'fill="white" stroke="white" stroke-width="6" stroke-linejoin="round">{s}</text>' + out
    return out


def chevron(tip, d, size=12, width=2):
    """Open arrowhead at page point tip, pointing along page direction d."""
    u = unit(d); n = (-u[1], u[0])
    p1 = add(sub(tip, mul(u, size)), mul(n, size * 0.5))
    p2 = sub(sub(tip, mul(u, size)), mul(n, size * 0.5))
    return (f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" '
            f'fill="none" stroke-width="{width}"/>')


class PFig(Fig):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.under, self.over = [], []

    def svg(self):
        out = super().svg()
        T, k = self._transform()
        under = "\n".join(fn(T, k) for fn in self.under)
        over = "\n".join(fn(T, k) for fn in self.over)
        i = out.index(">", out.index("<g ")) + 1
        out = out[:i] + "\n" + under + out[i:]
        out = out.replace("</g></svg>", over + "\n</g></svg>")
        out = re.sub(r">-(\d)", r">−\1", out)
        return out

    # ---- raw helpers (math coordinates in, page pixels out) ----
    def raw_text(self, p, s, size=None, anchor="middle", italic=False, dx=0, dy=0, rotate=None, weight="normal", halo=True):
        size = size or self.font
        def fn(T, k):
            x, y = T(p)
            return T_text(x + dx, y + dy, s, size, anchor, italic, rotate, weight, halo)
        self.over.append(fn)

    def curve_arrow(self, fn_, x_end, x_inner, size=14):
        """Arrowhead at the curve end x_end, tangent to the curve (x_inner is a nearby x toward the inside)."""
        def f(T, k):
            tip = T((x_end, fn_(x_end))); back = T((x_inner, fn_(x_inner)))
            return chevron(tip, sub(tip, back), size=size, width=self.stroke * 1.1)
        self.over.append(f)

    def open_square(self, p, half=7):
        def f(T, k):
            x, y = T(p)
            return f'<rect x="{x - half:.1f}" y="{y - half:.1f}" width="{2 * half}" height="{2 * half}" fill="white" stroke-width="2.2"/>'
        self.over.append(f)

    def plot(self, x0, x1, y0, y1, gx=None, gy=None, xnums=(), ynums=(), xticks=None, yticks=None,
             ext=0.5, exty=None, arrows=True, origin="0", xlabel="x", ylabel="y", label_mode="end",
             num_size=None, label_size=None, grid=True, nfmt=fmt, xshift=None, yright=()):
        """Grid over [x0,x1]x[y0,y1], axes through the origin (or the low edge) with arrows past the range."""
        exty = ext if exty is None else exty
        ns = num_size or self.font * 0.72
        ls = label_size or self.font * 0.9
        ax_y = 0 if y0 <= 0 <= y1 else y0
        ax_x = 0 if x0 <= 0 <= x1 else x0
        xticks = list(xnums) if xticks is None else xticks
        yticks = list(ynums) if yticks is None else yticks
        XE, YE = x1 + (ext if arrows else 0), y1 + (exty if arrows else 0)
        self.view(x0 if ax_x != x0 else x0, XE, y0 if ax_y != y0 else y0, YE)

        def under(T, k):
            o = []
            if grid:
                xs = [x0 + i * gx for i in range(int(round((x1 - x0) / gx)) + 1)]
                ys = [y0 + i * gy for i in range(int(round((y1 - y0) / gy)) + 1)]
                for x in xs:
                    (px, py0), (_, py1) = T((x, y0)), T((x, y1))
                    o.append(f'<line x1="{px:.1f}" y1="{py0:.1f}" x2="{px:.1f}" y2="{py1:.1f}" stroke="{GRID}" stroke-width="1.2"/>')
                for y in ys:
                    (px0, py), (px1, _) = T((x0, y)), T((x1, y))
                    o.append(f'<line x1="{px0:.1f}" y1="{py:.1f}" x2="{px1:.1f}" y2="{py:.1f}" stroke="{GRID}" stroke-width="1.2"/>')
            # axes
            (a0x, ay), (a1x, _) = T((x0, ax_y)), T((XE, ax_y))
            (bx, b0y), (_, b1y) = T((ax_x, y0)), T((ax_x, YE))
            o.append(f'<line x1="{a0x:.1f}" y1="{ay:.1f}" x2="{a1x:.1f}" y2="{ay:.1f}" stroke-width="2"/>')
            o.append(f'<line x1="{bx:.1f}" y1="{b0y:.1f}" x2="{bx:.1f}" y2="{b1y:.1f}" stroke-width="2"/>')
            if arrows:
                o.append(chevron((a1x, ay), (1, 0)))
                o.append(chevron((bx, b1y), (0, -1)))
            for x in xticks:
                if abs(x - ax_x) < 1e-9 and origin is not None:
                    continue
                px, py = T((x, ax_y))
                o.append(f'<line x1="{px:.1f}" y1="{py - 5:.1f}" x2="{px:.1f}" y2="{py + 5:.1f}" stroke-width="1.6"/>')
            for y in yticks:
                if abs(y - ax_y) < 1e-9 and origin is not None:
                    continue
                px, py = T((ax_x, y))
                o.append(f'<line x1="{px - 5:.1f}" y1="{py:.1f}" x2="{px + 5:.1f}" y2="{py:.1f}" stroke-width="1.6"/>')
            return "\n".join(o)
        self.under.append(under)

        def over(T, k):
            o = []
            for x in xnums:
                if abs(x - ax_x) < 1e-9:
                    continue
                px, py = T((x, ax_y))
                o.append(T_text(px + (xshift or {}).get(x, 0), py + 21, nfmt(x), ns, halo=True))
            for y in ynums:
                if abs(y - ax_y) < 1e-9:
                    continue
                px, py = T((ax_x, y))
                if y in yright:
                    o.append(T_text(px + 12, py, nfmt(y), ns, anchor="start", halo=True))
                else:
                    o.append(T_text(px - 12, py, nfmt(y), ns, anchor="end", halo=True))
            if origin is not None:
                px, py = T((ax_x, ax_y))
                o.append(T_text(px - 12, py + 19, origin, ns, anchor="end", halo=True))
            (a1x, ay) = T((XE, ax_y)); (bx, b1y) = T((ax_x, YE))
            if label_mode == "end":
                o.append(T_text(a1x - 4, ay - 22, xlabel, ls, italic=True))
                o.append(T_text(bx + 20, b1y + 6, ylabel, ls, italic=True))
            return "\n".join(o)
        self.under.append(over)
