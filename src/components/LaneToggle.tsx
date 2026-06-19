import type { Lane } from '../types';
import styles from './SiteToggle.module.css';

interface Props {
  active: Lane;
  onChange: (lane: Lane) => void;
}

const LANES: { id: Lane; label: string }[] = [
  { id: 'audit', label: 'Deterministic audit' },
  { id: 'review', label: 'Copy review (advisory)' },
];

export default function LaneToggle({ active, onChange }: Props) {
  return (
    <div className={styles.toggle}>
      {LANES.map((lane) => (
        <button
          key={lane.id}
          className={`${styles.option} ${active === lane.id ? styles.active : ''}`}
          onClick={() => onChange(lane.id)}
        >
          {lane.label}
        </button>
      ))}
    </div>
  );
}
