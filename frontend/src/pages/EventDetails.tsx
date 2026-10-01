import { FormEvent, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import type { SecurityEvent } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function EventDetails() {
  const { id } = useParams();
  const [event, setEvent] = useState<SecurityEvent | null>(null);
  const [note, setNote] = useState('');

  useEffect(() => {
    api.get(`/events/${id}`).then((response) => setEvent(response.data)).catch(() => undefined);
  }, [id]);

  const addNote = async (formEvent: FormEvent) => {
    formEvent.preventDefault();
    await api.post(`/events/${id}/notes`, { note });
    setNote('');
  };

  if (!event) return <div className="panel">Loading event...</div>;

  return (
    <section>
      <div className="page-head"><div><h1>Investigation</h1><p>{event.id}</p></div></div>
      <div className="grid-two">
        <div className="panel">
          <h2>Event Metadata</h2>
          <dl>
            <dt>Source</dt><dd>{event.sourceIdentifier}:{event.sourcePort}</dd>
            <dt>Destination</dt><dd>{event.destinationIdentifier}:{event.destinationPort}</dd>
            <dt>Protocol</dt><dd>{event.protocol}</dd>
            <dt>Timestamp</dt><dd>{new Date(event.timestamp).toLocaleString()}</dd>
          </dl>
        </div>
        <div className="panel">
          <h2>Detection</h2>
          {event.detection ? (
            <>
              <SeverityBadge severity={event.detection.severity} />
              <div className="risk-number">{event.detection.riskScore.toFixed(1)}</div>
              <p>{event.detection.modelName} {event.detection.modelVersion}</p>
              <ul>{event.detection.reasons.map((reason) => <li key={reason}>{reason}</li>)}</ul>
            </>
          ) : <div className="empty">No detection stored.</div>}
        </div>
      </div>
      <form className="panel note-form" onSubmit={addNote}>
        <h2>Analyst Note</h2>
        <textarea value={note} onChange={(e) => setNote(e.target.value)} placeholder="Add investigation note" />
        <button disabled={!note.trim()}>Add Note</button>
      </form>
    </section>
  );
}

