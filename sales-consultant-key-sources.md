# Sales Cloud Consultant — Evidence Log for Changed Answer Keys

Companion to `sales-consultant-audit.md`. For every question whose key in `sales-consultant.json` differs from the source PDF (DXperience/dumpsschool dump v33.3), this lists where the correct answer was found. Verification took place 2026-09-14. **As of 2026-09-21 the bank uses the dump keys again (user decision); the "Bank" column below shows the documentation-supported answer, which is now recorded only in each question's explanation note and in `sales-consultant.verified-keys.json`.**

**Evidence strength**
- **Strong** — Salesforce documentation states the fact, or an ExamTopics community thread with reasoning agrees.
- **Medium** — independent transcriptions of the same exam (Brainscape flashcard sets, Pass4Success, prep sites) agree, or a variant of the question with a different option set implies the answer.
- **Docs reasoning** — no external copy of the question was found; the key rests on Salesforce platform behaviour cited in the explanation.

## Keys changed from the dump

| Q | Dump | Bank | Where the answer came from | Strength |
|---|---|---|---|---|
| 14 | B | A | Salesforce Help — [Enable Lead Conversion in the Salesforce Mobile App](https://help.salesforce.com/s/articleView?language=en_US&id=sf.customize_leads_enable_mobile_convert.htm&type=5) documents the Lead Settings checkbox; also [Convert Leads in the Salesforce Mobile App](https://help.salesforce.com/s/articleView?id=000336504&type=1&language=en_US). | Strong |
| 16 | A | B | Salesforce implicit-sharing behaviour — Account Hierarchy grants no access ([parent implicit sharing explained](https://www.simplysfdc.com/2016/11/salesforce-parent-implicit-sharing.html)); the [Brainscape "Aran Singh" set](https://www.brainscape.com/flashcards/set-1-17665675/packs/22560005) keys "shared manually". | Strong |
| 64 | B | C | [ExamTopics #366](https://www.examtopics.com/discussions/salesforce/view/337596-exam-certified-sales-cloud-consultant-topic-1-question-366/) — the real question contains "for every four prospect meetings held, one sale was generated" (sentence missing from the PDF; restored in the bank). | Strong |
| 72 | C | B | Salesforce Help — [Enable Contacts to Relate to Multiple Accounts](https://help.salesforce.com/s/articleView?id=ind.enable_shared_contacts.htm&type=5) (feature designed to keep a contact's history across companies); the 4-option variant of this question lists it as an answer option. | Medium |
| 75 | C | A | No external copy found. Public Read-Only OWD: a rep edits only opportunities they own. **Flagged.** | Docs reasoning |
| 76 | B | C | [ExamTopics #204](https://www.examtopics.com/discussions/salesforce/view/125783-exam-certified-sales-cloud-consultant-topic-1-question-204/) — report subscription gives managers control over frequency. | Strong |
| 78 | C | B | No external copy found. Private OWD + public group → criteria/owner-based sharing rule; there is no "object default visibility for a group". | Docs reasoning |
| 81 | A | B | No external copy found. Budget/priority governance is the remit of an executive steering committee. | Docs reasoning |
| 84 | A | B | No external copy found; the [roy rooy "Salesforce" set](https://www.brainscape.com/flashcards/salesforce-19367930/packs/23014807) keys B. Logins are the standard adoption KPI. | Docs reasoning |
| 88 | A | C | [ExamTopics #410](https://www.examtopics.com/discussions/salesforce/view/156556-exam-certified-sales-cloud-consultant-topic-1-question-410/) — suggested and commented answer C. | Strong |
| 105 | B | A | [ExamTopics #240](https://www.examtopics.com/discussions/salesforce/view/103729-exam-certified-sales-cloud-consultant-topic-1-question-240/) — commenters cite docs: rate changes update *all* records incl. closed opportunities (B false); objects-support statement true. Salesforce Help — [Considerations for Enabling Multiple Currencies](https://help.salesforce.com/s/articleView?language=en_US&id=sales.admin_enable_multicurrency_implications.htm&type=5). | Strong |
| 113 | A | C | Trailhead — [Optimize Salesforce Sales Forecasting Setup](https://trailhead.salesforce.com/content/learn/modules/sales-forecasting/configure-sales-forecasting-in-salesforce) (cumulative rollups total across categories); prep-site copies key Cumulative Forecast Rollups. | Medium |
| 145 | A | C | No external copy found. A product on an opportunity can't be deleted; unchecking Active retires it. The roy rooy set keys "archive", which also works but is not the most efficient. | Docs reasoning |
| 149 | B | A | [ExamTopics #117](https://www.examtopics.com/discussions/salesforce/view/239487-exam-certified-sales-cloud-consultant-topic-1-question-117/) — community: users need sharing access to the account to assign any active territory. | Strong |
| 159 | B | C | Salesforce Help — [Run territory assignment rules](https://help.salesforce.com/s/articleView?id=000385116&language=en_US&type=1); the [roy rooy Set 3_78](https://www.brainscape.com/flashcards/set-3_78-19375291/packs/23014807) keys the same option; consistent with Q26 (Planning state). | Strong |
| 173 | C | B | [roy rooy Set 3_78](https://www.brainscape.com/flashcards/set-3_78-19375291/packs/23014807) keys "conduct discovery sessions". | Medium |
| 177 | A | B | No external copy found; roy rooy keys the dump's A. Public Read-Only is the OWD that gives view-all / edit-own; a Read/Write sharing rule to everyone keeps the problem. | Docs reasoning |
| 182 | B | A | [roy rooy Set 3_78](https://www.brainscape.com/flashcards/set-3_78-19375291/packs/23014807) keys "Scope". | Medium |
| 186 | A | C | [exam-answer.com](https://www.exam-answer.com/sales-cloud-consultant-discovery-phase-steps) and [Brainly](https://brainly.com/question/49367564) — Discovery steps: establish goals, define sales processes, define success metrics; roy rooy "Salesforce" set keys C. | Medium |
| 189 | C | A | [ExamTopics #47](https://www.examtopics.com/discussions/salesforce/view/69901-exam-certified-sales-cloud-consultant-topic-1-question-47/) — roll-up summary fields can't aggregate across child accounts in a hierarchy (lookup, not master-detail); automation is required. | Strong |
| 190 | A | B | Salesforce Help — [Considerations for Creating and Updating Record Types](https://help.salesforce.com/s/articleView?id=platform.customize_recordtype_considerations.htm&language=en_US&type=5): an assigned lead "can keep the creator's default record type or take the record type of the assignee, depending on the lead settings specified by the administrator". | Strong |

## Overrides that were reverted after checking

| Q | Bank now | What the check showed |
|---|---|---|
| 50 | A (dump) | Two Brainscape transcriptions ([Aran Singh](https://www.brainscape.com/flashcards/set-1-17665675/packs/22560005), [roy rooy 2_72](https://www.brainscape.com/flashcards/set-2_72-19368031/packs/23014807)) and [Brainly](https://brainly.in/question/55854600) all key Percentage Split. |
| 127 | A (dump) | [ExamTopics #379](https://www.examtopics.com/discussions/salesforce/view/336688-exam-certified-sales-cloud-consultant-topic-1-question-379/) — votes split three ways, no comments. **Flagged.** |
| 137 | C (dump) | [ExamTopics #275](https://www.examtopics.com/discussions/salesforce/view/150861-exam-certified-sales-cloud-consultant-topic-1-question-275/) — two-answer version; both "one active model" and "profiles/permission sets" are correct. **Flagged.** |

## Structural fixes and their sources

| Q | Fix | Source |
|---|---|---|
| 64 | Restored the missing sentence "Historically, for every four prospect meetings held, one sale was generated." | [ExamTopics #366](https://www.examtopics.com/discussions/salesforce/view/337596-exam-certified-sales-cloud-consultant-topic-1-question-366/) |
| 117 | Stem had bled into option A in the PDF; stem restored, options re-lettered. | PDF text itself; option content confirmed by [roy rooy "Salesforce" set](https://www.brainscape.com/flashcards/salesforce-19367930/packs/23014807) and Trailhead on product-family forecast types. |
| 126 | Explanation rewritten to say all three dump options are strictly false. | [ExamTopics #321](https://www.examtopics.com/discussions/salesforce/view/142404-exam-certified-sales-cloud-consultant-topic-1-question-321/) — real version has different options (A & D). |

## Disputed keys that were kept, with the deciding source

| Q | Kept | Deciding source |
|---|---|---|
| 43 | Standard dashboard | Salesforce Help — [Standard Dashboard for Einstein Lead Scoring](https://help.salesforce.com/s/articleView?id=sf.sales_einstein_standard_reports.htm&language=en_US&type=5) |
| 55 | Universal Process Notation | Trailhead — [Understanding Universal Process Notation](https://trailhead.salesforce.com/content/learn/modules/business-process-mapping/understand-universal-process-notation) (multi-level "how the process works" view). Both flashcard sets key Capability Model — **flagged**. |
| 62 | Release in a Box | Salesforce — [Release in a Box](https://www.salesforce.com/resources/articles/release-in-a-box/): "prepare and present a comprehensive preview of release updates to your leadership teams, stakeholders" |
| 89 | Enable Forecast Quotas from Setup | [ExamTopics #191](https://www.examtopics.com/discussions/salesforce/view/142122-exam-certified-sales-cloud-consultant-topic-1-question-191/) — accepted set includes this option, commenter cites Salesforce Help |
| 163 | Start date within contract dates | Salesforce Help — [Guidelines for Creating Orders](https://help.salesforce.com/s/articleView?id=sales.order_create.htm&language=en_US&type=5) |
| 36 | Outbound Message + record-triggered flow | Salesforce Connect reads external data; it cannot push updates ([Work with External Data Sources](https://help.salesforce.com/s/articleView?id=sf.external_data_sources.htm&language=en_US&type=5)) |
| 148 | Developer sandbox | A sandbox carries the org's metadata; a Developer Edition or Trailhead org does not ([Salesforce sandbox guide](https://www.salesforce.com/platform/sandboxes-environments/salesforce-sandbox-guide/)) |
| 153 | Record-triggered flow | ACM doesn't support Opportunity→Account currency roll-ups ([About Advanced Currency Management](https://help.salesforce.com/s/articleView?id=sf.administration_about_advanced_currency_management.htm&language=en_US&type=5)) |

## Sources that turned out to be unreliable

- **ExamTopics vote percentages** as returned through the fetch tool were identical on every page (35/25/20) — ignored; only comment reasoning and suggested answers were used.
- **Brainscape "roy rooy Salesforce" set** gives letters only and orders options differently from our PDF, so letter matches were treated as noise; only the Set 3_78 (which includes answer text) was used for comparison.
