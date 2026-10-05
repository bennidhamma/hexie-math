package com.hexie.math.ui

import android.app.TimePickerDialog
import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.hexie.math.data.Progress
import com.hexie.math.notify.Reminders
import com.hexie.math.questions.Diagram
import com.hexie.math.questions.Question
import com.hexie.math.questions.QuestionFactory
import com.hexie.math.questions.Topic
import kotlin.random.Random

private val GREETINGS = listOf(
    "Ready to do some math?",
    "Let's do some math!",
    "I know where you live... and I know your math isn't done. Hee hee!",
    "My cauldron is bubbling with fresh problems for you, dearie.",
    "Today's special: probability stew. Smells like fractions!",
    "My toad says you're going to crush this today.",
    "A few problems a day keeps the frog curse away.",
)
private val DONE_GREETINGS = listOf(
    "All done for today! You wonderful little menace.",
    "Goal brewed! Come back tomorrow, I'll have more.",
    "You're done! Want a bonus problem? I have extra eyes of newt.",
)
private val RIGHT = listOf(
    "Wickedly good!", "Cackle-tastic!", "Hex yes!", "My toad is impressed.",
    "That's the right potion!", "Brew-tiful work!", "You're a math witch now.",
)
private val WRONG = listOf(
    "Ooh, close! Let's look at the trick.",
    "Even witches spill the cauldron sometimes.",
    "No worries, dearie. Here's how it works.",
    "That one is sneaky. Let me show you.",
)

enum class Screen { HOME, QUIZ, DONE, SETTINGS }

@Composable
fun HexieApp(progress: Progress, startQuiz: Boolean, onStartQuizHandled: () -> Unit) {
    var screen by remember { mutableStateOf(Screen.HOME) }
    var refresh by remember { mutableIntStateOf(0) }
    var sessionSolved by remember { mutableIntStateOf(0) }
    var sessionRight by remember { mutableIntStateOf(0) }

    if (startQuiz) {
        screen = Screen.QUIZ
        onStartQuizHandled()
    }
    // Back returns to the home screen. It closes the app only from home.
    BackHandler(enabled = screen != Screen.HOME) {
        refresh++
        screen = Screen.HOME
    }

    Box(
        Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        when (screen) {
            Screen.HOME -> HomeScreen(
                progress, refresh,
                onStart = { screen = Screen.QUIZ },
                onSettings = { screen = Screen.SETTINGS },
            )
            Screen.QUIZ -> QuizScreen(
                progress,
                onFinish = { solved, right ->
                    sessionSolved = solved; sessionRight = right
                    refresh++
                    screen = if (solved == 0) Screen.HOME else Screen.DONE
                },
            )
            Screen.DONE -> DoneScreen(
                progress, sessionSolved, sessionRight,
                onBonus = { screen = Screen.QUIZ },
                onHome = { refresh++; screen = Screen.HOME },
            )
            Screen.SETTINGS -> SettingsScreen(progress, onBack = { refresh++; screen = Screen.HOME })
        }
    }
}

// ---------------------------------------------------------------- Home

@Composable
private fun HomeScreen(progress: Progress, refresh: Int, onStart: () -> Unit, onSettings: () -> Unit) {
    val done = remember(refresh) { progress.doneToday() }
    val goal = progress.problemsPerDay
    val met = done >= goal
    val greeting = remember(refresh) { if (met) DONE_GREETINGS.random() else GREETINGS.random() }

    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Pill("🔥 ${progress.currentStreak()} day${if (progress.currentStreak() == 1) "" else "s"}")
            Spacer(Modifier.width(8.dp))
            Pill("👁 ${progress.newtEyes} newt eyes")
            Spacer(Modifier.weight(1f))
            IconButton(onClick = onSettings) {
                Icon(Icons.Default.Settings, contentDescription = "Settings", tint = MaterialTheme.colorScheme.primary)
            }
        }

        Spacer(Modifier.height(8.dp))
        SpeechBubble(greeting)
        Hexie(if (met) Mood.CHEER else Mood.HAPPY, Modifier.size(220.dp))

        Text("Today's cauldron", style = MaterialTheme.typography.titleMedium)
        Spacer(Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            repeat(goal) { i ->
                Box(
                    Modifier
                        .size(22.dp)
                        .clip(CircleShape)
                        .background(if (i < done) MaterialTheme.colorScheme.secondary else MaterialTheme.colorScheme.outline.copy(alpha = 0.4f))
                )
            }
        }
        Spacer(Modifier.height(6.dp))
        Text(
            if (met) "Goal met: $done of $goal problems" else "$done of $goal problems done",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

        Spacer(Modifier.height(20.dp))
        Button(
            onClick = onStart,
            modifier = Modifier
                .fillMaxWidth()
                .height(60.dp),
            shape = RoundedCornerShape(20.dp),
        ) {
            Text(if (met) "Bonus problem!" else if (done == 0) "Let's brew some math!" else "Keep brewing!", fontSize = 19.sp)
        }

        Spacer(Modifier.height(28.dp))
        WatchList(progress, refresh)
    }
}

