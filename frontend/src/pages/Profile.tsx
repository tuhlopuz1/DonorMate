import { useEffect, useState } from "react";
import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiUser, FiTrash2 } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

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

  const handleDeleteAccount = async () => {
    const result = await MySwal.fire({
      title: "Вы уверены?",
      text: "Это действие удалит все ваши данные без возможности восстановления.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#e3342f",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Да, удалить",
      cancelButtonText: "Отмена",
    });

    if (result.isConfirmed) {
      try {
        const res = await apiRequest({
          url: "https://api.donor.vickz.ru/api/delete-user",
          method: "DELETE",
          auth: true,
        });

        if (!res.ok) throw new Error("Ошибка при удалении аккаунта");

        await MySwal.fire({
          icon: "success",
          title: "Удалено!",
          text: "Ваши данные были успешно удалены.",
        });

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/#/";
      } catch (error) {
        console.error("Ошибка удаления аккаунта:", error);
        await MySwal.fire({
          icon: "error",
          title: "Ошибка",
          text: "Не удалось удалить данные. Попробуйте позже.",
        });
      }
    }
  };

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
        <div className="bg-white rounded-xl p-5 shadow-md border border-red-200">
          <div className="flex items-center gap-3 mb-3">
            <FiTrash2 size={20} className="text-red-600" />
            <h3 className="text-xl font-bold text-red-600">Удаление данных</h3>
          </div>
          <button onClick={handleDeleteAccount} className="text-red-600">
            Удалить все мои данные
          </button>
        </div>
      </div>

      <BottomNavBar />
    </>
  );
};

export default ProfilePage;
