package com.hexie.math.questions

import com.hexie.math.questions.Tex.Delim
import com.hexie.math.questions.Tex.Row
import com.hexie.math.questions.Tex.Scripts
import com.hexie.math.questions.Tex.Space
import com.hexie.math.questions.Tex.Sqrt
import com.hexie.math.questions.Tex.Sym

/**
 * A small LaTeX math parser. It covers the subset the question generators use.
 * Text marks inline math with \( ... \). The ui/MathText.kt renderer draws the tree.
 * An unknown command throws, so a unit test catches typos in the generators.
 */
sealed interface Tex {
    /** One run of characters. [italic] for variables. [op] adds space on both sides (=, +, −, ×). */
    data class Sym(val text: String, val italic: Boolean = false, val op: Boolean = false) : Tex
    data class Row(val items: List<Tex>) : Tex
    data class Frac(val num: Tex, val den: Tex) : Tex
    data class Scripts(val base: Tex, val sup: Tex?, val sub: Tex?) : Tex
    data class Sqrt(val body: Tex, val index: Tex?) : Tex
    /** A pair of delimiters that grows to fit [body]: ( ) [ ] | or "" for none. */
    data class Delim(val left: String, val body: Tex, val right: String) : Tex
    /** Horizontal space, in em. */
    data class Space(val em: Float) : Tex
}

class TexError(message: String) : IllegalArgumentException(message)

object TexParser {

    private val SYMBOLS = mapOf(
        "pi" to "π", "theta" to "θ", "alpha" to "α", "beta" to "β", "angle" to "∠", "triangle" to "△",
        "infty" to "∞", "ldots" to "…", "cdots" to "⋯", "%" to "%", "$" to "$", "{" to "{", "}" to "}",
        "circ" to "°", "degree" to "°", "prime" to "′",
    )
    private val OPERATORS = mapOf(
        "cdot" to "·", "times" to "×", "div" to "÷", "pm" to "±", "le" to "≤", "leq" to "≤",
        "ge" to "≥", "geq" to "≥", "ne" to "≠", "neq" to "≠", "approx" to "≈", "to" to "→",
        "Rightarrow" to "⇒", "implies" to "⇒",
    )
    private val FUNCTIONS = setOf("sin", "cos", "tan", "log", "ln")
    private val SPACES = mapOf("," to 0.17f, ":" to 0.22f, ";" to 0.28f, " " to 0.25f, "quad" to 1f, "qquad" to 2f, "!" to -0.1f)
    private const val OP_CHARS = "+-−=<>×÷·±≤≥≠≈→"

    /** Splits text into (isMath, content) pieces at \( and \). */
    fun split(text: String): List<Pair<Boolean, String>> {
        val out = mutableListOf<Pair<Boolean, String>>()
        var i = 0
        while (i < text.length) {
            val open = text.indexOf("\\(", i)
            if (open < 0) { out += false to text.substring(i); break }
            if (open > i) out += false to text.substring(i, open)
            val close = text.indexOf("\\)", open + 2)
            if (close < 0) throw TexError("Missing \\) in: $text")
            out += true to text.substring(open + 2, close)
            i = close + 2
        }
        return out
    }

    /**
     * Splits math at top-level relation signs, so a long equation can wrap between pieces.
     * "a = b = c" becomes ["a", "= b", "= c"].
     */
    fun breakPoints(tex: String): List<String> {
        val out = mutableListOf<String>()
        var depth = 0
        var start = 0
        var i = 0
        while (i < tex.length) {
            val c = tex[i]
            when {
                c == '\\' && tex.startsWith("\\left", i) -> { depth++; i += 5; continue }
                c == '\\' && tex.startsWith("\\right", i) -> { depth--; i += 6; continue }
                c == '\\' -> { i += 2; continue }
                c == '{' -> depth++
                c == '}' -> depth--
                c == '=' && depth == 0 && i > start -> {
                    out += tex.substring(start, i).trim()
                    start = i
                }
            }
            i++
        }
        out += tex.substring(start).trim()
        return out.filter { it.isNotEmpty() }
    }

    fun parse(tex: String): Tex {
        val p = Reader(tex)
        val row = p.row(stopAt = null)
        if (!p.done()) throw TexError("Unexpected '${p.peek()}' in: $tex")
        return row
    }

    private class Reader(val s: String) {
        var i = 0
        fun done() = i >= s.length
        fun peek() = s[i]

