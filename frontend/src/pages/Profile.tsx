import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiUser, FiSettings } from "react-icons/fi";

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

  const medotvods = [
    {
      startDate: "2025-06-15",
      endDate: "2025-07-01",
      comment: "ОРВИ, временный отвод",
    },
    {
      startDate: "2024-12-10",
      endDate: "2024-12-25",
      comment: "Послеоперационный период",
    },
  ];

  return (
    <>
      <PageTopBar title="Профиль" icon={<FiUser size={20} />} />

      <div className="p-6 pt-20 pb-28 flex flex-col gap-6">
        {/* Карточка пользователя */}
        <div className="bg-blue-600 text-white rounded-xl p-6 shadow-md">
          <h2 className="text-2xl font-bold mb-2">{user.name}</h2>
          <p className="text-sm text-white/80">Факультет: {user.faculty}</p>
          <p className="text-sm text-white/80">Группа: {user.group}</p>
          <p className="text-sm text-white/80">Дата рождения: {user.birthDate}</p>
        </div>

        {/* История донаций */}
        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">История донаций</h3>
          <p className="text-gray-700">Всего донаций: <b>{user.donations}</b></p>
          <p className="text-gray-700">Последняя донация: {user.lastDonation}</p>
          <p className="text-gray-700">Следующая возможная: {user.nextAvailableDate}</p>
        </div>

        {/* Медицинский статус */}
        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">Медицинский статус</h3>
          <p className={`font-semibold ${user.medicallyAccepted ? "text-green-600" : "text-red-500"}`}>
            {user.medicallyAccepted ? "Допущен" : "Не допущен"}
          </p>

          {/* История медотводов */}
          <div className="mt-4">
            <h4 className="text-md font-semibold mb-2">История медотводов</h4>
            {medotvods.length === 0 ? (
              <p className="text-gray-500 text-sm">Нет данных о медотводах</p>
            ) : (
              <ul className="space-y-3">
                {medotvods.map((entry, index) => (
                  <li
                    key={index}
                    className="border border-gray-200 rounded-lg p-3 bg-gray-50"
                  >
                    <p className="text-sm font-medium">
                      {entry.startDate} — {entry.endDate || "не указано"}
                    </p>
                    <p className="text-sm text-gray-600 italic">
                      {entry.comment || "Без комментария"}
                    </p>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Настройки */}
        <div
          onClick={() => { window.location.href = '/#/settings'; }}
          className="flex items-center gap-3 bg-white rounded-xl p-5 shadow-md cursor-pointer"
        >
          <FiSettings size={20} />
          <p>Настройки</p>
        </div>
      </div>

      <BottomNavBar />
    </>
  );
};


export default ProfilePage;
