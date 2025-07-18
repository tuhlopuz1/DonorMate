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
import EventPage from './pages/Event';
import AdminMainPage from './pages/AdminMain';
import AdminUsersPage from './pages/AdminUsers';
import AdminEventsPage from './pages/AdminEvents';
import AdminReportPage from './pages/AdminReports';
import AdminEventPage from './pages/AdminEvent';
import QrScanner from './pages/QrScanner';
import CreateEventPage from './pages/CreateEvent';
import AddMedotvod from './pages/AddMedotvod';
import AskOrganizers from './pages/Question';
import AddUserPage from './pages/AddUser';
import Donorship from './pages/Donorship';



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
        <Route path="/ask-organizers" element={<AskOrganizers />} />
        <Route path="/event/:id" element={<EventPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/donorship" element={<Donorship />} />
        <Route path="/settings/profile" element={<ProfileSettings />} />
        <Route path="/admin/main" element={<AdminMainPage />} />
        <Route path="/admin/users" element={<AdminUsersPage />} />
        <Route path="/admin/events" element={<AdminEventsPage />} />
        <Route path="/admin/reports" element={<AdminReportPage />} />
        <Route path="/admin/event/:id" element={<AdminEventPage />} />
        <Route path="/admin/scanner" element={<QrScanner />} />
        <Route path="/admin/add-user" element={<AddUserPage />} />
        <Route path="/admin/create-event" element={<CreateEventPage />} />
        <Route path="/not-available" element={<NotAvailable />} />
        <Route path="/not-available" element={<NotAvailable />} />
        <Route path="/add-medotvod" element={<AddMedotvod />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </HashRouter>
  </React.StrictMode>
);
