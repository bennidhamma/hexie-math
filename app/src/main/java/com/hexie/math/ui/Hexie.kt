package com.hexie.math.ui

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.graphics.drawscope.withTransform
import androidx.compose.ui.graphics.StrokeCap

enum class Mood { HAPPY, CHEER, OOPS, THINK }

private val Skin = Color(0xFFB8E2A6)
private val SkinShade = Color(0xFF8FC783)
private val Wart = Color(0xFF79B06E)
private val Hat = Color(0xFF6B3FA0)
private val HatDark = Color(0xFF52307D)
private val Band = Color(0xFFF4C24F)
private val Hair = Color(0xFFD9CCF2)
private val HairShade = Color(0xFFBBA8E3)
private val Cheek = Color(0xFFF79BB4)
private val Ink = Color(0xFF2E2240)
private val Cloak = Color(0xFF3F2A63)
private val Sparkle = Color(0xFFFFD45C)

/** Hexie, a small and very friendly hag. Drawn on a 200 × 200 grid and scaled to fit. */
@Composable
fun Hexie(mood: Mood, modifier: Modifier = Modifier) {
    val t = rememberInfiniteTransition(label = "hexie")
    val bob by t.animateFloat(
        0f, 1f,
        infiniteRepeatable(tween(1400, easing = LinearEasing), RepeatMode.Reverse), label = "bob",
    )
    val twinkle by t.animateFloat(
        0f, 1f,
        infiniteRepeatable(tween(700, easing = LinearEasing), RepeatMode.Reverse), label = "twinkle",
    )
    Canvas(modifier) {
        val s = size.minDimension / 200f
        val dx = (size.width - 200f * s) / 2f
        val dy = (size.height - 200f * s) / 2f
        withTransform({
            translate(dx, dy)
            scale(s, s, Offset.Zero)
        }) {
            val lift = if (mood == Mood.CHEER) -6f * bob else -3f * bob
            translate(0f, lift) { drawHexie(mood) }
            if (mood == Mood.CHEER) drawSparkles(twinkle)
        }
    }
}

private fun DrawScope.drawHexie(mood: Mood) {
    // Cloak, cut off at the bottom of the 200 × 200 box
    clipRect(0f, 0f, 200f, 196f) {
        drawOval(Cloak, Offset(50f, 156f), Size(100f, 70f))
    }
    drawCircle(Band, 5f, Offset(100f, 168f))

    // Hair poking out at the sides
    for ((x, y, r) in listOf(Triple(56f, 104f, 16f), Triple(50f, 124f, 13f), Triple(58f, 142f, 11f))) {
        drawCircle(HairShade, r + 1.5f, Offset(x, y + 1.5f))
        drawCircle(Hair, r, Offset(x, y))
        drawCircle(HairShade, r + 1.5f, Offset(200f - x, y + 1.5f))
        drawCircle(Hair, r, Offset(200f - x, y))
    }

    // Pointy ears
    val earL = Path().apply { moveTo(58f, 116f); lineTo(42f, 104f); lineTo(60f, 130f); close() }
    val earR = Path().apply { moveTo(142f, 116f); lineTo(158f, 104f); lineTo(140f, 130f); close() }
    drawPath(earL, Skin); drawPath(earR, Skin)

    // Face
    drawCircle(SkinShade, 49f, Offset(100f, 122f))
    drawCircle(Skin, 47f, Offset(100f, 120f))

    // Cheeks
    drawOval(Cheek.copy(alpha = 0.75f), Offset(62f, 128f), Size(18f, 11f))
    drawOval(Cheek.copy(alpha = 0.75f), Offset(120f, 128f), Size(18f, 11f))

    drawEyes(mood)
    drawNose()
    drawMouth(mood)
    if (mood == Mood.OOPS) {
        // Sweat drop
        val drop = Path().apply {
            moveTo(146f, 92f)
            quadraticTo(152f, 102f, 146f, 106f)
            quadraticTo(140f, 102f, 146f, 92f)
        }
        drawPath(drop, Color(0xFF8FD3F4))
    }

    drawHat()
}

