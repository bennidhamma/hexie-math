from hexie import *


def AREA_04(rng):
    increase = rng.choice([25, 50, 100])
    decrease = rng.choice([20, 25, 50])
    radius_factor = 1 + F(increase, 100)
    height_factor = 1 - F(decrease, 100)
    correct = radius_factor ** 2 * height_factor
    linear = radius_factor * height_factor
    unchanged_height = radius_factor ** 2
    increased_height = radius_factor ** 2 * (1 + F(decrease, 100))
    choices, answer = order(
        (correct, m(frac(correct))),
        [(value, m(frac(value))) for value in
         [linear, unchanged_height, increased_height]],
    )
    return problem(
        stem=(f"A cylinder's radius is increased by {m(str(increase) + r'\%')} "
              f"and its height is decreased by {m(str(decrease) + r'\%')}. "
              "What is the ratio of the new volume to the original volume?"),
        choices=choices,
        answer=answer,
        explanation=(
            "Cylinder volume changes by the square of the radius factor times the height factor.\n"
            f"Radius factor: {m('1+' + frac(F(increase, 100)) + '=' + frac(radius_factor))}.\n"
            f"Height factor: {m('1-' + frac(F(decrease, 100)) + '=' + frac(height_factor))}.\n"
            f"Volume ratio: {m('(' + frac(radius_factor) + ')^{2}' + r'\cdot' + frac(height_factor) + '=' + frac(correct))}.\n"
            f"Trap: {m(frac(linear))} does not square the radius factor; "
            f"{m(frac(unchanged_height))} ignores the height change; "
            f"{m(frac(increased_height))} increases the height instead of decreasing it."
        ),
    )


def AREA_07(rng):
    while True:
        width = rng.randint(4, 10)
        difference = rng.randint(2, 7)
        length = width + difference
        area = width * length
        correct = 2 * (width + length)
        half_perimeter = width + length
        width_square = 4 * width
        length_square = 4 * length
        if len({correct, half_perimeter, width_square, length_square}) == 4:
            break
    choices, answer = order(
        (correct, m(correct)),
        [(value, m(value)) for value in
         [half_perimeter, width_square, length_square]],
    )
    return problem(
        stem=(f"A rectangle has an area of {m(area)} square centimeters. "
              f"Its length is {m(difference)} centimeters greater than its width. "
              "What is its perimeter, in centimeters?"),
        choices=choices,
        answer=answer,
        explanation=(
            "Use the area to find the side lengths, then add all four sides.\n"
            f"Let {m('w')} be the width: {m('w(w+' + str(difference) + ')=' + str(area))}.\n"
            f"{m('(w-' + str(width) + ')(w+' + str(length) + ')=0')}, so the positive width is {m(width)}.\n"
            f"Length: {m(str(width) + '+' + str(difference) + '=' + str(length))}.\n"
            f"Perimeter: {m('2(' + str(width) + '+' + str(length) + ')=' + str(correct))} centimeters.\n"
            f"Trap: {m(half_perimeter)} counts only two sides; "
            f"{m(width_square)} uses the width for all four sides; "
            f"{m(length_square)} uses the length for all four sides."
        ),
    )


def AREA_10(rng):
    height_ratio = rng.choice([2, 4, 5])
    unit = rng.choice([30, 60, 90])
    total = (height_ratio + 3) * unit
    correct = height_ratio * unit
    third_of_total = F(total, 3)
    equal_split = F(total, 2)
    missing_third = F(height_ratio * total, height_ratio + 1)
    choices, answer = order(
        (correct, m(frac(correct) + r'\pi')),
        [(value, m(frac(value) + r'\pi')) for value in
         [third_of_total, equal_split, missing_third]],
    )
    return problem(
        stem=("A cone and a cylinder have the same base radius. "
              f"The cone's height is {m(height_ratio)} times the cylinder's height. "
              f"Their volumes have a sum of {m(str(total) + r'\pi')} cubic centimeters. "
              "What is the volume of the cone, in cubic centimeters?"),
        choices=choices,
        answer=answer,
        explanation=(
            "With equal base areas, the cone-to-cylinder volume ratio is one third of their height ratio.\n"
            f"Volume ratio: {m(tfrac(height_ratio, 3))}.\n"
            f"The cone accounts for {m(tfrac(height_ratio, height_ratio + 3))} of the combined volume.\n"
            f"Cone volume: {m(tfrac(height_ratio, height_ratio + 3) + r'\cdot' + str(total) + r'\pi=' + str(correct) + r'\pi')}.\n"
            f"Trap: {m(frac(third_of_total) + r'\pi')} takes one third of the combined volume; "
            f"{m(frac(equal_split) + r'\pi')} splits the volume equally; "
            f"{m(frac(missing_third) + r'\pi')} omits the cone formula's factor of {m(frac(F(1, 3)))}."
        ),
    )


