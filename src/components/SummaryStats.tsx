import type { PageAudit, Severity } from '../types';
import styles from './SummaryStats.module.css';

interface Props {
  pages: PageAudit[];
}

function countBySeverity(pages: PageAudit[], severity: Severity): number {
  return pages.flatMap((p) => p.categories).flatMap((c) => c.issues).filter((i) => i.severity === severity).length;
}

const stats: { severity: Severity; label: string }[] = [
  { severity: 'critical', label: 'Critical' },
  { severity: 'needs-work', label: 'Needs work' },
  { severity: 'minor', label: 'Minor' },
];

export default function SummaryStats({ pages }: Props) {
  return (
    <div className={styles.grid}>
      {stats.map(({ severity, label }) => (
        <div key={severity} className={`${styles.card} ${styles[severity]}`}>
          <span className={styles.count}>{countBySeverity(pages, severity)}</span>
          <span className={styles.label}>{label}</span>
        </div>
      ))}
    </div>
  );
}
