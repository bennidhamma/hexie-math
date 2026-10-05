package com.hexie.math.notify

import android.Manifest
import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import com.hexie.math.MainActivity
import com.hexie.math.R
import com.hexie.math.data.Progress
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId

object Reminders {
    private const val CHANNEL = "daily_math"
    private const val NOTIFICATION_ID = 1
    const val EXTRA_START_QUIZ = "start_quiz"

    private val MESSAGES = listOf(
        "Let's do some math!" to "Hexie's cauldron is bubbling. Come stir in a problem or two.",
        "Ready to do some math?" to "Hexie found a fresh problem under a toadstool.",
        "I know where you live..." to "...and I know you haven't done your math yet. 🧙‍♀️",
        "A problem escaped my cauldron!" to "Help Hexie catch it before it hops away.",
        "Psst. Math time." to "One eye of newt for every right answer. Hexie is very generous.",
        "The swamp is quiet..." to "Too quiet. Hexie thinks it needs some probability.",
        "My toad believes in you" to "He is a very smart toad. Let's do some math!",
        "Hexie is knitting you a sweater" to "She will finish it after you finish your math problems.",
        "Double, double, toil and trouble" to "Fractions boil and ratios bubble. Ready?",
        "Your broom is double-parked" to "Quick, do a math problem before Hexie gets a ticket.",
        "Brew-ha-ha!" to "That is a witch joke. Now let's do some math.",
    )

    fun ensureChannel(context: Context) {
        val manager = context.getSystemService(NotificationManager::class.java)
        if (manager.getNotificationChannel(CHANNEL) == null) {
            manager.createNotificationChannel(
                NotificationChannel(CHANNEL, "Daily math reminder", NotificationManager.IMPORTANCE_DEFAULT).apply {
                    description = "One friendly nudge from Hexie each day"
                }
            )
        }
    }

    /** Schedules the next reminder, or cancels it if reminders are off. */
    fun schedule(context: Context) {
        val progress = Progress(context)
        val alarms = context.getSystemService(AlarmManager::class.java)
        val pending = alarmIntent(context)
        alarms.cancel(pending)
        if (!progress.remindersOn) return

        val now = LocalDateTime.now()
        var next = now.toLocalDate().atTime(progress.reminderHour, progress.reminderMinute)
        // Skip today if the time has passed or today's goal is already met.
        if (!next.isAfter(now) || progress.goalMetToday()) next = next.plusDays(1)
        val millis = next.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
        // Inexact is fine for a friendly nudge, and it needs no special alarm permission.
        alarms.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, millis, pending)
    }

    fun show(context: Context, force: Boolean = false) {
        val progress = Progress(context)
        if (!force && progress.goalMetToday(LocalDate.now())) return
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) return

        ensureChannel(context)
        val streak = progress.currentStreak()
        val (title, body) = if (streak >= 2 && kotlin.random.Random.nextInt(3) == 0) {
            "Don't let your $streak-day streak turn into a toad!" to "Just ${progress.problemsPerDay} quick problem${if (progress.problemsPerDay == 1) "" else "s"} keeps it alive."
        } else {
            MESSAGES.random()
        }
        val open = PendingIntent.getActivity(
            context, 0,
            Intent(context, MainActivity::class.java)
                .putExtra(EXTRA_START_QUIZ, true)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP),
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
        )
        val notification = NotificationCompat.Builder(context, CHANNEL)
            .setSmallIcon(R.drawable.ic_notification)
            .setColor(0xFF7B4FA0.toInt())
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setContentIntent(open)
            .setAutoCancel(true)
            .build()
        NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, notification)
    }

    fun clear(context: Context) = NotificationManagerCompat.from(context).cancel(NOTIFICATION_ID)

    private fun alarmIntent(context: Context): PendingIntent = PendingIntent.getBroadcast(
        context, 0,
        Intent(context, ReminderReceiver::class.java),
        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
    )
}

class ReminderReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        Reminders.show(context)
        Reminders.schedule(context)
    }
}

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        Reminders.schedule(context)
    }
}
