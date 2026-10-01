import type { Severity } from '../types/api';

export function SeverityBadge({ severity }: { severity: Severity }) {
  return <span className={`badge ${severity.toLowerCase()}`}>{severity.replaceAll('_', ' ')}</span>;
}

