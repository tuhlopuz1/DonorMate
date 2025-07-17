import { useState } from "react";
import { FiPlus } from "react-icons/fi";
import { MdEvent } from "react-icons/md";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import BottomNavBar from "../components/layouts/NavBar";

export default function CreateEventPage() {
  const [title, setTitle] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [seats, setSeats] = useState("");
  const [description, setDescription] = useState("");
  const [address, setAddress] = useState("");

  const handleSave = () => {
    console.log("Создание мероприятия:", {
      title,
      date,
      time,
      seats,
      description,
      address,
    });
    // TODO: отправка на сервер
  };

  return (
    <div className="p-6 pt-20 max-w-xl mx-auto">
      <AdminPageTopBar title="Создание мероприятия" icon={<MdEvent size={20} />} />
      <h1 className="text-2xl font-bold text-black mb-6 flex items-center gap-2">
        Создание мероприятия
      </h1>

      <div className="space-y-5">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
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
          type="text"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          placeholder="Время мероприятия (например, 13:00-15:00)"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="number"
          value={seats}
          onChange={(e) => setSeats(e.target.value)}
          placeholder="Количество мест"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          min="1"
        />

        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Описание мероприятия"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
          rows={4}
        />

        <input
          type="text"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          placeholder="Адрес мероприятия"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

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
