package com.hexie.math.ui

import android.content.Context
import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.hexie.math.data.Progress
import com.hexie.math.questions.Bank
import com.hexie.math.questions.DataTable
import com.hexie.math.questions.Figure
import com.hexie.math.questions.Question
import kotlinx.coroutines.delay

/** Loads the problem bank from assets. An app built without bank.json uses only the generators. */
fun loadBank(context: Context): Bank = runCatching {
    Bank.parse(context.assets.open("bank.json").bufferedReader().use { it.readText() })
}.getOrDefault(Bank.EMPTY)

/** A data table with math in its cells. Scrolls sideways if it is too wide. */
@Composable
fun DataTableView(t: DataTable) {
    val line = MaterialTheme.colorScheme.outline
    Column {
        t.caption?.let {
            MathText(it, style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Bold))
            Spacer(Modifier.height(6.dp))
        }
        // Every column gets the same share of the width, so the cells line up like a printed table.
        Column(Modifier.fillMaxWidth().border(BorderStroke(1.dp, line), RoundedCornerShape(8.dp)).clip(RoundedCornerShape(8.dp))) {
            val all = listOf(t.headers) + t.rows
            all.forEachIndexed { r, row ->
                Row(
                    Modifier.fillMaxWidth().height(IntrinsicSize.Min)
                        .background(if (r == 0) MaterialTheme.colorScheme.primaryContainer else if (r % 2 == 0) Color(0xFFFAF6FC) else Color.White)
                ) {
                    row.forEachIndexed { c, cell ->
                        Box(
                            Modifier.weight(if (c == 0) 1.3f else 1f).fillMaxHeight()
                                .border(BorderStroke(0.5.dp, line.copy(alpha = 0.6f))).padding(horizontal = 8.dp, vertical = 8.dp)
                        ) {
                            MathText(cell, style = MaterialTheme.typography.bodyMedium.copy(fontWeight = if (r == 0) FontWeight.Bold else FontWeight.Normal))
                        }
                    }
                }
            }
        }
    }
}

/** A figure image from assets, on white, with the ACT "not drawn to scale" note when it applies. */
@Composable
fun FigureImage(f: Figure) {
    val context = LocalContext.current
    val bitmap = remember(f.asset) {
        runCatching { context.assets.open(f.asset).use { BitmapFactory.decodeStream(it) }?.asImageBitmap() }.getOrNull()
    }
    Column(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(Color.White)
            .border(BorderStroke(1.5.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.6f)), RoundedCornerShape(16.dp))
            .padding(8.dp)
    ) {
        if (bitmap != null) {
            Image(bitmap, contentDescription = f.alt, modifier = Modifier.fillMaxWidth(), contentScale = ContentScale.FillWidth)
        } else {
            Text("(Figure missing: ${f.alt})", style = MaterialTheme.typography.bodyMedium)
        }
        if (f.notToScale) {
            Text(
                "Note: Figure not drawn to scale.",
                Modifier.padding(start = 6.dp, top = 2.dp),
                fontSize = 13.sp, fontStyle = FontStyle.Italic, color = Color(0xFF5A4E66),
            )
        }
    }
}

/** Seconds since the question appeared. Orange after 60 seconds, the ACT pace. Stops when [running] is false. */
@Composable
fun PaceTimer(key: Any, running: Boolean) {
    var seconds by remember(key) { mutableIntStateOf(0) }
    LaunchedEffect(key, running) {
        while (running) {
            delay(1000)
            seconds++
        }
    }
    val late = seconds >= 60
    Text(
        "⏱ %d:%02d".format(seconds / 60, seconds % 60),
        style = MaterialTheme.typography.labelLarge,
        color = if (late) Color(0xFFD9652B) else MaterialTheme.colorScheme.onSurfaceVariant,
    )
}

private val FLAG_REASONS = listOf("Answer seems wrong", "Confusing wording", "Diagram problem", "Explanation unclear", "Too easy", "Too hard", "Other")

/** Short text that names a question in feedback: the bank id, or the start of the prompt for a warm-up. */
fun describe(q: Question): String =
    (q.bankId ?: "warm-up") + " [" + q.topic.label + "]: " + q.prompt.replace(Regex("\\\\[()]"), "").take(90)

/** The "flag this problem" dialog. */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun FlagDialog(question: Question, picked: Int?, progress: Progress, onDone: () -> Unit) {
    var reason by remember { mutableStateOf<String?>(null) }
    var note by remember { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = onDone,
        title = { Text("What's wrong with this one?") },
        text = {
            Column {
                FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    FLAG_REASONS.forEach { r ->
                        FilterChip(selected = reason == r, onClick = { reason = r }, label = { Text(r) })
                    }
                }
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(note, { note = it }, label = { Text("Anything else? (optional)") }, minLines = 2)
            }
        },
        confirmButton = {
            TextButton(enabled = reason != null, onClick = {
                val answer = picked?.let { " Picked ${"ABCD"[it]}, key ${"ABCD"[question.correctIndex]}." } ?: ""
                progress.addFeedback("problem", describe(question) + answer, reason!!, note)
                onDone()
            }) { Text("Send to the cauldron") }
        },
        dismissButton = { TextButton(onClick = onDone) { Text("Cancel") } },
    )
}

/** Opens the email app with all unsent feedback, addressed to the parent. Returns false if no email app exists. */
fun emailFeedback(context: Context, progress: Progress): Boolean {
    val items = progress.unsentFeedbackItems()
    val body = buildString {
        appendLine("Hexie Math feedback (${items.size} new)")
        appendLine("Streak: ${progress.currentStreak()} days. Eyes of newt: ${progress.newtEyes}.")
        appendLine()
        progress.topicStats().entries.sortedBy { it.key.ordinal }.forEach { (t, cw) ->
            appendLine("  ${t.label}: ${cw.first} right, ${cw.second} wrong")
        }
        appendLine()
        items.forEach { f ->
            appendLine("${f.time}  ${f.kind.uppercase()}: ${f.reason}")
            appendLine("  ${f.about}")
            if (f.note.isNotBlank()) appendLine("  Note: ${f.note}")
            appendLine()
        }
    }
    val intent = Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:")).apply {
        if (progress.parentEmail.isNotBlank()) putExtra(Intent.EXTRA_EMAIL, arrayOf(progress.parentEmail))
        putExtra(Intent.EXTRA_SUBJECT, "Hexie Math feedback")
        putExtra(Intent.EXTRA_TEXT, body)
    }
    return runCatching { context.startActivity(intent) }.isSuccess.also { if (it) progress.markFeedbackSent() }
}
