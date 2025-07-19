import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiUser } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest"; // путь подкорректируйте под ваш проект

type User = {
  id: string;
  fullName: string;
  role: string;
  group?: string;
  gavrilovaDonations: number;
  fmbaDonations: number;
  totalMl: number;
  lastGavrilovaDonation: string;
  lastFMBADonation: string;
  contact: string;
  phone: string;
};

const mapApiResponseToUser = (data: any): User => ({
  id: String(data.id),
  fullName: data.fsp,
  role: data.user_class,
  group: data.group,
  gavrilovaDonations: data.donations_gaur,
  fmbaDonations: data.donations_fmba,
  totalMl: data.donations,
  lastGavrilovaDonation: data.last_don_gaur ? data.last_don_gaur.split("T")[0] : "",
  lastFMBADonation: data.last_don_fmba ? data.last_don_fmba.split("T")[0] : "",
  contact: "", // в ответе нет, оставляем пустым
  phone: String(data.phone),
});

const UserProfilePage = () => {
  const { id } = useParams<{ id: string }>();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) {
      setError("ID пользователя не указан");
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    apiRequest({
      url: `/api/get-user/${id}`,
      auth: true,
      method: "GET",
    })
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(`Ошибка загрузки данных: ${res.statusText}`);
        }
        const data = await res.json();
        setUser(mapApiResponseToUser(data));
      })
      .catch((err) => {
        setError(err.message || "Не удалось загрузить данные пользователя");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <div className="p-6">Загрузка данных пользователя...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-600">Ошибка: {error}</div>;
  }

  if (!user) {
    return <div className="p-6">Пользователь не найден</div>;
  }

  return (
    <div className="p-6 pb-20 pt-12 space-y-6">
      <AdminPageTopBar title={`Профиль пользователя`} icon={<FiUser size={20} />} />

      <div className="bg-white p-6 rounded-2xl shadow-md space-y-4">
        <h1 className="text-2xl font-bold mb-4">Редактирование профиля</h1>

        <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
          <div>
            <label className="block text-sm font-medium mb-1">ФИО</label>
            <input
              type="text"
              defaultValue={user.fullName}
              className="w-full border rounded-md px-3 py-2 text-base"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Роль</label>
            <select
              defaultValue={user.role}
              className="w-full border rounded-md px-3 py-2 text-base"
            >
              <option>Студент МИФИ</option>
              <option>Сотрудник МИФИ</option>
              <option>Внешний донор</option>
            </select>
          </div>

          {user.role === "Студент МИФИ" && (
            <div>
              <label className="block text-sm font-medium mb-1">Учебная группа</label>
              <input
                type="text"
                defaultValue={user.group}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Кол-во донаций (Гаврилова)</label>
              <input
                type="number"
                defaultValue={user.gavrilovaDonations}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Кол-во донаций (ФМБА)</label>
              <input
                type="number"
                defaultValue={user.fmbaDonations}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Сумма донаций (мл)</label>
              <input
                type="number"
                defaultValue={user.totalMl}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Последняя донация (Гаврилова)</label>
              <input
                type="date"
                defaultValue={user.lastGavrilovaDonation}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Последняя донация (ФМБА)</label>
              <input
                type="date"
                defaultValue={user.lastFMBADonation}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Контакт (соцсети)</label>
              <input
                type="text"
                defaultValue={user.contact}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Телефон</label>
              <input
                type="tel"
                defaultValue={user.phone}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition font-semibold"
            >
              Сохранить изменения
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserProfilePage;
