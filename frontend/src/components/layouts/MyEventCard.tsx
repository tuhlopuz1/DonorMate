import React from "react";
import { FiMapPin, FiCalendar } from "react-icons/fi";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

type MyEventCardProps = {
  title: string;
  date: string;
  timeRange: string;
  location: string;
  description: string;
  onCancel?: () => void; // колбэк при подтверждении отмены
};

const MyEventCard: React.FC<MyEventCardProps> = ({
  title,
  date,
  timeRange,
  location,
  description,
  onCancel,
}) => {
  const formattedDate = new Date(date).toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  const handleCancelClick = () => {
    MySwal.fire({
      title: title,
      html: (
        <div className="text-left text-gray-800">
          <div className="mb-3">
            <div className="flex items-start text-sm mb-2 gap-1">
              <FiCalendar size={15} className="mt-1" />
              <span className="font-medium text-base">
                {formattedDate}, {timeRange}
              </span>
            </div>
            <div className="flex items-start text-sm gap-1">
              <FiMapPin size={15} className="mt-1" />
              <span className="font-medium text-base">{location}</span>
            </div>
          </div>
          <p className="text-sm text-gray-700">{description}</p>
        </div>
      ),
      showCancelButton: true,
      confirmButtonText: "Отменить запись",
      cancelButtonText: "Назад",
      customClass: {
        popup: "rounded-2xl p-6 border border-gray-100 shadow-md",
        confirmButton:
          "bg-red-600 text-white px-4 py-2 rounded-xl text-sm hover:bg-red-700",
        cancelButton:
          "bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm ml-2",
      },
      buttonsStyling: false,
    }).then((result) => {
      if (result.isConfirmed && onCancel) {
        onCancel();
      }
    });
  };

  return (
    <div className="bg-white shadow-[0_0_10px_rgba(0,0,0,0.15)] rounded-2xl p-6 w-full max-w-md border border-gray-100">
      <div className="mb-2">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">{title}</h2>
        <div className="flex items-start text-sm text-gray-700 mb-2 gap-1">
          <FiCalendar size={15} className="mt-1" />
          <span className="font-medium text-base">
            {formattedDate}, {timeRange}
          </span>
        </div>
      </div>

      <div className="flex items-start text-sm text-gray-700 mb-2 gap-1">
        <FiMapPin size={15} className="mt-1" />
        <span className="font-medium text-base">{location}</span>
      </div>

      <div className="text-sm text-gray-600 mb-4">{description}</div>

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <span className="text-sm font-medium px-3 py-1 rounded-full bg-blue-100 text-blue-700 w-fit">
          Вы записаны
        </span>

        {onCancel && (
          <button
            className="text-sm font-medium text-red-600 bg-red-200 p-2 rounded-2xl"
            onClick={handleCancelClick}
          >
            Отменить участие
          </button>
        )}
      </div>
    </div>
  );
};

export default MyEventCard;
