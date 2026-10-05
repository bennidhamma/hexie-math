package com.hexie.math.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.text.InlineTextContent
import androidx.compose.foundation.text.appendInlineContent
import androidx.compose.material3.LocalContentColor
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.takeOrElse
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.Placeholder
import androidx.compose.ui.text.PlaceholderVerticalAlign
import androidx.compose.ui.text.TextMeasurer
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.TextUnit
import androidx.compose.ui.unit.isSpecified
import androidx.compose.ui.unit.sp
import com.hexie.math.questions.Tex
import com.hexie.math.questions.TexParser
import kotlin.math.max

/**
 * Text with inline LaTeX math between \( and \). Plain text wraps as usual.
 * Each math piece is typeset and placed in the line like a small picture.
 */
@Composable
fun MathText(
    text: String,
    modifier: Modifier = Modifier,
    style: TextStyle = LocalTextStyle.current,
    color: Color = Color.Unspecified,
) {
    val ink = color.takeOrElse { style.color.takeOrElse { LocalContentColor.current } }
    val density = LocalDensity.current
    val tm = rememberTextMeasurer()
    val fontSize = if (style.fontSize.isSpecified) style.fontSize else 16.sp

    val (annotated, inline) = remember(text, fontSize, ink, density) {
        buildMath(text, fontSize, ink, density, tm, style)
    }
    // A fixed line height would clip tall math (stacked fractions). Let those lines grow to fit.
    val lineStyle = if (inline.isEmpty()) style else style.copy(lineHeight = TextUnit.Unspecified)
    Text(annotated, modifier, style = lineStyle.copy(color = ink), inlineContent = inline)
}

private fun buildMath(
    text: String,
    fontSize: TextUnit,
    ink: Color,
    density: Density,
    tm: TextMeasurer,
    style: TextStyle,
): Pair<AnnotatedString, Map<String, InlineTextContent>> {
    val inline = mutableMapOf<String, InlineTextContent>()
    val fsPx = with(density) { fontSize.toPx() }
    val typesetter = Typesetter(tm, ink, density, style.fontFamily ?: FontFamily.Default)
    val annotated = buildAnnotatedString {
        var n = 0
        for ((isMath, part) in TexParser.split(text)) {
            if (!isMath) { append(part); continue }
            TexParser.breakPoints(part).forEachIndexed { k, piece ->
                if (k > 0) append(" ")
                val box = typesetter.layout(TexParser.parse(piece), fsPx, leadingOp = k > 0)
                // Center the box on the math axis, so Placeholder TextCenter lines it up with the text.
                val axis = fsPx * AXIS
                val half = max(box.ascent - axis, box.descent + axis) + fsPx * 0.04f
                val id = "m${n++}"
                inline[id] = InlineTextContent(
                    Placeholder(
                        with(density) { (box.width + 1f).toSp() },
                        with(density) { (2 * half).toSp() },
                        PlaceholderVerticalAlign.TextCenter,
                    )
                ) {
                    Canvas(Modifier.fillMaxSize()) { box.draw(this, 0f, half + axis) }
                }
                appendInlineContent(id, piece)
            }
        }
    }
    return annotated to inline
}

/** Height of the fraction bar and the minus sign above the baseline, in em. */
private const val AXIS = 0.27f

/** A laid-out piece of math. [ascent] is above the baseline, [descent] below. Both are positive. */
private class Box(val width: Float, val ascent: Float, val descent: Float, val draw: DrawScope.(x: Float, baseline: Float) -> Unit)

private class Typesetter(val tm: TextMeasurer, val ink: Color, val density: Density, val family: FontFamily) {

    fun layout(t: Tex, fs: Float, leadingOp: Boolean = false): Box = when (t) {
        is Tex.Sym -> sym(t, fs, padLeft = !leadingOp, unary = false)
        is Tex.Space -> Box(t.em * fs, 0f, 0f) { _, _ -> }
        is Tex.Row -> row(t.items, fs, leadingOp)
        is Tex.Frac -> frac(t, fs)
        is Tex.Scripts -> scripts(t, fs)
        is Tex.Sqrt -> sqrt(t, fs)
        is Tex.Delim -> delim(t, fs)
        is Tex.Overline -> overline(t, fs)
    }

