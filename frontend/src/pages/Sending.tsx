import React, { useState } from "react";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiSend } from "react-icons/fi";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import apiRequest from "../components/utils/apiRequest"; // Убедитесь, что путь к apiRequest корректный

const Broadcasts: React.FC = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) {
      alert("Введите сообщение");
      return;
    }

    try {
      setIsLoading(true);
      const response = await apiRequest({
        url: "https://api.donor.vickz.ru/api/send-msg-all-usr",
        method: "POST",
        body: {message: message},
        auth: true,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Ошибка отправки: ${errorText}`);
      }

      alert("Рассылка отправлена!");
      setMessage("");
    } catch (error) {
      console.error("Ошибка при отправке рассылки:", error);
      alert("Не удалось отправить рассылку. Попробуйте позже.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <AdminPageTopBar title="Рассылка" icon={<FiSend />} />
      <h1 className="text-3xl font-semibold mb-6">Рассылки</h1>

      {/* Категория (временно убрана, если не используется) */}
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
          disabled={isLoading}
          className={`${
            isLoading ? "bg-blue-400" : "bg-blue-600 hover:bg-blue-700"
          } text-white font-medium px-6 py-2 rounded-lg text-lg transition`}
        >
          {isLoading ? "Отправка..." : "Отправить"}
        </button>
      </div>
      <AdminBottomNavBar />
    </div>
  );
};

export default Broadcasts;
