from hexie import *


def RAT_01(rng):
    a, b, c = rng.choice([(2, 3, 5), (3, 4, 5), (2, 5, 3), (1, 3, 4)])
    unit = (a + b) * rng.randint(3, 7)
    total = (a + b + c) * unit
    correct = b * unit
    omit = F(total * b, a + b)
    other = c * unit
    choices, answer = order(
        (correct, m(correct)),
        [(unit, m(unit)), (other, m(other)), (omit, m(frac(omit)))],
    )
    return problem(
        stem=f"A school distributes {m(total)} notebooks among the sixth, seventh, and eighth grades in the ratio {m(f'{a}:{b}:{c}')}, respectively. How many notebooks does the seventh grade receive?",
        choices=choices, answer=answer,
        explanation=f"Divide the total by the sum of the ratio parts, then use the seventh grade's share.\n"
        f"{m(f'{a}+{b}+{c}={a+b+c}')} parts, so each part is {m(tfrac(total, a+b+c)+f'={unit}')} notebooks.\n"
        f"The seventh grade receives {m(f'{b}'+r'\cdot'+f'{unit}={correct}')} notebooks.\n"
        f"Trap: {m(unit)} is just one part; {m(other)} is the eighth grade's share; {m(frac(omit))} leaves the eighth grade out of the ratio total.",
    )


def RAT_02(rng):
    while True:
        a, b, c, d = rng.choice([(2, 3, 3, 4), (3, 4, 5, 6), (3, 5, 5, 8), (4, 5, 5, 6)])
        t = rng.randint(2, 5)
        k = d * t
        added = (b * c - a * d) * t
        correct = (a + b) * k
        red = a * k
        current = correct + added
        unaligned = F(added * (a + b), c - a)
        if len({correct, red, current, unaligned}) == 4:
            break
    choices, answer = order((correct, m(correct)), [(v, m(frac(v))) for v in (red, current, unaligned)])
    return problem(
        stem=f"A bin contains only red and blue tiles in the ratio {m(f'{a}:{b}')}. After {m(added)} red tiles are added, the ratio of red to blue tiles is {m(f'{c}:{d}')}. How many tiles were in the bin originally?",
        choices=choices, answer=answer,
        explanation=f"Use one multiplier for the original ratio, and keep the blue count unchanged.\n"
        f"Let the original red and blue counts be {m(f'{a}k')} and {m(f'{b}k')}.\n"
        f"{m(tfrac(f'{a}k+{added}', f'{b}k')+'='+tfrac(c,d))}, so {m(f'{d}({a}k+{added})={b*c}k')} and {m(f'k={k}')}.\n"
        f"The original total is {m(f'({a}+{b})'+r'\cdot'+f'{k}={correct}')}.\n"
        f"Trap: {m(red)} counts only the original red tiles; {m(current)} is the new total; {m(frac(unaligned))} subtracts ratio terms without matching their blue parts.",
    )


def RAT_03(rng):
    while True:
        a, b = rng.choice([(4, 6), (6, 8), (8, 12)])
        ua = rng.choice([70, 75, 80, 85, 90, 95])
        ub = rng.choice([40, 45, 50, 55, 60, 65])
        pa, pb = F(a * ua, 100), F(b * ub, 100)
        count = math.lcm(a, b) * rng.randint(2, 4)
        correct = F(count * (ua - ub), 100)
        pack_gap = abs(pa - pb)
        unit_gap = F(ua - ub, 100)
        cost_b = F(count * ub, 100)
        if pb > pa and len({correct, pack_gap, unit_gap, cost_b}) == 4:
            break
    choices, answer = order((correct, money(correct)), [(v, money(v)) for v in (pack_gap, unit_gap, cost_b)])
    return problem(
        stem=f"Store A sells markers in packs of {m(a)} for {money(pa)} per pack. Store B sells the same markers in packs of {m(b)} for {money(pb)} per pack. With no tax or discounts, how much less does it cost to buy exactly {m(count)} markers at Store B than at Store A?",
        choices=choices, answer=answer,
        explanation=f"Compare the costs for the same number of markers.\n"
        f"Store A: {m(tfrac(count,a)+f'={count//a}')} packs cost {money(F(count*ua,100))}.\n"
        f"Store B: {m(tfrac(count,b)+f'={count//b}')} packs cost {money(cost_b)}.\n"
        f"Subtract the two costs to get {money(correct)}.\n"
        f"Trap: {money(pack_gap)} compares single-pack prices; {money(unit_gap)} is the savings on one marker; {money(cost_b)} is Store B's total cost.",
    )


