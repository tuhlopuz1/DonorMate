// AddMedotvodPage.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export type MedotvodData = {
  file: File | null;
  comment: string;
  startDate: string;
  endDate: string;
  doctorContact: string;
};

export function AddMedotvod() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [comment, setComment] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [doctorContact, setDoctorContact] = useState("");
  const [errors, setErrors] = useState({
    file: false,
    startDate: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Валидация
    const newErrors = {
      file: !file,
      startDate: !startDate,
    };
    
    setErrors(newErrors);
    
    if (newErrors.file || newErrors.startDate) {
      return;
    }
    
    // Здесь должна быть логика отправки данных
    const medotvodData: MedotvodData = {
      file,
      comment,
      startDate,
      endDate,
      doctorContact,
    };
    
    // Вызов API или обработка данных
    console.log("Отправка данных:", medotvodData);
    
    // После успешной отправки можно перенаправить пользователя
    navigate("/medotvody"); // или другой маршрут
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setErrors({...errors, file: false});
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Заголовок карточки с синим фоном */}
          <div className="bg-blue-600 py-4 px-6">
            <h1 className="text-2xl font-bold text-white">Добавить медицинский отвод</h1>
          </div>
          
          {/* Тело формы */}
          <form onSubmit={handleSubmit} className="space-y-6 p-6">
            <div className="space-y-5">
              {/* Поле для загрузки файла */}
              <div className="flex flex-col">
                <label className="font-medium mb-1 text-gray-700">
                  Загрузите документ (PDF, JPG, PNG) *
                </label>
                <input
                  type="file"
                  accept=".pdf,image/jpeg,image/png"
                  onChange={handleFileChange}
                  className={`p-2 border rounded-lg ${
                    errors.file ? "border-red-500" : "border-gray-300"
                  } focus:ring-2 focus:ring-blue-400 focus:border-blue-400`}
                />
                {errors.file && (
                  <p className="text-red-500 text-sm mt-1">
                    Пожалуйста, загрузите документ
                  </p>
                )}
              </div>

              {/* Дата начала */}
              <div className="flex flex-col">
                <label className="font-medium mb-1 text-gray-700">
                  Дата начала медотвода *
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => {
                    setStartDate(e.target.value);
                    setErrors({...errors, startDate: false});
                  }}
                  className={`p-2 border rounded-lg ${
                    errors.startDate ? "border-red-500" : "border-gray-300"
                  } focus:ring-2 focus:ring-blue-400 focus:border-blue-400`}
                />
                {errors.startDate && (
                  <p className="text-red-500 text-sm mt-1">
                    Укажите дату начала медотвода
                  </p>
                )}
              </div>

              {/* Дата окончания */}
              <div className="flex flex-col">
                <label className="font-medium mb-1 text-gray-700">
                  Дата окончания медотвода (если известна)
                </label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400"
                />
              </div>

              {/* Контактные данные */}
              <div className="flex flex-col">
                <label className="font-medium mb-1 text-gray-700">
                  Контактные данные врача или учреждения
                </label>
                <input
                  type="text"
                  value={doctorContact}
                  onChange={(e) => setDoctorContact(e.target.value)}
                  placeholder="Телефон или email (необязательно)"
                  className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:border-blue-400"
                />
              </div>

              {/* Комментарий */}
              <div className="flex flex-col">
                <label className="font-medium mb-1 text-gray-700">
                  Комментарий (необязательно)
                </label>
                <textarea
                  rows={3}
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Опишите причины или дополнительные детали"
                  className="p-2 border border-gray-300 rounded-lg resize-y focus:ring-2 focus:ring-blue-400 focus:border-blue-400"
                />
              </div>
            </div>

            {/* Кнопки */}
            <div className="flex justify-end space-x-3 pt-2">
              <button
                type="button"
                onClick={() => navigate(-1)}
                className="px-5 py-2.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200 font-medium"
              >
                Отмена
              </button>
              <button
                onClick={() => {window.location.href = '/#/main'}}
                type="submit"
                className="px-5 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200 font-medium shadow-sm"
              >
                Отправить
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AddMedotvod