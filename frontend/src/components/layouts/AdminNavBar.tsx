import { FiHome, FiCalendar, FiUsers} from 'react-icons/fi';
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
        ${active ? 'text-red-600 bg-red-100' : 'text-gray-500 hover:text-red-600'}
      `}
      aria-label={label}
      type="button"
    >
      <Icon size={22} className="mb-1" />
      {label}
    </button>
  );
}

export default function AdminBottomNavBar() {
  const current = window.location.href;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-md z-50">
      <div className="flex w-full max-w-md mx-auto">
        <NavButton
          label="Главная"
          Icon={FiHome}
          active={current.includes('#/admin/main')}
          onClick={() => (window.location.href = '#/admin/main')}
        />
        <NavButton
          label="Пользователи"
          Icon={FiUsers}
          active={current.includes('#/admin/users')}
          onClick={() => (window.location.href = '#/admin/users')}
        />
        <NavButton
          label="Мероприятия"
          Icon={FiCalendar}
          active={current.includes('#/admin/events')}
          onClick={() => (window.location.href = '#/admin/events')}
        />
        {/* <NavButton
          label="Отчёты"
          Icon={FiFileText}
          active={current.includes('#/admin/reports')}
          onClick={() => (window.location.href = '#/admin/reports')}
        /> */}
      </div>
    </nav>
  );
}
