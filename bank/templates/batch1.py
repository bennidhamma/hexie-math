from hexie import *


def PROB_01(rng):
    red = rng.randint(4, 7)
    blue = rng.randint(3, 6)
    green = rng.randint(2, 4)
    total = red + blue + green
    correct = F(red, total) * F(red - 1, total - 1)
    replacement = F(red, total) ** 2
    unchanged_total = F(red * (red - 1), total ** 2)
    one_draw = F(red, total)
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (replacement, unchanged_total, one_draw)],
    )
    return problem(
        stem=f"A bag contains {m(red)} red, {m(blue)} blue, and {m(green)} green marbles. Two marbles are drawn at random without replacement. What is the probability that both are red?",
        choices=choices, answer=answer,
        explanation=(
            "Without replacement, both the red count and the total count decrease after the first red marble.\n"
            f"The bag starts with {m(f'{red}+{blue}+{green}={total}')} marbles.\n"
            f"Multiply the probabilities: {m(tfrac(red, total) + r'\cdot' + tfrac(red - 1, total - 1) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(replacement))} assumes replacement; {m(frac(unchanged_total))} keeps the total unchanged; {m(frac(one_draw))} counts only the first draw."
        ),
    )


def PROB_02(rng):
    denominator = rng.choice([3, 4, 5])
    sensors = rng.choice([3, 4])
    detects = F(denominator - 1, denominator)
    misses = 1 - detects
    correct = 1 - misses ** sensors
    all_detect = detects ** sensors
    none_detect = misses ** sensors
    exactly_one = sensors * detects * misses ** (sensors - 1)
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (all_detect, none_detect, exactly_one)],
    )
    return problem(
        stem=f"A camera turns on if at least one of {m(sensors)} sensors detects movement. Each sensor detects a passing vehicle with probability {m(frac(detects))}, independently of the other sensors. What is the probability that a passing vehicle turns on the camera?",
        choices=choices, answer=answer,
        explanation=(
            "Use the complement: the camera stays off only if every sensor misses the vehicle.\n"
            f"One sensor misses with probability {m('1-' + frac(detects) + '=' + frac(misses))}.\n"
            f"All sensors miss with probability {m(r'\left(' + frac(misses) + r'\right)^{' + str(sensors) + '}=' + frac(none_detect))}.\n"
            f"The camera turns on with probability {m('1-' + frac(none_detect) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(all_detect))} requires every sensor to detect; {m(frac(none_detect))} is the complement; {m(frac(exactly_one))} counts exactly one detection."
        ),
    )


def PROB_03(rng):
    while True:
        a, b, c, d = [rng.randrange(8, 25, 2) for _ in range(4)]
        total = a + b + c + d
        correct = F(a, a + b)
        joint = F(a, total)
        column = F(a, a + c)
        complement = F(b, a + b)
        if len({correct, joint, column, complement}) == 4:
            break
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (joint, column, complement)],
    )
    return problem(
        stem="The table shows how students in two grades travel to school. One of the sophomores in the table is selected at random. What is the probability that this student takes the bus?",
        table={"caption": "Travel to school", "headers": ["Grade", "Takes bus", "Does not take bus"],
               "rows": [["Sophomores", m(a), m(b)], ["Juniors", m(c), m(d)]]},
        choices=choices, answer=answer,
        explanation=(
            "Restrict the sample space to the sophomores.\n"
            f"There are {m(f'{a}+{b}={a+b}')} sophomores.\n"
            f"Of these, {m(a)} take the bus, so the probability is {m(tfrac(a, a+b) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(joint))} uses all students; {m(frac(column))} conditions on taking the bus; {m(frac(complement))} counts sophomores who do not take the bus."
        ),
    )


