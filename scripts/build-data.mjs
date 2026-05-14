import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPORTS_DIR = path.join(__dirname, '..', 'reports');
const OUTPUT_DIR = path.join(__dirname, '..', 'public', 'data');

// Emoji severity (Format A: {slug}-audit.md)
const EMOJI_SEVERITY = { '🔴': 'critical', '🟡': 'needs-work', '🔵': 'minor' };
// Plain-text severity (Formats B & C: numbered / ubuntu.com_ files)
const TEXT_SEVERITY = { 'critical': 'critical', 'needs work': 'needs-work', 'minor': 'minor' };

const SKIP_SECTIONS = new Set([
  'summary',
  'what looks good',
  '✅ what looks good',
  'recommended priority order',
  'manual checks for reviewer',
  '🔲 manual checks for reviewer',
  'ux quality check',
]);

function detectFormat(content) {
  if (/^## UX quality check/im.test(content)) return 'template-wrapped';   // ubuntu.com_ files
  if (/^### 🔴|^### 🟡|^### 🔵/m.test(content)) return 'simple';          // {slug}-audit.md files
  return 'template-bare';                                                    // numbered files
}

function parseSeverity(header, withEmoji) {
  if (withEmoji) {
    for (const [emoji, sev] of Object.entries(EMOJI_SEVERITY)) {
      if (header.includes(emoji)) return sev;
    }
  } else {
    const key = header.toLowerCase().trim();
    return TEXT_SEVERITY[key] ?? null;
  }
  return null;
}

function parseReport(content) {
  const urlMatch = content.match(/\*\*URL:\*\*\s*(https?:\/\/\S+)/);
  if (!urlMatch) return null;

  const url = urlMatch[1].trim();
  const date = content.match(/\*\*Date:\*\*\s*(\d{4}-\d{2}-\d{2})/)?.[1] ?? '';
  const copyDocRaw = content.match(/\*\*Copydoc:\*\*\s*(https?:\/\/\S+)/)?.[1] ?? '';
  const copyDocUrl = copyDocRaw || undefined;

  const urlObj = new URL(url);
  const pagePath = urlObj.pathname || '/';

  const format = detectFormat(content);
  const categories = [];
  let currentCategory = null;
  let currentSeverity = null;
  let inUxSection = false;
  let skip = false;

  for (const line of content.split('\n')) {
    if (format === 'simple') {
      // ## Category, ### 🔴/🟡/🔵 Severity
      if (line.startsWith('## ')) {
        if (currentCategory?.issues.length) categories.push(currentCategory);
        const name = line.slice(3).trim();
        skip = SKIP_SECTIONS.has(name.toLowerCase());
        currentCategory = skip ? null : { name, issues: [] };
        currentSeverity = null;
        continue;
      }
      if (skip) continue;
      if (line.startsWith('### ')) {
        currentSeverity = parseSeverity(line.slice(4).trim(), true);
        continue;
      }
    } else if (format === 'template-wrapped') {
      // ## UX quality check > ### Category > #### Severity (plain text)
      if (line.startsWith('## ')) {
        if (currentCategory?.issues.length) categories.push(currentCategory);
        currentCategory = null;
        currentSeverity = null;
        const sectionName = line.slice(3).trim().toLowerCase().replace(/^[✅🔲]\s*/, '');
        inUxSection = sectionName === 'ux quality check';
        continue;
      }
      if (!inUxSection) continue;
      if (line.startsWith('### ')) {
        if (currentCategory?.issues.length) categories.push(currentCategory);
        currentCategory = { name: line.slice(4).trim(), issues: [] };
        currentSeverity = null;
        continue;
      }
      if (line.startsWith('#### ')) {
        currentSeverity = parseSeverity(line.slice(5).trim(), false);
        continue;
      }
    } else {
      // template-bare: ### Category > #### Severity (plain text), no wrapper
      if (line.startsWith('## ')) {
        if (currentCategory?.issues.length) categories.push(currentCategory);
        const name = line.slice(3).trim();
        skip = SKIP_SECTIONS.has(name.toLowerCase());
        currentCategory = skip ? null : { name, issues: [] };
        currentSeverity = null;
        inUxSection = !skip;
        continue;
      }
      if (skip || !inUxSection) continue;
      if (line.startsWith('### ')) {
        if (currentCategory?.issues.length) categories.push(currentCategory);
        currentCategory = { name: line.slice(4).trim(), issues: [] };
        currentSeverity = null;
        continue;
      }
      if (line.startsWith('#### ')) {
        currentSeverity = parseSeverity(line.slice(5).trim(), false);
        continue;
      }
    }

    // Issue bullet — works for all formats
    if (currentCategory && currentSeverity && line.startsWith('- **')) {
      const match = line.match(/^- \*\*(.+?)\*\*:?\s*(?:[—\-]\s*)?(.+)?$/);
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

const EXCLUDED = new Set(['SUMMARY.md', 'COMPREHENSIVE_SUMMARY.md']);

const siteDirs = fs.readdirSync(REPORTS_DIR, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name);

for (const siteDomain of siteDirs) {
  const auditsDir = path.join(REPORTS_DIR, siteDomain, 'audits');
  if (!fs.existsSync(auditsDir)) continue;

  const auditFiles = fs.readdirSync(auditsDir).filter(f =>
    f.endsWith('.md') &&
    !EXCLUDED.has(f) &&
    !f.startsWith('00-SUMMARY') &&
    !f.startsWith('SUMMARY'),
  );

  const pages = [];
  for (const file of auditFiles) {
    const content = fs.readFileSync(path.join(auditsDir, file), 'utf8');
    const page = parseReport(content);
    if (page) pages.push(page);
  }

  // Deduplicate by path — keep the most recently dated entry
  const byPath = new Map();
  for (const page of pages) {
    const existing = byPath.get(page.path);
    if (!existing || page.date > existing.date) byPath.set(page.path, page);
  }

  const deduped = [...byPath.values()].sort((a, b) => a.path.localeCompare(b.path));

  const siteSlug = siteDomain.replace(/\./g, '-');
  fs.writeFileSync(
    path.join(OUTPUT_DIR, `${siteSlug}.json`),
    JSON.stringify({ site: siteDomain, pages: deduped }, null, 2),
  );

  const total = deduped.reduce((n, p) => n + p.categories.flatMap(c => c.issues).length, 0);
  console.log(`${siteDomain}: ${deduped.length} pages, ${total} issues → ${siteSlug}.json`);
}
