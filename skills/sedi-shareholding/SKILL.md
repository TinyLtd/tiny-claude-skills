---
name: sedi-shareholding
description: >-
  SEDI and shareholding discrepancy checker for a TSX-listed public company.
  Use whenever someone mentions SEDI, insider reports, insider filings, early
  warning reports, beneficial ownership, deferred share units (DSUs), options,
  RSUs, share register, shareholding comparison, beneficial ownership table,
  10% threshold, reporting insider, director share ownership, officer share
  ownership, or needs to reconcile questionnaire-reported holdings against SEDI
  records or a share register. Compares data sources, flags discrepancies,
  produces a reconciliation table. Never auto-files SEDI reports, never makes
  the legal determination of whether someone is a reporting insider, never sends
  anything to regulators.
---

# SEDI / Shareholding Checker

Compare, reconcile, and flag. Never auto-file. Never make the legal call on insider status.

**Hard stops**: no SEDI filing automation, no submissions to regulators, no determination that someone is or is not a reporting insider.

---

## Data sources this skill works with

| Source | What it contains | Format |
|---|---|---|
| **Director/Officer Questionnaire** | Self-reported share counts, DSUs, options, warrants | Text or structured table |
| **SEDI public filings** | Filed insider reports (you paste the data in or upload CSV) | Pasted text / CSV |
| **Share register (Computershare/TSX Trust)** | Registered share counts by account | CSV or pasted table |
| **Prior year MIC / AIF** | Prior year holdings table | PDF or text |
| **Stock option register** | Option grants, exercise prices, expiry dates, vesting | Spreadsheet |
| **DSU register** | DSU grants and balances | Spreadsheet |

---

## Comparison workflow

### Step 1 — Collect data

Ask the user to provide (any or all of):
1. Completed questionnaire holdings section (paste text or upload)
2. SEDI data — as of 2026-06, insider reports are still filed and searched on **sedi.ca**; SEDAR+ has NOT yet absorbed SEDI (CSA "Phase 2" SEDI migration is announced but undated). BEFORE relying on this, confirm the current insider-reporting system at osc.ca/sedi or securities-administrators.ca, because the destination changes on SEDAR+ Phase 2 launch. (Instruct: go to the current system → Issuer → [Company] → Insider Summary → paste or export.)
3. Share register extract as at the record date
4. Stock option register
5. DSU register

Confirm the **as-at date** for each source — they must match or be close enough to explain differences.

### Step 2 — Produce the master comparison table

```
SHAREHOLDING RECONCILIATION — [COMPANY NAME]
As at: [DATE]
Prepared: [DATE]
⚠️ DRAFT — CONFIRM ALL FIGURES BEFORE INCLUSION IN ANY FILING

| Name | Role | Questionnaire shares | SEDI shares | Register shares | Option register | DSU register | Net position | Discrepancy? | Flag | Notes |
```

Columns:
- **Questionnaire shares**: Common shares self-reported
- **SEDI shares**: Last filed insider report balance
- **Register shares**: Registered position in share register
- **Option register**: Unvested + vested unexercised options (count + weighted avg exercise price)
- **DSU register**: DSU balance as at date
- **Net position**: Shares + in-the-money options + DSUs — FOR INTERNAL OWNERSHIP-GUIDELINE USE ONLY. Do NOT reuse this figure as a SEDI balance (report each security designation separately) or as the NI 62-103 early-warning %, which uses its own deemed-conversion inclusion rules
- **Discrepancy?**: Yes / No / Unknown
- **Flag**: 🔴 / 🟡 / 🟢

### Step 3 — Flag logic

🔴 **File a discrepancy report — may require SEDI amendment**
- Share count on questionnaire differs from SEDI by more than rounding/settlement
- Option count differs from option register (potential missed grant or exercise filing)
- Person is listed in option register but not shown as insider on SEDI
- DSU balance differs from DSU register

🟡 **Review — likely explainable but confirm**
- Difference of <500 shares (could be settlement timing, fractional entitlements, DRIP)
- DSU grant issued after last SEDI filing date
- Options exercised but not yet reflected in share register
- Person approaches 10% threshold (calculate and flag)

🟢 **Clean — no action**
- All sources agree within rounding
- Differences explained by documented timing (e.g., grant dated after record date)

### Step 4 — 10% threshold watch

For each person, calculate:
- Shares / total shares outstanding = % ownership
- If ≥9.0%: 🟡 monitor
- If ≥9.9%: 🔴 flag — early warning obligations may be triggered on crossing 10%
- If already >10%: confirm ongoing early warning obligations are being tracked

> NOTE: The 9.0% / 9.9% gates are **practitioner watch-levels, not statutory thresholds**. The
> NI 62-103 early-warning 10% test is based on **beneficial ownership or control or direction over
> the class — and INCLUDES securities convertible within 60 days** (options, warrants, certain
> units) under the deemed-conversion rule, so compute the EW % on a **partially-diluted basis**, not
> just registered shares. This is separate from whether the person is a reporting insider (directors
> and officers are reporting insiders at any %). On crossing 10%, the obligation is a **news release
> promptly (before opening next trading day) + an Early Warning Report within 2 business days + a
> purchase moratorium** — not a single "next business day" filing.

