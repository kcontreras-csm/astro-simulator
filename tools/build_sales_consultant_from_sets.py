#!/usr/bin/env python3
"""Build sales-consultant.json from datasets/sales/set1.json … set6.json (119 questions).

Each set file is a list of {"question": "N. stem", "options": ["A. …", …], "answer": "X"}.
Keys are used exactly as given in the sets. Questions that match the previous bank
(datasets/source-snapshots/sales-consultant/sales-consultant.pre-sets.json, = git bac3b8d:sales-consultant.json)
with the same options and the same key reuse its explanation; every other question has a fresh
explanation below. Where Salesforce documentation or the previous bank points to a different answer,
the explanation states the exam key plus a note, and the item is marked review/reviewNote.

Run: python3 tools/build_sales_consultant_from_sets.py
"""
import re, json, glob
from collections import Counter
ROOT = "/Users/kcontreras/dot/sf-exam"
old = {q['id']: q for q in json.load(open(f'{ROOT}/datasets/source-snapshots/sales-consultant/sales-consultant.pre-sets.json'))}

# Same question in the previous bank (same options). Explanation is reused when the key agrees and the
# question has no entry in EXP; otherwise the id is kept as prevId only.
SAME = {2: 227, 3: 7, 7: 142, 8: 168, 10: 170, 14: 221, 16: 171, 19: 71, 26: 51, 27: 85, 30: 61, 32: 83, 33: 43, 37: 163,
        39: 68, 41: 95, 43: 73, 44: 24, 47: 153, 48: 111, 50: 183, 52: 26, 53: 69, 57: 6, 58: 117, 60: 115, 61: 99, 63: 35,
        64: 41, 66: 92, 68: 32, 69: 10, 76: 231, 77: 230, 78: 229, 79: 228, 80: 226, 81: 225, 83: 107, 84: 175, 85: 224,
        86: 223, 88: 222, 90: 93, 93: 151, 94: 70, 95: 158, 96: 129, 98: 123, 105: 156, 107: 124, 112: 155, 114: 104, 117: 66}
LETTER_FIX = {69: [("(Option A)", "(Option B)")]}   # option order differs from the previous bank

IS, CP, SL, PK, LC, AC, OM, DR, AI = ("Implementation Strategies", "Consulting Practices", "Sales Life Cycle & Forecasting",
    "Product Knowledge & Integration", "Lead & Campaign Management", "Account & Contact Management",
    "Opportunity Management", "Data, Reports & Dashboards", "Agentforce & AI")
CAT = {1: OM, 2: PK, 3: PK, 4: CP, 5: PK, 6: IS, 7: PK, 8: SL, 9: PK, 10: DR, 11: IS, 12: PK, 13: AI, 14: CP, 15: DR,
       16: LC, 17: IS, 18: DR, 19: AC, 20: IS, 21: IS, 22: AI, 23: OM, 24: PK, 25: DR, 26: DR, 27: AC, 28: AI, 29: LC, 30: DR,
       31: PK, 32: LC, 33: PK, 34: SL, 35: IS, 36: DR, 37: PK, 38: LC, 39: CP, 40: AI, 41: CP, 42: AI, 43: OM, 44: IS, 45: SL,
       46: AI, 47: PK, 48: PK, 49: OM, 50: OM, 51: DR, 52: SL, 53: LC, 54: AI, 55: IS, 56: LC, 57: SL, 58: SL, 59: PK, 60: PK,
       61: DR, 62: DR, 63: CP, 64: CP, 65: LC, 66: LC, 67: PK, 68: DR, 69: PK, 70: OM, 71: PK, 72: AI, 73: PK, 74: DR, 75: LC,
       76: DR, 77: DR, 78: PK, 79: AI, 80: IS, 81: DR, 82: IS, 83: IS, 84: PK, 85: IS, 86: AC, 87: PK, 88: AI, 89: IS, 90: LC,
       91: PK, 92: IS, 93: SL, 94: IS, 95: OM, 96: LC, 97: AC, 98: OM, 99: CP, 100: LC, 101: CP, 102: IS, 103: IS, 104: OM,
       105: AC, 106: OM, 107: DR, 108: PK, 109: OM, 110: PK, 111: PK, 112: SL, 113: PK, 114: IS, 115: IS, 116: AI, 117: DR,
       118: DR, 119: OM}

