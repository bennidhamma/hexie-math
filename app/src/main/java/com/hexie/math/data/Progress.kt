package com.hexie.math.data

import android.content.Context
import com.hexie.math.questions.Bank
import com.hexie.math.questions.Question
import com.hexie.math.questions.Topic
import org.json.JSONArray
import org.json.JSONObject
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

/** Settings, streak, and per-topic stats. Stored in SharedPreferences. */
class Progress(context: Context) {

    private val prefs = context.applicationContext.getSharedPreferences("hexie", Context.MODE_PRIVATE)

    var problemsPerDay: Int
        get() = prefs.getInt("perDay", 3)
        set(v) = prefs.edit().putInt("perDay", v.coerceIn(1, 5)).apply()

    var remindersOn: Boolean
        get() = prefs.getBoolean("remind", true)
        set(v) = prefs.edit().putBoolean("remind", v).apply()

    var reminderHour: Int
        get() = prefs.getInt("hour", 16)
        set(v) = prefs.edit().putInt("hour", v).apply()

    var reminderMinute: Int
        get() = prefs.getInt("minute", 30)
        set(v) = prefs.edit().putInt("minute", v).apply()

    var showPaceTimer: Boolean
        get() = prefs.getBoolean("paceTimer", true)
        set(v) = prefs.edit().putBoolean("paceTimer", v).apply()

    /** Where "Send feedback" addresses its email. Set on the device, so it is not in the public code. */
    var parentEmail: String
        get() = prefs.getString("parentEmail", "") ?: ""
        set(v) = prefs.edit().putString("parentEmail", v.trim()).apply()

    var askedNotificationPermission: Boolean
        get() = prefs.getBoolean("askedPerm", false)
        set(v) = prefs.edit().putBoolean("askedPerm", v).apply()

    /** Eyes of newt: one for each correct answer. Pure bragging rights. */
    val newtEyes: Int get() = prefs.getInt("newts", 0)

    val bestStreak: Int get() = prefs.getInt("best", 0)

    /** Problems answered today, counted toward the daily goal. */
    fun doneToday(today: LocalDate = LocalDate.now()): Int =
        if (prefs.getString("day", null) == today.toString()) prefs.getInt("dayCount", 0) else 0

    fun goalMetToday(today: LocalDate = LocalDate.now()) = doneToday(today) >= problemsPerDay

    /** The streak still alive today: the goal was met today or yesterday. */
    fun currentStreak(today: LocalDate = LocalDate.now()): Int {
        val last = prefs.getString("lastGoal", null)?.let(LocalDate::parse) ?: return 0
        return if (last == today || last == today.minusDays(1)) prefs.getInt("streak", 0) else 0
    }

    /** Records one answer. Returns true if this answer completed today's goal. */
    fun record(question: Question, correct: Boolean, today: LocalDate = LocalDate.now()): Boolean {
        question.family?.let { recordFamily(it, correct, today) }
        return record(question.topic, correct, today)
    }

    fun record(topic: Topic, correct: Boolean, today: LocalDate = LocalDate.now()): Boolean {
        val stats = topicStats()
        val (c, w) = stats[topic] ?: (0 to 0)
        stats[topic] = if (correct) (c + 1) to w else c to (w + 1)
        val json = JSONObject()
        stats.forEach { (t, cw) -> json.put(t.name, "${cw.first},${cw.second}") }

        val wasMet = goalMetToday(today)
        val count = doneToday(today) + 1
        val edit = prefs.edit()
            .putString("stats", json.toString())
            .putString("day", today.toString())
            .putInt("dayCount", count)
        if (correct) edit.putInt("newts", newtEyes + 1)

        val nowMet = !wasMet && count >= problemsPerDay
        if (nowMet) {
            val streak = currentStreak(today) + 1
            edit.putInt("streak", streak)
                .putString("lastGoal", today.toString())
                .putInt("best", maxOf(bestStreak, streak))
        }
        edit.apply()
        return nowMet
    }

    /** Topic → (correct, wrong). */
    fun topicStats(): MutableMap<Topic, Pair<Int, Int>> {
        val out = mutableMapOf<Topic, Pair<Int, Int>>()
        val raw = prefs.getString("stats", null) ?: return out
        val json = JSONObject(raw)
        for (t in Topic.entries) {
            val v = json.optString(t.name, "").split(",")
            if (v.size == 2) out[t] = v[0].toInt() to v[1].toInt()
        }
        return out
    }

