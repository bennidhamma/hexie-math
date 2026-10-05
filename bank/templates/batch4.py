from hexie import *


def FUN_01(rng):
    while True:
        a, b, c, t = rng.randint(2, 4), rng.randint(1, 9), rng.randint(2, 5), rng.randint(2, 4)
        inner = t + c
        right = a * inner ** 2 - b
        reverse = a * t ** 2 - b + c
        product = (a * t ** 2 - b) * inner
        square = a * (t ** 2 + c) - b
        if len({right, reverse, product, square}) == 4:
            break
    choices, answer = order((right, m(right)), [(v, m(v)) for v in (reverse, product, square)])
    return problem(
        stem=f"Let {m('f(x) = ' + poly([a, 0, -b]))} and {m(f'g(x) = x + {c}')}. What is {m(f'f(g({t}))')}?",
        choices=choices, answer=answer,
        explanation="Evaluate the inner function first, then use its output as the input to the outer function.\n"
        + f"{m(f'g({t}) = {t} + {c} = {inner}')}\n"
        + f"{m(f'f({inner}) = {a}({inner})^{{2}} - {b} = {right}')}\n"
        + f"Trap: {m(reverse)} reverses the functions; {m(product)} multiplies their outputs; {m(square)} fails to square the whole input.")


def FUN_02(rng):
    while True:
        a, b, c = rng.randint(2, 5), rng.randint(1, 9), rng.randint(2, 6)
        if b != a * c:
            break
    correct = m(tfrac(poly([-c, b]), poly([1, -a])))
    plus_top = m(tfrac(poly([c, b]), poly([1, -a])))
    plus_bottom = m(tfrac(poly([-c, b]), poly([1, a])))
    both = m(tfrac(poly([c, b]), poly([1, a])))
    choices, answer = order((0, correct), [(1, plus_bottom), (2, plus_top), (3, both)])
    return problem(
        stem=f"The function {m('f(x) = ' + tfrac(poly([a, b]), poly([1, c])))} is defined for {m(f'x \\ne -{c}')}. Which expression equals {m('f^{-1}(x)')} for every {m('x')} in the domain of the inverse?",
        choices=choices, answer=answer,
        explanation="Swap the input and output, then solve for the new output.\n"
        + m('x = ' + tfrac(poly([a, b], 'y'), poly([1, c], 'y'))) + '\n'
        + m(f'xy + {c}x = {a}y + {b}') + '\n'
        + m(f'y(x - {a}) = {b} - {c}x') + '\n'
        + m('f^{-1}(x) = ' + tfrac(poly([-c, b]), poly([1, -a]))) + '\n'
        + f"Trap: {plus_top} misses the sign change on {m(f'{c}x')}; {plus_bottom} misses it on {m(f'{a}y')}; {both} misses both.")


def FUN_05(rng):
    a, b, c, h = rng.randint(2, 4), rng.randint(1, 6), rng.randint(1, 7), rng.randint(2, 4)
    right = (a, 2 * a * h + b, a * h * h + b * h + c)
    no_cross = (a, b, right[2])
    outside = (a, b, c + h)
    partial = (a, right[1], a * h * h + c)
    choices, answer = order((right, m(poly(right))), [(v, m(poly(v))) for v in (no_cross, outside, partial)], key=lambda item: item[0])
    return problem(
        stem=f"If {m('f(x) = ' + poly([a, b, c]))}, which expression equals {m(f'f(x + {h})')}?",
        choices=choices, answer=answer,
        explanation="Replace every input with the entire expression, then expand.\n"
        + m(f'f(x + {h}) = {a}(x + {h})^{{2}} + {b}(x + {h}) + {c}') + '\n'
        + m(f'f(x + {h}) = ' + poly(right)) + '\n'
        + f"Trap: {m(poly(no_cross))} omits the squared binomial's middle term; {m(poly(outside))} adds to the output; {m(poly(partial))} leaves the linear input unchanged.")


