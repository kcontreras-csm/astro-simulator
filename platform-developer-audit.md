# Platform Developer I Question Bank — Build Notes

> **2026-11-19 — bank rebuilt from `Master File for Platform Developer 1.pdf`.** It replaces the 2026-11-18 bank (193 q from the DamianOs22 simulator HTML). That bank is preserved at `datasets/source-snapshots/platform-developer/platform-developer.simulator-based.json`. The exam id changed from `platform-developer-1` to `plat-dev-201`, so saved progress and flags on the old questions don't attach to the new ones.

## Source → bank

- The PDF is **image-only** (69 rendered pages, no text layer). Pages were extracted with `pdfimages` and OCR'd with tesseract (`tools/parse_platform_developer_master.py` documents the commands and gives a regex parse of the OCR for cross-checking).
- The questions were then **transcribed from the page images** into `datasets/source-snapshots/platform-developer-master/batch-1..5.json`, using the OCR as a draft. Each item has a section, an explanation and review flags. `tools/build_platform_developer.py` merges the batches into `platform-developer.json`.
- **225 items** in the PDF. The printed numbering is unreliable (two "Question 51", four "Question 133", no 134/135/196–200/225), so questions are numbered 1–N in file order. `sourceRef` keeps the page and printed label.
- **18 repeats dropped → 207 questions**: 11 exact repeats, 6 that differ only in transcription or option order, and one question printed twice with different keys (labels 203/205; the copy whose key matches the commonly cited answer is kept). All are listed in `DUPES`/`NEAR_DUPES` in the build script.
- Sections (the PDF has none, so they were assigned per the PD1 outline): Developer Fundamentals 65, Testing, Debugging & Deployment 46, User Interface 46, Process Automation & Logic 50. 63 questions are multi-select.
- Text cleanup: `_c` → `__c`/`__r`, OCR artifacts, code put back onto separate lines, "Choose N answers" lines removed (the app shows "Select N").
- **Keys are exactly as printed**, except two garbled answer lines: label 50 printed "CA,C" (read as A, C) and label 229 printed "Answer: Acreates an Apex interface" (read as A).

## Explanations

The PDF has none. All 207 were written for this bank. A few were adapted from the 2026-11-18 bank where the question and key matched.

## Flagged items (53)

These carry `"review": true` and a `reviewNote`, so the app shows a **⚠ Key contested** badge with the note.

### Key appears incorrect or questionable (25)
The explanation starts with "Exam key: …" and adds a "Note:" with the documented answer.