EXP = {
1: "Einstein Opportunity Scoring gives every opportunity a score for how likely it is to close and lists the positive and negative factors behind it, so reps can see why a deal ranks high or low. Collaborative Forecasting projects revenue rather than ranking deals, and In-App Guidance only displays prompts.",
5: "A product can only be added to an opportunity if it has an active entry in the opportunity's price book, so the missing products need entries in the international Price Book. Product families only group products for reporting and forecasting, and product records aren't shared to reps.",
9: "Wrapping the contact's first and last name in quotation marks makes global search treat them as an exact phrase, which cuts the results down to matching contacts. The other two options change what is shown in the results list, not what the search matches.",
11: "Scheduling the Sales Adoption Dashboard from the Adoption & Data Quality dashboard pack shows which teams and users are and aren't entering opportunities consistently, so the consultant can pinpoint where adoption breaks down before changing anything. Forcing required picklists treats the symptom and adds friction, and surveys are a follow-up once the data shows where the gaps are.",
12: "Unchecking Active on the Product record retires it: it can no longer be added to new opportunities, quotes or orders, while every existing line item and its history stays intact. A product used on opportunities can't simply be deleted, and stripping it from existing deals or deleting its price book entries would lose sales history.",
13: "Einstein's generative sales emails can only use CRM data the running user is allowed to read; when field-level security hides a field, the draft has nothing to merge and leaves a placeholder. A missing Sales Emails permission would block drafting altogether, and an unsupported locale would affect the whole email rather than individual attributes.",
15: "Deferring sharing calculations lets the admin load millions of records into a private model and merge users into the role hierarchy without a sharing recalculation on every batch; sharing is recalculated once at the end, avoiding timeouts and lock contention. Small batch sizes don't remove the recalculation, and the Data Import Wizard is limited to 50,000 records.",
17: "The Lightning Usage App's built-in metrics include page views, so admins can see the most viewed pages without installing or building anything. The Adoption Dashboards package and a custom report on Lightning Exit by Page metrics take extra setup, and exit metrics show where users leave rather than which pages they view most.",
18: "Load parents before children: Accounts first, then Contacts (which look up to Accounts), then Opportunities (which reference Accounts and their contacts). Loading children first leaves lookups unresolved and forces a second pass to associate the records.",
20: "Salesforce Trust (trust.salesforce.com) publishes each instance's scheduled maintenance windows, upgrades and incidents, so it's where the admin confirms the org won't be under maintenance during the deployment. Release Notes describe features, and System Overview shows org usage and limits.",
21: "Changes to an existing sales process are built and tested in a Developer sandbox, which carries a copy of production's metadata, and then deployed. Building in production risks disrupting live users, and a Developer Edition org has none of the org's existing configuration.",
22: "Inclusive AI starts with the training data: datasets that represent the diversity of the people the model will serve reduce the chance it underperforms or behaves unfairly for some groups. Excluding outliers can remove exactly the under-represented groups, and a large dataset isn't necessarily a representative one.",
24: "Sales Dialer lets reps make and log calls from Salesforce with click-to-dial, call notes and voicemail drop, which makes calling prospects faster and keeps every call recorded. Omni-Channel routes service work to agents, and Activity Capture syncs email and calendar data, not calls.",
28: "Einstein Sales Summaries generate a short summary of the key data on account, contact, lead and opportunity records, giving the account manager a quick snapshot before the call. Work Summaries is the Service Cloud feature that summarizes customer conversations, not sales records.",
29: "Einstein Lead Scoring uses machine learning on the org's past conversions to score every lead by how likely it is to convert, so reps can sort and work the best leads first. Lead assignment rules route leads without ranking them, and Campaign Influence attributes revenue to campaigns.",
31: "Reduction orders are the Salesforce Orders feature for returns and quantity reductions: once enabled, a reduction order is created against an activated order to reduce or return its products while the original order stays intact. Orders with negative amounts aren't supported, and optional price books are unrelated to returns.",
35: "Training built around the users' real business scenarios shows each role how the customized solution supports the work they actually do, which is what makes training stick for a heavily customized org. Generic Trailhead modules don't cover custom functionality, and a single modality ignores different roles and learning styles.",
38: "A custom matching rule only finds duplicates once it's activated and used by an active duplicate rule, so the first check is whether the custom lead matching rule is active. The standard lead matching rule's criteria can't be edited, and making Email required doesn't detect duplicates.",
45: "An opportunity's forecast category comes from its stage, through the Stage-to-Forecast Category mapping on the Opportunity Stage picklist values. When opportunities land in the wrong category after a rollout, checking those mappings for the new business unit's stages is the quickest fix. The forecast hierarchy decides whose forecast an opportunity rolls into, not its category, and requiring the field doesn't fix the mapping.",
46: "If the model is fed societal data that carries regional patterns, its output can suit some regions better than others, which shows up as uneven satisfaction. That is a bias problem in the data, not a matter of how much users review content or how much automation each region has.",
49: "Revenue schedules on the opportunity's products split each product's revenue into installments over the payment term (for example monthly over 12, 24 or 36 months starting in the month of sale), which gives finance a forecastable revenue timeline. Price books don't hold payment schedules, and a custom installment object rebuilds what schedules already provide.",
51: "A reporting snapshot copies the results of an Opportunity report into a custom object on a schedule, building month-by-month history of closed deals that can be compared over time. A dashboard refresh only shows the current state, and Opportunity History tracks field changes rather than monthly totals.",
54: "Transparency, being clear about when AI is used and how it reaches its outputs, is a core Salesforce trusted-AI practice and lets users judge when to rely on it. Reducing human oversight increases risk, and encrypting outputs is a security measure rather than an ethical practice.",
56: "Handing prospects to sales means sales needs them as Leads it can qualify, assign and convert, so the integration should create Lead records in Sales Cloud. Tasks carrying lead details can't be scored, routed or converted, and an AppExchange package is only one way to build an integration, not the design decision itself.",
59: "Einstein Activity Capture connects to reps' Google (Gmail and Google Calendar) or Microsoft accounts and automatically adds their emails and events to the activity timeline of related records. Email to Salesforce only logs emails reps BCC or forward one at a time, and an AppExchange app adds cost for something Sales Cloud already includes.",
62: "With multiple currencies enabled, Salesforce displays amounts in the record's currency followed by the converted amount in parentheses, so the team can read Australian deals in USD without extra configuration. Reports aren't limited to the user's default currency, and a currency formula field duplicates the built-in conversion.",
67: "Einstein Activity Capture automatically syncs reps' emails and calendar events into Salesforce and provides activity metrics, giving the VP visibility with no manual logging. Email Insights and an inbox view surface information to the rep but don't capture activity for managers.",
70: "Einstein Opportunity Scoring learns from the org's past won and lost deals and scores each open opportunity on its likelihood to close, so reps can drop low-probability deals and focus on winnable ones. Einstein Lead Scoring scores leads, not opportunities, and Calculated Insights are Data Cloud metrics, not deal predictions.",
72: "Safety in Salesforce's guidelines for responsible generative AI means mitigating bias, toxicity and harmful output, for example with toxicity detection, testing and guardrails. Transparency is about disclosing AI use and explaining outputs, and Empowerment is about AI supporting people's work.",
73: "Call Explorer, part of Einstein Conversation Insights, analyzes recorded voice and video calls so users can find competitor mentions, coaching moments and other key information across calls. Call Summaries summarize a single call, and Einstein Sales Insights isn't the call-analysis tool.",
74: "Before syncing the customer list from back-office systems, the Account object needs an External ID field holding each system's customer key, so the integration can upsert and match records reliably without creating duplicates. A matching rule only flags duplicates, and an ID on Opportunity doesn't identify customers.",
75: "Customizable Campaign Influence attributes an opportunity's revenue across all the campaigns that touched it, using standard or custom attribution models, which is what a multi-touch buying journey needs. Primary Campaign Source credits a single campaign, and a custom junction object rebuilds what Campaign Influence already provides.",
82: "For a complex release going to a large, globally distributed workforce, train-the-trainer scales: local trainers learn the release in depth and then train their own offices in their language and time zone. Trailhead and documentation alone don't ensure a complex release is understood, and Path is a configuration feature, not a training approach.",
87: "When multiple currencies are enabled (without dated exchange rates), changing a conversion rate recalculates the converted amounts on all records, closed opportunities included. Existing records are given the corporate currency automatically during enablement, and many objects besides Opportunities and Leads support currencies.",
89: "Logins only show that users signed in; opportunities modified in the last 30 days show reps are actually working their pipeline in Salesforce, which makes it the stronger companion adoption metric. Web-to-Lead submissions measure marketing volume, and creating products is an admin task.",
91: "Sales Engagement provides work queues and cadences that present the next lead automatically, with calling, notes, voicemail drop and call-back steps, and with conversation insights supervisors can coach from call transcripts. Sales Cloud alone doesn't automate the call queue, and a CTI connector only adds telephony.",
92: "When a deployment falls on a Salesforce release weekend, the safe practice is to move the deployment, update the project plan and communicate the change, since the instance may be under maintenance and the release can affect what was tested. Deploying during the release adds avoidable risk, and announcing that it will fail isn't a plan.",
99: "Scope creep is controlled with a formal change management process: every new request is reviewed for its impact on timeline, cost and resources and approved before it's built. Locking scope outright ignores legitimate business needs, and adding developers doesn't stop uncontrolled requests.",
100: "A schedule-triggered flow runs on a set schedule (for example nightly) against the leads that meet its criteria, such as still open and created more than 90 days ago, and deletes them. An autolaunched flow needs something else to start it, and Omni-Channel flows route work items.",
101: "In Agile, requirements are captured as user stories (\"As a sales manager, I want … so that …\"), which the team estimates and delivers in sprints. Epics are large bodies of work broken down into stories, and sprints are time-boxes, not requirements.",
103: "A change that relies on functionality from a newer Salesforce version can't be deployed to an org still on the older version, so the fix is deployed once both environments are on the same release. Deploying before or during the upgrade window fails or puts production at risk.",
104: "Schedules are a product feature: once quantity and revenue schedules are enabled in Product Schedules Settings and on the subscription product, each opportunity product can carry a one-time, monthly, quarterly or annual schedule. Schedules aren't enabled on the Opportunity or Order object.",
106: "Opportunity Teams let each rep add the specific users who should work a given opportunity, with Read/Write access to that opportunity, and team membership can be reported on per opportunity. Account Teams or account sharing would open every opportunity on the account to the same people, and Modify All goes far beyond what's needed.",
108: "With multiple currencies (and no dated exchange rates), changing a rate updates the converted amounts on all opportunities, open and closed, as well as new ones. Closed opportunities keep their historical rate only under Advanced Currency Management, and rate changes aren't recorded in Opportunity Field History.",
109: "Opportunity Team access is granted per opportunity, so removing the user's Opportunity Team member record from that opportunity revokes their access right away. Changing default opportunity teams only affects future opportunities, and a flow is unnecessary for an ad hoc removal.",
110: "Einstein Activity Capture Standard is included with Sales Cloud and connects reps' email and calendar accounts so recent emails and events appear on Salesforce activity timelines, which fits 75 reps who need about the last two months of email. Email to Salesforce only logs emails reps forward or BCC, and Sales Cloud Einstein is a paid add-on beyond this need.",
111: "Salesforce Connect exposes the ERP's order data as an external object that can be shown as a related list on Account and is read live from the ERP rather than copied into Salesforce. A custom object needs a batch load and is stale between syncs, and a report can't show data that isn't in Salesforce.",
113: "Call Explorer is part of Einstein Conversation Insights, so users need the Einstein Conversation Insights permission set (with ECI enabled and call recordings connected) before they can use it. It doesn't need custom actions built first, and its setup has nothing to do with Salesforce Knowledge.",
115: "A Center of Excellence brings together business owners, admins and executive sponsors to govern the platform, prioritize enhancements and share best practices, which is how continuous improvement is sustained after go-live. An enablement site or a CI/CD pipeline are tools a COE might use, not the culture-building structure itself.",
116: "The model underperforms for people whose cultural and language nuances weren't well represented, which falls under the Inclusive principle: AI should be trained and tested on diverse, representative data so it serves everyone it affects. Responsible and Empowering cover other parts of Salesforce's trusted AI principles.",
119: "Opportunity Splits, enabled from Setup, let team members share credit for an opportunity's revenue (revenue splits that total 100%, or overlay splits for supporting roles), and the splits roll into reports and forecasts. A custom field or child opportunities would need custom logic and break forecasting.",
# ---- contested: key kept as given in the sets; explanation states it and adds a note ----
4: "Exam key: the ERP admin, who owns the system of record and knows how it accepts customer and opportunity updates. Note: designing an immediate update from Salesforce to the ERP is integration design, and the previous bank's version of this question keyed the integration architect; in practice both roles are involved.",
6: "Exam key as printed: Deployment. Note: business users testing newly configured functionality before release is User Acceptance Testing (UAT), which comes before deployment and go-live; the previous bank keyed UAT for this question.",
8: "Exam key: schedule the auto-assignment rules in the territory model. Note: Salesforce documentation assigns territories to opportunities in bulk with filter-based opportunity territory assignment, which runs an Apex filter class against opportunities; territory assignment rules assign accounts, not opportunities. The previous bank keyed the filter-based option.",
23: "Exam key: build an Opportunities with Opportunity Teams report and use a summary formula to calculate the support reps' 15%. Note: Salesforce's built-in way to credit supporting team members is Opportunity Splits with an overlay split type, which doesn't have to total 100%; a report formula only displays a number and doesn't record the credit.",
25: "Exam key: update the account sharing rule to use a public group. Note: 290,000 contacts under one account is account data skew, which causes record locking and slow sharing recalculation. Salesforce's guidance is to keep each account under 10,000 child records by spreading them across more accounts (290,000 ÷ 30 is just under 10,000, hence \"at least 30 accounts\"). The previous bank's variant keyed redistributing the contacts.",
27: "Exam key: index the fields shown in the invoice related list and train users. Note: the slow load comes from rendering a related list with millions of child rows; moving it to a separate tab on the record page defers that load until a user opens the tab, which is what the previous bank keyed. Indexing speeds up filtered queries but doesn't reduce what the page renders.",
30: "Exam key: a joined report with blocks for closed opportunities, Forecasting Items and Quotas, which puts forecast amounts by product family next to team quotas. Forecasting Items and Forecasting Quotas are separate objects, so they're typically reported side by side in joined-report blocks. Note: the previous bank's version of this question keyed a custom report type with Forecasting Quotas and Forecasting Items.",
34: "Exam key: simplify the role hierarchy by moving managers into the forecast hierarchy. Note: Collaborative Forecasts handles roles with several users by having the admin choose the forecast manager for each role in the forecast hierarchy (Setup > Forecasts Hierarchy), with no change to the role hierarchy; that is the \"Assign the manager in the forecast hierarchy\" option.",
36: "Exam key: to activate customizable sales forecasting and lead scoring. Note: Data Cloud's core value is unifying customer data from every source into trusted profiles and then using segments and calculated insights, such as customer lifetime value, to drive targeted processes, which is closer to the customer-lifetime-value option. The previous bank's version (with different options) keyed creating customer segments with personas and scoring.",
37: "Exam key: a cloned order must have a later end date than the associated contract. Note: Salesforce Help's order guidelines say an order's start date must fall within the associated contract's start and end dates, which is the rule a cloned order must also meet; the clone doesn't have to use the same contract. The previous bank keyed the start-date option.",
39: "Exam key: confirm that the statement of work (SOW) is realistic, since deadlines that are consistently missed may have been set too aggressively. Note: missed deadlines together with missed meetings also point to a communication breakdown, and the previous bank keyed revisiting the communication plan with more frequent check-ins.",
40: "Exam key: usage has exceeded the 2,000-emails-per-hour limit, so Draft with Einstein is unavailable and users see an error until usage falls back under the limit. Note: the previous bank's variant of this question keyed an invalid recipient email address, and the hourly limit wasn't confirmed against current Salesforce documentation.",
42: "Exam key as printed: Optimize for Clarity. Note: Einstein's sales-email refinements include tone adjustments such as Make Less Formal, which is the one that gives a draft a more casual tone; clarity edits improve readability without changing tone. The previous bank's variant keyed the less-formal tone adjustment.",
43: "Exam key: change the stage on the opportunity. Probability is driven by stage, so the stage decides when a deal crosses 75%. Note: changing a stage doesn't send any email; the documented solution is a record-triggered flow with an email alert when Amount ≥ 100,000 and Probability ≥ 75% (Opportunity Big Deal Alerts serve the same purpose). The previous bank keyed the flow.",
50: "Exam key: the opportunity is implicitly Write for the team. Note: Opportunity Team members get explicit Read Only or Read/Write access to the opportunity, set per member, and implicit (parent) sharing gives them Read access to the opportunity's Account even when Account OWD is Private. The previous bank keyed the Account option.",
52: "Exam key: build reports and dashboards that compare the existing and new territories. Note: Sales Territories already supports this: with the model in the Planning state, sales operations can run the updated assignment rules and review the resulting accounts on each territory's detail page before activating, without affecting users. The previous bank keyed that option.",
55: "Exam key: combining the territory changes with the incentive management package increases downtime and ramp-up time for users just as they're focused on the year-end close. Note: the previous bank's variant keyed the deployment-risk option; both options argue against releasing the two changes together near quarter end.",
63: "Exam key: Value Stream Map. Note: Trailhead's business process mapping content describes a Capability Model as the diagram of the high-level processes within a business, used to show a process's context within the overall business, which matches this stem almost word for word. A value stream map follows one end-to-end flow of value. The previous bank keyed Capability Model.",
64: "Exam key: establish KPIs for end users, since agreeing on measurable outcomes during Discovery shows which capabilities are needed to move them. Note: the previous bank keyed observing end users, which reveals how work is actually done; both are Discovery techniques.",
65: "Exam key: assign the Einstein Lead Scoring permission set, because users without Einstein Lead Scoring access can't see scores. Note: the stem says Sales Cloud Einstein was already rolled out to the pilot users, so the more likely gap is that the Lead Score field (or the Einstein scoring component) isn't on the Lead page layout or record page; the previous bank's variant keyed adding the field to the page layout.",
71: "Exam key: delete the Product record. Note: this contradicts Q12 in the same set. A product that appears on opportunities, quotes or orders can't be deleted, and deleting would lose history; the documented way to make a discontinued product unavailable is to uncheck Active (or, of the options here, remove its price book entries). The previous bank's variant keyed removing it from all price books.",
93: "Exam key: multiple forecast types must be created and activated. Note: different sales stages per product line still map to the same forecast categories, so one opportunity forecast type covers every line. What every Collaborative Forecasts rollout does require is choosing Single Category or Cumulative Forecast Rollups, which the previous bank keyed.",
97: "Exam key: distribute the records equally across the roles in the role hierarchy, which spreads out the ownership skew. Note: Salesforce's ownership-skew guidance is to spread records across more owners or, if one user must own more than 10,000 records, to give that user no role (or a role of their own at the top of the hierarchy) so sharing changes don't recalculate through the hierarchy. That makes removing the user from the role hierarchy the documented option; moving them to the bottom makes it worse.",
102: "Exam key: validate data completeness and accuracy so data stays clean as volume grows. Note: for performance at higher data volumes and user activity, Salesforce's scalability guidance centres on the data model (relationships, skew, indexing, archiving) and on efficient automation; the previous bank's variant keyed evaluating and optimizing the data model and automations.",
114: "Exam key: build the issue-resolution release in the staging environment. Note: fixes normally follow the standard path of building in a development sandbox, testing in staging/UAT and then deploying to production; the previous bank keyed the development-sandbox option. UAT doesn't belong in a development sandbox.",
117: "Exam key: settle the role hierarchy and sharing rules before migrating, so incoming records land with the right owners and visibility and sharing doesn't have to be recalculated afterwards. Note: the previous bank keyed identifying the volume of customer, partner and prospect data first, because data volume drives the migration approach and tooling.",
118: "Exam key: opportunities missing Price Book information. Note: the usual sign that an opportunity is at risk is a lack of activity, since deals reps aren't working tend to stall; the previous bank's variant keyed opportunities with no recorded activities. Missing price book data is a data-quality gap rather than a deal-risk signal.",
}
WRONG = "Key appears incorrect: "
TAKEN = "Key taken from the sales sets; "
REVIEW = {
4: TAKEN + "the previous bank's variant (Q249) keyed \"Integration architect\".",
6: WRONG + "the scenario describes User Acceptance Testing (UAT). The previous bank's variant (Q251) keyed UAT.",
8: TAKEN + "the previous bank (Q168) keyed \"Run the filter-based Opportunity territory assignment\", which matches Salesforce documentation.",
23: "Contested: Opportunity Splits (overlay split) is the documented feature for crediting supporting team members.",
25: WRONG + "Salesforce's data-skew guidance points to splitting the contacts across ~30 accounts (under 10,000 each). The previous bank's variant (Q269) keyed redistributing the contacts.",
27: TAKEN + "the previous bank (Q85) keyed \"Move the invoice related list to a separate tab\".",
30: TAKEN + "the previous bank (Q61) keyed \"Create a custom report type with Forecasting Quotas and Forecasting Items\".",
34: WRONG + "Salesforce designates one forecast manager per role in the forecast hierarchy. The previous bank's variant (Q278) keyed that option.",
36: "Contested: Data Cloud is about unified profiles, segments and calculated insights (e.g. customer lifetime value). The previous bank (Q49, different options) keyed customer segments.",
37: WRONG + "Salesforce Help requires the order start date to fall within the contract dates. The previous bank (Q163) keyed that option.",
39: TAKEN + "the previous bank (Q68) keyed \"Revisit the communication plan and set up more frequent check-ins\".",
40: TAKEN + "the previous bank's variant (Q281) keyed an invalid email address. The hourly limit wasn't verified against current documentation.",
42: WRONG + "\"Make Less Formal\" is the tone adjustment that makes a draft more casual. The previous bank's variant (Q282) keyed it.",
43: WRONG + "only the flow with an email alert actually notifies the VP. The previous bank (Q73) keyed that option.",
50: WRONG + "implicit sharing gives team members Read on the parent Account; opportunity access is set explicitly per member. The previous bank (Q183) keyed the Account option.",
52: TAKEN + "the previous bank (Q26) keyed running the assignment rules in the Planning State, which matches Salesforce documentation.",
55: TAKEN + "the previous bank's variant (Q293) keyed the deployment-risk option.",
63: WRONG + "Trailhead defines the Capability Model with this stem's wording. The previous bank (Q35) keyed Capability Model.",
64: TAKEN + "the previous bank (Q41) keyed \"Observe end users\".",
65: TAKEN + "the previous bank's variant (Q300) keyed adding the Lead Score field to the page layout.",
71: WRONG + "it contradicts Q12 (uncheck Active). The previous bank's variant (Q236) keyed removing the product from all price books.",
93: WRONG + "different stages map to forecast categories, so multiple forecast types aren't required. The previous bank (Q151) keyed the rollup option.",
97: "Contested: Salesforce's ownership-skew guidance points to removing the user from the role hierarchy (or giving them a top-level role of their own). The previous bank's variant (Q214) keyed a lower role.",
102: TAKEN + "the previous bank's variant (Q208) keyed \"Evaluate and optimize data model and automations\".",
114: TAKEN + "the previous bank (Q104) keyed \"Build out the issue resolution release in a development sandbox\".",
117: TAKEN + "the previous bank (Q66) keyed \"Volume of customer, partner, and prospect data\".",
118: "Contested: opportunities with no activity is the usual at-risk metric. The previous bank's variant (Q243) keyed it.",
}

