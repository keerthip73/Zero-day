import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Alerts } from './pages/Alerts';
import { EventDetails } from './pages/EventDetails';
import { Events } from './pages/Events';
import { Login } from './pages/Login';
import { Model } from './pages/Model';
import { Overview } from './pages/Overview';
import { Register } from './pages/Register';
import { Settings } from './pages/Settings';
import './styles/app.css';

function Protected({ children }: { children: React.ReactNode }) {
  return localStorage.getItem('zg_token') ? children : <Navigate to="/login" />;
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Protected><Layout /></Protected>}>
          <Route index element={<Overview />} />
          <Route path="events" element={<Events />} />
          <Route path="events/:id" element={<EventDetails />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="model" element={<Model />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

