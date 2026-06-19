#!/usr/bin/env python3
"""
Ticketable filter — the clean "must fix" list that maps 1:1 to Jira tickets.

Unlike batch_lint.py (which buckets findings by rule), this filter keeps only
findings that carry an exact before->after replacement, so every item can be
submitted as an unambiguous copy update:

    "On {page}, {section}: change '{found}' -> '{suggestion}'."

Judgement prompts ("verify…", "simplify", "rephrase", "avoid…") and findings
without a literal replacement target are excluded — they need human review and
are deliberately not auto-submittable.

Usage:
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --limit 20
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --save
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --json
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from page_lint import fetch_html_metadata, fetch_page_markdown, lint_content, Finding
from batch_lint import fetch_sitemap_urls, should_exclude

# ---------------------------------------------------------------------------
# The ticketable filter — single source of truth for what gets submitted
# ---------------------------------------------------------------------------

# Suggestion text that is a judgement prompt, not a literal drop-in replacement.
# If a finding's suggestion matches any of these it is NOT ticketable.
_HINT_RE = re.compile(
    r"rephrase|simplify|verify|trim|consider|^use\b|^add\b|^avoid\b|"
    r"distinct|descriptive|backed by",
    re.IGNORECASE,
)

# Sections that are shared chrome (nav/footer), repeated on every page.
_NAV_SECTIONS = {
    "Quick links", "Categories", "Partner programs", "Explore Canonical",
    "Industries", "Page Content",
}

# Page paths that are fragments/templates, not real content pages.
_FRAGMENT_RE = re.compile(r"/navigation/|/templates?/|nojs", re.IGNORECASE)


def is_ticketable(f: Finding) -> bool:
    """True if a finding is an exact find->replace, ready to submit as a ticket."""
    if not f.found or not f.suggestion:
        return False
    if f.section in _NAV_SECTIONS:
        return False
    return _HINT_RE.search(f.suggestion) is None


def collect_tickets(urls: list[str]) -> list[dict]:
    """Lint each URL and return the clean, ticketable findings as dicts."""
    tickets: list[dict] = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}", file=sys.stderr)
        try:
            metadata = fetch_html_metadata(url)
            content = fetch_page_markdown(url)
            for f in lint_content(content.splitlines(), metadata):
                if is_ticketable(f):
                    tickets.append({
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
        except Exception as e:
            print(f"  ⚠️  Error: {e}", file=sys.stderr)
    return tickets


def render_markdown(tickets: list[dict], domain: str, pages: int) -> str:
    """Render the ticketable list grouped by page."""
    lines = [
        f"# Ticketable copy fixes – {domain}",
        f"**Date:** {date.today().isoformat()}",
        f"**Pages scanned:** {pages}",
        f"**Clean tickets:** {len(tickets)}",
        "",
        "Every item below is an exact find→replace, ready to submit as a "
        "copy-update ticket. Judgement-call findings are excluded.",
        "",
        "---",
        "",
    ]

    # Rule summary
    from collections import Counter
    by_rule = Counter(t["rule"] for t in tickets)
    lines.append("**By rule:** " + ", ".join(
        f"{rule} ({count})" for rule, count in by_rule.most_common()))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by page
    by_path: dict[str, list[dict]] = {}
    for t in tickets:
        by_path.setdefault(t["path"], []).append(t)

    for path in sorted(by_path):
        lines.append(f"## `{path}`")
        lines.append("")
        for t in by_path[path]:
            lines.append(
                f"- **{t['section']}** | [{t['rule']}] "
                f"`{t['found']}` → `{t['suggestion']}`")
        lines.append("")

    return "\n".join(lines)


def to_bauer(tickets: list[dict]) -> list[dict]:
    """Group tickets by page and emit Bauer-shaped ActionableSuggestions.

    Mirrors canonical/Bauer's internal/gdocs schema: one entry per page
    carries `suggested_url` (Bauer resolves the target template file from it)
    and a list of suggestions in ActionableSuggestion form. We never call
    Bauer — this is a self-contained JSON artifact for them to ingest.
    """
    import hashlib

    by_url: dict[str, list[dict]] = {}
    for t in tickets:
        by_url.setdefault(t["url"], []).append(t)

    pages = []
    for url in sorted(by_url):
        suggestions = []
        for t in by_url[url]:
            before = t["preceding"] + t["found"] + t["following"]
            after = t["preceding"] + t["suggestion"] + t["following"]
            sid = hashlib.sha1(
                f"{t['path']}|{t['preceding']}|{t['found']}".encode()
            ).hexdigest()[:12]
            suggestions.append({
                "id": f"onaur-{sid}",
                "anchor": {
                    "preceding_text": t["preceding"],
                    "following_text": t["following"],
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


def main():
    parser = argparse.ArgumentParser(
        description="Produce the clean, ticketable copy-fix list from a sitemap")
    parser.add_argument("sitemap", help="Sitemap XML URL")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of pages to scan (0 = all)")
    parser.add_argument("--json", action="store_true",
                        help="Print the tickets as JSON instead of markdown")
    parser.add_argument("--bauer", action="store_true",
                        help="Emit Bauer-shaped ActionableSuggestions JSON "
                             "(grouped by page) instead of markdown")
    parser.add_argument("--save", action="store_true",
                        help="Save markdown + JSON to reports/ and push to GitHub")
    args = parser.parse_args()

    print(f"Fetching sitemap: {args.sitemap}", file=sys.stderr)
    all_urls = fetch_sitemap_urls(args.sitemap)
    urls = [u for u in all_urls
            if not should_exclude(u) and not _FRAGMENT_RE.search(u)]
    print(f"Found {len(all_urls)} URLs, {len(urls)} after exclusions",
          file=sys.stderr)

    if args.limit:
        urls = urls[:args.limit]
        print(f"Limited to {args.limit} pages", file=sys.stderr)

    tickets = collect_tickets(urls)
    domain = urlparse(urls[0]).netloc if urls else "unknown"

    if args.bauer:
        output = json.dumps(to_bauer(tickets), indent=2)
    elif args.json:
        output = json.dumps(tickets, indent=2)
    else:
        output = render_markdown(tickets, domain, len(urls))
    print(output)

    print(f"\n✅ {len(tickets)} ticketable fixes found", file=sys.stderr)

    if args.save:
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        slug = domain.replace(".", "-")
        today = date.today().isoformat()
        md_path = report_dir / f"{slug}-tickets-{today}.md"
        json_path = report_dir / f"{slug}-tickets-{today}.json"
        bauer_path = report_dir / f"{slug}-bauer-{today}.json"

        md_path.write_text(render_markdown(tickets, domain, len(urls)) + "\n",
                           encoding="utf-8")
        json_path.write_text(json.dumps(tickets, indent=2) + "\n",
                            encoding="utf-8")
        bauer_path.write_text(json.dumps(to_bauer(tickets), indent=2) + "\n",
                             encoding="utf-8")
        print(f"📄 Saved: {md_path}, {json_path} and {bauer_path}",
              file=sys.stderr)

        subprocess.run(
            ["git", "add", str(md_path), str(json_path), str(bauer_path)],
            check=True)
        subprocess.run(
            ["git", "commit", "-m",
             f"report: ticketable fixes {domain} ({len(tickets)} tickets)"],
            check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Pushed to GitHub", file=sys.stderr)


if __name__ == "__main__":
    main()
