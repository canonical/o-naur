import { useState } from 'react';
import type { Lane, SiteId } from './types';
import { useSiteData } from './hooks/useSiteData';
import SiteToggle from './components/SiteToggle';
import LaneToggle from './components/LaneToggle';
import SummaryStats from './components/SummaryStats';
import PageList from './components/PageList';
import styles from './App.module.css';

export default function App() {
  const [activeSite, setActiveSite] = useState<SiteId>('ubuntu.com');
  const [activeLane, setActiveLane] = useState<Lane>('audit');
  const { data, loading, error } = useSiteData(activeSite, activeLane);

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <h1 className={styles.title}>UX Audit</h1>
          <div className={styles.toggles}>
            <LaneToggle active={activeLane} onChange={setActiveLane} />
            <SiteToggle active={activeSite} onChange={setActiveSite} />
          </div>
        </div>
      </header>
      <main className={styles.main}>
        {activeLane === 'review' && (
          <p className={styles.advisory}>
            Advisory copy review — judgement calls for page owners to weigh.
            Not auto-applied and never sent to Bauer.
          </p>
        )}
        {loading && <p className={styles.status}>Loading…</p>}
        {error && <p className={styles.status}>{error}</p>}
        {data && (
          <>
            <SummaryStats pages={data.pages} />
            <PageList key={`${activeSite}-${activeLane}`} pages={data.pages} />
          </>
        )}
      </main>
    </div>
  );
}
