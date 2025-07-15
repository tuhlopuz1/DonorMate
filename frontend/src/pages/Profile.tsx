import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiUser, FiEdit, FiBell } from "react-icons/fi";

const ProfilePage = () => {
  const user = {
    name: "Никитин Владимир",
    birthDate: "2002-05-14",
    faculty: "ФКТИ",
    group: "ИКБО-01-21",
    donations: 7,
    lastDonation: "2025-06-12",
    nextAvailableDate: "2025-08-12",
    medicallyAccepted: false,
  };

  return (
    <>
      <PageTopBar title="Профиль" icon={<FiUser size={20} />} />

      <div className="p-6 pt-20 pb-28 flex flex-col gap-6">
        <div className="bg-blue-600 text-white rounded-xl p-6 shadow-md">
          <h2 className="text-2xl font-bold mb-2">{user.name}</h2>
          <p className="text-sm text-white/80">Факультет: {user.faculty}</p>
          <p className="text-sm text-white/80">Группа: {user.group}</p>
          <p className="text-sm text-white/80">Дата рождения: {user.birthDate}</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">История донаций</h3>
          <p className="text-gray-700">Всего донаций: <b>{user.donations}</b></p>
          <p className="text-gray-700">Последняя донация: {user.lastDonation}</p>
          <p className="text-gray-700">Следующая возможная: {user.nextAvailableDate}</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">Медицинский статус</h3>
          <p className={`font-semibold ${user.medicallyAccepted === true ? "text-green-600" : "text-red-500"}`}>
            {user.medicallyAccepted ? "Допущен" : "Не допущен"}
          </p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">Настройки</h3>
          <div className="flex items-center justify-between py-2">
            <span className="text-gray-700">Уведомления</span>
            <FiBell size={20} className="text-gray-600" />
          </div>
          <div className="flex items-center justify-between py-2">
            <span className="text-gray-700">Редактировать профиль</span>
            <FiEdit size={20} className="text-gray-600" />
          </div>
        </div>
      </div>

      <BottomNavBar />
    </>
  );
};

export default ProfilePage;
