#!/usr/bin/env python3
"""Build platform-developer.json from "Master File for Platform Developer 1.pdf".

The PDF is image-only (69 pages). Pages were extracted and OCR'd (see tools/parse_platform_developer_master.py),
then transcribed from the page images into datasets/source-snapshots/platform-developer-master/batch-1..5.json:
  [{page, label, stem, options {A..E}, answer [letters], category, explanation, review?, reviewNote?, restored?}]
`label` is the printed question number (the source has duplicate/skipped numbers), so questions are numbered
1..N in file order. Exact repeats (same stem, options and key) are dropped and listed in DUPES.
Keys are kept as printed; disagreements are noted in the explanation and flagged review/reviewNote.

The previous bank (DamianOs22 simulator, 193 q) is backed up at
datasets/source-snapshots/platform-developer/platform-developer.simulator-based.json.

Text fields are rendered as HTML (the app inserts them with innerHTML): everything is escaped,
multi-line code becomes <pre class="q-code">, code-like options and `backticked` spans become <code>.

Run: python3 tools/build_platform_developer.py
"""
import html, json, re, textwrap
from collections import Counter
ROOT = "/Users/kcontreras/dot/sf-exam"
SNAP = f"{ROOT}/datasets/source-snapshots/platform-developer-master"
CATS = ["Developer Fundamentals", "Process Automation & Logic", "User Interface", "Testing, Debugging & Deployment"]

SRC = []
for n in range(1, 6):
    SRC += json.load(open(f"{SNAP}/batch-{n}.json"))

CODE_LINE = re.compile(r"[;{}]\s*$|^\s*[@<}]|^\s*(public|private|global|trigger|for|if|List<|SELECT)\b")
CODE_OPT = re.compile(r"[;{}]|^@|^<|^\$\w|^\[?\s*(SELECT|FIND)\b|^(public|global|private|webservice)\b|^[\w.]+\(.*\)$|^\w+: \w+, \w+: \w+$")

PROSE_WORDS = re.compile(r"\b(to|the|and|is|are|not|within|when|of|with|lines?|into|using)\b")

def is_code_line(line):
    return line.startswith((" ", "\t")) or bool(CODE_LINE.search(line))

def render_stem(s):
    """Prose lines (the PDF's line wraps) are rejoined into one paragraph; runs of code lines
    (indented, or ending in ; { }) become a dedented <pre>."""
    out, run, kind = [], [], None
    def flush():
        if not run:
            return
        if kind == "code":
            code = textwrap.dedent("\n".join(run)).strip("\n")
            out.append(f'<pre class="q-code">{html.escape(code, quote=False)}</pre>')
        else:
            out.append(f'<span>{html.escape(" ".join(l.strip() for l in run), quote=False)}</span> ')
        run.clear()
    for line in s.strip().split("\n"):
        if not line.strip():
            flush(); kind = None; continue
        k = "code" if is_code_line(line) else "prose"
        if k != kind:
            flush(); kind = k
        run.append(line)
    flush()
    return "".join(out).strip()

def looks_like_code(s):
    return bool(CODE_OPT.search(s)) and len(PROSE_WORDS.findall(s)) < 2

def render_options(opts):
    """Multi-line options become <pre>; if at least half the options look like code, all are <code>."""
    opts = {k: v.strip().rstrip(",") for k, v in opts.items()}
    as_code = 2 * sum(map(looks_like_code, opts.values())) >= len(opts)
    def one(s):
        if "\n" in s:
            return f'<pre class="q-code">{html.escape(s, quote=False)}</pre>'
        return f"<code>{html.escape(s, quote=False)}</code>" if as_code else html.escape(s, quote=False)
    return [{"letter": k, "text": one(v)} for k, v in opts.items()]

def render_prose(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s.strip(), quote=False))

# Same question as an earlier item, but transcribed with different option order/wording, so the exact
# match above misses it. (page, label) of the copy to drop -> label of the kept copy.
NEAR_DUPES = {(54, 173): 44, (63, 209): 60, (64, 211): 62, (65, 214): 73, (57, 185): 120, (68, 223): 156,
              # Same Agentforce-limits question printed twice with different keys (A,B on p.61 vs B,C on p.62);
              # the p.62 key matches the commonly cited answer, so that copy is kept.
              (61, 203): 205}
# reviewNote overrides for kept items whose note referred to a dropped copy
NOTE = {(62, 205): "The source prints this question twice with different keys (A, B and B, C); this copy's key "
                   "(primitive data types + messaging character limits) matches the commonly cited answer."}

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

bank, seen, DUPES = [], {}, []
for q in SRC:
    key = (norm(q["stem"]), tuple(norm(v) for v in q["options"].values()), tuple(sorted(q["answer"])))
    if key in seen:
        DUPES.append((q["page"], q["label"], seen[key])); continue
    if (q["page"], q["label"]) in NEAR_DUPES:
        DUPES.append((q["page"], q["label"], f"label {NEAR_DUPES[(q['page'], q['label'])]}")); continue
    assert q["category"] in CATS, (q["label"], q["category"])
    assert q["answer"] and all(a in q["options"] for a in q["answer"]), (q["label"], q["answer"])
    n = len(bank) + 1
    seen[key] = n
    item = {
        "id": n,
        "category": q["category"],
        "text": render_stem(q["stem"]),
        "options": render_options(q["options"]),
        "answer": sorted(q["answer"]),
        "multi": len(q["answer"]) > 1,
        "explanation": render_prose(q["explanation"]),
        "sourceRef": f"Master File p.{q['page']} Q{q['label']}",
    }
    if q.get("review"):
        item["review"] = True
        item["reviewNote"] = render_prose(NOTE.get((q["page"], q["label"])) or q.get("reviewNote")
                                          or "Answer key flagged during the bank audit.")
    bank.append(item)

json.dump(bank, open(f"{ROOT}/platform-developer.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(SRC)} source items, {len(DUPES)} exact repeats dropped -> {len(bank)} questions, "
      f"{sum(q['multi'] for q in bank)} multi, {sum(bool(q.get('review')) for q in bank)} review")
print("repeats (page, label -> kept id):", DUPES)
print(json.dumps(Counter(q["category"] for q in bank), indent=1))
