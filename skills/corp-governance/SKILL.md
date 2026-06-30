---
name: corp-governance
description: >-
  Corporate governance workflow skill for TSX-listed public companies. Use
  whenever someone mentions board resolutions, written resolutions, consent
  resolutions, director approvals, board packages, board pack, meeting notices,
  annual information form, AIF, management information circular, MIC, meeting
  minutes, AGM, special meeting, signature status, DocuSign, e-signature,
  governance calendar, SEDAR+, SEDI, Clear Governance, Computershare, Broadridge,
  securities filing deadlines, or any task involving the board or outside
  counsel on a governance matter. Also triggers when preparing agendas,
  notices, resolutions, officer certificates, compliance checklists, or audit
  trails for a board or committee. Covers both the governance command-center
  (deadlines, trackers, checklists) and the document-drafting side (shells for
  minutes, resolutions, board pack assembly). Drafts and tracks only — never
  auto-files, sends, publishes, or signs anything.
---

# Corp Governance Skill

Draft, track, assemble, and flag. Legal / board approve anything that matters.
**Hard stops**: never auto-file on SEDAR+/SEDI, never send press releases, never mark a resolution as signed, never make legal calls.

**Use the exact house boilerplate.** When drafting any resolution, minutes, agenda, or notice,
read the matching reference file and match its verbatim language and structure:
- `references/resolution-templates.md` — directors'/committee resolution boilerplate (preamble,
  recitals, general authorization, all three counterparts variants, dating, signature block).
- `references/minutes-agenda-notice.md` — narrative minutes, agenda (with Consent Agenda +
  embedded chair script), and notice of meeting.

Use the legal entity name **exactly as on the Certificate of Incumbency** (caps in title
blocks) — not a trade name. Pull the current director roster from the latest Certificate of
Incumbency or last signed resolution rather than hardcoding it.

**Key process model**: the board meeting is for discussion; substantive approvals move to
**written resolution**. Minutes are narrative and say "Management was asked to circulate a
written resolution of the Board for approval" — they do NOT contain `RESOLVED THAT … Carried`
motions for those items. The agenda lists them under a **Consent Agenda**.

## Scope of this skill

| Module | What it does |
|---|---|
| **Command Centre** | Deadline calendar, document checklist, DocuSign/e-sig tracker |
| **Board Pack & Resolutions** | Agendas, notices, minutes shells, written resolutions, signature status |
| **E-signature guidance** | Google Workspace vs DocuSign decision tree for a TSX co |

For questionnaire / MIC / AIF prefill → see `mic-aif-questionnaire` skill.  
For SEDI / shareholding discrepancy checks → see `sedi-shareholding` skill.  
For AGM scripts, proxy voting, Computershare/Broadridge follow-ups → see `agm-operations` skill.

---

## Module 1 — Governance Command Centre

### Deadline calendar template

When asked to build or update a governance calendar, produce a table with these columns:

| Deadline | Item | Regulatory driver | Owner | Status | Notes |
|---|---|---|---|---|---|

Populate from the fiscal year-end the user provides. Standard TSX / CBCA deadlines to pre-fill:

- **T+40**: Audit committee year-end review meeting
- **T+90**: SEDAR+ filing deadline — Annual Financial Statements + Annual MD&A (non-venture issuer; NI 51-102 s. 4.2/5.1)
- **T+120**: SEDAR+ filing deadline — Annual Financial Statements + Annual MD&A (venture issuer; NI 51-102 s. 4.2/5.1)
- **Concurrent with annual financials/MD&A (and AIF, if later)**: CEO & CFO annual certificates (NI 52-109 s. 4.1, Form 52-109F1) — filed on the same date as, but as separate documents from, the AFS + annual MD&A. (There is no "T+30" certificate deadline in Canadian securities law.)
- **T+90**: AIF filing deadline — non-venture issuers only (NI 51-102 s. 6.1, Form 51-102F2). Venture issuers are NOT required to file an AIF (may file voluntarily for short-form prospectus eligibility).
- **Meeting-driven**: Management proxy circular / MIC and Notice of Meeting sent to shareholders per NI 54-101 notice/record-date timing (work back from the chosen meeting date; confirm record date and notice period with counsel/transfer agent — see the agm-operations skill for the N&A minimums).
- **Latest AGM date**: the EARLIER of (i) 15 months after the last annual meeting and (ii) 6 months after the financial year-end (CBCA s. 133(1)(b) / OBCA s. 94 / BCBCA s. 182). For a Dec 31 year-end the 6-month limb (June 30) typically governs. Compute the actual date; do not assume a fixed "T+120."
- Quarterly: CEO/CFO interim certificates — filed concurrently with the interim filings (NI 52-109 s. 5.1, Form 52-109F2)
- Quarterly: Audit committee interim review
- Quarterly: SEDAR+ interim financial report + interim MD&A — T+45 (non-venture) / T+60 (venture) from quarter-end (NI 51-102 s. 4.4/5.1)

