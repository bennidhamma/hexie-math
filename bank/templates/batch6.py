from hexie import *


def COORD_01(rng):
    rise, run = rng.choice([(2, 3), (3, 2), (3, 4), (4, 3)])
    slope = F(rise, run)
    intercept = rng.choice([-5, -3, 2, 4, 5])
    x1 = run * rng.randint(1, 3)
    x2 = x1 + run * rng.randint(1, 2)
    y1, y2 = slope * x1 + intercept, slope * x2 + intercept
    correct = (slope, intercept)
    reciprocal = (1 / slope, y1 - x1 / slope)
    sign_error = (-slope, y1 + slope * x1)
    omit = (slope, y1)

    def equation(pair):
        return m('y = ' + poly(pair))

    choices, answer = order((correct, equation(correct)),
                            [(p, equation(p)) for p in (reciprocal, sign_error, omit)],
                            key=lambda item: item[0])
    return problem(
        stem=f'Which equation represents the line through {m(f"({x1}, {frac(y1)})")} and {m(f"({x2}, {frac(y2)})")}?',
        choices=choices, answer=answer,
        explanation='Find the slope, then use either point to find the intercept.\n'
        + m('m = ' + tfrac(f'{frac(y2)} - {paren(y1)}', f'{x2} - {x1}') + ' = ' + frac(slope)) + '\n'
        + m(f'b = {frac(y1)} - ({frac(slope)})({x1}) = {intercept}') + '\n'
        + equation(correct) + '\n'
        + f'Trap: {equation(reciprocal)} reverses rise and run; {equation(sign_error)} reverses only one subtraction; {equation(omit)} uses the first point’s height as the intercept.')


def COORD_03(rng):
    while True:
        a = rng.choice([3, 4, 5, 6, 8])
        b = rng.choice([2, 3, 4, 6, 9])
        c = b * rng.randint(2, 6)
        correct = -F(a, b)
        wrong = [-F(b, a), F(a, b), F(c, b)]
        if len(set([correct] + wrong)) == 4:
            break
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'A line has equation {m(f"{a}x + {b}y = {c}")}. What is its slope?',
        choices=choices, answer=answer,
        explanation='Isolate the vertical coordinate to read the slope.\n'
        + m(f'{b}y = -{a}x + {c}') + '\n'
        + m('y = ' + poly([correct, F(c, b)])) + '\n'
        + f'The slope is {m(frac(correct))}.\n'
        + f'Trap: {m(frac(wrong[0]))} reverses the ratio; {m(frac(wrong[1]))} loses the minus sign; {m(frac(wrong[2]))} is the intercept.')


def COORD_04(rng):
    u, v, hyp = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
    scale = rng.randint(1, 2)
    u, v, hyp = u * scale, v * scale, hyp * scale
    ax, ay = rng.randint(-7, 2), rng.randint(-6, 3)
    mx, my = ax + u, ay + v
    bx, by = 2 * mx - ax, 2 * my - ay
    correct = 2 * hyp
    wrong = [hyp, 2 * (u + v), correct ** 2]
    choices, answer = order((correct, m(correct)), [(n, m(n)) for n in wrong])
    return problem(
        stem=f'The midpoint of {m("\\overline{AB}")} is {m(f"M({mx}, {my})")}, and {m(f"A = ({ax}, {ay})")}. What is the length of {m("\\overline{AB}")} in coordinate units?',
        choices=choices, answer=answer,
        explanation='Recover the other endpoint using the midpoint, then apply the distance formula.\n'
        + m(f'B = (2({mx}) - {paren(ax)}, 2({my}) - {paren(ay)}) = ({bx}, {by})') + '\n'
        + m(f'AB = \\sqrt{{({bx} - {paren(ax)})^{{2}} + ({by} - {paren(ay)})^{{2}}}} = \\sqrt{{{correct ** 2}}} = {correct}') + '\n'
        + f'Trap: {m(hyp)} is only half the segment; {m(wrong[1])} adds the horizontal and vertical changes; {m(wrong[2])} omits the square root.')