def RAT_04(rng):
    while True:
        workers = rng.choice([8, 12, 16])
        leaving = workers // 4
        stay = workers - leaving
        first = rng.randint(2, 5)
        block = rng.randint(3, 5)
        planned = first + 3 * block
        remaining = 4 * block
        correct = first + remaining
        late_crew = F(workers * planned, stay)
        direct = first + F((planned - first) * stay, workers)
        if len({correct, remaining, late_crew, direct}) == 4:
            break
    choices, answer = order((correct, m(correct)), [(v, m(frac(v))) for v in (remaining, late_crew, direct)])
    return problem(
        stem=f"A crew of {m(workers)} workers could finish a job in {m(planned)} days. After all {m(workers)} workers work for {m(first)} days, {m(leaving)} leave. Each worker works at the same constant rate. How many days from the start will the remaining crew need to finish the job?",
        choices=choices, answer=answer,
        explanation=f"Measure the unfinished work in worker-days before dividing by the smaller crew.\n"
        f"After {m(first)} days, {m(f'{workers}({planned}-{first})={workers*(planned-first)}')} worker-days remain.\n"
        f"The remaining {m(stay)} workers need {m(tfrac(workers*(planned-first),stay)+f'={remaining}')} more days.\n"
        f"Total time: {m(f'{first}+{remaining}={correct}')} days.\n"
        f"Trap: {m(remaining)} omits the days already worked; {m(frac(late_crew))} uses the smaller crew for the entire job; {m(frac(direct))} makes time decrease when workers leave.",
    )


def RAT_05(rng):
    a = rng.choice([4, 6, 8, 10])
    b = 3 * a // 2
    correct = F(a * b, a + b)
    rate = F(1, a) + F(1, b)
    mean = F(a + b, 2)
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in (rate, mean, a+b)])
    return problem(
        stem=f"Pipe A can fill an empty tank in {m(a)} hours, and Pipe B can fill it in {m(b)} hours. Both pipes work at constant rates. How many hours will it take to fill the empty tank with both pipes open?",
        choices=choices, answer=answer,
        explanation=f"Add the filling rates, then take the reciprocal to find the time.\n"
        f"Together the pipes fill {m(tfrac(1,a)+'+'+tfrac(1,b)+'='+frac(rate))} of the tank per hour.\n"
        f"Filling time: {m('1'+r'\div'+frac(rate)+'='+frac(correct))} hours.\n"
        f"Trap: {m(frac(rate))} is the rate, not the time; {m(frac(mean))} averages the filling times; {m(a+b)} adds the filling times.",
    )


def RAT_06(rng):
    while True:
        a, b, c, d = rng.choice([(2, 3, 4, 5), (3, 4, 2, 5), (2, 5, 3, 4), (3, 5, 4, 6)])
        k = math.lcm(d-c, d-a) * rng.randint(1, 3)
        red, blue, green = a*c*k, b*c*k, b*d*k
        gap = green - red
        wrong_gap = F(gap*c, d-c)
        unaligned = F(gap*b, d-a)
        if len({blue, red, wrong_gap, unaligned}) == 4:
            break
    choices, answer = order((blue, m(blue)), [(v, m(frac(v))) for v in (red, wrong_gap, unaligned)])
    return problem(
        stem=f"In a collection of beads, the ratio of red to blue beads is {m(f'{a}:{b}')}, and the ratio of blue to green beads is {m(f'{c}:{d}')}. There are {m(gap)} more green beads than red beads. How many blue beads are in the collection?",
        choices=choices, answer=answer,
        explanation=f"Match the blue parts before combining the two ratios.\n"
        f"Red, blue, and green are in the ratio {m(f'{a*c}:{b*c}:{b*d}')}.\n"
        f"The green-minus-red difference is {m(f'{b*d}-{a*c}={b*d-a*c}')} parts, so one part is {m(tfrac(gap,b*d-a*c)+f'={k}')}.\n"
        f"Blue beads: {m(f'{b*c}'+r'\cdot'+f'{k}={blue}')}.\n"
        f"Trap: {m(red)} counts red beads; {m(frac(wrong_gap))} treats the given difference as green minus blue; {m(frac(unaligned))} combines the ratios without matching the blue parts.",
    )


