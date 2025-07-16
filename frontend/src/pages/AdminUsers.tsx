import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminMainTopBar from "../components/layouts/AdminMainTopBar";
import { FiDownload } from "react-icons/fi";

const AdminUsersPage = () => {
  return (
    <div className="p-4 pb-20 pt-12 space-y-6">
     <AdminMainTopBar />
        <div className="flex gap-3 items-center justify-between bg-blue-500 shadow rounded-2xl p-5">
            <p className="text-lg font-bold text-white"> Экспорт данных в CSV</p>
            <FiDownload color="white" size={23}/>
        </div>
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

    <div className="bg-white shadow rounded-2xl p-4">
        <p className="text-lg font-sans font-bold mb-5  ">Поиск</p>
        <input className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm"
            placeholder="Поиск по имени, tg username"
        />

    </div>



      <AdminBottomNavBar />
    </div>
  );
};

export default AdminUsersPage;