def PROB_04(rng):
    while True:
        a, b, c, d = [rng.randrange(6, 25, 2) for _ in range(4)]
        total = a + b + c + d
        correct = F(d, b + d)
        joint = F(d, total)
        row = F(d, c + d)
        complement = F(b, b + d)
        if len({correct, joint, row, complement}) == 4:
            break
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (joint, row, complement)],
    )
    return problem(
        stem=f"A total of {m(total)} volunteers each worked exactly one of two shifts. The table shows their club membership and shifts, with one entry missing. If a volunteer is chosen at random from those who worked the afternoon shift, what is the probability that the volunteer is not a club member?",
        table={"caption": "Volunteer shifts", "headers": ["Membership", "Morning", "Afternoon"],
               "rows": [["Club member", m(a), m(b)], ["Not a club member", m(c), "?"]]},
        choices=choices, answer=answer,
        explanation=(
            "Find the missing count, then use only the afternoon column.\n"
            f"The missing count is {m(f'{total}-{a}-{b}-{c}={d}')}.\n"
            f"There are {m(f'{b}+{d}={b+d}')} afternoon volunteers.\n"
            f"The probability is {m(tfrac(d, b+d) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(joint))} uses all volunteers; {m(frac(row))} uses the nonmember row; {m(frac(complement))} counts afternoon club members."
        ),
    )


def PROB_06(rng):
    n = rng.randint(5, 7)
    unrestricted = math.factorial(n)
    adjacent = 2 * math.factorial(n - 1)
    one_order = unrestricted - math.factorial(n - 1)
    correct = unrestricted - adjacent
    choices, answer = order(
        (correct, m(correct)), [(v, m(v)) for v in (adjacent, unrestricted, one_order)],
    )
    return problem(
        stem=f"A group of {m(n)} students, including Maya and Leo, will stand in a single row for a photo. How many different arrangements are possible if Maya and Leo must not stand next to each other?",
        choices=choices, answer=answer,
        explanation=(
            "Subtract the arrangements with Maya and Leo together from all arrangements.\n"
            f"All arrangements: {m(f'{n}!={unrestricted}')}.\n"
            f"Treat Maya and Leo as one block, with either student first: {m(f'2({n-1}!)={adjacent}')}.\n"
            f"Allowed arrangements: {m(f'{unrestricted}-{adjacent}={correct}')}.\n"
            f"Traps: {m(adjacent)} counts adjacent arrangements; {m(unrestricted)} ignores the restriction; {m(one_order)} subtracts only one order within the pair."
        ),
    )


def PROB_07(rng):
    n = rng.randint(6, 10)
    correct = math.comb(n, 3)
    ordered = n * (n - 1) * (n - 2)
    replacement = n ** 3
    pair = math.comb(n, 2)
    choices, answer = order(
        (correct, m(correct)), [(v, m(v)) for v in (ordered, replacement, pair)],
    )
    return problem(
        stem=f"A club with {m(n)} members will choose a committee of {m(3)} members. The committee has no assigned offices. How many different committees can be chosen?",
        choices=choices, answer=answer,
        explanation=(
            "A committee is an unordered group, so divide out the orders of its members.\n"
            f"Ordered selections: {m(f'{n}({n-1})({n-2})={ordered}')}.\n"
            f"Each committee appears {m('3!=6')} times, so there are {m(tfrac(ordered, 6) + '=' + str(correct))} committees.\n"
            f"Traps: {m(ordered)} counts orders; {m(replacement)} also allows repeated members; {m(pair)} chooses only two members."
        ),
    )


def PROB_08(rng):
    while True:
        technicians = rng.randint(3, 5)
        engineers = rng.randint(4, 7)
        total = technicians + engineers
        pairs = math.comb(total, 2)
        no_technician = math.comb(engineers, 2)
        correct = F(pairs - no_technician, pairs)
        exactly_one = F(technicians * engineers, pairs)
        one_draw = F(technicians, total)
        both = F(math.comb(technicians, 2), pairs)
        if len({correct, exactly_one, one_draw, both}) == 4:
            break
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (exactly_one, one_draw, both)],
    )
    return problem(
        stem=f"A project team consists of {m(technicians)} technicians and {m(engineers)} engineers. Two different team members are selected at random, with every pair equally likely. What is the probability that at least one selected member is a technician?",
        choices=choices, answer=answer,
        explanation=(
            "Count all pairs and subtract pairs containing only engineers.\n"
            f"Total pairs: {m(tfrac(f'{total}({total-1})', 2) + '=' + str(pairs))}.\n"
            f"Engineer-only pairs: {m(tfrac(f'{engineers}({engineers-1})', 2) + '=' + str(no_technician))}.\n"
            f"The probability is {m(tfrac(f'{pairs}-{no_technician}', pairs) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(exactly_one))} counts exactly one technician; {m(frac(one_draw))} uses one selection; {m(frac(both))} requires two technicians."
        ),
    )