Ask the user: fiscal year-end date, **venture or non-venture issuer status** (NOT "accelerated/non-accelerated" — that is a US SEC concept with no application in Canada), jurisdiction of incorporation (CBCA, OBCA, BCBCA, etc.), and any known portco exceptions.

> ⚠️ Status note: per the house records, this issuer graduated from TSXV to the **TSX effective October 1, 2025** and is now a **non-venture issuer**. Use the non-venture deadlines (annual T+90, interim T+45, AIF mandatory at T+90). The venture (T+120 / T+60 / no AIF) branches above are retained for general reference only and do NOT apply to this issuer unless counsel confirms otherwise.

Flag anything within 14 days as 🔴, 15–30 days as 🟡, >30 days as 🟢.

> ⚠️ Treat every regulatory date/deadline in this skill as a planning estimate, NOT authority. Cite the governing rule (NI 51-102 s. 4.2/4.4/6.1; NI 52-109 s. 4.1; CBCA s. 133) beside each deadline and append `⚠️ CONFIRM DEADLINE WITH COUNSEL / CURRENT RULE` to any generated calendar. Never present a filing date as settled.

### Document checklist

Standard year-end governance package items (adapt to context):

- [ ] Audited financial statements (final version from auditor)
- [ ] MD&A (draft → legal → CEO/CFO → audit committee → board)
- [ ] CEO certificate (52-109)
- [ ] CFO certificate (52-109)
- [ ] Audit committee approval resolution
- [ ] Board approval resolution — financials & MD&A
- [ ] Board approval resolution — AIF
- [ ] Management Information Circular (MIC) / Proxy
- [ ] Notice of AGM
- [ ] Annual Information Form — Form 51-102F2 (MANDATORY for non-venture issuers; this issuer is non-venture post-Oct 2025)
- [ ] SEDAR+ filing confirmation
- [ ] Transfer agent instruction letter (Computershare / TSX Trust)
- [ ] Press release — annual results
- [ ] Press release — AGM notice
- [ ] Report of voting results (NI 51-102 s. 11.3) — filed on SEDAR+ promptly after the meeting (free-form report; there is NO prescribed form number — do not cite "Form 51-102F8")

### DocuSign / e-signature tracker

When tracking signature status, produce a table:

| Document | Signer | Role | Sent | Signed | Platform | Audit cert saved? |
|---|---|---|---|---|---|---|

Platforms: `DocuSign` | `Google Workspace eSign` | `Wet ink` | `Pending`

---

## Module 2 — Board Pack & Resolutions

All four artifacts (resolution, minutes, agenda, notice) follow exact house boilerplate.
**Read `references/resolution-templates.md` before drafting any resolution** and
**`references/minutes-agenda-notice.md` before drafting minutes, an agenda, or a notice.**
Match their verbatim language; the summaries below are orientation only.

### Board pack assembly

When asked to assemble a board pack, ask:
1. Meeting type (regular board / committee / special)
2. Meeting date, time, timezone, videoconference link
3. Current director roster and guests (or point me to the latest Certificate of Incumbency)
4. Agenda items — for each: presenter initials, action (Review/Approve), duration
5. Which items will be approved in-session vs. moved to the **Consent Agenda** (written resolution)
6. Prior minutes to be confirmed (do you have the drafts?)

Assemble: **Notice → Agenda (with Consent Agenda + chair script) → prior draft minutes →
materials list**, using the skeletons in `references/minutes-agenda-notice.md`.

### Written resolutions

Build from `references/resolution-templates.md`. Pick the correct preamble (board vs. CG&N
committee), recitals, general-authorization variant, and **counterparts variant** (three
exist — A "one or more counterparts", B "single instrument / DocuSign", C inline numbered).
Use the legal entity name and ALL-CAPS director names from the incumbency certificate.

Drafting rules:
- The operative verb is `NOW THEREFORE BE IT RESOLVED THAT:` (numbered) or `IT IS RESOLVED that`
  (short form for minutes-approval) — match the matter.
- "Subject to" conditions (shareholder approval, Exchange acceptance) go in the operative paragraph.
- Attach supporting materials by reference; don't embed them.
- Header every draft `DRAFT — FOR LEGAL REVIEW — NOT FOR EXECUTION`.

### Minutes

Build from `references/minutes-agenda-notice.md`. **Narrative, not motion-by-motion.** Record
deliberation; for approval items write that "Management was asked to circulate a written
resolution of the Board for approval." Use the standard recurring phrases verbatim (quorum,
agenda review, other business, in-camera, termination). End with the two-column Chair /
Corporate Secretary block and a `Confirmed:` line (date added only once approved by written
resolution).

