#!/usr/bin/env python3
"""
LLM judgement review — the "needs human review" lane, kept separate from the
deterministic, ticketable lane (page_lint.py / ticketable.py).

Where ticketable.py emits exact find->replace fixes that can be auto-applied
(and handed to Bauer), this script asks an LLM to make the *judgement* calls a
regex cannot: is this heading actually descriptive? does this CTA make sense out
of context? does the copy read like a human expert or like generic filler?

The checks are adapted from canonical's automated-ux-qa-checklist
(default-checklist.md) — specifically the judgement-based items that benefit
from an LLM and are NOT already covered deterministically by page_lint.py.

Output is a markdown report saved to reports/, clearly labelled as advisory.
This lane deliberately does NOT connect to Bauer and is never auto-submitted.

---------------------------------------------------------------------------
ONE-TIME SETUP (why this script needs an API key)
---------------------------------------------------------------------------
The actual judgement ("is this heading vague?") is made by Anthropic's AI,
which runs on Anthropic's servers — not on your machine. This script phones
that AI over the internet. To do that it needs an API key: a secret string
that proves you're allowed to use the service and tells Anthropic whose
account to bill (each page costs a fraction of a cent).

Steps (do once):
  1. Go to https://console.anthropic.com , sign in, add a payment method.
  2. Create an API key and copy the "sk-ant-..." string.
  3. Make it available to this script via an environment variable:
         export ANTHROPIC_API_KEY=sk-ant-your-key-here
     (or put that line in a local .env file — .env is gitignored, so the key
     is never committed or shared. NEVER paste the key into this file.)
  4. Run the script (see Usage below).

If you don't have a key yet, you can still preview the report format offline
with --response-file (see below) — no key or network needed.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 scripts/review.py https://canonical.com/solutions/telco
    python3 scripts/review.py https://canonical.com/solutions/telco --save
    python3 scripts/review.py https://canonical.com/solutions/telco --dry-run   # print prompt only
    # Testing/offline: render from a pre-computed model response instead of calling the API
    python3 scripts/review.py https://canonical.com/solutions/telco --response-file resp.json --save
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from page_lint import fetch_html_metadata, fetch_page_markdown

# ---------------------------------------------------------------------------
# The judgement checklist — adapted from automated-ux-qa-checklist.
# Only items that (a) need judgement an LLM can give and (b) are NOT already
# handled deterministically by page_lint.py. Deterministic items (spelling,
# product names, exact banned words, number formatting, heading-level skips,
# duplicate CTAs) are intentionally excluded — they live in the ticketable lane.
# ---------------------------------------------------------------------------

JUDGEMENT_CHECKLIST = """\
## Structure & hierarchy
- Headings are meaningful and descriptive — not vague, generic, or filler
  (e.g. "Overview", "More", "Our solution" with no specifics).
- The most important information or action appears first; the page does not
  bury the lede.
- Lists and bullet groups are introduced by a heading or lead-in sentence.

## CTAs & links
- CTAs use specific, honest action verbs and make sense out of context — a user
  should know what happens when they click, without surrounding copy.
- Link text describes its destination (judge meaning, not just exact phrases).

## Clarity & reading level
- Sentences are concrete and scannable; flag dense, abstract, or padded copy
  that a reader would struggle to parse.
- Flag jargon or internal language that a target reader would not understand.

## Brand voice & tone
- Copy reads like a human expert wrote it — not generic, hedging, or over-formal
  "marketing LLM" filler.
- Flag unsubstantiated hype or vague value claims that add no information.
"""

# Items we explicitly DO NOT judge here (handled deterministically elsewhere, or
# not reliably determinable from extracted text). Stated in the prompt so the
# model stays in its lane and we don't double-report.
OUT_OF_SCOPE = """\
Do NOT report any of the following (handled elsewhere or not determinable from text):
- Spelling, US/UK spelling, product-name casing, punctuation, number formatting.
- Exact banned phrases like "click here" / "read more" (already caught by rules).
- Image alt text, form field labels, focus order, or anything requiring the live
  DOM / rendered page — you are only seeing extracted text.
"""

SYSTEM_PROMPT = (
    "You are a senior UX content reviewer for Canonical. You make judgement "
    "calls about copy quality that a deterministic linter cannot. You are "
    "precise, you cite the exact text you are reacting to, and you never invent "
    "issues to pad the list. If the page reads well, say so and report few or "
    "no issues."
)


def build_prompt(url: str, metadata: dict, content: str) -> str:
    title = metadata.get("title", "") if metadata else ""
    desc = metadata.get("description", "") if metadata else ""
    return f"""\
Review the copy of this live web page against the judgement checklist below.

URL: {url}
Meta title: {title}
Meta description: {desc}

{JUDGEMENT_CHECKLIST}

{OUT_OF_SCOPE}

Return STRICT JSON only (no prose, no markdown fences) in exactly this shape:
{{
  "findings": [
    {{
      "section": "<page section/heading the issue sits under, best guess>",
      "category": "<Structure|CTAs|Clarity|Voice>",
      "severity": "<critical|needs-work|minor>",
      "issue": "<what is wrong and why it matters, one or two sentences>",
      "found": "<the exact text you are reacting to, verbatim>",
      "recommendation": "<concrete suggested improvement>"
    }}
  ],
  "what_looks_good": ["<specific genuine positive>", "..."]
}}

Severity guide: critical = blocks comprehension or misleads; needs-work = vague
or weak copy that should change; minor = small polish. Only include findings you
are confident about.

