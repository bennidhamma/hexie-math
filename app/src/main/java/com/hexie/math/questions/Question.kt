package com.hexie.math.questions

import kotlin.random.Random

/** One multiple-choice problem. [choices] always has 4 distinct entries, like the ACT math section. */
data class Question(
    val topic: Topic,
    val prompt: String,
    val choices: List<String>,
    val correctIndex: Int,
    val explanation: String,
    /** Optional fixed-width block (a table or a figure in text form) shown under the prompt. */
    val figure: String? = null,
    /** Drawn under the prompt. */
    val diagram: Diagram? = null,
    /** Drawn inside the explanation, after the student answers. */
    val explanationDiagram: Diagram? = null,
)

/**
 * Topics come from the "missed" rows of the March 2026 practice-test score report.
 * [baseWeight] is higher for the topics with the most misses.
 */
enum class Topic(val label: String, val baseWeight: Double) {
    PROBABILITY("Probability", 4.0),
    RATIOS("Ratios & Proportions", 3.0),
    PERCENT("Percents", 1.5),
    WORD_PROBLEMS("Word Problems", 2.0),
    EXPONENTS("Exponents & Roots", 3.0),
    REWRITING("Rewriting Equations", 2.0),
    AREA_VOLUME("Perimeter, Area & Volume", 2.0),
    SLOPE("Slope-Intercept Form", 2.0),
    ANGLES("Lines & Angles", 2.0),
    FRACTIONS("Fractions & Operations", 2.0),
    UNIT_CIRCLE("Unit Circle & Trig", 2.0),
    LOGARITHMS("Logarithms", 2.0),
    LAW_SINES_COSINES("Law of Sines & Cosines", 2.0),
}

/** Puts the correct answer and the distractors in random order. Fills gaps if distractors collide. */
internal fun buildQuestion(
    r: Random,
    topic: Topic,
    prompt: String,
    correct: String,
    distractors: List<String>,
    explanation: String,
    figure: String? = null,
    filler: (Int) -> String = { "None of these" },
): Question {
    val right = minus(correct)
    val picked = linkedSetOf(right)
    for (d in distractors) {
        if (picked.size == 4) break
        picked.add(minus(d))
    }
    var k = 0
    while (picked.size < 4) {
        picked.add(minus(filler(k++)))
        require(k < 100) { "Could not build 4 distinct choices for $topic" }
    }
    val shuffled = picked.toList().shuffled(r)
    return Question(topic, minus(prompt), shuffled, shuffled.indexOf(right), minus(explanation), figure)
}

private val HYPHEN_MINUS = Regex("(?<![\\p{L}\\d])-(?=[\\d(xπ√])")

/** Swaps a hyphen used as a negative sign for a true minus sign, so "-4" and "−4" are one choice. */
internal fun minus(s: String): String = s.replace(HYPHEN_MINUS, "−")

/** Exact fraction, always stored in lowest terms with a positive denominator. */
data class Frac(val n: Long, val d: Long) {
    companion object {
        fun of(n: Long, d: Long): Frac {
            require(d != 0L)
            val g = gcd(kotlin.math.abs(n), kotlin.math.abs(d)).coerceAtLeast(1)
            val s = if (d < 0) -1 else 1
            return Frac(s * n / g, s * d / g)
        }
        fun of(n: Int, d: Int) = of(n.toLong(), d.toLong())
    }

    operator fun plus(o: Frac) = of(n * o.d + o.n * d, d * o.d)
    operator fun minus(o: Frac) = of(n * o.d - o.n * d, d * o.d)
    operator fun times(o: Frac) = of(n * o.n, d * o.d)
    operator fun div(o: Frac) = of(n * o.d, d * o.n)

    override fun toString() = if (d == 1L) "$n" else "$n/$d"
}

tailrec fun gcd(a: Long, b: Long): Long = if (b == 0L) a else gcd(b, a % b)
fun gcd(a: Int, b: Int): Int = gcd(a.toLong(), b.toLong()).toInt()

private val SUPERSCRIPTS = mapOf(
    '0' to '⁰', '1' to '¹', '2' to '²', '3' to '³', '4' to '⁴',
    '5' to '⁵', '6' to '⁶', '7' to '⁷', '8' to '⁸', '9' to '⁹', '-' to '⁻',
)