def COORD_06(rng):
    while True:
        h = rng.choice([-4, -3, -2, 2, 3, 4])
        k = rng.choice([-4, -3, -2, 2, 3, 4])
        u, v, radius = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
        px, py = h + u, k + v
        radius2 = u * u + v * v
        constant = h * h + k * k - radius2
        correct = (-2 * h, -2 * k, constant)
        use_radius = (-2 * h, -2 * k, h * h + k * k - radius)
        flip_center = (2 * h, 2 * k, constant)
        use_origin = (-2 * h, -2 * k, h * h + k * k - px * px - py * py)
        if len({correct, use_radius, flip_center, use_origin}) == 4:
            break

    def equation(coefs):
        a, b, c = coefs
        return m(f'x^{{2}} + y^{{2}} {signed(a)}x {signed(b)}y {signed(c)} = 0')

    choices, answer = order((correct, equation(correct)),
                            [(p, equation(p)) for p in (use_radius, flip_center, use_origin)],
                            key=lambda item: item[0])
    return problem(
        stem=f'A circle has center {m(f"({h}, {k})")} and passes through {m(f"({px}, {py})")}. Which equation represents the circle?',
        choices=choices, answer=answer,
        explanation='The squared radius is the squared distance from the center to the given point.\n'
        + m(f'r^{{2}} = ({px} - {paren(h)})^{{2}} + ({py} - {paren(k)})^{{2}} = {radius2}') + '\n'
        + m(f'(x {signed(-h)})^{{2}} + (y {signed(-k)})^{{2}} = {radius2}') + '\n'
        + equation(correct) + '\n'
        + f'Trap: the constant {m(use_radius[2])} uses the radius instead of its square; reversed linear signs put the center at {m(f"({-h}, {-k})")}; the constant {m(use_origin[2])} uses distance from the origin.')


def COORD_07(rng):
    while True:
        a, b = rng.choice([(2, 3), (3, 2), (3, 4), (4, 3)])
        old_intercept = rng.randint(1, 9)
        c = b * old_intercept
        px, py = b * rng.randint(1, 3), rng.randint(-4, 6)
        slope = -F(a, b)
        correct = (slope, py - slope * px)
        perpendicular = (F(b, a), py - F(b, a) * px)
        old_line = (slope, F(old_intercept))
        omit = (slope, F(py))
        if len({correct, perpendicular, old_line, omit}) == 4:
            break

    def equation(pair):
        return m('y = ' + poly(pair))

    choices, answer = order((correct, equation(correct)),
                            [(p, equation(p)) for p in (perpendicular, old_line, omit)],
                            key=lambda item: item[0])
    return problem(
        stem=f'Which equation represents the line through {m(f"({px}, {py})")} that is parallel to {m(f"{a}x + {b}y = {c}")}?',
        choices=choices, answer=answer,
        explanation='Parallel lines have the same slope but may have different intercepts.\n'
        + m('y = ' + poly([slope, old_intercept])) + f', so the slope is {m(frac(slope))}.\n'
        + m(f'b = {py} - ({frac(slope)})({px}) = {frac(correct[1])}') + '\n'
        + equation(correct) + '\n'
        + f'Trap: {equation(perpendicular)} is perpendicular; {equation(old_line)} keeps the original intercept; {equation(omit)} uses the point’s height as the intercept.')


