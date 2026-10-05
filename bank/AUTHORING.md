# Authoring brief: Hexie Math problem bank

You write ACT-style math problems for a 16-year-old who scored 25 on the math section of a practice ACT (easy 12/15, medium 9/15, hard 7/15). Most misses were medium and hard problems. The weakest areas were probability, proportional reasoning, exponents and roots, logarithms, the unit circle, and the law of sines and cosines.

The problems appear in an Android app, one at a time, on a phone screen. A friendly witch mascot named Hexie hosts the app, but the problems themselves must read like real ACT problems. Do not use witch themes in the problems.

## What makes a good problem here

- It matches the real ACT in style, length, and difficulty. Medium problems take 2 or 3 steps. Hard problems combine two ideas, hide the key fact in the wording or the figure, or need a non-obvious first step.
- It has exactly 4 answer choices (the current ACT math section uses 4). Exactly one choice is correct.
- Each wrong choice comes from a specific, common mistake (wrong order of operations, forgetting to square the scale factor, using the wrong side in the law of sines, and so on). No silly or random distractors.
- Choices are in a logical order: numbers ascending, or expressions in a sensible order.
- The wording is short, clear, and unambiguous. One reading only. State units. State "Note: Figure not drawn to scale." when that applies.
- Numbers work out cleanly by hand or with a basic calculator, like on the ACT.
- Every problem is original. Do not copy published ACT problems.

## The explanation

Write it for the student who just got it wrong. Keep it short:

1. One sentence that names the key idea.
2. The steps, one per line, with the math.
3. One line that names the trap: which wrong choice comes from which mistake.

Use plain, friendly, direct language. No filler.

## Math formatting

Put inline math between `\(` and `\)`. The app has its own small LaTeX renderer, so use ONLY these commands:

`\frac{a}{b}`, `x^{2}`, `x_{1}`, `\sqrt{x}`, `\sqrt[3]{x}`, `\left( \right)`, `\left[ \right]`, `\left| \right|`, `\overline{AB}`, `\pi`, `\theta`, `\alpha`, `\beta`, `\cdot`, `\times`, `\div`, `\pm`, `\le`, `\ge`, `\ne`, `\approx`, `\angle`, `\triangle`, `^{\circ}` for degrees, `\sin`, `\cos`, `\tan`, `\log`, `\ln`, `\text{...}`, `\infty`, `\%`, `\{ \}`, `\ldots`.

Rules:
- Every piece of math goes inside `\( \)`, including single variables like `\(x\)`.
- Do not use `$` for math. A literal dollar sign in a price is fine outside math: `$4.50`.
- No display math, no `\begin{...}`, no matrices, no `\dfrac` inside exponents.
- Write degrees as `\(40^{\circ}\)`. Write percent inside math as `\(25\%\)`, or outside math as `25%`.
- A choice that is pure math is one math piece: `"\\(\\frac{3}{8}\\)"`.

## Figures

About 30% of the slots ask for a figure, like the real ACT. When a slot says `figure: true`, the problem must actually need the figure or be much clearer with it (geometry, graphs, charts, a spinner, a Venn diagram).

Write `figure.description` as a precise drawing spec for an illustrator who knows no math. It becomes the prompt for an image model. Include:
- Every point, line, and shape, and where it sits (left, right, top).
- Every label, exactly as it must appear, and what it is attached to. Put a side length next to the middle of that side.
- Right-angle marks, tick marks for equal sides, arrows for parallel lines, dashed lines.
- For graphs: axis labels, the visible range, grid or no grid, and the exact points, lines, or curves with their key coordinates.
- Style: "black line art on white, ACT test style, sans-serif labels". Say "no other text" so the illustrator adds nothing.
- Never put the answer, or any value the student must find, in the figure.

Also write `figure.alt`: one sentence describing the figure.

Data tables are not figures. Put a table in the `table` field. The app draws it.

## Output

Write a JSON array to the output file named in your task. Each element:

```json
{
  "id": "PROB-03",
  "topic": "PROBABILITY",
  "difficulty": "hard",
  "skill": "conditional probability from a two-way table",
  "stem": "Text with \\(math\\).",
  "table": null,
  "figure": null,
  "choices": ["\\(\\frac{3}{8}\\)", "...", "...", "..."],
  "answer": 2,
  "explanation": "Text with \\(math\\). Use \\n for new lines.",
  "check": "One line of Python that prints the correct value, for a quick cross-check. Example: from fractions import Fraction as F; print(F(6,16)*F(5,15))"
}
```

- `table`, when used: `{"caption": "...", "headers": ["...", "..."], "rows": [["...", "..."], ...]}`. Cells may contain `\( \)` math.
- `figure`, when used: `{"description": "...", "alt": "...", "notToScale": true}`.
- `answer` is the 0-based index of the correct choice.
- The file must be valid JSON. Escape backslashes (`\\frac`) and use `\n` for line breaks.

## Templates for problems without a figure

Every slot with `figure: false` also needs a template, so the app can show new versions of the problem with different numbers. Write the templates in the Python file named in your task. One function per problem, named after the id with `-` replaced by `_`:

```python
from hexie import *   # m, frac, tfrac, num, money, root, poly, signed, paren, problem, order, F, math

def PROB_03(rng):
    a = rng.randint(3, 9)
    ...
    choices, answer = order((value, m(frac(value))), [(w1, m(frac(w1))), (w2, ...), (w3, ...)])
    return problem(stem=..., choices=choices, answer=answer, explanation=..., table=None)
```

Rules for templates:
- Read `hexie.py` first. Use its helpers to write the LaTeX.
- Pick numbers with `rng` so the answer stays clean (whole numbers or simple fractions) and the difficulty stays the same as the authored version.
- Compute the correct answer AND each wrong choice from the same mistake as in the authored version. Never hard-code a choice.
- If a random draw makes two choices equal or makes the problem degenerate, draw again (loop) instead of returning a bad problem.
- The explanation must use the new numbers.
- Keep the same wording as the authored problem, with only the numbers and maybe names changed.
- The JSON entry gets `"template": "PROB_03"`. Figure problems get `"template": null`.

Test your file before you finish: import it and call every function with 20 different seeds. Each call must return 4 distinct choices with a valid answer index.

Before you finish, solve every problem yourself a second time, from the stem only, and confirm that exactly one choice is correct. Fix anything that fails.
