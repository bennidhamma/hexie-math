package com.hexie.math.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.text.TextMeasurer
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.hexie.math.questions.Diagram
import kotlin.math.atan2
import kotlin.math.ceil
import kotlin.math.cos
import kotlin.math.max
import kotlin.math.min
import kotlin.math.sin
import kotlin.math.tan

private val Ink = Color(0xFF3A2F4A)
private val GridColor = Color(0xFFE9E1F0)
private val AxisColor = Color(0xFF9A8FA6)
private val Fill = Color(0x227B4FA0)
private val Accent = Color(0xFF7B4FA0)
private val Unknown = Color(0xFFD9652B)
private val Gold = Color(0xFFF4C24F)
private val Slice = Color(0xFFEBDDF7)
private val Garden = Color(0x335E9E52)
private val Leg = Color(0xFF5E9E52)

private val MARBLE_COLORS = mapOf(
    "red" to Color(0xFFE5566B), "blue" to Color(0xFF4F8FE0),
    "green" to Color(0xFF5DB36A), "purple" to Color(0xFF9B6BD0),
)

/** Draws a [Diagram]. A label that is exactly "?" is orange, to mark the unknown. */
@Composable
fun DiagramView(diagram: Diagram, modifier: Modifier = Modifier) {
    val tm = rememberTextMeasurer()
    val height = when (diagram) {
        is Diagram.Plane, is Diagram.UnitCircle -> 280.dp
        is Diagram.Marbles -> 16.dp + 36.dp * diagram.groups.size
        is Diagram.Rectangle -> 170.dp
        is Diagram.ParallelLines -> 200.dp
        else -> 220.dp
    }
    Canvas(modifier.fillMaxWidth().height(height)) {
        val pen = Pen(this, tm)
        when (diagram) {
            is Diagram.Triangle -> pen.triangle(diagram)
            is Diagram.ParallelLines -> pen.parallel(diagram)
            is Diagram.Rectangle -> pen.rectangle(diagram)
            is Diagram.Cylinder -> pen.cylinder(diagram)
            is Diagram.Circle -> pen.circle(diagram)
            is Diagram.Plane -> pen.plane(diagram)
            is Diagram.UnitCircle -> pen.unitCircle(diagram)
            is Diagram.Spinner -> pen.spinner(diagram)
            is Diagram.Marbles -> pen.marbles(diagram)
            is Diagram.Polygon -> pen.polygon(diagram)
        }
    }
}

private operator fun Offset.times(k: Double) = Offset((x * k).toFloat(), (y * k).toFloat())
private fun Offset.unit(): Offset { val d = getDistance(); return if (d == 0f) this else this / d }
private fun angleOf(o: Offset) = Math.toDegrees(atan2(o.y.toDouble(), o.x.toDouble())).toFloat()
/** Screen direction for a math angle (counterclockwise, y up). */
private fun dirOf(mathDeg: Double) = Offset(cos(Math.toRadians(mathDeg)).toFloat(), -sin(Math.toRadians(mathDeg)).toFloat())

/** Drawing helpers. [u] is one dp in pixels, so sizes look the same on every screen. */
private class Pen(val ds: DrawScope, val tm: TextMeasurer) {
    val u = ds.density
    val w get() = ds.size.width
    val h get() = ds.size.height
    val thick get() = 2.2f * u
    val thin get() = 1.4f * u

    /**
     * Draws [text] near [anchor]. With [push], the label sits on that side of the anchor,
     * so its nearest edge is [gap] dp away and it never covers the anchor.
     */
    fun label(text: String, anchor: Offset, push: Offset = Offset.Zero, gap: Float = 6f, sp: Int = 15, plate: Boolean = true, bold: Boolean = true) {
        val r = tm.measure(text, TextStyle(fontSize = sp.sp, fontWeight = if (bold) FontWeight.Bold else FontWeight.Normal, color = if (text == "?") Unknown else Ink))
        val tw = r.size.width.toFloat(); val th = r.size.height.toFloat()
        val d = push.unit()
        // Move the center so the box edge, not the center, is gap dp from the anchor.
        val reach = if (d == Offset.Zero) 0f else min(tw / 2 / maxOf(kotlin.math.abs(d.x), 0.001f), th / 2 / maxOf(kotlin.math.abs(d.y), 0.001f))
        val c = anchor + d * (reach + gap * u)
        val x = (c.x - tw / 2).coerceIn(2f, w - tw - 2f)
        val y = (c.y - th / 2).coerceIn(2f, h - th - 2f)
        if (plate) ds.drawRoundRect(Color(0xEEFFFFFF), Offset(x - 3 * u, y), Size(tw + 6 * u, th), CornerRadius(6 * u))
        ds.drawText(r, topLeft = Offset(x, y))
    }

