# Platform App Builder Question Bank — Rebuild Notes

`app-builder.json` was **rebuilt on 2026-09-22** from `datasets/source-snapshots/app-builder/Platform App Builder — Exam Simulator.html`, replacing the 236-question bank that had been parsed from `Plat-Admn-202 2.pdf`. The previous bank is preserved (gitignored) at `datasets/source-snapshots/app-builder/app-builder.pdf-based.json`.

## Source

The HTML is a self-contained JavaScript exam simulator. Its questions live in two arrays inside the inline `<script>`:

| Array | Items | Used |
|---|---|---|
| `BANK` | 153 | ✅ all |
| `ADDITIONAL_BANK` | 26 | ❌ every item is a re-shuffled duplicate of a `BANK` question (same stem, same correct option text) |

`tools/parse_app_builder_html.js` extracts both arrays to `app-builder-html-raw.json`; the bank is built from `BANK` only. There are no duplicates within `BANK`. Each item has `text`, `options` (4; one has 3), and `correct` (index) — **no explanations and no categories**, so all 153 explanations and category assignments were authored for this bank. Some items carry author flags: `changedFromOriginal` (11 — the simulator's author edited the question or key), `flowDiagram` (2), `screenshotStyle` (1).

Overlap with the old PDF bank: 27 exact + 38 near matches; 88 questions are new to this project, and 209 old PDF questions are no longer in the bank.

## Final bank: 153 questions, single-answer

| Category | Questions |
|---|---|
| Data Modeling & Management | 51 |
| Business Logic & Automation | 41 |
| User Interface | 34 |
| App Deployment | 22 |
| Salesforce Fundamentals | 5 |

Exam registry (`exams.json`, `app.js`): count 236 → 153; passing score, time, and category names unchanged.

## Answer keys

Keys were taken **exactly as set in the HTML** (`correct` index). None were changed. A few are worth a second look; each is noted inside its explanation rather than overridden:

| Q | File key | Concern |
|---|---|---|
| 72 | Update page layout assignments | If layouts are assigned, fields missing after a change set usually means field-level security wasn't deployed (profiles not included). |
| 146 | RowCount = count of parent (Account) records | In an "Accounts with Opportunities" report the row count reflects rows returned, i.e. Account–Opportunity pairs. Flagged `changedFromOriginal` by the author. |
| 113 | Read on Case and Issue__c | Junction visibility does require Read on both masters; object permission on the junction itself is also needed in practice. |
| 137 | Enable Dynamic Forms on Mobile "in Salesforce Mobile App Studio" | The setting lives under the Salesforce Mobile App settings in Setup; the feature name is right, the location wording is loose. |

## Structural fixes

- **Q101** — the stem in the file begins mid-sentence ("A follow-up Task is created…"); the missing opening was reconstructed as *"When a Case at Universal Containers is escalated, three things must happen automatically:"*, which is the only scenario consistent with the options.
- **Q144** — options were written as bullet lists; bullets were flattened into sentences.
- Line breaks inside stems/options were collapsed to single spaces.

## Legacy

`tools/parse_app_builder_pdf.py` and the `Plat-Admn-202 2.pdf` snapshot remain for reference but no longer feed the bank.

## Flagged questions in the app

Questions on the flagged list carry `"review": true` and a short `"reviewNote"` in the bank JSON. The app shows them with a ⚑ **Flagged** badge, prints the note above the explanation, and collects all of them in a virtual **⚑ Flagged Keys** tab and dashboard row (they still count in their real category for scoring).
