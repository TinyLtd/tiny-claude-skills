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

1. `cp -r template skills/my-skill`
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

**Claude Chat (claude.ai)** — skills are uploaded one zip at a time through
**Settings → Capabilities → Skills**. There is no bulk import, so:

1. Download the whole set as one file:
   <https://github.com/TinyLtd/tiny-claude-skills/releases/download/latest/all-skills.zip>
2. Unzip it — you'll get one `.zip` per skill.
3. In Claude, open **Settings → Capabilities → Skills → Upload skill** and pick
   a `.zip`. Repeat for each one you want.

(Or grab a single skill directly:
`.../releases/download/latest/<skill-name>.zip`. `index.json` on the release
lists every skill and its zip name.)