def clean(s):
    for a, b in [("marketingdata", "marketing data"), ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"')]:
        s = s.replace(a, b)
    s = re.sub(r'\bAl\b', 'AI', s)
    return re.sub(r'\s+', ' ', s).strip()

bank = []; reused = fresh = 0
for path in sorted(glob.glob(f'{ROOT}/datasets/sales/set*.json')):
    src = path.split('/')[-1]
    for raw in json.load(open(path)):
        m = re.match(r'(\d+)\.\s*(.*)', raw['question'], re.S)
        num, text = int(m.group(1)), m.group(2)
        opts = [re.match(r'([A-D])\.\s*(.*)', o, re.S).groups() for o in raw['options']]
        if num in EXP:
            exp = EXP[num]; fresh += 1
        else:
            exp = old[SAME[num]]['explanation']; reused += 1
            for a, b in LETTER_FIX.get(num, []):
                assert a in exp, num
                exp = exp.replace(a, b)
        item = {"id": num, "category": CAT[num], "text": clean(text),
                "options": [{"letter": L, "text": clean(t)} for L, t in opts],
                "answer": [raw['answer']], "multi": False, "explanation": exp, "sourceRef": f"{src} Q{num}"}
        if num in SAME: item['prevId'] = SAME[num]
        if num in REVIEW: item['review'] = True; item['reviewNote'] = REVIEW[num]
        bank.append(item)

bank.sort(key=lambda q: q['id'])
assert [q['id'] for q in bank] == list(range(1, len(bank) + 1))
assert set(EXP) | set(SAME) >= {q['id'] for q in bank} and set(REVIEW) <= set(EXP)
for q in bank:
    L = [o['letter'] for o in q['options']]
    assert q['answer'][0] in L and len(q['explanation']) > 60 and len(q['options']) >= 2, q['id']
json.dump(bank, open(f'{ROOT}/sales-consultant.json', 'w'), indent=1, ensure_ascii=False)
print('bank', len(bank), '| explanations reused', reused, 'fresh', fresh, '| review-marked', sum(1 for q in bank if q.get('review')))
print(json.dumps(Counter(q['category'] for q in bank), indent=1))
