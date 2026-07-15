# AGENTS.md

This file guides coding agents working in `TinyLtd/tiny-claude-skills`.

## Working agreement

- Read `README.md` and the repository documentation before making changes.
- Keep changes focused on the requested task and preserve existing behavior unless the request requires otherwise.
- Follow the repository's existing structure, naming, style, and dependency choices.
- Add or update tests when behavior changes. Run the relevant checks before finishing and report anything you could not run.
- Never commit credentials, secrets, `.env` files, generated build output, or private machine-specific details.
- Do not overwrite unrelated work. Call out migrations, deployment steps, or other manual follow-up clearly.

## Setup and validation

- Use the setup, development, and validation commands documented in `README.md` and existing project files; do not substitute a different toolchain without approval.

If a command above conflicts with the repository documentation, the repository documentation wins; update this file in the same change.