def FUN_06(rng):
    b, p, d, q = rng.randint(3, 6), rng.randint(2, 5), rng.randint(2, 4), rng.randint(2, 3)
    offset = (q - 1) * b + q * d
    start, right = b + d, b + p
    wrong_branch, stop, left_twice = b - q * d, b, b + d + 2 * p
    choices, answer = order((right, m(right)), [(v, m(v)) for v in (wrong_branch, stop, left_twice)])
    return problem(
        stem=f"For all real {m('x')}, {m(f'f(x) = x + {p}')} when {m(f'x \\le {b}')}, and {m('f(x) = ' + poly([q, -offset]))} when {m(f'x > {b}')}. What is {m(f'f(f({start}))')}?",
        choices=choices, answer=answer,
        explanation="Choose a branch using the input at each stage, including the boundary.\n"
        + m(f'{start} > {b}, f({start}) = {q}({start}) - {offset} = {b}') + '\n'
        + m(f'f({b}) = {b} + {p} = {right}') + '\n'
        + f"Trap: {m(wrong_branch)} uses the wrong branch at equality; {m(stop)} stops after one evaluation; {m(left_twice)} uses the first branch twice.")


def FUN_07(rng):
    a, boundary = rng.randint(2, 5), rng.randint(2, 6)
    excluded = boundary + rng.randint(2, 5)
    right = m(f'x \\ge {boundary} \\text{{ and }} x \\ne {excluded}')
    reverse = m(f'x \\le {boundary}')
    ignore = m(f'x \\ge {boundary}')
    strict = m(f'x > {boundary} \\text{{ and }} x \\ne {excluded}')
    choices, answer = order((2, right), [(0, reverse), (1, ignore), (3, strict)])
    expression = tfrac('\\sqrt{' + poly([a, -a * boundary]) + '}', poly([1, -excluded]))
    return problem(
        stem=f"What is the domain of the real-valued function {m('f(x) = ' + expression)}?",
        choices=choices, answer=answer,
        explanation="A square root needs a nonnegative radicand, and a denominator cannot be zero.\n"
        + m(poly([a, -a * boundary]) + f' \\ge 0, x \\ge {boundary}') + '\n'
        + m(f'x - {excluded} \\ne 0, x \\ne {excluded}') + '\n'
        + f"Trap: {reverse} reverses the root condition; {ignore} allows a zero denominator; {strict} unnecessarily excludes a zero radicand.")


def FUN_09(rng):
    while True:
        a, b, c = rng.randint(1, 3), rng.randint(1, 5), rng.randint(2, 8)
        lo = rng.randint(1, 3)
        hi = lo + rng.randint(3, 6)
        flo, fhi = a * lo * lo + b * lo + c, a * hi * hi + b * hi + c
        right = F(fhi - flo, hi - lo)
        change, add_inputs, origin = F(fhi - flo), F(fhi - flo, hi + lo), F(fhi, hi)
        if len({right, change, add_inputs, origin}) == 4:
            break
    choices, answer = order((right, m(frac(right))), [(v, m(frac(v))) for v in (change, add_inputs, origin)])
    return problem(
        stem=f"For {m('f(x) = ' + poly([a, b, c]))}, what is the average rate of change from {m(f'x = {lo}')} to {m(f'x = {hi}')}?",
        choices=choices, answer=answer,
        explanation="Divide the change in output by the change in input.\n"
        + m(f'f({lo}) = {flo}, f({hi}) = {fhi}') + '\n'
        + m(tfrac(f'{fhi} - {flo}', f'{hi} - {lo}') + ' = ' + frac(right)) + '\n'
        + f"Trap: {m(frac(change))} omits division; {m(frac(add_inputs))} adds the inputs in the denominator; {m(frac(origin))} measures from the origin.")


