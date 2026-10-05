package com.hexie.math.questions

import kotlin.math.abs
import kotlin.random.Random

/**
 * Builds a fresh question for a topic. Every answer is computed, so there are
 * no hand-typed answer keys to get wrong.
 *
 * Text uses inline LaTeX between \( and \). The helpers m(), tex(), tfrac(), and
 * friends live in Question.kt. ui/MathText.kt draws the math.
 */
object QuestionFactory {

    private val generators: Map<Topic, List<(Random) -> Question>> = mapOf(
        Topic.PROBABILITY to listOf(::marblesNoReplacement, ::atLeastOne, ::twoWayTable, ::expectedCount),
        Topic.RATIOS to listOf(::ratioPartOfTotal, ::inverseProportion, ::mapScaleArea, ::chainedRatio),
        Topic.PERCENT to listOf(::percentUpDown, ::originalPrice, ::percentOf),
        Topic.WORD_PROBLEMS to listOf(::planCost, ::ticketSystem, ::translateSentence),
        Topic.EXPONENTS to listOf(::powerOfMonomial, ::productOfMonomials, ::sameBaseEquation, ::addRadicals, ::fractionalExponent),
        Topic.REWRITING to listOf(::solveFormula, ::solveFormula, ::solveLinearNumbers),
        Topic.AREA_VOLUME to listOf(::rectanglePerimeterArea, ::scaleFactorVolume, ::cylinderVolume, ::circleFromCircumference),
        Topic.SLOPE to listOf(::lineThroughPoints, ::perpendicularLine, ::slopeFromStandardForm),
        Topic.ANGLES to listOf(::triangleAngles, ::parallelLines, ::polygonInteriorAngle),
        Topic.FRACTIONS to listOf(::orderOfOperationsFractions, ::complexFraction, ::evaluateWithNegatives),
        Topic.UNIT_CIRCLE to listOf(::quadrantTrig, ::specialAngle, ::degreesToRadians),
        Topic.LOGARITHMS to listOf(::logToExponent, ::evaluateLog, ::logRules, ::solveLog, ::logProduct),
        Topic.LAW_SINES_COSINES to listOf(::lawOfCosinesSide, ::lawOfSinesSide, ::lawOfCosinesAngle),
    )

    /** Topics that have generators. The problem bank covers the rest. */
    val topics: Set<Topic> get() = generators.keys

    fun make(topic: Topic, r: Random = Random.Default): Question =
        (generators[topic] ?: generators.getValue(Topic.PROBABILITY)).random(r)(r)

    /** Every generator, used by the unit tests. */
    internal fun allGenerators(): List<Pair<Topic, (Random) -> Question>> =
        generators.flatMap { (t, list) -> list.map { t to it } }
}

private fun Frac.toDouble() = n.toDouble() / d

private fun Frac.pow(k: Int): Frac {
    var out = Frac.of(1, 1)
    repeat(k) { out *= this }
    return out
}

private fun article(word: String) = if (word.first().lowercaseChar() in "aeiou") "an" else "a"

/** " = \frac{1}{2}" when the fraction n/d reduces, else nothing. */
private fun reduced(n: Int, d: Int, f: Frac) = if (f.n == n.toLong() && f.d == d.toLong()) "" else " = ${f.tex()}"

private fun Random.sign() = if (nextBoolean()) 1 else -1

private fun ipow(b: Int, e: Int): Int { var o = 1; repeat(e) { o *= b }; return o }

/** A math choice built from a fraction. */
private fun mf(f: Frac) = m(f.tex())

// ---------------------------------------------------------------- Probability

private fun marblesNoReplacement(r: Random): Question {
    val colors = listOf("red", "blue", "green", "purple").shuffled(r)
    val target = colors[0]
    val t = r.nextInt(3, 8)
    val o1 = r.nextInt(3, 8)
    val o2 = r.nextInt(2, 6)
    val n = t + o1 + o2
    val correct = Frac.of(t * (t - 1), n * (n - 1))
    val withReplacement = Frac.of(t * t, n * n)
    return buildQuestion(
        r, Topic.PROBABILITY,
        "Hexie's pouch holds $t $target, $o1 ${colors[1]}, and $o2 ${colors[2]} marbles. " +
            "She pulls out 2 marbles at random, one after the other, WITHOUT putting the first one back. " +
            "What is the probability that both marbles are $target?",
        mf(correct),
        listOf(mf(withReplacement), mf(Frac.of(t, n)), mf(Frac.of(t * (t - 1), n * n)), mf(Frac.of(t - 1, n - 1))),
        "There are $n marbles in all.\n\n" +
            "• First pick: $t of the $n are $target, so ${m("P = " + tfrac(t, n))}.\n" +
            "• The first marble stays out. Now ${t - 1} $target marbles are left out of ${n - 1}.\n" +
            "• Second pick: ${m("P = " + tfrac(t - 1, n - 1))}.\n\n" +
            "For \"this AND then that\", multiply:\n" +
            m("${tfrac(t, n)} \\times ${tfrac(t - 1, n - 1)} = ${tfrac(t * (t - 1), n * (n - 1))} = ${correct.tex()}") + "\n\n" +
            "Trap to avoid: ${mf(withReplacement)} is the answer only if the marble goes back in the pouch.",
        filler = { mf(Frac.of(t + it + 1, n)) },
    ).copy(diagram = Diagram.Marbles(listOf(target to t, colors[1] to o1, colors[2] to o2)))
}

private fun atLeastOne(r: Random): Question {
    val sections = listOf(4, 5, 6, 8).random(r)
    val gold = r.nextInt(1, sections / 2 + 1)
    val k = r.nextInt(2, 4)
    val p = Frac.of(gold, sections)
    val miss = Frac.of(sections - gold, sections)
    val correct = Frac.of(1, 1) - miss.pow(k)
    val times = if (k == 2) "twice" else "3 times"
    return buildQuestion(
        r, Topic.PROBABILITY,
        "A spinner has $sections equal sections. $gold of them ${if (gold == 1) "is" else "are"} gold. " +
            "The spinner is spun $times. What is the probability that it lands on gold AT LEAST once?",
        mf(correct),
        listOf(
            mf(p.pow(k)),
            mf(miss.pow(k)),
            mf(Frac.of(1, 1) - p.pow(k)),
            (p * Frac.of(k, 1)).let { if (it.n < it.d) mf(it) else mf(Frac.of(1, k + 1)) },
        ),
        "\"At least once\" has many cases (gold 1 time, 2 times, ...). It is easier to use the opposite: NO gold at all.\n\n" +
            "• P(not gold on one spin): ${m(tfrac(sections - gold, sections) + reduced(sections - gold, sections, miss))}\n" +
            "• P(no gold on ${if (k == 2) "both" else "all $k"} spins): ${m("\\left(${miss.tex()}\\right)^{$k} = ${miss.pow(k).tex()}")}\n" +
            "• P(at least one gold): ${m("1 - ${miss.pow(k).tex()} = ${correct.tex()}")}\n\n" +
            "Hexie's rule: when you see \"at least one\", think \"1 minus none\".",
        filler = { mf(Frac.of(it + 1, sections + it + 2)) },
    ).copy(diagram = Diagram.Spinner(sections, gold, "★"))
}

private fun twoWayTable(r: Random): Question {
    val rows = listOf("Cat", "Toad", "Owl")
    val cols = listOf("1st year", "2nd year")
    val cells = List(3) { List(2) { r.nextInt(4, 25) } }
    val rowT = cells.map { it.sum() }
    val colT = List(2) { c -> cells.sumOf { it[c] } }
    val total = rowT.sum()
    val ri = r.nextInt(3)
    val ci = r.nextInt(2)
    val cell = cells[ri][ci]

    val pr = Frac.of(cell, colT[ci])        // P(row | col)
    val pc = Frac.of(cell, rowT[ri])        // P(col | row)
    val pj = Frac.of(cell, total)           // P(row and col)
    val pRow = Frac.of(rowT[ri], total)

    val figure = buildString {
        appendLine("Familiar  1st yr  2nd yr  Total")
        rows.forEachIndexed { i, name ->
            appendLine(name.padEnd(8) + cells[i][0].toString().padStart(8) + cells[i][1].toString().padStart(8) + rowT[i].toString().padStart(7))
        }
        append("Total".padEnd(8) + colT[0].toString().padStart(8) + colT[1].toString().padStart(8) + total.toString().padStart(7))
    }
    val intro = "The table shows the familiars chosen by apprentices at Hexie's witch school."
    val rowName = rows[ri].lowercase()
    val a = article(rowName)
    val filler = { k: Int -> mf(Frac.of(cell + k + 1, total)) }
    return when (r.nextInt(3)) {
        0 -> buildQuestion(
            r, Topic.PROBABILITY,
            "$intro An apprentice is chosen at random from the ${cols[ci]} students. What is the probability that the apprentice chose $a $rowName?",
            mf(pr), listOf(mf(pc), mf(pj), mf(pRow), mf(Frac.of(cell, total - cell))),
            "The words \"from the ${cols[ci]} students\" shrink the group. You only look at the ${cols[ci]} column.\n\n" +
                "• ${cols[ci]} total: ${colT[ci]}\n• ${cols[ci]} who chose $a $rowName: $cell\n\n" +
                m("P = ${tfrac(cell, colT[ci])}${reduced(cell, colT[ci], pr)}") +
                "\n\nThe denominator is the group you choose FROM, not the whole school.",
            figure, filler = filler,
        )
        1 -> buildQuestion(
            r, Topic.PROBABILITY,
            "$intro An apprentice who chose $a $rowName is picked at random. What is the probability that the apprentice is a ${cols[ci]} student?",
            mf(pc), listOf(mf(pr), mf(pj), mf(Frac.of(colT[ci], total)), mf(Frac.of(cell, total - cell))),
            "\"An apprentice who chose $a $rowName\" shrinks the group to the $rowName row.\n\n" +
                "• $rowName total: ${rowT[ri]}\n• Of those, ${cols[ci]}: $cell\n\n" +
                m("P = ${tfrac(cell, rowT[ri])}${reduced(cell, rowT[ri], pc)}"),
            figure, filler = filler,
        )
        else -> buildQuestion(
            r, Topic.PROBABILITY,
            "$intro One apprentice is chosen at random from the whole school. What is the probability that the apprentice is a ${cols[ci]} student AND chose $a $rowName?",
            mf(pj), listOf(mf(pr), mf(pc), mf(pRow), mf(Frac.of(colT[ci], total))),
            "\"From the whole school\" means the denominator is the grand total, $total.\n\n" +
                "The apprentice must be in BOTH the ${cols[ci]} column AND the $rowName row. That is one cell: $cell.\n\n" +
                m("P = ${tfrac(cell, total)}${reduced(cell, total, pj)}"),
            figure, filler = filler,
        )
    }
}