        fun row(stopAt: Char?): Tex {
            val items = mutableListOf<Tex>()
            while (!done()) {
                val c = peek()
                if (stopAt != null && c == stopAt) break
                if (c == '}' && stopAt == null) throw TexError("Unmatched } in: $s")
                if (s.startsWith("\\right", i)) break
                when {
                    c.isWhitespace() -> i++
                    c == '^' || c == '_' -> {
                        i++
                        val arg = argument()
                        val base = items.removeLastOrNull() ?: Sym("")
                        // A function name like \log is Row(name, space). Scripts go on the name, before the space.
                        if (base is Row && base.items.size == 2 && base.items[1] is Space && base.items[0] is Sym) {
                            items += Row(listOf(if (c == '^') Scripts(base.items[0], arg, null) else Scripts(base.items[0], null, arg), base.items[1]))
                            continue
                        }
                        val prev = base as? Scripts
                        items += when {
                            c == '^' && arg == Sym("°") -> Row(listOf(base, Sym("°")))
                            prev != null && c == '^' && prev.sup == null -> prev.copy(sup = arg)
                            prev != null && c == '_' && prev.sub == null -> prev.copy(sub = arg)
                            c == '^' -> Scripts(base, arg, null)
                            else -> Scripts(base, null, arg)
                        }
                    }
                    else -> items += atom()
                }
            }
            return if (items.size == 1) items[0] else Row(items)
        }

        /** The argument of ^, _, or a command: a {group} or one atom. */
        fun argument(): Tex {
            while (!done() && peek().isWhitespace()) i++
            if (done()) throw TexError("Missing argument in: $s")
            return if (peek() == '{') group() else atom()
        }

        fun group(): Tex {
            expect('{')
            val r = row(stopAt = '}')
            expect('}')
            return r
        }

        fun expect(c: Char) {
            if (done() || peek() != c) throw TexError("Expected '$c' at $i in: $s")
            i++
        }

        fun atom(): Tex {
            val c = peek()
            return when {
                c == '\\' -> command()
                c == '{' -> group()
                c.isDigit() || (c == '.' && i + 1 < s.length && s[i + 1].isDigit()) -> {
                    val start = i
                    while (!done() && (peek().isDigit() || peek() == '.')) i++
                    Sym(s.substring(start, i))
                }
                c.isLetter() && c.code < 128 -> { i++; Sym(c.toString(), italic = true) }
                c in OP_CHARS -> { i++; Sym(if (c == '-') "−" else c.toString(), op = true) }
                c == ',' -> { i++; Row(listOf(Sym(","), Space(0.17f))) }
                c == '}' -> throw TexError("Unmatched } in: $s")
                else -> { i++; Sym(c.toString(), italic = c == 'θ') }
            }
        }

        fun command(): Tex {
            expect('\\')
            if (done()) throw TexError("Trailing backslash in: $s")
            val name = if (peek().isLetter()) {
                val start = i
                while (!done() && peek().isLetter()) i++
                s.substring(start, i)
            } else {
                s[i++].toString()
            }
            SPACES[name]?.let { return Space(it) }
            SYMBOLS[name]?.let { return Sym(it) }
            OPERATORS[name]?.let { return Sym(it, op = true) }
            if (name in FUNCTIONS) return Row(listOf(Sym(name), Space(0.12f)))
            return when (name) {
                "frac", "dfrac", "tfrac" -> Tex.Frac(argument(), argument())
                "sqrt" -> {
                    val index = if (!done() && peek() == '[') {
                        i++
                        val r = row(stopAt = ']')
                        expect(']')
                        r
                    } else null
                    Sqrt(argument(), index)
                }
                "text", "mathrm", "textrm" -> {
                    expect('{')
                    val start = i
                    var depth = 1
                    while (!done() && depth > 0) {
                        if (peek() == '{') depth++
                        if (peek() == '}') depth--
                        if (depth > 0) i++
                    }
                    val t = s.substring(start, i)
                    expect('}')
                    Sym(t)
                }
                "left" -> {
                    val l = delimiter()
                    val body = row(stopAt = null)
                    if (!s.startsWith("\\right", i)) throw TexError("\\left without \\right in: $s")
                    i += 6
                    Delim(l, body, delimiter())
                }
                else -> throw TexError("Unknown command \\$name in: $s")
            }
        }

        fun delimiter(): String {
            while (!done() && peek().isWhitespace()) i++
            if (done()) throw TexError("Missing delimiter in: $s")
            val c = peek()
            i++
            return when (c) {
                '(', ')', '[', ']', '|' -> c.toString()
                '.' -> ""
                else -> throw TexError("Bad delimiter '$c' in: $s")
            }
        }
    }
}
