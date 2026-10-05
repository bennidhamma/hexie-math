package com.hexie.math.questions

import org.json.JSONArray
import org.json.JSONObject

/**
 * The authored problem bank: ACT-style medium and hard problems, written by gpt-6-astra,
 * checked by independent solvers, with number variations from templates (see /bank in the repo).
 * The build script writes app/src/main/assets/bank.json.
 */
class Bank(val problems: List<Question>) {

    /** topic -> family -> variations */
    val byTopic: Map<Topic, Map<String, List<Question>>> =
        problems.groupBy { it.topic }.mapValues { (_, qs) -> qs.groupBy { it.family!! } }

    val topics: Set<Topic> get() = byTopic.keys

    /** Topics that have at least one problem at this difficulty ("medium" or "hard"). */
    fun topicsAt(difficulty: String): Set<Topic> =
        byTopic.filterValues { fams -> fams.values.any { it.first().difficulty == difficulty } }.keys

    companion object {
        val EMPTY = Bank(emptyList())

        fun parse(json: String): Bank {
            val arr = JSONArray(json)
            val out = ArrayList<Question>(arr.length())
            for (i in 0 until arr.length()) {
                val o = arr.getJSONObject(i)
                val topic = runCatching { Topic.valueOf(o.getString("topic")) }.getOrNull() ?: continue
                out += Question(
                    topic = topic,
                    prompt = o.getString("stem"),
                    choices = o.getJSONArray("choices").strings(),
                    correctIndex = o.getInt("answer"),
                    explanation = o.getString("explanation"),
                    table = o.optJSONObject("table")?.let(::table),
                    image = o.optJSONObject("figure")?.let {
                        Figure(it.getString("file"), it.optString("alt"), it.optBoolean("notToScale", false))
                    },
                    bankId = o.getString("id"),
                    difficulty = o.optString("difficulty").ifEmpty { null },
                )
            }
            return Bank(out)
        }

        private fun table(o: JSONObject) = DataTable(
            caption = o.optString("caption").ifEmpty { null },
            headers = o.getJSONArray("headers").strings(),
            rows = o.getJSONArray("rows").let { rows -> (0 until rows.length()).map { rows.getJSONArray(it).strings() } },
        )

        private fun JSONArray.strings() = (0 until length()).map { getString(it) }
    }
}