private fun expectedCount(r: Random): Question {
    val sections = listOf(5, 6, 8, 10, 12).random(r)
    val win = r.nextInt(1, sections / 2 + 1)
    val spins = sections * r.nextInt(3, 13)
    val correct = spins * win / sections
    return buildQuestion(
        r, Topic.PROBABILITY,
        "A cauldron game has $sections equal slots. $win of them hold a frog prize. " +
            "If the game is played $spins times, about how many frog prizes should a player expect to win?",
        "$correct",
        listOf("${spins / sections}", "${spins * (sections - win) / sections}", "${spins / win}", "${correct + win}"),
        "Expected count = (probability of the event) × (number of tries).\n\n" +
            "• P(frog): ${m(tfrac(win, sections))}\n• Tries: $spins\n\n" +
            m("${tfrac(win, sections)} \\times $spins = $correct"),
        filler = { "${correct + 2 * (it + 1)}" },
    ).copy(diagram = Diagram.Spinner(sections, win, "🐸"))
}

// ---------------------------------------------------------------- Ratios

private fun ratioPartOfTotal(r: Random): Question {
    var a: Int; var b: Int
    do { a = r.nextInt(2, 10); b = r.nextInt(2, 10) } while (a == b || gcd(a, b) != 1)
    val k = r.nextInt(3, 13)
    val total = (a + b) * k
    val correct = b * k
    return buildQuestion(
        r, Topic.RATIOS,
        "In Hexie's swamp, the ratio of frogs to newts is $a:$b. There are $total frogs and newts in all. How many newts are there?",
        "$correct",
        listOf("${a * k}", "${total / b}", "${total - b}", "${correct + k}"),
        "A ratio of $a:$b means the swamp splits into ${m("$a + $b = ${a + b}")} equal parts.\n\n" +
            "• One part: ${m("$total \\div ${a + b} = $k")}\n• Newts get $b parts: ${m("$b \\times $k = $correct")}\n\n" +
            "Check: frogs = ${m("$a \\times $k = ${a * k}")}, and ${m("${a * k} + $correct = $total")}. ✓",
        filler = { "${correct + 2 * k + it}" },
    )
}

private fun inverseProportion(r: Random): Question {
    while (true) {
        val w1 = r.nextInt(2, 10)
        val days1 = r.nextInt(2, 13)
        val w2 = r.nextInt(2, 13)
        val total = w1 * days1
        if (w2 == w1 || total % w2 != 0) continue
        val ans = total / w2
        if (ans == days1) continue
        return buildQuestion(
            r, Topic.RATIOS,
            "$w1 witches can brew a giant batch of potion in $days1 days. Working at the same rate, how many days would it take $w2 witches to brew the same batch?",
            "$ans",
            listOf(mf(Frac.of(days1 * w2, w1)), "${days1 + (w1 - w2)}", "$total", "${ans + 1}"),
            "More witches means FEWER days. This is an inverse proportion, so do not just scale up.\n\n" +
                "Find the total work in \"witch-days\":\n${m("$w1 \\times $days1 = $total")} witch-days\n\n" +
                "Share it among $w2 witches:\n${m("$total \\div $w2 = $ans")} days\n\n" +
                "Trap: setting up ${m("${tfrac(w1, days1)} = ${tfrac(w2, "x")}")} assumes more witches take MORE days.",
            filler = { "${ans + it + 2}" },
        )
    }
}

private fun mapScaleArea(r: Random): Question {
    val k = r.nextInt(2, 9)
    val a = r.nextInt(2, 7)
    val b = r.nextInt(2, 7)
    val correct = a * b * k * k
    return buildQuestion(
        r, Topic.RATIOS,
        "On a map of the Misty Woods, 1 centimeter represents $k kilometers. A rectangular bog on the map is $a cm by $b cm. What is the actual area of the bog, in square kilometers?",
        "$correct",
        listOf("${a * b * k}", "${2 * (a + b) * k}", "${a * b + k * k}", "${(a + b) * k}"),
        "Scale each length FIRST, then find the area.\n\n" +
            "• $a cm → ${m("$a \\times $k = ${a * k}")} km\n• $b cm → ${m("$b \\times $k = ${b * k}")} km\n\n" +
            "Area: ${m("${a * k} \\times ${b * k} = $correct")} km²\n\n" +
            "Trap: ${m("${a * b} \\times $k = ${a * b * k}")} scales the area only once. Area grows by the scale SQUARED, ${m("$k^{2} = ${k * k}")}.",
        filler = { "${correct + k * (it + 1)}" },
    ).copy(diagram = Diagram.Rectangle(a.toDouble(), b.toDouble(), "$a cm", "$b cm"))
}

private fun chainedRatio(r: Random): Question {
    var p: Int; var q: Int; var s: Int; var t: Int
    do {
        p = r.nextInt(1, 8); q = r.nextInt(2, 8); s = r.nextInt(2, 8); t = r.nextInt(1, 8)
    } while (gcd(p, q) != 1 || gcd(s, t) != 1 || q == s || p == t)
    val a = Frac.of(p * s, q * t)
    fun ratio(f: Frac) = "${f.n}:${f.d}"
    return buildQuestion(
        r, Topic.RATIOS,
        "In a potion, the ratio of moonwater to slime is $p:$q. The ratio of slime to dragon tears is $s:$t. What is the ratio of moonwater to dragon tears?",
        ratio(a),
        listOf(ratio(Frac.of(p, t)), ratio(Frac.of(p * t, q * s)), ratio(Frac.of(p + s, q + t)), ratio(Frac.of(q * t, p * s))),
        "Slime is in both ratios, so make the slime numbers match.\n\n" +
            "• Moonwater : slime = $p:$q → multiply by $s → ${p * s}:${q * s}\n" +
            "• Slime : tears = $s:$t → multiply by $q → ${q * s}:${q * t}\n\n" +
            "Now slime is ${q * s} in both, so moonwater : tears = ${p * s}:${q * t}" +
            (if (a.n.toInt() != p * s) " = ${ratio(a)}" else "") + ".",
        filler = { "${p * s + it + 1}:${q * t}" },
    )
}

// ---------------------------------------------------------------- Percent

private fun pct(hundredths: Int): String =
    if (hundredths % 100 == 0) "${hundredths / 100}%" else "%.2f".format(hundredths / 100.0).trimEnd('0').trimEnd('.') + "%"

private fun dec(x: Double) = "%.4f".format(x).trimEnd('0').trimEnd('.')

private fun percentUpDown(r: Random): Question {
    val p = listOf(10, 20, 25, 40, 50).random(r)
    val q = listOf(10, 20, 25, 40, 50).random(r)
    val final = (100 + p) * (100 - q) // in hundredths of a percent
    val up = dec((100 + p) / 100.0); val down = dec((100 - q) / 100.0)
    return buildQuestion(
        r, Topic.PERCENT,
        "The price of a broomstick goes UP by $p%. Later, the new price goes DOWN by $q%. The final price is what percent of the original price?",
        pct(final),
        listOf(pct((100 + p - q) * 100), pct((100 - p) * (100 + q)), "100%", pct((100 + p + q) * 100)),
        "Percent changes multiply. They do not add.\n\n" +
            "• Up $p% → multiply by $up\n• Down $q% → multiply by $down\n\n" +
            "${m("$up \\times $down = ${dec(final / 10000.0)}")}, so the final price is ${pct(final)} of the original.\n\n" +
            "Tip: try it with a \$100 broom. After +$p% it costs \$${100 + p}. Then $q% off leaves \$${dec(final / 100.0)}.",
        filler = { pct(final + 500 * (it + 1)) },
    )
}

private fun originalPrice(r: Random): Question {
    val p = listOf(10, 20, 25, 30, 40, 60).random(r)
    val orig = 20 * r.nextInt(2, 11)
    val sale = orig * (100 - p) / 100
    return buildQuestion(
        r, Topic.PERCENT,
        "A spell book is on sale for $p% off. The sale price is \$$sale. What was the original price?",
        "\$$orig",
        listOf("\$${sale + sale * p / 100}", "\$${sale + p}", "\$${sale * (100 + p) / 100 + 1}", "\$${orig + 10}"),
        "$p% off means you pay ${100 - p}% of the original price.\n\n" +
            m("${dec((100 - p) / 100.0)} \\times \\text{original} = $sale") + "\n" +
            m("\\text{original} = ${tfrac(sale, dec((100 - p) / 100.0))} = $orig") + "\n\n" +
            "Trap: adding $p% back to \$$sale gives the wrong answer, because the $p% was taken from the ORIGINAL, not the sale price.",
        filler = { "\$${orig + 5 * (it + 3)}" },
    )
}

private fun percentOf(r: Random): Question {
    val whole = listOf(40, 50, 80, 120, 160, 200, 250).random(r)
    val p = listOf(5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 75).filter { whole * it % 100 == 0 }.random(r)
    val part = whole * p / 100
    return buildQuestion(
        r, Topic.PERCENT,
        "Hexie collected $whole mushrooms. $part of them were glowing. What percent of the mushrooms were glowing?",
        "$p%",
        listOf("${p / 2 + 1}%", "${whole * 100 / part}%", "${part}%", "${100 - p}%"),
        "Percent = part ÷ whole × 100.\n\n" +
            m("${tfrac(part, whole)} = ${dec(part.toDouble() / whole)}") + "\n" +
            m("${dec(part.toDouble() / whole)} \\times 100 = $p\\%"),
        filler = { "${p + 5 * (it + 1)}%" },
    )
}

