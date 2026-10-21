#!/usr/bin/env python3
"""
Test Suite for block-destructive-bash hook
Verifies all required acceptance criteria.
"""

import subprocess
import json
import os
from pathlib import Path

HOOK_PATH = Path(__file__).parent / "block-destructive-bash.py"

def run_test(command: str) -> tuple[int, str]:
    payload = json.dumps({
        "tool_name": "bash",
        "tool_input": {"command": command},
        "cwd": "/test/project"
    })
    result = subprocess.run(
        ["python", str(HOOK_PATH)],
        input=payload,
        text=True,
        capture_output=True
    )
    return result.returncode, result.stderr

def main():
    print("Testing block-destructive-bash hook...")

    # Should be BLOCKED (exit code 1)
    blocked_cases = [
        "rm -rf /tmp/test",
        "rm -rf node_modules",
        "DROP TABLE users;",
        "git push origin main --force",
        "git push -f origin feature",
        "TRUNCATE TABLE sessions;",
        "DELETE FROM users;",
    ]

    for cmd in blocked_cases:
        code, err = run_test(cmd)
        assert code == 1, f"Expected '{cmd}' to be BLOCKED, got exit code {code}"
        assert "BLOCKED BY HOOK" in err, f"Expected error message for '{cmd}'"
        print(f"  ✅ Correctly blocked: {cmd}")

    # Should be ALLOWED (exit code 0)
    allowed_cases = [
        "git status",
        "npm install",
        "pnpm build",
        "rm file.txt",
        "DELETE FROM users WHERE id = 42;",
        "SELECT * FROM users;",
    ]

    for cmd in allowed_cases:
        code, err = run_test(cmd)
        assert code == 0, f"Expected '{cmd}' to be ALLOWED, got exit code {code} ({err})"
        print(f"  ✅ Correctly allowed: {cmd}")

    # Verify log file was written
    log_file = Path.home() / ".claude" / "hooks" / "blocked.log"
    assert log_file.exists(), "Log file ~/.claude/hooks/blocked.log was not created!"
    print(f"  ✅ Blocked log verified at {log_file}")

    print("\n🎉 All 13 test assertions PASSED successfully!")

if __name__ == "__main__":
    main()
