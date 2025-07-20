import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import React from "react";

type PageTopBarProps = {
  title: string;
  icon: React.ReactNode;
};

export default function PageTopBar({ title, icon }: PageTopBarProps) {
  const navigate = useNavigate();

  return (
    <header className="fixed top-0 left-0 z-50 w-full bg-blue-500 text-white px-4 py-2 flex items-center shadow-md">
      {/* Кнопка назад */}
      <button
        onClick={() => navigate(-1)}
        className="p-2 rounded-full hover:bg-blue-600 transition"
      >
        <ArrowLeft className="w-6 h-6" />
      </button>

      {/* Иконка страницы и заголовок */}
      <div className="flex items-center space-x-2 ml-4">
        <div className="text-white">{icon}</div>
        <h1 className="text-lg font-semibold">{title}</h1>
      </div>
    </header>
  );
}
