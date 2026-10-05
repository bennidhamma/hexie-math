package com.hexie.math.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class DifficultyTest {

    @Test
    fun sessionsStartEasyAndNeverEndHard() {
        for (mode in ChallengeMode.entries) for (n in 2..5) {
            val plan = planSession(n, intArrayOf(mode.easy, mode.medium, mode.hard))
            assertEquals("$mode $n", n, plan.size)
            assertEquals("$mode $n: $plan", Level.EASY, plan.first())
            assertNotEquals("$mode $n: $plan", Level.HARD, plan.last())
        }
    }

    @Test
    fun balancedFiveHasAMix() {
        val plan = planSession(5, intArrayOf(30, 45, 25))
        assertTrue(plan.toString(), Level.EASY in plan && Level.MEDIUM in plan && Level.HARD in plan)
    }

    @Test
    fun roughStretchShiftsTowardEasy() {
        val rough = adjustedMix(ChallengeMode.BALANCED, List(10) { it < 3 })    // 30% right
        val strong = adjustedMix(ChallengeMode.BALANCED, List(10) { true })     // 100% right
        assertTrue(rough.toList().toString(), rough[0] > 30 && rough[2] < 25)
        assertTrue(strong.toList().toString(), strong[2] > 25)
        assertEquals(100, rough.sum()); assertEquals(100, strong.sum())
    }
}
