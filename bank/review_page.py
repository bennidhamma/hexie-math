"""Writes astra-problems.html: every reviewed problem, typeset, with its figure when one exists."""
import json, html, os, re

notes = {}
probs = []
for n in range(1, 7):
    rv = f"reviews/batch{n}.md"
    if os.path.exists(rv):
        for line in open(rv):
            m = re.match(r"^\W*([A-Z]+-\d+)\W*:?\s*(.*)$", line.strip())
            if m:
                notes[m.group(1)] = m.group(2)
    for d in ("reviewed", "drafts"):
        p = f"{d}/batch{n}.json"
        if os.path.exists(p):
            probs += json.load(open(p))
            break

def esc(s): return html.escape(s).replace("\n", "<br>")

out = ['''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Astra Problem Bank</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{delimiters:[{left:'\\\\(',right:'\\\\)',display:false}]})"></script>
<style>
:root{--bg:#fff8ee;--card:#fff;--ink:#2b2232;--muted:#6a5e75;--accent:#7b4fa0;--ok:#3e9b4f;--fix:#d9652b}
body{background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif;margin:0;padding:16px}
main{max-width:860px;margin:auto} h1{margin:.2em 0} .card{background:var(--card);border-radius:14px;padding:16px 18px;margin:14px 0;box-shadow:0 1px 3px #0002}
.tag{font-size:12px;font-weight:700;letter-spacing:.06em;color:var(--accent)} .hard{color:#b03050}
ol{padding-left:1.4em} li.right{color:var(--ok);font-weight:600} .exp{background:#eef7ea;border-radius:10px;padding:10px 12px;margin-top:8px}
.fig img{max-width:100%;border:1px solid #ddd;border-radius:10px} .figspec{font-size:13px;color:var(--muted)}
.nts{font-size:13px;font-style:italic;color:var(--muted)} .note{font-size:13px;color:var(--muted)} .note.fixed{color:var(--fix)}
table{border-collapse:collapse;margin:8px 0} td,th{border:1px solid #ccc;padding:4px 10px}
details summary{cursor:pointer;color:var(--accent)} nav a{margin-right:10px} .only{margin:8px 0}
</style></head><body><main>
<h1>Astra's problem bank</h1>
<p>Problems written by gpt-6-astra and checked by Claude. Figures are hand-built SVG. Correct choices are green. Open "Explanation" for the worked steps.</p>
<label class="only"><input type="checkbox" id="figonly" onchange="document.querySelectorAll('.card').forEach(c=>c.style.display=(this.checked&&!c.dataset.fig)?'none':'')"> Show only problems with figures</label>''']
topics = []
for p in probs:
    if p["topic"] not in topics:
        topics.append(p["topic"])
out.append("<nav>" + "".join(f'<a href="#{t}">{t.replace("_", " ").title()}</a>' for t in topics) + "</nav>")
cur = None
for p in probs:
    if p["topic"] != cur:
        cur = p["topic"]
        out.append(f'<h2 id="{cur}">{cur.replace("_", " ").title()}</h2>')
    fig = p.get("figure")
    out.append(f'<div class="card"{" data-fig=1" if fig else ""}>')
    out.append(f'<div class="tag {"hard" if p["difficulty"] == "hard" else ""}">{p["id"]} · {p["difficulty"].upper()} · {html.escape(p.get("skill", ""))}{" · has variations" if p.get("template") else ""}</div>')
    out.append(f"<p>{esc(p['stem'])}</p>")
    t = p.get("table")
    if t:
        out.append("<table>" + f"<caption>{esc(t.get('caption') or '')}</caption><tr>" + "".join(f"<th>{esc(h)}</th>" for h in t["headers"]) + "</tr>" + "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in t["rows"]) + "</table>")
    if fig:
        png = f"figures/{p['id']}.png"
        if os.path.exists(png):
            out.append(f'<div class="fig"><img src="{png}" alt="{html.escape(fig.get("alt", ""))}">')
            if fig.get("notToScale"):
                out.append('<div class="nts">Note: Figure not drawn to scale.</div>')
            out.append(f'<details><summary class="figspec">Drawing spec</summary><div class="figspec">{esc(fig["description"])}</div></details></div>')
        else:
            out.append(f'<div class="figspec"><b>Figure not drawn yet:</b> {esc(fig["description"])}</div>')
    out.append('<ol type="A">' + "".join(f'<li class="{"right" if i == p["answer"] else ""}">{esc(c)}</li>' for i, c in enumerate(p["choices"])) + "</ol>")
    out.append(f'<details><summary>Explanation</summary><div class="exp">{esc(p["explanation"])}</div></details>')
    note = notes.get(p["id"], "")
    if note:
        out.append(f'<div class="note {"fixed" if note.upper().startswith("FIXED") else ""}">Checker: {html.escape(note)}</div>')
    out.append("</div>")
out.append("</main></body></html>")
open("astra-problems.html", "w").write("\n".join(out))
print(len(probs), "problems,", sum(1 for p in probs if p.get("figure") and os.path.exists(f"figures/{p['id']}.png")), "figures drawn")
