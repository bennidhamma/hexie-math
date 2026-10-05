"""
Makes figure images with Codex image generation, one Codex session per batch, in parallel.
Usage: python3 gen_figures.py [ID ...]   (no IDs: every figure problem that has no image yet)
Each image lands in figures/<ID>.png. Review every image before building the bank.
"""
import json, os, subprocess, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = (
    "Style: an ACT math test figure. Clean black line art on a pure white background. Thin even strokes. "
    "Labels in a plain sans-serif font, italic capital letters for points. No color, no shading unless the "
    "description asks for shading (then use light gray hatching or light gray fill). No title, no caption, "
    "no 'not drawn to scale' note, no answer, and no text other than the labels in the description. "
    "Landscape 3:2 image with a generous white margin. Every label must appear exactly once, spelled exactly as given, "
    "placed next to the thing it labels and not touching any line."
)

def problems():
    out = []
    for n in range(1, 7):
        for d in ("reviewed", "drafts"):
            path = os.path.join(HERE, d, f"batch{n}.json")
            if os.path.exists(path):
                out += [(n, p) for p in json.load(open(path)) if p.get("figure")]
                break
    return out

def main():
    want = set(sys.argv[1:])
    todo = [(n, p) for n, p in problems()
            if (p["id"] in want) or (not want and not os.path.exists(os.path.join(HERE, "figures", p["id"] + ".png")))]
    by_batch = {}
    for n, p in todo:
        by_batch.setdefault(n, []).append(p)
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    procs = []
    for n, ps in by_batch.items():
        jobs = "\n\n".join(f"### {p['id']}\nSave as: figures/{p['id']}.png\nFigure: {p['figure']['description']}" for p in ps)
        prompt = (
            "Use your image generation tool to make the figures below, one image per figure. "
            "After each image is generated, copy the PNG from where the tool saved it to the path given. "
            "Make each image separately; do not combine figures.\n\n" + STYLE + "\n\n" + jobs +
            "\n\nWhen done, list each saved path."
        )
        log = open(os.path.join(HERE, "logs", f"figures{n}.log"), "w")
        procs.append(subprocess.Popen(
            ["codex", "exec", "-s", "workspace-write", "--skip-git-repo-check", prompt],
            cwd=HERE, stdout=log, stderr=subprocess.STDOUT))
        print(f"batch{n}: {len(ps)} figures")
    for pr in procs:
        pr.wait()
    print("missing:", [p["id"] for _, p in todo if not os.path.exists(os.path.join(HERE, "figures", p["id"] + ".png"))])

if __name__ == "__main__":
    main()