@Composable
private fun WatchList(progress: Progress, refresh: Int) {
    val stats = remember(refresh) { progress.topicStats() }
    Card(
        Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        shape = RoundedCornerShape(20.dp),
    ) {
        Column(Modifier.padding(16.dp)) {
            Text("Hexie's spell book", style = MaterialTheme.typography.titleMedium)
            Spacer(Modifier.height(4.dp))
            if (stats.isEmpty()) {
                Text(
                    "Hexie read your practice ACT. She will focus on probability, ratios, exponents, and the trickier " +
                        "topics like logarithms and the law of cosines. Your scores for each topic will show here.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            } else {
                Text(
                    "Topics you miss come back more often.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Spacer(Modifier.height(10.dp))
                stats.entries
                    .sortedBy { (_, cw) -> cw.first.toFloat() / (cw.first + cw.second) }
                    .forEach { (topic, cw) -> TopicRow(topic, cw.first, cw.second) }
            }
        }
    }
}

@Composable
private fun TopicRow(topic: Topic, right: Int, wrong: Int) {
    val total = right + wrong
    val frac = if (total == 0) 0f else right.toFloat() / total
    Column(Modifier.padding(vertical = 5.dp)) {
        Row {
            Text(topic.label, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.weight(1f))
            Text("$right / $total", style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Bold)
        }
        Spacer(Modifier.height(3.dp))
        LinearProgressIndicator(
            progress = { frac },
            modifier = Modifier
                .fillMaxWidth()
                .height(8.dp)
                .clip(RoundedCornerShape(4.dp)),
            color = if (frac >= 0.75f) RightGreen else if (frac >= 0.5f) Color(0xFFE0A030) else WrongRed,
            trackColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.3f),
            drawStopIndicator = {},
        )
    }
}

@Composable
private fun Pill(text: String) {
    Box(
        Modifier
            .clip(RoundedCornerShape(50))
            .background(MaterialTheme.colorScheme.primaryContainer)
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(text, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onPrimaryContainer)
    }
}

@Composable
private fun SpeechBubble(text: String, modifier: Modifier = Modifier) {
    Card(
        modifier.fillMaxWidth(),
        shape = RoundedCornerShape(topStart = 22.dp, topEnd = 22.dp, bottomEnd = 22.dp, bottomStart = 4.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(2.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.35f)),
    ) {
        Text(
            text,
            Modifier.padding(horizontal = 18.dp, vertical = 14.dp),
            style = MaterialTheme.typography.bodyLarge,
            fontWeight = FontWeight.Medium,
        )
    }
}

// ---------------------------------------------------------------- Quiz

@Composable
private fun QuizScreen(progress: Progress, onFinish: (solved: Int, right: Int) -> Unit) {
    val context = LocalContext.current
    // The daily goal sets the session length. After the goal, each session is one bonus problem.
    val total = remember { (progress.problemsPerDay - progress.doneToday()).coerceAtLeast(1) }
    val bonus = remember { progress.goalMetToday() }
    var index by remember { mutableIntStateOf(0) }
    var right by remember { mutableIntStateOf(0) }
    var lastTopic by remember { mutableStateOf<Topic?>(null) }
    var question by remember { mutableStateOf(newQuestion(progress, null)) }
    var picked by remember { mutableStateOf<Int?>(null) }
    var reaction by remember { mutableStateOf("") }

    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 12.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = { onFinish(index + if (picked != null) 1 else 0, right) }) {
                Icon(Icons.Default.Close, contentDescription = "Stop")
            }
            LinearProgressIndicator(
                progress = { (index + if (picked != null) 1 else 0).toFloat() / total },
                modifier = Modifier
                    .weight(1f)
                    .height(12.dp)
                    .clip(RoundedCornerShape(6.dp)),
                color = MaterialTheme.colorScheme.secondary,
                trackColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.3f),
                drawStopIndicator = {},
            )
            Spacer(Modifier.width(12.dp))
            Text(if (bonus) "Bonus" else "${index + 1}/$total", style = MaterialTheme.typography.labelLarge)
        }

        Spacer(Modifier.height(10.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            val mood = when {
                picked == null -> Mood.THINK
                picked == question.correctIndex -> Mood.CHEER
                else -> Mood.OOPS
            }
            Hexie(mood, Modifier.size(92.dp))
            Spacer(Modifier.width(8.dp))
            SpeechBubble(if (picked == null) "Hmm, what do you think?" else reaction)
        }

        Spacer(Modifier.height(12.dp))
        Text(
            question.topic.label.uppercase(),
            style = MaterialTheme.typography.labelLarge,
            color = MaterialTheme.colorScheme.primary,
            letterSpacing = 1.sp,
        )
        Spacer(Modifier.height(6.dp))
        MathText(question.prompt, style = MaterialTheme.typography.bodyLarge)
        question.figure?.let { fig ->
            Spacer(Modifier.height(12.dp))
            Box(
                Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant)
                    .horizontalScroll(rememberScrollState())
                    .padding(12.dp)
            ) {
                Text(fig, fontFamily = FontFamily.Monospace, fontSize = 14.sp, lineHeight = 20.sp)
            }
        }
        question.diagram?.let { d ->
            Spacer(Modifier.height(12.dp))
            DiagramCard(d)
        }

        Spacer(Modifier.height(16.dp))
        question.choices.forEachIndexed { i, choice ->
            ChoiceButton(
                letter = "ABCD"[i],
                text = choice,
                state = when {
                    picked == null -> ChoiceState.OPEN
                    i == question.correctIndex -> ChoiceState.RIGHT
                    i == picked -> ChoiceState.WRONG
                    else -> ChoiceState.DIM
                },
                onClick = {
                    if (picked == null) {
                        picked = i
                        val correct = i == question.correctIndex
                        if (correct) right++
                        reaction = if (correct) RIGHT.random() else WRONG.random()
                        val metNow = progress.record(question.topic, correct)
                        if (metNow) {
                            Reminders.clear(context)
                            Reminders.schedule(context)
                        }
                    }
                },
            )
            Spacer(Modifier.height(10.dp))
        }

        AnimatedVisibility(picked != null, enter = fadeIn() + slideInVertically { it / 4 }) {
            Column {
                Spacer(Modifier.height(6.dp))
                Card(
                    Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer),
                ) {
                    Column(Modifier.padding(16.dp)) {
                        val correct = picked == question.correctIndex
                        MathText(
                            if (correct) "✨ Correct! Here's why:" else "The answer is ${"ABCD"[question.correctIndex]}: ${question.choices[question.correctIndex]}",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onSecondaryContainer,
                        )
                        Spacer(Modifier.height(8.dp))
                        MathText(
                            question.explanation,
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSecondaryContainer,
                        )
                        question.explanationDiagram?.let { d ->
                            Spacer(Modifier.height(12.dp))
                            DiagramCard(d)
                        }
                    }
                }
                Spacer(Modifier.height(16.dp))
                Button(
                    onClick = {
                        if (index + 1 >= total) {
                            onFinish(index + 1, right)
                        } else {
                            index++
                            lastTopic = question.topic
                            question = newQuestion(progress, lastTopic)
                            picked = null
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(18.dp),
                ) {
                    Text(if (index + 1 >= total) "Finish" else "Next problem", fontSize = 18.sp)
                }
                Spacer(Modifier.height(24.dp))
            }
        }
    }
}

