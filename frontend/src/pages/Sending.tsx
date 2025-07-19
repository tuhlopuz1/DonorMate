import React, { useState } from "react";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiSend } from "react-icons/fi";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";



const Broadcasts: React.FC = () => {
  const [message, setMessage] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("");

  const handleSend = () => {
    if (!message.trim() || !selectedCategory) {
      alert("Введите сообщение и выберите категорию");
      return;
    }

    console.log("Рассылка отправлена", {
      message,
      category: selectedCategory,
    });

    alert("Рассылка отправлена!");
    setMessage("");
    setSelectedCategory("");
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
        <AdminPageTopBar title="Рассылка" icon={<FiSend />}/>
      <h1 className="text-3xl font-semibold mb-6">Рассылки</h1>

      {/* Категория */}
      <div className="bg-white shadow-md rounded-xl mb-6">
        <div className="p-4">
          <h2 className="text-xl font-medium mb-4">Рассылка всем пользователям</h2>
        </div>
      </div>

      {/* Сообщение */}
      <div className="bg-white shadow-md rounded-xl mb-6">
        <div className="p-4">
          <h2 className="text-xl font-medium mb-4">Сообщение</h2>
          <textarea
            placeholder="Введите текст рассылки..."
            className="w-full min-h-[120px] p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>
      </div>

      {/* Кнопка */}
      <div className="text-right">
        <button
          onClick={handleSend}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg text-lg transition"
        >
          Отправить
        </button>
      </div>
      <AdminBottomNavBar />
    </div>
  );
};

export default Broadcasts;