def AREA_11(rng):
    radius = rng.randint(5, 12)
    circumference = 2 * radius
    correct = radius ** 2
    unsquared = radius
    circumference_as_area = circumference
    diameter_squared = circumference ** 2
    choices, answer = order(
        (correct, m(str(correct) + r'\pi')),
        [(value, m(str(value) + r'\pi')) for value in
         [unsquared, circumference_as_area, diameter_squared]],
    )
    return problem(
        stem=(f"A circle has a circumference of {m(str(circumference) + r'\pi')} inches. "
              "What is its area, in square inches?"),
        choices=choices,
        answer=answer,
        explanation=(
            "Find the radius from the circumference before using the area formula.\n"
            f"{m(r'2\pi r=' + str(circumference) + r'\pi')}, so {m('r=' + str(radius))}.\n"
            f"{m(r'A=\pi(' + str(radius) + ')^{2}=' + str(correct) + r'\pi')} square inches.\n"
            f"Trap: {m(str(unsquared) + r'\pi')} does not square the radius; "
            f"{m(str(circumference_as_area) + r'\pi')} reports the circumference as the area; "
            f"{m(str(diameter_squared) + r'\pi')} uses the diameter as the radius."
        ),
    )


def ANG_05(rng):
    sides = rng.choice([8, 9, 10, 12, 15, 18])
    total = (sides - 2) * 180
    correct = F(total, sides)
    exterior = F(360, sides)
    wrong_triangle_count = F((sides - 1) * 180, sides)
    choices, answer = order(
        (correct, m(frac(correct) + r'^{\circ}')),
        [(value, m(frac(value) + r'^{\circ}')) for value in
         [exterior, wrong_triangle_count, total]],
    )
    return problem(
        stem=(f"A regular polygon has {m(sides)} sides. "
              "What is the measure of each interior angle?"),
        choices=choices,
        answer=answer,
        explanation=(
            "Divide the sum of the interior angles by the number of equal angles.\n"
            f"Angle sum: {m('(' + str(sides) + r'-2)\cdot180^{\circ}=' + str(total) + r'^{\circ}')}.\n"
            f"Each interior angle: {m(tfrac(total, sides) + r'^{\circ}=' + frac(correct) + r'^{\circ}')}.\n"
            f"Trap: {m(frac(exterior) + r'^{\circ}')} is an exterior angle; "
            f"{m(frac(wrong_triangle_count) + r'^{\circ}')} uses {m(str(sides) + '-1')} triangles instead of {m(str(sides) + '-2')}; "
            f"{m(str(total) + r'^{\circ}')} is the sum of all interior angles."
        ),
    )


def ANG_10(rng):
    while True:
        multiple = rng.choice([3, 4, 5, 8, 9, 11])
        exterior = F(180, multiple + 1)
        correct = F(360, exterior)
        half_turn = F(180, exterior)
        omitted_exterior = 2 * multiple
        if len({correct, half_turn, omitted_exterior, exterior}) == 4:
            break
    choices, answer = order(
        (correct, m(frac(correct))),
        [(value, m(frac(value))) for value in
         [half_turn, omitted_exterior, exterior]],
    )
    return problem(
        stem=("For a regular polygon, the measure of each interior angle is "
              f"{m(multiple)} times the measure of each exterior angle. "
              "How many sides does the polygon have?"),
        choices=choices,
        answer=answer,
        explanation=(
            "An interior angle and its adjacent exterior angle add to a straight angle.\n"
            f"Let {m('e')} be the exterior angle measure in degrees: {m(str(multiple) + 'e+e=180')}.\n"
            f"{m('e=' + tfrac(180, multiple + 1) + '=' + frac(exterior))}.\n"
            f"Number of sides: {m(tfrac(360, frac(exterior)) + '=' + frac(correct))}.\n"
            f"Trap: {m(frac(half_turn))} divides {m('180')} by the exterior angle instead of {m('360')}; "
            f"{m(omitted_exterior)} uses {m(tfrac(180, multiple))} for the exterior angle, omitting it from the straight-angle sum; "
            f"{m(frac(exterior))} reports the exterior angle measure as the side count."
        ),
    )