    private fun overline(o: Tex.Overline, fs: Float): Box {
        val body = layout(o.body, fs)
        val gap = fs * 0.08f
        val stroke = max(fs * 0.05f, 1f)
        return Box(body.width, body.ascent + gap + stroke, body.descent) { x, b ->
            body.draw(this, x, b)
            val y = b - body.ascent - gap
            drawLine(ink, Offset(x + fs * 0.04f, y), Offset(x + body.width - fs * 0.02f, y), stroke)
        }
    }

    private fun sym(s: Tex.Sym, fs: Float, padLeft: Boolean, unary: Boolean): Box {
        if (s.text.isEmpty()) return Box(0f, 0f, 0f) { _, _ -> }
        val style = TextStyle(
            fontSize = with(density) { fs.toSp() },
            fontStyle = if (s.italic) FontStyle.Italic else FontStyle.Normal,
            // Serif gives the look of a typeset LaTeX equation.
            fontFamily = FontFamily.Serif,
            color = ink,
        )
        val r = tm.measure(s.text, style)
        // A unary sign (−6, x = −3) hugs its number. A binary operator gets space on both sides.
        val pad = if (s.op && !unary) fs * 0.22f else if (s.italic) fs * 0.02f else 0f
        val left = if (padLeft) pad else 0f
        return Box(r.size.width + left + pad, fs * 0.74f, fs * 0.24f) { x, base ->
            drawText(r, topLeft = Offset(x + left, base - r.firstBaseline))
        }
    }

    private fun row(items: List<Tex>, fs: Float, leadingOp: Boolean): Box {
        val boxes = items.mapIndexed { i, it ->
            if (it is Tex.Sym && it.op && (it.text == "−" || it.text == "+") && isUnaryPosition(items, i, leadingOp)) sym(it, fs, padLeft = false, unary = true)
            else layout(it, fs, leadingOp = i == 0 && leadingOp)
        }
        val w = boxes.sumOf { it.width.toDouble() }.toFloat()
        val a = boxes.maxOfOrNull { it.ascent } ?: 0f
        val d = boxes.maxOfOrNull { it.descent } ?: 0f
        return Box(w, a, d) { x, base ->
            var cx = x
            for (b in boxes) { b.draw(this, cx, base); cx += b.width }
        }
    }

    /** A sign is unary at the start of a row, or right after another operator or an opening bracket. */
    private fun isUnaryPosition(items: List<Tex>, i: Int, leadingOp: Boolean): Boolean {
        if (i == 0) return !leadingOp
        val prev = items[i - 1]
        return (prev is Tex.Sym && (prev.op || prev.text in setOf("(", "[", "{", "|", ","))) ||
            prev is Tex.Space ||
            (prev is Tex.Row && prev.items.lastOrNull() is Tex.Space)  // after a comma: (−2, −3)
    }

    private fun frac(f: Tex.Frac, fs: Float): Box {
        val inner = max(fs * 0.8f, 9f * density.density)
        val num = layout(f.num, inner); val den = layout(f.den, inner)
        val pad = fs * 0.1f
        val w = max(num.width, den.width) + 2 * pad
        val gap = fs * 0.12f
        val bar = max(fs * 0.055f, 1f)
        val axis = fs * AXIS
        val ascent = axis + bar / 2 + gap + num.descent + num.ascent
        val descent = -axis + bar / 2 + gap + den.ascent + den.descent
        return Box(w + fs * 0.08f, ascent, max(descent, 0f)) { x, base ->
            val y = base - axis
            drawLine(ink, Offset(x + fs * 0.04f, y), Offset(x + fs * 0.04f + w, y), bar)
            num.draw(this, x + fs * 0.04f + (w - num.width) / 2, y - bar / 2 - gap - num.descent)
            den.draw(this, x + fs * 0.04f + (w - den.width) / 2, y + bar / 2 + gap + den.ascent)
        }
    }