def COORD_09(rng):
    while True:
        a, b = rng.randint(2, 6), rng.randint(2, 5)
        factor, offset = rng.randint(2, 4), rng.randint(1, 5)
        d = b * factor
        c, e = rng.randint(1, 9), rng.randint(1, 9)
        correct = -a * factor - offset
        wrong = [a * factor - offset, -F(a, factor) - offset, -a * factor]
        if len(set([correct] + wrong)) == 4:
            break
    choices, answer = order((correct, m(correct)), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'For what value of {m("k")} are the lines {m(f"{a}x - {b}y = {c}")} and {m(f"(k + {offset})x + {d}y = {e}")} parallel?',
        choices=choices, answer=answer,
        explanation='Set the slopes equal, keeping the signs from each standard-form equation.\n'
        + m('-' + tfrac(f'k + {offset}', d) + ' = ' + tfrac(a, b)) + '\n'
        + m(f'k + {offset} = {-a * factor}') + '\n'
        + m(f'k = {correct}') + '\n'
        + f'Trap: {m(frac(wrong[0]))} drops the slope’s minus sign; {m(frac(wrong[1]))} divides by the scale factor instead of multiplying; {m(wrong[2])} forgets to subtract {m(offset)}.')


def COORD_10(rng):
    while True:
        h, k = rng.choice([-4, -3, -2, 2, 3, 4]), rng.choice([-4, -3, -2, 2, 3, 4])
        radius = rng.randint(6, 10)
        constant = h * h + k * k - radius * radius
        if constant < 0:
            break
    correct = (h, k, radius)
    flipped = (-h, -k, radius)
    no_squares = (h, k, math.sqrt(-constant))
    no_root = (h, k, radius * radius)

    def choice(center_x, center_y, radius_tex):
        return f'Center {m(f"({center_x}, {center_y})")}, radius {m(radius_tex)}'

    choices, answer = order(
        (correct, choice(h, k, radius)),
        [(flipped, choice(-h, -k, radius)),
         (no_squares, choice(h, k, root(-constant))),
         (no_root, choice(h, k, radius * radius))], key=lambda item: item[0])
    return problem(
        stem=f'What are the center and radius of the circle {m(f"x^{{2}} + y^{{2}} {signed(-2 * h)}x {signed(-2 * k)}y {signed(constant)} = 0")}?',
        choices=choices, answer=answer,
        explanation='Complete both squares, then take the square root of the right side.\n'
        + m(f'(x^{{2}} {signed(-2 * h)}x + {h * h}) + (y^{{2}} {signed(-2 * k)}y + {k * k}) = {-constant} + {h * h} + {k * k}') + '\n'
        + m(f'(x {signed(-h)})^{{2}} + (y {signed(-k)})^{{2}} = {radius * radius}') + '\n'
        + f'The center is {m(f"({h}, {k})")} and the radius is {m(radius)}.\n'
        + f'Trap: {m(f"({-h}, {-k})")} reverses the center’s signs; radius {m(root(-constant))} omits the added squares; radius {m(radius * radius)} omits the square root.')