def RAT_09(rng):
    seconds = rng.choice([8, 10, 12, 15])
    fps = 22 * rng.randint(2, 5)
    feet = fps * seconds
    correct = F(fps * 3600, 5280)
    minute = correct / 60
    no_division = correct * seconds
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in (fps, minute, no_division)])
    return problem(
        stem=f"A car traveling at a constant speed covers {m(feet)} feet in {m(seconds)} seconds. What is its speed in miles per hour? There are {m(5280)} feet in a mile and {m(3600)} seconds in an hour.",
        choices=choices, answer=answer,
        explanation=f"Find feet per second, then convert both distance and time units.\n"
        f"The speed is {m(tfrac(feet,seconds)+f'={fps}')} feet per second.\n"
        f"In miles per hour: {m(f'{fps}'+r'\cdot'+tfrac(3600,5280)+'='+frac(correct))}.\n"
        f"Trap: {m(fps)} keeps feet per second; {m(frac(minute))} converts to miles per minute; {m(frac(no_division))} never divides the distance by the travel time.",
    )


def RAT_10(rng):
    low = rng.choice([10, 15, 20])
    rise = rng.choice([5, 10, 15])
    fall = rng.choice([v for v in (10, 15, 20) if v != rise])
    target, high = low + rise, low + rise + fall
    volume = fall * rng.randint(1, 3)
    correct = F(volume * rise, fall)
    fixed_volume = F(volume * rise, high)
    final_volume = F(volume * rise, high-low)
    total = volume + correct
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in (fixed_volume, final_volume, total)])
    return problem(
        stem=f"A technician has {m(volume)} liters of a solution that is {m(str(low)+r'\%')} alcohol by volume. How many liters of a {m(str(high)+r'\%')} alcohol solution must be added to obtain a {m(str(target)+r'\%')} alcohol solution? Assume the volumes add.",
        choices=choices, answer=answer,
        explanation=f"The amount of alcohol in the two starting solutions must equal the amount in the final mixture.\n"
        f"Let {m('x')} be the liters added: {m(frac(F(low,100))+r'\cdot'+f'{volume}+'+frac(F(high,100))+'x='+frac(F(target,100))+f'({volume}+x)')}.\n"
        f"Multiplying by {m(100)} and collecting terms gives {m(f'{fall}x={volume*rise}')}, so {m('x='+frac(correct))} liters.\n"
        f"Trap: {m(frac(fixed_volume))} keeps the final volume at {m(volume)} liters; {m(frac(final_volume))} treats {m(volume)} as the final rather than initial volume; {m(frac(total))} is the total mixture volume.",
    )


def RAT_11(rng):
    k = rng.randint(2, 5)
    x1 = rng.randint(3, 8)
    x2 = x1 + rng.randint(2, 6)
    y1, y2 = k*x1, k*x2
    multiply = k*y2
    additive = x1+y2-y1
    inverse = F(x1*y1, y2)
    choices, answer = order((x2, m(x2)), [(v, m(frac(v))) for v in (multiply, additive, inverse)])
    return problem(
        stem=f"The variable {m('y')} varies directly with {m('x')}. When {m(f'x={x1}')}, {m(f'y={y1}')}. What is the value of {m('x')} when {m(f'y={y2}')}?",
        choices=choices, answer=answer,
        explanation=f"Direct variation means the ratio of {m('y')} to {m('x')} stays constant.\n"
        f"{m('y=kx')} and {m('k='+tfrac(y1,x1)+f'={k}')}.\n"
        f"{m(f'{y2}={k}x')}, so {m('x='+tfrac(y2,k)+f'={x2}')}.\n"
        f"Trap: {m(multiply)} multiplies by the constant instead of dividing; {m(additive)} adds the change in {m('y')} to {m('x')}; {m(frac(inverse))} uses inverse variation.",
    )


