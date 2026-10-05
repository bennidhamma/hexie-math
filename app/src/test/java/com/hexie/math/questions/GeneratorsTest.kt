package com.hexie.math.questions

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class GeneratorsTest {

    @Test
    fun everyGeneratorBuildsFourDistinctChoices() {
        val failures = mutableListOf<String>()
        for ((topic, gen) in QuestionFactory.allGenerators()) {
            repeat(2000) { seed ->
                val q = try {
                    gen(Random(seed))
                } catch (e: Exception) {
                    failures += "$topic seed=$seed threw $e"
                    return@repeat
                }
                val ok = q.choices.size == 4 && q.choices.toSet().size == 4 &&
                    q.correctIndex in 0..3 && q.choices.none { it == "None of these" } &&
                    q.explanation.isNotBlank()
                for (d in listOfNotNull(q.diagram, q.explanationDiagram)) {
                    if (d is Diagram.Triangle) {
                        val good = d.angleA.isFinite() && d.angleB.isFinite() && d.angleA > 1 && d.angleB > 1 && d.angleA + d.angleB < 179
                        if (!good) failures += "$topic seed=$seed bad triangle $d :: ${q.prompt.take(50)}"
                    }
                }
                if (!ok) failures += "$topic seed=$seed ${q.choices} :: ${q.prompt.take(70)}"
            }
        }
        val byKind = failures.groupBy { it.substringBefore(" seed") + " " + it.substringAfter(":: ").take(30) }
        assertTrue(byKind.entries.joinToString("\n") { "${it.value.size}x ${it.value.first()}" }, failures.isEmpty())
    }

    @Test
    fun fractionsReduce() {
        assertEquals("1/2", Frac.of(3, 6).toString())
        assertEquals(Frac.of(-1, 3), Frac.of(2, -6))
        assertEquals("2√3", rootString(12))
        assertEquals("y = −x + 2", lineString(Frac.of(-1, 1), Frac.of(2, 1)))
        assertEquals("y = (1/2)x − 3", lineString(Frac.of(1, 2), Frac.of(-3, 1)))
    }
}
