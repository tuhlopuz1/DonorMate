import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiSettings, FiBell, FiUser, FiTrash2 } from "react-icons/fi";
import { useState } from "react";

const SettingsPage = () => {
  const [notificationsEnabled, setNotificationsEnabled] = useState('all');

  const handleDeleteData = () => {

  };

  return (
    <>
      <PageTopBar title="Настройки" icon={<FiSettings size={20} />} />

      <div className="p-6 pt-20 pb-28 flex flex-col gap-6">

{/* Уведомления */}
<div className="bg-white rounded-xl p-5 shadow-md">
  <div className="flex items-center gap-3 mb-3">
    <FiBell size={20} />
    <h3 className="text-xl font-bold">Уведомления</h3>
  </div>
  <label className="flex flex-col gap-2">
    <span className="text-gray-800">Настройка уведомлений</span>
    <select
      value={notificationsEnabled}
      onChange={(e) => setNotificationsEnabled(e.target.value)}
      className="p-2 border border-gray-300 rounded-md"
    >
      <option value="all">Получать все уведомления</option>
      <option value="important">Только важные</option>
      <option value="none">Не получать уведомления</option>
    </select>
  </label>
</div>



        {/* Редактирование профиля (заглушка) */}
        <div className="bg-white rounded-xl p-5 shadow-md">
          <div className="flex items-center gap-3 mb-3">
            <FiUser size={20} />
            <h3 className="text-xl font-bold">Профиль</h3>
          </div>
          <button
            onClick={() => alert("Редактирование профиля пока не реализовано")}
            className="text-black"
          >
            Изменить личные данные
          </button>
        </div>

        {/* Удаление данных */}
        <div onClick={handleDeleteData} className="bg-white rounded-xl p-5 shadow-md border border-red-200">
          <div className="flex items-center gap-3 mb-3">
            <FiTrash2 size={20} className="text-red-600" />
            <h3 className="text-xl font-bold text-red-600">Удаление данных</h3>
          </div>
          <button
            
            className="text-red-600"
          >
            Удалить все мои данные
          </button>
        </div>
      </div>

      <BottomNavBar />
    </>
  );
};

export default SettingsPage;
