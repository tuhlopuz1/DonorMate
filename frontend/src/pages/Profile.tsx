import { useEffect, useState } from "react";
import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiUser, FiSettings } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest";

interface Medotvod {
  medic_phone_num: string;
  user_id: number;
  start_date: string;
  end_date: string;
  comment: string;
  url: string;
  id: string;
}

interface UserProfile {
  user_id: number;
  username: string;
  tg_name: string;
  role: string;
  created_at: string;
  fullname: string;
  surname: string;
  patronymic: string;
  birth_date: string;
  gender: "MALE" | "FEMALE";
  university: string;
  group: string;
  weight: number;
  chronic_disease: boolean;
  medical_exemption: boolean;
  donor_earlier: "YES" | "NO";
}

const ProfilePage = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [medotvods, setMedotvods] = useState<Medotvod[]>([]);
  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingMedotvods, setLoadingMedotvods] = useState(true);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const res = await apiRequest({
          url: "https://api.donor.vickz.ru/api/profile",
          method: "GET",
          auth: true,
        });

        if (!res.ok) throw new Error("Ошибка при получении профиля");
        const data: UserProfile = await res.json();
        setUser(data);
      } catch (error) {
        console.error("Ошибка загрузки профиля:", error);
      } finally {
        setLoadingUser(false);
      }
    };

    const fetchExemptions = async () => {
      try {
        const res = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-medical-exemptions",
          method: "GET",
          auth: true,
        });

        if (!res.ok) throw new Error("Ошибка при получении медотводов");
        const data: Medotvod[] = await res.json();
        setMedotvods(data);
      } catch (error) {
        console.error("Ошибка загрузки медотводов:", error);
      } finally {
        setLoadingMedotvods(false);
      }
    };

    fetchUserProfile();
    fetchExemptions();
  }, []);

  return (
    <>
      <PageTopBar title="Профиль" icon={<FiUser size={20} />} />

      <div className="p-6 pt-20 pb-28 flex flex-col gap-6">
        {/* Карточка пользователя */}
        <div className="bg-blue-600 text-white rounded-xl p-6 shadow-md">
          {loadingUser ? (
            <p className="text-white/80">Загрузка профиля...</p>
          ) : user ? (
            <>
              <h2 className="text-2xl font-bold mb-2">{user.fullname}</h2>
              <p className="text-sm text-white/80">Университет: {user.university}</p>
              <p className="text-sm text-white/80">Группа: {user.group}</p>
              <p className="text-sm text-white/80">Дата рождения: {user.birth_date}</p>
              <p className="text-sm text-white/80">
                Пол: {user.gender === "FEMALE" ? "Женский" : "Мужской"}
              </p>
              <p className="text-sm text-white/80">Вес: {user.weight} кг</p>
            </>
          ) : (
            <p className="text-white/80">Не удалось загрузить профиль</p>
          )}
        </div>

        {/* История донаций (заглушка пока что) */}
        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">История донаций</h3>
          {loadingUser ? (
            <p className="text-gray-500 text-sm">Загрузка...</p>
          ) : user ? (
            <>
              <p className="text-gray-700">
                Был донором ранее: <b>{user.donor_earlier === "YES" ? "Да" : "Нет"}</b>
              </p>
              <p className="text-gray-700">
                Хронические заболевания:{" "}
                <b>{user.chronic_disease ? "Есть" : "Нет"}</b>
              </p>
            </>
          ) : (
            <p className="text-gray-500 text-sm">Нет данных о донациях</p>
          )}
        </div>

        {/* Медицинский статус */}
        <div className="bg-white rounded-xl p-5 shadow-md">
          <h3 className="text-xl font-bold mb-3">Медицинский статус</h3>
          {loadingUser ? (
            <p className="text-gray-500 text-sm">Загрузка...</p>
          ) : user ? (
            <p
              className={`font-semibold ${
                user.medical_exemption ? "text-red-500" : "text-green-600"
              }`}
            >
              {user.medical_exemption ? "Не допущен (есть медотвод)" : "Допущен"}
            </p>
          ) : (
            <p className="text-gray-500 text-sm">Нет данных</p>
          )}

          {/* История медотводов */}
          <div className="mt-4">
            <h4 className="text-md font-semibold mb-2">История медотводов</h4>
            {loadingMedotvods ? (
              <p className="text-gray-500 text-sm">Загрузка...</p>
            ) : medotvods.length === 0 ? (
              <p className="text-gray-500 text-sm">Нет данных о медотводах</p>
            ) : (
              <ul className="space-y-3">
                {medotvods.map((entry) => (
                  <li
                    key={entry.id}
                    className="border border-gray-200 rounded-lg p-3 bg-gray-50"
                  >
                    <p className="text-sm font-medium">
                      {entry.start_date} — {entry.end_date || "не указано"}
                    </p>
                    <p className="text-sm text-gray-600 italic">
                      {entry.comment || "Без комментария"}
                    </p>
                    {entry.url && (
                      <a
                        href={entry.url}
                        download
                        className="text-blue-600 text-sm underline mt-1 inline-block"
                      >
                        Скачать справку
                      </a>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Настройки */}
        <div
          onClick={() => {
            window.location.href = "/#/settings";
          }}
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
