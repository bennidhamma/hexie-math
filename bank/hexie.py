"""
Helpers for problem templates. A template is a Python function

    def make(rng):  # rng is a random.Random
        ...
        return problem(stem=..., choices=[...], answer=..., explanation=...)

The build script (build_bank.py) calls make() with several seeds and keeps the variations that pass its checks.
All math text uses the app's LaTeX subset (see AUTHORING.md). These helpers write that LaTeX for you.
"""
from fractions import Fraction as F
import math


def m(tex):
    """Inline math: m("x^{2}") -> "\\(x^{2}\\)"."""
    return "\\(" + str(tex) + "\\)"


def frac(x):
    """LaTeX for a Fraction (or int) in lowest terms: 3/4 -> \\frac{3}{4}, -1/2 -> -\\frac{1}{2}, 5 -> 5."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = "-" if x < 0 else ""
    return f"{sign}\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def tfrac(n, d):
    """An unreduced fraction, for showing work: tfrac(6, 16) -> \\frac{6}{16}."""
    return f"\\frac{{{n}}}{{{d}}}"


def num(x, places=2):
    """A decimal with trailing zeros removed: num(2.50) -> 2.5, num(3.0) -> 3."""
    s = f"{x:.{places}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def money(x):
    """$12.50 style text (outside math)."""
    return f"${x:,.2f}"


def simplify_root(n):
    """sqrt(n) = a*sqrt(b). Returns (a, b)."""
    a, b, f = 1, n, 2
    while f * f <= b:
        while b % (f * f) == 0:
            b //= f * f
            a *= f
        f += 1
    return a, b


def root(n, coef=1):
    """LaTeX for coef*sqrt(n), simplified: root(72) -> 6\\sqrt{2}, root(16) -> 4."""
    a, b = simplify_root(n)
    a *= coef
    if b == 1:
        return str(a)
    return ("" if a == 1 else str(a)) + f"\\sqrt{{{b}}}"


def poly(coefs, var="x"):
    """LaTeX for a polynomial from highest power down: poly([2, -3, 0, 5]) -> 2x^{3} - 3x^{2} + 5."""
    deg = len(coefs) - 1
    parts = []
    for i, c in enumerate(coefs):
        p = deg - i
        c = F(c)
        if c == 0:
            continue
        mag = abs(c)
        body = "" if (mag == 1 and p > 0) else frac(mag)
        if p >= 1:
            body += var + (f"^{{{p}}}" if p > 1 else "")
        sign = "-" if c < 0 else "+"
        parts.append((sign, body))
    if not parts:
        return "0"
    first_sign, first = parts[0]
    out = ("-" if first_sign == "-" else "") + first
    for sign, body in parts[1:]:
        out += f" {sign} {body}"
    return out


def signed(x):
    """'+ 3' or '- 3', for building expressions."""
    x = F(x)
    return f"- {frac(-x)}" if x < 0 else f"+ {frac(x)}"


def paren(x):
    """A number wrapped in parentheses when negative, for substitution: paren(-3) -> (-3)."""
    s = frac(x)
    return f"({s})" if F(x) < 0 else s


def problem(stem, choices, answer, explanation, table=None):
    """Return a problem dict. choices: 4 strings. answer: index of the correct one."""
    return {"stem": stem, "choices": list(choices), "answer": answer, "explanation": explanation, "table": table}


def order(correct, wrong, key=None):
    """
    Put the correct choice and 3 wrong ones in ascending order (ACT style).
    correct / wrong items are (value, text) pairs. Returns (choice_texts, answer_index).
    Raises ValueError if two choices have the same text.
    """
    items = [correct] + list(wrong)
    if len({t for _, t in items}) != 4:
        raise ValueError("choices are not distinct")
    items_sorted = sorted(items, key=key or (lambda vt: float(vt[0])))
    texts = [t for _, t in items_sorted]
    return texts, texts.index(correct[1])
