import { useState } from 'react';
import type { PageAudit } from '../types';
import CategorySection from './CategorySection';
import styles from './PageRow.module.css';

interface Props {
  page: PageAudit;
}

function totalIssues(page: PageAudit): number {
  return page.categories.flatMap((c) => c.issues).length;
}

export default function PageRow({ page }: Props) {
  const [expanded, setExpanded] = useState(false);
  const total = totalIssues(page);

  return (
    <div className={styles.wrapper}>
      <button
        className={`${styles.row} ${expanded ? styles.rowExpanded : ''}`}
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <span className={styles.titleCell}>
          <span className={styles.chevron}>{expanded ? '▾' : '▸'}</span>
          <span className={styles.title}>{page.path}</span>
        </span>
        <span className={styles.count}>{total}</span>
      </button>

      {expanded && (
        <div className={styles.detail}>
          {page.copyDocUrl && (
            <a
              className={styles.copyDoc}
              href={page.copyDocUrl}
              target="_blank"
              rel="noreferrer"
            >
              Copy doc ↗
            </a>
          )}
          {page.categories.map((category) => (
            <CategorySection key={category.name} category={category} />
          ))}
        </div>
      )}
    </div>
  );
}
