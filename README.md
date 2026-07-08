# O-NAUR: Observe, Notify, Audit, Update and Remediate

An LLM-powered agent that audits live web pages for UX quality and publishes structured reports to a dashboard.

---

## How it works

O-NAUR is a two-part system:

1. **Audit agent** — an LLM skill that fetches a live URL, checks it against a UX content checklist, and writes a structured markdown report.
2. **Dashboard** — a React app that parses those reports and visualises issues by page, category, and severity.

The data flow is:

```
Audit skill runs on a URL
        ↓
Markdown report saved to reports/{site}/audits/
        ↓
npm run build-data parses all reports → public/data/{site}.json
        ↓
Dashboard fetches JSON at runtime and renders the results
```

---

## Running an audit

Audits are run using the UX audit skill defined in `.opencode/skills/ux-audit/SKILL.md`. Trigger it by asking the agent to audit a URL:

> "Audit https://ubuntu.com/security"

The skill will:
1. Extract the copydoc URL from the page's `<meta name="copydoc">` tag
2. Fetch and analyse the page content against the default checklist (`url-ux-audit/references/default-checklist.md`)
3. Write a report to `reports/{site-domain}/audits/{page-slug}-audit.md`

### Report filename convention

| URL | Report file |
|-----|-------------|
| `ubuntu.com/security` | `reports/ubuntu.com/audits/security-audit.md` |
| `ubuntu.com/security/fips` | `reports/ubuntu.com/audits/security-fips-audit.md` |
| `canonical.com/ceph` | `reports/canonical.com/audits/ceph-audit.md` |

### Adding URLs to the audit queue

Each site has a `paths.txt` file listing pages to audit:

```
reports/ubuntu.com/paths.txt
reports/canonical.com/paths.txt
```

Add one path per line (without the protocol), e.g. `ubuntu.com/new-page`.

---

## Content linting pipeline (scripts/)

Alongside the LLM-based audit skill above, `scripts/` holds a separate,
deterministic pipeline for scanning a whole site for hard style-guide
violations (UK spelling, banned words, punctuation, product names, number
formatting, etc.) and turning the clean-cut ones into a ticket queue for
Bauer. It does not call any LLM and does not hit the Bauer API directly —
it only produces a JSON artifact shaped for Bauer to ingest.

```
page_lint.py     Core rule set — lints a single page's markdown content,
                 returns a list of Finding(rule, severity, section, ...)
batch_lint.py    Crawls a sitemap, runs page_lint on every page (minus
                 excluded paths like /docs/, /blog/, /careers/), and
                 writes a consolidated must-fix / nice-to-fix report
ticketable.py    Filters findings down to the subset that are safe to
                 auto-submit (exact find→replace, not a judgement call),
                 and drives the scan → review → approve → Bauer flow
```

### Scan → review → approve → Bauer

Nothing is auto-submitted. Every run requires a human to check off which
candidates are approved before a Bauer artifact is produced. The checklist
("Copy edits for review") lives in `reports/pending/` while it's awaiting
review, then gets filed into `reports/reviewed/` once it's been approved —
so `reports/pending/` always shows exactly what's still outstanding:

```bash
# 1. Scan a site and save a checklist of candidate fixes
python3 scripts/ticketable.py https://canonical.com/sitemap_tree.xml --save
#    → reports/pending/{site}-copy-edits-{date}.md   (checklist, - [ ] per candidate)
#    → reports/pending/{site}-copy-edits-{date}.json (full candidate data)

# 2. Open the .md file, tick the boxes for fixes you approve (- [x])

# 3. Emit the Bauer artifact for approved items only — this also files the
#    reviewed checklist (.md + .json) out of reports/pending/ and into
#    reports/reviewed/, alongside the Bauer artifact it produced
python3 scripts/ticketable.py --approve reports/pending/{site}-copy-edits-{date}.md --save
#    → reports/reviewed/{site}-copy-edits-{date}.md
#    → reports/reviewed/{site}-copy-edits-{date}.json
#    → reports/reviewed/{site}-bauer-{date}.json
```

Only findings that are unambiguous, exact-replacement fixes are ever
offered as candidates — see `is_ticketable()` in `ticketable.py`. Judgement
calls (e.g. "flowery language") never reach the checklist at all.

`--limit N` caps the scan to the first N pages. Both scanning and the
sitemap fetch send an identifying `User-Agent` and pace requests with a
short delay between pages, to be a good citizen of production
infrastructure being scraped.

### Regression tests

```bash
python3 -m unittest discover tests
```

`tests/test_lint_rules.py` pins down every false positive this pipeline
has already produced and shipped in a report once (see the file's
docstring) so they can't silently regress.

### Picking up where you left off

This repo also ships a local, gitignored `PROJECT_LOG.md` plus
`CLAUDE.md` / `.github/copilot-instructions.md` so that asking
Claude Code or GitHub Copilot "where did we leave off?" in this repo
gets you a plain-language status update and suggested next steps.

---

## Dashboard

A React + Vite app that visualises audit reports for all sites.

### Running locally

```bash
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

`npm run dev` automatically runs the build script before starting the dev server, so the dashboard always reflects the latest reports.

### Rebuilding data without restarting

To regenerate the dashboard data from reports without restarting the dev server:

```bash
npm run build-data
```

Then refresh the browser — the dashboard fetches data at runtime, so no restart is needed.

### Building for production

```bash
npm run build
```

---

## Project structure

```
.opencode/skills/ux-audit/    # Audit agent skill definition
  SKILL.md                    # Step-by-step instructions for the agent
  references/
    default-checklist.md      # UX checklist used in every audit
    report-template.md        # Report output format

reports/                      # All audit reports (committed to repo)
  ubuntu.com/
    paths.txt                 # Pages to audit
    audits/                   # One .md file per audited page
  canonical.com/
    paths.txt
    audits/
  pending/                    # Copy-edit checklists awaiting review
  reviewed/                   # Filed-away checklists + approved Bauer artifacts

scripts/
  build-data.mjs              # Parses .md reports → public/data/*.json
  page_lint.py                # Deterministic content lint rules
  batch_lint.py                # Sitemap crawl + consolidated lint report
  ticketable.py                # scan → review → approve → Bauer pipeline
  review.py                    # Advisory review lane

tests/
  test_lint_rules.py          # Regression suite for scripts/*.py

public/data/                  # Generated JSON consumed by the dashboard
  ubuntu-com.json
  canonical-com.json

src/                          # Dashboard React app
  components/
  hooks/
    useSiteData.ts            # Fetches site JSON at runtime
  types.ts                    # Shared data model
```

---

## Adding a new site

1. Create a directory: `reports/{site-domain}/audits/`
2. Add a `reports/{site-domain}/paths.txt` with pages to audit
3. Run audits against those URLs — reports will be saved automatically
4. Run `npm run build-data` — a new `public/data/{site-slug}.json` is generated
5. Add the new `SiteId` to `src/types.ts` and wire it into `src/components/SiteToggle.tsx`

---

## References

- Audit checklist: `url-ux-audit/references/default-checklist.md`
- Report template: `url-ux-audit/references/report-template.md`
- Workshop (agent runner): https://github.com/canonical/workshop