PAGE CONTENT (extracted visible text, markdown):
---
{content}
---
"""


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def call_llm(prompt: str, model: str, max_tokens: int = 4000) -> str:
    """Call the Anthropic Messages API and return the raw text response.

    Auth resolution, in order:
      1. ANTHROPIC_API_KEY via the standard `x-api-key` header (production).
      2. If that is rejected and a CLAUDE_CODE_OAUTH_TOKEN is present, retry with
         `Authorization: Bearer` (running inside Claude Code).
    Honors ANTHROPIC_BASE_URL if set.
    """
    base = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    oauth = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
    if not api_key and not oauth:
        sys.exit(
            "No ANTHROPIC_API_KEY found.\n"
            "This script needs an Anthropic API key to ask the AI for its "
            "judgement. One-time setup:\n"
            "  1. Create a key at https://console.anthropic.com\n"
            "  2. export ANTHROPIC_API_KEY=sk-ant-your-key-here\n"
            "  3. re-run this command\n"
            "(See the setup notes at the top of this file. To preview the "
            "report format with no key, use --response-file.)")

    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    auth_modes = []
    if api_key:
        auth_modes.append({"x-api-key": api_key})
    if oauth:
        auth_modes.append({"authorization": f"Bearer {oauth}"})

    last_err = None
    for headers in auth_modes:
        for attempt in range(4):
            req = urllib.request.Request(
                base + "/v1/messages", data=body,
                headers={"content-type": "application/json",
                         "anthropic-version": "2023-06-01", **headers})
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    data = json.load(r)
                return data["content"][0]["text"]
            except urllib.error.HTTPError as e:
                code = e.code
                last_err = f"HTTP {code}: {e.read()[:200].decode(errors='replace')}"
                if code == 401:
                    break  # wrong auth mode — try the next one
                if code in (429, 529):
                    time.sleep(2 ** attempt)  # backoff and retry
                    continue
                break
            except Exception as e:
                last_err = str(e)
                time.sleep(1)
    sys.exit(f"LLM call failed: {last_err}")


def parse_response(raw: str) -> dict:
    """Extract the JSON object from a model response, tolerating stray text."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        sys.exit(f"Could not find JSON in model response:\n{raw[:500]}")
    return json.loads(raw[start:end + 1])


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

_SEV = [("critical", "🔴 Critical"), ("needs-work", "🟡 Needs work"),
        ("minor", "🔵 Minor")]


def render_report(url: str, result: dict, model: str) -> str:
    findings = result.get("findings", [])
    good = result.get("what_looks_good", [])
    counts = {sev: sum(1 for f in findings if f.get("severity") == sev)
              for sev, _ in _SEV}

    lines = [
        f"# UX copy review (judgement lane) – {urlparse(url).path or '/'}",
        f"**URL:** {url}",
        f"**Date:** {date.today().isoformat()}",
        f"**Reviewer:** LLM ({model})",
        "",
        "> ⚠️ **Advisory only — needs human review.** These are judgement calls, "
        "not deterministic fixes. They are intentionally NOT ticketable and are "
        "never auto-submitted or sent to Bauer.",
        "",
        f"**Issues:** {len(findings)} "
        f"({counts['critical']} critical, {counts['needs-work']} needs work, "
        f"{counts['minor']} minor)",
        "",
        "---",
        "",
        "## Issues",
        "",
    ]
    if not findings:
        lines.append("✅ No judgement issues raised.")
        lines.append("")
    else:
        # Group by section, preserve order of first appearance.
        order, by_section = [], {}
        for f in findings:
            sec = f.get("section") or "(unspecified)"
            if sec not in by_section:
                by_section[sec] = []
                order.append(sec)
            by_section[sec].append(f)
        for sec in order:
            lines.append(f"### {sec}")
            lines.append("")
            for sev, label in _SEV:
                items = [f for f in by_section[sec] if f.get("severity") == sev]
                if not items:
                    continue
                for f in items:
                    lines.append(
                        f"- **{label}** [{f.get('category','')}] — {f.get('issue','')}")
                    if f.get("found"):
                        lines.append(f"  - *Found:* \"{f['found']}\"")
                    if f.get("recommendation"):
                        lines.append(f"  - *Suggestion:* {f['recommendation']}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## ✅ What looks good")
    lines.append("")
    if good:
        for g in good:
            lines.append(f"- {g}")
    else:
        lines.append("_No specific positives noted._")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LLM judgement review of a live page (advisory, not ticketable)")
    parser.add_argument("url", help="Page URL to review")
    parser.add_argument("--model", default=os.environ.get("DEFAULT_LLM_MODEL")
                        or "claude-sonnet-4-20250514",
                        help="Anthropic model id")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the assembled prompt and exit (no API call)")
    parser.add_argument("--response-file",
                        help="Render from a saved model JSON response instead of "
                             "calling the API (testing/offline)")
    parser.add_argument("--save", action="store_true",
                        help="Save the report to reports/")
    args = parser.parse_args()

    print(f"Fetching: {args.url}", file=sys.stderr)
    metadata = fetch_html_metadata(args.url)
    content = fetch_page_markdown(args.url)
    prompt = build_prompt(args.url, metadata, content)

    if args.dry_run:
        print(prompt)
        return

    if args.response_file:
        raw = Path(args.response_file).read_text(encoding="utf-8")
    else:
        print(f"Calling LLM ({args.model})…", file=sys.stderr)
        raw = call_llm(prompt, args.model)

    result = parse_response(raw)
    report = render_report(args.url, result, args.model)
    print(report)

    if args.save:
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        slug = (urlparse(args.url).path or "/").strip("/").replace("/", "-") or "home"
        domain = urlparse(args.url).netloc.replace(".", "-")
        out = report_dir / f"{domain}-{slug}-review-{date.today().isoformat()}.md"
        out.write_text(report + "\n", encoding="utf-8")
        print(f"\n📄 Saved: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