    /** Arc at [v] between the rays toward [p1] and [p2]. Returns the bisector direction. */
    fun arc(v: Offset, p1: Offset, p2: Offset, radiusDp: Float, color: Color): Offset {
        val u1 = (p1 - v).unit(); val u2 = (p2 - v).unit()
        val a1 = angleOf(u1)
        var sweep = angleOf(u2) - a1
        while (sweep > 180f) sweep -= 360f
        while (sweep < -180f) sweep += 360f
        val r = radiusDp * u
        ds.drawArc(color, a1, sweep, false, v - Offset(r, r), Size(2 * r, 2 * r), style = Stroke(2f * u))
        return (u1 + u2).unit()
    }

    fun dashed() = PathEffect.dashPathEffect(floatArrayOf(6 * u, 4 * u))

    // ------------------------------------------------------------ triangle

    fun triangle(t: Diagram.Triangle) {
        val angC = 180.0 - t.angleA - t.angleB
        fun rad(d: Double) = Math.toRadians(d)
        // Math coordinates: A at the origin, B on the x-axis, C above. Side lengths from the law of sines.
        val c = sin(rad(angC)); val b = sin(rad(t.angleB))
        val px = listOf(0.0, c, b * cos(rad(t.angleA)))
        val py = listOf(0.0, 0.0, b * sin(rad(t.angleA)))
        val padX = 58 * u; val padY = 34 * u
        val bw = px.max() - px.min(); val bh = py.max() - py.min()
        val k = min((w - 2 * padX) / bw, (h - 2 * padY) / bh)
        val ox = (w - bw * k) / 2 - px.min() * k
        val oy = (h + bh * k) / 2
        val pts = px.indices.map { Offset((ox + px[it] * k).toFloat(), (oy - py[it] * k).toFloat()) }
        val (A, B, C) = pts
        val g = (A + B + C) / 3f

        val path = Path().apply { moveTo(A.x, A.y); lineTo(B.x, B.y); lineTo(C.x, C.y); close() }
        ds.drawPath(path, Fill)
        ds.drawPath(path, Ink, style = Stroke(thick))

        fun side(p: Offset, q: Offset, text: String?) {
            text ?: return
            val mid = (p + q) / 2f
            // Outward normal of the side
            var n = Offset(-(q - p).y, (q - p).x).unit()
            if ((n.x * (mid - g).x + n.y * (mid - g).y) < 0) n = n * -1.0
            label(text, mid, push = n, gap = 4f)
        }
        side(B, C, t.sideA); side(A, C, t.sideB); side(A, B, t.sideC)

        fun corner(v: Offset, p: Offset, q: Offset, deg: Double, text: String?, name: String) {
            if (t.vertexNames) label(name, v, push = v - g, gap = 3f, sp = 14, plate = false)
            text ?: return
            val color = if (text == "?") Unknown else Accent
            val arcR = if (deg > 100) 16f else 22f
            val dir = arc(v, p, q, arcR, color)
            // Narrow corners need the label farther in, so it fits between the two sides.
            val gap = (arcR + 2f) + (if (deg < 50) (12.0 / tan(Math.toRadians(deg / 2))).toFloat().coerceAtMost(40f) else 0f)
            label(text, v + dir * (gap * u).toDouble(), push = dir, gap = 0f, sp = 14)
        }
        corner(A, B, C, t.angleA, t.labelA, "A")
        corner(B, A, C, t.angleB, t.labelB, "B")
        corner(C, A, B, angC, t.labelC, "C")
    }

    // ------------------------------------------------------------ parallel lines

