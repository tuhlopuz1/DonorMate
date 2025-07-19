import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router-dom";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiUser } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest";

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
  contact: "", // отсутствует в API
  phone: String(data.phone),
});

const UserProfilePage = () => {
  const { id } = useParams<{ id: string }>();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitStatus, setSubmitStatus] = useState<string | null>(null);

  // Refs
  const fullNameRef = useRef<HTMLInputElement>(null);
  const roleRef = useRef<HTMLSelectElement>(null);
  const groupRef = useRef<HTMLInputElement>(null);
  const gaurDonRef = useRef<HTMLInputElement>(null);
  const fmbaDonRef = useRef<HTMLInputElement>(null);
  const lastGaurRef = useRef<HTMLInputElement>(null);
  const lastFmbaRef = useRef<HTMLInputElement>(null);
  const contactRef = useRef<HTMLInputElement>(null);
  const phoneRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!id) {
      setError("ID пользователя не указан");
      setLoading(false);
      return;
    }

    apiRequest({
      url: `https://api.donor.vickz.ru/api/get-user/${id}`,
      auth: true,
      method: "GET",
    })
      .then(async (res) => {
        if (!res.ok) throw new Error(`Ошибка загрузки данных: ${res.statusText}`);
        const data = await res.json();
        setUser(mapApiResponseToUser(data));
      })
      .catch((err) => setError(err.message || "Не удалось загрузить данные пользователя"))
      .finally(() => setLoading(false));
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    setSubmitStatus(null);

    const body = {
      phone: Number(phoneRef.current?.value || 0),
      fsp: fullNameRef.current?.value || "",
      group: groupRef.current?.value || "",
      user_class: roleRef.current?.value || "",
      social: contactRef.current?.value || "",
      donations_fmba: Number(fmbaDonRef.current?.value || 0),
      donations_gaur: Number(gaurDonRef.current?.value || 0),
      donations:
        Number(fmbaDonRef.current?.value || 0) + Number(gaurDonRef.current?.value || 0),
      last_don_gaur: new Date(lastGaurRef.current?.value || "").toISOString(),
      last_don_fmba: new Date(lastFmbaRef.current?.value || "").toISOString(),
    };

    try {
      const res = await apiRequest({
        url: `https://api.donor.vickz.ru/api/edit-user-profile/${body.phone}`,
        method: "PUT",
        body,
        auth: true,
      });

      if (!res.ok) {
        const msg = await res.text();
        throw new Error(msg);
      }

      setSubmitStatus("Изменения успешно сохранены");
    } catch (err: any) {
      setSubmitStatus(`Ошибка при сохранении: ${err.message}`);
    }
  };

  if (loading) return <div className="p-6">Загрузка данных пользователя...</div>;
  if (error) return <div className="p-6 text-red-600">Ошибка: {error}</div>;
  if (!user) return <div className="p-6">Пользователь не найден</div>;

  return (
    <div className="p-6 pb-20 pt-12 space-y-6">
      <AdminPageTopBar title="Профиль пользователя" icon={<FiUser size={20} />} />

      <div className="bg-white p-6 rounded-2xl shadow-md space-y-4">
        <h1 className="text-2xl font-bold mb-4">Редактирование профиля</h1>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-1">ФИО</label>
            <input
              ref={fullNameRef}
              type="text"
              defaultValue={user.fullName}
              className="w-full border rounded-md px-3 py-2 text-base"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Роль</label>
            <select
              ref={roleRef}
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
                ref={groupRef}
                type="text"
                defaultValue={user.group}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                Кол-во донаций (Гаврилова)
              </label>
              <input
                ref={gaurDonRef}
                type="number"
                defaultValue={user.gavrilovaDonations}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Кол-во донаций (ФМБА)
              </label>
              <input
                ref={fmbaDonRef}
                type="number"
                defaultValue={user.fmbaDonations}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Последняя донация (Гаврилова)
              </label>
              <input
                ref={lastGaurRef}
                type="date"
                defaultValue={user.lastGavrilovaDonation}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Последняя донация (ФМБА)
              </label>
              <input
                ref={lastFmbaRef}
                type="date"
                defaultValue={user.lastFMBADonation}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Контакт (соцсети)</label>
              <input
                ref={contactRef}
                type="text"
                defaultValue={user.contact}
                className="w-full border rounded-md px-3 py-2 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Телефон</label>
              <input
                ref={phoneRef}
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

          {submitStatus && (
            <div className="pt-2 text-sm text-center text-green-700">{submitStatus}</div>
          )}
        </form>
      </div>
    </div>
  );
};

export default UserProfilePage;