def PROB_09(rng):
    while True:
        tickets = rng.choice([10, 20])
        big = rng.choice([10, 20, 30])
        small = rng.choice([2, 4, 5])
        cost = rng.choice([2, 3])
        gross = F(big + 2 * small, tickets)
        correct = gross - cost
        if correct < 0:  # keep a losing game, as in the authored version
            break
    missing_prize = F(big + small, tickets) - cost
    winners_only = F(big + 2 * small, 3) - cost
    values = [correct, gross, missing_prize, winners_only]
    # Currency is rounded only for display; all expected values use exact fractions.
    texts = [("-" if v < 0 else "") + money(float(abs(v))) for v in values]
    choices, answer = order((correct, texts[0]), list(zip(values[1:], texts[1:])))
    return problem(
        stem=f"A game costs {money(cost)} to play. A player draws one ticket at random from {m(tickets)} tickets: one pays {money(big)}, two pay {money(small)} each, and the rest pay nothing. What is the expected net change in the player's money per play, to the nearest cent?",
        choices=choices, answer=answer,
        explanation=(
            "Expected net change is the probability-weighted payout minus the cost to play.\n"
            f"Expected payout: {m(tfrac(f'{big}+2({small})', tickets) + '=' + num(float(gross)))} dollars.\n"
            f"Subtract the cost: {m(num(float(gross)) + '-' + str(cost) + '=' + num(float(correct)))} dollars.\n"
            f"Traps: {texts[1]} ignores the cost; {texts[2]} counts only one smaller prize; {texts[3]} averages only the winning tickets."
        ),
    )


def PROB_11(rng):
    band_only = rng.randint(8, 18)
    choir_only = rng.randint(10, 20)
    both = rng.randint(4, 8)
    neither = rng.randint(8, 15)
    band = band_only + both
    choir = choir_only + both
    total = band_only + choir_only + both + neither
    correct = F(band + choir - both, total)
    double_count = F(band + choir, total)
    exactly_one = F(band + choir - 2 * both, total)
    intersection = F(both, total)
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (double_count, exactly_one, intersection)],
    )
    return problem(
        stem=f"Of {m(total)} students in a class, {m(band)} are in band, {m(choir)} are in choir, and {m(both)} are in both. If one student is selected at random, what is the probability that the student is in band or choir or both?",
        choices=choices, answer=answer,
        explanation=(
            "Subtract the overlap once when counting students in either group.\n"
            f"Students in at least one group: {m(f'{band}+{choir}-{both}={band+choir-both}')}.\n"
            f"The probability is {m(tfrac(band+choir-both, total) + ('' if correct.denominator == total else '=' + frac(correct)))}.\n"
            f"Traps: {m(frac(double_count))} counts the overlap twice; {m(frac(exactly_one))} excludes the overlap; {m(frac(intersection))} counts only the overlap."
        ),
    )


