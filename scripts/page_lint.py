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
    # Anchor context — exact text immediately before/after the match on its
    # line. Populated after matching (see lint_content) and used to locate the
    # change unambiguously in source (maps to Bauer's SuggestionAnchor).
    preceding: str = ""
    following: str = ""


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
    "catalogue": "catalog",
    "catalogues": "catalogs",
    "sceptical": "skeptical",
    "travelling": "traveling",
    "defence": "defense",
}

# Canonical house-style spellings (style guide "Consistency" section).
# Deterministic single-form preferences — each has one correct replacement.
# Context-dependent pairs (setup/set up, backup/back up, license/licence,
# program/programme) are deliberately excluded: they need human judgement.
HOUSE_STYLE_WORDS = [
    (r"\be-mails?\b", "email"),
    (r"\bon-line\b", "online"),
    (r"\bwhite[\s-]papers?\b", "whitepaper"),
    (r"\bmulti[\s]cloud\b", "multi-cloud"),
    (r"\bmulticloud\b", "multi-cloud"),
]


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

    # House-style spellings (Canonical consistency rules)
    for pattern, replacement in HOUSE_STYLE_WORDS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            if m.group().lower() == replacement.lower():
                continue  # already the correct form
            findings.append(Finding(
                rule="house-style",
                severity="needs-work",
                section=section,
                message=f'"{m.group()}" — use "{replacement}"',
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
    # Product names with a single canonical spelling that are commonly mistyped.
    # Conservative set only — context-dependent casing (charm, snap, chisel) is
    # excluded to avoid false positives on ordinary English words.
    (r"\bMaas\b", "MAAS — all capitals", "MAAS", "needs-work"),
    (r"\bCharm\s+[Hh]ub\b|\bCharmHub\b", "Charmhub — one word, capital C only", "Charmhub", "needs-work"),
    (r"\bSnap\s+craft\b|\bSnapCraft\b", "Snapcraft — one word, capital S only", "Snapcraft", "needs-work"),
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

    # Flag only isolated em dashes used as sentence breaks. A run of two or
    # more dashes (— – -) is a decorative divider, not prose, so skip any em
    # dash that sits adjacent to another dash character.
    for _ in re.finditer(r'(?<![-–—])—(?![-–—])', text):
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
                severity="minor",
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
        # Skip standard/spec identifiers (e.g. ISO 27001, IEC 21434, RFC 1918)
        # — these are names, not quantities, and must not get thousands separators.
        if re.search(r'\b(ISO|IEC|RFC|CVE|SOC|ANSI|NIST|FIPS|PCI|DSS|EN|UL|SAE|AS)[\s/-]*$',
                     preceding, re.IGNORECASE):
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

    # Generic UI control labels (modal/overlay/menu controls) are expected to
    # repeat and are not marketing CTAs — don't flag them as duplicates.
    GENERIC_UI_LABELS = {
        "close", "menu", "open menu", "close menu", "search", "back", "next",
        "previous", "toggle navigation", "skip to main content",
    }

    for link_text, url, section in all_links:
        key = link_text.strip().lower()
        if key in GENERIC_UI_LABELS:
            continue
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

    # Remember the prose text per line so we can attach anchor context to each
    # finding afterwards (the text the checks actually matched against).
    prose_by_line: dict[int, str] = {}

    # Line-by-line checks
    for section_name, line_num, line in sections:
        if not line.strip():
            continue
        # Skip lines that are just markdown image syntax or URLs
        if re.match(r'^!\[', line) or re.match(r'^https?://', line.strip()):
            continue

        # Prose checks run on visible text only: collapse markdown links
        # [text](url) to their text so URL slugs (e.g. /open-source-security)
        # are not flagged as copy errors. Link/CTA checks still see the URL.
        prose = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', line)
        prose_by_line[line_num] = prose

        findings.extend(check_uk_spelling(prose, section_name, line_num))
        findings.extend(check_product_names(prose, section_name, line_num))
        findings.extend(check_banned_words(prose, section_name, line_num))
        findings.extend(check_punctuation(prose, section_name, line_num))
        findings.extend(check_links_and_ctas(line, section_name, line_num))
        findings.extend(check_placeholders(prose, section_name, line_num))
        findings.extend(check_claims(prose, section_name, line_num))
        findings.extend(check_numbers(prose, section_name, line_num))

        # Collect links for cross-line checks
        for link_text, url in extract_links(line):
            all_links.append((link_text, url, section_name))

    # Cross-line checks
    findings.extend(check_link_consistency(all_links))
    findings.extend(check_duplicate_ctas(all_links))

    # Attach anchor context (text before/after the match) to each finding, so
    # the change can be located unambiguously in source. Capped to a window;
    # repeated matches on a line are disambiguated with a moving cursor.
    ANCHOR_WINDOW = 60
    cursor: dict[tuple[int, str], int] = {}
    for f in findings:
        if not f.found:
            continue
        prose = prose_by_line.get(f.line)
        if not prose:
            continue
        key = (f.line, f.found)
        start = prose.find(f.found, cursor.get(key, 0))
        if start == -1:
            continue
        end = start + len(f.found)
        cursor[key] = end
        f.preceding = prose[max(0, start - ANCHOR_WINDOW):start]
        f.following = prose[end:end + ANCHOR_WINDOW]

    return findings


# Elements whose text is never visible page copy and must not be linted.
_NON_VISIBLE_TAGS = [
    "script", "style", "head", "noscript", "template", "svg",
    "code", "pre", "kbd", "samp",
]

# Class names commonly used to visually hide text (screen-reader-only,
# off-screen, collapsed mega-menus). Present in the DOM but not seen by users.
_HIDDEN_CLASS_RE = re.compile(
    r"\b(u-off-screen|u-hide|is-hidden|sr-only|screen-?reader|"
    r"visually-?hidden|visuallyhidden)\b",
    re.IGNORECASE,
)


def _html_to_markdown_bs4(html: str) -> str:
    """Extract visible page text as markdown using BeautifulSoup.

    Drops scripts, styles, code samples and hidden DOM nodes so the linter
    only sees copy a user actually reads. This avoids false positives from
    e.g. collapsed nav menus or screen-reader-only text that a visible-page
    search would never surface.
    """
    from bs4 import BeautifulSoup, NavigableString
    import html as html_module

    soup = BeautifulSoup(html, "html.parser")

    # Drop tags whose contents are never visible copy.
    for tag in soup(_NON_VISIBLE_TAGS):
        tag.decompose()

    # Drop elements hidden from sighted users but still present in the DOM.
    for tag in soup.find_all(True):
        if tag.decomposed:
            continue
        if tag.has_attr("hidden"):
            tag.decompose()
            continue
        if str(tag.get("aria-hidden", "")).lower() == "true":
            tag.decompose()
            continue
        style = str(tag.get("style", "")).lower().replace(" ", "")
        if "display:none" in style or "visibility:hidden" in style:
            tag.decompose()
            continue
        classes = " ".join(tag.get("class", []))
        if classes and _HIDDEN_CLASS_RE.search(classes):
            tag.decompose()
            continue

    # Preserve links as markdown so downstream link/CTA checks still work.
    for a in soup.find_all("a"):
        if a.decomposed:
            continue
        text = a.get_text(" ", strip=True)
        href = a.get("href", "")
        a.replace_with(NavigableString(f"[{text}]({href})" if href else text))

    # Preserve heading levels as markdown so heading-structure checks work.
    for level in range(1, 7):
        for tag in soup.find_all(f"h{level}"):
            if tag.decomposed:
                continue
            text = tag.get_text(" ", strip=True)
            tag.replace_with(NavigableString(f"\n{'#' * level} {text}\n"))

    raw = html_module.unescape(soup.get_text("\n"))
    return "\n".join(line.strip() for line in raw.splitlines() if line.strip())


def _html_to_markdown_legacy(html: str) -> str:
    """Regex-based HTML-to-text fallback when BeautifulSoup is unavailable."""
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    for i in range(1, 7):
        text = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'{"#" * i} \1', text, flags=re.DOTALL | re.IGNORECASE)

    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)

    import html as html_module
    text = html_module.unescape(text)

    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def fetch_page_markdown(url: str) -> str:
    """Fetch a URL and return its visible text as markdown."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        html = result.stdout

        try:
            return _html_to_markdown_bs4(html)
        except ImportError:
            print("BeautifulSoup not available, using regex fallback "
                  "(higher false-positive risk)", file=sys.stderr)
            return _html_to_markdown_legacy(html)

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


def url_to_report_path(url: str) -> Path:
    """Convert a URL to a report file path under reports/."""
    from urllib.parse import urlparse
    from datetime import date

    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "-")  # ubuntu.com → ubuntu-com
    path_slug = parsed.path.strip("/").replace("/", "-") or "home"
    today = date.today().isoformat()
    filename = f"{domain}-{path_slug}-{today}.md"
    return Path("reports") / filename


def main():
    parser = argparse.ArgumentParser(
        description="Lint a live web page for Canonical UX content issues"
    )
    parser.add_argument("target", nargs="?", help="URL to lint (or use --file)")
    parser.add_argument("--file", help="Path to pre-fetched markdown file")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    parser.add_argument("--save", action="store_true",
                        help="Save report to reports/ and push to GitHub")
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
        output = json.dumps([asdict(f) for f in findings], indent=2)
    else:
        output = format_findings(findings, source)

    print(output)

    # Save report and push to GitHub
    if args.save and args.target:
        report_path = url_to_report_path(args.target)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output + "\n", encoding="utf-8")
        print(f"\n📄 Report saved: {report_path}", file=sys.stderr)

        # Git add, commit, push
        subprocess.run(["git", "add", str(report_path)], check=True)
        subprocess.run(
            ["git", "commit", "-m", f"report: lint {source}"],
            check=True
        )
        subprocess.run(["git", "push"], check=True)
        print("✅ Pushed to GitHub", file=sys.stderr)

    # Exit with non-zero if critical issues found
    if any(f.severity == "critical" for f in findings):
        sys.exit(2)
    elif findings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
