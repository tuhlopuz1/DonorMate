import { useState } from "react";
import Swal from "sweetalert2";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiUserPlus } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest"; // путь подкорректируй под свой проект

const AddUserPage = () => {
  const [role, setRole] = useState("Студент МИФИ");

  const showGroupField = role === "Студент МИФИ";

  const handleExcelUpload = async () => {
    const { value: file } = await Swal.fire({
      title: "Добавить пользователей из Excel",
      html: `<input type="file" id="excelInput" accept=".xlsx,.xls" class="swal2-file" />`,
      showCancelButton: true,
      confirmButtonText: "Добавить",
      cancelButtonText: "Отмена",
      preConfirm: () => {
        const input = document.getElementById("excelInput") as HTMLInputElement;
        if (!input?.files || input.files.length === 0) {
          Swal.showValidationMessage("Пожалуйста, выберите файл");
          return false;
        }
        return input.files[0];
      },
    });

    if (file) {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await apiRequest({
          url: "https://api.donor.vickz.ru/api/load-users-xlsx",
          method: "POST",
          body: formData,
          auth: true,
          retry: true,
          headers: {}, // Не указываем Content-Type — браузер сам добавит boundary
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || "Ошибка при загрузке файла");
        }

        Swal.fire("Успешно!", "Файл успешно загружен", "success");
      } catch (error) {
        console.error("Ошибка загрузки файла:", error);
        Swal.fire("Ошибка", "Не удалось загрузить файл", "error");
      }
    }
  };

  return (
    <div className="p-6 pb-20 pt-12 space-y-6">
      <AdminPageTopBar title="Добавление пользователя" icon={<FiUserPlus size={20} />} />

      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold mb-4">Добавить пользователя</h1>
        <button
          onClick={handleExcelUpload}
          className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
        >
          <FiUserPlus />
          Добавить из Excel
        </button>
      </div>

      <form className="space-y-4 bg-white p-6 rounded-2xl shadow-md">
        <div>
          <label className="block text-sm font-medium mb-1">ФИО</label>
          <input
            required
            type="text"
            placeholder="Иванов Иван Иванович"
            className="w-full border rounded-md px-3 py-2 text-base"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Роль</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full border rounded-md px-3 py-2 text-base"
          >
            <option>Студент МИФИ</option>
            <option>Сотрудник МИФИ</option>
            <option>Внешний донор</option>
          </select>
        </div>

        {showGroupField && (
          <div>
            <label className="block text-sm font-medium mb-1">Учебная группа</label>
            <input
              type="text"
              placeholder="Группа"
              className="w-full border rounded-md px-3 py-2 text-base"
            />
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Кол-во донаций (Гаврилова)
            </label>
            <input type="number" min="0" className="w-full border rounded-md px-3 py-2 text-base" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Кол-во донаций (ФМБА)
            </label>
            <input type="number" min="0" className="w-full border rounded-md px-3 py-2 text-base" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Сумма донаций (мл)</label>
            <input type="number" min="0" className="w-full border rounded-md px-3 py-2 text-base" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Последняя донация (Гаврилова)</label>
            <input type="date" className="w-full border rounded-md px-3 py-2 text-base" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Последняя донация (ФМБА)</label>
            <input type="date" className="w-full border rounded-md px-3 py-2 text-base" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Контакт (соцсети)</label>
            <input
              type="text"
              placeholder="@username или ссылка"
              className="w-full border rounded-md px-3 py-2 text-base"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Телефон</label>
            <input
              type="tel"
              placeholder="+7 999 123-45-67"
              className="w-full border rounded-md px-3 py-2 text-base"
            />
          </div>
        </div>

        <div className="pt-4">
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition font-semibold"
          >
            Сохранить пользователя
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddUserPage;
