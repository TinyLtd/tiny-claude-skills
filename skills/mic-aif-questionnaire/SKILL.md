---
name: mic-aif-questionnaire
description: >-
  Annual governance questionnaire, Management Information Circular (MIC), and
  Annual Information Form (AIF) assistant for a TSX-listed public company.
  Use whenever someone mentions: director questionnaires, officer questionnaires,
  D&O questionnaire, governance questionnaire, MIC prefill, MIC drafting, proxy
  circular, information circular, AIF drafting, AIF update, insider questionnaire,
  related party disclosure, independence determination, audit committee disclosure,
  compensation discussion, skills matrix, advance notice bylaw, majority voting
  policy, director nomination, chasing missing questionnaire responses, comparing
  year-over-year answers, or flagging material changes in disclosure. Drafts,
  prefills, compares, and flags — never files or sends. For SEDI discrepancy
  checks, use the sedi-shareholding skill.
---

# MIC / AIF / Questionnaire Assistant

Draft, prefill, compare, chase, and flag. Legal / board review everything. Never file.

**Hard stops**: no auto-filing on SEDAR, no sending to directors without approval, no legal determination of independence or related-party status.

---

## Questionnaire workflows

### A. Prefill from prior year

When the user provides last year's completed questionnaire (PDF or text) and asks to prefill this year's version:

1. Extract every answer from the prior year, field by field
2. Mark each pre-filled answer as `[PRE-FILLED — CONFIRM]`
3. Highlight fields where the answer is likely stale:
   - Share counts and ownership percentages
   - Committee memberships
   - Other board/advisory positions
   - Compensation figures
   - Loans and indebtedness
   - Any answer referencing a specific date or year
4. Mark fields that **must** be answered fresh each year as `[MUST UPDATE]`:
   - Independence self-certification
   - Conflict of interest declarations
   - Related-party transactions in the past 12 months
   - Attendance record
   - Securities transactions in the fiscal year
5. Produce a clean prefilled draft with all flags visible

### B. Chase missing fields

When the user provides completed questionnaires from some directors/officers and asks for a status report:

Produce a table:

| Person | Role | Questionnaire received | Missing sections | Last chased | Notes |
|---|---|---|---|---|---|

Then draft a **chase email** for incomplete respondents (do not send — user must review and send):

```
Subject: [YEAR] Director/Officer Questionnaire — Action Required by [DEADLINE]

Dear [Name],

We are completing our annual director and officer questionnaire process
in preparation for our [YEAR] Management Information Circular.

Your questionnaire is [missing / partially completed — the following
sections require your attention]: [LIST MISSING ITEMS]

Please complete and return by [DATE].

If you have questions, please contact [NAME] at [EMAIL/PHONE].

Thank you,
[NAME]
[TITLE]
[COMPANY NAME]
```

### C. Flag year-over-year changes

When the user provides prior year and current year questionnaire responses:

Produce a change report:

| Person | Field | Prior year answer | Current year answer | Flag level | Notes |
|---|---|---|---|---|---|
| | | | | 🔴 Material / 🟡 Review / 🟢 Routine | |

Flag levels:
- 🔴 **Material** — new related-party transaction, change in independence status, new lawsuit, bankruptcy, criminal record, material change in shareholding
- 🟡 **Review** — new outside directorship, change in committee membership, share count change >5%, change in compensation structure
- 🟢 **Routine** — share count change <5%, minor updates to address/contact, updated employment title

> ⚠️ Independence and related-party determinations require legal review — this tool flags changes, it does not make the legal call.

---

## MIC / Proxy Circular drafting

### Standard MIC sections (TSX non-venture issuer, CBCA)

Governing instruments: the circular is prescribed by **Form 51-102F5 Information Circular** under
NI 51-102 Part 9. It incorporates by reference:
- **Form 51-102F6 Statement of Executive Compensation** (executive/director compensation)
- **Form 58-101F1 Corporate Governance Disclosure** (NI 58-101)
- **Form 52-110F1 Audit Committee disclosure** (NI 52-110), or AIF cross-reference
- CBCA s. 150 (proxy solicitation) / s. 172.1 (diversity disclosure)

Confirm the current consolidated forms before drafting — items and thresholds change.

When asked to draft or update a MIC, work section by section. Ask the user which sections need updating before producing output.

**Cover page and proxy instructions**
- Meeting date, time, location, record date
- Proxy voting instructions (form of proxy, proxyholder designation)
- Deadline for proxy submission
- Notice-and-access statement (if applicable)

