"""
A small library for ACT-style math figures as SVG: black line art, sans-serif labels,
exact geometry. Figures are built in "math" coordinates (y up) and fitted to the page.

    f = Fig()
    A, B = f.pt(0, 0), f.pt(14, 0)
    f.seg(A, B); f.label_point(A, "A", (-1, -1))
    f.save("out.svg", png="out.png")
"""
import math

FONT = "Arial, 'Liberation Sans', 'DejaVu Sans', sans-serif"
INK = "#111"
GRAY = "#d9d9d9"


def add(a, b): return (a[0] + b[0], a[1] + b[1])
def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def mul(a, k): return (a[0] * k, a[1] * k)
def length(a): return math.hypot(a[0], a[1])
def unit(a):
    d = length(a)
    return (a[0] / d, a[1] / d) if d else (0.0, 0.0)
def mid(a, b): return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
def ang(a): return math.degrees(math.atan2(a[1], a[0]))
def polar(r, deg): return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))


class Fig:
    """Collects shapes in math coordinates. Units are arbitrary; save() scales them to the page."""

    def __init__(self, width=900, height=600, margin=80, stroke=2.8, font=34, equal=True):
        self.W, self.H, self.margin = width, height, margin
        self.stroke, self.font = stroke, font
        self.items = []        # (kind, data) drawn in order
        self.pts = []          # every coordinate, for fitting
        self.fixed = None      # optional (xmin, xmax, ymin, ymax) view box in math units
        self.equal = equal     # same scale on both axes (geometry); False for charts

    # ---- coordinates ----
    def pt(self, x, y):
        self.pts.append((x, y))
        return (x, y)

    def view(self, xmin, xmax, ymin, ymax):
        """Fix the visible region (graphs). Otherwise the figure fits its points."""
        self.fixed = (xmin, xmax, ymin, ymax)

    # ---- drawing (all in math coordinates) ----
    def seg(self, a, b, dashed=False, width=None):
        self.pts += [a, b]
        self.items.append(("line", (a, b, dashed, width)))

    def poly(self, pts, fill="none", dashed=False, closed=True):
        self.pts += list(pts)
        self.items.append(("poly", (list(pts), fill, dashed, closed)))

    def circle(self, c, r, fill="none", dashed=False):
        self.pts += [add(c, (r, r)), sub(c, (r, r))]
        self.items.append(("circle", (c, r, fill, dashed)))

    def sector(self, c, r, a0, a1, fill=GRAY):
        """Filled sector from angle a0 to a1 (degrees, counterclockwise)."""
        self.items.append(("sector", (c, r, a0, a1, fill)))

    def fill(self, pts, fill=GRAY):
        """Fill a polygon region with no outline (draw it before the lines on top)."""
        self.items.append(("fill", (list(pts), fill)))

    def fill_circle(self, c, r, fill="white"):
        """Fill a disc with no outline, e.g. to cut a white hole out of a shaded region."""
        self.items.append(("fillcircle", (c, r, fill)))

    def curve(self, fn, x0, x1, steps=200, dashed=False):
        pts = [(x0 + (x1 - x0) * i / steps, fn(x0 + (x1 - x0) * i / steps)) for i in range(steps + 1)]
        self.items.append(("curve", (pts, dashed)))

    def dot(self, p, r=5, open_=False):
        self.pts.append(p)
        self.items.append(("dot", (p, r, open_)))

    def text(self, p, s, italic=False, size=None, anchor="middle", weight="normal"):
        """Text centered at math point p."""
        self.items.append(("text", (p, s, italic, size, anchor, weight)))

    def point(self, p, name, direction=(0, 1), dot=True):
        """A named point: a small dot (optional) and an italic label pushed out along direction."""
        self.pts.append(p)
        if dot:
            self.dot(p, 5.5)
        self.label_point(p, name, direction)
        return p

    # ---- labels with an offset in page pixels (dx right, dy up) ----
    def label_point(self, p, s, direction=(0, 1), gap=22, italic=True, size=None):
        d = unit(direction)
        self.items.append(("label", (p, s, d, gap, italic, size)))

    def label_seg(self, a, b, s, side=1, gap=24, italic=False, size=None):
        """Label a segment at its middle, on the left (side=1) or right (side=-1) of a->b."""
        d = unit(sub(b, a))
        n = (-d[1] * side, d[0] * side)
        self.items.append(("label", (mid(a, b), s, n, gap, italic, size)))

    def dimension(self, a, b, s, offset=-1.6, gap=6, italic=False):
        """A thin dimension line parallel to ab, offset by `offset` math units (negative: right of a->b),
        with end bars and the label in a gap at its middle. Use it when a point sits on the side."""
        d = unit(sub(b, a)); n = (-d[1], d[0])
        a2, b2 = add(a, mul(n, offset)), add(b, mul(n, offset))
        self.pts += [a2, b2]
        self.items.append(("dim", (a2, b2, s, italic)))

    # ---- marks ----
    def right_angle(self, v, a, b, size=16):
        """Small square at v between rays v->a and v->b (size in page pixels)."""
        self.items.append(("right", (v, a, b, size)))

    def angle_arc(self, v, a, b, r=34, label=None, label_gap=16, double=False, italic=False):
        """Arc at v from ray v->a to ray v->b (the smaller angle), with an optional label (page pixels)."""
        self.items.append(("arc", (v, a, b, r, label, label_gap, double, italic)))

    def ticks(self, a, b, n=1, size=12):
        """n tick marks across the middle of segment ab (equal sides)."""
        self.items.append(("ticks", (a, b, n, size)))

    def arrow_mark(self, a, b, n=1, at=0.5, size=12):
        """Parallel-line arrowheads on segment ab."""
        self.items.append(("arrows", (a, b, n, at, size)))

    def axes(self, xlabel="x", ylabel="y", ticks_every=1, grid=True, numbers=True, number_every=None):
        self.items.insert(0, ("axes", (xlabel, ylabel, ticks_every, grid, numbers, number_every or ticks_every)))

    def angle_mark(self, v, a, b, label, r=34, double=False, italic=False, at=0.5, pad=8, size=None, arc=True):
        """Arc at v from ray v->a to ray v->b (the smaller angle) with the label auto-placed inside the angle:
        the label moves out along the ray at fraction `at` of the sweep (0.5 = bisector) until its box
        clears both rays by `pad` pixels and clears the arc. Labels may use var() markup."""
        self.items.append(("anglemark", (v, a, b, r, label, double, italic, at, pad, size, arc)))

    def text_px(self, p, s, dx=0, dy=0, italic=False, size=None):
        """Text centered at math point p moved by (dx right, dy up) page pixels."""
        self.items.append(("pxtext", (p, s, dx, dy, italic, size)))

    # ---- output ----
    def _transform(self):
        if self.fixed:
            xmin, xmax, ymin, ymax = self.fixed
        else:
            xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
            xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
        w = max(xmax - xmin, 1e-9); h = max(ymax - ymin, 1e-9)
        kx, ky = (self.W - 2 * self.margin) / w, (self.H - 2 * self.margin) / h
        if self.equal:
            kx = ky = min(kx, ky)
        ox = (self.W - w * kx) / 2 - xmin * kx
        oy = (self.H + h * ky) / 2 + ymin * ky
        self.view_box = (xmin, xmax, ymin, ymax)
        return lambda p: (ox + p[0] * kx, oy - p[1] * ky), kx

    def svg(self):
        T, k = self._transform()
        s = self.stroke
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}">',
               f'<rect width="100%" height="100%" fill="white"/>',
               f'<g fill="none" stroke="{INK}" stroke-width="{s}" stroke-linecap="round" stroke-linejoin="round" font-family="{FONT}">']

        def txt(x, y, string, italic=False, size=None, anchor="middle", weight="normal"):
            style = "italic" if italic else "normal"
            if "<tspan" in string and anchor == "middle":
                # Some renderers center each tspan chunk on its own; anchor at the start instead.
                x -= markup_width(string, size or self.font, italic) / 2
                anchor = "start"
            return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size or self.font}" font-style="{style}" font-weight="{weight}" '
                    f'text-anchor="{anchor}" dominant-baseline="central" fill="{INK}" stroke="none">{string}</text>')

        for kind, d in self.items:
            if kind == "axes":
                xlabel, ylabel, every, grid, numbers, num_every = d
                xmin, xmax, ymin, ymax = self.view_box
                if grid:
                    x = math.ceil(xmin / every) * every
                    while x <= xmax + 1e-9:
                        (px, _), (_, py0), (_, py1) = T((x, 0)), T((0, ymin)), T((0, ymax))
                        out.append(f'<line x1="{px:.1f}" y1="{py0:.1f}" x2="{px:.1f}" y2="{py1:.1f}" stroke="#cfcfcf" stroke-width="1"/>')
                        x += every
                    y = math.ceil(ymin / every) * every
                    while y <= ymax + 1e-9:
                        (_, py), (px0, _), (px1, _) = T((0, y)), T((xmin, 0)), T((xmax, 0))
                        out.append(f'<line x1="{px0:.1f}" y1="{py:.1f}" x2="{px1:.1f}" y2="{py:.1f}" stroke="#cfcfcf" stroke-width="1"/>')
                        y += every
                (ax0, ay), (ax1, _) = T((xmin, 0)), T((xmax, 0))
                (bx, by0), (_, by1) = T((0, ymin)), T((0, ymax))
                out.append(f'<line x1="{ax0:.1f}" y1="{ay:.1f}" x2="{ax1:.1f}" y2="{ay:.1f}" stroke-width="2"/>')
                out.append(f'<line x1="{bx:.1f}" y1="{by0:.1f}" x2="{bx:.1f}" y2="{by1:.1f}" stroke-width="2"/>')
                out.append(f'<path d="M{ax1:.1f},{ay:.1f} l-12,-6 m12,6 l-12,6" stroke-width="2"/>')
                out.append(f'<path d="M{bx:.1f},{by1:.1f} l-6,12 m6,-12 l6,12" stroke-width="2"/>')
                out.append(txt(ax1 - 4, ay - 22, xlabel, italic=True, size=self.font * 0.9))
                out.append(txt(bx + 20, by1 + 6, ylabel, italic=True, size=self.font * 0.9))
                if numbers:
                    x = math.ceil(xmin / num_every) * num_every
                    while x <= xmax - num_every * 0.5:
                        if abs(x) > 1e-9:
                            px, py = T((x, 0))
                            out.append(f'<line x1="{px:.1f}" y1="{py - 5:.1f}" x2="{px:.1f}" y2="{py + 5:.1f}" stroke-width="1.6"/>')
                            out.append(txt(px, py + 20, fmt(x), size=self.font * 0.72))
                        x += num_every
                    y = math.ceil(ymin / num_every) * num_every
                    while y <= ymax - num_every * 0.5:
                        if abs(y) > 1e-9:
                            px, py = T((0, y))
                            out.append(f'<line x1="{px - 5:.1f}" y1="{py:.1f}" x2="{px + 5:.1f}" y2="{py:.1f}" stroke-width="1.6"/>')
                            out.append(txt(px - 12, py, fmt(y), size=self.font * 0.72, anchor="end"))
                        y += num_every
            elif kind == "line":
                a, b, dashed, width = d
                (x1, y1), (x2, y2) = T(a), T(b)
                dash = ' stroke-dasharray="10 8"' if dashed else ""
                wid = f' stroke-width="{width}"' if width else ""
                out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"{dash}{wid}/>')
            elif kind == "poly":
                pts, fill, dashed, closed = d
                ps = " ".join(f"{T(p)[0]:.1f},{T(p)[1]:.1f}" for p in pts)
                tag = "polygon" if closed else "polyline"
                dash = ' stroke-dasharray="10 8"' if dashed else ""
                out.append(f'<{tag} points="{ps}" fill="{fill}"{dash}/>')
            elif kind == "fill":
                pts, fill = d
                ps = " ".join(f"{T(p)[0]:.1f},{T(p)[1]:.1f}" for p in pts)
                out.append(f'<polygon points="{ps}" fill="{fill}" stroke="none"/>')
            elif kind == "fillcircle":
                c, r, fill = d
                cx, cy = T(c)
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * k:.1f}" fill="{fill}" stroke="none"/>')
            elif kind == "circle":
                c, r, fill, dashed = d
                (cx, cy) = T(c)
                dash = ' stroke-dasharray="10 8"' if dashed else ""
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * k:.1f}" fill="{fill}"{dash}/>')
            elif kind == "sector":
                c, r, a0, a1, fill = d
                p0, p1 = T(add(c, polar(r, a0))), T(add(c, polar(r, a1)))
                cx, cy = T(c)
                large = 1 if (a1 - a0) % 360 > 180 else 0
                out.append(f'<path d="M{cx:.1f},{cy:.1f} L{p0[0]:.1f},{p0[1]:.1f} A{r * k:.1f},{r * k:.1f} 0 {large} 0 {p1[0]:.1f},{p1[1]:.1f} Z" fill="{fill}" stroke="none"/>')
            elif kind == "curve":
                pts, dashed = d
                xmin, xmax, ymin, ymax = self.view_box
                segs, cur = [], []
                for p in pts:
                    if ymin - 1 <= p[1] <= ymax + 1:
                        cur.append(p)
                    elif cur:
                        segs.append(cur); cur = []
                if cur:
                    segs.append(cur)
                dash = ' stroke-dasharray="10 8"' if dashed else ""
                (cx0, cy0), (cx1, cy1) = T((xmin, ymax)), T((xmax, ymin))
                out.append(f'<clipPath id="view"><rect x="{cx0:.1f}" y="{cy0:.1f}" width="{cx1 - cx0:.1f}" height="{cy1 - cy0:.1f}"/></clipPath>')
                for sgm in segs:
                    dd = "M" + " L".join(f"{T(p)[0]:.1f},{T(p)[1]:.1f}" for p in sgm)
                    out.append(f'<path d="{dd}" stroke-width="{s * 1.1}" clip-path="url(#view)"{dash}/>')
            elif kind == "dot":
                p, r, open_ = d
                x, y = T(p)
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{"white" if open_ else INK}"/>')
            elif kind == "text":
                p, string, italic, size, anchor, weight = d
                x, y = T(p)
                out.append(txt(x, y, string, italic, size, anchor, weight))
            elif kind == "label":
                p, string, direction, gap, italic, size = d
                x, y = T(p)
                fs = size or self.font
                # Push the text box (about 0.55 em per character wide) out along the direction.
                tw = 0.56 * fs * vis_len(string); th = 0.8 * fs
                dx, dy = direction[0], -direction[1]
                reach = min(tw / 2 / max(abs(dx), 1e-3), th / 2 / max(abs(dy), 1e-3))
                out.append(txt(x + dx * (gap + reach), y + dy * (gap + reach), string, italic, fs))
            elif kind == "right":
                v, a, b, size = d
                pv, pa, pb = T(v), T(a), T(b)
                ua, ub = unit(sub(pa, pv)), unit(sub(pb, pv))
                p1 = add(pv, mul(ua, size)); p3 = add(pv, mul(ub, size)); p2 = add(p1, mul(ub, size))
                out.append(f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" stroke-width="{s * 0.8}"/>')
            elif kind == "arc":
                v, a, b, r, label, gap, double, italic = d
                pv, pa, pb = T(v), T(a), T(b)
                a0 = math.atan2(pa[1] - pv[1], pa[0] - pv[0]); a1 = math.atan2(pb[1] - pv[1], pb[0] - pv[0])
                sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
                for rr in ([r, r + 7] if double else [r]):
                    s0 = add(pv, (rr * math.cos(a0), rr * math.sin(a0)))
                    s1 = add(pv, (rr * math.cos(a0 + sweep), rr * math.sin(a0 + sweep)))
                    out.append(f'<path d="M{s0[0]:.1f},{s0[1]:.1f} A{rr},{rr} 0 0 {1 if sweep > 0 else 0} {s1[0]:.1f},{s1[1]:.1f}" stroke-width="{s * 0.8}"/>')
                if label:
                    am = a0 + sweep / 2
                    fs = self.font * 0.9
                    tw = 0.56 * fs * vis_len(label); th = 0.8 * fs
                    dx, dy = math.cos(am), math.sin(am)
                    reach = min(tw / 2 / max(abs(dx), 1e-3), th / 2 / max(abs(dy), 1e-3))
                    rr = r + gap + reach
                    out.append(txt(pv[0] + dx * rr, pv[1] + dy * rr, label, italic, fs))
            elif kind == "pxtext":
                p, string, dx, dy, italic, size = d
                x, y = T(p)
                out.append(txt(x + dx, y - dy, string, italic, size or self.font))
            elif kind == "anglemark":
                v, a, b, r, label, double, italic, at, pad, size, arc = d
                pv, pa, pb = T(v), T(a), T(b)
                a0 = math.atan2(pa[1] - pv[1], pa[0] - pv[0]); a1 = math.atan2(pb[1] - pv[1], pb[0] - pv[0])
                sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
                if arc:
                    for rr in ([r, r + 7] if double else [r]):
                        s0 = add(pv, (rr * math.cos(a0), rr * math.sin(a0)))
                        s1 = add(pv, (rr * math.cos(a0 + sweep), rr * math.sin(a0 + sweep)))
                        out.append(f'<path d="M{s0[0]:.1f},{s0[1]:.1f} A{rr},{rr} 0 0 {1 if sweep > 0 else 0} {s1[0]:.1f},{s1[1]:.1f}" stroke-width="{s * 0.8}"/>')
                fs = size or self.font * 0.9
                tw = markup_width(label, fs, italic) if "<" in label else 0.56 * fs * len(label)
                th = 0.75 * fs
                am = a0 + sweep * at
                dx, dy = math.cos(am), math.sin(am)
                rays = [(math.cos(a0), math.sin(a0)), (math.cos(a0 + sweep), math.sin(a0 + sweep))]
                dist = r
                for _ in range(2000):
                    cx, cy = pv[0] + dx * dist, pv[1] + dy * dist
                    x0, x1, y0, y1 = cx - tw / 2 - pad, cx + tw / 2 + pad, cy - th / 2 - pad, cy + th / 2 + pad
                    hit = any(x0 <= pv[0] + u[0] * t <= x1 and y0 <= pv[1] + u[1] * t <= y1
                              for u in rays for t in range(0, 2000, 2))
                    near = math.hypot(max(x0 + pad - pv[0], 0, pv[0] - x1 + pad), max(y0 + pad - pv[1], 0, pv[1] - y1 + pad))
                    if not hit and near > r + (7 if double else 0) + 4:
                        break
                    dist += 1
                out.append(txt(cx, cy, label, italic, fs))
            elif kind == "dim":
                a, b, string, italic = d
                pa, pb = T(a), T(b)
                u = unit(sub(pb, pa)); nrm = (-u[1], u[0]); m = mid(pa, pb)
                fs = self.font
                half = 0.32 * fs * vis_len(string) + 10
                for p, q in ((pa, sub(m, mul(u, half))), (pb, add(m, mul(u, half)))):
                    out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke-width="{s * 0.6}"/>')
                for p in (pa, pb):
                    e1, e2 = add(p, mul(nrm, 9)), sub(p, mul(nrm, 9))
                    out.append(f'<line x1="{e1[0]:.1f}" y1="{e1[1]:.1f}" x2="{e2[0]:.1f}" y2="{e2[1]:.1f}" stroke-width="{s * 0.6}"/>')
                out.append(txt(m[0], m[1], string, italic, fs))
            elif kind == "ticks":
                a, b, n, size = d
                pa, pb = T(a), T(b)
                u = unit(sub(pb, pa)); nrm = (-u[1], u[0]); m = mid(pa, pb)
                for i in range(n):
                    c = add(m, mul(u, (i - (n - 1) / 2) * 8))
                    p1, p2 = add(c, mul(nrm, size)), sub(c, mul(nrm, size))
                    out.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke-width="{s * 0.8}"/>')
            elif kind == "arrows":
                a, b, n, at, size = d
                pa, pb = T(a), T(b)
                u = unit(sub(pb, pa)); nrm = (-u[1], u[0])
                base = add(pa, mul(sub(pb, pa), at))
                for i in range(n):
                    tip = add(base, mul(u, i * 11))
                    p1 = add(sub(tip, mul(u, size)), mul(nrm, size * 0.7)); p2 = sub(sub(tip, mul(u, size)), mul(nrm, size * 0.7))
                    out.append(f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" stroke-width="{s * 0.8}"/>')
        out.append("</g></svg>")
        return "\n".join(out)

    def save(self, path, png=None):
        data = self.svg()
        open(path, "w").write(data)
        if png:
            import cairosvg
            cairosvg.svg2png(bytestring=data.encode(), write_to=png, output_width=self.W * 2, output_height=self.H * 2)


def fmt(x):
    return str(int(x)) if abs(x - round(x)) < 1e-9 else f"{x:g}"


def vis_len(s):
    """Number of visible characters in a label (ignores <tspan> markup from var())."""
    import re
    return len(re.sub(r"<[^>]*>", "", s))


def var(s):
    """Make single-letter variables italic inside an upright label, e.g. var("(3x+10)°").
    Letters next to other letters (words) stay upright."""
    import re
    return re.sub(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", r'<tspan font-style="italic">\1</tspan>', s)


def markup_width(s, size, italic=False):
    """Rendered width in pixels of a label that may hold var() markup."""
    import re
    parts = re.split(r'(<tspan font-style="italic">[^<]*</tspan>)', s)
    try:
        from PIL import ImageFont
        reg = ImageFont.truetype("LiberationSans-Italic.ttf" if italic else "LiberationSans-Regular.ttf", 100)
        ita = ImageFont.truetype("LiberationSans-Italic.ttf", 100)
        w = 0.0
        for p in parts:
            m = re.match(r'<tspan font-style="italic">([^<]*)</tspan>', p)
            w += (ita.getlength(m.group(1)) if m else reg.getlength(re.sub(r"<[^>]*>", "", p))) * size / 100
        return w
    except Exception:
        return 0.56 * size * vis_len(s)