def RAT_12(rng):
    scale = rng.choice([F(3, 2), F(2)])
    x1 = scale.denominator * rng.randint(2, 5)
    y1 = scale.numerator**2 * rng.randint(2, 8)
    percent = int((scale-1)*100)
    x2 = x1 * scale
    correct = y1 / scale**2
    linear = y1 / scale
    direct = y1 * scale**2
    increase_only = y1 / (scale-1)**2
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in (linear, direct, increase_only)])
    return problem(
        stem=f"The variable {m('y')} varies inversely with the square of {m('x')}. Initially, {m(f'x={x1}')} and {m(f'y={y1}')}. If {m('x')} increases by {m(str(percent)+r'\%')}, what is the new value of {m('y')}?",
        choices=choices, answer=answer,
        explanation=f"An inverse-square relationship divides {m('y')} by the square of the factor multiplying {m('x')}.\n"
        f"The new {m('x')} is {m(frac(scale)+r'\cdot'+f'{x1}='+frac(x2))}.\n"
        f"The new {m('y')} is {m(tfrac(y1,'('+frac(scale)+')^{2}')+'='+frac(correct))}.\n"
        f"Trap: {m(frac(linear))} uses inverse variation without the square; {m(frac(direct))} uses direct-square variation; {m(frac(increase_only))} uses only the increase in {m('x')} as its new value.",
    )


def RAT_13(rng):
    while True:
        cups = F(rng.choice([3, 5, 7]), 4)
        batch = rng.choice([8, 12, 16])
        scale = rng.choice([F(3, 2), F(5, 2), F(3, 4)])
        target = int(batch * scale)
        correct = cups * scale
        reverse = cups / scale
        additive = cups + scale
        whole_numerator = cups.numerator * scale
        if len({correct, reverse, additive, whole_numerator}) == 4:
            break
    choices, answer = order((correct, m(frac(correct))), [(v, m(frac(v))) for v in (reverse, additive, whole_numerator)])
    return problem(
        stem=f"A recipe uses {m(frac(cups))} cups of flour to make {m(batch)} muffins. How many cups of flour are needed to make {m(target)} muffins using the same recipe?",
        choices=choices, answer=answer,
        explanation=f"Multiply the flour amount by the ratio of the new batch size to the original batch size.\n"
        f"The scale factor is {m(tfrac(target,batch)+'='+frac(scale))}.\n"
        f"Flour needed: {m(frac(cups)+r'\cdot'+frac(scale)+'='+frac(correct))} cups.\n"
        f"Trap: {m(frac(reverse))} reverses the scale factor; {m(frac(additive))} adds the scale factor; {m(frac(whole_numerator))} drops the flour fraction's denominator.",
    )


def RAT_14(rng):
    u, v = rng.choice([(30, 60), (40, 60), (60, 90), (20, 30)])
    distance = math.lcm(u, v) * rng.choice([1, 2])
    correct = F(2*u*v, u+v)
    mean = F(u+v, 2)
    half = correct/2
    speed_weighted = F(u*u+v*v, u+v)
    choices, answer = order((correct, m(frac(correct))), [(w, m(frac(w))) for w in (mean, half, speed_weighted)])
    return problem(
        stem=f"A driver travels {m(distance)} miles from home to a town at {m(u)} miles per hour and returns along the same route at {m(v)} miles per hour. With no stops, what is the driver's average speed, in miles per hour, for the entire trip?",
        choices=choices, answer=answer,
        explanation=f"Average speed is total distance divided by total time.\n"
        f"Travel time: {m(tfrac(distance,u)+'+'+tfrac(distance,v)+f'={distance//u+distance//v}')} hours.\n"
        f"Average speed: {m(tfrac(2*distance,distance//u+distance//v)+'='+frac(correct))} miles per hour.\n"
        f"Trap: {m(frac(mean))} averages the speeds as though the times were equal; {m(frac(half))} uses only the one-way distance; {m(frac(speed_weighted))} pairs each speed with the other leg's travel time.",
    )


def WORD_01(rng):
    rate = rng.randint(3, 8)
    fee = rate * rng.randint(2, 4)
    discount = rate * rng.randint(1, 2)
    hours = rng.randint(4, 9)
    paid = fee + rate*hours - discount
    no_coupon = F(paid-fee, rate)
    no_fee = F(paid+discount, rate)
    add_fee = F(paid+discount+fee, rate)
    choices, answer = order((hours, m(hours)), [(v, m(frac(v))) for v in (no_coupon, no_fee, add_fee)])
    return problem(
        stem=f"A bicycle rental costs a fixed fee of {money(fee)} plus {money(rate)} per hour. A coupon reduces the total bill by {money(discount)}. If Jordan pays {money(paid)} after using the coupon, with no other charges, for how many hours did Jordan rent the bicycle?",
        choices=choices, answer=answer,
        explanation=f"The bill is the fixed fee plus the hourly charge, minus the coupon.\n"
        f"Let {m('h')} be the number of hours: {m(f'{fee}+{rate}h-{discount}={paid}')}.\n"
        f"{m(f'{rate}h={paid}+{discount}-{fee}={rate*hours}')}, so {m(f'h={hours}')}.\n"
        f"Trap: {m(frac(no_coupon))} ignores the coupon; {m(frac(no_fee))} ignores the fixed fee; {m(frac(add_fee))} adds the fee when undoing the bill.",
    )


