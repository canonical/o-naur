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
              <span className={styles.location}>{issue.location}</span>
              {issue.line && <code className={styles.line}>{issue.line}</code>}
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
