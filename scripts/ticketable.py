#!/usr/bin/env python3
"""
Ticketable filter — the clean "must fix" list that maps 1:1 to Jira tickets.

Unlike batch_lint.py (which buckets findings by rule), this filter keeps only
findings that carry an exact before->after replacement, so every item can be
submitted as an unambiguous copy update:

    "On {page}, {section}: change '{found}' -> '{suggestion}'."

Judgement prompts ("verify…", "simplify", "rephrase", "avoid…") and findings
without a literal replacement target are excluded — they need human review and
are deliberately not auto-submittable. So is flowery-language: each swap is a
literal word replacement, but which words read as "flowery" vs. just plain is
a judgement call, not an objective style-guide violation like UK spelling.

Two-step workflow — nothing reaches Bauer without a human checking it first:

    1. scan   — crawl a sitemap, write a candidate checklist to reports/
    2. approve — read back your checked-off items, emit the Bauer artifact
                 for approved items only

Usage:
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --save
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --limit 20
    python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --json

    # after checking off approved items in the saved *-tickets-*.md:
    python3 scripts/ticketable.py --approve reports/canonical-com-tickets-2026-07-02.md --save
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
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

# Rules that are judgement calls even when they carry a literal suggestion —
# excluded from the ticketable list regardless of what is_ticketable's other
# checks would allow.
_JUDGEMENT_RULES = {"flowery-language"}

# Sections that are shared chrome (nav/footer), repeated on every page.
_NAV_SECTIONS = {
    "Quick links", "Categories", "Partner programs", "Explore Canonical",
    "Industries", "Page Content",
}

# Page paths that are fragments/templates, not real content pages.
_FRAGMENT_RE = re.compile(r"/navigation/|/templates?/|nojs", re.IGNORECASE)

# Checkbox line format used in the reviewed markdown checklist, e.g.:
#   - [x] `a1b2c3d4e5f6` **Section** | [rule] `found` -> `suggestion`
_CHECKBOX_RE = re.compile(r"^-\s*\[([xX ])\]\s*`([a-f0-9]{12})`")


def is_ticketable(f: Finding) -> bool:
    """True if a finding is an exact find->replace, ready to submit as a ticket."""
    if f.rule in _JUDGEMENT_RULES:
        return False
    if not f.found or not f.suggestion:
        return False
    if f.section in _NAV_SECTIONS:
        return False
    return _HINT_RE.search(f.suggestion) is None


def ticket_id(t: dict) -> str:
    """Stable id for a ticket, used to match checklist approvals back to candidates."""
    return hashlib.sha1(
        f"{t['path']}|{t['preceding']}|{t['found']}".encode()
    ).hexdigest()[:12]


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
                    t = {
                        "url": url,
                        "path": urlparse(url).path or "/",
                        "section": f.section,
                        "rule": f.rule,
                        "found": f.found,
                        "suggestion": f.suggestion,
                        "message": f.message,
                        "preceding": f.preceding,
                        "following": f.following,
                    }
                    t["id"] = ticket_id(t)
                    tickets.append(t)
        except Exception as e:
            print(f"  ⚠️  Error: {e}", file=sys.stderr)
    return tickets


def render_markdown(tickets: list[dict], domain: str, pages: int) -> str:
    """Render the candidate checklist grouped by page, ready for review."""
    lines = [
        f"# Ticketable copy fixes – {domain}",
        f"**Date:** {date.today().isoformat()}",
        f"**Pages scanned:** {pages}",
        f"**Candidates:** {len(tickets)}",
        "",
        "Every item below is an exact find→replace. Judgement-call findings "
        "(including flowery-language) are excluded from this list entirely.",
        "",
        "**Review before submitting:** check the box for each fix you approve, "
        "commit this file, then run:",
        "",
        "```",
        f"python3 scripts/ticketable.py --approve reports/{domain.replace('.', '-')}"
        f"-tickets-{date.today().isoformat()}.md --save",
        "```",
        "",
        "Unchecked items are treated as rejected and will not be submitted.",
        "",
        "---",
        "",
    ]

    by_rule = Counter(t["rule"] for t in tickets)
    lines.append("**By rule:** " + ", ".join(
        f"{rule} ({count})" for rule, count in by_rule.most_common()))
    lines.append("")
    lines.append("---")
    lines.append("")

    by_path: dict[str, list[dict]] = {}
    for t in tickets:
        by_path.setdefault(t["path"], []).append(t)

    for path in sorted(by_path):
        lines.append(f"## `{path}`")
        lines.append("")
        for t in by_path[path]:
            lines.append(
                f"- [ ] `{t['id']}` **{t['section']}** | [{t['rule']}] "
                f"`{t['found']}` → `{t['suggestion']}`")
        lines.append("")

    return "\n".join(lines)


def parse_approved_ids(review_path: Path) -> set[str]:
    """Read a reviewed checklist and return the set of approved ticket ids.

    Approved = the checkbox is checked (`- [x] `id`` ...`). Anything left
    unchecked, including items the reviewer never got to, is not approved.
    """
    approved = set()
    for line in review_path.read_text(encoding="utf-8").splitlines():
        m = _CHECKBOX_RE.match(line.strip())
        if m and m.group(1).lower() == "x":
            approved.add(m.group(2))
    return approved


def to_bauer(tickets: list[dict], approved_ids: set[str] | None = None) -> list[dict]:
    """Group tickets by page and emit Bauer-shaped ActionableSuggestions.

    Mirrors canonical/Bauer's internal/gdocs schema: one entry per page
    carries `suggested_url` (Bauer resolves the target template file from it)
    and a list of suggestions in ActionableSuggestion form. We never call
    Bauer — this is a self-contained JSON artifact for them to ingest.

    If approved_ids is given, only tickets whose id is in that set are
    included — this is how the human-review gate is enforced.
    """
    if approved_ids is not None:
        tickets = [t for t in tickets if t["id"] in approved_ids]

    by_url: dict[str, list[dict]] = {}
    for t in tickets:
        by_url.setdefault(t["url"], []).append(t)

    pages = []
    for url in sorted(by_url):
        suggestions = []
        for t in by_url[url]:
            before = t["preceding"] + t["found"] + t["following"]
            after = t["preceding"] + t["suggestion"] + t["following"]
            suggestions.append({
                "id": f"onaur-{t['id']}",
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


def cmd_scan(args):
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

    if args.json:
        output = json.dumps(tickets, indent=2)
    else:
        output = render_markdown(tickets, domain, len(urls))
    print(output)

    print(f"\n✅ {len(tickets)} candidates found — review and check off approved "
          f"items before running --approve", file=sys.stderr)

    if args.save:
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        slug = domain.replace(".", "-")
        today = date.today().isoformat()
        md_path = report_dir / f"{slug}-tickets-{today}.md"
        json_path = report_dir / f"{slug}-tickets-{today}.json"

        md_path.write_text(render_markdown(tickets, domain, len(urls)) + "\n",
                           encoding="utf-8")
        json_path.write_text(json.dumps(tickets, indent=2) + "\n",
                            encoding="utf-8")
        print(f"📄 Saved: {md_path} and {json_path}", file=sys.stderr)

        subprocess.run(
            # -f: reports/*.md and *.json are gitignored by default (see
            # .gitignore) so new dated filenames are untracked; force-add
            # the deliverables we explicitly want committed.
            ["git", "add", "-f", str(md_path), str(json_path)], check=True)
        subprocess.run(
            ["git", "commit", "-m",
             f"report: candidate ticket list {domain} "
             f"({len(tickets)} candidates, pending review)"],
            check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Pushed candidate list to GitHub — nothing sent to Bauer yet",
              file=sys.stderr)


def cmd_approve(args):
    review_path = Path(args.approve)
    candidates_path = review_path.with_suffix(".json")
    if not candidates_path.exists():
        sys.exit(f"Candidates file not found: {candidates_path}\n"
                  f"(expected the *-tickets-*.json saved alongside {review_path})")

    all_tickets = json.loads(candidates_path.read_text(encoding="utf-8"))
    all_ids = {t["id"] for t in all_tickets}
    approved_ids = parse_approved_ids(review_path)

    stale = approved_ids - all_ids
    if stale:
        print(f"⚠️  {len(stale)} checked id(s) in {review_path} don't match "
              f"any candidate in {candidates_path} — ignoring them",
              file=sys.stderr)
        approved_ids -= stale

    if not approved_ids:
        sys.exit("No approved items found (no checked boxes) — nothing to submit.")

    bauer_pages = to_bauer(all_tickets, approved_ids)
    approved_count = sum(len(p["suggestions"]) for p in bauer_pages)
    output = json.dumps(bauer_pages, indent=2)
    print(output)
    print(f"\n✅ {approved_count} approved fixes ready for Bauer "
          f"(of {len(all_tickets)} candidates)", file=sys.stderr)

    if args.save:
        domain = urlparse(all_tickets[0]["url"]).netloc if all_tickets else "unknown"
        slug = domain.replace(".", "-")
        today = date.today().isoformat()
        bauer_path = Path("reports") / f"{slug}-bauer-{today}.json"
        bauer_path.write_text(output + "\n", encoding="utf-8")

        subprocess.run(["git", "add", "-f", str(bauer_path)], check=True)
        subprocess.run(
            ["git", "commit", "-m",
             f"report: approved Bauer submission {domain} "
             f"({approved_count} fixes)"],
            check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"📄 Saved & pushed: {bauer_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Produce the clean, ticketable copy-fix list from a sitemap, "
                     "gated on human review before anything reaches Bauer")
    parser.add_argument("sitemap", nargs="?",
                        help="Sitemap XML URL (omit when using --approve)")
    parser.add_argument("--approve", metavar="REVIEW_MD",
                        help="Path to a reviewed checklist (*-tickets-*.md); "
                             "emits the Bauer artifact for approved items only "
                             "and skips scanning")
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit number of pages to scan (0 = all)")
    parser.add_argument("--json", action="store_true",
                        help="Print candidates as JSON instead of markdown "
                             "(scan mode only)")
    parser.add_argument("--save", action="store_true",
                        help="Save output to reports/ and push to GitHub")
    args = parser.parse_args()

    if args.approve:
        cmd_approve(args)
    else:
        if not args.sitemap:
            parser.error("sitemap is required unless --approve is given")
        cmd_scan(args)


if __name__ == "__main__":
    main()