@Composable
private fun DiagramCard(d: Diagram) {
    Box(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(BorderStroke(1.5.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.6f)), RoundedCornerShape(16.dp))
            .padding(8.dp)
    ) {
        DiagramView(d)
    }
}

private fun newQuestion(progress: Progress, avoid: Topic?): Question =
    QuestionFactory.make(progress.pickTopic(Random.Default, avoid))

private enum class ChoiceState { OPEN, RIGHT, WRONG, DIM }

@Composable
private fun ChoiceButton(letter: Char, text: String, state: ChoiceState, onClick: () -> Unit) {
    val (bg, border, fg) = when (state) {
        ChoiceState.OPEN -> Triple(MaterialTheme.colorScheme.surface, MaterialTheme.colorScheme.outline, MaterialTheme.colorScheme.onSurface)
        ChoiceState.RIGHT -> Triple(RightGreen.copy(alpha = 0.14f), RightGreen, Color(0xFF1E5A2A))
        ChoiceState.WRONG -> Triple(WrongRed.copy(alpha = 0.12f), WrongRed, Color(0xFF7A1F2D))
        ChoiceState.DIM -> Triple(MaterialTheme.colorScheme.surface, MaterialTheme.colorScheme.outline.copy(alpha = 0.4f), MaterialTheme.colorScheme.onSurface.copy(alpha = 0.45f))
    }
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        border = BorderStroke(2.dp, border),
        colors = ButtonDefaults.outlinedButtonColors(containerColor = bg, contentColor = fg),
        contentPadding = androidx.compose.foundation.layout.PaddingValues(horizontal = 14.dp, vertical = 14.dp),
    ) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Box(
                Modifier
                    .size(32.dp)
                    .clip(CircleShape)
                    .background(border.copy(alpha = 0.18f)),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    when (state) { ChoiceState.RIGHT -> "✓"; ChoiceState.WRONG -> "✗"; else -> letter.toString() },
                    fontWeight = FontWeight.Bold,
                )
            }
            Spacer(Modifier.width(12.dp))
            MathText(text, Modifier.weight(1f), style = MaterialTheme.typography.bodyLarge, color = fg)
        }
    }
}