def TRIG_01(rng):
    reference = rng.choice([F(1, 6), F(1, 3)])
    quadrant = rng.choice([2, 3, 4])
    function = rng.choice(['sin', 'cos'])
    angle = {2: 1 - reference, 3: 1 + reference, 4: 2 - reference}[quadrant]
    sine_sign = 1 if quadrant == 2 else -1
    cosine_sign = 1 if quadrant == 4 else -1
    sign = sine_sign if function == 'sin' else cosine_sign
    uses_root = (function == 'sin' and reference == F(1, 3)) or (function == 'cos' and reference == F(1, 6))
    magnitude = math.sqrt(3) / 2 if uses_root else 0.5
    other_magnitude = 0.5 if uses_root else math.sqrt(3) / 2
    magnitude_tex = tfrac(root(3), 2) if uses_root else frac(F(1, 2))
    other_tex = frac(F(1, 2)) if uses_root else tfrac(root(3), 2)
    correct_tex = ('-' if sign < 0 else '') + magnitude_tex
    opposite_tex = ('-' if sign > 0 else '') + magnitude_tex
    swapped_tex = ('-' if sign < 0 else '') + other_tex
    both_tex = ('-' if sign > 0 else '') + other_tex
    angle_tex = tfrac(str(angle.numerator) + '\\pi', angle.denominator)
    reference_tex = tfrac('\\pi', reference.denominator)
    choices, answer = order((sign * magnitude, m(correct_tex)),
                            [(-sign * magnitude, m(opposite_tex)),
                             (sign * other_magnitude, m(swapped_tex)),
                             (-sign * other_magnitude, m(both_tex))])
    quadrant_name = {2: 'II', 3: 'III', 4: 'IV'}[quadrant]
    operation = {2: f'\\pi - {angle_tex}', 3: f'{angle_tex} - \\pi', 4: f'2\\pi - {angle_tex}'}[quadrant]
    return problem(
        stem=f'What is the exact value of {m(chr(92) + function + "(" + angle_tex + ")")}?',
        choices=choices, answer=answer,
        explanation='Use the reference angle for the magnitude and the quadrant for the sign.\n'
        + m(operation + ' = ' + reference_tex) + '\n'
        + f'In quadrant {quadrant_name}, {"sine" if function == "sin" else "cosine"} is {"positive" if sign > 0 else "negative"}.\n'
        + m(chr(92) + function + '(' + angle_tex + ') = ' + correct_tex) + '\n'
        + f'Trap: {m(opposite_tex)} has the wrong sign; {m(swapped_tex)} swaps sine and cosine magnitudes; {m(both_tex)} makes both mistakes.')


def TRIG_02(rng):
    opposite, adjacent, hyp = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    if rng.choice([False, True]):
        opposite, adjacent = adjacent, opposite
    quadrant = rng.choice([2, 3, 4])
    sine_sign = 1 if quadrant == 2 else -1
    cosine_sign = 1 if quadrant == 4 else -1
    sine = F(sine_sign * opposite, hyp)
    cosine = F(cosine_sign * adjacent, hyp)
    correct = sine / cosine
    wrong = [-correct, 1 / correct, sine]
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    quadrant_name = {2: 'II', 3: 'III', 4: 'IV'}[quadrant]
    return problem(
        stem=f'If {m("\\sin\\theta = " + frac(sine))} and {m("\\theta")} lies in quadrant {quadrant_name}, what is {m("\\tan\\theta")}?',
        choices=choices, answer=answer,
        explanation='Use the Pythagorean identity to find cosine with the correct sign, then divide sine by cosine.\n'
        + m('\\cos^{2}\\theta = 1 - (' + frac(sine) + ')^{2} = ' + frac(cosine * cosine)) + '\n'
        + m('\\cos\\theta = ' + frac(cosine)) + f' in quadrant {quadrant_name}.\n'
        + m('\\tan\\theta = ' + tfrac(frac(sine), frac(cosine)) + ' = ' + frac(correct)) + '\n'
        + f'Trap: {m(frac(wrong[0]))} uses the wrong quadrant sign; {m(frac(wrong[1]))} divides cosine by sine; {m(frac(wrong[2]))} repeats the sine value.')


def TRIG_05(rng):
    while True:
        first = rng.choice([90, 120, 135, 150, 210, 225])
        second = rng.choice([30, 45, 60, 75])
        correct = F(first + second, 180)
        wrong = [F(first - second, 180), F(first + second, 360), F(first, 180)]
        if len(set([correct] + wrong)) == 4:
            break

    def pi_tex(value):
        numerator = (str(value.numerator) if value.numerator != 1 else '') + '\\pi'
        return numerator if value.denominator == 1 else tfrac(numerator, value.denominator)

    choices, answer = order((correct, m(pi_tex(correct))), [(v, m(pi_tex(v))) for v in wrong])
    return problem(
        stem=f'A wheel turns through {m(str(first) + "^{\\circ}")}, then continues in the same direction through another {m(str(second) + "^{\\circ}")}. What is the total angle of rotation, in radians?',
        choices=choices, answer=answer,
        explanation='Add rotations in the same direction, then convert the total to radians.\n'
        + m(f'{first} + {second} = {first + second}') + ' degrees.\n'
        + m(f'{first + second} \\cdot ' + tfrac('\\pi', 180) + ' = ' + pi_tex(correct)) + '\n'
        + f'Trap: {m(pi_tex(wrong[0]))} subtracts the rotations; {m(pi_tex(wrong[1]))} uses {m(tfrac(chr(92) + "pi", 360))}; {m(pi_tex(wrong[2]))} omits the second rotation.')