    private fun scripts(s: Tex.Scripts, fs: Float): Box {
        val base = layout(s.base, fs)
        val small = max(fs * 0.7f, 8f * density.density)
        val sup = s.sup?.let { layout(it, small) }
        val sub = s.sub?.let { layout(it, small) }
        val up = max(fs * 0.4f, base.ascent - fs * 0.32f)
        val down = max(fs * 0.2f, base.descent - fs * 0.05f)
        val w = base.width + max(sup?.width ?: 0f, sub?.width ?: 0f) + fs * 0.04f
        val ascent = max(base.ascent, (sup?.let { up + it.ascent } ?: 0f))
        val descent = max(base.descent, (sub?.let { down + it.descent } ?: 0f))
        return Box(w, ascent, descent) { x, b ->
            base.draw(this, x, b)
            sup?.draw?.invoke(this, x + base.width + fs * 0.02f, b - up)
            sub?.draw?.invoke(this, x + base.width + fs * 0.02f, b + down)
        }
    }

    private fun sqrt(s: Tex.Sqrt, fs: Float): Box {
        val body = layout(s.body, fs)
        val index = s.index?.let { layout(it, max(fs * 0.55f, 8f * density.density)) }
        val gap = fs * 0.12f
        val stroke = max(fs * 0.06f, 1f)
        val hook = fs * 0.62f
        val lead = max(0f, (index?.width ?: 0f) - hook * 0.45f)
        val top = body.ascent + gap + stroke
        return Box(lead + hook + body.width + fs * 0.12f, top + stroke, body.descent + fs * 0.04f) { x, b ->
            val x0 = x + lead
            val path = Path().apply {
                moveTo(x0, b - top * 0.38f)
                lineTo(x0 + hook * 0.22f, b - top * 0.48f)
                lineTo(x0 + hook * 0.5f, b + body.descent)
                lineTo(x0 + hook * 0.92f, b - top)
                lineTo(x0 + hook + body.width + fs * 0.08f, b - top)
            }
            drawPath(path, ink, style = Stroke(stroke, cap = StrokeCap.Round, join = StrokeJoin.Round))
            body.draw(this, x0 + hook, b)
            index?.draw?.invoke(this, x, b - top * 0.5f)
        }
    }

    private fun delim(d: Tex.Delim, fs: Float): Box {
        val body = layout(d.body, fs)
        val ascent = max(body.ascent, fs * 0.74f) + fs * 0.06f
        val descent = max(body.descent, fs * 0.24f) + fs * 0.06f
        val gw = fs * 0.32f
        val lw = if (d.left.isEmpty()) 0f else gw
        val rw = if (d.right.isEmpty()) 0f else gw
        val stroke = max(fs * 0.065f, 1f)
        return Box(lw + body.width + rw, ascent, descent) { x, b ->
            drawDelim(d.left, x, gw, b - ascent, b + descent, stroke, left = true)
            body.draw(this, x + lw, b)
            drawDelim(d.right, x + lw + body.width, gw, b - ascent, b + descent, stroke, left = false)
        }
    }

    /** Draws a delimiter as a path, so it can grow to any height. */
    private fun DrawScope.drawDelim(kind: String, x: Float, w: Float, top: Float, bottom: Float, stroke: Float, left: Boolean) {
        val st = Stroke(stroke, cap = StrokeCap.Round, join = StrokeJoin.Round)
        val inner = if (left) x + w * 0.75f else x + w * 0.25f
        val outer = if (left) x + w * 0.2f else x + w * 0.8f
        when (kind) {
            "(", ")" -> {
                val p = Path().apply {
                    moveTo(inner, top)
                    cubicTo(outer, top + (bottom - top) * 0.25f, outer, top + (bottom - top) * 0.75f, inner, bottom)
                }
                drawPath(p, ink, style = st)
            }
            "[", "]" -> {
                val p = Path().apply { moveTo(inner, top); lineTo(outer, top); lineTo(outer, bottom); lineTo(inner, bottom) }
                drawPath(p, ink, style = st)
            }
            "|" -> drawLine(ink, Offset(x + w / 2, top), Offset(x + w / 2, bottom), stroke)
        }
    }
}
