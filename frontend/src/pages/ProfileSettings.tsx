import { useState } from "react";
import { FiUser, FiSave } from "react-icons/fi";
import PageTopBar from "../components/layouts/PageTopBar";


export default function ProfileSettings() {
  const [fullName, setFullName] = useState("Иванов Иван Иванович");
  const [gender, setGender] = useState("Мужской");
  const [faculty, setFaculty] = useState("Институт физики");
  const [group, setGroup] = useState("ФИ-101");

  const handleSave = () => {
    console.log("Сохранение профиля:", {
      fullName,
      gender,
      faculty,
      group,
    });
    // TODO: отправка на сервер
  };

  return (
    <div className="p-6 pt-20 max-w-xl mx-auto">
        <PageTopBar title="Настройки профиля" icon={<FiUser size={20}/>}/>
      <h1 className="text-2xl font-bold text-black mb-6 flex items-center gap-2">
        <FiUser /> Настройки профиля
      </h1>

      <div className="space-y-5">
        <input
          type="text"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Фамилия Имя Отчество"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <select
          value={gender}
          onChange={(e) => setGender(e.target.value)}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        >
          <option>Мужской</option>
          <option>Женский</option>
          <option>Предпочитаю не указывать</option>
        </select>

        <input
          type="text"
          value={faculty}
          onChange={(e) => setFaculty(e.target.value)}
          placeholder="Факультет / Институт"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="text"
          value={group}
          onChange={(e) => setGroup(e.target.value)}
          placeholder="Учебная группа"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <button
          onClick={handleSave}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl shadow-lg transition-all duration-300 flex items-center justify-center gap-2"
        >
          <FiSave /> Сохранить изменения
        </button>
      </div>
    </div>
  );
}