// ---------------------------------------------------------------- Done

@Composable
private fun DoneScreen(progress: Progress, solved: Int, right: Int, onBonus: () -> Unit, onHome: () -> Unit) {
    val met = progress.goalMetToday()
    val streak = progress.currentStreak()
    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Hexie(if (right * 2 >= solved) Mood.CHEER else Mood.HAPPY, Modifier.size(240.dp))
        Text(
            if (met) "Cauldron complete!" else "Nice brewing!",
            style = MaterialTheme.typography.headlineMedium,
            textAlign = TextAlign.Center,
        )
        Spacer(Modifier.height(8.dp))
        Text(
            "You got $right of $solved right.\n+$right eye${if (right == 1) "" else "s"} of newt 👁",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center,
        )
        if (met) {
            Spacer(Modifier.height(16.dp))
            Pill("🔥 $streak-day streak  ·  best ${progress.bestStreak}")
        }
        Spacer(Modifier.height(16.dp))
        Text(
            when {
                solved == 0 -> ""
                right == solved -> "Perfect! Hexie is doing a little jig."
                right == 0 -> "Every miss teaches Hexie what to show you next. Those topics will come back."
                else -> "Hexie will bring back the ones you missed so they stick."
            },
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )
        Spacer(Modifier.height(28.dp))
        Button(onClick = onHome, modifier = Modifier.fillMaxWidth().height(56.dp), shape = RoundedCornerShape(18.dp)) {
            Text("Back to the swamp", fontSize = 18.sp)
        }
        Spacer(Modifier.height(8.dp))
        TextButton(onClick = onBonus) { Text("One more problem?") }
    }
}

// ---------------------------------------------------------------- Settings

@Composable
private fun SettingsScreen(progress: Progress, onBack: () -> Unit) {
    val context = LocalContext.current
    var perDay by remember { mutableIntStateOf(progress.problemsPerDay) }
    var on by remember { mutableStateOf(progress.remindersOn) }
    var hour by remember { mutableIntStateOf(progress.reminderHour) }
    var minute by remember { mutableIntStateOf(progress.reminderMinute) }

    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = 12.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back") }
            Text("Settings", style = MaterialTheme.typography.titleLarge)
        }
        Spacer(Modifier.height(16.dp))

        Text("Problems per day: $perDay", style = MaterialTheme.typography.titleMedium)
        Slider(
            value = perDay.toFloat(),
            onValueChange = {
                perDay = it.toInt()
                progress.problemsPerDay = perDay
            },
            valueRange = 1f..5f,
            steps = 3,
        )
        Text(
            "A small number every day works better than a big pile once a week.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )

        HorizontalDivider(Modifier.padding(vertical = 20.dp))

        Row(verticalAlignment = Alignment.CenterVertically) {
            Text("Daily reminder", style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
            Switch(checked = on, onCheckedChange = {
                on = it
                progress.remindersOn = it
                Reminders.schedule(context)
            })
        }
        Spacer(Modifier.height(8.dp))
        OutlinedButton(
            enabled = on,
            onClick = {
                TimePickerDialog(context, { _, h, m ->
                    hour = h; minute = m
                    progress.reminderHour = h; progress.reminderMinute = m
                    Reminders.schedule(context)
                }, hour, minute, false).show()
            },
        ) {
            Text("Remind me at ${formatTime(hour, minute)}")
        }
        Spacer(Modifier.height(6.dp))
        Text(
            "Hexie sends one nudge a day. She stays quiet on days you already finished.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Spacer(Modifier.height(12.dp))
        TextButton(onClick = { Reminders.show(context, force = true) }) {
            Text("Send a test reminder now")
        }
    }
}

private fun formatTime(h: Int, m: Int): String {
    val hh = if (h % 12 == 0) 12 else h % 12
    return "%d:%02d %s".format(hh, m, if (h < 12) "AM" else "PM")
}