def TRIG_06(rng):
    total = rng.choice([F(6, 5), F(5, 4), F(4, 3), F(7, 5)])
    correct = (total * total - 1) / 2
    wrong = [total * total - 1, (total - 1) / 2, total * total / 2]
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'If {m("\\sin\\theta + \\cos\\theta = " + frac(total))}, what is the value of {m("\\sin\\theta \\cos\\theta")}?',
        choices=choices, answer=answer,
        explanation='Square the sum and replace the sum of the squared trig values with one.\n'
        + m('\\sin^{2}\\theta + 2\\sin\\theta\\cos\\theta + \\cos^{2}\\theta = ' + frac(total * total)) + '\n'
        + m('1 + 2\\sin\\theta\\cos\\theta = ' + frac(total * total)) + '\n'
        + m('\\sin\\theta\\cos\\theta = (' + frac(total * total) + ' - 1) \\div 2 = ' + frac(correct)) + '\n'
        + f'Trap: {m(frac(wrong[0]))} forgets to divide by {m(2)}; {m(frac(wrong[1]))} does not square the given sum; {m(frac(wrong[2]))} forgets to subtract {m(1)}.')


def TRIG_08(rng):
    amplitude = rng.randint(2, 6)
    shift = amplitude + rng.randint(1, 5)
    frequency = rng.choice([F(1, 2), F(2, 3), F(3, 2), F(3, 4), F(4, 3)])
    function = rng.choice(['sin', 'cos'])
    period = 2 / frequency

    def pi_tex(value):
        numerator = (str(value.numerator) if value.numerator != 1 else '') + '\\pi'
        return numerator if value.denominator == 1 else tfrac(numerator, value.denominator)

    def choice(pair):
        return f'Amplitude {m(pair[0])}, period {m(pi_tex(pair[1]))}'

    correct = (amplitude, period)
    negative = (-amplitude, period)
    multiply = (amplitude, 2 * frequency)
    use_shift = (shift, period)
    choices, answer = order((correct, choice(correct)),
                            [(p, choice(p)) for p in (negative, multiply, use_shift)],
                            key=lambda item: item[0])
    equation = f'y = {shift} - {amplitude}\\{function}\\left({frac(frequency)}x\\right)'
    return problem(
        stem=f'For the function {m(equation)}, {m("x")} is measured in radians. What are the amplitude and period?',
        choices=choices, answer=answer,
        explanation='Amplitude is the magnitude of the outside coefficient; period is two pi divided by the coefficient of the input.\n'
        + m(f'\\text{{Amplitude}} = \\left|-{amplitude}\\right| = {amplitude}') + '\n'
        + m('\\text{Period} = ' + tfrac('2\\pi', frac(frequency)) + ' = ' + pi_tex(period)) + '\n'
        + f'Trap: amplitude {m(-amplitude)} keeps the reflection sign; period {m(pi_tex(multiply[1]))} multiplies instead of dividing; amplitude {m(shift)} uses the vertical shift.')


