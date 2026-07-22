#!/usr/bin/env python3
"""
Collect approved findings from a triage checklist and output Bauer JSON.

Supports two input modes:
  --file   Read a markdown checklist file (triage-checklist.md)
  --tracking-issue  Read GitHub Issues via the API (requires GITHUB_TOKEN)

Usage:
    python3 scripts/collect_approved.py --file reports/triage-checklist.md
    python3 scripts/collect_approved.py --file reports/triage-checklist.md --output reports/approved-bauer.json

    export GITHUB_TOKEN=ghp_...
    python3 scripts/collect_approved.py --tracking-issue 42

Environment:
    GITHUB_TOKEN — Only needed for --tracking-issue mode
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

GITHUB_API = "https://api.github.com"


def github_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_issue(repo: str, issue_number: int) -> dict:
    """Fetch a single issue."""
    url = f"{GITHUB_API}/repos/{repo}/issues/{issue_number}"
    req = urllib.request.Request(url, headers=github_headers())
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def parse_checklist_file(path: str) -> tuple[list[dict], list[dict]]:
    """Parse a markdown checklist file and return (approved, archived)."""
    approved = []
    archived = []
    current_url = ""

    with open(path, encoding="utf-8") as f:
        for line in f:
            # Track current page URL
            url_match = re.match(r"\*\*Page:\*\* (https?://\S+)", line)
            if url_match:
                current_url = url_match.group(1)
                continue

            m = CHECKBOX_RE.match(line)
            if m and current_url:
                finding = {
                    "url": current_url,
                    "path": urlparse(current_url).path or "/",
                    "rule": m.group("rule"),
                    "section": m.group("section").strip(),
                    "found": m.group("found").replace("\\`", "`"),
                    "suggestion": m.group("suggestion").replace("\\`", "`"),
                }
                if m.group("checked").strip().lower() == "x":
                    approved.append(finding)
                else:
                    archived.append(finding)

    return approved, archived


# ---------------------------------------------------------------------------
# Parse checked items from GitHub issue body
# ---------------------------------------------------------------------------

# Matches: - [x] **[rule]** section: `found` → `suggestion`
CHECKBOX_RE = re.compile(
    r"^- \[(?P<checked>[xX ])\] \*\*\[(?P<rule>[^\]]+)\]\*\* "
    r"(?P<section>[^:]+): `(?P<found>[^`]+)` → `(?P<suggestion>[^`]+)`",
    re.MULTILINE,
)


def parse_issue_findings(body: str) -> tuple[list[dict], list[dict]]:
    """Parse issue body and return (approved, archived) findings."""
    approved = []
    archived = []

    # Extract page URL from body
    url_match = re.search(r"\*\*Page:\*\* (https?://\S+)", body)
    page_url = url_match.group(1) if url_match else ""

    for m in CHECKBOX_RE.finditer(body):
        finding = {
            "url": page_url,
            "path": urlparse(page_url).path or "/",
            "rule": m.group("rule"),
            "section": m.group("section").strip(),
            "found": m.group("found").replace("\\`", "`"),
            "suggestion": m.group("suggestion").replace("\\`", "`"),
        }

        if m.group("checked").strip().lower() == "x":
            approved.append(finding)
        else:
            archived.append(finding)

    return approved, archived


# ---------------------------------------------------------------------------
# Parse tracking issue to find page issue numbers
# ---------------------------------------------------------------------------

PAGE_ISSUE_RE = re.compile(r"^- \[[xX ]\] #(\d+)", re.MULTILINE)


def get_page_issue_numbers(tracking_body: str) -> list[int]:
    """Extract issue numbers from the tracking issue."""
    return [int(m.group(1)) for m in PAGE_ISSUE_RE.finditer(tracking_body)]


# ---------------------------------------------------------------------------
# Bauer output format
# ---------------------------------------------------------------------------

def to_bauer(approved: list[dict]) -> list[dict]:
    """Convert approved findings to Bauer-shaped ActionableSuggestions JSON."""
    by_url: dict[str, list[dict]] = {}
    for item in approved:
        by_url.setdefault(item["url"], []).append(item)

    pages = []
    for url, items in sorted(by_url.items()):
        suggestions = []
        for t in items:
            before = t.get("preceding", "") + t["found"] + t.get("following", "")
            after = t.get("preceding", "") + t["suggestion"] + t.get("following", "")
            sid = hashlib.sha256(
                f"{url}:{t['found']}:{t['suggestion']}".encode()
            ).hexdigest()[:12]
            suggestions.append({
                "id": f"onaur-{sid}",
                "anchor": {
                    "preceding_text": t.get("preceding", ""),
                    "following_text": t.get("following", ""),
                },
                "change": {
                    "type": "replace",
                    "original_text": t["found"],
                    "new_text": t["suggestion"],
                },
                "verification": {
                    "text_before_change": before,
                    "text_after_change": after,
                },
                "location": {
                    "section": "Body",
                    "parent_heading": t["section"],
                    "in_table": False,
                    "in_metadata": False,
                },
            })
        pages.append({"suggested_url": url, "suggestions": suggestions})
    return pages


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Collect approved triage findings and output Bauer JSON")
    parser.add_argument("--tracking-issue", type=int, default=None,
                        help="Issue number of the tracking issue (requires GITHUB_TOKEN)")
    parser.add_argument("--file", type=str, default=None,
                        help="Path to a markdown checklist file")
    parser.add_argument("--repo", default="canonical/o-naur",
                        help="GitHub repo (default: canonical/o-naur)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file path (default: stdout)")
    parser.add_argument("--archive-output", type=str, default=None,
                        help="Write archived (unchecked) items to this file")
    args = parser.parse_args()

    if not args.file and not args.tracking_issue:
        parser.error("Provide either --file or --tracking-issue")

    if args.file:
        # File mode — parse the markdown checklist
        print(f"Reading checklist: {args.file}", file=sys.stderr)
        all_approved, all_archived = parse_checklist_file(args.file)
    else:
        # GitHub Issues mode
        print(f"Fetching tracking issue #{args.tracking_issue}...", file=sys.stderr)
        tracking = get_issue(args.repo, args.tracking_issue)
        page_numbers = get_page_issue_numbers(tracking["body"])
        print(f"Found {len(page_numbers)} page issues to check", file=sys.stderr)

        all_approved = []
        all_archived = []
        for i, issue_num in enumerate(page_numbers, 1):
            print(f"[{i}/{len(page_numbers)}] Reading issue #{issue_num}...",
                  file=sys.stderr)
            issue = get_issue(args.repo, issue_num)
            approved, archived = parse_issue_findings(issue["body"])
            all_approved.extend(approved)
            all_archived.extend(archived)

    print(f"\n✅ {len(all_approved)} approved → Bauer", file=sys.stderr)
    print(f"📦 {len(all_archived)} archived (unchecked)", file=sys.stderr)

    # Output
    bauer_json = json.dumps(to_bauer(all_approved), indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(bauer_json + "\n")
        print(f"📄 Written to {args.output}", file=sys.stderr)
    else:
        print(bauer_json)

    if args.archive_output and all_archived:
        with open(args.archive_output, "w", encoding="utf-8") as f:
            json.dump(all_archived, f, indent=2)
            f.write("\n")
        print(f"📦 Archive written to {args.archive_output}", file=sys.stderr)


if __name__ == "__main__":
    main()
