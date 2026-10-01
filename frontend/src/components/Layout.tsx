import { Activity, Bell, Gauge, LogOut, Radar, Settings, ShieldAlert } from 'lucide-react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';

const items = [
  { to: '/', label: 'Overview', icon: Gauge },
  { to: '/events', label: 'Event Monitor', icon: Radar },
  { to: '/alerts', label: 'Alerts', icon: Bell },
  { to: '/model', label: 'Model', icon: Activity },
  { to: '/settings', label: 'Settings', icon: Settings }
];

export function Layout() {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem('zg_token');
    navigate('/login');
  };

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand"><ShieldAlert size={24} /> ZeroGuard AI</div>
        <nav>
          {items.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
        <button className="nav-item logout" onClick={logout}><LogOut size={18} /> Logout</button>
      </aside>
      <main className="main"><Outlet /></main>
    </div>
  );
}

