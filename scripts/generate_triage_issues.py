#!/usr/bin/env python3
"""
Generate GitHub Issues for triage of ticketable copy-lint findings.

Runs the ticketable scan across sitemap(s), then creates:
  - One GitHub Issue per page (with checkboxes for each finding)
  - One parent tracking issue linking all page issues

Usage:
    export GITHUB_TOKEN=ghp_...
    python3 scripts/generate_triage_issues.py https://canonical.com/sitemap_tree.xml
    python3 scripts/generate_triage_issues.py https://canonical.com/sitemap_tree.xml https://ubuntu.com/sitemap_tree.xml
    python3 scripts/generate_triage_issues.py https://canonical.com/sitemap_tree.xml --repo canonical/o-naur
    python3 scripts/generate_triage_issues.py --dry-run https://canonical.com/sitemap_tree.xml

Environment:
    GITHUB_TOKEN — Personal access token with repo scope
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from page_lint import fetch_html_metadata, fetch_page_markdown, lint_content
from batch_lint import fetch_sitemap_urls, should_exclude
from ticketable import is_ticketable, _FRAGMENT_RE


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


def create_issue(repo: str, title: str, body: str, labels: list[str] | None = None) -> dict:
    """Create a GitHub issue and return the response JSON."""
    url = f"{GITHUB_API}/repos/{repo}/issues"
    payload: dict = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels

    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=github_headers(), method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"GitHub API error {e.code}: {error_body}", file=sys.stderr)
        raise


# ---------------------------------------------------------------------------
# Scan and group findings
# ---------------------------------------------------------------------------

def scan_sitemaps(sitemap_urls: list[str], limit: int = 0) -> dict[str, list[dict]]:
    """Scan sitemaps and return ticketable findings grouped by page URL."""
    all_urls: list[str] = []
    for sitemap_url in sitemap_urls:
        print(f"Fetching sitemap: {sitemap_url}", file=sys.stderr)
        urls = fetch_sitemap_urls(sitemap_url)
        all_urls.extend(urls)

    # Apply exclusions
    urls = [u for u in all_urls if not should_exclude(u) and not _FRAGMENT_RE.search(u)]
    print(f"Found {len(all_urls)} URLs, {len(urls)} after exclusions", file=sys.stderr)

    if limit:
        urls = urls[:limit]
        print(f"Limited to {limit} pages", file=sys.stderr)

    # Scan each page
    by_page: dict[str, list[dict]] = {}
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}", file=sys.stderr)
        try:
            metadata = fetch_html_metadata(url)
            content = fetch_page_markdown(url)
            findings = lint_content(content.splitlines(), metadata)
            ticketable = []
            for f in findings:
                if is_ticketable(f):
                    ticketable.append({
                        "url": url,
                        "path": urlparse(url).path or "/",
                        "section": f.section,
                        "rule": f.rule,
                        "found": f.found,
                        "suggestion": f.suggestion,
                        "message": f.message,
                        "preceding": f.preceding,
                        "following": f.following,
                    })
            if ticketable:
                by_page[url] = ticketable
        except Exception as e:
            print(f"  ⚠️  Error: {e}", file=sys.stderr)

    return by_page


# ---------------------------------------------------------------------------
# Issue body formatting
# ---------------------------------------------------------------------------

def format_page_issue_body(url: str, findings: list[dict]) -> str:
    """Format the body of a per-page triage issue."""
    lines = [
        f"**Page:** {url}",
        f"**Findings:** {len(findings)}",
        f"**Scanned:** {date.today().isoformat()}",
        "",
        "Check the items you want to send to Bauer for fixing. "
        "Unchecked items will be archived when triage is complete.",
        "",
        "---",
        "",
    ]

    for t in findings:
        escaped_found = t["found"].replace("`", "\\`")
        escaped_suggestion = t["suggestion"].replace("`", "\\`")
        lines.append(
            f"- [ ] **[{t['rule']}]** {t['section']}: "
            f"`{escaped_found}` → `{escaped_suggestion}`"
        )

    return "\n".join(lines)


def format_tracking_issue_body(
    page_issues: list[tuple[str, int, int]],  # (url, finding_count, issue_number)
    total_findings: int,
) -> str:
    """Format the parent tracking issue body."""
    lines = [
        f"## Summary",
        f"- 📄 **{len(page_issues)}** pages with findings",
        f"- 🔍 **{total_findings}** total ticketable items",
        f"- 📅 Scanned: {date.today().isoformat()}",
        "",
        "Check off each page once you've finished reviewing its findings.",
        "",
        "---",
        "",
        "## Pages to review",
        "",
    ]

    for url, count, issue_num in page_issues:
        path = urlparse(url).path or "/"
        domain = urlparse(url).netloc
        lines.append(f"- [ ] #{issue_num} `{domain}{path}` ({count} findings)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scan sitemaps and create GitHub triage issues for ticketable findings")
    parser.add_argument("sitemaps", nargs="+", help="Sitemap XML URL(s) to scan")
    parser.add_argument("--repo", default="canonical/o-naur",
                        help="GitHub repo for issues (default: canonical/o-naur)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of pages to scan (0 = all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print issue bodies without creating them on GitHub")
    parser.add_argument("--labels", nargs="*", default=["copy-lint", "triage"],
                        help="Labels to apply to issues")
    args = parser.parse_args()

    # Scan
    by_page = scan_sitemaps(args.sitemaps, limit=args.limit)
    total_findings = sum(len(f) for f in by_page.values())
    print(f"\n✅ {total_findings} ticketable findings across {len(by_page)} pages",
          file=sys.stderr)

    if not by_page:
        print("No findings — nothing to do.", file=sys.stderr)
        return

    if args.dry_run:
        print("\n=== DRY RUN — would create these issues ===\n")
        for url, findings in sorted(by_page.items()):
            path = urlparse(url).path or "/"
            domain = urlparse(url).netloc
            title = f"[copy-lint] {domain}{path}"
            body = format_page_issue_body(url, findings)
            print(f"### {title}")
            print(body)
            print("\n---\n")
        print("### [tracking] Copy lint triage")
        print("(Would link to all page issues above)")
        return

    # Create per-page issues
    page_issues: list[tuple[str, int, int]] = []
    for url, findings in sorted(by_page.items()):
        path = urlparse(url).path or "/"
        domain = urlparse(url).netloc
        title = f"[copy-lint] {domain}{path}"
        body = format_page_issue_body(url, findings)

        print(f"Creating issue: {title}", file=sys.stderr)
        result = create_issue(args.repo, title, body, labels=args.labels)
        issue_num = result["number"]
        page_issues.append((url, len(findings), issue_num))

        # Rate limit: stay well under 30 requests/minute for secondary rate limits
        time.sleep(2)

    # Create tracking issue
    tracking_body = format_tracking_issue_body(page_issues, total_findings)
    tracking_title = f"Copy lint triage: {date.today().isoformat()}"
    print(f"Creating tracking issue: {tracking_title}", file=sys.stderr)
    tracking = create_issue(args.repo, tracking_title, tracking_body,
                            labels=args.labels + ["tracking"])

    print(f"\n🎉 Done! Tracking issue: {tracking['html_url']}", file=sys.stderr)


if __name__ == "__main__":
    main()