- **Q6** (p.2 Q6): Key appears incorrect: Developer Console cannot edit Lightning web components; VS Code (D) is the documented answer.
- **Q13** (p.4 Q13): Key appears incorrect: roll-up summary fields need master-detail; with a Lookup the answer is the record-triggered flow on Sales_Help_Request__c (C).
- **Q14** (p.4 Q14): Key appears incorrect: documented answer is Content asset files, SVG resources, Static resources (A, B, E); 'All external libraries' is false.
- **Q20** (p.6 Q20): Key appears incorrect: the import must name the method, '@salesforce/apex/AccountController.updateAccounts' (B).
- **Q23** (p.7 Q23): Key appears incorrect: individual orgs with production configuration for many developers are Developer Sandboxes (B).
- **Q36** (p.10 Q36): Key appears incorrect: the 5 MB size limit is wrong (current limit is 20 MB); documented answer is A, B, D.
- **Q48** (p.14 Q48): Key appears incorrect: newAccounts is never inserted, so the total is 5 + 1 = 6 (B).
- **Q53** (p.15 Q52): Key appears incorrect: documented answer is B, C (asynchronous limits apply and can still be exceeded).
- **Q66** (p.19 Q65): Key appears incorrect: documented answer is B (150 DML statements limit exceeded by update in loop).
- **Q82** (p.26 Q86): Key appears incorrect: documented answer is A (record-triggered flow on Opportunity); a Task trigger cannot fire on Opportunity creation.
- **Q84** (p.27 Q88): Key appears incorrect: documented answer is B (subquery must use the child relationship name Trainers__r).
- **Q98** (p.31 Q102): Key appears incorrect: documented requirements are 75% coverage and every trigger covered (B, C); System.assert calls are a best practice, not enforced.
- **Q100** (p.31 Q104): Key appears incorrect: >10,000 DML rows throws an uncatchable LimitException, so 'transaction will fail due to exceeding the governor limit' (B) is documented. Also the source dropped the 'A.' label on the first option; restored.
- **Q122** (p.38 Q126): Key appears incorrect: 'Allow reparenting' on the master-detail field (B) is the documented way to move detail records to a new master.
- **Q126** (p.39 Q130): Key appears incorrect: Edit overrides in Lightning Experience use a Lightning component (or Visualforce), not a Lightning page; documented answer is D.
- **Q145** (p.46 Q148): Key appears incorrect: asserts aren't required to deploy; documented requirements are 75% overall coverage and at least 1% (one line) trigger coverage (B, C).
- **Q146** (p.46 Q149): Key appears incorrect: the documented approach is Lightning Out in a Visualforce page (D); Apex can't render an LWC.
- **Q148** (p.47 Q151): Key appears incorrect: a virtual class is used via 'extends OrderRequest' (B), not 'implements Order'.
- **Q161** (p.51 Q164): Key appears incorrect: Trigger.old is null in insert triggers (C), not an empty list.
- **Q179** (p.56 Q183): Key appears incorrect: Account can't be the detail in a master-detail; correct model is a lookup on Account to Global Address (D).
- **Q180** (p.57 Q184): Key appears incorrect: a LIMIT clause would skip Assets; bulkifying getAssetsToUpdate (A) is the standard answer. Also the source omits the code snippet ('[Code snippet in document]').
- **Q183** (p.58 Q188): Key appears incorrect: INCLUDES() cannot compare a multi-select picklist to a field value; a record-triggered flow is the standard answer (yesterday's bank keyed it).
- **Q185** (p.59 Q190): Key appears incorrect: the commonly cited answer is A, D, E (Custom Permission, Dynamic Form, Dynamic Action on the Account Record Page); a custom LWC is not needed.
- **Q198** (p.66 Q218): Key appears incorrect: Salesforce docs list cascading deletes among operations that don't invoke triggers; only FeedItem updates is clearly correct, so the question has no valid second answer.
- **Q199** (p.66 Q219): Key appears incorrect: the Data Import Wizard supports up to 50,000 records but not Opportunities (D); yesterday's bank keyed D's wording.

### Text restored from garbled source (20)
Parts of the PDF are themselves garbled (pasted bad OCR, e.g. "Use SOQE to carry the app", `Test::ListSize(s)`, dropped options). Where the intended standard PD1 question was clear, the wording was restored.

- **Q12** (p.4 Q12): Restored the standard option set: the source omitted 'All triggers must have some test coverage', so the printed key A, B pointed to the custom-objects distractor. That option is restored as B, and the custom-objects option moved to D so the printed key matches.
- **Q25** (p.7 Q25): Option C was garbled in the source ('$C.AddQIsTest(seeAllData=true)$'); restored to 'Add @isTest(seeAllData=true) at the start of the unit test class.'
- **Q30** (p.9 Q30): Option D was garbled (LaTeX artifacts) and restored to @RestResource(urlMapping='/myService/*'). Key appears incorrect: @RestResource (D) is the documented answer.
- **Q33** (p.9 Q33): Option A was truncated in the source ('extends Payment {'); restored to the full standard implementation with override. Class name 'CreditCard Payment' was normalized to CreditCardPayment. Source lists only two options.
- **Q60** (p.18 Q59): Source lists only option A; options B-D restored from the standard question. Key appears incorrect: the standard answer is the re-parentable master-detail from Line Item to Order (roll-up summary needed).
- **Q63** (p.18 Q62): Option D header was garbled in the source ("extends SortableSalesforce" with no brace); restored to "extends Sortable, Drawable {".
- **Q71** (p.21 Q70): Source printed options C and D both as "aura-flow"; C restored to "aura:flow".
- **Q105** (p.33 Q109): Source code had the closing brace of the for loop before the query line; restored the query inside the loop as the question intends.
- **Q130** (p.41 Q133): Source text is partly garbled: first option read "Implement the 'up**** DML statement'"; restored to "Implement the upsert DML statement" and removed stray backticks from the options.
- **Q133** (p.42 Q136): Source layout put the pay() method outside the class braces in the keyed option and split the class/interface names ('CheckPayment Processor', 'Payment Processor'); restored the method inside the class and joined the names.
- **Q139** (p.44 Q142): Restored option text: source printed '<span/>' for <apex:includeLightning/> and '<span lightning/>' for <apex:slds/> (tags lost in conversion), and dropped the $ prefix on $Lightning methods.
- **Q147** (p.47 Q150): Restored option text: source printed '@AuraEnabled(cachedAlert=true)' and '@AuraEnabled(storable=true)' for the standard storable=true / cacheable=true options; keyed C now reads cacheable=true.
- **Q159** (p.50 Q162): Key appears incorrect: 'webservice class' is invalid; SOAP services need a global class with webservice static methods (D). Option D was truncated in the source and was completed with the standard wording.
- **Q169** (p.53 Q172): Source options garbled ('Seller record triggers flow', 'After querying', 'After record triggers flow', 'Validate rule'); restored to the standard wording. Key appears incorrect: an after-delete flow can't block deletion; documented answer is before-delete flow + Apex trigger (A, B).
- **Q176** (p.56 Q180): Restored garbled options to the standard wording (source: 'Prebuilt Components that will be tested', 'Extended sparsely inside for applications', 'Support for Course and Lightning IDs', 'Forfeited to create custom components').
- **Q177** (p.56 Q181): Restored garbled options B ('Employment is done...') and D ('...between two new retailers a deployment connection') to the standard wording.
- **Q178** (p.56 Q182): Restored garbled options ('Use SOQE to carry the app...', 'Test::ListSize(s)') to the standard wording with Test.loadData().
- **Q197** (p.66 Q217): Source code contained LaTeX-style artifacts ('Integer $x=0;$', '$x=x+1;$', 'while $(x<1)$'); restored to plain Apex.
- **Q201** (p.67 Q221): Source text has OCR typos ('Postal CodaToTime=ones', 'procoess', 'assignmnent', 'formmula fisld'); restored to the standard wording.
- **Q202** (p.67 Q222): Source code is garbled OCR ('Boolean isCE:r', 'iz0KE', '130K', 'w - 2'); restored to the standard isOK snippet (third branch 'isOK != null', consistent with key 4). Only three options in source.

### Other (8)

- **Q21** (p.6 Q21): Key appears incomplete: stem asks for two answers but key has one; documented answer is A, C (validation rule and before-save trigger).
- **Q24** (p.7 Q24): Source lists only two options (the original question has four, for example a static variable on a helper class); key kept as printed.
- **Q51** (p.15 Q50): Printed key is garbled ("CA,C"); read as A, C.
- **Q132** (p.42 Q133): Source text is garbled; no printed option is valid SOQL and the key D (Job_Application_s with Accounts.Industry) is not correct. Standard answer is (SELECT Id FROM Job_Applications__r) ... WHERE Account.Industry = 'Technology'.
- **Q174** (p.55 Q178): Source text is garbled in distractors A and B (nonsense phrases); kept as printed since the original wording isn't certain. Keyed C and D are readable.
- **Q190** (p.60 Q195): Keyed option uses standardController="Notice"; for a custom object the API name Notice__c is required, so the option is only correct in pattern.
- **Q194** (p.62 Q205): The source prints this question twice with different keys (A, B and B, C); this copy's key (primitive data types + messaging character limits) matches the commonly cited answer.
- **Q207** (p.69 Q229): Printed answer line is garbled ('Answer: Acreates an Apex interface'); key recorded as A.