def PROB_12(rng):
    while True:
        target = rng.choice([6, 8, 10])
        face = rng.randint(2, 5)
        outcomes = [(a, b) for a in range(1, 7) for b in range(1, 7)]
        sums = sum(a + b == target for a, b in outcomes)
        faces = sum(a == face or b == face for a, b in outcomes)
        overlap = sum(a + b == target and (a == face or b == face) for a, b in outcomes)
        correct = F(sums + faces - overlap, 36)
        double_count = F(sums + faces, 36)
        intersection = F(overlap, 36)
        sum_only = F(sums, 36)
        if len({correct, double_count, intersection, sum_only}) == 4:
            break
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (double_count, intersection, sum_only)],
    )
    return problem(
        stem=f"Two fair six-sided dice, each numbered {m(1)} through {m(6)}, are rolled independently. What is the probability that their sum is {m(target)} or at least one die shows {m(face)}, or both?",
        choices=choices, answer=answer,
        explanation=(
            "Count ordered outcomes and subtract outcomes shared by the two conditions.\n"
            f"There are {m('6(6)=36')} equally likely outcomes; {m(sums)} have sum {m(target)}.\n"
            f"At least one die shows {m(face)} in {m('6+6-1=11')} outcomes; {m(overlap)} also have sum {m(target)}.\n"
            f"The probability is {m(tfrac(f'{sums}+{faces}-{overlap}', 36) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(double_count))} counts the overlap twice; {m(frac(intersection))} requires both conditions; {m(frac(sum_only))} counts only the specified sum."
        ),
    )


def PROB_13(rng):
    scale = rng.randint(3, 5)
    even_parts = rng.randint(11, 13)
    counts = [2 * scale, 3 * scale, 3 * scale, 4 * scale,
              (15 - even_parts) * scale, (even_parts - 7) * scale]
    total = sum(counts)
    even_count = sum(counts[1::2])
    odd_count = total - even_count
    experimental = F(even_count, total)
    theoretical = F(1, 2)
    correct = experimental - theoretical
    compare_frequencies = F(even_count - odd_count, total)
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (experimental, theoretical, compare_frequencies)],
    )
    return problem(
        stem=f"A fair six-sided die numbered {m(1)} through {m(6)} was rolled {m(total)} times, with the results shown in the table. By how much does the experimental probability of rolling an even number exceed the theoretical probability?",
        table={"caption": "Die-roll results", "headers": ["Number rolled", "Frequency"],
               "rows": [[m(face), m(count)] for face, count in enumerate(counts, 1)]},
        choices=choices, answer=answer,
        explanation=(
            "Compare the observed fraction of even rolls with the fair die's probability of an even roll.\n"
            f"Experimental probability: {m(tfrac(f'{counts[1]}+{counts[3]}+{counts[5]}', total) + '=' + frac(experimental))}.\n"
            f"Theoretical probability: {m(r'\frac{3}{6}=\frac{1}{2}')}.\n"
            f"The difference is {m(frac(experimental) + '-' + frac(theoretical) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(experimental))} gives only the experimental probability; {m(frac(theoretical))} gives only the theoretical probability; {m(frac(compare_frequencies))} compares even rolls with odd rolls."
        ),
    )


def PROB_14(rng):
    a, b = rng.choice([(4, 6), (3, 5), (6, 8), (4, 10)])
    common = math.lcm(a, b)
    limit = common * rng.randint(2, 5)
    count_a, count_b, count_both = limit // a, limit // b, limit // common
    correct = F(count_a + count_b - 2 * count_both, limit)
    double_count = F(count_a + count_b, limit)
    inclusive = F(count_a + count_b - count_both, limit)
    intersection = F(count_both, limit)
    choices, answer = order(
        (correct, m(frac(correct))),
        [(v, m(frac(v))) for v in (double_count, inclusive, intersection)],
    )
    return problem(
        stem=f"An integer is selected at random from {m(1)} through {m(limit)}, inclusive, with all integers equally likely. What is the probability that it is divisible by {m(a)} or {m(b)}, but not by both?",
        choices=choices, answer=answer,
        explanation=(
            "Remove common multiples from both divisibility counts because the integer must satisfy exactly one condition.\n"
            f"There are {m(count_a)} multiples of {m(a)} and {m(count_b)} multiples of {m(b)}.\n"
            f"Common multiples are multiples of {m(common)}, so there are {m(count_both)}.\n"
            f"The probability is {m(tfrac(f'{count_a}+{count_b}-2({count_both})', limit) + '=' + frac(correct))}.\n"
            f"Traps: {m(frac(double_count))} counts common multiples twice; {m(frac(inclusive))} includes them once; {m(frac(intersection))} counts only common multiples."
        ),
    )