    fun parallel(p: Diagram.ParallelLines) {
        // θ is the transversal's angle above horizontal (math orientation).
        val theta = (if (p.sameSide) 180.0 - p.angle1 else p.angle1).coerceIn(30.0, 150.0)
        val y1 = h * 0.28f; val y2 = h * 0.74f
        val cx = w / 2
        val dx = ((y2 - y1) / tan(Math.toRadians(theta)) / 2).toFloat()
        val p1 = Offset(cx + dx, y1); val p2 = Offset(cx - dx, y2)
        val m = 12 * u
        ds.drawLine(Ink, Offset(m, y1), Offset(w - m, y1), thick)
        ds.drawLine(Ink, Offset(m, y2), Offset(w - m, y2), thick)
        val dir = dirOf(theta)
        ds.drawLine(Ink, p2 - dir * (40 * u), p1 + dir * (40 * u), thick, StrokeCap.Round)
        // Arrowheads mark the lines as parallel.
        for (y in listOf(y1, y2)) {
            val x = w - 34 * u; val a = 5 * u
            ds.drawLine(Ink, Offset(x - a, y - a), Offset(x, y), thin)
            ds.drawLine(Ink, Offset(x - a, y + a), Offset(x, y), thin)
        }
        fun mark(v: Offset, from: Double, span: Double, text: String) {
            val r = 18 * u
            ds.drawArc(Accent, (-(from + span)).toFloat(), span.toFloat(), false, v - Offset(r, r), Size(2 * r, 2 * r), style = Stroke(2.5f * u))
            val mid = dirOf(from + span / 2)
            label(text, v + mid * (r + 4 * u).toDouble(), push = mid, gap = 0f, sp = 14)
        }
        if (p.sameSide) mark(p1, 180.0 + theta, 180.0 - theta, p.label1)  // top crossing, right of transversal
        else mark(p1, 180.0, theta, p.label1)                              // top crossing, left of transversal
        mark(p2, 0.0, theta, p.label2)                                     // bottom crossing, right of transversal
    }

    // ------------------------------------------------------------ rectangle, cylinder, circle

    fun rectangle(r: Diagram.Rectangle) {
        val k = min(w * 0.6f / r.width, h * 0.62f / r.height).toFloat()
        val rw = (r.width * k).toFloat(); val rh = (r.height * k).toFloat()
        val tl = Offset((w - rw) / 2, (h - rh) / 2 - 8 * u)
        ds.drawRect(Garden, tl, Size(rw, rh))
        ds.drawRect(Ink, tl, Size(rw, rh), style = Stroke(thick))
        label(r.widthLabel, Offset(tl.x + rw / 2, tl.y + rh), push = Offset(0f, 1f))
        label(r.heightLabel, Offset(tl.x + rw, tl.y + rh / 2), push = Offset(1f, 0f))
    }

    fun cylinder(c: Diagram.Cylinder) {
        val cw = min(w * 0.42f, 150 * u); val eh = cw * 0.3f
        val top = 14 * u; val bottom = h - 14 * u
        val left = (w - cw) / 2; val right = left + cw; val cx = w / 2
        ds.drawRect(Fill, Offset(left, top + eh / 2), Size(cw, bottom - top - eh))
        ds.drawOval(Fill, Offset(left, bottom - eh), Size(cw, eh))
        ds.drawLine(Ink, Offset(left, top + eh / 2), Offset(left, bottom - eh / 2), thick)
        ds.drawLine(Ink, Offset(right, top + eh / 2), Offset(right, bottom - eh / 2), thick)
        ds.drawArc(Ink, 0f, 180f, false, Offset(left, bottom - eh), Size(cw, eh), style = Stroke(thick))
        ds.drawArc(Ink, 180f, 180f, false, Offset(left, bottom - eh), Size(cw, eh), style = Stroke(thin, pathEffect = dashed()))
        ds.drawOval(Color(0x337B4FA0), Offset(left, top), Size(cw, eh))
        ds.drawOval(Ink, Offset(left, top), Size(cw, eh), style = Stroke(thick))
        val center = Offset(cx, top + eh / 2)
        ds.drawCircle(Ink, 3 * u, center)
        ds.drawLine(Accent, center, Offset(right, center.y), thick)
        label(c.radiusLabel, Offset(cx + cw / 4, center.y + eh / 2), push = Offset(0f, 1f), gap = 4f)
        // Height bracket on the right
        val bx = right + 10 * u
        ds.drawLine(Accent, Offset(bx, center.y), Offset(bx, bottom - eh / 2), thin)
        label(c.heightLabel, Offset(bx, (center.y + bottom - eh / 2) / 2), push = Offset(1f, 0f))
    }

    fun circle(c: Diagram.Circle) {
        val r = min(w, h) * 0.36f
        val center = Offset(w / 2, h / 2 - 12 * u)
        ds.drawCircle(Fill, r, center)
        ds.drawCircle(Ink, r, center, style = Stroke(thick))
        ds.drawCircle(Ink, 3 * u, center)
        ds.drawLine(Accent, center, center + Offset(r, 0f), thick, pathEffect = dashed())
        label(c.radiusLabel, center + Offset(r / 2, 0f), push = Offset(0f, -1f))
        label(c.caption, Offset(center.x, center.y + r), push = Offset(0f, 1f), sp = 14)
    }

