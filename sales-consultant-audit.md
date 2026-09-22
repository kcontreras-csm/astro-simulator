# Sales Cloud Consultant Question Bank — Build Notes

> **2026-09-21 — bank rebuilt with the dump's original keys.** At the user's request `sales-consultant.json` now uses the answer key exactly as printed in `Sales-Cloud-Consultant (1).pdf` (v33.3, content-identical to the original PDF). The 21 documentation-based corrections described below are **no longer applied**; each affected explanation states the exam key and carries a "Note (documentation)" where Salesforce sources disagree. The verified-key version is preserved locally at `datasets/source-snapshots/sales-consultant/sales-consultant.verified-keys.json`. All 21 questions are in `flagged-questions.json`.

`sales-consultant.json` was built from `datasets/source-snapshots/sales-consultant/Sales-Cloud-Consultant.pdf` (DXperience dump, v33.3, 2026-08-31, 64 pages, "Salesforce Certified Agentforce Sales Consultant" header) on 2026-09-11.

## Source → bank

- `tools/parse_sales_consultant_pdf.py` extracts the 190 `Question: N / A. B. C. / Answer: X` blocks into `sales-consultant-raw.json`.
- The PDF has **no explanations** — all 190 were written from Salesforce documentation and consulting best practice.
- All questions are single-answer with 3 options (one 4-option question, Q117, was a parse artifact — see below).
- No duplicate questions within the PDF.

Final bank: **190 questions**.

| Category | Questions |
|---|---|
| Product Knowledge & Integration | 35 |
| Data, Reports & Dashboards | 28 |
| Implementation Strategies | 26 |
| Lead & Campaign Management | 25 |
| Account & Contact Management | 22 |
| Consulting Practices | 22 |
| Sales Life Cycle & Forecasting | 20 |
| Opportunity Management | 12 |

Categories map to the official exam outline with two merges: *Implementation Strategies* and *Consulting Practices* stay separate; *Sales Life Cycle* absorbs forecasting/territories/quotas; *Application of Product Knowledge* absorbs *Sales Productivity & Integration*; *Sales Metrics, Reports & Dashboards* absorbs *Data Management*.

## Answer keys

The dump key was reviewed question by question, then the uncertain ones were cross-checked (2026-09-14) against ExamTopics community discussions and Salesforce Help. **21 keys differ from the dump:**

| Q | Dump | Bank | Reason / evidence |
|---|---|---|---|
| 14 | B | A | Salesforce Help: *Enable Lead Conversion in the Salesforce Mobile App* is a Lead Settings option |
| 16 | A | B | Account Hierarchy is display-only; it never grants record access |
| 64 | B | C | Real exam text adds "for every four prospect meetings held, one sale was generated" (ExamTopics #366) — sentence restored in the bank |
| 72 | C | B | Contacts to Multiple Accounts preserves history as a contractor changes companies |
| 75 | C | A | Under Public Read-Only, a rep edits only opportunities they own *(no external evidence — judgment call)* |
| 76 | B | C | Report subscriptions let managers control frequency (ExamTopics #204) |
| 78 | C | B | Private OWD + public group → sharing rule |
| 81 | A | B | Budget/priority governance → executive steering committee |
| 84 | A | B | Adoption KPI is logins, not Closed Lost |
| 88 | A | C | Build in Developer sandbox, test in staging (ExamTopics #410) |
| 105 | B | A | ExamTopics #240 consensus: rate changes update *all* records incl. closed opps, so B is false; A is the true statement |
| 113 | A | C | Cumulative Forecast Rollups give the across-categories view |
| 145 | A | C | Retire a product by unchecking Active |
| 149 | B | A | ExamTopics #117: users need sharing access to the account to assign any active territory |
| 159 | B | C | Run assignment rules in Planning; activation isn't needed to view results |
| 173 | C | B | Documenting use cases starts with discovery |
| 177 | A | B | View-all / edit-own → Public Read-Only OWD |
| 182 | B | A | Training deliverables live in the SOW Scope section |
| 186 | A | C | Discovery = establish goals, define sales processes, define success metrics (multiple prep sources) |
| 189 | C | A | Roll-ups need master-detail; Account Hierarchy is a lookup → flow |
| 190 | A | B | Salesforce Help: Lead Settings decides whether the assignee's default record type is applied |

Reverted to the dump key after cross-checking: **Q127** (community split three ways, no consensus) and **Q137** (the real question is two-answer; both "one active model" and "profiles/permission sets" are correct, so the dump's C is fine and the explanation covers both).

**Still judgment calls**: Q2, 8, 18, 25, 34, 53, 55, 60, 75, 102, 118, 126, 127, 137, 184 — listed in `datasets/source-snapshots/sales-consultant/flagged-questions.json`. (Q50 was reverted to the dump's *Opportunity Percentage Split* after three independent transcriptions agreed on it.) Q126 deserves a note: the real exam version has different options; all three options in the dump version are strictly false, so A is kept as the exam key with an explanation that says so.

## Other fixes

- **Q117** — the question stem bled into option A in the PDF; stem restored, options re-lettered A–C, key kept on "Forecast Type on Opportunity Product grouped by Product Family".
- OCR cleanup across stems/options: `dat a`→`data`, `formul a`→`formula`, `Sales Could`→`Sales Cloud`, stray capitalised `In/Is/Items/Information`, `4 custom field`→`a custom field`, `@ report`→`a report`, `assignedsales`, `flied`→`field`, broken hyphens (`real- time`, `Read- Only`), curly quotes.

## Registration

Exam `sales-cloud-consultant` added to `exams.json` and the embedded `EXAM_REGISTRY` in `app.js` (passing score 62%, 105 minutes, 190 questions). Exam code `SALES-CON-201` (Salesforce's current code for this credential).

## Full external verification (2026-09-14)

Per-question sources for every changed key: see [sales-consultant-key-sources.md](sales-consultant-key-sources.md).

Every question was checked against at least one source outside our PDF where one could be found:

- **ExamTopics discussion threads** (community-corrected keys) — ~20 questions, mostly the disputed ones.
- **Two independent flashcard transcriptions of the same dump** (Brainscape: "Aran Singh" set covers Q1–65; "roy rooy" Set 3_78 covers Q128–190 with answer text) — used to detect where our PDF's key differs from other copies.
- **Salesforce Help / Trailhead** for factual claims (mobile lead conversion setting, order start-date rule, Release in a Box, standard Einstein Lead Scoring dashboard, Data Loader limits, dated exchange rates, Person Account merge rules, private contacts, etc.).
- Prep sites (Pass4Success, exam4training, exam-answer) as weak corroboration.

Outcome: 174 of 190 have at least one external source agreeing with the bank key. The flashcard sets disagree with the bank on ~30 questions, but in each case the disagreement was resolved on Salesforce documentation (e.g. Q36 Salesforce Connect cannot push data to an ERP; Q142 dated rates always use Close Date; Q148 a sandbox has the org's metadata, a Developer Edition org does not; Q153 ACM blocks Opportunity→Account currency roll-ups; Q163 order start date must fall within the contract dates). Where the transcriptions and Salesforce docs both pointed away from our key, the key was changed (Q50).

**No external evidence found (kept on documentation reasoning only):** Q68, 75, 78, 79, 81, 90, 93, 94, 97, 98, 99, 102, 103, 104, 114, 118.

## Flagged questions in the app

Questions on the flagged list carry `"review": true` and a short `"reviewNote"` in the bank JSON. The app shows them with a ⚑ **Flagged** badge, prints the note above the explanation, and collects all of them in a virtual **⚑ Flagged Keys** tab and dashboard row (they still count in their real category for scoring).
