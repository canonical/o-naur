---
name: github-crawl-audit
description: >
  Use this skill to crawl a GitHub repository's templates directory and run UX audits
  on all static pages. The user provides a GitHub repo URL, and this skill will
  fetch all template files and audit them using the LLM-powered audit process.
  Triggers include: "crawl GitHub repo", "audit templates from repo", "run audit on
  repository templates", or when user provides a GitHub URL and asks to audit templates.
---

# GitHub Repository Crawl & Audit Skill

Automatically crawls a GitHub repository's templates directory and runs UX content
audits on all static pages.

---

## Inputs

| Input | Required | Notes |
|---|---|---|
| GitHub Repository URL | Yes | Public repository URL (e.g., https://github.com/canonical/ubuntu.com) |
| Branch name | Optional | Defaults to "main" or "master" |
| Templates path | Optional | Defaults to "templates/" |

---

## Step 0 — Confirm inputs

1. Check that the user has provided a GitHub repository URL
2. Extract owner and repository name from the URL
3. Ask for branch name if not provided (default: main/master)
4. Confirm the templates directory path (default: templates/)
5. Tell the user what will be audited

---

## Step 1 — Parse GitHub repository URL

1. Extract the owner and repository name from the URL
2. Determine the correct branch (main, master, or user-specified)
3. Validate that the repository is accessible

Example URL parsing:
```
https://github.com/canonical/ubuntu.com → owner: canonical, repo: ubuntu.com
https://github.com/canonical/webteam → owner: canonical, repo: webteam
```

---

## Step 2 — Crawl templates directory

1. Use GitHub API to recursively list all files in the templates directory
2. Filter for HTML files only (`.html` extension)
3. Exclude underscore-prefixed files (partials/includes)
4. Fetch raw HTML content for each file and check for `noindex` meta tag
5. Exclude files with `noindex` in robots meta tag
6. Build a mapping of URL paths to file paths

### Path Resolution Rules

For most pages:
```
URL: ubuntu.com/desktop/upcoming-features
File: templates/desktop/upcoming-features.html
```

For index pages:
```
URL: ubuntu.com/desktop
File: templates/desktop/index.html
```

For nested paths:
```
URL: ubuntu.com/engage/resources/guide
File: templates/engage/resources/guide.html
```

### File Discovery

Look for these file patterns:
- `*.html` — HTML template files
- `*.md` — Markdown pages
- `*.yaml` / `*.yml` — YAML configuration (skip, not audit targets)

### Exclusion Rules

**Exclude files that match any of the following criteria:**

1. **Underscore-prefixed files** — Files starting with `_` are partials/includes
   - Exclude: `templates/shared/_header.html`
   - Exclude: `templates/engage/_article-card.html`
   - Exclude: `templates/macros/_macro-example.jinja`
   
2. **Files with `noindex` meta tag** — Pages marked as not indexable
   - Check each HTML file for `<meta name="robots" content="noindex">` or similar
   - Exclude: Any file containing `noindex` in the robots meta tag content
   - Example: `<meta name="robots" content="noindex, nofollow">`

3. **Non-page files** — Skip configuration and data files
   - Exclude: `form-data.json`
   - Exclude: `list_endpoints.py`
   - Exclude: `ubuntu-ia.csv`, `ubuntu-ia.txt`
   - Exclude: `sitemap.xml` files

### File Discovery Process

1. Recursively list all files in templates directory
2. Filter for `*.html` files only
3. Exclude files starting with `_`
4. For each remaining file, fetch raw HTML content and check for `noindex` meta tag
5. Exclude files with `noindex` in robots meta tag
6. Build URL mapping for remaining files

### Exclusion Rules

**Exclude files that match any of the following criteria:**

1. **Underscore-prefixed files** — Files starting with `_` are partials/includes
   - Exclude: `templates/shared/_header.html`
   - Exclude: `templates/engage/_article-card.html`
   - Exclude: `templates/macros/_macro-example.jinja`
   
2. **Files with `noindex` meta tag** — Pages marked as not indexable
   - Check each HTML file for `<meta name="robots" content="noindex">` or similar
   - Exclude: Any file containing `noindex` in the robots meta tag content
   - Example: `<meta name="robots" content="noindex, nofollow">`

3. **Non-page files** — Skip configuration and data files
   - Exclude: `form-data.json`
   - Exclude: `list_endpoints.py`
   - Exclude: `ubuntu-ia.csv`, `ubuntu-ia.txt`
   - Exclude: `sitemap.xml` files

### File Discovery Process

1. Recursively list all files in templates directory
2. Filter for `*.html` files only
3. Exclude files starting with `_`
4. For each remaining file, fetch raw HTML content and check for `noindex` meta tag
5. Exclude files with `noindex` in robots meta tag
6. Build URL mapping for remaining files

---

## Step 3 — Generate audit URLs

For each template file discovered:

1. **Index pages** — If file is `index.html` in a folder, the URL is the folder path
   - `templates/desktop/index.html` → `/desktop`
   
2. **Regular pages** — Convert file path to URL
   - `templates/desktop/upcoming-features.html` → `/desktop/upcoming-features`
   
3. **Nested pages** — Preserve directory structure
   - `templates/engage/resources/guide.html` → `/engage/resources/guide`

4. **Remove file extensions** — Strip `.html`, `.md` from paths

5. **Build full URLs** — Combine with base URL from environment

---

## Step 4 — Run UX audits

For each generated URL:

1. **Fetch the static page content**
   - If the template files are hosted somewhere, fetch them directly
   - Otherwise, use the GitHub raw content URL for preview
   
2. **Extract copydoc URL**
   - Parse `<meta name="copydoc">` from HTML
   - Record the copydoc URL in the report
   
3. **Run LLM-based audit**
   - Use WebFetch with `format: "html"`
   - Extract visible content grouped by sections
   - Run UX quality checks against the checklist

4. **Save audit report**
   - Use filename format: `[page-slug]-[YYYY-MM-DD].md`
   - Save to `reports/` directory
   - Include copydoc URL in report header

---

## Step 5 — Generate summary report

After all audits complete:

1. Count total pages audited
2. Summarize issues found:
   - Critical issues
   - Needs work
   - Minor issues
3. List all successful audit reports
4. List any failed audits with error messages

---

## Step 6 — Deliver results

1. Output the summary report inline in chat
2. Provide links to all individual audit reports
3. Highlight any critical issues that need immediate attention
4. Offer to dive deeper into specific pages or sections

---

## Edge cases

| Situation | How to handle |
|---|---|
| Repository is private | Tell user the repo must be public or provide a valid GitHub token |
| Templates directory doesn't exist | Ask user to confirm the correct templates path |
| No template files found | Inform user and ask if they want to search a different directory |
| Large repository | Process in batches, show progress, limit to first N pages |
| File encoding issues | Skip problematic files, log error, continue with others |
| GitHub API rate limit | Implement retry logic with exponential backoff |

---

## References

- `references/default-checklist.md` — Full default UX content checklist
- `references/report-template.md` — Report structure template
- `reports/` — Saved audit reports, named `[page-slug]-[YYYY-MM-DD].md`
- GitHub API: https://docs.github.com/en/rest

---

## Example Usage

**User:** "Crawl the canonical/ubuntu.com repository and audit all templates"

**Skill:**
1. Confirms repository: https://github.com/canonical/ubuntu.com
2. Crawls templates/ directory
3. Discovers 45 template files
4. Runs UX audits on all pages
5. Saves 45 audit reports
6. Generates summary: "45 pages audited, 3 critical issues, 12 needs work, 8 minor"

**Output:**
```
# O-NAUR Audit Summary Report

**Generated:** 2026-05-13 15:30:00

## Overview
- Total pages audited: 45
- Critical issues: 3
- Needs work: 12
- Minor issues: 8

## Critical Issues
- /pro — Missing H1 in hero section
- /ceph — Empty alt text on informational images
- /kubernetes — Vague CTA link text

## All Reports
- [pro](reports/pro-2026-05-13.md)
- [ceph](reports/ubuntu-com-ceph-2026-05-13.md)
- [kubernetes](reports/kubernetes-2026-05-13.md)
...
```
