package com.hexie.math

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.hexie.math.questions.QuestionFactory
import com.hexie.math.ui.DiagramView
import com.hexie.math.ui.MathText
import androidx.compose.ui.text.TextStyle
import com.hexie.math.ui.HexieTheme
import kotlin.random.Random

/** Debug-only screen: one question per generator that has a diagram. Pass "seed" to vary them. */
class DiagramGalleryActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val seed = intent.getIntExtra("seed", 1)
        val questions = QuestionFactory.allGenerators()
            .map { (_, gen) -> gen(Random(seed)) }
            .filter { intent.getBooleanExtra("all", false) || it.diagram != null || it.explanationDiagram != null }
        setContent {
            HexieTheme {
                LazyColumn(Modifier.fillMaxSize().background(Color.White).safeDrawingPadding().padding(12.dp)) {
                    items(questions) { q ->
                        Column(Modifier.padding(vertical = 8.dp)) {
                            MathText(q.prompt, style = TextStyle(fontSize = 16.sp, lineHeight = 24.sp))
                            q.diagram?.let { DiagramView(it) }
                            q.choices.forEachIndexed { i, c ->
                                MathText((if (i == q.correctIndex) "✓ " else "    ") + c, Modifier.padding(vertical = 4.dp), style = TextStyle(fontSize = 17.sp))
                            }
                            MathText(q.explanation, style = TextStyle(fontSize = 15.sp, lineHeight = 22.sp, color = Color(0xFF1C3A16)))
                            q.explanationDiagram?.let { DiagramView(it) }
                            HorizontalDivider()
                        }
                    }
                }
            }
        }
    }
}
