#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md frontmatter. Optionally emit an index.

Usage:
  validate_skills.py                 # validate, exit 1 on any error
  validate_skills.py --manifest out.json   # also write a marketplace index

Frontmatter contract (Anthropic skill format):
  name         required, == directory name, ^[a-z0-9]+(-[a-z0-9]+)*$, <=64 chars
  description  required, non-empty, <=1024 chars
Everything else (allowed-tools, etc.) is passed through untouched.
"""
import json
import re
import sys
from pathlib import Path

import yaml  # PyYAML; installed by the workflow

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text: str):
    """Return the YAML frontmatter dict, or raise ValueError."""
    if not text.startswith("---"):
        raise ValueError("missing opening '---' frontmatter fence")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("missing closing '---' frontmatter fence")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a YAML mapping")
    return data


def validate_skill(skill_dir: Path):
    """Return (front, errors) for one skill directory."""
    errors = []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return None, [f"{skill_dir.name}: no SKILL.md"]
    try:
        front = parse_frontmatter(md.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as e:
        return None, [f"{skill_dir.name}/SKILL.md: {e}"]

    name = front.get("name")
    if not name:
        errors.append(f"{skill_dir.name}: 'name' is required")
    else:
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: name '{name}' != directory name")
        if not NAME_RE.match(str(name)):
            errors.append(f"{skill_dir.name}: name must be lowercase-hyphenated")
        if len(str(name)) > 64:
            errors.append(f"{skill_dir.name}: name exceeds 64 chars")

    desc = front.get("description")
    if not desc or not str(desc).strip():
        errors.append(f"{skill_dir.name}: 'description' is required")
    elif len(str(desc)) > 1024:
        errors.append(f"{skill_dir.name}: description exceeds 1024 chars")

    return front, errors


def main():
    if not SKILLS_DIR.is_dir():
        print(f"error: {SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not dirs:
        print("error: no skills found under skills/", file=sys.stderr)
        return 1

    all_errors, index = [], []
    for d in dirs:
        front, errors = validate_skill(d)
        all_errors.extend(errors)
        if front and not errors:
            index.append({
                "name": front["name"],
                "description": str(front["description"]).strip(),
                "zip": f"{front['name']}.zip",
            })
            print(f"ok: {d.name}")

    if all_errors:
        print("\nVALIDATION FAILED:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if "--manifest" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--manifest") + 1])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"skills": index}, indent=2) + "\n")
        print(f"\nwrote {out} ({len(index)} skills)")

    print(f"\nall {len(index)} skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
