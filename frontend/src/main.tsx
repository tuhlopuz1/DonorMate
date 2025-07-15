// main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import About from './pages/About';
import WelcomePage from './pages/Welcome';
import NotFound from './pages/NotFound';
import './index.css';
import UserSurvey from './pages/UserSurvey';
import MainPage from './pages/Main';
import AppointmentsPage from './pages/Appointments';
import SchedulePage from './pages/Schedule';
import ProfilePage from './pages/Profile';
import NotAvailable from './pages/NotAvailable';
import NotificationsPage from './pages/Notifications';
import SettingsPage from './pages/Settings';
import ProfileSettings from './pages/ProfileSettings';



ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <HashRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/about" element={<About />} />
        <Route path="/welcome" element={<WelcomePage />} />
        <Route path="/survey" element={<UserSurvey />} />
        <Route path="/main" element={<MainPage />} />
        <Route path="/appointments" element={<AppointmentsPage />} />
        <Route path="/schedule" element={<SchedulePage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/notifications" element={<NotificationsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/settings/profile" element={<ProfileSettings />} />
        <Route path="/not-available" element={<NotAvailable />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </HashRouter>
  </React.StrictMode>
);
