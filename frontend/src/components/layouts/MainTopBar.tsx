// src/components/TopBar.tsx
// import { Bell } from "lucide-react";
import logo from "../../assets/donor_logo.jpg"

export default function MainTopBar() {
  return (
    <header className="fixed top-0 left-0 z-50 w-full bg-blue-500 text-white px-4 py-2 flex items-center justify-between shadow-md">
      <div className="flex items-center space-x-3">
        {/* Заглушка логотипа */}
        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
          <img src={logo} className="rounded-full"></img>
        </div>
        <h1 className="text-xl font-semibold">DonorMate</h1>
      </div>

      {/* Кнопка уведомлений */}
      {/* <button onClick={() => {window.location.href = '/#/notifications'}} className="relative p-2 hover:bg-blue-500 rounded-full transition">
        <Bell className="w-6 h-6 text-white" />
      </button> */}
    </header>
  );
}