// ---------------------------------------------------------------- Word problems

private fun planCost(r: Random): Question {
    val fee = 5 * r.nextInt(2, 9)
    val rate = r.nextInt(2, 9)
    val units = r.nextInt(4, 16)
    val total = fee + rate * units
    return buildQuestion(
        r, Topic.WORD_PROBLEMS,
        "A broom-rental shop charges a flat fee of \$$fee plus \$$rate for each hour. Hexie's bill was \$$total. For how many hours did she rent the broom?",
        "$units",
        listOf(Frac.of(total, rate).let { if (it.d == 1L) "$it" else dec(total.toDouble() / rate) }, "${(total + fee) / rate}", "${total / (fee + rate)}", "${units + 1}"),
        "Write the equation: ${m("$fee + ${rate}h = $total")}\n\n" +
            "• Subtract the flat fee: ${m("${rate}h = ${total - fee}")}\n• Divide by $rate: ${m("h = $units")}\n\n" +
            "Trap: dividing $total by $rate forgets that the \$$fee fee is paid only once.",
        filler = { "${units + it + 2}" },
    )
}

private fun ticketSystem(r: Random): Question {
    val adult = r.nextInt(8, 16)
    var kid: Int
    do { kid = r.nextInt(4, 10) } while (kid >= adult)
    val x = r.nextInt(5, 30)
    val y = r.nextInt(5, 30)
    val n = x + y
    val total = adult * x + kid * y
    return buildQuestion(
        r, Topic.WORD_PROBLEMS,
        "Tickets to the Midnight Potion Fair cost \$$adult for adults and \$$kid for kids. $n tickets were sold for a total of \$$total. How many ADULT tickets were sold?",
        "$x",
        listOf("$y", "${n / 2}", "${total / adult}", "${x + 2}"),
        "Let ${m("a")} = adult tickets and ${m("k")} = kid tickets.\n\n" +
            m("a + k = $n") + "\n" + m("${adult}a + ${kid}k = $total") + "\n\n" +
            "Replace ${m("k")} with ${m("$n - a")}:\n" +
            m("${adult}a + $kid($n - a) = $total") + "\n" +
            m("${adult}a + ${kid * n} - ${kid}a = $total") + "\n" +
            m("${adult - kid}a = ${total - kid * n}") + "\n" +
            m("a = $x") + "\n\n" +
            "Check: $x adults and $y kids. ${m("$adult($x) + $kid($y) = $total")}. ✓",
        filler = { "${x + it + 3}" },
    )
}

private fun translateSentence(r: Random): Question {
    val a = r.nextInt(2, 6)
    val b = r.nextInt(2, 10)
    val c = r.nextInt(2, 10)
    val word = listOf("two", "three", "four", "five")[a - 2]
    return buildQuestion(
        r, Topic.WORD_PROBLEMS,
        "\"$b less than $word times a number n is equal to $c more than the number.\" Which equation matches this sentence?",
        m("${a}n - $b = n + $c"),
        listOf(m("$b - ${a}n = n + $c"), m("$a(n - $b) = n + $c"), m("${a}n - $b = ${c}n"), m("${a}n + $b = n - $c")),
        "Translate one piece at a time.\n\n" +
            "• \"$word times a number n\" → ${m("${a}n")}\n" +
            "• \"$b less than\" that → ${m("${a}n - $b")} (start with ${m("${a}n")}, then take $b away)\n" +
            "• \"is equal to\" → ${m("=")}\n• \"$c more than the number\" → ${m("n + $c")}\n\n" +
            "Trap: \"$b less than X\" is ${m("X - $b")}, not ${m("$b - X")}.",
        filler = { m("${a}n - $b = n + ${c + it + 1}") },
    )
}

// ---------------------------------------------------------------- Exponents & roots

private fun mono(coef: Int, xe: Int, ye: Int): String = "$coef${powTex("x", xe)}${powTex("y", ye)}"

private fun powerOfMonomial(r: Random): Question {
    val a = r.nextInt(2, 4)
    val mx = r.nextInt(2, 5)
    val n = r.nextInt(1, 4)
    val k = r.nextInt(2, 4)
    val ak = ipow(a, k)
    return buildQuestion(
        r, Topic.EXPONENTS,
        "Which expression is equivalent to ${m("\\left(${mono(a, mx, n)}\\right)^{$k}")}?",
        m(mono(ak, mx * k, n * k)),
        listOf(m(mono(a * k, mx * k, n * k)), m(mono(ak, mx + k, n + k)), m(mono(a, mx * k, n * k)), m(mono(a * k, mx + k, n + k))),
        "A power outside the parentheses goes to EVERY factor inside.\n\n" +
            "• ${m("$a^{$k} = $ak")}\n" +
            "• ${m("\\left(x^{$mx}\\right)^{$k} = x^{${mx * k}}")}  (multiply exponents: ${m("$mx \\times $k")})\n" +
            "• ${m("\\left(${powTex("y", n)}\\right)^{$k} = ${powTex("y", n * k)}")}\n\n" +
            "Answer: ${m(mono(ak, mx * k, n * k))}\n\n" +
            "Trap: the coefficient $a is RAISED to the power $k, not multiplied by $k.",
        filler = { m(mono(ak + it + 1, mx * k, n * k)) },
    )
}

private fun productOfMonomials(r: Random): Question {
    val a = r.nextInt(2, 7); val b = r.nextInt(2, 7)
    val p = r.nextInt(2, 6); val q = r.nextInt(1, 5)
    val s = r.nextInt(2, 6); val t = r.nextInt(1, 5)
    return buildQuestion(
        r, Topic.EXPONENTS,
        "Which expression is equivalent to ${m("\\left(${mono(a, p, q)}\\right)\\left(${mono(b, s, t)}\\right)")}?",
        m(mono(a * b, p + s, q + t)),
        listOf(m(mono(a * b, p * s, q * t)), m(mono(a + b, p + s, q + t)), m(mono(a + b, p * s, q * t)), m(mono(a * b, p + s, q * t))),
        "Multiply the numbers. Then ADD the exponents of matching letters.\n\n" +
            "• ${m("$a \\times $b = ${a * b}")}\n" +
            "• ${m("x^{$p} \\cdot x^{$s} = x^{${p + s}}")}\n" +
            "• ${m("${powTex("y", q)} \\cdot ${powTex("y", t)} = ${powTex("y", q + t)}")}\n\n" +
            "Answer: ${m(mono(a * b, p + s, q + t))}\n\n" +
            "Rule: same base, multiplying → add exponents. Power of a power → multiply exponents.",
        filler = { m(mono(a * b + it + 1, p + s, q + t)) },
    )
}

private fun sameBaseEquation(r: Random): Question {
    while (true) {
        val a = r.nextInt(1, 6)
        val b = r.nextInt(1, 6)
        if (a == b) continue
        val k = r.nextInt(1, 5)
        if ((b * k) % (b - a) != 0) continue
        val x = b * k / (b - a)
        val baseA = 1 shl a
        val baseB = 1 shl b
        return buildQuestion(
            r, Topic.EXPONENTS,
            "What value of ${m("x")} makes this equation true?\n\n${m("$baseA^{x} = $baseB^{x - $k}")}",
            m("$x"),
            listOf(m("${-x}"), m("$k"), m("${x + 1}"), m("${b * k}")),
            "Write both sides as powers of 2.\n\n" +
                "• ${m("$baseA = 2^{$a}")}, so ${m("$baseA^{x} = 2^{${xTex(a)}}")}\n" +
                "• ${m("$baseB = 2^{$b}")}, so ${m("$baseB^{x - $k} = 2^{$b(x - $k)}")}\n\n" +
                "Same base, so the exponents are equal:\n" +
                m("${xTex(a)} = ${b}x - ${b * k}") + "\n" +
                (if (b > a) m("${b * k} = ${xTex(b - a)}") else m("${xTex(a - b)} = -${b * k}")) + "\n" +
                m("x = $x"),
            filler = { m("${x + it + 2}") },
        )
    }
}

private fun addRadicals(r: Random): Question {
    val b = listOf(2, 3, 5, 6, 7).random(r)
    val a = r.nextInt(2, 6)
    var c: Int
    do { c = r.nextInt(2, 7) } while (c == a)
    val n1 = a * a * b
    val n2 = c * c * b
    val correct = "${a + c}\\sqrt{$b}"
    return buildQuestion(
        r, Topic.EXPONENTS,
        "Which expression is equivalent to ${m("\\sqrt{$n1} + \\sqrt{$n2}")}?",
        m(correct),
        listOf(m(rootTex(n1 + n2).let { if (it == correct) "${a * c}\\sqrt{$b}" else it }), m("${a + c}\\sqrt{${2 * b}}"), m("${a * c}\\sqrt{$b}"), m("\\sqrt{${n1 + n2 + b}}")),
        "Pull perfect squares out of each root first.\n\n" +
            "• ${m("\\sqrt{$n1} = \\sqrt{${a * a} \\cdot $b} = $a\\sqrt{$b}")}\n" +
            "• ${m("\\sqrt{$n2} = \\sqrt{${c * c} \\cdot $b} = $c\\sqrt{$b}")}\n\n" +
            "Now they are like terms (both have ${m("\\sqrt{$b}")}):\n" +
            m("$a\\sqrt{$b} + $c\\sqrt{$b} = $correct") + "\n\n" +
            "Trap: ${m("\\sqrt{$n1} + \\sqrt{$n2}")} is NOT ${m("\\sqrt{${n1 + n2}}")}. You cannot add under one root.",
        filler = { m("${a + c + it + 1}\\sqrt{$b}") },
    )
}

