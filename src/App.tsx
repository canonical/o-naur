import { useState } from 'react';
import type { SiteId } from './types';
import { useSiteData } from './hooks/useSiteData';
import SiteToggle from './components/SiteToggle';
import SummaryStats from './components/SummaryStats';
import PageList from './components/PageList';
import styles from './App.module.css';

export default function App() {
  const [activeSite, setActiveSite] = useState<SiteId>('ubuntu.com');
  const { data, loading, error } = useSiteData(activeSite);

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <h1 className={styles.title}>UX Audit</h1>
          <SiteToggle active={activeSite} onChange={setActiveSite} />
        </div>
      </header>
      <main className={styles.main}>
        {loading && <p className={styles.status}>Loading…</p>}
        {error && <p className={styles.status}>{error}</p>}
        {data && (
          <>
            <SummaryStats pages={data.pages} />
            <PageList pages={data.pages} />
          </>
        )}
      </main>
    </div>
  );
}