def FUN_10(rng):
    while True:
        d, gap, k, mult = rng.randint(2, 5), rng.randint(2, 4), rng.randint(2, 6), rng.randint(2, 4)
        a = d + gap
        c = a * mult
        target = F(a * a + k * a + c, gap)
        if target.denominator != 1:
            continue
        sign = F(target * gap - a * a + c, a)
        ignore = F(target - a * a - c, a)
        no_divide = a * k
        if len({F(k), sign, ignore, F(no_divide)}) == 4:
            break
    choices, answer = order((k, m(k)), [(v, m(frac(v))) for v in (sign, ignore, no_divide)])
    return problem(
        stem=f"Let {m('f(x) = ' + tfrac(f'x^{{2}} + kx + {c}', f'x - {d}'))}, where {m('k')} is a constant. If {m(f'f({a}) = {target}')}, what is {m('k')}?",
        choices=choices, answer=answer,
        explanation="Substitute the given input, clear the denominator, and isolate the constant.\n"
        + m(tfrac(f'{a * a} + {a}k + {c}', gap) + f' = {target}') + '\n'
        + m(f'{a}k = {target * gap} - {a * a} - {c} = {a * k}') + '\n'
        + m(f'k = {k}') + '\n'
        + f"Trap: {m(frac(sign))} adds the numerator's constant; {m(frac(ignore))} ignores the denominator; {m(no_divide)} stops before dividing by {m(a)}.")


def QUAD_01(rng):
    a, q = rng.randint(2, 4), rng.randint(1, 4)
    p = q + rng.randint(2, 4)
    right, reverse, positive, negative = (-q, p), (-p, q), (q, p), (-p, -q)
    def label(pair):
        return m('\\{' + f'{pair[0]}, {pair[1]}' + '\\}')
    choices, answer = order((right, label(right)), [(v, label(v)) for v in (reverse, positive, negative)], key=lambda item: item[0])
    return problem(
        stem=f"What is the solution set of {m(poly([a, a * (q - p), 0]) + f' = {a * p * q}')}?",
        choices=choices, answer=answer,
        explanation="Move all terms to one side, factor, and set each factor equal to zero.\n"
        + m(poly([1, q - p, -p * q]) + ' = 0') + '\n'
        + m(f'(x - {p})(x + {q}) = 0') + '\n'
        + m(f'x = {p} \\text{{ or }} x = -{q}') + '\n'
        + f"Trap: {label(reverse)} keeps both factor signs; {label(positive)} loses the negative root; {label(negative)} makes both roots negative.")


def QUAD_02(rng):
    a, p, q = rng.randint(2, 4), rng.randint(3, 7), rng.randint(1, 3)
    b, c = a * p + q, p * q
    total, product = F(b, a), F(c, a)
    right = total * total - 2 * product
    omit, add, undivided = total * total, total * total + 2 * product, total * total - 2 * c
    choices, answer = order((right, m(frac(right))), [(v, m(frac(v))) for v in (omit, add, undivided)])
    return problem(
        stem=f"The roots of {m(poly([a, -b, c]) + ' = 0')} are {m('r')} and {m('s')}. What is {m('r^{2} + s^{2}')}?",
        choices=choices, answer=answer,
        explanation="Use the sum and product of the roots in the square-of-a-sum identity.\n"
        + m('r + s = ' + frac(total) + ', rs = ' + frac(product)) + '\n'
        + m('r^{2} + s^{2} = (r + s)^{2} - 2rs') + '\n'
        + m('(' + frac(total) + ')^{2} - 2(' + frac(product) + ') = ' + frac(right)) + '\n'
        + f"Trap: {m(frac(omit))} omits {m('2rs')}; {m(frac(add))} adds it; {m(frac(undivided))} fails to divide the product by {m(a)}.")