private fun fractionalExponent(r: Random): Question {
    val root = r.nextInt(2, 5)
    val n = if (root == 2) r.nextInt(2, 6) else r.nextInt(2, 4)
    var mm: Int
    do { mm = r.nextInt(1, n + 1) } while (gcd(mm, n) != 1 && n > 1)
    val base = ipow(root, n)
    val value = ipow(root, mm)
    val negative = r.nextInt(4) == 0
    val exp = (if (negative) "-" else "") + tfrac(mm, n)
    val correct = if (negative) tfrac(1, value) else "$value"
    return buildQuestion(
        r, Topic.EXPONENTS,
        "What is the value of ${m("$base^{$exp}")}?",
        m(correct),
        if (negative) listOf(m("-$value"), m("$value"), m("-" + tfrac(1, value)), m(tfrac(1, base * mm)))
        else listOf(m(if (base * mm % n == 0) "${base * mm / n}" else "${value + root}"), m("${root * mm}"), m("${value * root}"), m("${base / n}")),
        "A fraction exponent ${m(tfrac("m", "n"))} means: take the n-th root, then raise to the m-th power.\n\n" +
            "• The ${ordinal(n)} root of $base is $root, because ${m("$root^{$n} = $base")}\n" +
            "• ${m("$root^{$mm} = $value")}\n" +
            (if (negative) "• A negative exponent flips it: ${m(tfrac(1, value))}\n\nA negative exponent never makes the answer negative."
            else "\nTake the root first. It keeps the numbers small."),
        filler = { m("${value + root * (it + 2)}") },
    )
}

private fun ordinal(n: Int) = when (n) { 2 -> "square"; 3 -> "cube"; else -> "${n}th" }

// ---------------------------------------------------------------- Rewriting equations

private class FormulaItem(val prompt: String, val correct: String, val wrong: List<String>, val explanation: String)

/** Builds a step list: one equation per line, each with an optional note before it. */
private fun steps(vararg s: Pair<String, String>) = s.joinToString("\n") { (note, tex) -> if (note.isEmpty()) m(tex) else "$note: ${m(tex)}" }

private val FORMULAS = listOf(
    FormulaItem(
        "${m("A = P(1 + rt)")}. Which expression gives ${m("t")} in terms of ${m("A")}, ${m("P")}, and ${m("r")}?",
        m("t = \\frac{A - P}{Pr}"),
        listOf(m("t = \\frac{A - P}{r}"), m("t = \\frac{A}{Pr} - P"), m("t = \\frac{A - 1}{Pr}")),
        "Undo the steps from the outside in.\n\n" + steps(
            "" to "A = P(1 + rt)", "Divide by P" to "\\frac{A}{P} = 1 + rt", "Subtract 1" to "\\frac{A}{P} - 1 = rt",
            "Divide by r" to "t = \\frac{\\frac{A}{P} - 1}{r}", "Multiply top and bottom by P" to "t = \\frac{A - P}{Pr}",
        ),
    ),
    FormulaItem(
        "${m("F = \\frac{9}{5}C + 32")}. Which expression gives ${m("C")} in terms of ${m("F")}?",
        m("C = \\frac{5}{9}(F - 32)"),
        listOf(m("C = \\frac{5}{9}F - 32"), m("C = \\frac{9}{5}(F - 32)"), m("C = \\frac{5}{9}(F + 32)")),
        steps("" to "F = \\frac{9}{5}C + 32", "Subtract 32 FIRST" to "F - 32 = \\frac{9}{5}C", "Multiply by 5/9" to "C = \\frac{5}{9}(F - 32)") +
            "\n\nTrap: ${m("\\frac{5}{9}F - 32")} subtracts 32 too late.",
    ),
    FormulaItem(
        "${m("V = \\frac{1}{3}\\pi r^{2}h")}. Which expression gives ${m("h")} in terms of ${m("V")} and ${m("r")}?",
        m("h = \\frac{3V}{\\pi r^{2}}"),
        listOf(m("h = \\frac{V}{3\\pi r^{2}}"), m("h = 3V\\pi r^{2}"), m("h = \\frac{\\pi r^{2}}{3V}")),
        steps("" to "V = \\frac{1}{3}\\pi r^{2}h", "Multiply by 3" to "3V = \\pi r^{2}h", "Divide by πr²" to "h = \\frac{3V}{\\pi r^{2}}"),
    ),
    FormulaItem(
        "${m("ax + by = c")}. Which expression gives ${m("y")} in terms of ${m("a")}, ${m("b")}, ${m("c")}, and ${m("x")}?",
        m("y = \\frac{c - ax}{b}"),
        listOf(m("y = \\frac{c + ax}{b}"), m("y = \\frac{c}{b} - ax"), m("y = \\frac{ax - c}{b}")),
        steps("" to "ax + by = c", "Subtract ax" to "by = c - ax", "Divide EVERYTHING by b" to "y = \\frac{c - ax}{b}") +
            "\n\nTrap: ${m("\\frac{c}{b} - ax")} divides only part of the right side.",
    ),
    FormulaItem(
        "${m("\\frac{1}{f} = \\frac{1}{a} + \\frac{1}{b}")}. Which expression gives ${m("f")} in terms of ${m("a")} and ${m("b")}?",
        m("f = \\frac{ab}{a + b}"),
        listOf(m("f = a + b"), m("f = \\frac{a + b}{ab}"), m("f = \\frac{1}{a} + b")),
        "Add the fractions on the right with the common denominator ${m("ab")}:\n" +
            m("\\frac{1}{a} + \\frac{1}{b} = \\frac{b}{ab} + \\frac{a}{ab} = \\frac{a + b}{ab}") + "\n\n" +
            "So ${m("\\frac{1}{f} = \\frac{a + b}{ab}")}. Flip both sides:\n" + m("f = \\frac{ab}{a + b}") + "\n\n" +
            "Trap: ${m("\\frac{1}{f} = \\frac{1}{a} + \\frac{1}{b}")} does NOT mean ${m("f = a + b")}.",
    ),
    FormulaItem(
        "${m("S = 2\\pi r^{2} + 2\\pi rh")}. Which expression gives ${m("h")} in terms of ${m("S")} and ${m("r")}?",
        m("h = \\frac{S - 2\\pi r^{2}}{2\\pi r}"),
        listOf(m("h = \\frac{S - 2\\pi r^{2}}{2\\pi}"), m("h = \\frac{S}{2\\pi r} - 2\\pi r^{2}"), m("h = \\frac{S - 2\\pi r}{2\\pi r^{2}}")),
        steps("" to "S = 2\\pi r^{2} + 2\\pi rh", "Subtract 2πr²" to "S - 2\\pi r^{2} = 2\\pi rh", "Divide by 2πr" to "h = \\frac{S - 2\\pi r^{2}}{2\\pi r}"),
    ),
    FormulaItem(
        "${m("E = \\frac{1}{2}mv^{2}")}. If ${m("v > 0")}, which expression gives ${m("v")} in terms of ${m("E")} and ${m("m")}?",
        m("v = \\sqrt{\\frac{2E}{m}}"),
        listOf(m("v = \\frac{2E}{m}"), m("v = \\sqrt{\\frac{E}{2m}}"), m("v = \\left(\\frac{2E}{m}\\right)^{2}")),
        steps("" to "E = \\frac{1}{2}mv^{2}", "Multiply by 2" to "2E = mv^{2}", "Divide by m" to "v^{2} = \\frac{2E}{m}", "Take the square root" to "v = \\sqrt{\\frac{2E}{m}}"),
    ),
    FormulaItem(
        "${m("y = \\frac{x + 3}{x - 2}")}. Which expression gives ${m("x")} in terms of ${m("y")}?",
        m("x = \\frac{2y + 3}{y - 1}"),
        listOf(m("x = \\frac{3 - 2y}{y - 1}"), m("x = \\frac{y + 3}{y - 2}"), m("x = \\frac{2y - 3}{y + 1}")),
        steps(
            "" to "y = \\frac{x + 3}{x - 2}", "Multiply by (x − 2)" to "y(x - 2) = x + 3", "Distribute" to "xy - 2y = x + 3",
            "Get the x terms on one side" to "xy - x = 2y + 3", "Factor out x" to "x(y - 1) = 2y + 3", "Divide" to "x = \\frac{2y + 3}{y - 1}",
        ),
    ),
)

private fun solveFormula(r: Random): Question {
    val f = FORMULAS.random(r)
    return buildQuestion(r, Topic.REWRITING, f.prompt, f.correct, f.wrong, f.explanation, filler = { error("formula choices must be distinct") })
}

private fun solveLinearNumbers(r: Random): Question {
    val k = r.nextInt(2, 7)
    val a = r.nextInt(1, 9) * r.sign()
    val x = r.nextInt(-6, 10)
    val c = r.nextInt(1, 12) * r.sign()
    val d = k * (x - a) + c
    val inner = if (a < 0) "x + ${-a}" else "x - $a"
    val cTerm = if (c < 0) "- ${-c}" else "+ $c"
    return buildQuestion(
        r, Topic.REWRITING,
        "If ${m("$k($inner) $cTerm = $d")}, what is the value of ${m("x")}?",
        m("$x"),
        listOf(m("${x + 2 * a}"), m("${x - 2 * a}"), mf(Frac.of(d - c + a, k)), mf(Frac.of(d + c, k) + Frac.of(a, 1))),
        "Undo things in reverse order.\n\n" + steps(
            (if (c < 0) "Add ${-c}" else "Subtract $c") to "$k($inner) = ${d - c}",
            "Divide by $k" to "$inner = ${(d - c) / k}",
            (if (a < 0) "Subtract ${-a}" else "Add $a") to "x = $x",
        ),
        filler = { m("${x + it + 3}") },
    )
}

// ---------------------------------------------------------------- Perimeter, area, volume

