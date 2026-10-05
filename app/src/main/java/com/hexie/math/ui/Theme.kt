package com.hexie.math.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Purple = Color(0xFF7B4FA0)
val Swamp = Color(0xFF5E9E52)
val Cream = Color(0xFFFFF8EE)
val RightGreen = Color(0xFF3E9B4F)
val WrongRed = Color(0xFFD0475B)

private val Colors = lightColorScheme(
    primary = Purple,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFEBDDF7),
    onPrimaryContainer = Color(0xFF2E1847),
    secondary = Swamp,
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFDCEFD4),
    onSecondaryContainer = Color(0xFF1C3A16),
    background = Cream,
    onBackground = Color(0xFF2B2232),
    surface = Color.White,
    onSurface = Color(0xFF2B2232),
    surfaceVariant = Color(0xFFF3ECF7),
    onSurfaceVariant = Color(0xFF5A4E66),
    outline = Color(0xFFCBBFD6),
)

private val Rounded = FontFamily.SansSerif

private val Type = Typography(
    headlineMedium = TextStyle(fontFamily = Rounded, fontWeight = FontWeight.ExtraBold, fontSize = 28.sp),
    titleLarge = TextStyle(fontFamily = Rounded, fontWeight = FontWeight.Bold, fontSize = 22.sp),
    titleMedium = TextStyle(fontFamily = Rounded, fontWeight = FontWeight.Bold, fontSize = 17.sp),
    bodyLarge = TextStyle(fontFamily = Rounded, fontSize = 17.sp, lineHeight = 25.sp),
    bodyMedium = TextStyle(fontFamily = Rounded, fontSize = 15.sp, lineHeight = 22.sp),
    labelLarge = TextStyle(fontFamily = Rounded, fontWeight = FontWeight.Bold, fontSize = 16.sp),
)

@Composable
fun HexieTheme(content: @Composable () -> Unit) =
    MaterialTheme(colorScheme = Colors, typography = Type, content = content)
