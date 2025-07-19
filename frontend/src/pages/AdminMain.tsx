import { useEffect, useState, useRef } from "react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminMainTopBar from "../components/layouts/AdminMainTopBar";
import { Users, FilePlus } from "lucide-react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import { FiDownload, FiSend } from "react-icons/fi";
import TopDonors from "../components/layouts/TopDonor";
import apiRequest from "../components/utils/apiRequest";

const AdminMainPage = () => {
  const MySwal = withReactContent(Swal);
  const fileInputRef = useRef<HTMLInputElement>(null);
  console.log(fileInputRef)
  const [metrics, setMetrics] = useState({
    users_count: 0,
    donations_count: 0,
    new_events_count: 0,
    ended_events_count: 0,
  });

  const [roleMetrics, setRoleMetrics] = useState({
    users_count: 0,
    donors_count: 0,
    admins_count: 0,
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-metrics",
          auth: true,
        });

        if (!response.ok) throw new Error("Failed to fetch metrics");

        const data = await response.json();
        setMetrics(data);
      } catch (error) {
        console.error("Ошибка загрузки метрик:", error);
      }
    };

    const fetchRoleMetrics = async () => {
      try {
        const response = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-role-metrics",
          auth: true,
        });

        if (!response.ok) throw new Error("Failed to fetch role metrics");

        const data = await response.json();
        setRoleMetrics({
          users_count: data.users_count,
          donors_count: data.donors_count,
          admins_count: data.admins_count,
        });
      } catch (error) {
        console.error("Ошибка загрузки распределения ролей:", error);
      }
    };

    fetchMetrics();
    fetchRoleMetrics();
  }, []);

  const handleAddDonationsClick = () => {
    MySwal.fire({
      title: "Добавить донации из XLSX",
      html: `<input type="file" id="xlsxFile" accept=".xlsx" class="swal2-file" />`,
      showCancelButton: true,
      confirmButtonText: "Добавить",
      cancelButtonText: "Отмена",
      focusConfirm: false,
      preConfirm: () => {
        const file = (document.getElementById("xlsxFile") as HTMLInputElement)?.files?.[0];
        if (!file) {
          Swal.showValidationMessage("Пожалуйста, выберите файл");
          return null;
        }
        return file;
      },
    }).then(async (result) => {
      if (result.isConfirmed && result.value) {
        const file = result.value as File;
        const formData = new FormData();
        formData.append("file", file);

        try {
          const response = await apiRequest({
            url: "https://api.donor.vickz.ru/api/load-donations-xlsx",
            method: "POST",
            auth: true,
            retry: true,
            headers: {}, // важный момент: не указываем Content-Type, browser сам установит multipart
            body: formData as any, // костыль, потому что `body` в apiRequest принимает Record
          });

          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ошибка загрузки файла: ${errorText}`);
          }

          Swal.fire("Успешно", "Файл успешно загружен", "success");
        } catch (error: any) {
          console.error("Ошибка загрузки файла:", error);
          Swal.fire("Ошибка", error.message || "Не удалось загрузить файл", "error");
        }
      }
    });
  };

  return (
    <div className="p-4 pb-20 pt-12 space-y-6">
      <AdminMainTopBar />

      <div
        onClick={handleAddDonationsClick}
        className="flex mt-6 mx-4 gap-3 items-center justify-between bg-blue-500 shadow rounded-2xl p-5 cursor-pointer"
      >
        <p className="text-lg font-bold text-white">Добавить донации из XLSX</p>
        <FilePlus color="white" className="w-5 h-5" />
      </div>

      <div className="flex mt-6 mx-4 gap-3 items-center justify-between bg-red-500 shadow rounded-2xl p-5">
        <p className="text-lg font-bold text-white">Подробный отчёт</p>
        <FiDownload color="white" size={23} />
      </div>

      <div
        onClick={() => {
          window.location.href = "/#/admin/sending";
        }}
        className="flex mt-6 mx-4 gap-3 items-center justify-between bg-green-500 shadow rounded-2xl p-5 cursor-pointer"
      >
        <p className="text-lg font-bold text-white">Сделать рассылку</p>
        <FiSend color="white" size={23} />
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-2 gap-4">
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Всего пользователей</h3>
          <div className="text-2xl font-bold text-blue-600">{metrics.users_count}</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Предстоящие мероприятия</h3>
          <div className="text-2xl font-bold text-green-600">{metrics.new_events_count}</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Завершённые мероприятия</h3>
          <div className="text-2xl font-bold text-purple-600">{metrics.ended_events_count}</div>
        </div>
        <div className="bg-white shadow rounded-2xl p-4">
          <h3 className="text-sm text-gray-500">Всего совершено донаций</h3>
          <div className="text-2xl font-bold text-orange-600">{metrics.donations_count}</div>
        </div>
      </div>

      <TopDonors />

      <div className="bg-white shadow rounded-2xl p-4">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Users className="w-5 h-5 text-gray-500" />
          Распределение ролей
        </h3>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span>Пользователи</span>
            <span className="bg-blue-200 px-3 text-blue-800 rounded-full text-center text-sm font-medium">
              {roleMetrics.users_count}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span>Доноры</span>
            <span className="bg-gray-200 px-3 text-gray-800 rounded-full text-center text-sm font-medium">
              {roleMetrics.donors_count}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span>Организаторы</span>
            <span className="bg-red-200 px-3 text-red-800 rounded-full text-center text-sm font-medium">
              {roleMetrics.admins_count}
            </span>
          </div>
        </div>
      </div>

      <AdminBottomNavBar />
    </div>
  );
};

export default AdminMainPage;
