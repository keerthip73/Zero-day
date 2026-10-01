import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api } from '../api/client';
import { demoEvents } from '../api/demoEvents';
import type { Alert, DashboardSummary, SecurityEvent } from '../types/api';
import { SeverityBadge } from '../components/SeverityBadge';

export function Overview() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const load = async () => {
    const [summaryResponse, eventsResponse, alertsResponse] = await Promise.all([
      api.get('/dashboard/summary'),
      api.get('/events?size=8&sort=timestamp,desc'),
      api.get('/alerts')
    ]);
    setSummary(summaryResponse.data);
    setEvents(eventsResponse.data.content ?? []);
    setAlerts(alertsResponse.data);
  };

  useEffect(() => {
    load().catch(() => undefined);
  }, []);

  const ingestDemo = async () => {
    await Promise.all(demoEvents.map((event) => api.post('/events', { ...event, timestamp: new Date().toISOString() })));
    await load();
  };

  const severityData = [
    { name: 'Normal', value: summary?.normalEvents ?? 0, color: '#22c55e' },
    { name: 'Suspicious', value: summary?.suspiciousEvents ?? 0, color: '#eab308' },
    { name: 'High Risk', value: summary?.highRiskEvents ?? 0, color: '#f97316' },
    { name: 'Open Alerts', value: summary?.criticalAlerts ?? 0, color: '#ef4444' }
  ];

  const riskData = events.map((event) => ({
    name: event.id.slice(0, 6),
    risk: event.detection?.riskScore ?? 0
  }));

  return (
    <section>
      <div className="page-head">
        <div>
          <h1>Security Overview</h1>
          <p>Network-flow anomaly monitoring and analyst triage</p>
        </div>
        <button onClick={ingestDemo}>Run Demo Events</button>
      </div>
      <div className="kpi-grid">
        <Kpi label="Total Events" value={summary?.totalEvents ?? 0} />
        <Kpi label="Normal" value={summary?.normalEvents ?? 0} />
        <Kpi label="Suspicious" value={summary?.suspiciousEvents ?? 0} />
        <Kpi label="High Risk" value={summary?.highRiskEvents ?? 0} />
        <Kpi label="Open Alerts" value={summary?.criticalAlerts ?? 0} />
        <Kpi label="Avg Risk" value={(summary?.averageRiskScore ?? 0).toFixed(1)} />
      </div>
      <div className="grid-two">
        <div className="panel">
          <h2>Severity Distribution</h2>
          <ResponsiveContainer height={260}>
            <PieChart>
              <Pie data={severityData} dataKey="value" nameKey="name" outerRadius={90}>
                {severityData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="panel">
          <h2>Recent Risk Scores</h2>
          <ResponsiveContainer height={260}>
            <BarChart data={riskData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#23304a" />
              <XAxis dataKey="name" stroke="#90a4c4" />
              <YAxis stroke="#90a4c4" domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="risk" fill="#38bdf8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="panel">
        <h2>Recent Alerts</h2>
        {alerts.length === 0 ? <div className="empty">No high-risk alerts yet.</div> : alerts.map((alert) => (
          <div className="alert-row" key={alert.id}>
            <SeverityBadge severity={alert.severity} />
            <span>{alert.title}</span>
            <span>{alert.status}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function Kpi({ label, value }: { label: string; value: string | number }) {
  return <div className="kpi"><span>{label}</span><strong>{value}</strong></div>;
}

