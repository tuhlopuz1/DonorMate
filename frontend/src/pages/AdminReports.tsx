import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { CalendarDays, Users, } from "lucide-react";
import { FiFileText, FiDownload } from "react-icons/fi";
import TopDonorCard from "../components/layouts/TopDonor";


const AdminReportsPage = () => {
  return (
    <div className="p-4 pb-20 pt-12 space-y-6">

     <AdminPageTopBar title="Отчёты" icon={<FiFileText size={20}/>} />

      <div className="flex mt-6 mx-4 gap-3 items-center justify-between bg-red-500 shadow rounded-2xl p-5">
          <p className="text-lg font-bold text-white">Подробный отчёт</p>
          <FiDownload color="white" size={23}/>
      </div>


      {/* Карточки статистики */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-2 gap-4">
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Всего пользователей</h3>
          <div className="text-2xl font-bold text-blue-600">3</div>

        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Предстоящие мероприятия</h3>
          <div className="text-2xl font-bold text-green-600">2</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Завершённые мероприятия</h3>
          <div className="text-2xl font-bold text-purple-600">1</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Всего совершено донаций</h3>
          <div className="text-2xl font-bold text-orange-600">37</div>
        </div>
      </div>

        <TopDonorCard  />

      {/* Последняя активность */}
      <div className="bg-white shadow rounded-2xl p-4">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <CalendarDays className="w-5 h-5 text-gray-500" />
          Последняя активность
        </h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b pb-2">
            <div>
              <p className="font-medium">Донорская акция "Капля жизни"</p>
              <p className="text-sm text-gray-500">15.12.2024</p>
            </div>
            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">
              Открыто
            </span>
          </div>
          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium">Плановая донация студентов</p>
              <p className="text-sm text-gray-500">22.12.2024</p>
            </div>
            <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-semibold">
              Открыто
            </span>
          </div>
        </div>
      </div>

      {/* Распределение ролей */}
      <div className="bg-white shadow rounded-2xl p-4">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Users className="w-5 h-5 text-gray-500" />
          Распределение ролей
        </h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span>Пользователи</span>
            <span className="bg-blue-200 px-3 text-blue-800 rounded-full text-center text-sm font-medium">
              266
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span>Доноры</span>
            <span className="bg-gray-200 px-3 text-gray-800 rounded-full text-center text-sm font-medium">
              105
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span>Организаторы</span>
            <span className="bg-red-200 px-3 text-red-800 rounded-full text-center text-sm font-medium">
              12
            </span>
          </div>
        </div>
      </div>
      <AdminBottomNavBar />
    </div>
  );
};

export default AdminReportsPage;
