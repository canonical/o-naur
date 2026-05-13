import { useState } from 'react';
import type { PageAudit } from '../types';
import PageRow from './PageRow';
import styles from './PageList.module.css';

interface Props {
  pages: PageAudit[];
}

export default function PageList({ pages }: Props) {
  const [query, setQuery] = useState('');

  const withIssues = pages.filter((page) =>
    page.categories.some((c) => c.issues.length > 0),
  );

  const filtered = query.trim()
    ? withIssues.filter((page) =>
        page.path.toLowerCase().includes(query.trim().toLowerCase()),
      )
    : withIssues;

  return (
    <div className={styles.list}>
      <div className={styles.toolbar}>
        <div className={styles.searchWrap}>
          <svg className={styles.searchIcon} width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <circle cx="6.5" cy="6.5" r="5" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M10.5 10.5L14 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <input
            className={styles.searchInput}
            type="search"
            placeholder="Search pages…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label="Search pages"
          />
          {query && (
            <button
              className={styles.clearBtn}
              onClick={() => setQuery('')}
              aria-label="Clear search"
            >
              ×
            </button>
          )}
        </div>
      </div>
      <div className={styles.header}>
        <span>Page</span>
        <span className={styles.colIssues}>Issues</span>
      </div>
      {filtered.length > 0 ? (
        filtered.map((page) => <PageRow key={page.path} page={page} />)
      ) : (
        <p className={styles.empty}>
          {query ? `No pages matching "${query}"` : 'No pages with issues'}
        </p>
      )}
    </div>
  );
}
