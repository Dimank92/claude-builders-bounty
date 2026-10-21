# Git Changelog Generator Skill

> Auto-generates clean, structured `CHANGELOG.md` following Keep a Changelog & Conventional Commits.
> Solves **[Bounty #1 ($50)](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/1)**.

---

## ⚡ Quick Setup (3 Steps or Fewer)

1. **Copy the script to your repo:**
   ```bash
   cp changelog.py ./changelog.py
   ```
2. **Run the generator:**
   ```bash
   python changelog.py
   ```
3. **Commit the generated CHANGELOG.md:**
   ```bash
   git add CHANGELOG.md && git commit -m "docs: update CHANGELOG.md"
   ```

---

## 📋 Features

- 🏷️ **Tag-Aware:** Extracts commits since the last git release tag (`git describe --tags`). Falls back to root commit if no tags exist.
- 🎯 **Automatic Categorization:**
  - `feat:`, `add:`, `new:` ➔ **Added**
  - `fix:`, `bug:`, `patch:` ➔ **Fixed**
  - `refactor:`, `perf:`, `chore:`, `style:` ➔ **Changed**
  - `remove:`, `deprecate:`, `revert:` ➔ **Removed**
- 🛡️ **Preserves Existing History:** Prepends new releases while preserving previous changelog entries.