**Business of the meeting**
Standard items for most AGMs:
1. Receive financial statements
2. Elect directors
3. Appoint auditor and authorize audit committee to fix remuneration
4. Advisory vote on executive compensation (say-on-pay) — **VOLUNTARY in Canada today** (non-binding); include only if the company has adopted a say-on-pay policy. ⚠️ WATCH: a CBCA mandatory advisory say-on-pay regime (CBCA s. 82.2, Bill C-25) is enacted but **not yet in force** — confirm the force-in-date with counsel each cycle; once in force it becomes mandatory and the vote result must be disclosed.
5. Any special business

**Director election section**
For each director nominee:
- Name, age, municipality of residence
- Director since
- Principal occupation
- Independence determination (Independent / Non-independent — with basis)
- Board/committee memberships
- Attendance record (prior year meetings attended / total)
- Other public company boards
- Shares / DSUs / options held (table format)
- Skills matrix checkbox (read from questionnaire or prior year AIF)

> ⚠️ CBCA majority voting (in force 31 Aug 2022): directors of a CBCA distributing corporation are
> elected **INDIVIDUALLY** by a **majority of votes cast "FOR" and "AGAINST"** in an uncontested
> election (NOT "for/withhold"). An incumbent who fails to get a majority may hold over up to 90 days
> (CBCA s. 106(3.1)–(3.5)). The circular must disclose this standard and the form of proxy must offer
> FOR/AGAINST per nominee. Do NOT reuse a pre-2022 "withhold" / TSX majority-voting-policy template
> for a CBCA issuer. Confirm jurisdiction of incorporation with counsel — a non-CBCA TSX issuer still
> relies on the TSX policy (Company Manual s. 461.3) plus its own majority-voting policy, which uses
> "for/withhold" with a resignation trigger. The two regimes use different ballot wording.

```
DIRECTOR NOMINEE SHELL

Name: [FULL NAME]
Age: [AGE]
Residence: [CITY, PROVINCE]
Director since: [YEAR]

Principal occupation: [TITLE] at [COMPANY] since [YEAR]

Independence: [Independent / Non-independent]
[If non-independent, state basis: e.g., "Member of management" /
"Relationship with [entity]"]

Committee memberships: [LIST]
2024 attendance: [X/Y meetings] ([Z]%)

Securities held as at [RECORD DATE]:
  Common shares: [#]
  DSUs: [#]
  Options: [#] (exercise price $[X], expiry [DATE])
  Total value at [DATE]: $[X] (based on closing price of $[X])

Other public company boards: [LIST or None]

⚠️ CONFIRM: Independence determination, share counts, and committee memberships
with current questionnaire before including in filed document.
```

**Audit committee disclosure** (NI 52-110; Form 52-110F1 for non-venture)
- Composition: every member must be independent (NI 52-110 s. 3.1(3), non-venture) — subject only to the Part 3 exemptions (IPO / controlled co / events outside control / vacancy). Venture issuers use the majority-independent standard. ⚠️ Independence is a board legal determination — CONFIRM WITH COUNSEL.
- Financial literacy: state whether each member is "financially literate" within the NI 52-110 s. 1.6 meaning (ability to read and understand financials of comparable breadth/complexity). ⚠️ This is a board determination — CONFIRM WITH COUNSEL; do not assert it from the questionnaire alone.
- Audit committee charter reference
- External auditor fees (audit / audit-related / tax / other) — prior two fiscal years
- Pre-approval policies

**Corporate governance disclosure (NI 58-101 / Form 58-101F1)**
- Board independence, mandate, position descriptions, orientation/continuing education, ethical business conduct, nomination, compensation, committees, board assessments, director term limits
- Skills matrix, advance notice by-law, majority voting policy (see CBCA majority-voting note above)
- DIVERSITY — mandatory, two overlapping regimes:
  - **Form 58-101F1**: representation of women on the board and in executive officer positions; policies, targets, term limits, board-renewal mechanisms
  - **CBCA s. 172.1** (CBCA issuers): representation of the four designated groups — women, Indigenous peoples, persons with disabilities, members of visible minorities — on the board and in senior management, disclosed in the notice/circular at every annual meeting
  - ⚠️ Confirm whether any expanded CSA Form 58-101F1 diversity amendments are in force at draft date