def PROB_16(rng):
    while True:
        red = rng.choice([8, 10, 12, 14])
        removed = rng.randint(2, 4)
        added = rng.randint(2, 4)
        ratio = rng.randint(1, 3)
        remaining = red - removed
        probability = F(ratio, ratio + 1)
        correct = ratio * remaining - added
        ignore_removal = ratio * red - added
        final_blue = ratio * remaining
        denominator_only = ratio * (remaining + added)
        if correct > 0 and len({correct, ignore_removal, final_blue, denominator_only}) == 4:
            break
    choices, answer = order(
        (correct, m(correct)),
        [(v, m(v)) for v in (ignore_removal, final_blue, denominator_only)],
    )
    return problem(
        stem=f"A bag initially contains {m(red)} red beads and some blue beads, with no other beads. After {m(removed)} red beads are removed and {m(added)} blue beads are added, the probability of drawing a blue bead at random is {m(frac(probability))}. How many blue beads were initially in the bag?",
        choices=choices, answer=answer,
        explanation=(
            "Write the probability using the updated blue count and updated total.\n"
            f"Let {m('x')} be the initial blue count; {m(f'{red}-{removed}={remaining}')} red beads remain.\n"
            f"Then {m(tfrac(f'x+{added}', f'x+{added}+{remaining}') + '=' + frac(probability))}.\n"
            f"Cross-multiplying gives {m(f'x+{added}={ratio}({remaining})={final_blue}')}, so {m(f'x={correct}')}.\n"
            f"Traps: {m(ignore_removal)} ignores the removed red beads; {m(final_blue)} gives the final blue count; {m(denominator_only)} adds the new beads only to the denominator."
        ),
    )


def PCT_01(rng):
    original = rng.choice([80, 120, 160, 200])
    increase = rng.choice([20, 25, 50])
    decrease = rng.choice([10, 20, 25])
    up = 1 + F(increase, 100)
    down = 1 - F(decrease, 100)
    correct = original * up * down
    net_rate = original * (1 + F(increase - decrease, 100))
    ignore_increase = original * down
    ignore_decrease = original * up
    choices, answer = order(
        (correct, money(float(correct))),
        [(v, money(float(v))) for v in (net_rate, ignore_increase, ignore_decrease)],
    )
    return problem(
        stem=f"A store increases the price of a jacket originally priced at {money(original)} by {m(str(increase) + r'\%')}. It then discounts the increased price by {m(str(decrease) + r'\%')}. What is the final price before tax?",
        choices=choices, answer=answer,
        explanation=(
            "Apply each percent change to the price at that stage.\n"
            f"After the increase: {m(f'{original}({num(float(up))})={num(float(original*up))}')} dollars.\n"
            f"After the discount: {m(f'{num(float(original*up))}({num(float(down))})={num(float(correct))}')} dollars.\n"
            f"Traps: {money(float(net_rate))} subtracts the percentages; {money(float(ignore_increase))} skips the increase; {money(float(ignore_decrease))} skips the discount."
        ),
    )


def PCT_02(rng):
    original = rng.choice([80, 120, 160, 200, 240])
    discount = rng.choice([20, 25, 30])
    tax = rng.choice([5, 8, 10])
    down = 1 - F(discount, 100)
    up = 1 + F(tax, 100)
    paid = original * down * up
    ignore_tax = paid / down
    ignore_discount = paid / up
    combine_rates = paid / (1 - F(discount, 100) + F(tax, 100))
    combine_rates = F(math.floor(combine_rates * 100 + F(1, 2)), 100)  # round half up to the cent
    choices, answer = order(
        (original, money(original)),
        [(v, money(float(v))) for v in (ignore_tax, ignore_discount, combine_rates)],
    )
    return problem(
        stem=f"A customer buys a backpack at {m(str(discount) + r'\%')} off its original price, then pays {m(str(tax) + r'\%')} sales tax on the discounted price. The total paid is {money(float(paid))}. What was the original price, to the nearest cent?",
        choices=choices, answer=answer,
        explanation=(
            "Undo the tax and discount by dividing by their multipliers.\n"
            f"Price before tax: {m(num(float(paid)) + r'\div' + num(float(up)) + '=' + num(float(paid/up)))} dollars.\n"
            f"Original price: {m(num(float(paid/up)) + r'\div' + num(float(down)) + '=' + str(original))} dollars.\n"
            f"Traps: {money(float(ignore_tax))} leaves the tax in; {money(float(ignore_discount))} leaves the discount in; {money(float(combine_rates))} combines the rates by subtraction."
        ),
    )


