package com.hexie.math.questions

/**
 * A picture that goes with a question. This is plain data with no Android types,
 * so the generators and their unit tests stay pure Kotlin. ui/DiagramView.kt draws it.
 * A null label means "draw nothing there". Use "?" to mark the unknown.
 */
sealed interface Diagram {

    /**
     * Triangle ABC. The shape comes from the real angles at A and B (degrees).
     * Side a is opposite A (segment BC), b is opposite B, c is opposite C.
     */
    data class Triangle(
        val angleA: Double,
        val angleB: Double,
        val sideA: String? = null,
        val sideB: String? = null,
        val sideC: String? = null,
        val labelA: String? = null,
        val labelB: String? = null,
        val labelC: String? = null,
        val vertexNames: Boolean = true,
    ) : Diagram {
        companion object {
            /** Builds the shape from three side lengths with the law of cosines. */
            fun fromSides(a: Double, b: Double, c: Double) = Triangle(
                angleA = Math.toDegrees(kotlin.math.acos((b * b + c * c - a * a) / (2 * b * c))),
                angleB = Math.toDegrees(kotlin.math.acos((a * a + c * c - b * b) / (2 * a * c))),
            )
        }
    }

    /**
     * Two horizontal parallel lines cut by a transversal.
     * [angle1] is the real measure of the angle at the top crossing, used to set the tilt.
     */
    data class ParallelLines(val angle1: Double, val label1: String, val label2: String, val sameSide: Boolean) : Diagram

    data class Rectangle(val width: Double, val height: Double, val widthLabel: String, val heightLabel: String) : Diagram

    data class Cylinder(val radiusLabel: String, val heightLabel: String) : Diagram

    data class Circle(val radiusLabel: String, val caption: String) : Diagram

    data class PlanePoint(val x: Int, val y: Int)

    /** A line y = m·x + b, drawn across the whole grid. */
    data class PlaneLine(val m: Double, val b: Double, val label: String? = null)

    data class Plane(val points: List<PlanePoint>, val lines: List<PlaneLine> = emptyList()) : Diagram

    /**
     * Unit circle with a terminal ray at [degrees]. When [legs] is set, it also draws the
     * reference triangle with labels (opposite, adjacent, hypotenuse).
     */
    data class UnitCircle(
        val degrees: Double,
        val angleLabel: String,
        val legs: Triple<String, String, String>? = null,
    ) : Diagram

    /** A spinner with [sections] equal slices. The first [marked] slices hold [icon]. */
    data class Spinner(val sections: Int, val marked: Int, val icon: String) : Diagram

    /** Rows of marbles. Color names: red, blue, green, purple. */
    data class Marbles(val groups: List<Pair<String, Int>>) : Diagram

    /** A regular polygon with one interior angle marked. */
    data class Polygon(val sides: Int, val angleLabel: String) : Diagram
}
