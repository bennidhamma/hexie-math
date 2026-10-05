EXP-01: FIXED - Template EXP_01 could draw q = 1 and print "y^{1}" in the stem (seeds 13 and 15). The loop now requires q > 1. The authored problem is correct.
EXP-02: OK
EXP-03: OK
EXP-04: OK
EXP-05: FIXED - Template EXP_05 could make a distractor that reduces to a whole-number fraction, for example 4(sqrt3+1)/4 (seed 1). The loop now redraws when n is a multiple of d+c^2 or d. The authored problem is correct.
EXP-06: OK
EXP-07: OK
EXP-08: OK
EXP-09: OK
EXP-10: OK
REW-01: FIXED - Template REW_01 could draw a, b, c with a common factor, for example P=(2x+2y)/2 (seed 2). Then the formula is trivial and every choice is unreduced. The loop now requires gcd(a, b, c) = 1. The authored problem is correct.
REW-02: FIXED - Template REW_02 could draw a, b, c, d with a common factor, which gives a reducible function and an unreduced key. The loop now requires gcd(a, b, c, d) = 1. The authored problem is correct.
REW-03: OK
REW-04: OK
REW-05: OK
REW-06: OK
REW-07: OK
REW-08: OK
LOG-01: OK
LOG-02: OK
LOG-03: OK
LOG-04: OK
LOG-05: OK
LOG-06: OK