    /**
     * Picks a topic. Topics from the score report start with a higher weight.
     * Misses raise a topic's weight. A run of correct answers lowers it, but never to zero.
     */
    fun pickTopic(random: kotlin.random.Random, avoid: Topic? = null, available: Set<Topic> = Topic.entries.toSet()): Topic {
        val stats = topicStats()
        val weights = Topic.entries.filter { it in available }.map { t ->
            val (c, w) = stats[t] ?: (0 to 0)
            val adaptive = (1.0 + 2.0 * w) / (1.0 + 0.5 * c)
            val weight = t.baseWeight * adaptive.coerceIn(0.35, 4.0)
            t to if (t == avoid) weight * 0.2 else weight
        }
        var roll = random.nextDouble() * weights.sumOf { it.second }
        for ((t, w) in weights) {
            roll -= w
            if (roll <= 0) return t
        }
        return weights.last().first
    }

    // ------------------------------------------------------------ problem bank

    /** family -> (correct, wrong, day of last attempt as epoch day) */
    private fun families(): JSONObject = JSONObject(prefs.getString("families", "{}") ?: "{}")

    private fun recordFamily(family: String, correct: Boolean, today: LocalDate) {
        val all = families()
        val (c, w) = all.optString(family, "0,0,0").split(",").map { it.toLong() }.let { it[0] to it[1] }
        all.put(family, "${if (correct) c + 1 else c},${if (correct) w else w + 1},${today.toEpochDay()}")
        // A miss that was answered right the last time counts as fixed: the latest result decides.
        all.put("$family!last", if (correct) "right" else "wrong")
        prefs.edit().putString("families", all.toString()).apply()
    }

    /**
     * Picks a bank problem in [topic]. Order of preference:
     * 1. a family the student missed last time, at least 3 days ago (spaced review);
     * 2. a family the student has not seen;
     * 3. the family seen longest ago.
     * Then picks a random number variation, so a review is not the exact same problem.
     */
    fun pickBankQuestion(bank: Bank, topic: Topic, random: kotlin.random.Random, today: LocalDate = LocalDate.now()): Question? {
        val families = bank.byTopic[topic] ?: return null
        val seen = families()
        fun lastDay(f: String) = seen.optString(f, "").split(",").getOrNull(2)?.toLongOrNull()
        val review = families.keys.filter {
            seen.optString("$it!last") == "wrong" && (lastDay(it) ?: Long.MAX_VALUE) <= today.toEpochDay() - 3
        }
        val unseen = families.keys.filter { lastDay(it) == null }
        val family = when {
            review.isNotEmpty() -> review.random(random)
            unseen.isNotEmpty() -> unseen.random(random)
            else -> families.keys.minBy { lastDay(it) ?: 0L }
        }
        return families.getValue(family).random(random)
    }

    // ------------------------------------------------------------ feedback

    data class Feedback(val time: String, val kind: String, val about: String, val reason: String, val note: String)

    private val stamp = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")

    fun addFeedback(kind: String, about: String, reason: String, note: String) {
        val all = JSONArray(prefs.getString("feedback", "[]"))
        all.put(JSONObject().put("time", LocalDateTime.now().format(stamp)).put("kind", kind).put("about", about).put("reason", reason).put("note", note))
        prefs.edit().putString("feedback", all.toString()).apply()
    }

    fun allFeedback(): List<Feedback> {
        val all = JSONArray(prefs.getString("feedback", "[]"))
        return (0 until all.length()).map { i ->
            all.getJSONObject(i).let { Feedback(it.getString("time"), it.getString("kind"), it.getString("about"), it.getString("reason"), it.getString("note")) }
        }
    }

    /** How many feedback items have not gone into an email yet. */
    val unsentFeedback: Int get() = allFeedback().size - prefs.getInt("feedbackSent", 0)

    fun unsentFeedbackItems(): List<Feedback> = allFeedback().drop(prefs.getInt("feedbackSent", 0))

    fun markFeedbackSent() = prefs.edit().putInt("feedbackSent", allFeedback().size).apply()
}
