import type { Category, Severity } from '../types';
import styles from './CategorySection.module.css';

interface Props {
  category: Category;
}

const SEVERITY_LABEL: Record<Severity, string> = {
  critical: 'Critical',
  'needs-work': 'Needs work',
  minor: 'Minor',
};

export default function CategorySection({ category }: Props) {
  if (category.issues.length === 0) return null;

  return (
    <div className={styles.section}>
      <div className={styles.heading}>
        <span className={styles.name}>{category.name}</span>
        <span className={styles.count}>{category.issues.length}</span>
      </div>
      <ul className={styles.issues}>
        {category.issues.map((issue, i) => (
          <li key={i} className={styles.issue}>
            <span className={styles.body}>
              <span className={styles.description}>{issue.description}</span>
              {issue.location && (
                <span className={styles.location}>{issue.location}</span>
              )}
              {issue.line && <code className={styles.line}>{issue.line}</code>}

              {issue.whyItMatters && (
                <span className={styles.detail}>
                  <span className={styles.detailLabel}>Why it matters</span>
                  {issue.whyItMatters}
                </span>
              )}
              {issue.found && (
                <span className={styles.detail}>
                  <span className={styles.detailLabel}>Found</span>
                  <q className={styles.found}>{issue.found}</q>
                </span>
              )}
              {issue.recommendation && (
                <span className={styles.detail}>
                  <span className={styles.detailLabel}>Suggested fix</span>
                  {issue.recommendation}
                </span>
              )}
              {issue.styleRef && (
                <span className={styles.source}>
                  Source:{' '}
                  {issue.styleRef.url ? (
                    <a
                      href={issue.styleRef.url}
                      target="_blank"
                      rel="noreferrer"
                      className={styles.sourceLink}
                    >
                      {issue.styleRef.section}
                    </a>
                  ) : (
                    <span className={styles.sourceName}>
                      {issue.styleRef.section}
                    </span>
                  )}
                  {' — '}
                  <span className={styles.principle}>
                    “{issue.styleRef.principle}”
                  </span>
                </span>
              )}
            </span>
            <span className={`${styles.badge} ${styles[issue.severity]}`}>
              {SEVERITY_LABEL[issue.severity]}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
