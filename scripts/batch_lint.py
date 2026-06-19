#!/usr/bin/env python3
"""
Batch page linter — scans all pages on a site from its sitemap.

Fetches the sitemap, filters out excluded paths, runs the linter on each page,
and produces a consolidated report.

Usage:
    python3 scripts/batch_lint.py https://canonical.com/sitemap_tree.xml
    python3 scripts/batch_lint.py https://canonical.com/sitemap_tree.xml --save
    python3 scripts/batch_lint.py https://canonical.com/sitemap_tree.xml --limit 10
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

# Import the linter
sys.path.insert(0, str(Path(__file__).parent))
from page_lint import (
    fetch_html_metadata, fetch_page_markdown, lint_content, Finding, SEVERITY_ICONS
)

# ---------------------------------------------------------------------------
# Exclusion patterns — paths to skip
# ---------------------------------------------------------------------------

EXCLUDE_PATTERNS = [
    r"/docs/",
    r"/docs$",
    r"/blog/",
    r"/blog$",
    r"/careers/",
    r"/careers$",
    r"/cve/",
    r"/cve$",
    r"/security/cves",
    r"/contact-us$",
    r"/thank-you",
    r"/login",
    r"/sitemap",
]


def should_exclude(url: str) -> bool:
    """Check if a URL matches any exclusion pattern."""
    path = urlparse(url).path
    return any(re.search(p, path) for p in EXCLUDE_PATTERNS)


# ---------------------------------------------------------------------------
# Sitemap fetching
# ---------------------------------------------------------------------------

def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Fetch URLs from a sitemap XML."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", sitemap_url],
            capture_output=True, text=True, timeout=20
        )
        urls = re.findall(r'<loc>([^<]+)</loc>', result.stdout)
        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Batch lint pages from a sitemap")
    parser.add_argument("sitemap", help="Sitemap XML URL")
    parser.add_argument("--save", action="store_true", help="Save report and push to GitHub")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of pages to scan (0 = all)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Additional path patterns to exclude")
    parser.add_argument("--actionable", action="store_true",
                        help="Only show auto-fixable issues (spelling, product names, banned words)")
    args = parser.parse_args()

    # Add custom exclusions
    for pattern in args.exclude:
        EXCLUDE_PATTERNS.append(pattern)

    # Fetch sitemap
    print(f"Fetching sitemap: {args.sitemap}", file=sys.stderr)
    all_urls = fetch_sitemap_urls(args.sitemap)
    urls = [u for u in all_urls if not should_exclude(u)]

    print(f"Found {len(all_urls)} URLs, {len(urls)} after exclusions", file=sys.stderr)

    if args.limit:
        urls = urls[:args.limit]
        print(f"Limited to {args.limit} pages", file=sys.stderr)

    # Run linter on each page
    all_findings: list[tuple[str, Finding]] = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}", file=sys.stderr)
        try:
            metadata = fetch_html_metadata(url)
            content = fetch_page_markdown(url)
            lines = content.splitlines()
            findings = lint_content(lines, metadata)
            for f in findings:
                all_findings.append((url, f))
        except Exception as e:
            print(f"  ⚠️  Error: {e}", file=sys.stderr)

    # Exclude shared nav/footer sections (same on every page)
    NAV_SECTIONS = {
        "Quick links", "Categories", "Partner programs", "Explore Canonical",
        "Industries",  # shared component repeated on every page
        "Page Content",  # generic pre-heading content (usually nav/JS artifacts)
    }
    all_findings = [(url, f) for url, f in all_findings
                    if f.section not in NAV_SECTIONS]

    # Split into must-fix vs nice-to-fix
    MUST_FIX_RULES = {
        "uk-spelling", "house-style", "product-names", "punctuation",
        "placeholder", "metadata", "character-limits", "security-claims",
    }
    # Nice-to-fix: everything else that's actionable
    NICE_TO_FIX_RULES = {
        "banned-words", "flowery-language", "superlatives",
        "link-text", "duplicate-cta", "link-consistency",
        "heading-levels", "number-formatting",
    }

    if args.actionable:
        all_findings = [(url, f) for url, f in all_findings
                        if f.rule in MUST_FIX_RULES or f.rule in NICE_TO_FIX_RULES]

    must_fix = [(url, f) for url, f in all_findings if f.rule in MUST_FIX_RULES]
    nice_to_fix = [(url, f) for url, f in all_findings if f.rule in NICE_TO_FIX_RULES]

    # Generate consolidated report
    domain = urlparse(urls[0]).netloc if urls else "unknown"
    report_lines = []
    report_lines.append(f"# Batch lint report – {domain}")
    report_lines.append(f"**Date:** {date.today().isoformat()}")
    report_lines.append(f"**Pages scanned:** {len(urls)}")
    report_lines.append(f"**Must fix:** {len(must_fix)} | **Nice to fix:** {len(nice_to_fix)}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # Must fix section
    report_lines.append("## 🔴 Must fix")
    report_lines.append("")
    report_lines.append("Typos, UK spelling, product names, punctuation, missing metadata, placeholders.")
    report_lines.append("")

    if not must_fix:
        report_lines.append("✅ None found.")
        report_lines.append("")
    else:
        for url, f in must_fix:
            path = urlparse(url).path or "/"
            icon = SEVERITY_ICONS.get(f.severity, "❓")
            report_lines.append(f"- {icon} `{path}` | **{f.section}** – {f.message}")
            if f.found:
                report_lines.append(f"  - Found: `{f.found}`")
        report_lines.append("")

    report_lines.append("---")
    report_lines.append("")

    # Nice to fix section
    report_lines.append("## 🟡 Nice to fix")
    report_lines.append("")
    report_lines.append("Banned/flowery words, vague link text, superlatives, heading structure, number formatting.")
    report_lines.append("")

    if not nice_to_fix:
        report_lines.append("✅ None found.")
        report_lines.append("")
    else:
        for url, f in nice_to_fix:
            path = urlparse(url).path or "/"
            icon = SEVERITY_ICONS.get(f.severity, "❓")
            report_lines.append(f"- {icon} `{path}` | **{f.section}** – {f.message}")
            if f.found:
                report_lines.append(f"  - Found: `{f.found}`")
        report_lines.append("")

    report = "\n".join(report_lines)
    print(report)

    # Save and push
    if args.save:
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        slug = domain.replace(".", "-")
        filename = f"{slug}-batch-{date.today().isoformat()}.md"
        report_path = report_dir / filename
        report_path.write_text(report + "\n", encoding="utf-8")
        print(f"\n📄 Report saved: {report_path}", file=sys.stderr)

        subprocess.run(["git", "add", str(report_path)], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"report: batch lint {domain} ({len(urls)} pages)"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("✅ Pushed to GitHub", file=sys.stderr)


if __name__ == "__main__":
    main()