    // ------------------------------------------------------------ coordinate plane

    fun plane(p: Diagram.Plane) {
        val pad = 8 * u
        val pw = w - 2 * pad; val ph = h - 2 * pad
        val xs = p.points.map { it.x } + 0; val ys = p.points.map { it.y } + 0
        val rx0 = xs.min() - 1.5; val rx1 = xs.max() + 1.5
        val ry0 = ys.min() - 1.5; val ry1 = ys.max() + 1.5
        // One scale for both axes, so slopes and right angles look true.
        val k = min(pw / (rx1 - rx0), ph / (ry1 - ry0))
        val xr = pw / k; val yr = ph / k
        val x0 = (rx0 + rx1) / 2 - xr / 2; val x1 = x0 + xr
        val y0 = (ry0 + ry1) / 2 - yr / 2; val y1 = y0 + yr
        fun sx(x: Double) = (pad + (x - x0) * k).toFloat()
        fun sy(y: Double) = (pad + (y1 - y) * k).toFloat()
        val step = listOf(1, 2, 5, 10).first { max(xr, yr) / it <= 16 }

        var gx = ceil(x0 / step) * step
        while (gx <= x1) { ds.drawLine(GridColor, Offset(sx(gx), pad), Offset(sx(gx), pad + ph), 1f * u); gx += step }
        var gy = ceil(y0 / step) * step
        while (gy <= y1) { ds.drawLine(GridColor, Offset(pad, sy(gy)), Offset(pad + pw, sy(gy)), 1f * u); gy += step }
        ds.drawLine(AxisColor, Offset(pad, sy(0.0)), Offset(pad + pw, sy(0.0)), 1.6f * u)
        ds.drawLine(AxisColor, Offset(sx(0.0), pad), Offset(sx(0.0), pad + ph), 1.6f * u)
        label("x", Offset(pad + pw, sy(0.0)), push = Offset(-0.4f, -1f), sp = 13, plate = false, bold = false)
        label("y", Offset(sx(0.0), pad), push = Offset(1f, 0.3f), sp = 13, plate = false, bold = false)
        label("$step", Offset(sx(step.toDouble()), sy(0.0)), push = Offset(0f, 1f), gap = 2f, sp = 11, plate = false, bold = false)

        ds.clipRect(pad, pad, pad + pw, pad + ph) {
            for (l in p.lines) {
                drawLine(Accent, Offset(sx(x0), sy(l.m * x0 + l.b)), Offset(sx(x1), sy(l.m * x1 + l.b)), 2.5f * u)
            }
        }
        for (l in p.lines) {
            val text = l.label ?: continue
            // Put the label where the line is inside the grid, toward the right.
            val lx = (x0 + xr * 0.78).let { x -> if (l.m * x + l.b in y0..y1) x else (((if (l.m > 0) y1 else y0) - l.b) / l.m - xr * 0.05) }
            label(text, Offset(sx(lx), sy(l.m * lx + l.b)), push = Offset(0.35f, -1f), gap = 4f, sp = 13)
        }
        for (pt in p.points) {
            val c = Offset(sx(pt.x.toDouble()), sy(pt.y.toDouble()))
            ds.drawCircle(Unknown, 5 * u, c)
            ds.drawCircle(Color.White, 2 * u, c)
            label("(${m(pt.x)}, ${m(pt.y)})", c, push = Offset(0.25f, -1f), gap = 4f, sp = 13)
        }
    }

    private fun m(n: Int) = if (n < 0) "−${-n}" else "$n"

    // ------------------------------------------------------------ unit circle

