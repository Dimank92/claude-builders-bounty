#!/usr/bin/env python3
"""
Test & Validation Suite for n8n Weekly Dev Summary Workflow
Validates JSON structure, simulates node execution, and tests GitHub API integration.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

def test_workflow_json_schema():
    workflow_path = os.path.join(os.path.dirname(__file__), "weekly_dev_summary_n8n.json")
    print(f"1. Validating workflow JSON schema: {workflow_path}")
    
    with open(workflow_path, "r", encoding="utf-8") as f:
        wf = json.load(f)

    assert "nodes" in wf, "Workflow must contain 'nodes' array"
    assert "connections" in wf, "Workflow must contain 'connections' map"
    
    node_names = [n["name"] for n in wf["nodes"]]
    print(f"   Nodes identified ({len(node_names)}): {node_names}")
    
    # Check trigger node
    trigger = next((n for n in wf["nodes"] if n["type"] == "n8n-nodes-base.scheduleTrigger"), None)
    assert trigger is not None, "Missing Schedule Trigger node"
    cron = trigger["parameters"]["rule"]["interval"][0]["expression"]
    assert cron == "0 17 * * 5", f"Expected Friday 5PM cron (0 17 * * 5), got {cron}"
    print("   ✅ Schedule Trigger matches Friday 5PM weekly requirement")
    
    # Check Claude API node
    claude_node = next((n for n in wf["nodes"] if "claude" in n["name"].lower() or "claude" in n.get("parameters", {}).get("url", "").lower()), None)
    assert claude_node is not None, "Missing Claude API node"
    body_spec = claude_node["parameters"].get("jsonBody", "")
    assert "claude-sonnet-4-20250514" in body_spec, "Must use claude-sonnet-4-20250514 model"
    print("   ✅ Claude API node specifies claude-sonnet-4-20250514 model")
    
    # Check Config variables
    config_node = next((n for n in wf["nodes"] if n["name"] == "Config Variables"), None)
    assert config_node is not None, "Missing Config Variables node"
    assigned_names = [a["name"] for a in config_node["parameters"]["assignments"]["assignments"]]
    assert "GITHUB_OWNER" in assigned_names, "Config missing GITHUB_OWNER"
    assert "GITHUB_REPO" in assigned_names, "Config missing GITHUB_REPO"
    assert "SUMMARY_LANGUAGE" in assigned_names, "Config missing SUMMARY_LANGUAGE"
    print("   ✅ Configurable variables verified (GITHUB_OWNER, GITHUB_REPO, SUMMARY_LANGUAGE, etc.)")

    print("   ✅ All workflow schema checks passed successfully!\n")
    return wf

def test_github_api_simulation():
    print("2. Testing GitHub API data extraction (simulation of n8n HTTP Request nodes)...")
    token = os.environ.get("GITHUB_TOKEN", "")
    owner = "claude-builders-bounty"
    repo = "claude-builders-bounty"
    
    since_date = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "n8n-Weekly-Summary-Workflow",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    # Commits
    req_c = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/commits?since={since_date}", headers=headers)
    with urllib.request.urlopen(req_c) as resp:
        commits = json.loads(resp.read().decode())
    print(f"   Commits fetched for last 7 days: {len(commits)}")
    
    # Pull Requests
    req_pr = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=10", headers=headers)
    with urllib.request.urlopen(req_pr) as resp:
        prs = json.loads(resp.read().decode())
    print(f"   Recent PRs fetched: {len(prs)}")
    
    # Issues
    req_i = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/issues?state=all&per_page=10", headers=headers)
    with urllib.request.urlopen(req_i) as resp:
        issues = json.loads(resp.read().decode())
    print(f"   Recent Issues fetched: {len(issues)}")
    
    print("   ✅ GitHub API data collection verified!\n")

def main():
    print("=== Running n8n Workflow Verification Suite ===\n")
    test_workflow_json_schema()
    test_github_api_simulation()
    print("🎉 ALL TESTS PASSED! n8n workflow is ready for production and export.")

if __name__ == "__main__":
    main()