private fun rectanglePerimeterArea(r: Random): Question {
    val w = r.nextInt(3, 13)
    val d = r.nextInt(2, 9)
    val l = w + d
    val p = 2 * (l + w)
    return buildQuestion(
        r, Topic.AREA_VOLUME,
        "A rectangular herb garden is $d feet longer than it is wide. Its perimeter is $p feet. What is its area, in square feet?",
        "${l * w}",
        listOf("${w * w}", "${l * l}", "${(p / 4) * (p / 4)}", "${l * w + d}"),
        "Let the width be ${m("w")}. Then the length is ${m("w + $d")}.\n\n" + steps(
            "Perimeter" to "2w + 2(w + $d) = $p", "" to "4w + ${2 * d} = $p", "" to "4w = ${p - 2 * d}", "" to "w = $w",
        ) + "\n\nSo the length is $l, and the area is ${m("$l \\times $w = ${l * w}")}.",
        filler = { "${l * w + 3 * (it + 2)}" },
    ).copy(diagram = Diagram.Rectangle(l.toDouble(), w.toDouble(), "w + $d", "w"))
}

private fun scaleFactorVolume(r: Random): Question {
    val a = r.nextInt(2, 4)
    val hb = listOf(Frac.of(1, 2), Frac.of(1, 1), Frac.of(2, 1), Frac.of(3, 1)).random(r)
    val factor = Frac.of(a * a, 1) * hb
    val hWord = when (hb) {
        Frac.of(1, 2) -> "the height is cut in half"
        Frac.of(1, 1) -> "the height stays the same"
        else -> "the height is multiplied by ${hb.n}"
    }
    return buildQuestion(
        r, Topic.AREA_VOLUME,
        "Hexie's cauldron is a cylinder. She makes a new cauldron: the radius is multiplied by $a, and $hWord. The new volume is the old volume multiplied by what number?",
        mf(factor),
        listOf(mf(Frac.of(a, 1) * hb), mf(Frac.of(a * a * a, 1) * hb), mf(Frac.of(a, 1) + hb), mf(Frac.of(2 * a, 1))),
        "Cylinder volume: ${m("V = \\pi r^{2}h")}\n\n" +
            "The radius is SQUARED, so multiplying ${m("r")} by $a multiplies ${m("V")} by ${m("$a^{2} = ${a * a}")}.\n" +
            "The height is not squared, so it multiplies ${m("V")} by ${mf(hb)}.\n\n" +
            "Total: ${m("${a * a} \\times ${hb.tex()} = ${factor.tex()}")}",
        filler = { mf(factor + Frac.of(it + 1, 1)) },
    ).copy(diagram = Diagram.Cylinder("r", "h"))
}

private fun cylinderVolume(r: Random): Question {
    val rad = r.nextInt(2, 8)
    val h = r.nextInt(2, 11)
    return buildQuestion(
        r, Topic.AREA_VOLUME,
        "A cylindrical potion jar has a radius of $rad inches and a height of $h inches. What is its volume, in cubic inches?",
        m("${rad * rad * h}\\pi"),
        listOf(m("${2 * rad * h}\\pi"), m("${rad * h * h}\\pi"), m("${2 * rad * rad * h}\\pi"), m("${rad * h}\\pi")),
        m("V = \\pi r^{2}h = \\pi \\cdot $rad^{2} \\cdot $h = \\pi \\cdot ${rad * rad} \\cdot $h = ${rad * rad * h}\\pi") + "\n\n" +
            "Trap: ${m("${2 * rad * h}\\pi")} uses ${m("2\\pi rh")}. That is the area of the jar's side, not its volume.",
        filler = { m("${rad * rad * h + it + 1}\\pi") },
    ).copy(diagram = Diagram.Cylinder("$rad in", "$h in"))
}

private fun circleFromCircumference(r: Random): Question {
    val rad = r.nextInt(2, 13)
    return buildQuestion(
        r, Topic.AREA_VOLUME,
        "A magic circle has a circumference of ${m("${2 * rad}\\pi")} meters. What is its area, in square meters?",
        m("${rad * rad}\\pi"),
        listOf(m("${4 * rad * rad}\\pi"), m("${2 * rad}\\pi"), m("$rad\\pi"), m("${rad * rad * 2}\\pi")),
        "Circumference: ${m("2\\pi r = ${2 * rad}\\pi")}, so ${m("r = $rad")}.\n\n" +
            "Area: ${m("\\pi r^{2} = \\pi \\cdot $rad^{2} = ${rad * rad}\\pi")}\n\n" +
            "Trap: ${m("${4 * rad * rad}\\pi")} uses the diameter (${2 * rad}) in place of the radius.",
        filler = { m("${rad * rad + it + 1}\\pi") },
    ).copy(diagram = Diagram.Circle("r", "Circumference = ${2 * rad}π m"))
}

// ---------------------------------------------------------------- Slope-intercept

private fun lineThroughPoints(r: Random): Question {
    var mm: Int
    do { mm = r.nextInt(-4, 5) } while (mm == 0)
    val b = r.nextInt(-6, 7)
    val x1 = r.nextInt(-4, 3)
    val x2 = x1 + r.nextInt(1, 4)
    val y1 = mm * x1 + b
    val y2 = mm * x2 + b
    val mfr = Frac.of(mm, 1)
    val bf = Frac.of(b, 1)
    return buildQuestion(
        r, Topic.SLOPE,
        "Which equation describes the line that passes through ${m("($x1, $y1)")} and ${m("($x2, $y2)")}?",
        m(lineTex(mfr, bf)),
        listOf(
            m(lineTex(Frac.of(1, mm), bf)),
            m(if (b != 0) lineTex(mfr, Frac.of(-b, 1)) else lineTex(mfr, Frac.of(y1, 1))),
            m(lineTex(Frac.of(-mm, 1), bf)),
            m(lineTex(mfr, Frac.of(y1, 1))),
        ),
        "Step 1: the slope is the change in y over the change in x.\n" +
            m("m = \\frac{$y2 - ${par(y1)}}{$x2 - ${par(x1)}} = ${tfrac(y2 - y1, x2 - x1)} = $mm") + "\n\n" +
            "Step 2: put one point into ${m("y = ${xTex(mm)} + b")}:\n" +
            m("$y1 = $mm($x1) + b") + "\n" + m("$y1 = ${mm * x1} + b") + "\n" + m("b = $b") + "\n\n" +
            "Answer: ${m(lineTex(mfr, bf))}",
        filler = { m(lineTex(mfr, Frac.of(b + it + 1, 1))) },
    ).copy(diagram = Diagram.Plane(listOf(Diagram.PlanePoint(x1, y1), Diagram.PlanePoint(x2, y2)), listOf(Diagram.PlaneLine(mm.toDouble(), b.toDouble()))))
}

private fun perpendicularLine(r: Random): Question {
    val mm = listOf(Frac.of(2, 1), Frac.of(3, 1), Frac.of(-2, 1), Frac.of(1, 2), Frac.of(-1, 3), Frac.of(2, 3), Frac.of(-3, 2)).random(r)
    val b0 = r.nextInt(-5, 6)
    val perp = Frac.of(-mm.d, mm.n)
    val px = (perp.d * r.nextInt(-2, 3)).toInt()
    val py = r.nextInt(-5, 6)
    val b = Frac.of(py, 1) - perp * Frac.of(px, 1)
    fun through(s: Frac) = Frac.of(py, 1) - s * Frac.of(px, 1)
    return buildQuestion(
        r, Topic.SLOPE,
        "Which line is perpendicular to ${m(lineTex(mm, Frac.of(b0, 1)))} and passes through the point ${m("($px, $py)")}?",
        m(lineTex(perp, b)),
        listOf(
            m(lineTex(mm, through(mm))),
            m(lineTex(Frac.of(mm.d, mm.n), through(Frac.of(mm.d, mm.n)))),
            m(lineTex(Frac.of(-mm.n, mm.d), through(Frac.of(-mm.n, mm.d)))),
            m(lineTex(perp, Frac.of(b0, 1))),
        ),
        "Perpendicular slopes are NEGATIVE RECIPROCALS: flip the fraction and change the sign.\n\n" +
            "• Old slope: ${mf(mm)}\n• New slope: ${mf(perp)}\n\n" +
            "Put the point ${m("($px, $py)")} into ${m("y = ${xTex(perp)} + b")}:\n" +
            m("$py = ${perp.tex()} \\cdot ${par(px)} + b") + "\n" + m("b = ${b.tex()}") + "\n\n" +
            "Answer: ${m(lineTex(perp, b))}",
        filler = { m(lineTex(perp, b + Frac.of(it + 1, 1))) },
    ).copy(
        diagram = Diagram.Plane(listOf(Diagram.PlanePoint(px, py)), listOf(Diagram.PlaneLine(mm.toDouble(), b0.toDouble(), lineString(mm, Frac.of(b0, 1))))),
        explanationDiagram = Diagram.Plane(
            listOf(Diagram.PlanePoint(px, py)),
            listOf(Diagram.PlaneLine(mm.toDouble(), b0.toDouble()), Diagram.PlaneLine(perp.toDouble(), b.toDouble(), lineString(perp, b))),
        ),
    )
}

private fun slopeFromStandardForm(r: Random): Question {
    var a: Int; var b: Int
    do { a = r.nextInt(1, 8) * r.sign(); b = r.nextInt(1, 8) * r.sign() } while (abs(a) == abs(b))
    val c = r.nextInt(1, 20)
    val slope = Frac.of(-a, b)
    fun coef(n: Int) = when (n) { 1 -> ""; -1 -> "-"; else -> "$n" }
    val eq = "${coef(a)}x ${if (b < 0) "-" else "+"} ${coef(abs(b))}y = $c"
    return buildQuestion(
        r, Topic.SLOPE,
        "What is the slope of the line ${m(eq)}?",
        mf(slope),
        listOf(mf(Frac.of(a, b)), mf(Frac.of(b, a)), mf(Frac.of(-b, a)), mf(Frac.of(c, b))),
        "Solve for ${m("y")} to get the form ${m("y = mx + b")}.\n\n" +
            m(eq) + "\n" + m("${coef(b)}y = ${xTex(-a)} + $c") + "\n" + m(lineTex(slope, Frac.of(c, b))) + "\n\n" +
            "The slope is the number in front of ${m("x")}: ${mf(slope)}\n\n" +
            "Shortcut: for ${m("Ax + By = C")}, the slope is ${m("-\\frac{A}{B}")}.",
        filler = { mf(slope + Frac.of(it + 1, 1)) },
    )
}

