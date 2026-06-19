#!/usr/bin/env python3
"""
Page linter — deterministic UX content checks for live web pages.

Fetches a URL (or reads a pre-fetched markdown file), then runs Canonical
style and UX checks on the visible text content.

Adapted from the copy doc linter in canonical/automated-ux-qa-checklist-and-quality-standards.

Usage:
    python page_lint.py <URL>
    python page_lint.py <URL> --json
    python page_lint.py --file <path-to-markdown.md>
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    rule: str
    severity: str  # critical, needs-work, minor
    section: str
    message: str
    found: str = ""
    suggestion: str = ""
    line: int = 0


# ---------------------------------------------------------------------------
# Section parser (for WebFetch-style markdown from live pages)
# ---------------------------------------------------------------------------

def identify_section(line: str, prev_section: str) -> str:
    """Infer page section from markdown headings and landmark hints."""
    stripped = line.strip()

    # Markdown headings become section markers
    m = re.match(r'^(#{1,6})\s+(.*)', stripped)
    if m:
        heading_text = m.group(2).strip()
        if heading_text:
            return heading_text

    # Common landmark patterns in WebFetch output
    lower = stripped.lower()
    if lower in ("navigation", "nav", "header", "footer", "main"):
        return stripped.title()

    return prev_section


def parse_sections(lines: list[str]) -> list[tuple[str, int, str]]:
    """Return list of (section_name, line_number, line_text)."""
    result = []
    current_section = "Page Content"
    for i, line in enumerate(lines, 1):
        new_section = identify_section(line, current_section)
        if new_section != current_section:
            current_section = new_section
        result.append((current_section, i, line))
    return result


# ---------------------------------------------------------------------------
# HTML metadata extraction (via curl)
# ---------------------------------------------------------------------------

def fetch_html_metadata(url: str) -> dict[str, str]:
    """Extract title and meta description from a live URL using curl."""
    metadata = {}
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        html = result.stdout

        # Extract <title>
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if title_match:
            metadata["page title"] = re.sub(r'\s+', ' ', title_match.group(1)).strip()

        # Extract meta description
        desc_match = re.search(
            r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
            html, re.IGNORECASE
        )
        if not desc_match:
            desc_match = re.search(
                r'<meta\s+[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']',
                html, re.IGNORECASE
            )
        if desc_match:
            metadata["page description"] = desc_match.group(1).strip()

    except (subprocess.TimeoutExpired, Exception):
        pass

    return metadata


# ---------------------------------------------------------------------------
# Metadata checks (adapted for HTML pages)
# ---------------------------------------------------------------------------

CHAR_LIMITS = {
    "page title": 60,
    "page description": 160,
}


def check_page_metadata(metadata: dict[str, str]) -> list[Finding]:
    """Check page title and meta description presence and length."""
    findings = []

    if not metadata.get("page title"):
        findings.append(Finding(
            rule="metadata",
            severity="critical",
            section="Metadata",
            message="Page has no <title> tag",
        ))

    if not metadata.get("page description"):
        findings.append(Finding(
            rule="metadata",
            severity="needs-work",
            section="Metadata",
            message="Page has no meta description",
        ))

    for key, val in metadata.items():
        limit = CHAR_LIMITS.get(key)
        if limit and val and len(val) > limit:
            findings.append(Finding(
                rule="character-limits",
                severity="needs-work",
                section="Metadata",
                message=f"{key} is {len(val)} characters (limit: {limit})",
                found=val[:80] + ("..." if len(val) > 80 else ""),
                suggestion=f"Trim to {limit} characters or fewer",
            ))

    return findings


# ---------------------------------------------------------------------------
# Style guide: UK spelling variants
# ---------------------------------------------------------------------------

ISE_WORDS = [
    (r"\borganise[sd]?\b", "organize"),
    (r"\bvirtualise[sd]?\b", "virtualize"),
    (r"\boptimise[sd]?\b", "optimize"),
    (r"\bcustomise[sd]?\b", "customize"),
    (r"\bminimise[sd]?\b", "minimize"),
    (r"\bmaximise[sd]?\b", "maximize"),
    (r"\butilise[sd]?\b", "utilize (or better: use)"),
    (r"\bcontainerise[sd]?\b", "containerize"),
    (r"\bmodernise[sd]?\b", "modernize"),
    (r"\bprioritise[sd]?\b", "prioritize"),
    (r"\bauthorise[sd]?\b", "authorize"),
    (r"\bstandardise[sd]?\b", "standardize"),
    (r"\bspecialise[sd]?\b", "specialize"),
    (r"\bcentralise[sd]?\b", "centralize"),
]

UK_WORDS = {
    "colour": "color",
    "colours": "colors",
    "behaviour": "behavior",
    "behaviours": "behaviors",
    "favour": "favor",
    "favourable": "favorable",
    "favourite": "favorite",
    "labour": "labor",
    "honour": "honor",
    "centre": "center",
    "centres": "centers",
}


def check_uk_spelling(text: str, section: str, line_num: int) -> list[Finding]:
    """Flag UK spelling variants."""
    findings = []
    matched_spans: list[tuple[int, int]] = []
    lower = text.lower()

    # "data centre" compound phrase
    for m in re.finditer(r"\bdata\s+centres?\b", text, re.IGNORECASE):
        matched_spans.append((m.start(), m.end()))
        findings.append(Finding(
            rule="uk-spelling",
            severity="needs-work",
            section=section,
            message=f'UK spelling "{m.group()}" — use "data center"',
            found=m.group(),
            suggestion="data center",
            line=line_num,
        ))

    # "per cent"
    for m in re.finditer(r"\bper\s+cent\b", text, re.IGNORECASE):
        findings.append(Finding(
            rule="uk-spelling",
            severity="needs-work",
            section=section,
            message='"per cent" — use "percent"',
            found=m.group(),
            suggestion="percent",
            line=line_num,
        ))

    # Exact UK words
    for uk, us in UK_WORDS.items():
        pattern = rf"\b{uk}\b"
        for m in re.finditer(pattern, lower):
            if any(s <= m.start() < e for s, e in matched_spans):
                continue
            findings.append(Finding(
                rule="uk-spelling",
                severity="needs-work",
                section=section,
                message=f'UK spelling "{m.group()}" — use US spelling "{us}"',
                found=m.group(),
                suggestion=us,
                line=line_num,
            ))

    # -ise words
    for pattern, replacement in ISE_WORDS:
        if replacement is None:
            continue
        for m in re.finditer(pattern, text, re.IGNORECASE):
            findings.append(Finding(
                rule="uk-spelling",
                severity="needs-work",
                section=section,
                message=f'UK spelling "{m.group()}" — use "{replacement}"',
                found=m.group(),
                suggestion=replacement,
                line=line_num,
            ))

    return findings


# ---------------------------------------------------------------------------
# Product name enforcement
# ---------------------------------------------------------------------------

PRODUCT_NAME_RULES = [
    (r"\bMicrocloud\b(?!\.)", "MicroCloud requires capital C", "MicroCloud", "needs-work"),
    (r"\bmicrocloud\b(?!\.)", "MicroCloud requires capital M and C", "MicroCloud", "needs-work"),
    (r"\bVMWare\b", "VMware — lowercase 'w', not 'W'", "VMware", "needs-work"),
    (r"\bVmware\b", "VMware — capital W after VM", "VMware", "needs-work"),
    (r"\bvmware\b", "VMware should be capitalized", "VMware", "needs-work"),
    (r"\bUbuntu\s+Linux\b", 'Never use "Ubuntu Linux" — just "Ubuntu"', "Ubuntu", "needs-work"),
    (r"\bUbuntu\s+Advantage\b", 'Legacy name — use "Ubuntu Pro"', "Ubuntu Pro", "needs-work"),
    (r"\bExtended\s+Security\s+Maintenance\b", 'Use "Expanded Security Maintenance"', "Expanded Security Maintenance", "needs-work"),
    (r"\bEnd\s+of\s+Life\b", 'Use "End of Standard Support"', "End of Standard Support", "needs-work"),
    (r"\bEoL\b", 'Use "End of Standard Support"', "End of Standard Support", "needs-work"),
    (r"\bUbuntu\s+server\b", "Ubuntu Server requires capital S", "Ubuntu Server", "needs-work"),
    (r"(?<!\w)open-source(?!\w)", '"open source" — no hyphen', "open source", "needs-work"),
    (r"(?<!\w)opensource(?!\w)", '"open source" — two words', "open source", "needs-work"),
    (r"(?<![.A-Z])Open\s+Source(?!\s+(Initiative|Definition|Security))", '"open source" — lowercase mid-sentence', "open source", "needs-work"),
]


def check_product_names(text: str, section: str, line_num: int) -> list[Finding]:
    """Check product and brand name rules."""
    findings = []
    for pattern, message, suggestion, severity in PRODUCT_NAME_RULES:
        for m in re.finditer(pattern, text):
            findings.append(Finding(
                rule="product-names",
                severity=severity,
                section=section,
                message=message,
                found=m.group(),
                suggestion=suggestion,
                line=line_num,
            ))
    return findings


# ---------------------------------------------------------------------------
# Banned words and phrases
# ---------------------------------------------------------------------------

BANNED_PHRASES = [
    (r"\bthe ability to\b", "rephrase — e.g. 'can'"),
    (r"\bis able to\b", "rephrase — e.g. 'can'"),
    (r"\bnot only\b.*?\bbut also\b", "wordy — simplify"),
    (r"\bbare\s+metal\b", "avoid 'bare metal'"),
    (r"\b(eliminate|execute|terminate|kill)\b", "avoid violent/negative language"),
    (r"\bleverage\b", "use 'use' instead"),
    (r"\bgoing forward\b", "remove — adds nothing"),
    (r"\bin order to\b", "simplify to 'to'"),
    (r"\bform factor\b", "avoid 'form factor'"),
    (r"\bend\s+users?\b", "use 'user' instead"),
    (r"\bdisruptive\b", "avoid 'disruptive'"),
    (r"\bexplosive\b", "avoid 'explosive'"),
]

FLOWERY_WORDS = {
    "assist": "help",
    "alleviate": "ease",
    "ameliorate": "improve",
    "approximately": "about",
    "ascertain": "learn",
    "attempt": "try",
    "cease": "stop",
    "commence": "begin",
    "initiate": "begin",
    "facilitate": "help",
    "magnitude": "size",
    "necessitate": "need",
    "numerous": "many",
    "prior to": "before",
    "possesses": "has",
    "purchase": "buy",
    "regarding": "about",
    "subsequently": "later",
    "utilize": "use",
    "utilise": "use",
    "whilst": "while",
}


def check_banned_words(text: str, section: str, line_num: int) -> list[Finding]:
    """Flag banned words and flowery language."""
    findings = []

    for pattern, suggestion in BANNED_PHRASES:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            findings.append(Finding(
                rule="banned-words",
                severity="needs-work",
                section=section,
                message=f'Avoid "{m.group()}" — {suggestion}',
                found=m.group(),
                suggestion=suggestion,
                line=line_num,
            ))

    lower = text.lower()
    for word, replacement in FLOWERY_WORDS.items():
        pattern = rf"\b{re.escape(word)}\b"
        for m in re.finditer(pattern, lower):
            findings.append(Finding(
                rule="flowery-language",
                severity="needs-work",
                section=section,
                message=f'Prefer plain English: "{word}" → "{replacement}"',
                found=word,
                suggestion=replacement,
                line=line_num,
            ))

    return findings


# ---------------------------------------------------------------------------
# Punctuation checks
# ---------------------------------------------------------------------------

def check_punctuation(text: str, section: str, line_num: int) -> list[Finding]:
    """Check punctuation rules."""
    findings = []

    if "—" in text:
        findings.append(Finding(
            rule="punctuation",
            severity="minor",
            section=section,
            message="Use en dash with spaces ( – ) not em dash (—)",
            found="—",
            suggestion=" – ",
            line=line_num,
        ))

    for m in re.finditer(r'(?<=[a-zA-Z]) - (?=[a-zA-Z])', text):
        findings.append(Finding(
            rule="punctuation",
            severity="minor",
            section=section,
            message="Use en dash with spaces ( – ) not hyphen ( - ) for sentence breaks",
            found=" - ",
            suggestion=" – ",
            line=line_num,
        ))

    # Exclamation marks
    if "!" in text and not text.strip().startswith(("!", "[!", "#")):
        clean = re.sub(r'!\[', '', text)
        if "!" in clean:
            findings.append(Finding(
                rule="punctuation",
                severity="minor",
                section=section,
                message="No exclamation marks in webpage copy",
                found="!",
                line=line_num,
            ))

    return findings


# ---------------------------------------------------------------------------
# Link and CTA checks
# ---------------------------------------------------------------------------

BANNED_LINK_TEXT = [
    "click here",
    "read more",
    "see more",
    "find out more",
    "learn more",
]


def extract_links(text: str) -> list[tuple[str, str]]:
    """Extract (link_text, url) pairs from markdown."""
    return re.findall(r'\[([^\]]+)\]\(([^)]*)\)', text)


def check_links_and_ctas(text: str, section: str, line_num: int) -> list[Finding]:
    """Check link text and CTA rules."""
    findings = []
    links = extract_links(text)

    for link_text, url in links:
        lt_lower = link_text.strip().lower()
        for banned in BANNED_LINK_TEXT:
            if lt_lower == banned or lt_lower.startswith(banned + " "):
                findings.append(Finding(
                    rule="link-text",
                    severity="needs-work",
                    section=section,
                    message=f'Avoid "{link_text}" as link text — use descriptive text',
                    found=link_text,
                    line=line_num,
                ))
                break

    for link_text, url in links:
        if not url.strip():
            findings.append(Finding(
                rule="cta-destination",
                severity="critical",
                section=section,
                message=f'Link/CTA "{link_text}" has an empty destination',
                found=f"[{link_text}]()",
                suggestion="Add the destination URL",
                line=line_num,
            ))

    return findings


# ---------------------------------------------------------------------------
# Placeholder / TBD detection
# ---------------------------------------------------------------------------

PLACEHOLDER_PATTERNS = [
    r"\bTBD\b",
    r"\bTBC\b",
    r"\bTK\b",
    r"\bTODO\b",
    r"\b[Pp]laceholder\b",
    r"\bLorem\s+ipsum\b",
    r"\bXXX\b",
]


def check_placeholders(text: str, section: str, line_num: int) -> list[Finding]:
    """Flag placeholder and TBD markers."""
    findings = []
    for pattern in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pattern, text):
            findings.append(Finding(
                rule="placeholder",
                severity="critical",
                section=section,
                message=f"Unresolved placeholder: {m.group()}",
                found=m.group(),
                line=line_num,
            ))
    return findings


# ---------------------------------------------------------------------------
# Heading level checks
# ---------------------------------------------------------------------------

def check_heading_levels(lines: list[str]) -> list[Finding]:
    """Check for skipped heading levels."""
    findings = []
    prev_level = 0
    for i, line in enumerate(lines, 1):
        m = re.match(r'^(#{1,6})\s', line)
        if m:
            level = len(m.group(1))
            if prev_level > 0 and level > prev_level + 1:
                findings.append(Finding(
                    rule="heading-levels",
                    severity="needs-work",
                    section="Structure",
                    message=f"Skipped heading level: H{prev_level} → H{level}",
                    found=line.strip(),
                    line=i,
                ))
            prev_level = level
    return findings


# ---------------------------------------------------------------------------
# Superlatives and absolute claims
# ---------------------------------------------------------------------------

SUPERLATIVES = [
    r"\bunique\b",
    r"\bfirst\b",
    r"\bonly\b",
    r"\bsole\b",
    r"\bfastest\b",
    r"\blargest\b",
    r"\bbest\b",
    r"\bmost\b",
    r"\bunprecedented\b",
    r"\bexceptional\b",
    r"\bbest[\s-]+in[\s-]+class\b",
    r"\bbest[\s-]+of[\s-]+breed\b",
    r"\bcutting[\s-]+edge\b",
    r"\bstate[\s-]+of[\s-]+the[\s-]+art\b",
    r"\bgame[\s-]+chang",
    r"\brevolutionary\b",
]

SECURITY_CLAIMS = [
    (r"\bsecure\s+open\s+source\b", "use 'trusted open source'"),
    (r"\bmost\s+secure\b", "use 'designed with security in mind'"),
    (r"\bsecurity[\s-]+guaranteed\b", "use 'security-maintained'"),
    (r"\balways\s+secure\b", "use 'security-maintained'"),
    (r"\bfully\s+secured\b", "use 'we help you secure...'"),
]


def check_claims(text: str, section: str, line_num: int) -> list[Finding]:
    """Flag superlatives and security/absolute claims."""
    findings = []

    for pattern, suggestion in SECURITY_CLAIMS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            findings.append(Finding(
                rule="security-claims",
                severity="critical",
                section=section,
                message=f'Unprovable security claim: "{m.group()}" — {suggestion}',
                found=m.group(),
                suggestion=suggestion,
                line=line_num,
            ))

    for pattern in SUPERLATIVES:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            word = m.group().lower()
            if word == "first" and ("first mention" in text.lower()
                                    or "first time" in text.lower()):
                continue
            findings.append(Finding(
                rule="superlatives",
                severity="needs-work",
                section=section,
                message=f'Superlative "{m.group()}" — verify it is backed by evidence',
                found=m.group(),
                line=line_num,
            ))

    return findings


# ---------------------------------------------------------------------------
# Number formatting
# ---------------------------------------------------------------------------

def check_numbers(text: str, section: str, line_num: int) -> list[Finding]:
    """Check number formatting rules."""
    findings = []

    # No space between value and unit
    for m in re.finditer(r'\b(\d+)\s+(GB|MB|KB|TB|GHz|b)\b', text):
        findings.append(Finding(
            rule="number-formatting",
            severity="minor",
            section=section,
            message=f'No space between value and unit: "{m.group()}"',
            found=m.group(),
            suggestion=m.group(1) + m.group(2),
            line=line_num,
        ))

    # Large numbers without commas
    for m in re.finditer(r'(?<!\d)(\d{4,})(?!\d|[-/])', text):
        num = m.group(1)
        if re.match(r'^(19|20)\d{2}$', num):
            continue
        start = m.start()
        preceding = text[:start]
        if re.search(r'https?://\S*$', preceding) or re.search(r'\]\([^)]*$', preceding):
            continue
        if "," not in num and int(num) >= 10000:
            formatted = f"{int(num):,}"
            findings.append(Finding(
                rule="number-formatting",
                severity="minor",
                section=section,
                message=f'Use commas in numbers over 999: "{num}" → "{formatted}"',
                found=num,
                suggestion=formatted,
                line=line_num,
            ))

    return findings


# ---------------------------------------------------------------------------
# Link consistency (cross-page)
# ---------------------------------------------------------------------------

def check_link_consistency(all_links: list[tuple[str, str, str]]) -> list[Finding]:
    """Check that links with the same text go to the same destination."""
    findings = []
    text_to_urls: dict[str, set[str]] = {}
    text_to_section: dict[str, str] = {}

    for link_text, url, section in all_links:
        key = link_text.strip().lower()
        if key not in text_to_urls:
            text_to_urls[key] = set()
            text_to_section[key] = section
        text_to_urls[key].add(url)

    for text, urls in text_to_urls.items():
        if len(urls) > 1:
            findings.append(Finding(
                rule="link-consistency",
                severity="needs-work",
                section=text_to_section[text],
                message=f'Link text "{text}" points to {len(urls)} different URLs',
                found=f'"{text}" → {", ".join(sorted(urls))}',
            ))

    return findings


# ---------------------------------------------------------------------------
# Duplicate CTAs
# ---------------------------------------------------------------------------

def check_duplicate_ctas(all_links: list[tuple[str, str, str]]) -> list[Finding]:
    """Flag duplicate CTA labels on the same page."""
    findings = []
    seen: dict[str, list[str]] = {}

    for link_text, url, section in all_links:
        key = link_text.strip().lower()
        if key not in seen:
            seen[key] = []
        seen[key].append(section)

    for text, sections in seen.items():
        if len(sections) > 2:
            findings.append(Finding(
                rule="duplicate-cta",
                severity="needs-work",
                section=sections[0],
                message=f'CTA "{text}" appears {len(sections)} times on the page',
                found=text,
                suggestion="Use distinct CTA text for each instance",
            ))

    return findings


# ---------------------------------------------------------------------------
# Main lint runner
# ---------------------------------------------------------------------------

def lint_content(lines: list[str], metadata: dict[str, str] | None = None) -> list[Finding]:
    """Run all checks on page content (as markdown lines)."""
    findings: list[Finding] = []
    all_links: list[tuple[str, str, str]] = []

    # Metadata checks
    if metadata:
        findings.extend(check_page_metadata(metadata))

    # Heading structure
    findings.extend(check_heading_levels(lines))

    # Parse sections
    sections = parse_sections(lines)

    # Line-by-line checks
    for section_name, line_num, line in sections:
        if not line.strip():
            continue
        # Skip lines that are just markdown image syntax or URLs
        if re.match(r'^!\[', line) or re.match(r'^https?://', line.strip()):
            continue

        findings.extend(check_uk_spelling(line, section_name, line_num))
        findings.extend(check_product_names(line, section_name, line_num))
        findings.extend(check_banned_words(line, section_name, line_num))
        findings.extend(check_punctuation(line, section_name, line_num))
        findings.extend(check_links_and_ctas(line, section_name, line_num))
        findings.extend(check_placeholders(line, section_name, line_num))
        findings.extend(check_claims(line, section_name, line_num))
        findings.extend(check_numbers(line, section_name, line_num))

        # Collect links for cross-line checks
        for link_text, url in extract_links(line):
            all_links.append((link_text, url, section_name))

    # Cross-line checks
    findings.extend(check_link_consistency(all_links))
    findings.extend(check_duplicate_ctas(all_links))

    return findings


def fetch_page_markdown(url: str) -> str:
    """Fetch a URL and return markdown content using a simple curl + html-to-text approach."""
    try:
        # Use curl to get HTML, then do a basic HTML-to-text conversion
        # For a proper implementation, you'd use WebFetch or a library like markdownify
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        html = result.stdout

        # Basic HTML to readable text extraction
        # Remove script and style blocks
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

        # Convert headings
        for i in range(1, 7):
            text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'{"#" * i} \1', text, flags=re.DOTALL | re.IGNORECASE)

        # Convert links
        text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL | re.IGNORECASE)

        # Remove remaining tags
        text = re.sub(r'<[^>]+>', ' ', text)

        # Decode HTML entities
        text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'")
        text = re.sub(r'&#x[0-9a-fA-F]+;', '', text)
        text = re.sub(r'&#\d+;', '', text)

        # Clean up whitespace
        lines = []
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                lines.append(stripped)

        return "\n".join(lines)

    except (subprocess.TimeoutExpired, Exception) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"critical": 0, "needs-work": 1, "minor": 2}
SEVERITY_ICONS = {"critical": "🔴", "needs-work": "🟡", "minor": "🔵"}


def format_findings(findings: list[Finding], source: str) -> str:
    """Format findings as a readable report."""
    if not findings:
        return "✅ No issues found."

    lines = []
    lines.append("# Page lint report")
    lines.append(f"**Source:** {source}")
    lines.append("")

    # Summary
    by_severity = {"critical": 0, "needs-work": 0, "minor": 0}
    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    total = len(findings)
    lines.append(f"**{total} issues:** "
                 f"{by_severity['critical']} critical, "
                 f"{by_severity['needs-work']} needs work, "
                 f"{by_severity['minor']} minor")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Group by section, then severity
    section_order = []
    section_findings: dict[str, list[Finding]] = {}
    for f in findings:
        if f.section not in section_findings:
            section_order.append(f.section)
            section_findings[f.section] = []
        section_findings[f.section].append(f)

    for section in section_order:
        lines.append(f"## {section}")
        lines.append("")

        sfindings = sorted(section_findings[section],
                           key=lambda f: SEVERITY_ORDER.get(f.severity, 9))

        for f in sfindings:
            icon = SEVERITY_ICONS.get(f.severity, "❓")
            line_ref = f" (line {f.line})" if f.line else ""
            lines.append(f"- {icon} **[{f.rule}]** {f.message}{line_ref}")
            if f.found:
                lines.append(f"  - *Found:* `{f.found}`")
            if f.suggestion:
                lines.append(f"  - *Suggestion:* {f.suggestion}")

        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Lint a live web page for Canonical UX content issues"
    )
    parser.add_argument("target", nargs="?", help="URL to lint (or use --file)")
    parser.add_argument("--file", help="Path to pre-fetched markdown file")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()

    if not args.target and not args.file:
        parser.error("Provide a URL or --file <path>")

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        content = path.read_text(encoding="utf-8")
        source = args.file
        metadata = {}
    else:
        url = args.target
        source = url
        metadata = fetch_html_metadata(url)
        content = fetch_page_markdown(url)

    lines = content.splitlines()
    findings = lint_content(lines, metadata)

    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(format_findings(findings, source))

    # Exit with non-zero if critical issues found
    if any(f.severity == "critical" for f in findings):
        sys.exit(2)
    elif findings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
