import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPORTS_DIR = path.join(__dirname, '..', 'reports');
const OUTPUT_DIR = path.join(__dirname, '..', 'public', 'data');

const SEVERITY_MAP = { '🔴': 'critical', '🟡': 'needs-work', '🔵': 'minor' };

const SKIP_SECTIONS = new Set([
  'summary',
  'what looks good',
  'recommended priority order',
  'manual checks for reviewer',
  'ux quality check',
]);

function parseReport(content) {
  const urlMatch = content.match(/\*\*URL:\*\*\s*(https?:\/\/\S+)/);
  if (!urlMatch) return null;

  const url = urlMatch[1].trim();
  const date = content.match(/\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})/)?.[1] ?? '';
  const copyDocRaw = content.match(/\*\*Copydoc:\*\*\s*(https?:\/\/\S+)/)?.[1] ?? '';
  const copyDocUrl = copyDocRaw || undefined;

  const urlObj = new URL(url);
  const pagePath = urlObj.pathname || '/';

  const categories = [];
  let currentCategory = null;
  let currentSeverity = null;
  let skip = false;

  for (const line of content.split('\n')) {
    // Category-level heading (##)
    if (line.startsWith('## ')) {
      if (currentCategory?.issues.length) categories.push(currentCategory);
      const name = line.slice(3).trim();
      skip = SKIP_SECTIONS.has(name.toLowerCase());
      currentCategory = skip ? null : { name, issues: [] };
      currentSeverity = null;
      continue;
    }

    if (skip) continue;

    // Severity heading (###)
    if (line.startsWith('### ')) {
      const header = line.slice(4).trim();
      currentSeverity = null;
      for (const [emoji, sev] of Object.entries(SEVERITY_MAP)) {
        if (header.includes(emoji)) { currentSeverity = sev; break; }
      }
      continue;
    }

    // Issue bullet: - **Name:** description  or  - **Name** — description
    if (currentCategory && currentSeverity && line.startsWith('- **')) {
      const match = line.match(/^- \*\*(.+?)\*\*:?\s*(?:[—-]\s*)?(.+)?$/);
      if (match) {
        const name = match[1].replace(/:$/, '').trim();
        const detail = match[2]?.trim() ?? '';
        currentCategory.issues.push({
          description: detail ? `${name} — ${detail}` : name,
          location: '',
          severity: currentSeverity,
        });
      }
    }
  }

  if (currentCategory?.issues.length) categories.push(currentCategory);

  const result = { path: pagePath, url, date, categories };
  if (copyDocUrl) result.copyDocUrl = copyDocUrl;
  return result;
}

fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const siteDirs = fs.readdirSync(REPORTS_DIR, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name);

for (const siteDomain of siteDirs) {
  const auditsDir = path.join(REPORTS_DIR, siteDomain, 'audits');
  if (!fs.existsSync(auditsDir)) continue;

  const auditFiles = fs.readdirSync(auditsDir)
    .filter(f => f.endsWith('-audit.md') && !f.startsWith('SUMMARY') && !f.startsWith('00-SUMMARY'));

  const pages = [];
  for (const file of auditFiles) {
    const content = fs.readFileSync(path.join(auditsDir, file), 'utf8');
    const page = parseReport(content);
    if (page) pages.push(page);
  }

  pages.sort((a, b) => a.path.localeCompare(b.path));

  const siteSlug = siteDomain.replace(/\./g, '-');
  fs.writeFileSync(
    path.join(OUTPUT_DIR, `${siteSlug}.json`),
    JSON.stringify({ site: siteDomain, pages }, null, 2),
  );

  const total = pages.reduce((n, p) => n + p.categories.flatMap(c => c.issues).length, 0);
  console.log(`${siteDomain}: ${pages.length} pages, ${total} issues → ${siteSlug}.json`);
}
