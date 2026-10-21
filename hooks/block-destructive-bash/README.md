# Block Destructive Bash Commands Hook

> Pre-tool-use hook for Claude Code that prevents catastrophic irreversible bash commands.
> Solves **[Bounty #3 ($100)](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/3)**.

---

## 🛡️ Protected Patterns

This hook intercepts and blocks the following hazardous commands before execution:
1. `rm -rf` (recursive forced file deletion)
2. `DROP TABLE` (destructive database schema operations)
3. `git push --force` or `git push -f` (destructive history overwrites)
4. `TRUNCATE` (instant table wiping)
5. `DELETE FROM ...` without a `WHERE` clause (accidental whole-table data loss)

Normal operations (e.g., `DELETE FROM users WHERE id = 1`, `git status`, `npm run dev`) pass through cleanly.

---

## ⚡ Installation (2 Commands)

```bash
mkdir -p ~/.claude/hooks
cp block-destructive-bash.py ~/.claude/hooks/pre-tool-use.py && chmod +x ~/.claude/hooks/pre-tool-use.py
```

---

## 📋 Audit Logging

Every intercepted command is recorded with an ISO timestamp and project path to:
```
~/.claude/hooks/blocked.log
```

Example log entry:
```
[2026-10-22T01:43:46.123456] BLOCKED: "rm -rf node_modules" | CWD: /path/to/project | REASON: Recursive forced file removal (rm -rf)
```

---

## 🧪 Testing

Run the included verification suite:
```bash
python test_hook.py
```
