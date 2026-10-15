#!/usr/bin/env python3
"""Rebuild agentforce.json from datasets/source-snapshots/agentforce/download.pdf (image-only PDF).

Pipeline (run once, outputs cached under the scratch dir given as argv[1]):
  pdftoppm -r 200 -png download.pdf p        -> page PNGs
  tesseract p-NN.png p-NN --psm 4 -l eng     -> per-page OCR text, concatenated with "===== PAGE NN" markers
  af2_parsed.json  : parsed questions (num, page, text, options, letters, answer)
  af2_match.json   : best match of each PDF question against the previous bank (prevId, key agreement)

This script consumes those two JSON files plus the previous bank
(agentforce.pre-download-pdf.json) and writes agentforce.json with the PDF's keys.
"""
import re, json, sys, html
from collections import Counter
S = sys.argv[1]
ROOT = "/Users/kcontreras/dot/sf-exam"
qs = {q['num']: q for q in json.load(open(f'{S}/af2_parsed.json'))}
match = {m['num']: m for m in json.load(open(f'{S}/af2_match.json'))}
old = {q['id']: q for q in json.load(open(f'{ROOT}/datasets/source-snapshots/agentforce/agentforce.pre-download-pdf.json'))}
DROP = {28, 8, 131, 97, 57, 95, 112, 130}                 # identical duplicates in the PDF (same key) — later copy dropped
CONFLICT = {10: 119, 119: 10, 21: 92, 92: 21}             # same stem, different key inside the PDF — both kept, flagged
FORCE_AGREE = {20, 34}                                    # long answer text; matcher misread as disagreement
REUSE_OLD = {123: 37, 129: 81}                             # reworded copies of previous-bank questions (same key) — reuse their explanation
CAT_NEW = {9: "Agentforce & Data", 10: "Prompt Engineering", 119: "Prompt Engineering", 17: "Trust Layer & Security", 45: "Agentforce Concepts",
           68: "Agentforce Concepts", 70: "Setup & Integration", 79: "Agentforce & Data", 80: "Prompt Engineering", 82: "Agentforce Concepts",
           83: "Setup & Integration", 91: "Agentforce Concepts", 101: "Trust Layer & Security", 123: "Agentforce Concepts", 129: "Setup & Integration"}
