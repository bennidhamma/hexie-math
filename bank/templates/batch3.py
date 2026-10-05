from hexie import *


def _numeric(correct, wrong):
    return order((correct, m(frac(correct))), [(v, m(frac(v))) for v in wrong])


def _monomial(coefficient, x_power, y_power):
    top, bottom = [], []
    if abs(coefficient) != 1:
        top.append(str(abs(coefficient)))
    for variable, power in (("x", x_power), ("y", y_power)):
        if power:
            term = variable if abs(power) == 1 else f"{variable}^{{{abs(power)}}}"
            (top if power > 0 else bottom).append(term)
    numerator = "".join(top) or "1"
    body = tfrac(numerator, "".join(bottom)) if bottom else numerator
    return ("-" if coefficient < 0 else "") + body


def _scientific(coefficient, exponent):
    coefficient = F(coefficient)
    while coefficient >= 10:
        coefficient /= 10
        exponent += 1
    while coefficient < 1:
        coefficient *= 10
        exponent -= 1
    return f"{num(float(coefficient))} \\times 10^{{{exponent}}}"


def EXP_01(rng):
    while True:
        a, b = rng.randint(2, 5), rng.randint(2, 5)
        c = rng.choice([v for v in range(2, 6) if a * b % v == 0])
        p, t, e = rng.randint(2, 4), rng.randint(1, 2), rng.randint(2, 4)
        s, u, f = rng.randint(2, 4), rng.randint(2, 3), rng.randint(1, 3)
        r, q = p - t + e, s + u - f
        correct = (a * b // c, e, -f)
        wrong = [(a * b // c, e - 2 * t, -f + 2 * u),
                 (a * b // c, p + r - t, q + s - u), (a * b, e, -f)]
        if len(set([correct] + wrong)) == 4 and q > 1:
            break
    render = lambda v: m(_monomial(*v))
    choices, answer = order(((e, -f, correct[0]), render(correct)),
                            [((v[1], v[2], v[0]), render(v)) for v in wrong],
                            key=lambda item: item[0])
    numerator = f"({a}x^{{-{p}}}y^{{{q}}})({b}x^{{{r}}}y^{{-{s}}})"
    denominator = f"{c}x^{{-{t}}}y^{{{u}}}"
    return problem(
        stem=f"For nonzero {m('x')} and {m('y')}, which expression is equivalent to {m(tfrac(numerator, denominator))}?",
        choices=choices, answer=answer,
        explanation="Add exponents when multiplying and subtract exponents when dividing.\n"
        + m(f"{a} \\cdot {b} \\div {c} = {correct[0]}") + "\n"
        + m(f"x^{{-{p}+{r}-(-{t})}}y^{{{q}-{s}-{u}}}=x^{{{e}}}y^{{-{f}}}") + "\n"
        + f"The result is {render(correct)}.\n"
        + f"Traps: {render(wrong[0])} adds the denominator's exponents; {render(wrong[1])} treats negative exponents as positive; {render(wrong[2])} omits division by {m(c)}.")


def EXP_02(rng):
    while True:
        base = rng.choice([2, 3])
        p, q = rng.choice([(2, 3), (3, 2), (2, 4), (4, 2)])
        a, r = rng.randint(1, 4), rng.randint(1, 6)
        correct = F(p * a - r, p - q)
        wrong = [F(p * a + r, p - q), F(a - r, p - q), F(p * a - r, p + q)]
        if len(set([correct] + wrong)) == 4:
            break
    choices, answer = _numeric(correct, wrong)
    equation = f"{base ** p}^{{x-{a}}}=" + tfrac(f"{base ** q}^{{x}}", base ** r)
    return problem(
        stem=f"What real value of {m('x')} satisfies {m(equation)}?",
        choices=choices, answer=answer,
        explanation="Rewrite both sides with the same base, then equate their exponents.\n"
        + m(f"{base}^{{{p}(x-{a})}}={base}^{{{q}x-{r}}}") + "\n"
        + m(f"{p}x-{p*a}={q}x-{r}") + "\n"
        + m(f"({p}-{q})x={p*a-r}") + ", so " + m(f"x={frac(correct)}") + ".\n"
        + f"Traps: {m(frac(wrong[0]))} adds the denominator's exponent; {m(frac(wrong[1]))} fails to distribute {m(p)}; {m(frac(wrong[2]))} adds the coefficients of {m('x')} instead of subtracting.")


def EXP_03(rng):
    while True:
        a, b = rng.randint(2, 5), rng.randint(2, 5)
        if a != b and math.gcd(a, b) == 1:
            break
    correct = F(b, a) ** 2
    wrong = [F(a, b) ** 2, F(b, a), F(b, a) ** 3]
    choices, answer = _numeric(correct, wrong)
    expression = r"\left(" + tfrac(a ** 3, b ** 3) + r"\right)^{-\frac{2}{3}}"
    return problem(
        stem=f"What is the value of {m(expression)}?",
        choices=choices, answer=answer,
        explanation="The denominator of the exponent gives the root, and a negative exponent takes the reciprocal.\n"
        + m(r"\sqrt[3]{" + tfrac(a**3, b**3) + "}=" + frac(F(a, b))) + "\n"
        + m(r"\left(" + frac(F(a, b)) + r"\right)^{-2}=\left(" + frac(F(b, a)) + r"\right)^{2}=" + frac(correct)) + "\n"
        + f"Traps: {m(frac(wrong[0]))} ignores the negative sign; {m(frac(wrong[1]))} omits squaring; {m(frac(wrong[2]))} takes only the reciprocal of the original fraction.")


def EXP_04(rng):
    while True:
        d, u, v = rng.choice([2, 3, 5, 6, 7]), rng.randint(4, 7), rng.randint(2, 4)
        w = rng.randint(2, u - 1)
        k = u + v - w
        combined = d * (u*u + 2*v*v - w*w)
        values = [k*k*d, (u+2*v-w)**2*d, (u+v+w)**2*d, combined]
        if len(set(values)) == 4 and len({u, 2*v, w}) == 3:
            break
    correct_tex = root(d, k)
    wrong_tex = [root(d, u+2*v-w), root(d, u+v+w), root(combined)]
    choices, answer = order((math.sqrt(values[0]), m(correct_tex)),
                            [(math.sqrt(value), m(tex)) for value, tex in zip(values[1:], wrong_tex)])
    expression = f"\\sqrt{{{u*u*d}}}+\\frac{{1}}{{2}}\\sqrt{{{4*v*v*d}}}-\\sqrt{{{w*w*d}}}"
    return problem(
        stem=f"Which expression is equivalent to {m(expression)}?",
        choices=choices, answer=answer,
        explanation="Extract perfect-square factors before combining like radicals.\n"
        + m(f"\\sqrt{{{u*u*d}}}={root(d,u)}, \\sqrt{{{4*v*v*d}}}={root(d,2*v)}, \\sqrt{{{w*w*d}}}={root(d,w)}") + "\n"
        + m(f"({u}+{v}-{w})\\sqrt{{{d}}}={correct_tex}") + "\n"
        + f"Traps: {m(wrong_tex[0])} drops the factor {m(frac(F(1,2)))}; {m(wrong_tex[1])} adds the last radical; {m(wrong_tex[2])} combines the radicands before taking a square root.")


def EXP_05(rng):
    while True:
        c = rng.randint(1, 3)
        d = rng.choice([v for v in [2, 3, 5, 6, 7, 10, 11, 13] if v > c*c])
        k = rng.randint(1, 3)
        n = k * (d - c*c)
        if n % (d + c*c) != 0 and n % d != 0:
            break
    plus = f"(\\sqrt{{{d}}}+{c})"
    correct_tex = (str(k) if k != 1 else "") + plus
    wrong_tex = [(str(k) if k != 1 else "") + f"(\\sqrt{{{d}}}-{c})",
                 tfrac(f"{n}" + plus, d+c*c), tfrac(f"{n}" + plus, d)]
    value = k * (math.sqrt(d) + c)
    wrong = [k*(math.sqrt(d)-c), n*(math.sqrt(d)+c)/(d+c*c), n*(math.sqrt(d)+c)/d]
    choices, answer = order((value, m(correct_tex)), [(v, m(t)) for v, t in zip(wrong, wrong_tex)])
    expression = tfrac(n, f"\\sqrt{{{d}}}-{c}")
    return problem(
        stem=f"Which expression is equivalent to {m(expression)} and has a rational denominator?",
        choices=choices, answer=answer,
        explanation="Multiply numerator and denominator by the conjugate of the denominator.\n"
        + m(expression + r"\cdot " + tfrac(plus, plus) + "=" + tfrac(f"{n}" + plus, f"{d}-{c*c}")) + "\n"
        + m(tfrac(f"{n}" + plus, d-c*c) + "=" + correct_tex) + "\n"
        + f"Traps: {m(wrong_tex[0])} keeps the minus sign in the numerator; {m(wrong_tex[1])} adds the squares in the denominator; {m(wrong_tex[2])} omits the subtracted square.")


def EXP_06(rng):
    doubling, start = rng.randint(2, 5), rng.randint(1, 4)
    count = rng.choice([50, 75, 100, 125])
    steps = rng.choice([4, 6])
    observed_time, observed_count = start + 2*doubling, count*4
    target = count * 2**steps
    correct = start + steps*doubling
    wrong = [steps*doubling, start + steps*(observed_time-start),
             start + F(target-count, observed_count-count)*(observed_time-start)]
    choices, answer = _numeric(correct, wrong)
    return problem(
        stem=f"A bacterial population doubles at a constant time interval. At hour {m(start)}, it contains {m(count)} bacteria; at hour {m(observed_time)}, it contains {m(observed_count)}. At what hour will it first contain {m(target)} bacteria?",
        choices=choices, answer=answer,
        explanation="Use the observed growth to find the doubling time, then count the required doublings.\n"
        + m(f"{tfrac(observed_count,count)}=4=2^{{2}}") + f", so one doubling takes {m(tfrac(observed_time-start,2)+'='+str(doubling))} hours.\n"
        + m(f"{tfrac(target,count)}=2^{{{steps}}}") + f", so {m(steps)} doublings are needed after hour {m(start)}.\n"
        + m(f"{start}+{steps}({doubling})={correct}") + " hours.\n"
        + f"Traps: {m(frac(wrong[0]))} gives elapsed time only; {m(frac(wrong[1]))} treats the observed interval as one doubling; {m(frac(wrong[2]))} assumes linear growth.")


def EXP_07(rng):
    a, b, c = rng.choice([(4,6,2), (6,8,4), (3,8,2), (5,6,2), (6,6,2), (8,8,4), (6,8,2)])
    p, q, r = rng.randint(3, 6), rng.randint(-5, -2), rng.randint(-3, -1)
    coefficient, exponent = F(a*b,c), p+q-r
    correct = coefficient * F(10)**exponent
    wrong = [correct/10, coefficient*F(10)**(p+q+r), F(a+b,c)*F(10)**exponent]
    correct_tex = _scientific(coefficient, exponent)
    wrong_tex = [_scientific(coefficient, exponent-1), _scientific(coefficient, p+q+r), _scientific(F(a+b,c), exponent)]
    choices, answer = order((correct, m(correct_tex)), [(v, m(t)) for v, t in zip(wrong, wrong_tex)])
    expression = tfrac(f"({a}\\times 10^{{{p}}})({b}\\times 10^{{{q}}})", f"{c}\\times 10^{{{r}}}")
    coefficient_step = tfrac(str(a) + r"\cdot " + str(b), c)
    return problem(
        stem=f"What is the value of {m(expression)}, written in scientific notation?",
        choices=choices, answer=answer,
        explanation="Calculate the coefficient and power of ten separately, then normalize the coefficient.\n"
        + m(coefficient_step + "=" + frac(coefficient)) + "\n"
        + m(f"{p}+({q})-({r})={exponent}") + "\n"
        + m(f"{frac(coefficient)}\\times 10^{{{exponent}}}={correct_tex}") + "\n"
        + f"Traps: {m(wrong_tex[0])} moves the decimal without changing the exponent; {m(wrong_tex[1])} adds the denominator's exponent; {m(wrong_tex[2])} adds the coefficients in the numerator.")


def EXP_08(rng):
    shift, exponent = rng.randint(2, 4), rng.randint(3, 6)
    total = (2**shift - 1) * 2**exponent
    correct = F(total, 2*(2**shift-1))
    wrong = [F(total, 2**shift-1), F(total, 2*2**shift), F(total, 2*(shift-1))]
    choices, answer = _numeric(correct, wrong)
    return problem(
        stem=f"If {m(f'2^{{x+{shift}}}-2^{{x}}={total}')}, what is the value of {m('2^{x-1}')}?",
        choices=choices, answer=answer,
        explanation=f"Factor out {m('2^{x}')} before solving for the requested power.\n"
        + m(f"2^{{x}}(2^{{{shift}}}-1)={total}") + "\n"
        + m(f"2^{{x}}={tfrac(total,2**shift-1)}={2**exponent}") + "\n"
        + m(f"2^{{x-1}}={tfrac(2**exponent,2)}={frac(correct)}") + "\n"
        + f"Traps: {m(frac(wrong[0]))} stops at {m('2^{x}')}; {m(frac(wrong[1]))} drops the subtracted term; {m(frac(wrong[2]))} uses {m(shift)} instead of {m(f'2^{{{shift}}}')} as the multiplier.")


def EXP_09(rng):
    a, p, q, k = rng.randint(2, 5), rng.randint(3, 5), rng.randint(1, 3), rng.choice([2, 3])
    correct = ((-a)**k, p*k, -q*k)
    wrong = [(-a*k, p*k, -q*k), (-a, p*k, -q*k), ((-a)**k, p+k, -q+k)]
    choices, answer = order((correct, m(_monomial(*correct))),
                            [(v, m(_monomial(*v))) for v in wrong], key=lambda item: item[0])
    expression = f"(-{a}x^{{{p}}}y^{{-{q}}})^{{{k}}}"
    return problem(
        stem=f"For nonzero {m('x')} and {m('y')}, which expression is equivalent to {m(expression)}?",
        choices=choices, answer=answer,
        explanation="Raise every factor to the outer power, multiplying the exponents on powers.\n"
        + m(f"(-{a})^{{{k}}}={correct[0]}, (x^{{{p}}})^{{{k}}}=x^{{{p*k}}}, (y^{{-{q}}})^{{{k}}}=y^{{-{q*k}}}") + "\n"
        + f"The result is {m(_monomial(*correct))}.\n"
        + f"Traps: {m(_monomial(*wrong[0]))} multiplies the coefficient by the outer exponent; {m(_monomial(*wrong[1]))} leaves the coefficient unchanged; {m(_monomial(*wrong[2]))} adds exponents instead of multiplying.")


def EXP_10(rng):
    lost = rng.choice([F(1, 5), F(1, 4)])
    retained = 1 - lost
    interval, elapsed = rng.randint(2, 5), rng.randint(2, 3)
    first, last = interval, interval*(elapsed+1)
    amount = rng.randint(1, 3) * retained.denominator**(elapsed+1)
    correct = amount * retained**elapsed
    wrong = [amount*lost**elapsed, amount*(1-elapsed*lost), amount*retained**(elapsed+1)]
    choices, answer = _numeric(correct, wrong)
    percent = m(str(int(lost*100)) + r"\%")
    return problem(
        stem=f"A chemical sample loses {percent} of its remaining mass every {m(interval)} hours. At {m(first)} hours after an experiment begins, its mass is {m(amount)} grams. What is its mass, in grams, at {m(last)} hours after the experiment begins?",
        choices=choices, answer=answer,
        explanation="Apply the retained fraction once for each interval after the given measurement.\n"
        + m(f"{tfrac(str(last)+'-'+str(first),interval)}={elapsed}") + " intervals.\n"
        + m(f"1-{frac(lost)}={frac(retained)}") + " of the mass remains each interval.\n"
        + m(f"{amount}\\left({frac(retained)}\\right)^{{{elapsed}}}={frac(correct)}") + " grams.\n"
        + f"Traps: {m(frac(wrong[0]))} uses the lost fraction as the retained fraction; {m(frac(wrong[1]))} subtracts the same mass each interval; {m(frac(wrong[2]))} counts intervals from the start of the experiment.")


def REW_01(rng):
    while True:
        a, b, c = rng.randint(2, 7), rng.randint(2, 6), rng.randint(2, 5)
        if math.gcd(math.gcd(a, b), c) == 1:
            break
    correct = tfrac(f"{c}P-{a}x", b)
    wrong = [tfrac(f"P-{a}x", b), tfrac(f"{c}(P-{a}x)", b), tfrac(f"{c}P+{a}x", b)]
    choices = [m(wrong[0]), m(wrong[1]), m(correct), m(wrong[2])]
    equation = "P=" + tfrac(f"{a}x+{b}y", c)
    return problem(
        stem=f"If {m(equation)}, which expression equals {m('y')}?",
        choices=choices, answer=2,
        explanation=f"Clear the denominator, then isolate the term containing {m('y')}.\n"
        + m(f"{c}P={a}x+{b}y") + "\n"
        + m(f"{b}y={c}P-{a}x") + "\n"
        + m("y=" + correct) + "\n"
        + f"Traps: {m(wrong[0])} drops the original denominator; {m(wrong[1])} multiplies the subtracted term by {m(c)} too; {m(wrong[2])} adds instead of subtracting {m(f'{a}x')}.")


def REW_02(rng):
    while True:
        a, b, c, d = rng.randint(2, 5), rng.randint(1, 6), rng.randint(2, 5), rng.randint(2, 5)
        if math.gcd(math.gcd(a, b), math.gcd(c, d)) == 1:
            break
    correct = tfrac(f"{d}y+{b}", f"{c}y-{a}")
    wrong = [tfrac(f"{d}y-{b}", f"{c}y-{a}"), tfrac(f"{d}y+{b}", f"{c}y+{a}"), tfrac(f"{c}y-{a}", f"{d}y+{b}")]
    choices = [m(wrong[0]), m(correct), m(wrong[1]), m(wrong[2])]
    equation = "y=" + tfrac(f"{a}x+{b}", f"{c}x-{d}")
    restrictions = m(f"{c}x\\ne {d}") + " and " + m(f"{c}y\\ne {a}")
    return problem(
        stem=f"If {m(equation)}, with {restrictions}, which expression equals {m('x')}?",
        choices=choices, answer=1,
        explanation=f"Collect the terms containing {m('x')} and factor out {m('x')}.\n"
        + m(f"{c}xy-{d}y={a}x+{b}") + "\n"
        + m(f"x({c}y-{a})={d}y+{b}") + "\n"
        + m("x=" + correct) + "\n"
        + f"Traps: {m(wrong[0])} changes the sign of the constant {m(b)}; {m(wrong[1])} adds {m(a)} when collecting terms; {m(wrong[2])} reverses the final quotient.")


def REW_03(rng):
    while True:
        a, c, e = rng.randint(1, 7), rng.randint(1, 7), rng.randint(1, 5)
        b, d = rng.randint(2, 5), rng.randint(2, 6)
        correct = F(b*d*e+d*a-b*c, b+d)
        wrong = [F(b*d*e-d*a-b*c, b+d), F(e+d*a-b*c, b+d), F(e*(b+d)+a-c, 2)]
        if b != d and correct != a and correct.denominator == 1 and 1 <= correct <= 15 and len(set([correct]+wrong)) == 4:
            break
    choices, answer = _numeric(correct, wrong)
    equation = tfrac(f"x-{a}", b) + "+" + tfrac(f"x+{c}", d) + f"={e}"
    return problem(
        stem=f"What value of {m('x')} satisfies {m(equation)}?",
        choices=choices, answer=answer,
        explanation="Multiply every term by a common denominator before combining like terms.\n"
        + m(f"{d}(x-{a})+{b}(x+{c})={b*d*e}") + "\n"
        + m(f"{b+d}x={b*d*e+d*a-b*c}") + "\n"
        + m(f"x={frac(correct)}") + "\n"
        + f"Traps: {m(frac(wrong[0]))} changes the sign of {m(a)} inside the first numerator; {m(frac(wrong[1]))} fails to multiply the right side; {m(frac(wrong[2]))} adds the two denominators.")


def REW_04(rng):
    while True:
        a, b, d = rng.randint(2, 4), rng.randint(2, 5), rng.randint(1, 7)
        center = rng.randint(2, 5)
        c = b * center
        distance = rng.randint(c+1, c+6)
        rhs = a*distance+d
        correct = F(2*c, b)
        wrong = [F(c+distance, b), F(2*distance, b), 2*c]
        if len(set([correct]+wrong)) == 4:
            break
    choices, answer = _numeric(correct, wrong)
    equation = f"{a}\\left|{b}x-{c}\\right|+{d}={rhs}"
    positive, negative = F(c+distance, b), F(c-distance, b)
    return problem(
        stem=f"What is the sum of all real solutions of {m(equation)}?",
        choices=choices, answer=answer,
        explanation="An absolute value equal to a positive number gives two linear equations.\n"
        + m(f"\\left|{b}x-{c}\\right|={distance}") + "\n"
        + m(f"{b}x-{c}={distance}") + " or " + m(f"{b}x-{c}=-{distance}") + "\n"
        + m(f"x={frac(positive)}") + " or " + m(f"x={frac(negative)}") + "\n"
        + m(f"{frac(positive)}+({frac(negative)})={frac(correct)}") + "\n"
        + f"Traps: {m(frac(wrong[0]))} uses only the positive branch; {m(frac(wrong[1]))} adds the absolute values of the solutions; {m(frac(wrong[2]))} omits division by {m(b)}.")


def REW_05(rng):
    while True:
        a, b = rng.randint(1, 4), rng.randint(2, 7)
        if a < b and math.gcd(a, b) == 1:
            break
    a_tex = "" if a == 1 else str(a)
    fraction = tfrac(f"{b}V", f"{a_tex}\\pi h")
    correct = r"\sqrt{" + fraction + "}"
    wrong = [fraction, r"\sqrt{" + tfrac(f"{a_tex}V", f"{b}\\pi h") + "}",
             tfrac(f"\\sqrt{{{b}V}}", f"{a_tex}\\pi h")]
    choices = [m(wrong[0]), m(wrong[1]), m(correct), m(wrong[2])]
    equation = f"V={frac(F(a,b))}\\pi r^{{2}}h"
    return problem(
        stem=f"Positive quantities {m('V')}, {m('r')}, and {m('h')} satisfy {m(equation)}. Which expression gives {m('r')}?",
        choices=choices, answer=2,
        explanation="Isolate the squared variable, then take the positive square root.\n"
        + m(f"{b}V={a_tex}\\pi r^{{2}}h") + "\n"
        + m("r^{2}=" + fraction) + "\n"
        + m("r=" + correct) + "\n"
        + f"Traps: {m(wrong[0])} stops at {m('r^{2}')}; {m(wrong[1])} reverses the fraction incorrectly; {m(wrong[2])} takes the square root of only the numerator.")


def REW_06(rng):
    while True:
        k, d, e, b = rng.randint(2, 4), rng.randint(2, 4), rng.randint(1, 7), rng.randint(2, 6)
        if e != d*b:
            break
    a, c = k*d, k*e
    correct = (k, -k*b)
    wrong = [(1, -b), (k, -b), (k, k*b)]
    choices, answer = order((correct, m(poly(correct))), [(v, m(poly(v))) for v in wrong], key=lambda item: item[0])
    expression = tfrac(f"{a}x(x-{b})-{c}(x-{b})", f"{d}x-{e}")
    restriction = m("x\\ne " + frac(F(e,d)))
    return problem(
        stem=f"For {restriction}, which expression is equivalent to {m(expression)}?",
        choices=choices, answer=answer,
        explanation="Factor out the repeated binomial, then cancel the common factor.\n"
        + m(f"{a}x(x-{b})-{c}(x-{b})=(x-{b})({a}x-{c})") + "\n"
        + m(f"{a}x-{c}={k}({d}x-{e})") + "\n"
        + m(expression + f"={k}(x-{b})=" + poly(correct)) + "\n"
        + f"Traps: {m(poly(wrong[0]))} drops the factor {m(k)}; {m(poly(wrong[1]))} fails to distribute {m(k)} to the constant; {m(poly(wrong[2]))} changes the subtraction to addition.")


def REW_07(rng):
    while True:
        a, b, c, d = rng.randint(3, 12), rng.randint(2, 5), rng.randint(2, 4), rng.randint(1, 5)
        bound = rng.randint(1, 6)
        rhs = a+b*d-b*c*bound
        sign_error = F(a-b*d-rhs, b*c)
        moving_error = F(a+b*d+rhs, b*c)
        if len({F(bound), sign_error, moving_error}) == 3:
            break
    correct = m(f"x\\ge {bound}")
    wrong = [m(f"x\\le {bound}"), m("x\\ge " + frac(sign_error)), m("x\\ge " + frac(moving_error))]
    choices, answer = order(((F(bound), 1), correct), [((F(bound),0),wrong[0]), ((sign_error,1),wrong[1]), ((moving_error,1),wrong[2])], key=lambda item: item[0])
    inequality = f"{a}-{b}({c}x-{d})\\le {rhs}"
    return problem(
        stem=f"Which inequality describes all real solutions of {m(inequality)}?",
        choices=choices, answer=answer,
        explanation="Reverse the inequality when dividing by a negative number.\n"
        + m(f"{a+b*d}-{b*c}x\\le {rhs}") + "\n"
        + m(f"-{b*c}x\\le {rhs-a-b*d}") + "\n"
        + correct + "\n"
        + f"Traps: {wrong[0]} keeps the inequality direction; {wrong[1]} distributes the negative sign incorrectly; {wrong[2]} uses the wrong sign for the right-side constant when rearranging.")


def REW_08(rng):
    while True:
        c, v = rng.randint(2, 6), rng.randint(1, 3)
        u = v + rng.randint(2, 5)
        a, b = u-v, u*v-c*(u-v)
        good, bad = c+u, c-v
        if b > 0 and bad != 0:
            break
    solution_sum = good+bad
    singleton = lambda value: m(r"\{" + str(value) + r"\}")
    both = m(r"\{" + f"{bad}, {good}" + r"\}")
    choices, answer = order(((1,good), singleton(good)), [((1,bad),singleton(bad)), ((1,solution_sum),singleton(solution_sum)), ((2,bad),both)], key=lambda item: item[0])
    equation = r"\sqrt{" + poly([a,b]) + f"}}=x-{c}"
    factored = f"(x{signed(-good)})(x{signed(-bad)})=0"
    return problem(
        stem=f"Which set contains all real solutions of {m(equation)}?",
        choices=choices, answer=answer,
        explanation="Squaring can introduce an extra root, so check both candidates in the original equation.\n"
        + m(poly([a,b]) + f"=(x-{c})^{{2}}") + "\n"
        + m(factored) + f", giving {m(f'x={bad}')} or {m(f'x={good}')}.\n"
        + m(f"x={bad}") + f" gives {m(f'{v}=-{v}')}, which is false.\n"
        + m(f"x={good}") + f" gives {m(f'{u}={u}')}, so the solution set is {singleton(good)}.\n"
        + f"Traps: {singleton(bad)} keeps only the rejected root; {both} skips the check; {singleton(solution_sum)} adds the candidates instead of checking them.")


def LOG_01(rng):
    while True:
        base, exponent = rng.choice([(2,3), (3,2), (3,4), (4,3), (5,2), (5,3)])
        offset = rng.randint(2, min(8, base**exponent-1))
        correct = base**exponent-offset
        wrong = [base*exponent-offset, exponent**base-offset, base**exponent+offset]
        if len(set([correct]+wrong)) == 4:
            break
    choices, answer = _numeric(correct, wrong)
    equation = f"\\log_{{{base}}}(x+{offset})={exponent}"
    return problem(
        stem=f"What value of {m('x')} satisfies {m(equation)}?",
        choices=choices, answer=answer,
        explanation="Rewrite a logarithmic equation as a power of its base.\n"
        + m(f"x+{offset}={base}^{{{exponent}}}={base**exponent}") + "\n"
        + m(f"x={base**exponent}-{offset}={correct}") + "\n"
        + f"Traps: {m(wrong[0])} multiplies the base by the exponent; {m(wrong[1])} swaps the base and exponent; {m(wrong[2])} adds the offset instead of subtracting it.")


def LOG_02(rng):
    while True:
        base, p, q, r = rng.choice([2,3,5]), rng.randint(3,5), rng.choice([2,4,6]), rng.randint(2,4)
        correct = F(2*p) + F(q,2) - r
        wrong = [F(2*p)+F(q,2)+r, F(2*p+q-r), F(p*p)+F(q,2)-r]
        if len(set([correct]+wrong)) == 4:
            break
    choices, answer = _numeric(correct, wrong)
    argument = tfrac(r"u^{2}\sqrt{v}", base**r)
    expression = f"\\log_{{{base}}}\\left({argument}\\right)"
    given_u = m(f"\\log_{{{base}}}u={p}")
    given_v = m(f"\\log_{{{base}}}v={q}")
    return problem(
        stem=f"For positive numbers {m('u')} and {m('v')}, {given_u} and {given_v}. What is the value of {m(expression)}?",
        choices=choices, answer=answer,
        explanation="Use the product, quotient, and power rules to separate the logarithm.\n"
        + m(expression + f"=2\\log_{{{base}}}u+\\frac{{1}}{{2}}\\log_{{{base}}}v-\\log_{{{base}}}{base**r}") + "\n"
        + m(f"2({p})+\\frac{{1}}{{2}}({q})-{r}={frac(correct)}") + "\n"
        + f"Traps: {m(frac(wrong[0]))} adds the denominator's logarithm; {m(frac(wrong[1]))} ignores the square root; {m(frac(wrong[2]))} squares the logarithm instead of multiplying it by two.")


def LOG_03(rng):
    while True:
        base, p, q = rng.choice([2,3]), rng.choice([2,3]), rng.randint(1,5)
        if q % p != 0:
            break
    correct = F(-q,p)
    wrong = [F(-q), F(q,p), F(-p,q)]
    choices, answer = _numeric(correct, wrong)
    expression = f"\\log_{{{base**p}}}\\left({tfrac(1,base**q)}\\right)"
    return problem(
        stem=f"What is the value of {m(expression)}?",
        choices=choices, answer=answer,
        explanation="Express the base and reciprocal argument as powers of the same number.\n"
        + f"Let {m('y')} be the logarithm: " + m(f"({base}^{{{p}}})^{{y}}={base}^{{-{q}}}") + ".\n"
        + m(f"{p}y=-{q}") + "\n"
        + m(f"y={frac(correct)}") + "\n"
        + f"Traps: {m(frac(wrong[0]))} ignores the power in the base; {m(frac(wrong[1]))} ignores the reciprocal; {m(frac(wrong[2]))} reverses the ratio of exponents.")


def LOG_04(rng):
    base, exponent, lower = rng.choice([(2,3,1), (2,4,1), (2,5,1), (2,5,2), (3,3,1), (3,4,1), (5,3,1)])
    good, magnitude = base**(exponent-lower), base**lower
    offset, bad = good-magnitude, -magnitude
    product = base**exponent
    sum_error = F(product+offset,2)
    singleton = lambda value: m(r"\{" + frac(value) + r"\}")
    both = m(r"\{" + f"{bad}, {good}" + r"\}")
    choices, answer = order(((1,F(good)),singleton(good)), [((1,F(bad)),singleton(bad)), ((1,sum_error),singleton(sum_error)), ((2,F(bad)),both)], key=lambda item: item[0])
    equation = f"\\log_{{{base}}}x+\\log_{{{base}}}(x-{offset})={exponent}"
    return problem(
        stem=f"Which set contains all real solutions of {m(equation)}?",
        choices=choices, answer=answer,
        explanation="Combine the logarithms using a product, and require both original arguments to be positive.\n"
        + m(f"x>{offset}") + " is required.\n"
        + m(f"x(x-{offset})={base}^{{{exponent}}}={product}") + "\n"
        + m(f"(x-{good})(x+{magnitude})=0") + f", giving {m(f'x={good}')} or {m(f'x={bad}')}.\n"
        + f"Only {m(good)} is greater than {m(offset)}, so the solution set is {singleton(good)}.\n"
        + f"Traps: {singleton(bad)} keeps only the invalid root; {both} ignores the domain; {singleton(sum_error)} adds the arguments instead of multiplying them.")


def LOG_05(rng):
    while True:
        a, b = rng.sample([2,3,5,7],2)
        log_a, log_b = F(round(math.log(a)*1000),1000), F(round(math.log(b)*1000),1000)
        correct = round(float((log_a+log_b)/(2*log_b)),2)
        wrong = [round(float(2*log_b/(log_a+log_b)),2), round(float((log_a+log_b)/log_b),2), round(float(log_a/2),2)]
        if len(set([correct]+wrong)) == 4 and correct == round(math.log(a*b)/math.log(b*b),2):
            break
    display = lambda value: m(f"{value:.2f}")
    choices, answer = order((correct,display(correct)), [(v,display(v)) for v in wrong])
    given_a = f"\\ln {a}\\approx {num(float(log_a),3)}"
    given_b = f"\\ln {b}\\approx {num(float(log_b),3)}"
    target = f"\\log_{{{b*b}}}{a*b}"
    ratio = tfrac(f"\\ln {a}+\\ln {b}",f"2\\ln {b}")
    substituted = tfrac(num(float(log_a),3)+"+"+num(float(log_b),3), "2("+num(float(log_b),3)+")")
    return problem(
        stem=f"Use {m(given_a)} and {m(given_b)}. What is {m(target)}, to the nearest hundredth?",
        choices=choices, answer=answer,
        explanation="Apply change of base, then expand the logarithms of the product and the square.\n"
        + m(target + "=" + tfrac(f"\\ln {a*b}",f"\\ln {b*b}") + "=" + ratio) + "\n"
        + m(substituted + f"\\approx {correct:.2f}") + "\n"
        + f"Traps: {display(wrong[0])} reverses the change-of-base quotient; {display(wrong[1])} forgets that the base is a square; {display(wrong[2])} multiplies the logarithms of the factors.")


def LOG_06(rng):
    while True:
        base, a, k, c = rng.choice([2,3,5]), rng.randint(3,7), rng.randint(2,4), rng.randint(1,3)
        ratio = rng.choice([6,7,10,12,15])
        rhs = a*ratio
        value = (math.log(ratio)/math.log(base)-c)/k
        wrong_values = [(math.log(rhs)/math.log(base)-c)/k, (math.log(ratio)/math.log(base)+c)/k, math.log(ratio)/math.log(base)-c]
        if all(abs(v-w)>1e-8 for i,v in enumerate([value]+wrong_values) for w in ([value]+wrong_values)[i+1:]):
            break
    offset = (str(c) if c != 1 else "") + f"\\ln {base}"
    denominator = f"{k}\\ln {base}"
    correct = tfrac(f"\\ln {ratio}-{offset}",denominator)
    wrong = [tfrac(f"\\ln {rhs}-{offset}",denominator), tfrac(f"\\ln {ratio}+{offset}",denominator), tfrac(f"\\ln {ratio}-{offset}",f"\\ln {base}")]
    choices, answer = order((value,m(correct)), [(v,m(t)) for v,t in zip(wrong_values,wrong)])
    equation = f"{a}\\cdot {base}^{{{k}x+{c}}}={rhs}"
    return problem(
        stem=f"Which expression gives the real solution of {m(equation)}?",
        choices=choices, answer=answer,
        explanation="Isolate the exponential factor, take logarithms, and solve the resulting linear equation.\n"
        + m(f"{base}^{{{k}x+{c}}}={ratio}") + "\n"
        + m(f"({k}x+{c})\\ln {base}=\\ln {ratio}") + "\n"
        + m("x=" + correct) + "\n"
        + f"Traps: {m(wrong[0])} forgets to divide by {m(a)}; {m(wrong[1])} adds the exponent's constant term when isolating {m('x')}; {m(wrong[2])} omits division by {m(k)}.")