def QUAD_04(rng):
    a, h, v = rng.randint(2, 4), rng.randint(2, 5), -rng.randint(2, 10)
    c = a * h * h + v
    right, sign, constant, outer = (h, v), (-h, v), (h, c), (h, c - h * h)
    def label(point):
        return m(f'({point[0]}, {point[1]})')
    choices, answer = order((right, label(right)), [(w, label(w)) for w in (sign, constant, outer)], key=lambda item: item[0])
    return problem(
        stem=f"What is the vertex of the parabola {m('y = ' + poly([a, -2 * a * h, c]))}?",
        choices=choices, answer=answer,
        explanation="Complete the square after factoring the leading coefficient from the variable terms.\n"
        + m(f'y = {a}(x^{{2}} - {2 * h}x) {signed(c)}') + '\n'
        + m(f'y = {a}(x - {h})^{{2}} - {a * h * h} {signed(c)}') + '\n'
        + m(f'y = {a}(x - {h})^{{2}} {signed(v)}') + '\n'
        + f"Trap: {label(sign)} reverses the horizontal coordinate; {label(constant)} uses the original constant; {label(outer)} forgets the outer factor when adjusting the constant.")


def QUAD_05(rng):
    h, r = rng.randint(2, 5), rng.choice([2, 3, 5, 6, 7, 10])
    c = h * h - r
    right = m(f'{h} \\pm ' + root(r))
    sign = m(f'-{h} \\pm ' + root(r))
    radical = m(f'{h} \\pm ' + root(4 * r))
    no_divide = m(f'{2 * h} \\pm ' + root(4 * r))
    choices, answer = order((1, right), [(0, sign), (2, radical), (3, no_divide)])
    return problem(
        stem=f"What are the solutions of {m(poly([1, -2 * h, c]) + ' = 0')}?",
        choices=choices, answer=answer,
        explanation="Apply the quadratic formula and simplify the radical before dividing both numerator terms.\n"
        + m('x = ' + tfrac(f'{2 * h} \\pm \\sqrt{{{4 * h * h} - 4({paren(c)})}}', 2)) + '\n'
        + m('x = ' + tfrac(f'{2 * h} \\pm ' + root(4 * r), 2) + f' = {h} \\pm ' + root(r)) + '\n'
        + f"Trap: {sign} uses the wrong sign for {m('-b')}; {radical} divides only the first numerator term; {no_divide} omits the denominator.")


def QUAD_07(rng):
    while True:
        a, b, c = rng.randint(2, 5), rng.randint(2, 8), rng.randint(2, 6)
        if b != a * c:
            break
    right = (a, b - a * c, -b * c)
    coefficient, cross_sign, constant_sign = (a, b - c, -b * c), (a, b + a * c, -b * c), (a, b - a * c, b * c)
    choices, answer = order((right, m(poly(right))), [(v, m(poly(v))) for v in (coefficient, cross_sign, constant_sign)], key=lambda item: item[0])
    return problem(
        stem=f"Which expression is equivalent to {m(f'({poly([a, b])})(x - {c})')}?",
        choices=choices, answer=answer,
        explanation="Multiply every term in one factor by every term in the other, then combine like terms.\n"
        + m(f'{a}x^{{2}} - {a * c}x + {b}x - {b * c}') + '\n'
        + m(poly(right)) + '\n'
        + f"Trap: {m(poly(coefficient))} drops {m(a)} from a cross product; {m(poly(cross_sign))} changes that product's sign; {m(poly(constant_sign))} gives the constant the wrong sign.")


def QUAD_08(rng):
    half_b, c = rng.randint(2, 5), rng.randint(2, 6)
    b, bound = 2 * half_b, F(half_b * half_b, c)
    right = m(f'k < {frac(bound)} \\text{{ and }} k \\ne 0')
    linear = m(f'k < {frac(bound)}')
    equal = m(f'k \\le {frac(bound)} \\text{{ and }} k \\ne 0')
    reverse = m(f'k > {frac(bound)}')
    choices, answer = order((1, right), [(0, linear), (2, equal), (3, reverse)])
    return problem(
        stem=f"For which real values of {m('k')} does {m(f'kx^{{2}} + {b}x + {c} = 0')} have exactly two distinct real solutions for {m('x')}?",
        choices=choices, answer=answer,
        explanation="Two distinct real roots require a genuine quadratic and a positive discriminant.\n"
        + m(f'k \\ne 0, {b}^{{2}} - 4(k)({c}) > 0') + '\n'
        + m(f'{b * b} - {4 * c}k > 0, k < {frac(bound)}') + '\n'
        + f"Trap: {linear} includes a linear equation; {equal} allows a repeated root; {reverse} reverses the discriminant inequality.")