def LAW_03(rng):
    a, b, c = rng.choice([(4, 5, 6), (5, 7, 8), (6, 7, 9), (7, 8, 9), (8, 9, 13)])
    numerator = a * a + b * b - c * c
    correct = F(numerator, 2 * a * b)
    wrong = [-correct, 2 * correct, F(numerator, 2 * a * c)]
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'In {m("\\triangle ABC")}, {m(f"AB = {a}")}, {m(f"AC = {b}")}, and {m(f"BC = {c}")}, all in centimeters. What is {m("\\cos\\angle A")}?',
        choices=choices, answer=answer,
        explanation='In the law of cosines, subtract the square of the side opposite the requested angle.\n'
        + m(f'{c}^{{2}} = {a}^{{2}} + {b}^{{2}} - 2({a})({b})\\cos\\angle A') + '\n'
        + m('\\cos\\angle A = ' + tfrac(f'{a}^{{2}} + {b}^{{2}} - {c}^{{2}}', f'2({a})({b})') + ' = ' + frac(correct)) + '\n'
        + f'Trap: {m(frac(wrong[0]))} reverses the numerator’s sign; {m(frac(wrong[1]))} omits the factor {m(2)}; {m(frac(wrong[2]))} uses an opposite side in the denominator.')


def STAT_01(rng):
    count = rng.randint(6, 10)
    mean = rng.randint(15, 28)
    drop = rng.randint(2, 5)
    removed = mean + drop * (count - 1)
    correct = F(count * mean - removed, count - 1)
    wrong = [F(count * mean - removed, count), F(count * mean + removed, count + 1), mean - F(removed, count - 1)]
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'A set of {m(count)} scores has a mean of {m(mean)} points. One score of {m(removed)} points is removed. What is the mean of the remaining scores, in points?',
        choices=choices, answer=answer,
        explanation='Subtract the removed score from the original total, then reduce the number of scores by one.\n'
        + m(f'\\text{{Original total}} = {count}({mean}) = {count * mean}') + '\n'
        + m('\\text{New mean} = ' + tfrac(f'{count * mean} - {removed}', count - 1) + ' = ' + frac(correct)) + '\n'
        + f'Trap: {m(frac(wrong[0]))} keeps the old count; {m(frac(wrong[1]))} adds the score instead of removing it; {m(frac(wrong[2]))} subtracts from the mean instead of the total.')


def STAT_02(rng):
    count = rng.choice([4, 6, 8])
    mean = rng.randint(68, 80)
    increase = rng.randint(2, 4)
    target = mean + increase
    correct = F((count + 2) * target - count * mean, 2)
    wrong = [(count + 1) * target - count * mean,
             F((count + 1) * target - count * mean, 2),
             2 * target - mean]
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'Maya’s {m(count)} quizzes have a mean of {m(mean)} points. For her course grade, each quiz counts once and the final exam counts twice. What final-exam score, in points, gives her a weighted mean of {m(target)}?',
        choices=choices, answer=answer,
        explanation='Count the exam twice in both the score total and the total weight.\n'
        + m(tfrac(f'{count}({mean}) + 2x', count + 2) + f' = {target}') + '\n'
        + m(f'2x = {target}({count + 2}) - {count * mean} = {(count + 2) * target - count * mean}') + '\n'
        + m('x = ' + frac(correct)) + '\n'
        + f'Trap: {m(frac(wrong[0]))} counts the exam only once; {m(frac(wrong[1]))} uses total weight {m(count + 1)}; {m(frac(wrong[2]))} gives the quiz mean and exam equal weight.')


def STAT_05(rng):
    n1 = rng.choice([8, 12, 16, 20])
    factor = rng.choice([2, 3])
    n2 = factor * n1
    mean1 = rng.randint(10, 20)
    step = rng.randint(2, 6)
    mean2 = mean1 + (factor + 1) * step
    correct = F(n1 * mean1 + n2 * mean2, n1 + n2)
    wrong = [F(mean1 + mean2, 2), F(n2 * mean1 + n1 * mean2, n1 + n2), mean1 + mean2]
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    return problem(
        stem=f'In one class, {m(n1)} students read for a mean of {m(mean1)} minutes each. In another class, {m(n2)} students read for a mean of {m(mean2)} minutes each. What is the mean reading time, in minutes, for all the students in these two classes?',
        choices=choices, answer=answer,
        explanation='Weight each class mean by its number of students.\n'
        + m(f'\\text{{Total minutes}} = {n1}({mean1}) + {n2}({mean2}) = {n1 * mean1 + n2 * mean2}') + '\n'
        + m('\\text{Combined mean} = ' + tfrac(n1 * mean1 + n2 * mean2, n1 + n2) + ' = ' + frac(correct)) + '\n'
        + f'Trap: {m(frac(wrong[0]))} averages the means without weights; {m(frac(wrong[1]))} swaps the class sizes; {m(wrong[2])} adds the means.')


