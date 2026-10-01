export function Settings() {
  return (
    <section>
      <div className="page-head"><div><h1>Settings</h1><p>Local academic project configuration</p></div></div>
      <div className="panel prose">
        <p>Backend API URL is controlled by <code>VITE_API_BASE_URL</code>. Alerts are created when risk score crosses the backend <code>ALERT_RISK_THRESHOLD</code>.</p>
      </div>
    </section>
  );
}