def QUAD_09(rng):
    a, b = rng.randint(2, 5), rng.randint(2, 7)
    right, sign, no_roots, one_root = (a, -b), (a, b), (a * a, -b * b), (a, -b * b)
    choices, answer = order((right, m(poly(right))), [(v, m(poly(v))) for v in (sign, no_roots, one_root)], key=lambda item: item[0])
    expression = tfrac(poly([a * a, 0, -b * b]), poly([a, b]))
    return problem(
        stem=f"Which expression is equivalent to {m(expression)} for {m('x \\ne ' + frac(F(-b, a)))}?",
        choices=choices, answer=answer,
        explanation="Factor the difference of squares, then cancel the common nonzero factor.\n"
        + m(poly([a * a, 0, -b * b]) + f' = ({poly([a, -b])})({poly([a, b])})') + '\n'
        + m(expression + ' = ' + poly(right)) + '\n'
        + f"Trap: {m(poly(sign))} keeps the canceled factor; {m(poly(no_roots))} leaves both coefficients squared; {m(poly(one_root))} leaves only the constant squared.")


def QUAD_10(rng):
    while True:
        d, a, k = rng.randint(2, 4), rng.randint(1, 5), rng.randint(-8, 8)
        c = -d ** 3 - a * d * d - k * d
        no_divide = d * k
        wrong_input = F(-d ** 3 + a * d * d + c, d)
        remainder = k + 1
        if c and len({F(k), F(no_divide), wrong_input, F(remainder)}) == 4:
            break
    choices, answer = order((k, m(k)), [(v, m(frac(v))) for v in (no_divide, wrong_input, remainder)])
    polynomial = poly([1, a, 0, 0]) + f' + kx {signed(c)}'
    return problem(
        stem=f"If {m(f'x - {d}')} is a factor of {m(polynomial)}, what is the value of {m('k')}?",
        choices=choices, answer=answer,
        explanation="A factor makes the polynomial equal zero at the factor's root.\n"
        + m(f'{d ** 3} + {a * d * d} + {d}k {signed(c)} = 0') + '\n'
        + m(f'{d}k = {-d ** 3 - a * d * d - c}') + '\n'
        + m(f'k = {k}') + '\n'
        + f"Trap: {m(no_divide)} stops before division; {m(frac(wrong_input))} substitutes {m(-d)}; {m(remainder)} sets the remainder equal to {m(d)} instead of zero.")


def NUM_01(rng):
    first, step, j = rng.randint(3, 9), rng.randint(3, 7), rng.randint(3, 5)
    k = j + rng.randint(3, 5)
    n = k + rng.randint(4, 7)
    aj, ak = first + (j - 1) * step, first + (k - 1) * step
    right = first + (n - 1) * step
    restart, raw, extra = ak + (n - 1) * step, ak + (n - k) * (ak - aj), right + step
    choices, answer = order((right, m(right)), [(v, m(v)) for v in (restart, raw, extra)])
    return problem(
        stem=f"An arithmetic sequence has terms {m(f'a_{{{j}}} = {aj}')} and {m(f'a_{{{k}}} = {ak}')}. What is {m(f'a_{{{n}}}')}?",
        choices=choices, answer=answer,
        explanation="Find the change per term, then count the steps from a known term.\n"
        + m('d = ' + tfrac(f'{ak} - {aj}', f'{k} - {j}') + f' = {step}') + '\n'
        + m(f'a_{{{n}}} = {ak} + ({n} - {k})({step}) = {right}') + '\n'
        + f"Trap: {m(restart)} treats {m(f'a_{{{k}}}')} as the first term; {m(raw)} uses the entire known change as one step; {m(extra)} takes one extra step.")


