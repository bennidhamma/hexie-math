package com.hexie.math

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.hexie.math.questions.QuestionFactory
import com.hexie.math.ui.Cream
import com.hexie.math.ui.ExplanationCard
import com.hexie.math.ui.HexieTheme
import com.hexie.math.ui.QuestionBody
import com.hexie.math.ui.loadBank
import kotlin.random.Random
import kotlin.reflect.KCallable

/**
 * Debug builds only. Shows one generated question for screenshots.
 * Extras: "gen" (generator index), "seed", and "part" ("q" for the question, "e" for the explanation).
 * Every launch logs the generator list under the tag HexieReview.
 */
class ReviewActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val gens = QuestionFactory.allGenerators()
        gens.forEachIndexed { i, (topic, gen) ->
            Log.i("HexieReview", "GEN $i ${topic.name} ${(gen as? KCallable<*>)?.name ?: "gen$i"}")
        }
        val index = intent.getIntExtra("gen", 0).coerceIn(gens.indices)
        val seed = intent.getIntExtra("seed", 1)
        val part = intent.getStringExtra("part") ?: "q"
        // "bank" picks a problem-bank version by id, like "PROB-03#0", in place of a generator.
        val bankId = intent.getStringExtra("bank")
        val q = bankId?.let { id -> loadBank(this).problems.firstOrNull { it.bankId == id } } ?: gens[index].second(Random(seed))
        val topic = q.topic
        setContent {
            HexieTheme {
                Column(Modifier.fillMaxSize().background(Cream).padding(horizontal = 20.dp, vertical = 16.dp)) {
                    Text(
                        if (bankId != null) "$bankId" else "${topic.label.uppercase()}  ·  #$index  ·  seed $seed",
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.primary,
                    )
                    Spacer(Modifier.height(8.dp))
                    if (part == "q") QuestionBody(q, picked = null, onPick = {})
                    else ExplanationCard(q, correct = false)
                }
            }
        }
    }
}
