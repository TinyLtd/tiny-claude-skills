# Publishing the Release — Newsfile + the Wire-API Landscape

## The binding constraint (read first)
Tiny is a **TSX issuer**. Material disclosure must go through a **regulatory-grade wire** that
disseminates simultaneously to Canadian financial press + regulators and files **SEDAR+**. This rules
OUT the cheap, easy-API wires (EIN Presswire, Newswire.com, IssueWire, openPR, etc.) for material
news — they do not do Canadian regulatory dissemination or SEDAR+. So "find a wire with an easy API"
is the wrong optimization for material releases; the right wire list is short and regulatory-grade.

## Findings on the wires that actually qualify

| Wire | Submit API? | Canadian reg. dissemination + SEDAR+? | Notes |
|---|---|---|---|
| **Newsfile (TMX Newsfile)** — Tiny's CURRENT vendor | **No public inbound submission API.** Integration page only offers RSS/FTP/SFTP, and that's for *agencies syndicating content OUT*, not a "submit my release" endpoint. | **Yes** (TMX-owned; SEDAR+ filing in the package). | ~$10.4k/yr, already paid. Submission is via their **dashboard** or **account team / editorial desk**. |
| **ACCESS Newswire** (formerly ACCESSWIRE / Issuer Direct, NYSE: ACCS) | **Yes — real REST API** for programmatic submission (built for high-volume/agency/legal customers). | Yes (IR/regulatory distribution; SEDAR filing available). | Cleanest developer API among regulatory-grade wires. Requires an account; some sales touch. |
| **GlobeNewswire (Notified)** | **Yes — API submission available to customers.** | Yes — in-house regulatory team, **SEDAR** filing option. | Enterprise; sales-driven onboarding. |
| **Business Wire** | API (NX) exists | Yes | Enterprise; sales-driven. |
| Cheap self-serve (EIN, Newswire.com, IssueWire…) | Easy APIs, low cost | **No** Canadian reg. dissemination / SEDAR+ | OK ONLY for clearly **non-material** marketing news — but adds vendor sprawl + risk of pushing material news through the wrong channel. Not recommended for Tiny. |

## Recommendation
1. **Do not switch wires just to get an API.** Newsfile is cheap, TMX-owned, already files SEDAR+, and
   IR-website auto-population is already wired. The publish automation is a convenience, not worth
   re-papering the disclosure vendor, retraining IR, and re-pointing the website RSS.
2. **Realistic "publish" today = stage, don't auto-send.** The skill produces a perfectly formatted,
   approved, wire-ready release and hands it off one of two ways (no new contract, no sales call):
   - **(a) Formatted email to the Newsfile desk / account rep** with send instructions and timing, OR
   - **(b) Paste-ready package** for whoever loads the Newsfile dashboard.
   A human still hits send — which is what the law requires for material disclosure anyway.
3. **Only chase an API if volume justifies it.** If Tiny ever wants true programmatic auto-staging,
   **ACCESS Newswire** has the most accessible customer API among regulatory-grade wires, with
   **GlobeNewswire/Notified** second. Both are a vendor switch + sales conversation — worth it only at
   high release volume, which Tiny is not at (~22 releases/yr on the Newsfile plan).

## Build the publish step as a pluggable adapter
Design the "stage" output so the delivery mechanism is swappable. The skill's job ends at a
**wire-ready artifact + a chosen adapter**:

- `adapter: email` (default, works today) → renders the release + a cover note to the Newsfile desk.
- `adapter: dashboard` → renders a clean paste block + field-by-field instructions for the Newsfile UI.
- `adapter: access-newswire-api` (future) → POST to ACCESS Newswire REST endpoint (needs account + key).
- `adapter: globenewswire-api` (future) → Notified submission API (needs account + key).

Store any future API keys in 1Password ("Dev Credentials") and reference via env var; never inline.

## What's still needed to finish the publishing piece
- One answer from the Newsfile rep: **"Do we have any inbound submission API, or is it dashboard/
  email only?"** (Public docs say no API — but confirm, since account-level options vary.)
- The Newsfile **account ID / client code** and the **desk contact email** for the `email` adapter.
- Decision on whether to pursue an ACCESS Newswire / GlobeNewswire account later for true auto-staging.