    fun unitCircle(c: Diagram.UnitCircle) {
        val center = Offset(w / 2, h / 2)
        val r = min(w, h) * 0.38f
        ds.drawLine(AxisColor, Offset(center.x - r - 16 * u, center.y), Offset(center.x + r + 16 * u, center.y), 1.4f * u)
        ds.drawLine(AxisColor, Offset(center.x, center.y - r - 12 * u), Offset(center.x, center.y + r + 12 * u), 1.4f * u)
        ds.drawCircle(Ink, r, center, style = Stroke(thick))
        listOf("I" to 45.0, "II" to 135.0, "III" to 225.0, "IV" to 315.0).forEach { (n, a) ->
            label(n, center + dirOf(a) * (r * 1.08).toDouble(), sp = 12, plate = false, bold = false)
        }

        val tip = center + dirOf(c.degrees) * r.toDouble()
        c.legs?.let { (opp, adj, hyp) ->
            val foot = Offset(tip.x, center.y)
            val tri = Path().apply { moveTo(center.x, center.y); lineTo(tip.x, tip.y); lineTo(foot.x, foot.y); close() }
            ds.drawPath(tri, Fill)
            ds.drawLine(Unknown, tip, foot, 2.5f * u)
            ds.drawLine(Leg, center, foot, 2.5f * u)
            // Right-angle box at the foot
            val sx = if (foot.x > center.x) -1f else 1f
            val sy = if (tip.y < center.y) -1f else 1f
            val b = 7 * u
            ds.drawLine(Ink, foot + Offset(sx * b, 0f), foot + Offset(sx * b, sy * b), 1.2f * u)
            ds.drawLine(Ink, foot + Offset(sx * b, sy * b), foot + Offset(0f, sy * b), 1.2f * u)
            label(opp, (tip + foot) / 2f, push = Offset(-sx, 0f))
            label(adj, (center + foot) / 2f, push = Offset(0f, -sy))
            var n = Offset(-(tip - center).y, (tip - center).x).unit()
            val inward = (foot - (center + tip) / 2f)
            if (n.x * inward.x + n.y * inward.y > 0) n = n * -1.0
            label(hyp, (center + tip) / 2f, push = n)
        }
        ds.drawLine(Accent, center, tip, 3f * u, StrokeCap.Round)
        ds.drawCircle(Accent, 4.5f * u, tip)
        // Angle arc from the positive x-axis, counterclockwise
        val ar = 20 * u
        ds.drawArc(Unknown, 0f, -c.degrees.toFloat(), false, center - Offset(ar, ar), Size(2 * ar, 2 * ar), style = Stroke(2f * u))
        val mid = dirOf(c.degrees / 2)
        label(c.angleLabel, center + mid * (ar + 2 * u).toDouble(), push = mid, gap = 0f, sp = 14)
    }

    // ------------------------------------------------------------ spinner, marbles, polygon

    fun spinner(s: Diagram.Spinner) {
        val center = Offset(w / 2, h / 2)
        val r = min(w, h) * 0.45f
        val sweep = 360f / s.sections
        val box = Size(2 * r, 2 * r); val tl = center - Offset(r, r)
        for (i in 0 until s.sections) {
            val start = -90f + i * sweep
            ds.drawArc(if (i < s.marked) Gold else Slice, start, sweep, true, tl, box)
            ds.drawArc(Ink, start, sweep, true, tl, box, style = Stroke(thin))
            if (i < s.marked) {
                val mid = Math.toRadians((start + sweep / 2).toDouble())
                label(s.icon, center + Offset(cos(mid).toFloat(), sin(mid).toFloat()) * (r * 0.64f), sp = 18, plate = false)
            }
        }
        ds.drawCircle(Ink, r, center, style = Stroke(thick))
        ds.drawLine(Ink, center, center + Offset(r * 0.5f, -r * 0.32f), 4 * u, StrokeCap.Round)
        ds.drawCircle(Ink, 6 * u, center)
    }

    fun marbles(m: Diagram.Marbles) {
        val row = 36 * u; val r = 10 * u
        m.groups.forEachIndexed { i, (color, count) ->
            val y = 8 * u + row * i + row / 2
            label("$count $color", Offset(4 * u, y), push = Offset(1f, 0f), gap = 0f, sp = 14, plate = false)
            for (j in 0 until count) {
                val c = Offset(96 * u + j * (2 * r + 5 * u), y)
                ds.drawCircle(MARBLE_COLORS[color] ?: Ink, r, c)
                ds.drawCircle(Color(0x88FFFFFF), r * 0.32f, c + Offset(-r * 0.35f, -r * 0.35f))
            }
        }
    }

    fun polygon(p: Diagram.Polygon) {
        val center = Offset(w / 2, h / 2)
        val r = min(w, h) * 0.44f
        // One flat side at the bottom.
        val start = Math.PI / 2 + Math.PI / p.sides
        val pts = List(p.sides) { i ->
            val a = start + 2 * Math.PI * i / p.sides
            center + Offset(cos(a).toFloat(), sin(a).toFloat()) * r
        }
        val path = Path().apply { moveTo(pts[0].x, pts[0].y); pts.drop(1).forEach { lineTo(it.x, it.y) }; close() }
        ds.drawPath(path, Fill)
        ds.drawPath(path, Ink, style = Stroke(thick))
        val v = pts[0]
        val dir = arc(v, pts[1], pts[p.sides - 1], 22f, Unknown)
        label(p.angleLabel, v + dir * (26 * u).toDouble(), push = dir, gap = 0f)
    }
}