> ⚠️ Early warning thresholds under NI 62-103 / NI 62-104 are complex. This is a flag only — confirm with securities counsel.

---

## Deferred units and options — special handling

These defaults reflect the company's omnibus equity incentive plan (a 10% rolling, evergreen
plan; Insider Participation Limit 10%; Class A common shares). Confirm against current plan text.

> ⚠️ These are PLACEHOLDER defaults from one company's plan and are very likely wrong for any other
> issuer or after a plan amendment. Treat every number below (vesting schedules, max term, the 10%
> limits) as UNVERIFIED until checked against the executed plan text and the most recent
> shareholder-approved amendment. Do not state any of these figures as fact in a reconciliation or to a director.

### DSUs
- DSUs are not shares — they don't appear on the share register
- DSUs DO appear on SEDI, reported as an **issuer derivative / related financial instrument** (a security designation such as "deferred share units"), **not** as common shares and **not** as "non-securities compensation." Confirm the correct SEDI security designation and nature-of-transaction code with the filer/agent.
- Self-reported DSU counts must match DSU register AND SEDI filing
- Default vesting if unspecified: one year following the Date of Grant
- DSUs settle on/after the holder's Termination Date (cease to be director/employee), not while
  serving — a director's DSUs persist through re-election
- Directors may elect to take a % of cash fees as DSUs (Election Notice on file)

### Options
- Options appear on SEDI when granted and when exercised
- Options do NOT appear on share register until exercised
- Default vesting if unspecified: 25% per year over 4 years; max term 10 years
- Common error: director/officer reports exercised options as shares on questionnaire without filing SEDI exercise report → flag 🔴
- Net/cashless exercise: options surrendered (not shares issued) count toward the 10% limits

### RSUs / PSUs
- Default RSU vesting if unspecified: 25% / 25% / 50% over three anniversaries; PSUs vest on
  performance goals; both must settle by the final business day of the third calendar year after grant year
- Treat like DSUs for SEDI purposes; confirm share-settled vs cash-settled — BUT note both are generally reportable on SEDI as related financial instruments by a reporting insider; do NOT assume cash-settled units are exempt. Any "automatic securities purchase / compensation plan" exemption (NI 55-104 Part 5) is counsel's call.

---

## SEDI filing timeline reference (for flagging only — do not file)

| Event | SEDI deadline | Form |
|---|---|---|
| Become a reporting insider | 10 calendar days | Insider Report (Form 55-102F2), filed on SEDI. NOTE: a first-time insider must also create an Insider Profile (Form 55-102F1) before filing. There is no separate "initial" form — the first F2 is filed within the 10-day window. |
| Change in holdings (trade, grant, exercise, DSU/RSU/PSU grant) | 5 calendar days | Insider Report (Form 55-102F2), filed on SEDI |
| Cease to be a reporting insider | No fixed deadline / no separate form | Note the status change in the SEDI "Remarks" field on the next filing or by amending the last transaction (CSA Staff Notice 55-316). There is NO "Cessation of Insider Status" form and NO 10-day cessation deadline — confirm with counsel. |
| Early warning — cross 10% (NI 62-103 / NI 62-104) | News release: promptly (and before opening of trading the next business day); REPORT: within **2 business days** of the acquisition; moratorium on further purchases until 1 business day after filing | Early Warning Report (Form 62-103F1). Note: 2% top-up re-reporting triggers and the Alternative Monthly Reporting regime (eligible institutional investors; monthly, within 10 days of month-end) may apply — confirm with counsel. |

> 🔴 If a discrepancy suggests a late or missed SEDI filing, escalate to the Corporate Secretary and outside counsel immediately. Late filings attract OSC / CSA attention.

---

## Output format

Produce three things:

1. **Master reconciliation table** (see Step 2 format)
2. **Discrepancy summary** — bullet list of every 🔴 and 🟡 item with a one-line explanation
3. **Recommended actions list** — for each 🔴 item, what action is needed and who needs to do it

```
RECOMMENDED ACTIONS

🔴 [Person] — SEDI shows [X] shares, questionnaire shows [Y]. Difference of [Z].
   → Action: Confirm against register; if register matches questionnaire, SEDI
     amendment may be required. Escalate to counsel.
   → Owner: [Corporate Secretary / CFO / Outside Counsel]
   → Deadline: Before MIC filing

🟡 [Person] — Options vested but exercise not shown on SEDI.
   → Action: Confirm whether options were exercised; if so, SEDI exercise report
     may be outstanding.
   → Owner: [Director name / Corporate Secretary]
   → Deadline: SEDI deadline is 5 days from exercise date
```

---

## What this skill does NOT do

- Does not access sedi.ca (user must pull the data and paste it in)
- Does not determine whether someone is legally a "reporting insider" — that's counsel's call
- Does not prepare or submit SEDI filings
- Does not determine whether an early warning report is required — flags proximity to threshold only
- Does not make representations about insider trading compliance
