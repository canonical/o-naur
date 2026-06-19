export type Severity = 'critical' | 'needs-work' | 'minor';
export type SiteId = 'ubuntu.com' | 'canonical.com';
export type Lane = 'audit' | 'review';

// A pointer back to the copy style guide, so an owner can see *why* a
// recommendation was made. `url` is only present once a published guide URL
// is configured (STYLE_GUIDE_URL); otherwise the section + principle render
// inline as plain text.
export interface StyleRef {
  section: string;
  anchor?: string;
  principle: string;
  url?: string;
}

export interface Issue {
  description: string;
  location: string;
  line?: string;
  severity: Severity;
  // Advisory (copy review) lane only — optional so audit-lane issues are
  // unaffected.
  found?: string;
  recommendation?: string;
  whyItMatters?: string;
  styleRef?: StyleRef;
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
