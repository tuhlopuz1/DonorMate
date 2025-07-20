// useMedotvodModal.ts
import { useState } from "react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

export type MedotvodData = {
  file: File | null;
  comment: string;
  startDate: string;
  endDate: string;
  doctorContact: string;
};

export function useMedotvodModal(onSubmit: (data: MedotvodData) => void) {
  const [file, setFile] = useState<File | null>(null);
  const [comment, setComment] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [doctorContact, setDoctorContact] = useState("");
  const openModal = () => {
    MySwal.fire({
      title: "Прикрепить медицинский отвод",
      html: (
        <div className="w-[90vw] max-w-full sm:max-w-[36rem] flex flex-col text-left text-gray-800 space-y-4">
          <label className="flex flex-col font-medium">
            Загрузите документ (PDF, JPG, PNG) *
            <input
              type="file"
              accept=".pdf,image/jpeg,image/png"
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  setFile(e.target.files[0]);
                }
              }}
              className="mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <label className="flex flex-col font-medium">
            Дата начала медотвода *
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <label className="flex flex-col font-medium">
            Дата окончания медотвода (если известна)
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <label className="flex flex-col font-medium">
            Контактные данные врача или учреждения
            <input
              type="text"
              value={doctorContact}
              onChange={(e) => setDoctorContact(e.target.value)}
              placeholder="Телефон или email (необязательно)"
              className="mt-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <label className="flex flex-col font-medium">
            Комментарий (необязательно)
            <textarea
              rows={3}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Опишите причины или дополнительные детали"
              className="mt-1 p-2 border border-gray-300 rounded-lg resize-y focus:ring-2 focus:ring-blue-400"
            />
          </label>
        </div>
      ),
      focusConfirm: false,
      showCancelButton: true,
      confirmButtonText: "Отправить",
      cancelButtonText: "Отмена",
      customClass: {
        popup: "p-0 pb-3 bg-white rounded-xl shadow-md w-auto max-w-none",
        confirmButton:
          "bg-blue-600 text-white px-5 py-2 rounded-lg text-sm hover:bg-blue-700",
        cancelButton:
          "bg-gray-200 text-gray-700 px-5 py-2 rounded-lg text-sm ml-2 hover:bg-gray-300",
      },
      preConfirm: () => {
        if (!file) {
          Swal.showValidationMessage("Пожалуйста, загрузите документ.");
          return false;
        }
        if (!startDate) {
          Swal.showValidationMessage("Укажите дату начала медотвода.");
          return false;
        }
        return true;
      },
    }).then((result) => {
      if (result.isConfirmed) {
        onSubmit({ file, comment, startDate, endDate, doctorContact });

        // Очистка
        setFile(null);
        setComment("");
        setStartDate("");
        setEndDate("");
        setDoctorContact("");
      }
    });
  };

  return openModal;
}
