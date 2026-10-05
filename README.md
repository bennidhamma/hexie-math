# Hexie Math

An Android app for daily ACT math practice. Hexie, a small and friendly hag, gives 1 to 5 multiple-choice problems each day. After each answer, the app shows a step-by-step explanation.

Most problems come from a bank of 150 ACT-style medium and hard problems, with about 760 number variations. gpt-6-astra wrote them, and independent Claude solvers checked them. Figures are hand-built SVG. See [bank/README.md](bank/README.md).

## Install on a phone

1. Build the APK (see below), or get `HexieMath.apk` from the person who built it.
2. Copy the APK to the phone (email, Google Drive, or USB).
3. Open the file on the phone.
4. If Android asks, allow installs from that source.
5. Open Hexie Math and allow notifications.

## Features

- **Daily goal.** Set 1 to 5 problems per day in Settings. The default is 3.
- **Daily reminder.** One notification each day at a time you choose. The default is 4:30 PM. The app sends no reminder on days when the goal is already done. Tap the notification to start a quiz.
- **Explanations.** Each problem shows the steps and names the common trap.
- **Typeset math.** Equations show as real math: stacked fractions, exponents, roots, and subscripts. The app has a small built-in LaTeX renderer, so it needs no internet.
- **Diagrams.** Geometry, trig, graphing, and probability problems show a drawn figure: triangles, parallel lines, polygons, cylinders, coordinate grids, the unit circle, spinners, and marbles. Some explanations add a second figure, such as the reference triangle for a trig problem.
- **Streaks and newt eyes.** The streak counts days in a row with the goal met. Each correct answer gives one eye of newt.
- **Bonus problems.** After the goal is met, the student can do more problems.
- **A mix of easy, medium, and hard.** Easy problems are quick one-step problems from the generators. Medium and hard come from the problem bank. Each session starts easy, puts hard problems in the middle, and does not end on a hard one.
- **Challenge level.** In Settings: Gentle (50% easy, 40% medium, 10% hard), Balanced (30/45/25, the default), or Challenge (15/45/40). The mix moves toward easy after a rough stretch (under 50% right in the last 12 answers) and toward hard after a strong one (over 85%). After a miss, the next problem is one level easier.
- **Spaced review.** A missed bank problem comes back 3 or more days later, with new numbers when it has a template.
- **Pace timer.** Shows the time on each problem and turns orange after 60 seconds, the ACT pace. Turn it off in Settings.
- **Feedback.** The student can flag any problem (wrong answer, confusing wording, diagram problem, too easy, too hard) and rate each session. In Settings, enter the parent's email once. "Email feedback" then opens the email app with all new feedback and the topic scores filled in.

## How the app picks problems

The topics come from a March 2026 ACT practice-test score report. The app gives more weight to the topics with the most misses:

| Weight | Topics |
| --- | --- |
| Highest | Probability |
| High | Ratios and proportions, exponents and roots |
| Medium | Word problems, rewriting equations, area and volume, slope, lines and angles, fractions, unit circle, logarithms, law of sines and cosines |
| Lower | Percents |

Each miss makes its topic come back more often. Correct answers make a topic come back less often, but never stop it.

The app makes each problem from a generator, so problems do not repeat. The app computes every answer, so there is no answer key to get wrong. The unit tests do these checks:

- They build 2,000 problems from each generator and check that each one has 4 different choices.
- They parse every equation in 300 problems from each generator, so a LaTeX typo fails the build.

## Build from source

The build needs JDK 17 and the Android SDK (platform 35).

```sh
./gradlew testDebugUnitTest   # run the generator tests
./gradlew assembleRelease     # APK at app/build/outputs/apk/release/
```

The release build uses the debug signing key, so it installs by sideload. Do not use this key for the Play Store.

## Code map

| Path | Contents |
| --- | --- |
| `questions/Generators.kt` | One generator per problem type, grouped by topic |
| `questions/Question.kt` | Question model, exact fractions, LaTeX helpers |
| `questions/Tex.kt` | Parser for the LaTeX math subset that the questions use |
| `questions/Diagram.kt` | Diagram data (no Android types, so the tests can check it) |
| `data/Progress.kt` | Settings, streak, topic stats, topic weighting |
| `notify/Reminders.kt` | Daily alarm, notification messages |
| `ui/Hexie.kt` | The mascot, drawn in code with four moods |
| `ui/MathText.kt` | Typesets inline math between `\(` and `\)` |
| `ui/DiagramView.kt` | Draws each diagram type |
| `ui/Screens.kt` | Home, quiz, done, and settings screens |
| `src/debug/.../DiagramGalleryActivity.kt` | Debug builds only: a page that shows every question type, for visual checks |