def PCT_03(rng):
    while True:
        before = rng.choice([40, 60, 80, 120])
        rate = rng.choice([25, 50])
        after = before * (100 + rate) // 100
        change = after - before
        correct = F(100 * change, before)
        new_base = F(100 * change, after)
        absolute = F(change)
        total_ratio = F(100 * after, before)
        values = [correct, new_base, absolute, total_ratio]
        if len(set(values)) == 4:
            break
    texts = [m(num(float(v), 1) + r'\%') for v in values]
    choices, answer = order((correct, texts[0]), list(zip(values[1:], texts[1:])))
    return problem(
        stem=f"A shop completed {m(before)} repairs in March and {m(after)} repairs in April. What was the percent increase in the number of repairs, to the nearest tenth of a percent?",
        choices=choices, answer=answer,
        explanation=(
            "Divide the increase by the original number of repairs.\n"
            f"The increase is {m(f'{after}-{before}={change}')} repairs.\n"
            f"The percent increase is {m(tfrac(change, before) + r'\times 100\%=' + frac(correct) + r'\%')}.\n"
            f"Traps: {texts[1]} uses April as the base; {texts[2]} treats the number of additional repairs as a percent; {texts[3]} gives April's total as a percent of March's."
        ),
    )


def PCT_04(rng):
    music_percent, band_percent, base = rng.choice([
        (40, 20, 150), (60, 30, 100), (50, 25, 120), (75, 25, 160),
    ])
    total = base * rng.randint(2, 5)
    music_rate, band_rate = F(music_percent, 100), F(band_percent, 100)
    band = total * music_rate * band_rate
    music = band / band_rate
    ignore_band_rate = band / music_rate
    add_rates = band / (music_rate + band_rate)
    choices, answer = order(
        (total, m(total)),
        [(v, m(frac(v))) for v in (music, ignore_band_rate, add_rates)],
    )
    return problem(
        stem=f"At a school, {m(str(music_percent) + r'\%')} of all students are in the music program. Of the students in the music program, {m(str(band_percent) + r'\%')} are in the marching band. If the marching band has {m(frac(band))} students, how many students attend the school?",
        choices=choices, answer=answer,
        explanation=(
            "Work backward through the two nested groups.\n"
            f"Music-program enrollment: {m(frac(band) + r'\div' + num(float(band_rate)) + '=' + frac(music))}.\n"
            f"School enrollment: {m(frac(music) + r'\div' + num(float(music_rate)) + '=' + str(total))}.\n"
            f"Traps: {m(frac(music))} stops at the music program; {m(frac(ignore_band_rate))} ignores the band percentage; {m(frac(add_rates))} adds the two percentages."
        ),
    )


def PCT_06(rng):
    principal = rng.choice([800, 1600, 2400, 3200])
    percent = rng.choice([5, 10, 20])
    rate = F(percent, 100)
    simple_balance = principal * (1 + 3 * rate)
    compound_balance = principal * (1 + rate) ** 3
    correct = compound_balance - simple_balance
    two_years = principal * rate ** 2
    simple_interest = simple_balance - principal
    compound_interest = compound_balance - principal
    choices, answer = order(
        (correct, money(float(correct))),
        [(v, money(float(v))) for v in (two_years, simple_interest, compound_interest)],
    )
    return problem(
        stem=f"Two accounts each start with {money(principal)}. One earns {m(str(percent) + r'\%')} simple interest per year; the other earns {m(str(percent) + r'\%')} interest compounded annually. No money is deposited or withdrawn. After {m(3)} years, how much greater is the balance in the compound-interest account?",
        choices=choices, answer=answer,
        explanation=(
            "Simple interest uses the original principal each year, while compound interest uses the growing balance.\n"
            f"Simple-interest balance: {m(f'{principal}(1+3({num(float(rate))}))={num(float(simple_balance))}')} dollars.\n"
            f"Compound-interest balance: {m(f'{principal}({num(float(1+rate))})' + '^{3}=' + num(float(compound_balance)))} dollars.\n"
            f"Difference: {m(f'{num(float(compound_balance))}-{num(float(simple_balance))}={num(float(correct))}')} dollars.\n"
            f"Traps: {money(float(two_years))} is the difference after two years; {money(float(simple_interest))} is all the simple interest; {money(float(compound_interest))} is all the compound interest."
        ),
    )