/** Writes an integer exponent as superscript digits: sup(12) == "¹²". */
fun sup(e: Int): String = e.toString().map { SUPERSCRIPTS.getValue(it) }.joinToString("")

/** "x" with an exponent, where 1 is hidden and 0 drops the variable. */
fun pow(v: String, e: Int): String = when (e) {
    0 -> ""
    1 -> v
    else -> v + sup(e)
}

/** Simplifies √n into a√b. Returns (a, b). */
fun simplifyRoot(n: Int): Pair<Int, Int> {
    var outside = 1
    var inside = n
    var f = 2
    while (f * f <= inside) {
        while (inside % (f * f) == 0) {
            inside /= f * f
            outside *= f
        }
        f++
    }
    return outside to inside
}

fun rootString(n: Int): String {
    val (a, b) = simplifyRoot(n)
    return when {
        b == 1 -> "$a"
        a == 1 -> "√$b"
        else -> "$a√$b"
    }
}

/** Formats "m x + b" as a clean line equation: y = 3x − 4, y = −x + 2, y = 5. */
fun lineString(m: Frac, b: Frac): String {
    val mx = xTerm(m)
    val bs = when {
        b.n == 0L -> ""
        mx.isEmpty() -> fracStr(b)
        b.n < 0 -> " − ${fracStr(Frac.of(-b.n, b.d))}"
        else -> " + ${fracStr(b)}"
    }
    return "y = " + (mx + bs).ifEmpty { "0" }
}

/** The "mx" part of an expression: x, −x, 3x, (2/3)x, or empty when m is 0. */
fun xTerm(m: Frac): String = when {
    m.n == 0L -> ""
    m == Frac.of(1, 1) -> "x"
    m == Frac.of(-1, 1) -> "−x"
    m.d == 1L -> "${neg(m.n)}x"
    else -> "${if (m.n < 0) "−" else ""}(${kotlin.math.abs(m.n)}/${m.d})x"
}

fun xTerm(m: Int): String = xTerm(Frac.of(m, 1))

fun neg(n: Long): String = if (n < 0) "−${-n}" else "$n"
fun neg(n: Int): String = neg(n.toLong())
fun fracStr(f: Frac): String = if (f.n < 0) "−" + Frac.of(-f.n, f.d) else f.toString()

/** Signed term for building expressions: term(3) == "+ 3", term(-3) == "− 3". */
fun term(n: Int): String = if (n < 0) "− ${-n}" else "+ $n"

// ---------------------------------------------------------------- LaTeX helpers

/** Marks [tex] as inline math. */
fun m(tex: String) = "\\($tex\\)"

/** LaTeX for a fraction in lowest terms: "\frac{2}{3}", "-\frac{1}{2}", or a whole number. */
fun Frac.tex(): String = when {
    d == 1L -> "$n"
    n < 0 -> "-\\frac{${-n}}{$d}"
    else -> "\\frac{$n}{$d}"
}

/** An unreduced fraction, for showing work. */
fun tfrac(n: Any, d: Any) = "\\frac{$n}{$d}"

fun powTex(v: String, e: Int): String = when (e) {
    0 -> ""
    1 -> v
    else -> "$v^{$e}"
}

fun rootTex(n: Int): String {
    val (a, b) = simplifyRoot(n)
    return when {
        b == 1 -> "$a"
        a == 1 -> "\\sqrt{$b}"
        else -> "$a\\sqrt{$b}"
    }
}

/** The "mx" part of a line: x, -x, 3x, \frac{2}{3}x. */
fun xTex(m: Frac): String = when {
    m.n == 0L -> ""
    m == Frac.of(1, 1) -> "x"
    m == Frac.of(-1, 1) -> "-x"
    else -> "${m.tex()}x"
}

fun xTex(m: Int): String = xTex(Frac.of(m, 1))

fun lineTex(m: Frac, b: Frac): String {
    val mx = xTex(m)
    val bs = when {
        b.n == 0L -> ""
        mx.isEmpty() -> b.tex()
        b.n < 0 -> " - ${Frac.of(-b.n, b.d).tex()}"
        else -> " + ${b.tex()}"
    }
    return "y = " + (mx + bs).ifEmpty { "0" }
}

/** A number in parentheses when negative, for substitution: (-3). */
fun par(n: Int) = if (n < 0) "($n)" else "$n"
