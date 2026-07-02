# tiny-pr

Drafts and stages TSX-compliant press releases for Tiny Ltd (TSX: TINY) in Andrew Wilkinson's voice.

## What it does

Takes rough bullets or notes and produces a finished, wire-ready news release through a structured pipeline:

1. **Intake** — identifies release type (earnings, M&A/material change, financing, governance/AGM, company update)
2. **Fact grounding** — pulls from `tiny-kb` (requires connector); tags unverified items `[UNCONFIRMED]`
3. **Interview** — asks for missing facts, headline angle, emphasis, and quote preferences
4. **Drafting team** — runs four specialist agents in parallel: PR/IR strategist, investor-psychology specialist, securities-compliance reviewer, Tiny-voice writer; synthesizes one best draft + alternatives
5. **Compliance lint** — checks every item in `references/compliance-checklist.md`
6. **Approval gate** — renders full draft inline; blocks staging until explicit recorded approval
7. **Staging** — prepares Newsfile package for human send; never auto-publishes

## Hard constraints

- Never auto-publishes material disclosure without recorded human approval in the current thread
- Never invents or estimates financial figures — marks gaps `[[FINANCE: …]]`
- Never pulls Folly/personal holdings into a Tiny public-company release
- Always uses current TSX (not TSX Venture) disclaimer wording
- Requires `tiny-kb` MCP connector for knowledge lookups — degrades gracefully without it (user must supply all facts)

## Reference files

| File | Purpose |
|---|---|
| `references/SKILL.md` | Main skill instructions and pipeline |
| `references/boilerplate.md` | Current verbatim About Tiny, Forward-Looking note, Non-IFRS note, contact block, dateline/house style, leadership roster — extracted from Q1 2026 release (May 13 2026). **Auto-inserted into every draft.** Refresh from newest release periodically. |
| `references/compliance-checklist.md` | TSX issuer lint — every item must be PASS/FIX/BLOCK before staging |
| `references/drafting-team.md` | Expert agent roster, orchestration instructions, investor-psychology playbook |
| `references/interview-bank.md` | Gap questions and angle/emphasis/quote questions, organized by release type |
| `references/publishing-and-api-landscape.md` | Newsfile staging workflow, wire-API landscape, adapter design notes |
| `references/templates.md` | Release structure skeletons by type (earnings, M&A, financing, governance, company update) |
| `references/voice-and-style.md` | Tiny/Andrew Wilkinson voice guide — founder-direct, Berkshire-letter register |

## Dependencies

- **`tiny-kb` MCP connector** — used for grounding facts against Tiny public filings and corporate knowledge. Without it, the skill still works but all facts must come from the user.
- **Google Drive/Docs connector** (optional) — used to create a review doc and share with the standard distribution list (chris@tiny.com, austin@tiny.com, caleb@tiny.com, andrew@tiny.com) when Andrew approves that step.

## Maintenance

`references/boilerplate.md` contains dated content (leadership titles, About Tiny copy, financial contact). Refresh after each new results release or material change that updates any of these. Last refreshed: 2026-06-13 from Q1 2026 results (May 13 2026).
