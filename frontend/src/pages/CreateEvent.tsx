import { useState } from "react";
import { FiPlus } from "react-icons/fi";
import { MdEvent } from "react-icons/md";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import BottomNavBar from "../components/layouts/NavBar";
import apiRequest from "../components/utils/apiRequest"; // Путь подкорректируй под свой проект

export default function CreateEventPage() {
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [timeStart, setTimeStart] = useState("");
  const [timeEnd, setTimeEnd] = useState("");
  const [description, setDescription] = useState("");
  const [place, setPlace] = useState("ЦК ФМБА");

  const handleSave = async () => {
    if (!name || !date || !timeStart || !timeEnd || !description || !place) {
      alert("Пожалуйста, заполните все поля");
      return;
    }

    const start_date = new Date(`${date}T${timeStart}`).toISOString();
    const end_date = new Date(`${date}T${timeEnd}`).toISOString();

    const payload = {
      name,
      start_date,
      end_date,
      organizer: 0, // замените на ID текущего пользователя, если он есть
      description,
      place,
    };

    try {
      const response = await apiRequest({
        url: "https://api.donor.vickz.ru/api/create-event",
        method: "POST",
        body: payload,
        auth: true,
      });

      if (response.ok) {
        alert("Мероприятие успешно создано!");
      } else {
        const error = await response.json();
        alert(`Ошибка: ${error.message || "Не удалось создать мероприятие"}`);
      }
    } catch (err) {
      alert("Ошибка при отправке запроса");
    }
  };

  return (
    <div className="p-6 py-20 h-full max-w-xl mx-auto">
      <AdminPageTopBar title="Создание мероприятия" icon={<MdEvent size={20} />} />
      <h1 className="text-2xl font-bold text-black mb-6 flex items-center gap-2">
        Создание мероприятия
      </h1>

      <div className="space-y-5">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Название мероприятия"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="time"
          value={timeStart}
          onChange={(e) => setTimeStart(e.target.value)}
          placeholder="Начало (например, 13:00)"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="time"
          value={timeEnd}
          onChange={(e) => setTimeEnd(e.target.value)}
          placeholder="Окончание (например, 15:00)"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Описание мероприятия"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
          rows={4}
        />

        <select
          value={place}
          onChange={(e) => setPlace(e.target.value)}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
        >
          <option value="ЦК ФМБА">ЦК ФМБА</option>
          <option value="ЦК им. Гаврилова">ЦК им. Гаврилова</option>
        </select>

        <button
          onClick={handleSave}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl shadow-lg transition-all duration-300 flex items-center justify-center gap-2"
        >
          <FiPlus /> Добавить мероприятие
        </button>
      </div>

      <BottomNavBar />
    </div>
  );
}
