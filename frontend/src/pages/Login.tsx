import { FormEvent, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

export function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('analyst@zeroguard.local');
  const [password, setPassword] = useState('Password123');
  const [error, setError] = useState('');

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    try {
      const response = await api.post('/auth/login', { email, password });
      localStorage.setItem('zg_token', response.data.token);
      navigate('/');
    } catch {
      setError('Login failed. Register a demo analyst first or check the backend.');
    }
  };

  return (
    <main className="auth-page">
      <form className="auth-panel" onSubmit={submit}>
        <h1>ZeroGuard AI</h1>
        <p>Security analyst console</p>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
        {error && <div className="error">{error}</div>}
        <button>Sign in</button>
        <Link to="/register">Create analyst account</Link>
      </form>
    </main>
  );
}

