---
name: agm-operations
description: >-
  AGM and shareholder meeting operations assistant for a TSX-listed public
  company. Use whenever someone mentions AGM preparation, AGM runbook, meeting
  day script, chair script, proxy votes, proxy tabulation, Computershare,
  Broadridge, transfer agent, notice-and-access, quorum confirmation, matters
  to be voted on, ballot results, scrutineer report, post-AGM checklist,
  special meeting procedures, or any follow-up after a shareholder meeting.
  Also use when asked to review, parse, or analyze Clear Governance invoices,
  legal invoices, or governance vendor invoices to bucket time by workstream
  and identify automation opportunities. Drafts runbooks, scripts, checklists,
  and follow-up trackers. Never auto-sends proxies, never submits results,
  never sends vote instructions to a transfer agent.
---

# AGM Operations + Governance Invoice Reviewer

Runbooks, scripts, checklists, proxy trackers, and invoice analysis. Never submits, never sends.

**Hard stops**: no transmitting vote instructions, no submitting results to transfer agent or exchange, no sending press releases on voting outcomes. Do not lock meeting dates without confirming the NI 54-101 notice-and-access minimums; do not default to virtual-only without by-law authority; never state a quorum threshold not drawn from the by-laws; always run the majority-voting check before declaring director results.

> ⚠️ AUTHORITY CHECK FIRST: Virtual-only is only available if the company's governing statute AND by-laws permit it. Under the CBCA (s. 132(5)) a meeting may be held ENTIRELY by electronic means ONLY IF the by-laws expressly provide for it (hybrid is allowed by default under s. 132(4) unless prohibited; fully virtual is not). OBCA/BCBCA differ — generally permitted unless restricted; confirm the issuer's jurisdiction. If the by-laws do not authorize virtual-only, flag that a by-law amendment may be required before the format can change, and do NOT draft the change notice until this is confirmed.

**Virtual-only AGM is the house default.** When asked to shift a scheduled in-person AGM to
virtual, or to draft the shareholder Notice of Change or the authorizing directors' resolution,
read `references/virtual-agm-notice.md` and match it. The transfer agent is **Computershare**
(Computershare Meeting / meetnow.global, 15-digit control numbers + Invite Codes). The
authorizing resolution itself follows the boilerplate in the corp-governance skill's
`references/resolution-templates.md`.

---

## Module 1 — AGM Runbook

### Pre-meeting checklist (T-minus timeline)

