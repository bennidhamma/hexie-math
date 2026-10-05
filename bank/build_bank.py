"""
Builds app/src/main/assets/bank.json from the reviewed drafts.

For each problem:
- version #0 is the authored problem;
- problems with a template get up to VARIANTS more versions with new numbers.

Every version must have 4 distinct choices and a valid answer index, or the build fails.
Problems listed in rejected.json are left out. Figure files come from figures/<ID>.png.

Run from the bank/ directory:  python3 build_bank.py
"""
import importlib, json, os, random, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
VARIANTS = 6
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "app", "src", "main", "assets")


def load_drafts():
    problems = []
    for n in range(1, 7):
        path = os.path.join(HERE, "reviewed", f"batch{n}.json")
        if not os.path.exists(path):
            path = os.path.join(HERE, "drafts", f"batch{n}.json")
        if os.path.exists(path):
            for p in json.load(open(path)):
                p["_batch"] = n
                problems.append(p)
    return problems


def check(v, where):
    ch = v["choices"]
    assert isinstance(ch, list) and len(ch) == 4, f"{where}: needs 4 choices"
    assert len(set(ch)) == 4, f"{where}: choices not distinct: {ch}"
    assert 0 <= v["answer"] <= 3, f"{where}: bad answer index"
    for key in ("stem", "explanation"):
        assert isinstance(v[key], str) and v[key].strip(), f"{where}: empty {key}"
        assert v[key].count("\\(") == v[key].count("\\)"), f"{where}: unbalanced math in {key}"
        assert "$$" not in v[key], f"{where}: display math in {key}"


NOTE = re.compile(r"\s*Note: Figure not drawn to scale\.?\s*", re.I)


def crop_figure(src, dst, pad=36):
    """Copy a figure PNG, cropped to its drawing plus a small white margin, so it fills the phone width."""
    from PIL import Image, ImageChops
    im = Image.open(src).convert("RGB")
    box = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
    if box:
        l, t, r, b = box
        im = im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))
    im.save(dst, optimize=True)


def main():
    rejected = set(json.load(open(os.path.join(HERE, "rejected.json")))) if os.path.exists(os.path.join(HERE, "rejected.json")) else set()
    out, errors, figures = [], [], []
    modules = {}
    for p in load_drafts():
        pid = p["id"]
        if pid in rejected:
            continue
        base = {"topic": p["topic"], "difficulty": p["difficulty"], "skill": p.get("skill", "")}
        fig = None
        if p.get("figure"):
            f = p["figure"]
            src = os.path.join(HERE, "figures", f"{pid}.png")
            if not os.path.exists(src):
                errors.append(f"{pid}: missing figure file figures/{pid}.png")
                continue
            fig = {"file": f"figures/{pid}.png", "alt": f.get("alt", ""), "notToScale": bool(f.get("notToScale"))}
            figures.append(src)
        # The app prints the "not drawn to scale" note under the figure, so drop it from the text.
        stem = NOTE.sub(" ", p["stem"]).strip() if fig else p["stem"]
        v0 = {"id": f"{pid}#0", **base, "stem": stem, "table": p.get("table"), "figure": fig,
              "choices": p["choices"], "answer": p["answer"], "explanation": p["explanation"]}
        try:
            check(v0, pid)
        except AssertionError as e:
            errors.append(str(e)); continue
        out.append(v0)

        name = p.get("template")
        if not name or fig:
            continue
        n = p["_batch"]
        if n not in modules:
            try:
                modules[n] = importlib.import_module(f"templates.batch{n}")
            except Exception as e:
                errors.append(f"templates/batch{n}.py: {e}"); modules[n] = None
        mod = modules[n]
        fn = getattr(mod, name, None) if mod else None
        if fn is None:
            errors.append(f"{pid}: template {name} not found"); continue
        seen = {tuple(v0["choices"])}
        k, seed = 0, 0
        while k < VARIANTS and seed < VARIANTS * 5:
            seed += 1
            try:
                v = fn(random.Random(1000 * seed + 7))
                vv = {"id": f"{pid}#{k + 1}", **base, "stem": v["stem"], "table": v.get("table"), "figure": None,
                      "choices": v["choices"], "answer": v["answer"], "explanation": v["explanation"]}
                check(vv, f"{pid} seed {seed}")
            except Exception as e:
                errors.append(f"{pid} seed {seed}: {e}"); continue
            if tuple(vv["choices"]) in seen:
                continue  # same numbers as a version we already have
            seen.add(tuple(vv["choices"]))
            out.append(vv); k += 1

    if errors:
        print("ERRORS:"); print("\n".join(errors[:60]))
    os.makedirs(os.path.join(ASSETS, "figures"), exist_ok=True)
    for f in figures:
        crop_figure(f, os.path.join(ASSETS, "figures", os.path.basename(f)))
    json.dump(out, open(os.path.join(ASSETS, "bank.json"), "w"), ensure_ascii=False, indent=0)
    fams = {o["id"].split("#")[0] for o in out}
    print(f"{len(out)} versions from {len(fams)} problems, {len(figures)} figures, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
