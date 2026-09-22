#!/usr/bin/env node
/* Extract the embedded question arrays from the Platform App Builder simulator HTML.
   Usage: node tools/parse_app_builder_html.js
   Reads  datasets/source-snapshots/app-builder/Platform App Builder — Exam Simulator.html
   Writes datasets/source-snapshots/app-builder/app-builder-html-raw.json
   Items: {num, text, options:[str], answer:[letter], multi:false, source:'BANK'|'ADDITIONAL', flags:[...]}.
   ADDITIONAL_BANK entries are re-shuffled duplicates of BANK items; the final bank uses BANK only. */
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "..");
const SRC = path.join(ROOT, "datasets/source-snapshots/app-builder/Platform App Builder — Exam Simulator.html");
const OUT = path.join(ROOT, "datasets/source-snapshots/app-builder/app-builder-html-raw.json");
const html = fs.readFileSync(SRC, "utf8");
const js = html.slice(html.indexOf("<script>") + 8, html.indexOf("</script>"));
function grab(name) {
  const i = js.indexOf("const " + name + " = [");
  const start = js.indexOf("[", i);
  let depth = 0, j = start, inT = false, inS = false, inD = false;
  for (; j < js.length; j++) {
    const c = js[j], p = js[j - 1];
    if (inT) { if (c === "`" && p !== "\\") inT = false; continue; }
    if (inS) { if (c === "'" && p !== "\\") inS = false; continue; }
    if (inD) { if (c === '"' && p !== "\\") inD = false; continue; }
    if (c === "`") inT = true; else if (c === "'") inS = true; else if (c === '"') inD = true;
    else if (c === "[") depth++; else if (c === "]") { depth--; if (depth === 0) break; }
  }
  return eval(js.slice(start, j + 1));
}
const BANK = grab("BANK"), ADD = grab("ADDITIONAL_BANK");
const conv = (q, i, source) => ({
  num: i + 1, text: q.text.replace(/\s*\n\s*/g, " ").trim(), options: q.options.map(o => o.trim()),
  answer: [String.fromCharCode(65 + q.correct)], multi: false, source,
  flags: ["changedFromOriginal", "flowDiagram", "screenshotStyle"].filter(k => q[k]),
});
const items = [...BANK.map((q, i) => conv(q, i, "BANK")), ...ADD.map((q, i) => conv(q, BANK.length + i, "ADDITIONAL"))];
fs.writeFileSync(OUT, JSON.stringify(items, null, 1));
console.log(`BANK ${BANK.length} + ADDITIONAL ${ADD.length} = ${items.length} -> ${path.basename(OUT)}`);
