# tiny-claude-skills

A skills marketplace for Claude. Each skill is a directory under `skills/`
containing a `SKILL.md`. Merge to `main` and CI validates the frontmatter,
builds one zip per skill, and publishes them to a rolling `latest` release.

```
skills/
  <skill-name>/
    SKILL.md          # required: name + description frontmatter
    ...               # optional bundled files (scripts, refs, templates)
scripts/validate_skills.py
.github/workflows/skills.yml
```

## Add a skill

1. `cp -r skills/example-skill skills/my-skill`
2. Edit `skills/my-skill/SKILL.md` — `name` must equal the directory name.
3. Validate locally: `python scripts/validate_skills.py`
4. Open a PR. CI validates; merging publishes the zips.

## Syncing to your Claude account

There is **no API to push skills into a Claude account** — these are the real
paths:

**Claude Code** — git-pull the skills straight into your skills dir:
```bash
git clone https://github.com/TinyLtd/tiny-claude-skills ~/src/tiny-claude-skills
ln -s ~/src/tiny-claude-skills/skills/* ~/.claude/skills/
# update later with: git -C ~/src/tiny-claude-skills pull
```

**Claude Chat (claude.ai)** — skills are uploaded as zips through the UI.
Grab a stable zip from the latest release and upload it:
```
https://github.com/TinyLtd/tiny-claude-skills/releases/download/latest/<skill-name>.zip
```
`index.json` on the same release lists every skill and its zip name.
