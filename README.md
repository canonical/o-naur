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

scripts/
  build-data.mjs              # Parses .md reports → public/data/*.json

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
