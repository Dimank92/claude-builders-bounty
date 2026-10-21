---
name: generate-changelog
description: Automatically generates a structured CHANGELOG.md from git commits since the last tag following Keep a Changelog format.
---

# Generate Changelog Skill

Use this skill when you want to summarize recent git history into a formatted `CHANGELOG.md`.

## Instructions
1. Run `python skills/changelog-generator/changelog.py` from the root of your repository.
2. The script inspects `git describe --tags --abbrev=0` and groups all commits into `Added`, `Fixed`, `Changed`, and `Removed`.
3. Prepend the structured entry to `CHANGELOG.md`.