**Executive compensation (CD&A)**
- NEO identification per Form 51-102F6: (a) CEO; (b) CFO; (c) each of the 3 most highly compensated executive officers (or individuals acting in a similar capacity), other than CEO/CFO, serving at fiscal year-end whose **total compensation individually exceeded $150,000**. ⚠️ If fewer than 3 such officers clear $150,000, there are fewer than 5 NEOs — do not pad to 5. ⚠️ "Executive officer" is a defined term (NI 51-102 s. 1.1) — confirm status with counsel, not job title. Prior-year comp must still be shown for anyone who is an NEO this year, even if <$150k in a prior year.
- Compensation philosophy and objectives
- Elements of compensation (base / STI / LTI)
- Performance metrics and results
- Summary compensation table
- Outstanding share-based and option-based awards table
- Director compensation table
- Termination and change-of-control: estimated incremental payments/benefits to each NEO triggered by termination, resignation, retirement, or change of control (Form 51-102F6 Item 5)
- Clawback / compensation recovery policy disclosure (and confirm any pending CBCA s. 82.x clawback requirement — enacted but check force-in-date with counsel)
- Performance graph (cumulative TSR vs. index, where required)

**Say-on-pay**
Standard advisory vote language:
```
BE IT RESOLVED, on an advisory basis and not to diminish the role and
responsibilities of the Board of Directors, that the shareholders accept
the approach to executive compensation disclosed in the management
information circular of the Corporation dated [DATE].
```

**Interest of informed persons in material transactions (continuous disclosure)**
- Disclose any material transaction in which an "informed person" (director, officer, or any holder of **10% or more** of the voting rights — note: 10%-or-more, **not** ">10%"), or an associate/affiliate of such a person, has a material interest. Source: Form 51-102F5 Item 11 / Form 51-102F2 Item 15.
- Source data: questionnaire responses + prior year AIF + management review
- 🔴 Flag any new transactions not in prior year disclosure
- ⚠️ SEPARATE REGIME — **MI 61-101**: a related-party transaction or business combination may also trigger formal valuation and minority-approval requirements under MI 61-101 (25% market-cap exemption test; ON/QC). This is a DISTINCT analysis from CD disclosure. 🔴 LEGAL REVIEW REQUIRED — do not assume CD disclosure satisfies MI 61-101 or vice versa.

---

## AIF drafting and updating

### Standard AIF sections (Form 51-102F2)

When asked to draft or update an AIF section, ask for the prior year AIF and any material changes since filing.

Sections that typically change year over year (flag for review):
- Item 4: General Development of the Business (add current year narrative)
- Item 5: Description of the Business (update metrics, products, headcount)
- Item 6: Dividends (any changes to policy)
- Item 7: Capital Structure (share counts, options outstanding)
- Item 8: Market for Securities (updated trading range table)
- Item 9: Escrowed Securities (update release schedule)
- Item 10: Directors and Officers (update bios, share holdings, committee memberships)
- Item 11: Audit Committee (update if composition changed)
- Item 12: Legal Proceedings (add any new matters, remove resolved ones)
- Item 13: Regulatory Actions (confirm none, or update)
- Item 14: Related Party Transactions (reconcile with questionnaire responses)

Sections that are largely static (confirm no change):
- Item 1: Cover page / date and currency of information
- Item 2: Corporate Structure (name, incorporation, intercorporate relationships)
- Item 3: General Development of the Business — three-year history (older years static)

⚠️ Form 51-102F2 runs **beyond Item 14** — do NOT treat the list above as complete. Also confirm:
- Item 4: Narrative Description of the Business
- Item 15: Interest of Management and Others in Material Transactions (the AIF related-party item)
- Item 16: Transfer Agents and Registrars · Item 17: Material Contracts · Item 18: Interests of Experts
- Item 19: Additional Information
- Forward-looking information: every AIF/MIC with FLI needs the NI 51-102 Part 4A.3 disclaimer (material factors/assumptions + risk that results differ)
- ⚠️ CONFIRM item numbering against the current consolidated Form 51-102F2 — it has been renumbered over time.

**AIF change summary table** (produce this before full drafting):

| AIF section | Prior year status | Change needed? | Source of update | Flag |
|---|---|---|---|---|

---

## Output rules

- All output is a **draft for legal review** — include this header on every document:
  `DRAFT — FOR LEGAL REVIEW — NOT FOR FILING OR DISTRIBUTION`
- Every independence determination is flagged `⚠️ CONFIRM WITH COUNSEL`
- Every related-party disclosure is flagged `🔴 LEGAL REVIEW REQUIRED`
- Every share/option count is flagged `[CONFIRM AGAINST SHARE REGISTER]`
- Prefilled answers from prior year are always marked `[PRE-FILLED — CONFIRM]`
- Any draft containing forward-looking information carries the NI 51-102 Part 4A.3 FLI disclaimer (material assumptions + risk that actual results differ) — flag `⚠️ FLI DISCLAIMER REQUIRED — CONFIRM WITH COUNSEL`
- A version formatted/paginated "for filing" is still a DRAFT until counsel and board approve and a human files it — formatting readiness is never filing authorization
- Never produce a "final" version — always "draft" or "revised draft"