def WORD_02(rng):
    while True:
        step = rng.randint(3, 5)
        adult_price, student_price = 3*step, 2*step
        adults = 3*rng.randint(4, 9)
        students = 3*rng.randint(5, 12)
        count = adults+students
        revenue = adult_price*adults + student_price*students
        all_adults = F(revenue, adult_price)
        full_price = F(revenue-student_price*count, adult_price)
        if len({adults, students, all_adults, full_price}) == 4:
            break
    choices, answer = order((adults, m(adults)), [(v, m(frac(v))) for v in (students, all_adults, full_price)])
    return problem(
        stem=f"Tickets to a play cost {money(adult_price)} for adults and {money(student_price)} for students. A total of {m(count)} tickets were sold for {money(revenue)}. How many adult tickets were sold?",
        choices=choices, answer=answer,
        explanation=f"Use both the total ticket count and the total sales amount.\n"
        f"If {m('a')} adult tickets were sold, then {m(f'{count}-a')} student tickets were sold.\n"
        f"{m(f'{adult_price}a+{student_price}({count}-a)={revenue}')}.\n"
        f"{m(f'{step}a={revenue-student_price*count}')}, so {m(f'a={adults}')}.\n"
        f"Trap: {m(students)} counts student tickets; {m(frac(all_adults))} treats every ticket as an adult ticket; {m(frac(full_price))} divides the extra revenue by the adult price instead of the price difference.",
    )


def WORD_04(rng):
    while True:
        n1 = rng.choice([20, 30, 40])
        n2 = n1*rng.choice([3, 4])
        n3 = n2+n1
        rate = rng.randint(2, 5)
        fee = n1*rng.randint(1, 3)
        c1, c2 = fee+rate*n1, fee+rate*n2
        correct = fee+rate*n3
        proportional = F(c1*n3, n1)
        no_fee = rate*n3
        same_increment = c2+(c2-c1)
        if len({correct, proportional, no_fee, same_increment}) == 4:
            break
    choices, answer = order((correct, money(correct)), [(v, money(v)) for v in (proportional, no_fee, same_increment)])
    return problem(
        stem=f"A shop charges a fixed setup fee plus a constant price per badge. An order of {m(n1)} badges costs {money(c1)}, and an order of {m(n2)} badges costs {money(c2)}. What would an order of {m(n3)} badges cost under the same pricing model?",
        choices=choices, answer=answer,
        explanation=f"Find the price per additional badge from the change in cost, then find the setup fee.\n"
        f"Price per badge: {m(tfrac(f'{c2}-{c1}',f'{n2}-{n1}')+f'={rate}')} dollars.\n"
        f"Setup fee: {m(f'{c1}-{rate}'+r'\cdot'+f'{n1}={fee}')} dollars.\n"
        f"The new order costs {m(f'{fee}+{rate}'+r'\cdot'+f'{n3}={correct}')} dollars.\n"
        f"Trap: {money(proportional)} scales the setup fee along with the order; {money(no_fee)} omits the setup fee; {money(same_increment)} repeats the earlier cost increase even though the quantity increase is different.",
    )


def WORD_05(rng):
    first = rng.randint(4, 25)
    total = 3*first+3
    correct = first+2
    middle = first+1
    too_far = first+3
    choices, answer = order((correct, m(correct)), [(v, m(v)) for v in (first, middle, too_far)])
    return problem(
        stem=f"The sum of three consecutive integers is {m(total)}. What is the greatest of these integers?",
        choices=choices, answer=answer,
        explanation=f"For three consecutive integers, the middle integer equals one-third of the sum.\n"
        f"The middle integer is {m(tfrac(total,3)+f'={middle}')}.\n"
        f"The greatest integer is {m(f'{middle}+1={correct}')}.\n"
        f"Trap: {m(first)} is the smallest integer; {m(middle)} is the middle integer; {m(too_far)} treats the average as the first integer and adds two.",
    )


