import React from "react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
import { FiMapPin, FiCalendar } from "react-icons/fi";

const MySwal = withReactContent(Swal);

type EventCardProps = {
  title: string;
  date: string;
  timeRange: string;
  location: string;
  spotsLeft: number;
  totalSpots: number;
  description: string;
  isRegistered: boolean;
};

const EventCard: React.FC<EventCardProps> = ({
  title,
  date,
  timeRange,
  location,
  spotsLeft,
  totalSpots,
  description,
  isRegistered,
}) => {
  const eventDate = new Date(date);
  const today = new Date();
  today.setHours(0, 0, 0, 0); // убрать время из сравнения
  const formattedDate = eventDate.toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  const isFull = spotsLeft <= 0;
  const isPastEvent = eventDate < today;

  const handleRegisterClick = () => {
    if (isPastEvent) return;

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
      confirmButtonText: "Записаться",
      cancelButtonText: "Отмена",
      customClass: {
        popup: "rounded-2xl p-6 border border-gray-100 shadow-md",
        confirmButton:
          "bg-blue-600 text-white px-4 py-2 rounded-xl text-sm hover:bg-blue-700",
        cancelButton:
          "bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm ml-2",
      },
      buttonsStyling: false,
    }).then((result) => {
      if (result.isConfirmed) {
        console.log("Пользователь записался на мероприятие:", title);
      }
    });
  };

  return (
    <div
      className={`bg-white rounded-2xl p-6 w-full max-w-md border shadow ${
        isPastEvent ? "border-gray-200 bg-gray-50 opacity-70" : "border-gray-100"
      }`}
    >
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

      <div className="flex flex-col gap-3 justify-between">
        {isPastEvent ? (
          <span className="text-sm font-medium px-3 py-1 rounded-full bg-gray-200 text-gray-700 w-auto">
            Мероприятие завершено
          </span>
        ) : (
          <span
            className={`text-sm font-medium px-3 py-1 rounded-full w-auto ${
              isFull
                ? "bg-red-100 text-red-700"
                : "bg-green-100 text-green-700"
            }`}
          >
            {isFull
              ? "Мест нет"
              : `Осталось мест: ${spotsLeft} / ${totalSpots}`}
          </span>
        )}

        <button
          className={`font-medium px-4 py-2 rounded-xl text-sm transition ${
            isPastEvent
              ? "bg-gray-300 text-gray-600 cursor-not-allowed"
              : isRegistered
              ? "bg-gray-300 text-gray-600 cursor-not-allowed"
              : isFull
              ? "bg-blue-400 text-white cursor-not-allowed"
              : "bg-blue-600 text-white hover:bg-blue-700"
          }`}
          disabled={isPastEvent || isRegistered || isFull}
          onClick={handleRegisterClick}
        >
          {isPastEvent
            ? "Мероприятие завершено"
            : isRegistered
            ? "Вы уже записаны"
            : "Записаться"}
        </button>
      </div>
    </div>
  );
};

export default EventCard;