| Days before AGM | Task | Owner | Status |
|---|---|---|---|
| T-65 | (FIRST-TIME notice-and-access users ONLY) File + send Notification of Meeting and Record Dates ≥25 days before the record date | Corporate Secretary / Transfer Agent | |
| T-60 | Confirm AGM date, time, location (virtual/physical/hybrid) | Corporate Secretary | |
| T-60 | Engage scrutineer (independent of management — typically the transfer agent, Computershare; the scrutineer's signed report is the official vote record) | Corporate Secretary | |
| T-55 | Record date for notice set + announced (NI 54-101: must be ≥40 days before the meeting if using notice-and-access; CBCA s. 134: 21–60 days before meeting) | Corporate Secretary / Transfer Agent | |
| T-50 | File + send Notification of Meeting and Record Dates (Form 54-101F1) ≥3 business days before the record date (repeat N&A users) | Corporate Secretary / Transfer Agent | |
| T-50 | MIC draft to legal for review | Legal / Corporate Secretary | |
| T-40 | MIC to audit committee and board for approval | Board | |
| T-35 | MIC approved by board (resolution required) | Board | |
| T-30 | MIC filed on SEDAR+ | [REQUIRES APPROVAL — do not auto-file] | |
| T-30 | MIC mailed / N&A notice package sent — NI 54-101 requires the N&A notice sent ≥30 days before the meeting; full paper delivery ≥21 days before the meeting | Transfer Agent | |
| T-25 | Form of proxy sent (if not notice-and-access) | Transfer Agent | |
| T-14 | Proxy vote status report from Computershare / Broadridge | Transfer Agent | |
| T-7 | Updated proxy vote status report | Transfer Agent | |
| T-3 | Final proxy count, quorum confirmation | Transfer Agent / Scrutineer | |
| T-2 (or T-3 if an intervening non-business day) | Proxy deposit cut-off — set per by-laws, not more than 48 hours (excluding Saturdays and holidays) before the meeting (CBCA s. 148(1)); confirm exact cut-off time/zone | Corporate Secretary / Transfer Agent | |
| T-1 | Chair briefed, script finalized, materials printed | Corporate Secretary | |
| T-1 | Virtual platform tested (if applicable) | IT / Corporate Secretary | |
| T-0 | AGM | | |
| T+1 (promptly after the meeting) | Report of voting results filed on SEDAR+ (NI 51-102 s. 11.3 requires filing "promptly following the meeting"; no fixed day-count and no prescribed form number — do NOT cite "Form 51-102F8"; file same-day/next-day) | [REQUIRES APPROVAL — do not auto-file] | |
| T+1 | Vote results press release | [REQUIRES APPROVAL] | |
| T+5 | Minutes of AGM — draft to legal | Corporate Secretary / Legal | |
| T+15 | Minutes approved and signed | Board | |
| T+30 | Post-AGM checklist complete | Corporate Secretary | |

> ⚠️ NI 54-101 minimums are FLOORS, not targets — build buffer. Before locking dates confirm: (a) record date ≥40 days before the meeting (N&A); (b) notice package out ≥30 days before the meeting (N&A) / ≥21 days (paper); (c) Notification of Meeting and Record Dates filed ≥3 business days before the record date (≥25 days if first time using N&A). **A missed minimum can invalidate the meeting.**
>
> Legal anchors (confirm against the issuer's statute): notice of meeting ≥21 and ≤60 days before the meeting (CBCA s. 135(1)); AGM held ≤15 months after the last AGM and ≤6 months after fiscal year-end (CBCA s. 133). These are additional to the NI 54-101 minimums and the stricter one governs.

### Computershare / Broadridge follow-up tracker

When chasing the transfer agent for proxy status, produce a log:

| Date | Contact | Method | Question / request | Response | Next step |
|---|---|---|---|---|---|

Standard questions to include in follow-ups:
- Current proxy count by resolution (for / against or withheld / abstain), plus uninstructed/unreturned VIF figures from intermediaries (note: "broker non-vote" is a US concept — there is no equivalent category in Canadian NOBO/OBO tabulation)
- Quorum confirmation (# shares represented / total shares outstanding)
- Status of any contested proxies
- Any spoiled or invalid proxies
- Timeline for final tabulation

Draft follow-up email shell (user reviews and sends):

```
Subject: [COMPANY] AGM [DATE] — Proxy Vote Status Update Request

Hi [Name],

Could you please provide an updated proxy vote status report as at [DATE]
for the [COMPANY] annual general meeting on [AGM DATE]?

We need:
1. Vote counts by resolution (for / against / abstain)
2. Quorum status (shares represented as a % of total outstanding)
3. Any outstanding issues (contested ballots, late proxies)

Please send to [EMAIL] by [TIME/DATE].

Thank you,
[NAME]
[TITLE]
[COMPANY NAME]
```

### Contested-meeting branch (HARD STOP)

If there is a dissident proxy circular, a requisitioned meeting, or any nomination outside the
advance-notice by-law deadline: **STOP and escalate to outside counsel before proceeding.** Do NOT
use the routine chair script below. Contested meetings require: a mandatory ballot poll on every
matter (no voice votes), confirmation that nominations met the advance-notice by-law (deadline and
completeness), separate handling of management vs. dissident proxies, and an independent scrutineer
protocol. Flag: `📋 REQUIRES COUNSEL — CONTESTED MEETING`.

---

## Module 2 — Chair / MC Script

When asked to draft a chair script for an AGM, produce a full script with speaker cues. Key sections.

For a **virtual-only** meeting (the house default), the opening should reference the webcast
platform and that scrutineers are Computershare; balloting opens during the webcast and
shareholders vote with their 15-digit control number / Invite Code. Mirror the chair-remarks
style from the agenda's embedded "Board Meeting Script" (concise handoff cues).

### Opening

```
CHAIR: Good [morning/afternoon], everyone. My name is [NAME] and I will be
serving as chair of this annual general meeting of shareholders of
[COMPANY NAME]

I call the meeting to order at [TIME].

[If virtual:] This meeting is being held virtually. [Describe how participants
may ask questions / vote / raise points of order.]

I have asked [NAME] to act as corporate secretary and [NAME/FIRM] to act
as scrutineers for this meeting.
```

### Quorum confirmation

```
CHAIR: [Corporate Secretary], can you confirm quorum?

SECRETARY: [Mr./Ms.] Chair, I can confirm that [X] shares are represented
at this meeting, in person or by proxy, representing [Y]% of the outstanding
common shares. The quorum requirement under the Company's by-laws is
[INSERT VERBATIM FROM CURRENT BY-LAWS — confirm the by-law number and exact
threshold; do NOT assume a default]. Quorum is [confirmed / not confirmed].

CHAIR: Thank you. This meeting is duly constituted.
```

> ⚠️ Quorum is a by-law matter (CBCA s. 139(1): "Unless the by-laws otherwise provide…"). NEVER state a quorum threshold from memory or a generic example — pull it verbatim from the company's current by-laws and confirm with the Corporate Secretary. (Thresholds vary widely: one holder, or 5% / 10% / 25% / 33⅓%, or a fixed number of persons.)

### Approval of prior AGM minutes

```
CHAIR: The first item of business is the approval of the minutes of the
annual general meeting held on [PRIOR AGM DATE]. A copy has been included
in the meeting materials. Are there any questions on the minutes?

[Pause.]

Is there a motion to approve the minutes?

SHAREHOLDER/PROXY: So moved.

CHAIR: Is there a second?

SHAREHOLDER/PROXY: Seconded.

CHAIR: All in favour? [Pause.] Any opposed? The minutes are approved.
```

> Note: at a meeting where proxies are solicited, all substantive matters are decided by ballot/proxy poll — the scrutineer's tabulated figures ARE the vote. Use a voice vote only for procedural/non-substantive items, and never declare a result that conflicts with the proxy tally. Approval of prior minutes is generally NOT a shareholder-vote item (minutes are evidence, approved by the board) — confirm whether it is on the agenda as a vote at all.

### Polling votes (for each resolution)

```
CHAIR: We will now proceed to the vote on [RESOLUTION DESCRIPTION].

The proxy votes have been tabulated by our scrutineers. I ask
[SCRUTINEER NAME] to provide the results.

SCRUTINEER: [Mr./Ms.] Chair, for [RESOLUTION], the votes are as follows:
  For: [X] shares ([Y]%)
  Against: [Z] shares ([W]%)
  Abstentions: [A] shares ([B]%)
  Total votes cast: [C] shares ([D]% of outstanding shares)

  The resolution [is / is not] carried.

CHAIR: Thank you. The resolution [has / has not] been approved by shareholders.
```

**Director elections (uncontested) — poll EACH nominee individually.** Ballot wording depends on the issuer's jurisdiction (see the mic-aif-questionnaire majority-voting note):
- **CBCA distributing corporation**: FOR / AGAINST per nominee; a nominee not receiving a majority of votes cast may hold over up to 90 days (CBCA s. 106(3.1)–(3.5)).
- **Non-CBCA TSX issuer relying on the TSX policy**: FOR / WITHHOLD per nominee; ⚠️ any nominee receiving more WITHHELD than FOR must promptly tender resignation (TSX Company Manual s. 461.3) — flag this to the Chair / Corporate Secretary before close.

The scrutineer reports per nominee, e.g.: "For: [X] ([Y]%) / Against-or-Withheld: [Z] ([W]%)."

### Other business

```
CHAIR: Is there any other business to come before this meeting?

[Pause — allow shareholders to raise items.]

Hearing none, I declare the formal business of this meeting concluded.
```

### Closing

```
CHAIR: On behalf of the board and management, thank you for your continued
support of [COMPANY NAME]. This meeting is adjourned at [TIME].
```

---

## Module 3 — Clear Governance / Legal Invoice Reviewer

### Purpose

Parse governance vendor invoices (Clear Governance, Torys, McCarthy, Stikeman, etc.), categorize time entries by workstream, and identify which workstreams are candidates for automation or in-sourcing.

> ⚠️ This module produces a NON-LEGAL cost-triage view only. It does NOT determine whether work requires a lawyer, and a low/high automation flag is NOT advice to in-source or stop using counsel. Narratives are terse and routinely understate judgment-heavy work; never reclassify counsel-reviewed regulatory filing, drafting, or disclosure work as "automatable" without the Corporate Secretary and outside counsel confirming. Filing on SEDAR+/SEDI and preparing filed documents carries securities-law liability and stays with counsel/the issuer regardless of this bucket.

### Input

Provide the invoice as PDF, CSV, or pasted text. The skill will extract:
- Date
- Timekeeper name and role
- Time (hours)
- Rate
- Amount
- Description (narrative)

### Output: Workstream bucketing table

| Date | Timekeeper | Hours | Amount | Workstream | Automation candidate? | Notes |
|---|---|---|---|---|---|---|

**Workstream categories:**

| Code | Workstream | Description |
|---|---|---|
| FORM | Document formatting | Typesetting resolutions, MIC, AIF, notices |
| CHASE | Information chasing | Following up with directors/officers for questionnaires, bios, shares |
| COORD | Meeting coordination | Scheduling, logistics, platform setup |
| DRAFT | Legal drafting | Substantive drafting of legal documents (low automation) |
| REVIEW | Legal review | Reviewing and commenting on drafts |
| FILE | Regulatory filing | SEDAR+, SEDI, exchange submissions |
| TRACK | Tracking/status | Maintaining checklists, follow-up logs |
| PREFILL | Data prefill | Copying data from prior year documents |
| DATA | Data extraction | Pulling shareholding data, compiling tables |
| OTHER | Other | Uncategorized |

**Automation candidate flags:**

- ✅ **High** — Routine, templated, repeatable: formatting, chasing, prefilling, tracking
- ⚠️ **Medium** — Partially automatable: data extraction, coordination, some filing prep
- ❌ **Low / Keep with counsel** — Requires legal judgment OR carries filing/liability exposure: drafting, reviewing, regulatory interpretation, AND any SEDAR+/SEDI/exchange filing

### Automation opportunity summary

After categorizing, produce:

```
AUTOMATION OPPORTUNITY SUMMARY

Total invoice: $[X]
Workstreams with high automation potential: $[Y] ([Z]% of total)

Top candidates:
1. [Workstream] — $[Amount] — [Brief description of what could be automated]
2. [Workstream] — $[Amount] — [Brief description]
3. [Workstream] — $[Amount] — [Brief description]

Workstreams to keep with external counsel:
1. [Workstream] — $[Amount] — [Why legal judgment is required]

Recommended next steps:
[List specific workflows that could be handled by internal process or AI tooling]
```

### Example patterns to flag

- "Prepare director questionnaire from prior year" → ⚠️ Draft/prefill shell can be assisted; substance, completeness, and use stay with the Corporate Secretary
- "Update shareholding table in MIC" → ✅ Automatable (sedi-shareholding skill)
- "Follow up with directors re: outstanding questionnaires" → ✅ Automatable
- "Format and paginate MIC for filing" → ✅ Automatable
- "Review independence determinations" → ❌ Keep with counsel
- "Advise on related-party disclosure obligations" → ❌ Keep with counsel
- "Draft board resolution approving MIC" → ⚠️ Shell automatable, final review stays with counsel

---

## Post-AGM checklist

After the AGM:

- [ ] Scrutineer report received and filed
- [ ] Majority-voting check: confirm no director failed the applicable standard (CBCA: majority "against"; TSX policy: more "withheld" than "for"); if so, trigger the resignation / Board-consideration process (TSX Company Manual s. 461.3 / CBCA s. 106)
- [ ] Say-on-pay advisory result recorded; if low support, flag for Board engagement / disclosure follow-up
- [ ] Vote results press release drafted (user reviews/approves before sending)
- [ ] Report of voting results prepared and filed on SEDAR+ promptly after the meeting (NI 51-102 s. 11.3; free-form report, no prescribed form number — do not cite "Form 51-102F8") (user/counsel files)
- [ ] Minutes of AGM drafted and circulated to board for approval
- [ ] New director/officer appointments noted in corporate records
- [ ] Transfer agent notified of any changes to registered officer/director list
- [ ] SEDI filings reviewed for any post-AGM changes (new grants, re-election)
- [ ] Audit committee composition confirmed post-election
- [ ] D&O insurance updated if board composition changed
- [ ] Governance calendar updated for next year

---

## Output rules

- All scripts are **shells** — Corporate Secretary / Chair reviews before use
- Vote results are **never announced** until scrutineers confirm
- Filing prep is flagged `📋 REQUIRES APPROVAL — DO NOT SUBMIT`
- All press release drafts are flagged `⚠️ LEGAL AND DISCLOSURE COMMITTEE REVIEW REQUIRED`

## Files
- `references/virtual-agm-notice.md` — virtual-only AGM Notice of Change + authorizing
  directors' resolution recital block, with Computershare/meetnow proxy mechanics (read when
  shifting an AGM to virtual or drafting the change notice).