// ---------------------------------------------------------------- Lines & angles

/** "3x + 5" for k = 3, c = 5. Drops a zero constant and a coefficient of 1. */
private fun lin(k: Int, c: Int) = "${if (k == 1) "" else k}x" + when {
    c > 0 -> " + $c"
    c < 0 -> " - ${-c}"
    else -> ""
}

private fun triangleAngles(r: Random): Question {
    while (true) {
        val x = r.nextInt(8, 31)
        val k1 = r.nextInt(1, 4); val k2 = r.nextInt(2, 5)
        val c1 = r.nextInt(-10, 21); val c2 = r.nextInt(-10, 21)
        val a1 = k1 * x + c1; val a2 = k2 * x + c2
        val t = 180 - a1 - a2
        if (a1 < 10 || a2 < 10 || t < 15 || t > 120) continue
        val sumC = c1 + c2 + t
        return buildQuestion(
            r, Topic.ANGLES,
            "The angles of a triangle measure ${m("(${lin(k1, c1)})^{\\circ}")}, ${m("(${lin(k2, c2)})^{\\circ}")}, and ${m("$t^{\\circ}")}. What is the value of ${m("x")}?",
            m("$x"),
            listOf(
                m(Frac.of(360 - t - c1 - c2, k1 + k2).let { if (it.d == 1L) "$it" else "${x + 5}" }),
                m(Frac.of(180 - t, k1 + k2).let { if (it.d == 1L) "$it" else "${x - 3}" }),
                m("$a2"), m("${x + 2}"),
            ),
            "The angles of a triangle add to ${m("180^{\\circ}")}.\n\n" + steps(
                "" to "(${lin(k1, c1)}) + (${lin(k2, c2)}) + $t = 180",
                "" to "${k1 + k2}x ${if (sumC < 0) "- ${-sumC}" else "+ $sumC"} = 180",
                "" to "${k1 + k2}x = ${180 - sumC}",
                "" to "x = $x",
            ) + "\n\nCheck: ${m("$a1^{\\circ} + $a2^{\\circ} + $t^{\\circ} = 180^{\\circ}")}. ✓",
            filler = { m("${x + it + 4}") },
        ).copy(diagram = Diagram.Triangle(a1.toDouble(), a2.toDouble(), labelA = "(${lin(k1, c1).replace("-", "−")})°", labelB = "(${lin(k2, c2).replace("-", "−")})°", labelC = "$t°", vertexNames = false))
    }
}

private fun parallelLines(r: Random): Question {
    while (true) {
        val supplementary = r.nextBoolean()
        val x = r.nextInt(5, 31)
        val k1 = r.nextInt(2, 6); val k2 = r.nextInt(2, 6)
        if (k1 == k2) continue
        val c1 = r.nextInt(-20, 31)
        val angle1 = k1 * x + c1
        val angle2 = if (supplementary) 180 - angle1 else angle1
        val c2 = angle2 - k2 * x
        if (angle1 !in 20..160 || angle1 == 90) continue
        val e1 = lin(k1, c1); val e2 = lin(k2, c2)
        val kind = if (supplementary) "same-side interior angles" else "alternate interior angles"
        val solve = if (supplementary) steps("" to "($e1) + ($e2) = 180", "" to "x = $x") else steps("" to "$e1 = $e2", "" to "x = $x")
        return buildQuestion(
            r, Topic.ANGLES,
            "Two parallel lines are cut by a transversal. A pair of $kind measure ${m("($e1)^{\\circ}")} and ${m("($e2)^{\\circ}")}. What is the measure of the angle ${m("($e1)^{\\circ}")}?",
            m("$angle1^{\\circ}"),
            listOf(m("${180 - angle1}^{\\circ}"), m("$x^{\\circ}"), m("${angle1 + 10}^{\\circ}"), m("${90 - x % 90}^{\\circ}")),
            (if (supplementary) "Same-side interior angles are SUPPLEMENTARY. They add to ${m("180^{\\circ}")}.\n\n"
            else "Alternate interior angles are EQUAL.\n\n") + solve +
                "\n\nThe question asks for the ANGLE, not ${m("x")}:\n${m("$k1($x) ${if (c1 < 0) "- ${-c1}" else "+ $c1"} = $angle1^{\\circ}")}\n\nTrap: stopping at ${m("x = $x")}.",
            filler = { m("${angle1 + 5 * (it + 3)}^{\\circ}") },
        ).copy(diagram = Diagram.ParallelLines(angle1.toDouble(), "(${e1.replace("-", "−")})°", "(${e2.replace("-", "−")})°", supplementary))
    }
}

private fun polygonInteriorAngle(r: Random): Question {
    val (n, name) = listOf(5 to "pentagon", 6 to "hexagon", 8 to "octagon", 9 to "nonagon", 10 to "decagon", 12 to "dodecagon").random(r)
    val each = 180 * (n - 2) / n
    fun deg(v: Int) = m("$v^{\\circ}")
    return buildQuestion(
        r, Topic.ANGLES,
        "Hexie's magic rune is a regular $name ($n equal sides). What is the measure of each interior angle?",
        deg(each),
        listOf(deg(360 / n), deg(180 * (n - 2)), deg(180 - each / 2), deg(each - 10)),
        "The interior angles of an n-sided polygon add to ${m("(n - 2) \\cdot 180^{\\circ}")}.\n\n" +
            "• Sum: ${m("($n - 2) \\cdot 180^{\\circ} = ${180 * (n - 2)}^{\\circ}")}\n" +
            "• Regular means all $n angles are equal: ${m("${tfrac("${180 * (n - 2)}^{\\circ}", n)} = $each^{\\circ}")}\n\n" +
            "Shortcut: each exterior angle is ${m("${tfrac("360^{\\circ}", n)} = ${360 / n}^{\\circ}")}, and the interior angle is ${m("180^{\\circ} - ${360 / n}^{\\circ} = $each^{\\circ}")}.",
        filler = { deg(each + 5 * (it + 1)) },
    ).copy(diagram = Diagram.Polygon(n, "?"))
}

// ---------------------------------------------------------------- Fractions & operations

private fun orderOfOperationsFractions(r: Random): Question {
    val a = Frac.of(r.nextInt(1, 5), r.nextInt(2, 7))
    val b = Frac.of(r.nextInt(1, 5), r.nextInt(2, 6))
    val c = Frac.of(r.nextInt(1, 6), r.nextInt(2, 6))
    val correct = a + b * c
    return buildQuestion(
        r, Topic.FRACTIONS,
        "What is the value of ${m("${a.tex()} + ${b.tex()} \\times ${c.tex()}")}?",
        mf(correct),
        listOf(mf((a + b) * c), mf(a * b + c), mf(Frac.of(a.n + b.n * c.n, a.d + b.d * c.d)), mf(a + b + c)),
        "Order of operations: multiply BEFORE you add.\n\n" +
            "• ${m("${b.tex()} \\times ${c.tex()} = ${(b * c).tex()}")}\n" +
            "• ${m("${a.tex()} + ${(b * c).tex()} = ${correct.tex()}")}\n\n" +
            "Trap: ${m("\\left(${a.tex()} + ${b.tex()}\\right) \\times ${c.tex()} = ${((a + b) * c).tex()}")} adds first.",
        filler = { mf(correct + Frac.of(it + 1, 2)) },
    )
}

private fun complexFraction(r: Random): Question {
    var a: Int; var b: Int
    do { a = r.nextInt(2, 7); b = r.nextInt(2, 9) } while (a == b)
    val c = r.nextInt(2, 6)
    val sum = Frac.of(1, a) + Frac.of(1, b)
    val correct = sum * Frac.of(c, 1)
    return buildQuestion(
        r, Topic.FRACTIONS,
        "What is the value of ${m("\\frac{\\frac{1}{$a} + \\frac{1}{$b}}{\\frac{1}{$c}}")}?",
        mf(correct),
        listOf(mf(sum / Frac.of(c, 1)), mf(Frac.of(2 * c, a + b)), mf(Frac.of(c, a + b)), mf(Frac.of(c, a * b))),
        "• Top: ${m("\\frac{1}{$a} + \\frac{1}{$b} = ${tfrac(b, a * b)} + ${tfrac(a, a * b)} = ${sum.tex()}")}\n" +
            "• Dividing by ${m(tfrac(1, c))} is the same as multiplying by $c.\n\n" +
            m("${sum.tex()} \\times $c = ${correct.tex()}") + "\n\n" +
            "Trap: ${m("\\frac{1}{$a} + \\frac{1}{$b}")} is NOT ${m(tfrac(2, a + b))}.",
        filler = { mf(correct + Frac.of(it + 1, 1)) },
    )
}

private fun evaluateWithNegatives(r: Random): Question {
    val k = r.nextInt(2, 7)
    val x = -k
    val mm = r.nextInt(1, 10)
    val absPart = abs(x - mm)
    val correct = x * x - 3 * x + absPart
    return buildQuestion(
        r, Topic.FRACTIONS,
        "If ${m("x = -$k")}, what is the value of ${m("x^{2} - 3x + |x - $mm|")}?",
        m("$correct"),
        listOf(m("${-k * k + 3 * k + absPart}"), m("${k * k + 3 * k + (x - mm)}"), m("${k * k - 3 * k + absPart}"), m("${correct + 2 * mm}")),
        "Put ${m("(-$k)")} in with parentheses.\n\n" +
            "• ${m("x^{2} = (-$k)^{2} = ${k * k}")}  (a negative squared is positive)\n" +
            "• ${m("-3x = -3(-$k) = ${3 * k}")}\n" +
            "• ${m("|x - $mm| = |-$k - $mm| = |${x - mm}| = $absPart")}\n\n" +
            m("${k * k} + ${3 * k} + $absPart = $correct"),
        filler = { m("${correct + it + 1}") },
    )
}

// ---------------------------------------------------------------- Unit circle & trig

