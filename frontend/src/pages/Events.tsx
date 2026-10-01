import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/client';
import type { SecurityEvent } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function Events() {
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [query, setQuery] = useState('');

  useEffect(() => {
    api.get('/events?size=50&sort=timestamp,desc').then((response) => setEvents(response.data.content ?? [])).catch(() => undefined);
  }, []);

  const filtered = events.filter((event) => [event.protocol, event.sourceIdentifier, event.destinationIdentifier].join(' ').toLowerCase().includes(query.toLowerCase()));

  return (
    <section>
      <div className="page-head">
        <div><h1>Event Monitor</h1><p>Searchable network-flow detection table</p></div>
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Filter events" />
      </div>
      <div className="panel">
        <table>
          <thead><tr><th>Time</th><th>Protocol</th><th>Source</th><th>Destination</th><th>Risk</th><th>Severity</th><th></th></tr></thead>
          <tbody>
            {filtered.map((event) => (
              <tr key={event.id}>
                <td>{new Date(event.timestamp).toLocaleString()}</td>
                <td>{event.protocol}</td>
                <td>{event.sourceIdentifier}:{event.sourcePort}</td>
                <td>{event.destinationIdentifier}:{event.destinationPort}</td>
                <td>{event.detection?.riskScore?.toFixed(1) ?? '-'}</td>
                <td>{event.detection && <SeverityBadge severity={event.detection.severity} />}</td>
                <td><Link to={`/events/${event.id}`}>Investigate</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="empty">No events match the current filter.</div>}
      </div>
    </section>
  );
}

