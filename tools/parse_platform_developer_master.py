#!/usr/bin/env python3
"""Parse the OCR text of "Master File for Platform Developer 1.pdf" into raw question items.

The PDF is image-only (69 rendered pages, no text layer). OCR it first:
  D=datasets/source-snapshots/platform-developer-master
  pdfimages -png "$D/Master File for Platform Developer 1.pdf" $D/pages/p
  (cd $D/pages && ls p-*.png | xargs -P 8 -I{} tesseract {} {}.ocr --psm 4 -l eng)
  cat $D/pages/p-*.ocr.txt > $D/ocr-all.txt

Question headers in the source are "Question N" or "N. stem…", and the numbering has mistakes
(two "Question 51", four "Question 133", missing 134/135/196–200/225), so items are numbered by
their order in the file; `label` keeps the printed number. Answers look like "Answer: A, C" or
"Answer: ABD". Writes $D/pd1-master-raw.json:
  {num, label, page, stem, options {A..E}, answer [letters]}
Run: python3 tools/parse_platform_developer_master.py
"""
import glob, json, re, os
ROOT = "/Users/kcontreras/dot/sf-exam"
D = f"{ROOT}/datasets/source-snapshots/platform-developer-master"

HEADER = re.compile(r"^\s*(?:Question\s+(\d+)\s*$|(\d{1,3})\.\s+(\S.*))")
OPTION = re.compile(r"^\s*([A-E])(?:[.,]|c\.)\s*(.*)$")   # OCR sometimes reads "C." as "Cc."
ANSWER = re.compile(r"Answer:\s*([A-E](?:\s*[,&]?\s*[A-E])*)")

lines = []   # (page, text)
for path in sorted(glob.glob(f"{D}/pages/p-*.ocr.txt")):
    page = int(re.search(r"p-(\d+)", path).group(1)) + 1
    lines += [(page, l.rstrip()) for l in open(path, encoding="utf-8").read().splitlines()]

items, cur = [], None
def close():
    if cur: items.append(cur)
for page, line in lines:
    m = HEADER.match(line)
    if m and not (cur and cur["opt"] and not cur["answer"] and m.group(2)):   # "1." inside options isn't a header
        close()
        cur = {"label": int(m.group(1) or m.group(2)), "page": page, "stem": [m.group(3)] if m.group(3) else [],
               "options": {}, "opt": None, "answer": []}
        continue
    if not cur or cur["answer"]:
        continue
    a = ANSWER.search(line)
    if a:
        cur["answer"] = sorted(set(re.findall(r"[A-E]", a.group(1))))
        continue
    o = OPTION.match(line)
    if o and (o.group(1) not in cur["options"]) and (cur["opt"] or o.group(1) == "A"):
        cur["opt"] = o.group(1)
        cur["options"][cur["opt"]] = o.group(2)
        continue
    if cur["opt"]:
        if line.strip():
            cur["options"][cur["opt"]] += ("\n" if re.match(r"^\s{2,}|.*[;{}]\s*$", line) else " ") + line.strip()
    else:
        cur["stem"].append(line)
close()

out = []
for n, it in enumerate(items, 1):
    stem = "\n".join(it["stem"]).strip()
    stem = re.sub(r"\n{3,}", "\n\n", stem)
    out.append({"num": n, "label": it["label"], "page": it["page"], "stem": stem,
                "options": {k: v.strip() for k, v in it["options"].items()}, "answer": it["answer"]})
json.dump(out, open(f"{D}/pd1-master-raw.json", "w"), indent=1, ensure_ascii=False)
bad = [q["num"] for q in out if len(q["options"]) < 3 or not q["answer"] or any(a not in q["options"] for a in q["answer"])]
print(f"{len(out)} items; suspicious: {bad}")
