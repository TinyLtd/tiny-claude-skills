# tiny-claude-skills

Tiny's skills for Claude, installable from one repo. Each
skill is a directory under `skills/` containing a `SKILL.md`. Merge to `main`
and CI validates the frontmatter and publishes per-skill zips (plus a bundle)
to a rolling `latest` release.

```
.claude-plugin/
  marketplace.json    # makes this repo a Claude Code plugin marketplace
  plugin.json         # bundles all skills as one installable plugin
skills/
  <skill-name>/
    SKILL.md          # required: name + description frontmatter
    ...               # optional bundled files (references, scripts)
template/             # copy-me starting point for new skills (not shipped)
scripts/validate_skills.py
.github/workflows/skills.yml
```

## Skills

| Skill | What it does |
|-------|--------------|
| `agm-operations` | AGM and shareholder meeting operations for a TSX-listed company — runbooks, chair scripts, proxy tabulation, governance-invoice review, post-AGM follow-up. |
| `corp-governance` | Corporate governance command-center and document drafting — board resolutions, minutes, notices, board packs, filing deadlines. |
| `mic-aif-questionnaire` | Annual governance questionnaire, Management Information Circular (MIC), and Annual Information Form (AIF) drafting, prefill, and year-over-year comparison. |
| `sedi-shareholding` | SEDI and shareholding discrepancy checker — reconciles reported holdings against SEDI records and the share register. |
| `tiny-decks` | Builds on-brand Tiny presentation decks as editable PowerPoint (.pptx) and Google Slides from Excel, CSV, PDF, Word, or prior decks. |

## Install

### Claude Code — one command

Add the marketplace once, then install the whole bundle:

```
/plugin marketplace add TinyLtd/tiny-claude-skills
/plugin install tiny-skills-bundle@tiny-skills
```

Pull updates later with `/plugin marketplace update tiny-skills`. Skills are
namespaced under the plugin, e.g. `/tiny-skills-bundle:corp-governance`.

### Claude Chat (claude.ai) — upload zips

Chat uploads skills one zip at a time through **Settings → Capabilities →
Skills**; there's no bulk import or API. So:

1. Download the whole set as one file:
   <https://github.com/TinyLtd/tiny-claude-skills/releases/download/latest/all-skills.zip>
2. Unzip it — you'll get one `.zip` per skill.
3. In Claude, **Settings → Capabilities → Skills → Upload skill** and pick a
   `.zip`. Repeat for each one you want.

(Or grab a single skill directly:
`.../releases/download/latest/<skill-name>.zip`. `index.json` on the release
lists every skill and its zip name.)

## Add a skill

1. `cp -r template skills/my-skill`
2. Edit `skills/my-skill/SKILL.md` — `name` must equal the directory name.
3. Validate locally: `python scripts/validate_skills.py`
4. Open a PR. CI validates on the PR; merging to `main` republishes the
   release and the plugin picks up the new skill on next update.