---

## Module 3 — E-Signature: Google Workspace vs DocuSign

### Background
Google Workspace eSignature (generally available since June 2024) produces legally binding e-signatures with tamper-evident audit trails under PIPEDA and provincial electronic commerce acts. For most commercial purposes in Canada, it meets the four enforceability tests: identity, intent, reliable link to document, and record integrity.

### What the company already does (from executed examples)
The company's own counterparts clauses **already authorize ".pdf or DocuSign" execution** of
directors' and committee resolutions, and recent board/committee resolutions, AGM
material approvals, the notice-of-change resolution, and minutes confirmations were all
executed in **DocuSign**. So the "is e-signature acceptable for written resolutions" question
is, in practice, already answered yes by counsel — the open question is only whether to move
that volume to Google Workspace eSign to save cost, which is a different decision.

One hard transfer-agent rule from the **Computershare Certificate of Incumbency**: if
Computershare is instructed to accept a DocuSign signature, the **DocuSign signature must be
affixed beside the original (wet) signature** on the certificate to be valid. Treat the
incumbency certificate as a wet-ink-plus-DocuSign document, not pure e-sign.

### Decision matrix for a TSX-listed issuer

| Document type | Google Workspace eSign OK? | Notes |
|---|---|---|
| Internal approvals, internal resolutions | ✅ Yes | Low stakes, keep in ecosystem |
| Board / committee written resolutions | ✅ Already on DocuSign | House clauses bless ".pdf or DocuSign"; moving to Google eSign is a cost choice, confirm counsel is indifferent to platform |
| Officer certificates (52-109) | ⚠️ Confirm with counsel | Filed on SEDAR+ — auditors may have a view on acceptable format |
| MIC / Proxy — director signatures | ⚠️ Confirm with counsel | Computershare / Broadridge may require DocuSign-certified certificates |
| Certificate of Incumbency | ❌ Special rule | Computershare requires DocuSign affixed **beside an original signature** |
| NDA / vendor agreements | ✅ Yes | Standard commercial contracts |
| Employment agreements | ✅ Yes | Routine for Canadian employers |
| Share certificates | ❌ No | Require specific form; transfer agent controls |
| Statutory declarations | ❌ No | Require wet ink or notarized signature |
| Documents filed with courts | ❌ No | Court rules vary; wet ink typically required |

### What Google Workspace eSign lacks vs DocuSign

> Vendor feature details below were accurate at time of writing and drift — verify against current DocuSign / Google product docs before relying on them. The legal-enforceability framing (PIPEDA + provincial electronic-commerce / e-transactions acts; four-part test) is the durable part.
- **Certificate of Completion**: DocuSign's tamper-evident PDF seal with cryptographic hash is a recognized audit artifact. Google's audit trail is a separate report — must be saved alongside the signed document.
- **Template library with compliance workflows**: DocuSign IAM has pre-built CBCA/TSX governance templates. Google does not.
- **Bulk send**: DocuSign supports bulk send. Google supports up to 10 signers per document.
- **Chain-of-custody PDF**: DocuSign embeds the audit trail into the signed PDF. Google produces a separate file.

### Recommended approach for Tiny
1. **Use Google Workspace eSign** for: internal resolutions that do not go to SEDAR+, committee approvals, non-material agreements, NDAs, vendor contracts.
2. **Keep DocuSign** for: officer certificates filed on SEDAR+, documents where KPMG / outside counsel explicitly require a DocuSign certificate, any document Computershare / TSX Trust requires in a specific form.
3. **Confirm counsel is platform-indifferent** before switching board resolutions from DocuSign to Google eSign — counsel already accepts electronic/DocuSign execution, so this is about whether they care which platform, not whether e-sign is valid.
4. **Save the audit log** for every Google eSign request to the same Drive folder as the signed document, immediately on completion.

> ⚠️ This is a framework for discussion, not legal advice. Confirm with the Corporate Secretary and outside counsel before changing the signing workflow for any SEDAR+-filed document.

---

## Output rules

- Always produce **shells and drafts**, never final executed documents
- Flag every legal judgment call with `⚠️ CONFIRM WITH COUNSEL`
- Flag every SEDAR+/regulatory item with `📋 REQUIRES FILING — DO NOT AUTO-SUBMIT`
- Produce audit-trail notes (who saw it, when, what version) whenever drafting anything that will be approved
- Do not make representations about what the board "approved" or "resolved" — that language is only in the signed, final document

## Files
- `references/resolution-templates.md` — verbatim directors'/committee resolution boilerplate (read before drafting any resolution).
- `references/minutes-agenda-notice.md` — verbatim narrative minutes, agenda (Consent Agenda + chair script), and notice of meeting (read before drafting any of these).