EXP = {
9: "An Agentforce Data Library accepts file uploads directly: create the library, upload the policy PDFs, and the platform handles the ingestion, chunking and indexing in Data 360 behind the scenes. That grounds the agent exclusively in the approved documents with the least manual setup. Option B is the manual Data 360 route the library automates, and Option A isn't a grounding mechanism.",
10: "A Flex prompt template accepts several unrelated records as inputs — the opportunity products, the nearby events and the tone/voice examples — so all three can be referenced as resources in one email prompt. Note: this PDF asks the same question again as Q119 and keys the prompt-initiated flow there; both mechanisms exist, and a Flex template is the direct way to take multiple record inputs.",
119: "A template-triggered (prompt-initiated) flow can fetch related items at run time — the opportunity's products, events near the customer and tone examples — and pass them back to the prompt template with Add Prompt Instructions. Note: the same question appears as Q10 in this PDF keyed to a Flex template; both approaches are valid, and a Flex template is the more direct answer when the records are simply supplied as inputs.",
17: "The Einstein Service Agent user runs the flow under its own permissions, so under a Private OWD it sees nothing. Least privilege means granting that user exactly what it needs — object permissions in its permission set plus sharing rules for the relevant opportunities. Running the flow in system mode without sharing (B) or opening the OWD (C) exposes far more data than required.",
45: "Misrouting between subagents is usually semantic competition — two subagents whose descriptions and instructions overlap so the planner can't discriminate. Auditing and tightening the subagent instructions, and adding deterministic filters (guard conditions / available-when logic) for clear cases like billing, fixes routing quickly while keeping the LLM free to handle non-linear conversations. Forbidden-keyword lists (A) are brittle, and a manual router flow (C) removes the flexibility the manager wants to keep.",
68: "In Agent Script an action's description is what the LLM reads to decide whether and when to invoke the action; the label is only a display name and the target points at the implementation. A vague or overlapping description is the usual reason the right subagent is chosen but the wrong action is picked.",
70: "Agentforce Service Agent on the Email channel sends its replies through a Lightning email template that defines the structure of every outbound email, which the specialist connects to the agent's email configuration. Classic templates aren't supported for the agent, and Draft Email Template is not the mechanism for the agent's own replies. Note: earlier prep sources key the Email Configuration step for this scenario.",
79: "Since every policy version must stay indexed, the fix is scoping retrieval rather than deleting data: a custom retriever with a dynamic filter on the policy-version metadata, populated at run time from the customer's Contract record, restricts the search to the correct version before similarity ranking. Tagging chunks and hoping the LLM picks the right version (B) isn't reliable, and one data stream per version (C) is unnecessary duplication.",
80: "Exam key: expose the ERP order status as an external object through Salesforce Connect and reference it with External Object record merge fields, which reads the current value at prompt time. Note: Salesforce guidance also supports an Apex resource for real-time callouts, and earlier prep sources key Apex merge fields for this scenario.",
82: "Hybrid reasoning in Agent Script mixes declarative natural-language instructions, which the LLM interprets flexibly, with procedural instructions prefixed by run, which execute deterministically in order — so identity verification can be guaranteed before account data is touched while the rest of the conversation stays fluid. It doesn't involve multiple LLMs (A) or a split between Canvas and Script views (B).",
83: "Agentforce Testing Center can generate test cases automatically from the knowledge available to the agent — here the 200 FAQ articles in the data library — producing a broad initial suite without manual authoring. Generating from subagents and actions (C) targets action selection rather than knowledge coverage, and uploading test cases (A) still requires writing them.",
91: "The Lead Nurturing Agent (the successor to the SDR Agent) autonomously engages inbound leads around the clock, answers their questions from approved knowledge, and books meetings with qualified prospects, handing reps a warm pipeline. Marketing Agent focuses on campaign work, and Pipeline Management is not an agent.",
101: "Agentforce Session Tracing records every turn of an agent conversation — the reasoning engine's plan, each action with its inputs and outputs, and any errors — which is exactly the auditable trail a regulated industry needs. Agentforce Optimization aggregates and scores sessions to find improvement areas, and Utterance Analysis clusters what users asked.",
3: "Exam key: connecting a Service Agent to a Digital Experience (Experience Cloud) site for Messaging for In-App and Web means placing the messaging Lightning web component on the site, configured with the standard or custom Lightning Type for Agentforce so the pre-chat membership variable is passed to the agent. MuleSoft isn't involved, and while an Omni-Channel flow routes work to the agent, it isn't the site-connection step.",
11: "Exam key: within Agent Script, the run keyword chains a follow-up action so send_verification executes immediately after create_account succeeds, with no extra user turn. Making the action merely available (B) leaves invocation to the LLM. Note: Salesforce documentation places run statements in the procedural (reasoning) instructions, so the previous bank keyed Option A; both exam sources key the run keyword.",
21: "Exam key as printed: Option A. Note: this PDF asks the same question again as Q92 and keys Option B there, and Salesforce's prompt-engineering guidance for reliable extraction is clear, positive instructions with few-shot examples (B) — open-ended questions invite variable output, and high temperature increases randomness.",
23: "Prompt templates reference the model by its API name; if the custom LLM's API name in production doesn't match the one used in the sandbox, the change set deployment fails. Marking the prompt as custom or deactivating the template doesn't resolve the reference.",
43: "Exam key: after choosing a related list resource for the Account, use the field picker in Prompt Builder to select the merge fields you want in the prompt. Note: Salesforce documentation states the fields exposed for a related list come from the object's page layout for the running user (Option C), which is why earlier bank versions keyed C.",
67: "Prompt Builder is for generative text grounded in CRM data, so drafting a quote proposal in reply to a request for quote is a natural fit. Forecasting trends and scoring leads are predictive use cases handled by Einstein predictions, not prompts.",
73: "Exam key: Option A. Note: in Agent Script the documented way to guarantee that an action runs before the LLM reasons is the before_reasoning block of the subagent, and the first line of reasoning instructions is interpreted by the LLM rather than guaranteed; treat this key as the source's reading.",
77: "Exam key: enable the Answer Questions with Knowledge standard action on the General FAQ subagent, which is the action through which the agent answers factual questions and can be configured to draw on web search results. Replacing the subagent (C) or mapping a retriever to a search index (B) isn't required.",
81: "Agentforce Testing Center runs batches of real-world utterances against the agent and reports which subagent and action were selected for each, which is the way to validate action selection before activation. Agentforce Builder's preview tests one utterance at a time, and Prompt Builder is for prompt templates.",
94: "Exam key: Agent Inspection. Note: the current Agentforce Observability feature that lets you follow an interaction from the first request to resolution is Session Tracing (surfaced through Agent Optimization); earlier bank versions keyed Agent Insights. This item is contested across sources.",
109: "Exam key: an ensemble retriever that stitches related chunks back together at retrieval time restores the context of a table that was split across chunks. Note: Salesforce also documents switching the search index's parser to Docling, which preserves table structure at ingestion; the previous bank keyed that option.",
}
EXP[8] = EXP[3]
def clean(s):
    s = html.unescape(s)
    for a, b in [("Agenttorce", "Agentforce"), ("turn-by-tum", "turn-by-turn"), ("by-tum", "by-turn"), (" tum ", " turn "), ("$24/7$", "24/7"), ("claims- related", "claims-related"),
                 ("compliance- regulated", "compliance-regulated"), ("Docking", "Docling"), ("Al_Analysis_c", "AI_Analysis__c"),
                 ("@variables. |IsActive", "@variables.IsActive"), (" ot the ", " of the "), (" Is deploying ", " is deploying "),
                 (" Its support ", " its support "), ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"')]:
        s = s.replace(a, b)
    s = re.sub(r'\bAl\b', 'AI', s)
    return re.sub(r'\s+', ' ', s).strip()
bank = []; nid = 0; reused = fresh = 0
for num in sorted(qs):
    if num in DROP: continue
    q = qs[num]; nid += 1; m = match[num]
    agree = bool(m.get('bank')) and (m.get('same') or num in FORCE_AGREE)
    if agree and num not in EXP:
        ob = old[m['bank']]; cat = ob['category']; exp = ob['explanation']; reused += 1
    else:
        cat = old[m['bank']]['category'] if m.get('bank') else CAT_NEW[num]
        if num in REUSE_OLD and num not in EXP: exp = old[REUSE_OLD[num]]['explanation']; item_prev = REUSE_OLD[num]; reused += 1
        else: exp = EXP[num]; fresh += 1
    item = {"id": nid, "category": cat, "text": clean(q['text']),
            "options": [{"letter": L, "text": clean(o)} for L, o in zip(q['letters'], q['options'])],
            "answer": [q['answer']], "multi": False, "explanation": exp, "sourceRef": f"download.pdf Q{num} (p{q['page']})"}
    if m.get('bank'): item['prevId'] = m['bank']
    elif num in REUSE_OLD: item['prevId'] = REUSE_OLD[num]
    notes = []
    if m.get('bank') and not agree: notes.append(f"Key taken from download.pdf; the previous bank (Q{m['bank']}) keyed a different answer — see the note in the explanation.")
    if num in CONFLICT: notes.append(f"The PDF contains this question twice (Q{num} and Q{CONFLICT[num]}) with different keys.")
    if num == 38: notes.append("The PDF prints only two options for this question.")
    if notes: item['review'] = True; item['reviewNote'] = ' '.join(notes)
    bank.append(item)
for q in bank:
    L = [o['letter'] for o in q['options']]; assert q['answer'][0] in L and len(q['explanation']) > 60 and len(q['options']) >= 2, q['id']
json.dump(bank, open(f'{ROOT}/agentforce.json', 'w'), indent=1, ensure_ascii=False)
print('bank', len(bank), '| explanations reused', reused, 'fresh', fresh, '| review-marked', sum(1 for q in bank if q.get('review')))
print(json.dumps(Counter(q['category'] for q in bank), indent=1))
print('option counts', dict(Counter(len(q['options']) for q in bank)))
print('leftover OCR suspects:', [(q['id'], w) for q in bank for w in re.findall(r'\b(?:Cc|ot|Al|tum|Agenttorce)\b', q['text'] + ' '.join(o['text'] for o in q['options']))][:10])
