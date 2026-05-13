import { useEffect, useState } from 'react';
import type { SiteData, SiteId } from '../types';

const SITE_SLUG: Record<SiteId, string> = {
  'ubuntu.com': 'ubuntu-com',
  'canonical.com': 'canonical-com',
};

export function useSiteData(site: SiteId): {
  data: SiteData | null;
  loading: boolean;
  error: string | null;
} {
  const [data, setData] = useState<SiteData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch(`/data/${SITE_SLUG[site]}.json`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load data for ${site}`);
        return res.json() as Promise<SiteData>;
      })
      .then((json) => {
        if (!cancelled) {
          setData(json);
          setLoading(false);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Unknown error');
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [site]);

  return { data, loading, error };
}
