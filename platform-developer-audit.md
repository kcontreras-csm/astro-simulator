# Platform Developer I Question Bank — Build Notes

> **2026-11-18 — new exam, ported from the simulator at https://github.com/DamianOs22/Platform-Developer-I/blob/main/index.html** (saved to `datasets/source-snapshots/platform-developer/index.html`, gitignored).

## Source → bank

`tools/build_platform_developer.py` reads the simulator's `const SECTIONS=` and `const QUESTIONS=` lines (both are JSON) and writes `platform-developer.json`.

- **193 questions** (`id` = the simulator's id, `sourceRef` = its `PLAT-DEV-201 Qn` ref). 136 single-answer, 44 choose-2, 13 choose-3. Options: 179 with four, 12 with five, 2 with three.
- **Categories** are the simulator's four sections, which match the official exam outline: Developer Fundamentals (42), Process Automation & Logic (47), User Interface (52), Testing, Debugging & Deployment (52).
- **Keys are exactly as given in the simulator.** It marks 25 keys as corrected by its author (`verified_conflict`). Those were kept too.
- Exam id `platform-developer-1`, code PLAT-DEV-201, passing score 68%, 105 minutes.

## Rendering

The app inserts question text, options and explanations as HTML, and this bank has Apex, SOQL, LWC and Visualforce code. The build escapes every field and then:
- turns multi-line code in stems and options into `<pre class="q-code">`
- shows all of a question's options in `<code>` when at least half of them look like code
- turns `backticked` spans in explanations into `<code>`

Styles for this are in `styles.css` (`.q-code`, inline `code`).

Stem fixes: 6 stems had code flattened onto one line (Q52, 61, 64, 159, 167, 175) and were put back on separate lines. OCR typos were fixed (`Whatld` → `WhatId`, `Parentid`, `Contactid`, `SOQL Is`).

## Explanations

The simulator's explanations are PDF text. Many are cut off mid-sentence, have words run together, or are filler ("Below is the formatted response…"). **All 193 explanations were rewritten** (2–4 sentences, why the key is right and why the other options are wrong). They are stored in `datasets/source-snapshots/platform-developer/exp-1..4.json`, keyed by id. To change one, edit its entry there and rerun the build.

## Contested keys (9)

These carry `review`/`reviewNote` (the **⚠ Key contested** badge). Their explanations start with "Exam key: …" and add a "Note:".

**Exhibit missing from the source:** Q20 (trigger code, lines 03/16), Q48 (the three roll-up fields), Q59 (Visualforce snippet; options look garbled), Q71 (Visualforce page and controller).

**Key appears incorrect or questionable:** Q36 (approval processes aren't auto-launched; a before-save trigger also works), Q49 (debug DML rollback is optional; a schedule-triggered debug run uses one record), Q95 (Enhance methods return `List<List<Recommendation>>`), Q106 (dependent-picklist JavaScript validation runs first), Q118 (SOQL returns Integer from `COUNT()`, not Double).

These checks used Salesforce platform knowledge only. No web verification was done for this build.
