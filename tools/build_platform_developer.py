#!/usr/bin/env python3
"""Build platform-developer.json from the Platform Developer I simulator HTML (193 questions).

Source: https://github.com/DamianOs22/Platform-Developer-I/blob/main/index.html, saved to
datasets/source-snapshots/platform-developer/index.html. Its `const QUESTIONS=[...]` line is JSON:
{id, question, options {A..E}, answers [letters], explanation, section, verified_conflict, ...}.

Keys and section assignments are used exactly as given. The source explanations are mostly truncated
PDF text, so every explanation comes from datasets/source-snapshots/platform-developer/exp-1..4.json
({"id": {"explanation", "review"?, "reviewNote"?, "text"?}}); "text" replaces a stem whose code was
flattened onto one line.

Text fields are rendered as HTML (the app inserts them with innerHTML): everything is escaped,
multi-line code becomes <pre class="q-code">, code-like options and `backticked` spans become <code>.

Run: python3 tools/build_platform_developer.py
"""
import html, json, re
from collections import Counter
ROOT = "/Users/kcontreras/dot/sf-exam"
SNAP = f"{ROOT}/datasets/source-snapshots/platform-developer"

src = open(f"{SNAP}/index.html", encoding="utf-8").read()
def grab(name):
    line = next(l for l in src.splitlines() if l.startswith(f"const {name}="))
    return json.loads(line[len(f"const {name}="):].rstrip().rstrip(";"))
SECTIONS = {s["id"]: s["name"] for s in grab("SECTIONS")}
QUESTIONS = grab("QUESTIONS")

EXP = {}
for n in range(1, 5):
    EXP.update({int(k): v for k, v in json.load(open(f"{SNAP}/exp-{n}.json")).items()})

# OCR typos in the source stems/options (lowercase l/i for I/l).
TYPO = {"Whatld": "WhatId", "Parentid": "ParentId", "Contactid": "ContactId", "SOQL Is ": "SOQL is "}
def fix(s):
    for a, b in TYPO.items():
        s = s.replace(a, b)
    return s

CODE_LINE = re.compile(r"[;{}]\s*$|^\s*[@<}]|^\s*(public|private|global|trigger|for|if|List<|SELECT)\b")
CODE_OPT = re.compile(r"[;{}]|^@|^<|^\$\w|^\[?\s*(SELECT|FIND)\b|^(public|global|private|webservice)\b|^[\w.]+\(.*\)$|^\w+: \w+, \w+: \w+$")

PROSE_WORDS = re.compile(r"\b(to|the|and|is|are|not|within|when|of|with|lines?|into|using)\b")

def render_stem(s):
    out = []
    for para in re.split(r"\n\s*\n", s.strip()):
        if "\n" in para or CODE_LINE.search(para):
            out.append(f'<pre class="q-code">{html.escape(para.rstrip(), quote=False)}</pre>')
        else:
            out.append(html.escape(para.strip(), quote=False))
    return "".join(p if p.startswith("<pre") else f"<span>{p}</span> " for p in out).strip()

def looks_like_code(s):
    return bool(CODE_OPT.search(s)) and len(PROSE_WORDS.findall(s)) < 2

def render_options(opts):
    """Multi-line options become <pre>; if at least half the options look like code, all are <code>."""
    opts = {k: fix(v).strip().rstrip(",") for k, v in opts.items()}
    as_code = 2 * sum(map(looks_like_code, opts.values())) >= len(opts)
    def one(s):
        if "\n" in s:
            return f'<pre class="q-code">{html.escape(s, quote=False)}</pre>'
        return f"<code>{html.escape(s, quote=False)}</code>" if as_code else html.escape(s, quote=False)
    return [{"letter": k, "text": one(v)} for k, v in opts.items()]

def render_prose(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s.strip(), quote=False))

bank, missing = [], []
for q in QUESTIONS:
    e = EXP.get(q["id"])
    if not e:
        missing.append(q["id"]); continue
    item = {
        "id": q["id"],
        "category": SECTIONS[q["section"]],
        "text": render_stem(fix(e.get("text") or q["question"])),
        "options": render_options(q["options"]),
        "answer": q["answers"],
        "multi": len(q["answers"]) > 1,
        "explanation": render_prose(e["explanation"]),
        "sourceRef": ", ".join(q["source_refs"]),
    }
    if e.get("review"):
        item["review"] = True
        item["reviewNote"] = render_prose(e.get("reviewNote") or "Answer key flagged during the bank audit.")
    bank.append(item)

assert not missing, f"no explanation for ids {missing}"
json.dump(bank, open(f"{ROOT}/platform-developer.json", "w"), indent=1, ensure_ascii=False)
print(f"{len(bank)} questions, {sum(q['multi'] for q in bank)} multi, {sum(bool(q.get('review')) for q in bank)} review")
print(json.dumps(Counter(q["category"] for q in bank), indent=1))
