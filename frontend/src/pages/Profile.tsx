import { useEffect, useState } from "react";
import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiUser } from "react-icons/fi";
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
  phone: number;
  fsp: string;
}

const ProfilePage = () => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [medotvods, setMedotvods] = useState<Medotvod[]>([]);
  const [loadingUser, setLoadingUser] = useState(true);
  const [loadingMedotvods, setLoadingMedotvods] = useState(true);

  console.log(medotvods, loadingMedotvods);

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
              <h2 className="text-2xl font-bold mb-2">ПРОФИЛЬ</h2>
              <p className="text-sm text-white/80">ФИО: {user.fsp}</p>
              <p className="text-sm text-white/80">Телефон: {user.phone}</p>
            </>
          ) : (
            <p className="text-white/80">Не удалось загрузить профиль</p>
          )}
        </div>

        {/* Удаление данных */}
        <button onClick={() => {window.location.href = '/#/about'}} className="w-full bg-white text-blue-600 font-semibold py-3 rounded-2xl border border-blue-400 hover:border-blue-500 hover:bg-blue-50 shadow-sm hover:shadow-md transition-all duration-300 animate-fade-in-slow">
            Узнать больше о проекте
        </button>
      </div>

      <BottomNavBar />
    </>
  );
};

export default ProfilePage;
