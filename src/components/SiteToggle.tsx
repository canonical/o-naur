import type { SiteId } from '../types';
import styles from './SiteToggle.module.css';

interface Props {
  active: SiteId;
  onChange: (site: SiteId) => void;
}

const sites: SiteId[] = ['ubuntu.com', 'canonical.com'];

export default function SiteToggle({ active, onChange }: Props) {
  return (
    <div className={styles.toggle}>
      {sites.map((site) => (
        <button
          key={site}
          className={`${styles.option} ${active === site ? styles.active : ''}`}
          onClick={() => onChange(site)}
        >
          {site}
        </button>
      ))}
    </div>
  );
}
