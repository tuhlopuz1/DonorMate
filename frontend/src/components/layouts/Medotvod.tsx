import React, { useState } from 'react';

type MedotvodModalProps = {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: {
    file: File | null;
    comment: string;
    startDate: string;
    endDate: string;
    doctorContact: string;
  }) => void;
};

export default function MedotvodModal({ isOpen, onClose, onSubmit }: MedotvodModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [comment, setComment] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [doctorContact, setDoctorContact] = useState('');

  if (!isOpen) return null;

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file) {
      alert('Пожалуйста, загрузите документ с медицинским отводом.');
      return;
    }
    if (!startDate) {
      alert('Пожалуйста, укажите дату начала медотвода.');
      return;
    }
    // endDate может быть необязательной, если медотвод бессрочный
    onSubmit({ file, comment, startDate, endDate, doctorContact });
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 backdrop-blur-sm p-4"
      aria-modal="true"
      role="dialog"
      aria-labelledby="modal-title"
    >
      <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 flex flex-col">
        <h2 id="modal-title" className="text-2xl font-semibold text-blue-700 mb-4 text-center">
          Прикрепить медицинский отвод
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col space-y-5">
          <label className="flex flex-col text-gray-700 font-medium">
            Загрузите документ (PDF, JPG, PNG) *
            <input
              type="file"
              accept=".pdf,image/jpeg,image/png"
              onChange={handleFileChange}
              className="mt-2 p-2 border border-gray-300 rounded-lg cursor-pointer
                focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
          </label>

          <label className="flex flex-col text-gray-700 font-medium">
            Дата начала медотвода *
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="mt-2 p-2 border border-gray-300 rounded-lg
                focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
          </label>

          <label className="flex flex-col text-gray-700 font-medium">
            Дата окончания медотвода (если известна)
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="mt-2 p-2 border border-gray-300 rounded-lg
                focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <label className="flex flex-col text-gray-700 font-medium">
            Контактные данные врача или медицинского учреждения
            <input
              type="text"
              value={doctorContact}
              onChange={(e) => setDoctorContact(e.target.value)}
              placeholder="Телефон или email (необязательно)"
              className="mt-2 p-2 border border-gray-300 rounded-lg
                focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <label className="flex flex-col text-gray-700 font-medium">
            Комментарий (необязательно)
            <textarea
              rows={3}
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Опишите причины или дополнительные детали"
              className="mt-2 p-3 border border-gray-300 rounded-lg resize-y
                focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </label>

          <div className="flex justify-end space-x-4 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2 rounded-lg bg-gray-200 text-gray-700 hover:bg-gray-300 transition"
            >
              Отмена
            </button>
            <button
              type="submit"
              className="px-5 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
            >
              Отправить
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
