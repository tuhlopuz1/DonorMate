// src/components/TopBar.tsx
import { Bell } from "lucide-react";

export default function MainTopBar() {
  return (
    <header className="fixed top-0 left-0 z-50 w-full bg-blue-500 text-white px-4 py-2 flex items-center justify-between shadow-md">
      <div className="flex items-center space-x-3">
        {/* Заглушка логотипа */}
        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
          <span className="text-blue-600 font-bold">L</span>
        </div>
        <h1 className="text-xl font-semibold">DonorMate</h1>
      </div>

      {/* Кнопка уведомлений */}
      <button className="relative p-2 hover:bg-blue-500 rounded-full transition">
        <Bell className="w-6 h-6 text-white" />
        {/* <span className="absolute top-0 right-0 block w-2 h-2 bg-red-500 rounded-full ring-2 "></span> */}
      </button>
    </header>
  );
}