def NUM_02(rng):
    p, q = rng.choice([(1, 2), (2, 3), (3, 2)])
    scale = rng.randint(2, 5)
    a2, a5 = scale * q ** 3, scale * p ** 3
    ratio = F(p, q)
    right = a5 * ratio ** 2
    wrong_gap, invert, one_step = F(a5 * a5, a2), a5 / ratio ** 2, a5 * ratio
    choices, answer = order((right, m(frac(right))), [(v, m(frac(v))) for v in (wrong_gap, invert, one_step)])
    return problem(
        stem=f"A geometric sequence has positive terms, with {m(f'a_{{2}} = {a2}')} and {m(f'a_{{5}} = {a5}')}. What is {m('a_{7}')}?",
        choices=choices, answer=answer,
        explanation="The exponent on the common ratio equals the gap between term numbers.\n"
        + m('r^{3} = ' + tfrac(a5, a2) + ' = ' + frac(ratio ** 3) + ', r = ' + frac(ratio)) + '\n'
        + m(f'a_{{7}} = {a5}(' + frac(ratio) + ')^{2} = ' + frac(right)) + '\n'
        + f"Trap: {m(frac(wrong_gap))} treats the second-to-fifth gap as two steps; {m(frac(invert))} reverses the ratio; {m(frac(one_step))} advances only one step from the fifth term.")


def NUM_03(rng):
    while True:
        a, b, c, d = (rng.randint(2, 5) for _ in range(4))
        real, imag = a * c + b * d, b * c - a * d
        if abs(imag) > 1 and a * c != b * d:
            break
    right, i_square, cross, drop = (real, imag), (a * c - b * d, imag), (real, b * c + a * d), (a * c, imag)
    def label(value):
        return m(f'{value[0]} {signed(value[1])}i')
    choices, answer = order((right, label(right)), [(v, label(v)) for v in (i_square, cross, drop)], key=lambda item: item[0])
    return problem(
        stem=f"For the imaginary unit {m('i')}, where {m('i^{2} = -1')}, what is {m(f'({a} + {b}i)({c} - {d}i)')}?",
        choices=choices, answer=answer,
        explanation="Distribute, then replace the square of the imaginary unit with negative one.\n"
        + m(f'{a * c} - {a * d}i + {b * c}i - {b * d}i^{{2}}') + '\n'
        + m(f'{a * c} + {b * d} {signed(imag)}i = {real} {signed(imag)}i') + '\n'
        + f"Trap: {label(i_square)} uses {m('i^{2} = 1')}; {label(cross)} adds both imaginary cross products; {label(drop)} drops the product of the imaginary terms.")


def NUM_04(rng):
    while True:
        a, b, c, d = (rng.randint(2, 5) for _ in range(4))
        if a != b and a != c and b != d:
            break
    top, bottom = f'{a}y - {b}x', f'{c}y + {d}x'
    right = m(tfrac(top, bottom))
    swap = m(tfrac(f'{a}x - {b}y', f'{c}x + {d}y'))
    sign = m(tfrac(top, f'{c}y - {d}x'))
    cancel = m(frac(F(a - b, c + d)))
    choices, answer = order((3, right), [(0, cancel), (1, swap), (2, sign)])
    expression = tfrac(tfrac(a, 'x') + ' - ' + tfrac(b, 'y'), tfrac(c, 'x') + ' + ' + tfrac(d, 'y'))
    return problem(
        stem=f"For all {m('x')} and {m('y')} for which the original expression is defined, which expression is equivalent to {m(expression)}?",
        choices=choices, answer=answer,
        explanation="Multiply the entire numerator and denominator by the common denominator.\n"
        + m('xy(' + tfrac(a, 'x') + ' - ' + tfrac(b, 'y') + ') = ' + top) + '\n'
        + m('xy(' + tfrac(c, 'x') + ' + ' + tfrac(d, 'y') + ') = ' + bottom) + '\n'
        + right + '\n'
        + f"Trap: {cancel} cancels across sums; {swap} pairs each coefficient with the wrong variable; {sign} changes the denominator's addition to subtraction.")
