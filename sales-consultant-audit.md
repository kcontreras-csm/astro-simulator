# Sales Cloud Consultant Question Bank — Build Notes

> **2026-10-15 — bank rebuilt from `datasets/sales/set1.json` … `set6.json`.** The previous 390-question bank (PDF dump + Udemy course) was removed in commit `7673457`; it is preserved at `datasets/source-snapshots/sales-consultant/sales-consultant.pre-sets.json` (= `git show bac3b8d:sales-consultant.json`).

## Source → bank

`tools/build_sales_consultant_from_sets.py` reads the six set files (`{"question": "N. stem", "options": ["A. …"], "answer": "X"}`) and writes `sales-consultant.json`.

- **119 questions**, numbered 1–119 across the sets (set1: 1–15, set2: 16–35, set3: 36–55, set4: 56–75, set5: 76–95, set6: 96–119). Question `id` = set number; `sourceRef` = `setN.json QN`.
- All single-answer, 3 options. No duplicates within the sets (Q1/Q70, Q16/Q75 and Q59/Q67/Q78 test the same feature with different stems).
- Text cleanup only: `Al` → `AI`, `marketingdata` → `marketing data`.
- **Keys are exactly as given in the sets.**

## Explanations

- **41 reused** from the previous bank: same question, same options, same key (`prevId` = previous bank id). Q69's explanation had one option letter fixed because the option order changed.
- **78 written fresh**, including every question whose key disagrees with the previous bank.
- 13 more questions match the previous bank's options but key a different answer (Q8, 27, 30, 37, 39, 43, 50, 52, 63, 64, 93, 114, 117). They keep `prevId` and get a fresh explanation.

## Contested keys (27)

These items carry `"review": true` and a `reviewNote`, so the app shows a **⚠ Key contested** badge. Each explanation starts with "Exam key: …" and adds a "Note:" with the documentation-supported answer.

**Key appears incorrect (documentation clearly points elsewhere):** Q6 (UAT, not Deployment), Q25 (split contacts across ≥30 accounts, account data skew), Q34 (assign the manager in the forecast hierarchy), Q37 (order start date within contract dates), Q42 (Make Less Formal), Q43 (flow with email alert), Q50 (implicit Read on the parent Account), Q63 (Capability Model), Q71 (contradicts Q12; don't delete products in use), Q93 (Single Category / Cumulative Forecast Rollup).

**Previous bank keyed differently (no clear documentation verdict either way):** Q4, 8, 27, 30, 39, 40, 52, 55, 64, 65, 102, 114, 117.

**Contested on documentation reasoning:** Q23 (Opportunity Splits / overlay split), Q36 (Data Cloud → customer lifetime value), Q97 (ownership skew → remove user from role hierarchy), Q118 (opportunities missing activities).

Notes are based on the previous bank's audit (which used ExamTopics threads, flashcard transcriptions and Salesforce Help) and on Salesforce platform behaviour. No new web verification was done for this build.

## Registration

Exam id `sales-consultant` (new id, so saved progress and 🚩 flags from the old `sales-cloud-consultant` bank don't attach to different questions), added to `exams.json` and the embedded `EXAM_REGISTRY` in `app.js`: SALES-CON-201, 62% passing score, 105 minutes, 119 questions, 9 categories (same category set as the previous bank).

| Category | Questions |
|---|---|
| Product Knowledge & Integration | 26 |
| Implementation Strategies | 19 |
| Data, Reports & Dashboards | 18 |
| Opportunity Management | 12 |
| Lead & Campaign Management | 12 |
| Agentforce & AI | 11 |
| Consulting Practices | 8 |
| Sales Life Cycle & Forecasting | 8 |
| Account & Contact Management | 5 |