private fun quadrantTrig(r: Random): Question {
    val (p, q, h) = listOf(Triple(3, 4, 5), Triple(5, 12, 13), Triple(8, 15, 17), Triple(7, 24, 25)).random(r)
    val (opp, adj) = if (r.nextBoolean()) p to q else q to p
    val quad = listOf(2, 3, 4).random(r)
    val sinSign = if (quad == 2) 1 else -1
    val cosSign = if (quad == 4) 1 else -1
    val qName = listOf("", "I", "II", "III", "IV")[quad]
    fun s(sign: Int, n: Int, d: Int) = (if (sign < 0) "-" else "") + tfrac(n, d)
    val askTan = r.nextBoolean()
    val fn = if (askTan) "\\tan" else "\\cos"
    val correct = if (askTan) s(sinSign * cosSign, opp, adj) else s(cosSign, adj, h)
    val wrong = if (askTan) listOf(s(-sinSign * cosSign, opp, adj), s(sinSign * cosSign, adj, opp), s(cosSign, adj, h))
    else listOf(s(-cosSign, adj, h), s(cosSign, opp, h), s(cosSign, h, adj))
    fun sign(v: Int) = if (v > 0) "positive" else "negative"
    return buildQuestion(
        r, Topic.UNIT_CIRCLE,
        "If ${m("\\sin\\theta = ${s(sinSign, opp, h)}")} and ${m("\\theta")} is in Quadrant $qName, what is ${m("$fn\\theta")}?",
        m(correct), wrong.map(::m),
        "Draw a right triangle with opposite side $opp and hypotenuse $h. The Pythagorean theorem gives the third side:\n" +
            m("\\sqrt{$h^{2} - $opp^{2}} = \\sqrt{${h * h - opp * opp}} = $adj") + "\n\n" +
            "In Quadrant $qName, sine is ${sign(sinSign)} and cosine is ${sign(cosSign)}" +
            (if (askTan) ", so tangent is ${sign(sinSign * cosSign)}" else "") + ".\n" +
            "(Remember \"All Students Take Calculus\": Quadrant I all positive, II sin, III tan, IV cos.)\n\n" +
            (if (askTan) m("\\tan\\theta = \\frac{\\text{opposite}}{\\text{adjacent}} = $correct")
            else m("\\cos\\theta = \\frac{\\text{adjacent}}{\\text{hypotenuse}} = $correct")),
        filler = { m(if (askTan) s(-sinSign * cosSign, adj, opp) else s(-cosSign, opp, h)) },
    ).copy(
        explanationDiagram = Diagram.UnitCircle(
            degrees = Math.toDegrees(kotlin.math.atan2(opp.toDouble(), adj.toDouble())).let { ref ->
                when (quad) { 2 -> 180 - ref; 3 -> 180 + ref; else -> 360 - ref }
            },
            angleLabel = "θ",
            legs = Triple("$opp", "$adj", "$h"),
        ),
    )
}

private class Special(val deg: Int, val rad: String, val radPlain: String, val sin: String, val cos: String)

private val SPECIALS = listOf(
    Special(30, "\\frac{\\pi}{6}", "π/6", "\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}"),
    Special(45, "\\frac{\\pi}{4}", "π/4", "\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}"),
    Special(60, "\\frac{\\pi}{3}", "π/3", "\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}"),
    Special(120, "\\frac{2\\pi}{3}", "2π/3", "\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}"),
    Special(135, "\\frac{3\\pi}{4}", "3π/4", "\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{2}}{2}"),
    Special(150, "\\frac{5\\pi}{6}", "5π/6", "\\frac{1}{2}", "-\\frac{\\sqrt{3}}{2}"),
    Special(210, "\\frac{7\\pi}{6}", "7π/6", "-\\frac{1}{2}", "-\\frac{\\sqrt{3}}{2}"),
    Special(225, "\\frac{5\\pi}{4}", "5π/4", "-\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{2}}{2}"),
    Special(240, "\\frac{4\\pi}{3}", "4π/3", "-\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}"),
    Special(300, "\\frac{5\\pi}{3}", "5π/3", "-\\frac{\\sqrt{3}}{2}", "\\frac{1}{2}"),
    Special(315, "\\frac{7\\pi}{4}", "7π/4", "-\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{2}}{2}"),
    Special(330, "\\frac{11\\pi}{6}", "11π/6", "-\\frac{1}{2}", "\\frac{\\sqrt{3}}{2}"),
)

private fun specialAngle(r: Random): Question {
    val s = SPECIALS.random(r)
    val askSin = r.nextBoolean()
    val fn = if (askSin) "\\sin" else "\\cos"
    val correct = if (askSin) s.sin else s.cos
    val other = if (askSin) s.cos else s.sin
    val unsigned = correct.removePrefix("-")
    val flip = if (correct.startsWith("-")) unsigned else "-$correct"
    val ref = when { s.deg < 90 -> s.deg; s.deg < 180 -> 180 - s.deg; s.deg < 270 -> s.deg - 180; else -> 360 - s.deg }
    val pool = listOf("\\frac{1}{2}", "\\frac{\\sqrt{2}}{2}", "\\frac{\\sqrt{3}}{2}", "-\\frac{1}{2}", "-\\frac{\\sqrt{2}}{2}", "-\\frac{\\sqrt{3}}{2}", "1", "-1")
    val part = if (askSin) "sine is the y-value" else "cosine is the x-value"
    return buildQuestion(
        r, Topic.UNIT_CIRCLE,
        "What is the exact value of ${m("$fn\\left(${s.rad}\\right)")}?",
        m(correct),
        listOf(m(flip), m(other), m(other.removePrefix("-").let { if (it == unsigned) "1" else it })),
        "${m(s.rad)} radians is ${m("${s.deg}^{\\circ}")}.\n\n" +
            "• Reference angle: ${m("$ref^{\\circ}")}, and ${m("$fn $ref^{\\circ} = $unsigned")}\n" +
            "• ${m("${s.deg}^{\\circ}")} is in Quadrant ${quadrant(s.deg)}. On the unit circle, $part, and here it is ${if (correct.startsWith("-")) "negative" else "positive"}.\n\n" +
            m("$fn\\left(${s.rad}\\right) = $correct"),
        filler = { m(pool.shuffled(r)[it % pool.size]) },
    ).copy(explanationDiagram = Diagram.UnitCircle(s.deg.toDouble(), s.radPlain))
}

private fun quadrant(deg: Int) = when { deg < 90 -> "I"; deg < 180 -> "II"; deg < 270 -> "III"; else -> "IV" }

private fun degreesToRadians(r: Random): Question {
    val deg = listOf(20, 36, 40, 72, 100, 135, 150, 210, 240, 270, 300, 330).random(r)
    val f = Frac.of(deg, 180)
    fun piTex(x: Frac) = when {
        x.n == 1L && x.d == 1L -> "\\pi"
        x.d == 1L -> "${x.n}\\pi"
        x.n == 1L -> "\\frac{\\pi}{${x.d}}"
        else -> "\\frac{${x.n}\\pi}{${x.d}}"
    }
    return buildQuestion(
        r, Topic.UNIT_CIRCLE,
        "Hexie's broom turns through an angle of ${m("$deg^{\\circ}")}. What is this angle in radians?",
        m(piTex(f)),
        listOf(m(piTex(Frac.of(180, deg))), m(piTex(Frac.of(deg, 360))), m(piTex(Frac.of(deg, 90))), m(if (deg % 2 == 0) "${deg / 2}\\pi" else "$deg\\pi")),
        "${m("180^{\\circ} = \\pi")} radians. So multiply by ${m("\\frac{\\pi}{180}")}.\n\n" +
            m("$deg \\cdot \\frac{\\pi}{180} = ${piTex(f)}"),
        filler = { m(piTex(f + Frac.of(it + 1, 6))) },
    ).copy(diagram = Diagram.UnitCircle(deg.toDouble(), "$deg°"))
}

// ---------------------------------------------------------------- Logarithms

private fun log(b: Any) = "\\log_{$b}"

private fun logToExponent(r: Random): Question {
    val b = r.nextInt(2, 6)
    val k = r.nextInt(2, if (b <= 3) 5 else 4)
    val x = ipow(b, k)
    return buildQuestion(
        r, Topic.LOGARITHMS,
        "If ${m("${log(b)}(x) = $k")}, what is the value of ${m("x")}?",
        m("$x"),
        listOf(m("${b * k}"), m(if (ipow(k, b) != x) "${ipow(k, b)}" else "${x + b}"), m("${b + k}"), mf(Frac.of(k, b))),
        "A log is an exponent in disguise.\n\n" +
            "${m("${log(b)}(x) = $k")} means \"$b to the power $k is x\".\n\n" +
            m("x = $b^{$k} = $x"),
        filler = { m("${x + it + 1}") },
    )
}

private fun evaluateLog(r: Random): Question {
    val b = r.nextInt(2, 6)
    val k = r.nextInt(2, 5)
    val inverse = r.nextBoolean()
    val v = ipow(b, k)
    val arg = if (inverse) tfrac(1, v) else "$v"
    val ans = if (inverse) -k else k
    return buildQuestion(
        r, Topic.LOGARITHMS,
        "What is the value of ${m("${log(b)}\\left($arg\\right)")}?",
        m("$ans"),
        listOf(m("${-ans}"), m(tfrac(1, k)), m(if (inverse) "-" + tfrac(1, k) else "${v / b}"), m("$v")),
        "${m("${log(b)}\\left($arg\\right)")} asks: \"$b to WHAT power gives ${m(arg)}?\"\n\n" +
            (if (inverse) "${m("$b^{$k} = $v")}, and a negative exponent flips it: ${m("$b^{-$k} = ${tfrac(1, v)}")}.\n\nSo the answer is ${m("-$k")}."
            else "${m("$b^{$k} = $v")}, so the answer is $k."),
        filler = { m("${ans + it + 2}") },
    )
}

