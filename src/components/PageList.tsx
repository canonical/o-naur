import type { PageAudit } from '../types';
import PageRow from './PageRow';
import styles from './PageList.module.css';

interface Props {
  pages: PageAudit[];
}

export default function PageList({ pages }: Props) {
  return (
    <div className={styles.list}>
      <div className={styles.header}>
        <span className={styles.colPath}>Page</span>
        <span className={styles.colOwner}>Owner</span>
        <span className={styles.colIssues}>Issues</span>
      </div>
      {pages.map((page) => (
        <PageRow key={page.path} page={page} />
      ))}
    </div>
  );
}