def PCT_07(rng):
    while True:
        art = rng.choice([15, 20, 25])
        sports = rng.choice([30, 35, 40])
        science = rng.choice([10, 15, 20])
        other = 100 - art - sports - science
        scale = rng.randint(2, 4)
        counts = [scale * v for v in (art, sports, science, other)]
        total = sum(counts)
        correct = F(100 * counts[1], total)
        odds = F(100 * counts[1], total - counts[1])
        omit_other = F(100 * counts[1], sum(counts[:3]))
        complement = 100 - correct
        values = [correct, odds, omit_other, complement]
        texts = [m(num(float(v), 1) + r'\%') for v in values]
        if len(set(values)) == 4 and len(set(texts)) == 4:
            break
    choices, answer = order((correct, texts[0]), list(zip(values[1:], texts[1:])))
    return problem(
        stem="Each student in a survey selected exactly one favorite after-school activity category. The results are shown in the table. What percent of the students selected sports, to the nearest tenth of a percent?",
        table={"caption": "Favorite activity", "headers": ["Category", "Number of students"],
               "rows": [[label, m(count)] for label, count in zip(["Art", "Sports", "Science", "Other"], counts)]},
        choices=choices, answer=answer,
        explanation=(
            "Divide the sports count by the total across all categories.\n"
            f"Total students: {m('+'.join(str(v) for v in counts) + '=' + str(total))}.\n"
            f"Sports percentage: {m(tfrac(counts[1], total) + r'\times 100\%=' + frac(correct) + r'\%')}.\n"
            f"Traps: {texts[1]} divides by the nonsports count; {texts[2]} omits Other from the total; {texts[3]} counts students who did not select sports."
        ),
    )


def PCT_08(rng):
    more = rng.choice([40, 50, 60])
    less = rng.choice([20, 25])
    up = 1 + F(more, 100)
    down = 1 - F(less, 100)
    correct = 100 * (up / down - 1)
    add_rates = F(more + less)
    reverse_by_adding = 100 * (up * (1 + F(less, 100)) - 1)
    multiply_down = 100 * (up * down - 1)
    values = [correct, add_rates, reverse_by_adding, multiply_down]
    texts = [m(num(float(v), 1) + r'\%') for v in values]
    choices, answer = order((correct, texts[0]), list(zip(values[1:], texts[1:])))
    return problem(
        stem=f"Tank {m('A')} contains {m(str(more) + r'\%')} more water than tank {m('B')} and {m(str(less) + r'\%')} less water than tank {m('C')}. Tank {m('C')} contains what percent more water than tank {m('B')}, to the nearest tenth of a percent?",
        choices=choices, answer=answer,
        explanation=(
            "Translate each comparison into a multiplier with its own reference tank.\n"
            f"The volumes satisfy {m('A=' + num(float(up)) + 'B')} and {m('A=' + num(float(down)) + 'C')}.\n"
            f"Thus {m(tfrac('C', 'B') + '=' + tfrac(num(float(up)), num(float(down))))}.\n"
            f"The percent increase is {m(r'\left(' + tfrac(num(float(up)), num(float(down))) + r'-1\right)\times 100\%' + ('=' if correct * 10 == int(correct * 10) else r'\approx') + num(float(correct), 1) + r'\%')}.\n"
            f"Traps: {texts[1]} adds the rates; {texts[2]} tries to undo a decrease with the same percent increase; {texts[3]} multiplies by the decrease factor instead of dividing."
        ),
    )