private fun logRules(r: Random): Question {
    val p = r.nextInt(2, 8)
    val q = r.nextInt(2, 8)
    val mx = r.nextInt(1, 4)
    val ny = r.nextInt(1, 4)
    val divide = r.nextBoolean()
    val arg = if (divide) tfrac(powTex("x", mx), powTex("y", ny)) else powTex("x", mx) + powTex("y", ny)
    val expr = "\\log_{b}\\left($arg\\right)"
    val correct = if (divide) mx * p - ny * q else mx * p + ny * q
    val op = if (divide) "-" else "+"
    return buildQuestion(
        r, Topic.LOGARITHMS,
        "If ${m("\\log_{b}x = $p")} and ${m("\\log_{b}y = $q")}, what is the value of ${m(expr)}?",
        m("$correct"),
        listOf(m("${if (divide) mx * p + ny * q else mx * p - ny * q}"), m("${ipow(p, mx) * ipow(q, ny)}"), m("${(mx * p) * (ny * q)}"), m("${p + q}")),
        "Log rules:\n" +
            "• ${m("\\log(AB) = \\log A + \\log B")}\n" +
            "• ${m("\\log\\frac{A}{B} = \\log A - \\log B")}\n" +
            "• ${m("\\log A^{n} = n\\log A")}\n\n" +
            steps("" to "$expr = $mx\\log_{b}x $op $ny\\log_{b}y", "" to "= $mx($p) $op $ny($q)", "" to "= $correct"),
        filler = { m("${correct + it + 1}") },
    )
}

private fun solveLog(r: Random): Question {
    val b = r.nextInt(2, 4)
    val k = r.nextInt(2, 6)
    val a = r.nextInt(1, 10) * r.sign()
    val x = ipow(b, k) - a
    val inner = if (a < 0) "x - ${-a}" else "x + $a"
    return buildQuestion(
        r, Topic.LOGARITHMS,
        "What value of ${m("x")} makes ${m("${log(b)}($inner) = $k")} true?",
        m("$x"),
        listOf(m("${ipow(b, k) + a}"), m("${b * k - a}"), m(if (ipow(k, b) != ipow(b, k)) "${ipow(k, b) - a}" else "${x + 2}"), m("${ipow(b, k)}")),
        "Rewrite the log as an exponent:\n" + m("$inner = $b^{$k} = ${ipow(b, k)}") + "\n\n" +
            "${if (a < 0) "Add ${-a}" else "Subtract $a"}: ${m("x = $x")}",
        filler = { m("${x + it + 3}") },
    )
}

private fun logProduct(r: Random): Question {
    val options = listOf(
        Triple(6, 4 to 9, 2), Triple(6, 2 to 18, 2), Triple(6, 3 to 12, 2), Triple(6, 12 to 18, 3),
        Triple(10, 4 to 25, 2), Triple(10, 2 to 50, 2), Triple(10, 20 to 5, 2), Triple(10, 8 to 125, 3),
        Triple(12, 8 to 18, 2), Triple(12, 16 to 9, 2),
    )
    val (b, pair, k) = options.random(r)
    val (p, q) = pair
    return buildQuestion(
        r, Topic.LOGARITHMS,
        "What is the value of ${m("${log(b)}$p + ${log(b)}$q")}?",
        m("$k"),
        listOf(m("${log(b)}${p + q}"), m("${k + 1}"), m("${k - 1}"), m("${p * q}")),
        "Neither log is nice by itself. Use the rule ${m("\\log A + \\log B = \\log(AB)")}.\n\n" +
            m("${log(b)}$p + ${log(b)}$q = ${log(b)}($p \\cdot $q) = ${log(b)}${p * q}") + "\n\n" +
            "${m("$b^{$k} = ${p * q}")}, so the answer is $k.",
        filler = { m("${k + it + 2}") },
    )
}

// ---------------------------------------------------------------- Law of sines & cosines

private fun lawOfCosinesSide(r: Random): Question {
    while (true) {
        val a = r.nextInt(2, 11)
        val b = r.nextInt(2, 11)
        if (a == b) continue
        val obtuse = r.nextBoolean()
        val angle = if (obtuse) 120 else 60
        val c2 = if (obtuse) a * a + b * b + a * b else a * a + b * b - a * b
        val wrongSign = if (obtuse) a * a + b * b - a * b else a * a + b * b + a * b
        val correct = rootTex(c2)
        val cosTex = if (obtuse) "-\\frac{1}{2}" else "\\frac{1}{2}"
        return buildQuestion(
            r, Topic.LAW_SINES_COSINES,
            "In triangle ABC, side ${m("a = $a")}, side ${m("b = $b")}, and the angle between them, ${m("\\angle C")}, measures ${m("$angle^{\\circ}")}. What is the length of side ${m("c")}? Use ${m("\\cos $angle^{\\circ} = $cosTex")}.",
            m(correct),
            listOf(m(rootTex(wrongSign)), m(rootTex(a * a + b * b)), m("${a + b}"), m(rootTex(c2 + a * b).let { if (it == correct) "${a * b}" else it })),
            "Law of Cosines: ${m("c^{2} = a^{2} + b^{2} - 2ab\\cos C")}\n\n" + steps(
                "" to "c^{2} = $a^{2} + $b^{2} - 2($a)($b)\\left($cosTex\\right)",
                "" to "c^{2} = ${a * a} + ${b * b} ${if (obtuse) "+" else "-"} ${a * b}",
                "" to "c^{2} = $c2",
                "" to "c = $correct",
            ) + "\n\n" +
                (if (obtuse) "Watch the sign: ${m("\\cos 120^{\\circ}")} is negative, so the minus becomes a plus."
                else "Note: ${m(rootTex(a * a + b * b))} would be right only for a ${m("90^{\\circ}")} angle."),
            filler = { m(rootTex(c2 + it + 1)) },
        ).copy(diagram = Diagram.Triangle.fromSides(a.toDouble(), b.toDouble(), kotlin.math.sqrt(c2.toDouble())).copy(sideA = "$a", sideB = "$b", sideC = "?", labelC = "$angle°"))
    }
}

private fun lawOfSinesSide(r: Random): Question {
    val angA = listOf(35, 40, 50, 55, 65, 70).random(r)
    var angB: Int
    do { angB = listOf(25, 30, 40, 45, 60, 75).random(r) } while (angB == angA || angA + angB >= 150)
    val angC = 180 - angA - angB
    val a = r.nextInt(6, 21)
    val askC = r.nextBoolean()
    val target = if (askC) angC else angB
    val label = if (askC) "c" else "b"
    fun expr(top: Int, bottom: Int) = "\\frac{$a\\sin $top^{\\circ}}{\\sin $bottom^{\\circ}}"
    return buildQuestion(
        r, Topic.LAW_SINES_COSINES,
        "In triangle ABC, ${m("\\angle A = $angA^{\\circ}")}, ${m("\\angle B = $angB^{\\circ}")}, and side ${m("a = $a")}. Side ${m("a")} is opposite ${m("\\angle A")}. Which expression gives the length of side ${m(label)}?",
        m(expr(target, angA)),
        listOf(m(expr(angA, target)), m("\\frac{\\sin $target^{\\circ}}{$a\\sin $angA^{\\circ}}"), m(if (askC) expr(angB, angA) else expr(angC, angA))),
        "Law of Sines: ${m("\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C}")}. Each side pairs with the angle OPPOSITE it.\n\n" +
            (if (askC) "First find ${m("\\angle C")}: ${m("180^{\\circ} - $angA^{\\circ} - $angB^{\\circ} = $angC^{\\circ}")}\n\n" else "") +
            m("\\frac{$label}{\\sin $target^{\\circ}} = \\frac{$a}{\\sin $angA^{\\circ}}") + "\n" +
            "Multiply both sides by ${m("\\sin $target^{\\circ}")}:\n" + m("$label = ${expr(target, angA)}"),
        filler = { m(expr(target + 5 * (it + 1), angA)) },
    ).copy(diagram = Diagram.Triangle(angA.toDouble(), angB.toDouble(), sideA = "$a", sideB = if (askC) null else "?", sideC = if (askC) "?" else null, labelA = "$angA°", labelB = "$angB°"))
}

private fun lawOfCosinesAngle(r: Random): Question {
    while (true) {
        val a = r.nextInt(3, 10)
        val b = r.nextInt(3, 10)
        val c = r.nextInt(3, 12)
        if (a + b <= c || a + c <= b || b + c <= a) continue
        val num = a * a + b * b - c * c
        if (num == 0) continue
        val cos = Frac.of(num, 2 * a * b)
        return buildQuestion(
            r, Topic.LAW_SINES_COSINES,
            "A triangle has sides of length $a, $b, and $c. Let ${m("C")} be the angle opposite the side of length $c. What is ${m("\\cos C")}?",
            mf(cos),
            listOf(mf(Frac.of(-num, 2 * a * b)), mf(Frac.of(num, a * b)), mf(Frac.of(a * a + b * b + c * c, 2 * a * b)), mf(Frac.of(num, 2 * a * c))),
            "Law of Cosines, solved for the angle:\n" + m("\\cos C = \\frac{a^{2} + b^{2} - c^{2}}{2ab}") + "\n\n" +
                "The side OPPOSITE angle ${m("C")} is $c, so it gets the minus sign.\n\n" + steps(
                    "" to "\\cos C = \\frac{$a^{2} + $b^{2} - $c^{2}}{2 \\cdot $a \\cdot $b}",
                    "" to "= \\frac{${a * a} + ${b * b} - ${c * c}}{${2 * a * b}}",
                    "" to "= ${tfrac(num, 2 * a * b)}${reduced(num, 2 * a * b, cos)}",
                ) + (if (num < 0) "\n\nA negative cosine means angle ${m("C")} is obtuse (more than ${m("90^{\\circ}")})." else ""),
            filler = { mf(cos + Frac.of(it + 1, 2 * a * b)) },
        ).copy(diagram = Diagram.Triangle.fromSides(a.toDouble(), b.toDouble(), c.toDouble()).copy(sideA = "$a", sideB = "$b", sideC = "$c", labelC = "?"))
    }
}
