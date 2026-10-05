package com.hexie.math.data

import kotlin.random.Random

/** Easy problems come from the generators. Medium and hard come from the problem bank. */
enum class Level { EASY, MEDIUM, HARD;
    fun easier(): Level = entries[(ordinal - 1).coerceAtLeast(0)]
}

/** The parent's setting: the share of easy, medium, and hard problems, in percent. */
enum class ChallengeMode(val label: String, val easy: Int, val medium: Int, val hard: Int) {
    GENTLE("Gentle", 50, 40, 10),
    BALANCED("Balanced", 30, 45, 25),
    CHALLENGE("Challenge", 15, 45, 40),
}

/**
 * The mix for today: the mode's mix, moved toward easy after a rough stretch
 * (under 50% right in recent answers) and toward hard after a strong one (over 85%).
 */
fun adjustedMix(mode: ChallengeMode, recent: List<Boolean>): IntArray {
    var (e, m, h) = Triple(mode.easy, mode.medium, mode.hard)
    if (recent.size >= 5) {
        val rate = recent.count { it }.toDouble() / recent.size
        if (rate < 0.5) {
            val shift = minOf(15, h); h -= shift; e += shift
            if (shift < 15) { val more = minOf(15 - shift, m - 20).coerceAtLeast(0); m -= more; e += more }
        } else if (rate > 0.85) {
            val shift = minOf(10, e - 5).coerceAtLeast(0); e -= shift; h += shift
        }
    }
    return intArrayOf(e, m, h)
}

/**
 * Plans the levels for a session of [n] problems. The session starts easy, puts the hard
 * problems in the middle, and does not end on a hard one, so it finishes on something winnable.
 * A single problem is drawn at random from the mix.
 */
fun planSession(n: Int, mix: IntArray, random: Random = Random.Default): List<Level> {
    if (n <= 1) {
        val roll = random.nextInt(mix.sum())
        return listOf(if (roll < mix[0]) Level.EASY else if (roll < mix[0] + mix[1]) Level.MEDIUM else Level.HARD)
    }
    // Largest-remainder rounding of the mix to n problems.
    val exact = mix.map { it * n / 100.0 }
    val counts = exact.map { it.toInt() }.toIntArray()
    exact.indices.sortedByDescending { exact[it] - counts[it] }.take(n - counts.sum()).forEach { counts[it]++ }
    var (e, m, h) = Triple(counts[0], counts[1], counts[2])
    // Every session of 2 or more starts with an easy one.
    if (e == 0) { if (m > 0) m-- else h--; e = 1 }

    val seq = mutableListOf(Level.EASY); e--
    val firstMedium = m / 2
    repeat(firstMedium) { seq += Level.MEDIUM }
    repeat(h) { seq += Level.HARD }
    repeat(m - firstMedium) { seq += Level.MEDIUM }
    repeat(e) { seq += Level.EASY }
    if (seq.last() == Level.HARD) {
        // Swap the closing hard problem with the closest earlier problem that is not hard.
        // If the only other problem is the opening easy one, make the last one medium instead.
        val i = seq.indexOfLast { it != Level.HARD }
        if (i > 0) { seq[seq.lastIndex] = seq[i]; seq[i] = Level.HARD } else seq[seq.lastIndex] = Level.MEDIUM
    }
    return seq
}
