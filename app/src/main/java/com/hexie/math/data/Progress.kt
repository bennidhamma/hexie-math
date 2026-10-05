package com.hexie.math.data

import android.content.Context
import com.hexie.math.questions.Topic
import org.json.JSONObject
import java.time.LocalDate

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
    fun pickTopic(random: kotlin.random.Random, avoid: Topic? = null): Topic {
        val stats = topicStats()
        val weights = Topic.entries.map { t ->
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
}
