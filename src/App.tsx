import { useState } from 'react';
import type { SiteData, SiteId } from './types';
import ubuntuData from './data/ubuntu-com.json';
import canonicalData from './data/canonical-com.json';
import SiteToggle from './components/SiteToggle';
import SummaryStats from './components/SummaryStats';
import PageList from './components/PageList';
import styles from './App.module.css';

const sites: Record<SiteId, SiteData> = {
  'ubuntu.com': ubuntuData as SiteData,
  'canonical.com': canonicalData as SiteData,
};

export default function App() {
  const [activeSite, setActiveSite] = useState<SiteId>('ubuntu.com');
  const siteData = sites[activeSite];

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <h1 className={styles.title}>UX Audit</h1>
          <SiteToggle active={activeSite} onChange={setActiveSite} />
        </div>
      </header>
      <main className={styles.main}>
        <SummaryStats pages={siteData.pages} />
        <PageList pages={siteData.pages} />
      </main>
    </div>
  );
}
