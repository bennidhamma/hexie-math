package com.hexie.math.questions

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class TexTest {

    /** Every math piece in every generated question must parse. This catches LaTeX typos. */
    @Test
    fun everyGeneratedEquationParses() {
        val failures = mutableSetOf<String>()
        for ((topic, gen) in QuestionFactory.allGenerators()) {
            repeat(300) { seed ->
                val q = gen(Random(seed))
                for (text in listOf(q.prompt, q.explanation) + q.choices) {
                    try {
                        for ((isMath, part) in TexParser.split(text)) {
                            if (isMath) TexParser.breakPoints(part).forEach { TexParser.parse(it) }
                            else if ("\\" in part) failures += "$topic: backslash outside math: $part"
                        }
                    } catch (e: TexError) {
                        failures += "$topic: ${e.message}"
                    }
                }
            }
        }
        assertTrue(failures.take(20).joinToString("\n"), failures.isEmpty())
    }

    @Test
    fun parsesCommonForms() {
        val f = TexParser.parse("\\frac{1}{2}")
        assertEquals(Tex.Frac(Tex.Sym("1"), Tex.Sym("2")), f)
        val sup = TexParser.parse("x^{2}")
        assertEquals(Tex.Scripts(Tex.Sym("x", italic = true), Tex.Sym("2"), null), sup)
        assertEquals(listOf("a", "= b", "= c"), TexParser.breakPoints("a = b = c"))
        assertEquals(listOf("\\frac{a = 1}{2}"), TexParser.breakPoints("\\frac{a = 1}{2}"))
    }
}