def WORD_06(rng):
    ratio = rng.choice([4, 5])
    younger = rng.randint(7, 12)
    years = (ratio-2)*younger
    older = ratio*younger
    future = younger+years
    no_older_aging = 2*younger
    choices, answer = order((younger, m(younger)), [(v, m(v)) for v in (older, future, no_older_aging)])
    return problem(
        stem=f"Nora is currently {m(ratio)} times as old as Eli. In {m(years)} years, Nora will be twice as old as Eli. How old is Eli now, in years?",
        choices=choices, answer=answer,
        explanation=f"Add the same number of years to both current ages before using the future relationship.\n"
        f"If Eli is {m('x')} years old now, then Nora is {m(f'{ratio}x')}.\n"
        f"{m(f'{ratio}x+{years}=2(x+{years})')}, so {m(f'{ratio-2}x={years}')} and {m(f'x={younger}')}.\n"
        f"Trap: {m(no_older_aging)} increases only Eli's age in the future equation; {m(future)} is Eli's future age; {m(older)} is Nora's current age.",
    )


def WORD_07(rng):
    rate = rng.choice([225, 275, 350, 450])
    fee = rate*rng.randint(2, 4)
    count = rng.randint(8, 16)
    remainder = 25*rng.randint(1, (rate-1)//25)
    budget = fee+rate*count+remainder
    round_up = count+1
    no_fee = budget//rate
    add_fee = (budget+fee)//rate
    choices, answer = order((count, m(count)), [(v, m(v)) for v in (round_up, no_fee, add_fee)])
    return problem(
        stem=f"A print shop charges a setup fee of {money(F(fee,100))} plus {money(F(rate,100))} per poster. A club can spend at most {money(F(budget,100))}, with no other charges. What is the greatest number of posters the club can order?",
        choices=choices, answer=answer,
        explanation=f"Subtract the fixed fee, divide by the price per poster, and round down to a whole number.\n"
        f"For {m('n')} posters, {m(num(fee/100)+'+'+num(rate/100)+r'n\le'+num(budget/100))}.\n"
        f"Thus {m('n'+r'\le'+tfrac(num((budget-fee)/100),num(rate/100))+'='+frac(F(budget-fee,rate)))}.\n"
        f"The greatest whole number allowed is {m(count)}.\n"
        f"Trap: {m(round_up)} rounds up past the budget; {m(no_fee)} ignores the setup fee; {m(add_fee)} adds the setup fee to the available budget.",
    )


def WORD_09(rng):
    factor = rng.choice([2, 3])
    extra = (factor+1)*rng.randint(2, 3)
    width = rng.randint(6, 12)
    length = factor*width+extra
    perimeter = 2*(length+width)
    single_pair = F(perimeter-extra, factor+1)
    wrong_sign = F(F(perimeter,2)+extra, factor+1)
    no_extra = F(perimeter, 2*(factor+1))
    choices, answer = order((width, m(width)), [(v, m(frac(v))) for v in (single_pair, wrong_sign, no_extra)])
    return problem(
        stem=f"The length of a rectangular garden is {m(extra)} meters more than {m(factor)} times its width. The perimeter is {m(perimeter)} meters. What is the width, in meters?",
        choices=choices, answer=answer,
        explanation=f"The perimeter contains two lengths and two widths.\n"
        f"Let the width be {m('w')}; the length is {m(f'{factor}w+{extra}')}.\n"
        f"{m(f'2(w+{factor}w+{extra})={perimeter}')}, so {m(f'{factor+1}w+{extra}={perimeter//2}')}.\n"
        f"{m('w='+tfrac(f'{perimeter//2}-{extra}',factor+1)+f'={width}')} meters.\n"
        f"Trap: {m(frac(single_pair))} uses only one length and one width; {m(frac(wrong_sign))} adds instead of subtracting the extra length; {m(frac(no_extra))} ignores the extra length.",
    )


def WORD_10(rng):
    while True:
        first = rng.choice([F(1,5), F(1,4), F(2,5)])
        second = rng.choice([F(1,3), F(1,4), F(1,2)])
        retained = (1-first)*(1-second)
        additive_retained = 1-first-second
        remainder = math.lcm(retained.numerator, additive_retained.numerator)*rng.randint(5,10)
        gift = retained.numerator*rng.randint(5,15)
        balance = remainder+gift
        correct = remainder/retained
        additive = remainder/additive_retained
        ignore_gift = balance/retained
        late_subtract = balance/retained-gift
        if len({correct, additive, ignore_gift, late_subtract}) == 4:
            break
    percent = int(first*100)
    choices, answer = order((correct, money(correct)), [(v, money(v)) for v in (additive, ignore_gift, late_subtract)])
    return problem(
        stem=f"Lena spends {m(str(percent)+r'\%')} of her savings on a jacket, then spends {m(frac(second))} of the remaining money on shoes. She then adds a gift of {money(gift)} to her savings and has {money(balance)}. How much did she have before buying the jacket?",
        choices=choices, answer=answer,
        explanation=f"Undo the gift first, then divide by the fractions left after each purchase.\n"
        f"Before the gift, Lena had {m(f'{balance}-{gift}={remainder}')} dollars.\n"
        f"The purchases left {m('('+frac(1-first)+')('+frac(1-second)+')='+frac(retained))} of the original savings.\n"
        f"Original savings: {m(f'{remainder}'+r'\div'+frac(retained)+'='+frac(correct))} dollars.\n"
        f"Trap: {money(additive)} subtracts both spending fractions from the original whole; {money(ignore_gift)} ignores the gift; {money(late_subtract)} subtracts the gift after reversing the purchases.",
    )


def WORD_11(rng):
    initial = rng.randint(18, 40)
    rate = rng.randint(2, 6)
    minutes = rng.randint(4, 8)
    added = rate*minutes
    correct = (initial, added)
    wrong = [(initial, initial+added), (rate, initial*minutes), (rate, added)]

    def label(values):
        start, change = values
        return f"Initially {m(start)} gallons; {m(change)} gallons added."

    choices, answer = order((correct, label(correct)), [(v, label(v)) for v in wrong], key=lambda item: item[0])
    return problem(
        stem=f"As a tank fills, the amount of water is modeled by {m(f'W={initial}+{rate}t')}, where {m('W')} is measured in gallons and {m('t')} is the number of minutes since filling began. Which statement gives the initial amount of water and the amount added during the first {m(minutes)} minutes?",
        choices=choices, answer=answer,
        explanation=f"The constant term is the initial amount, and the coefficient of time is the filling rate.\n"
        f"At {m('t=0')}, {m(f'W={initial}')} gallons.\n"
        f"The amount added is {m(f'{rate}'+r'\cdot'+f'{minutes}={added}')} gallons.\n"
        f"Trap: {m(initial+added)} is the total water after filling; using {m(rate)} as the initial amount confuses the slope with the intercept; pairing that with {m(initial*minutes)} gallons added swaps both meanings.",
    )


def WORD_12(rng):
    while True:
        price = rng.choice([25, 30, 35, 40, 45])
        variable = rng.choice([10, 15, 20])
        margin = price-variable
        if margin < 6:
            continue
        below = rng.randint(15, 30)
        fixed = margin*below+rng.randint(1,margin-1)
        correct = math.ceil(F(fixed,margin))
        ignore_variable = math.ceil(F(fixed,price))
        add_variable = math.ceil(F(fixed,price+variable))
        if len({correct, below, ignore_variable, add_variable}) == 4:
            break
    choices, answer = order((correct, m(correct)), [(v, m(v)) for v in (below, ignore_variable, add_variable)])
    return problem(
        stem=f"For {m('x')} mugs produced and sold, a company has revenue {m(f'R(x)={price}x')} dollars and total cost {m(f'C(x)={fixed}+{variable}x')} dollars. What is the least whole number of mugs the company must sell for revenue to be at least total cost?",
        choices=choices, answer=answer,
        explanation=f"Revenue must cover both the fixed cost and the cost of each mug.\n"
        f"{m(f'{price}x'+r'\ge'+f'{fixed}+{variable}x')}, so {m(f'{margin}x'+r'\ge'+f'{fixed}')}.\n"
        f"{m('x'+r'\ge'+frac(F(fixed,margin)))}, so at least {m(correct)} mugs must be sold.\n"
        f"Trap: {m(below)} rounds down and leaves a loss; {m(ignore_variable)} ignores the per-mug cost; {m(add_variable)} adds that cost to the revenue per mug instead of subtracting it.",
    )