private fun DrawScope.drawEyes(mood: Mood) {
    val ly = 110f
    when (mood) {
        Mood.CHEER -> {
            // Happy closed eyes: ^ ^
            for (x in listOf(82f, 118f)) {
                val p = Path().apply { moveTo(x - 8f, ly + 3f); quadraticTo(x, ly - 8f, x + 8f, ly + 3f) }
                drawPath(p, Ink, style = Stroke(4f, cap = StrokeCap.Round))
            }
        }
        else -> {
            val look = if (mood == Mood.THINK) Offset(3f, -3f) else Offset.Zero
            for (x in listOf(82f, 118f)) {
                drawOval(Ink, Offset(x - 8f + look.x, ly - 10f + look.y), Size(16f, 20f))
                drawCircle(Color.White, 3.6f, Offset(x - 2.5f + look.x, ly - 4.5f + look.y))
                drawCircle(Color.White, 1.8f, Offset(x + 3f + look.x, ly + 4f + look.y))
            }
            if (mood == Mood.OOPS) {
                // Worried brows
                drawLine(Ink, Offset(72f, 94f), Offset(88f, 90f), 3f, StrokeCap.Round)
                drawLine(Ink, Offset(128f, 94f), Offset(112f, 90f), 3f, StrokeCap.Round)
            }
            if (mood == Mood.THINK) {
                drawLine(Ink, Offset(110f, 90f), Offset(126f, 92f), 3f, StrokeCap.Round)
            }
        }
    }
}

private fun DrawScope.drawNose() {
    // A cute hooked hag nose with one wart
    val nose = Path().apply {
        moveTo(96f, 112f)
        quadraticTo(110f, 122f, 106f, 134f)
        quadraticTo(100f, 138f, 94f, 132f)
        quadraticTo(92f, 122f, 96f, 112f)
        close()
    }
    drawPath(nose, SkinShade)
    drawCircle(Wart, 2.6f, Offset(103f, 124f))
}

private fun DrawScope.drawMouth(mood: Mood) {
    when (mood) {
        Mood.HAPPY -> {
            val smile = Path().apply { moveTo(84f, 142f); quadraticTo(100f, 156f, 116f, 142f) }
            drawPath(smile, Ink, style = Stroke(3.5f, cap = StrokeCap.Round))
            // Snaggle tooth
            drawRect(Color.White, Offset(104f, 145f), Size(5f, 5f))
        }
        Mood.CHEER -> {
            val open = Path().apply {
                moveTo(84f, 140f); quadraticTo(100f, 166f, 116f, 140f); close()
            }
            drawPath(open, Ink)
            drawOval(Color(0xFFE5677F), Offset(93f, 148f), Size(14f, 8f))
            drawRect(Color.White, Offset(103f, 140f), Size(5f, 5f))
        }
        Mood.OOPS -> {
            val wobble = Path().apply {
                moveTo(88f, 148f); quadraticTo(94f, 142f, 100f, 148f); quadraticTo(106f, 154f, 112f, 148f)
            }
            drawPath(wobble, Ink, style = Stroke(3.5f, cap = StrokeCap.Round))
        }
        Mood.THINK -> {
            drawLine(Ink, Offset(92f, 147f), Offset(110f, 144f), 3.5f, StrokeCap.Round)
        }
    }
}

private fun DrawScope.drawHat() {
    // Brim
    drawOval(HatDark, Offset(34f, 72f), Size(132f, 26f))
    drawOval(Hat, Offset(34f, 70f), Size(132f, 24f))
    // Cone, tilted with a floppy tip
    rotate(-8f, Offset(100f, 80f)) {
        val cone = Path().apply {
            moveTo(64f, 82f)
            lineTo(92f, 20f)
            quadraticTo(100f, 4f, 122f, 10f)
            quadraticTo(108f, 18f, 106f, 30f)
            lineTo(136f, 82f)
            close()
        }
        drawPath(cone, Hat)
        // Band and buckle
        val band = Path().apply {
            moveTo(66f, 78f); lineTo(134f, 78f); lineTo(129f, 66f); lineTo(71f, 66f); close()
        }
        drawPath(band, Band)
        drawRect(HatDark, Offset(93f, 66f), Size(14f, 12f))
        drawRect(Band, Offset(96f, 69f), Size(8f, 6f))
        // Little star on the hat
        drawStar(Offset(110f, 44f), 6f, Band)
    }
}

private fun DrawScope.drawSparkles(phase: Float) {
    val spots = listOf(Offset(26f, 60f), Offset(176f, 52f), Offset(170f, 150f), Offset(30f, 156f))
    spots.forEachIndexed { i, p ->
        val grow = if (i % 2 == 0) phase else 1f - phase
        drawStar(p, 5f + 5f * grow, Sparkle)
    }
}

private fun DrawScope.drawStar(c: Offset, r: Float, color: Color) {
    val p = Path()
    for (i in 0 until 8) {
        val radius = if (i % 2 == 0) r else r * 0.38f
        val a = Math.toRadians((i * 45 - 90).toDouble())
        val x = c.x + radius * kotlin.math.cos(a).toFloat()
        val y = c.y + radius * kotlin.math.sin(a).toFloat()
        if (i == 0) p.moveTo(x, y) else p.lineTo(x, y)
    }
    p.close()
    drawPath(p, color)
}
