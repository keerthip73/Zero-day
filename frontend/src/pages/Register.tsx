import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

export function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('analyst@zeroguard.local');
  const [password, setPassword] = useState('Password123');

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const response = await api.post('/auth/register', { email, password, role: 'ANALYST' });
    localStorage.setItem('zg_token', response.data.token);
    navigate('/');
  };

  return (
    <main className="auth-page">
      <form className="auth-panel" onSubmit={submit}>
        <h1>Create Account</h1>
        <p>Register a local analyst user</p>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" type="password" />
        <button>Create account</button>
      </form>
    </main>
  );
}