def STAT_06(rng):
    mean, sd = rng.randint(10, 25), rng.randint(2, 5)
    scale, new_mean = rng.randint(2, 4), rng.randint(10, 30)
    shift = scale * mean + new_mean
    new_sd = scale * sd
    correct = (new_mean, new_sd)
    negative = (new_mean, -new_sd)
    shift_sd = (new_mean, shift - scale * sd)
    omit_scale = (shift - mean, new_sd)

    def choice(pair):
        return f'Mean {m(pair[0])}, standard deviation {m(pair[1])}'

    choices, answer = order((correct, choice(correct)),
                            [(p, choice(p)) for p in (negative, shift_sd, omit_scale)],
                            key=lambda item: item[0])
    return problem(
        stem=f'A data set has mean {m(mean)} and standard deviation {m(sd)}. Each value {m("x")} is replaced by {m(f"{shift} - {scale}x")}. What are the mean and standard deviation of the resulting data set?',
        choices=choices, answer=answer,
        explanation='Apply the whole transformation to the mean, but only the absolute scale factor to the standard deviation.\n'
        + m(f'\\text{{New mean}} = {shift} - {scale}({mean}) = {new_mean}') + '\n'
        + m(f'\\text{{New standard deviation}} = \\left|-{scale}\\right|({sd}) = {new_sd}') + '\n'
        + f'Trap: standard deviation {m(-new_sd)} keeps a negative scale; standard deviation {m(shift_sd[1])} also applies the shift; mean {m(omit_scale[0])} omits the scale factor.')


def STAT_08(rng):
    while True:
        start = rng.choice([8, 10, 12, 14, 16])
        scores = [start, start + 2, start + 6, start + 8, start + 10]
        f1, f2 = rng.randint(2, 5), rng.randint(4, 8)
        half = f1 + f2
        f3 = rng.randint(1, half - 2)
        f4 = rng.randint(1, half - f3 - 1)
        f5 = half - f3 - f4
        frequencies = [f1, f2, f3, f4, f5]
        correct = F(scores[1] + scores[2], 2)
        mean = F(sum(v * n for v, n in zip(scores, frequencies)), 2 * half)
        wrong = [F(scores[1]), F(scores[2]), mean]
        if len(set([correct] + wrong)) == 4:
            break
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])
    table = {'caption': 'Quiz scores', 'headers': ['Score (points)', 'Number of students'],
             'rows': [[m(v), m(n)] for v, n in zip(scores, frequencies)]}
    return problem(
        stem='The table gives the number of students earning each score on a quiz. What is the median score, in points?',
        choices=choices, answer=answer, table=table,
        explanation='Use cumulative frequencies to locate both middle scores.\n'
        + m('N = ' + ' + '.join(map(str, frequencies)) + f' = {2 * half}') + '\n'
        + f'The middle positions are {m(half)} and {m(half + 1)}.\n'
        + f'The first {m(half)} scores end at {m(scores[1])}; position {m(half + 1)} has score {m(scores[2])}.\n'
        + m('\\text{Median} = ' + tfrac(f'{scores[1]} + {scores[2]}', 2) + ' = ' + frac(correct)) + '\n'
        + f'Trap: {m(scores[1])} uses only the lower middle score; {m(scores[2])} uses only the upper middle score; {m(frac(mean))} is the mean.')
