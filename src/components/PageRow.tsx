import { useState } from 'react';
import type { PageAudit, Severity } from '../types';
import CategorySection from './CategorySection';
import styles from './PageRow.module.css';

interface Props {
  page: PageAudit;
}

const AVATAR_COLORS = [
  '#7764E4', '#0099D8', '#38A169', '#DD6B20', '#D53F8C',
  '#3182CE', '#805AD5', '#2C7A7B',
];

function avatarColor(initials: string): string {
  const idx = initials.charCodeAt(0) % AVATAR_COLORS.length;
  return AVATAR_COLORS[idx];
}

function countSeverity(page: PageAudit, severity: Severity): number {
  return page.categories.flatMap((c) => c.issues).filter((i) => i.severity === severity).length;
}

function totalIssues(page: PageAudit): number {
  return page.categories.flatMap((c) => c.issues).length;
}

export default function PageRow({ page }: Props) {
  const [expanded, setExpanded] = useState(false);
  const critical = countSeverity(page, 'critical');
  const needsWork = countSeverity(page, 'needs-work');
  const minor = countSeverity(page, 'minor');
  const total = totalIssues(page);

  return (
    <div className={styles.wrapper}>
      <button
        className={`${styles.row} ${expanded ? styles.rowExpanded : ''}`}
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
      >
        <span className={styles.pathCell}>
          <span className={styles.chevron}>{expanded ? '▾' : '▸'}</span>
          <code className={styles.path}>{page.path}</code>
          <span className={styles.date}>{page.date}</span>
        </span>

        <span className={styles.ownerCell}>
          <span
            className={styles.avatar}
            style={{ background: avatarColor(page.ownerInitials) }}
          >
            {page.ownerInitials}
          </span>
          <span className={styles.ownerName}>{page.owner}</span>
        </span>

        <span className={styles.issuesCell}>
          <span className={styles.total}>{total}</span>
          <span className={styles.breakdown}>
            {critical > 0 && <span className={styles.critical}>{critical}</span>}
            {needsWork > 0 && <span className={styles.needsWork}>{needsWork}</span>}
            {minor > 0 && <span className={styles.minor}>{minor}</span>}
          </span>
        </span>
      </button>

      {expanded && (
        <div className={styles.detail}>
          {page.categories.map((category) => (
            <CategorySection key={category.name} category={category} />
          ))}
        </div>
      )}
    </div>
  );
}
