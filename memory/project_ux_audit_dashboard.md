---
name: project-ux-audit-dashboard
description: Hackweek 2026 UX audit dashboard — React+Vite app inside the o-naur repo, consumes existing markdown audit reports as JSON fixtures
metadata:
  type: project
---

React + Vite dashboard lives at `/Users/mariatrujillo/hackweek-2026/o-naur/dashboard/`. Entry: `npm run dev` from that directory.

**Why:** Hackweek 2026 project to visualize UX audit reports for ubuntu.com and canonical.com pages (O-NAUR: Observe, Notify, Audit, Update, Remediate).

**How to apply:** When adding new audit reports, create a JSON fixture in `dashboard/src/data/` matching the `SiteData` shape in `src/types.ts`, then import it in `App.tsx`. The data model supports per-page, per-category issues with `description`, `location`, `severity`, and optional `line` field.

Data files:
- `src/data/ubuntu-com.json` — ubuntu.com homepage (2026-05-13)
- `src/data/canonical-com.json` — canonical.com /, /ceph, /ceph/support

Source reports are markdown in `/reports/` (root) and `/url-ux-audit/reports/`. No automated parser yet — JSON is hand-authored from those reports. Automating the markdown→JSON conversion is a planned next step.

Owners in JSON are placeholder names (not in original reports) — should be updated when real owners are known.
