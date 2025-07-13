import { FiHome, FiCalendar, FiClipboard, FiUser } from 'react-icons/fi';
import React from 'react';

type NavButtonProps = {
  label: string;
  Icon: React.ComponentType<{ size?: number; className?: string }>;
  active?: boolean;
  onClick?: () => void;
};

function NavButton({ label, Icon, active, onClick }: NavButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-center justify-center text-xs font-medium flex-1 py-2
        transition-colors duration-200
        ${active ? 'text-blue-600 bg-blue-100' : 'text-gray-500 hover:text-blue-600'}
      `}
      aria-label={label}
      type="button"
    >
      <Icon size={22} className="mb-1" />
      {label}
    </button>
  );
}

export default function BottomNavBar() {
  const current = window.location.href;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-md z-50">
      <div className="flex w-full max-w-md mx-auto">
        <NavButton
          label="Главная"
          Icon={FiHome}
          active={current.includes('#/main')}
          onClick={() => (window.location.href = '#/main')}
        />
        <NavButton
          label="Расписание"
          Icon={FiCalendar}
          active={current.includes('#/schedule')}
          onClick={() => (window.location.href = '#/schedule')}
        />
        <NavButton
          label="Мои записи"
          Icon={FiClipboard}
          active={current.includes('#/appointments')}
          onClick={() => (window.location.href = '#/appointments')}
        />
        <NavButton
          label="Профиль"
          Icon={FiUser}
          active={current.includes('#/profile')}
          onClick={() => (window.location.href = '#/profile')}
        />
      </div>
    </nav>
  );
}
