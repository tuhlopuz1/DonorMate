import { useState, useEffect } from "react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminMainTopBar from "../components/layouts/AdminMainTopBar";
import { FiDownload, FiUserPlus } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest"; // путь подкорректируй по проекту

interface User {
  id: number;
  phone: number;
  fsp: string;
  group: string;
  user_class: string;
  donations: number;
}

const AdminUsersPage = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await apiRequest({
        url: "https://api.donor.vickz.ru/api/find-user",
        method: "GET",
        params: { fsp: searchQuery },
        auth: true,
      });

      if (!response.ok) {
        throw new Error("Ошибка при получении данных");
      }

      const data: User[] = await response.json();
      setUsers(data);
    } catch (err: any) {
      setError(err.message || "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (searchQuery.trim() === "") {
      setUsers([]);
    }
  }, [searchQuery]);

  return (
    <div className="p-4 pb-20 pt-12 space-y-6">
      <AdminMainTopBar />

      {/* Верхняя панель */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 bg-red-500 shadow rounded-2xl p-5">
        <div className="flex items-center gap-3">
          <p className="text-lg font-bold text-white">Экспорт данных в XLSX</p>
          <FiDownload color="white" size={23} />
        </div>
      </div>

      <button
        onClick={() => {
          window.location.href = "/#/admin/add-user";
        }}
        className="flex items-center shadow w-full gap-2 bg-white text-red-600 font-medium px-4 py-2 rounded-xl hover:bg-red-100 transition"
      >
        <FiUserPlus size={18} />
        Добавить пользователя
      </button>

      {/* Карточки статистики */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-2 gap-4">
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Всего пользователей</h3>
          <div className="text-2xl font-bold text-blue-600">3</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Доноры</h3>
          <div className="text-2xl font-bold text-green-600">2</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Постоянные доноры</h3>
          <div className="text-2xl font-bold text-purple-600">1</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Организаторы</h3>
          <div className="text-2xl font-bold text-orange-600">37</div>
        </div>
      </div>

      {/* Поиск */}
      <div className="bg-white shadow rounded-2xl p-4">
        <p className="text-lg font-sans font-bold mb-5">Поиск</p>
        <div className="flex gap-3">
          <input
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm"
            placeholder="Поиск по имени, tg username"
          />
          <button
            onClick={handleSearch}
            className="bg-red-500 text-white px-4 py-2 rounded-xl hover:bg-red-600 transition text-sm font-semibold"
          >
            Найти
          </button>
        </div>
      </div>

      {/* Результаты поиска */}
      {loading && <p>Загрузка...</p>}
      {error && <p className="text-red-500">{error}</p>}
      {!loading && users.length > 0 && (
        <div className="bg-white shadow rounded-2xl p-4">
          <p className="text-lg font-bold mb-4">Результаты поиска</p>
          <table className="min-w-full table-auto text-left text-sm">
            <thead>
              <tr className="text-gray-600 border-b">
                <th className="py-2">ID</th>
                <th className="py-2">Телефон</th>
                <th className="py-2">FSP</th>
                <th className="py-2">Группа</th>
                <th className="py-2">Класс</th>
                <th className="py-2">Донорства</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr onClick={() => {window.location.href = '/#/admin/user/'+user.phone}} key={user.id} className="border-b hover:bg-gray-50">
                  <td className="py-2">{user.phone}</td>
                  <td className="py-2">{user.fsp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <AdminBottomNavBar />
    </div>
  );
};

export default AdminUsersPage;
