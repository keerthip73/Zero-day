import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Alert } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const load = () => api.get('/alerts').then((response) => setAlerts(response.data)).catch(() => undefined);
  useEffect(() => { load(); }, []);

  const update = async (id: string, status: string) => {
    await api.patch(`/alerts/${id}/status?status=${status}`);
    await load();
  };

  return (
    <section>
      <div className="page-head"><div><h1>Alerts</h1><p>High-risk activity requiring analyst review</p></div></div>
      <div className="panel">
        {alerts.map((alert) => (
          <div className="alert-row" key={alert.id}>
            <SeverityBadge severity={alert.severity} />
            <span>{alert.title}</span>
            <span>{alert.status}</span>
            <button onClick={() => update(alert.id, 'INVESTIGATING')}>Investigate</button>
            <button onClick={() => update(alert.id, 'FALSE_POSITIVE')}>False Positive</button>
            <button onClick={() => update(alert.id, 'RESOLVED')}>Resolve</button>
          </div>
        ))}
        {alerts.length === 0 && <div className="empty">No alerts yet.</div>}
      </div>
    </section>
  );
}

