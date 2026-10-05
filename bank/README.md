# Problem bank

This folder builds the app's main question set: ACT-style medium and hard problems, checked by independent solvers, with hand-built SVG figures and number variations.

## Pipeline

1. **Slots.** `slots.py` lists 150 problem slots (topic, difficulty, skill, figure or not) and writes `slots/batchN.json`. About 27% of slots have a figure, close to the share on a real ACT.
2. **Writing.** gpt-6-astra wrote the problems through Codex, following `AUTHORING.md`. Output: `drafts/batchN.json`, plus a Python template for each problem without a figure in `templates/batchN.py`. Batch 6's text problems come from Astra's templates. Claude wrote batch 6's figure problems after Codex hit its usage limit.
3. **Checking.** Claude agents solved every problem from the stem alone, checked 4 template versions each, and fixed or rejected problems. Output: `reviewed/batchN.json` and the notes in `reviews/batchN.md`.
4. **Figures.** Each figure is a short Python script in `figures_src/` that uses `svgfig.py` (and `figures_src/_plotkit.py` for graphs and charts). It writes `figures/<ID>.svg` and `.png`. Geometry and data are drawn true to the numbers.
5. **Build.** `build_bank.py` runs every template for up to 6 more versions, checks each version (4 distinct choices, a valid answer, balanced math), crops the figures, and writes `app/src/main/assets/bank.json` and `app/src/main/assets/figures/`.

The app's unit test `TexTest.bankParses` parses every equation in `bank.json` with the app's own LaTeX parser.

## Commands

```sh
cd bank
python3 -m venv .venv && .venv/bin/pip install cairosvg pillow   # once
.venv/bin/python figures_src/AREA-01.py                           # redraw one figure
.venv/bin/python build_bank.py                                    # rebuild the app's bank
python3 review_page.py                                            # astra-problems.html, for reading the bank
```

## Adding a problem

1. Add it to a `reviewed/batchN.json` file with a new id.
2. For a text problem, add a template function to `templates/batchN.py` and set `"template"` to its name.
3. For a figure problem, add `figures_src/<ID>.py` and render it.
4. Run `build_bank.py`, then the app's unit tests.
