import { useRef } from "react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminMainTopBar from "../components/layouts/AdminMainTopBar";
import { Users, FilePlus } from "lucide-react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import { FiDownload, FiSend } from "react-icons/fi";
import TopDonors from "../components/layouts/TopDonor";
const AdminMainPage = () => {
  const MySwal = withReactContent(Swal);
  const fileInputRef = useRef<HTMLInputElement>(null);
  console.log(fileInputRef)
  const handleAddDonationsClick = () => {
    MySwal.fire({
      title: "Добавить донации из XLSX",
      html: `
        <input type="file" id="xlsxFile" accept=".xlsx" class="swal2-file" />
      `,
      showCancelButton: true,
      confirmButtonText: "Добавить",
      cancelButtonText: "Отмена",
      focusConfirm: false,
      preConfirm: () => {
        const file = (document.getElementById("xlsxFile") as HTMLInputElement)
          ?.files?.[0];
        if (!file) {
          Swal.showValidationMessage("Пожалуйста, выберите файл");
        }
        return file;
      },
    }).then((result) => {
      if (result.isConfirmed && result.value) {
        const file = result.value as File;
        // Здесь можно обработать файл
        console.log("Загружен файл:", file.name);
      }
    });
  };

  return (
    <div className="p-4 pb-20 pt-12 space-y-6">
      <AdminMainTopBar />

      
      <div onClick={handleAddDonationsClick} className="flex mt-6 mx-4 gap-3 items-center justify-between bg-blue-500 shadow rounded-2xl p-5">
                <p className="text-lg font-bold text-white">Добавить донации из XLSX</p>
          <FilePlus color="white" className="w-5 h-5" />
      </div>
        <div className="flex mt-6 mx-4 gap-3 items-center justify-between bg-red-500 shadow rounded-2xl p-5">
            <p className="text-lg font-bold text-white">Подробный отчёт</p>
            <FiDownload color="white" size={23}/>
        </div>
        <div onClick={() => {window.location.href = '/#/admin/sending'}} className="flex mt-6 mx-4 gap-3 items-center justify-between bg-green-500 shadow rounded-2xl p-5">
            <p className="text-lg font-bold text-white">Сделать рассылку</p>
            <FiSend color="white" size={23}/>
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

      <TopDonors />

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

export default AdminMainPage;
