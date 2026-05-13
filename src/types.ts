export type Severity = 'critical' | 'needs-work' | 'minor';
export type SiteId = 'ubuntu.com' | 'canonical.com';

export interface Issue {
  description: string;
  location: string;
  line?: string;
  severity: Severity;
}

export interface Category {
  name: string;
  issues: Issue[];
}

export interface PageAudit {
  path: string;
  url: string;
  date: string;
  copyDocUrl?: string;
  categories: Category[];
}

export interface SiteData {
  site: SiteId;
  pages: PageAudit[];
}
