package com.hexie.math

import android.Manifest
import android.content.Intent
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.hexie.math.data.Progress
import com.hexie.math.notify.Reminders
import com.hexie.math.ui.Cream
import com.hexie.math.ui.HexieApp
import com.hexie.math.ui.HexieTheme

class MainActivity : ComponentActivity() {

    private var startQuiz by mutableStateOf(false)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val progress = Progress(this)
        Reminders.ensureChannel(this)
        Reminders.schedule(this)
        startQuiz = intent?.getBooleanExtra(Reminders.EXTRA_START_QUIZ, false) == true

        setContent {
            HexieTheme {
                val askPermission = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) {
                    Reminders.schedule(this)
                }
                LaunchedEffect(Unit) {
                    if (Build.VERSION.SDK_INT >= 33 && !progress.askedNotificationPermission) {
                        progress.askedNotificationPermission = true
                        askPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
                    }
                }
                Box(
                    Modifier
                        .fillMaxSize()
                        .background(Cream)
                        .safeDrawingPadding()
                ) {
                    HexieApp(progress, startQuiz, onStartQuizHandled = { startQuiz = false })
                }
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        if (intent.getBooleanExtra(Reminders.EXTRA_START_QUIZ, false)) startQuiz = true
    }
}
