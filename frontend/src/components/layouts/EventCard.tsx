import React from "react";
import withReactContent from "sweetalert2-react-content";
import { FiMapPin, FiCalendar } from "react-icons/fi";
import Swal from "sweetalert2";
import apiRequest from "../utils/apiRequest";

const MySwal = withReactContent(Swal);

type EventData = {
  id: string;
  name: string;
  description: string;
  registred: number;
  start_date: string;
  end_date: string;
  created_at: string;
  is_registred: boolean;
  place: string;
};

type EventCardProps = {
  event: EventData;
  location?: string;
  totalSpots?: number;
};

const EventCard: React.FC<EventCardProps> = ({
  event,
  location = "Локация не указана",
  totalSpots = 20,
}) => {
  const {
    id,
    name,
    description,
    registred,
    start_date,
    end_date,
    is_registred,
    place,
  } = event;

  console.log(location)
  const startDate = new Date(start_date);
  const endDate = new Date(end_date);
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const formattedDate = startDate.toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  const formattedTimeRange = `${startDate.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  })} — ${endDate.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  })}`;

  const spotsLeft = totalSpots - registred;
  const isFull = spotsLeft <= 0;
  const isPastEvent = startDate < today;

  const handleRegisterClick = () => {
    if (isPastEvent) return;

    MySwal.fire({
      title: name,
      html: (
        <div className="text-left text-gray-800">
          <div className="mb-3">
            <div className="flex items-start text-sm mb-2 gap-1">
              <FiCalendar size={15} className="mt-1" />
              <span className="font-medium text-base">
                {formattedDate}, {formattedTimeRange}
              </span>
            </div>
            <div className="flex items-start text-sm gap-1">
              <FiMapPin size={15} className="mt-1" />
              <span className="font-medium text-base">{place}</span>
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
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const response = await apiRequest({
            url: `https://api.donor.vickz.ru/api/register-on-event/${id}`,
            method: "POST",
            auth: true,
          });

          if (!response.ok) {
            throw new Error("Ошибка при записи на мероприятие");
          }

          await MySwal.fire({
            icon: "success",
            title: "Вы успешно записались!",
            showConfirmButton: false,
            timer: 2000,
          });

          window.location.reload();
        } catch (error) {
          console.error(error);
          MySwal.fire({
            icon: "error",
            title: "Не удалось записаться",
            text: "Попробуйте еще раз позже.",
          });
        }
      }
    });
  };

  const handleUnregisterClick = () => {
    MySwal.fire({
      title: "Вы уверены, что хотите отменить запись?",
      text: "Вы больше не сможете участвовать в этом мероприятии.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Отменить запись",
      cancelButtonText: "Отмена",
      customClass: {
        popup: "rounded-2xl p-6 border border-gray-100 shadow-md",
        confirmButton:
          "bg-red-600 text-white px-4 py-2 rounded-xl text-sm hover:bg-red-700",
        cancelButton:
          "bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm ml-2",
      },
      buttonsStyling: false,
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const response = await apiRequest({
            url: `https://api.donor.vickz.ru/api/register-on-event/${id}`,
            method: "DELETE",
            auth: true,
          });

          if (!response.ok) {
            throw new Error("Ошибка при отмене записи");
          }

          await MySwal.fire({
            icon: "success",
            title: "Вы успешно отменили запись.",
            showConfirmButton: false,
            timer: 2000,
          });

          window.location.reload();
        } catch (error) {
          console.error(error);
          MySwal.fire({
            icon: "error",
            title: "Не удалось отменить запись",
            text: "Попробуйте еще раз позже.",
          });
        }
      }
    });
  };

  const handleDetailsClick = () => {
    window.location.href = `/#/event/${id}`;
  };

  return (
    <div
      className={`bg-white rounded-2xl p-6 w-full max-w-md border shadow ${
        isPastEvent ? "border-gray-200 bg-gray-50 opacity-70" : "border-gray-100"
      }`}
    >
      <div className="mb-2">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">{name}</h2>
        <div className="flex items-start text-sm text-gray-700 mb-2 gap-1">
          <FiCalendar size={15} className="mt-1" />
          <span className="font-medium text-base">
            {formattedDate}, {formattedTimeRange}
          </span>
        </div>
      </div>

      <div className="flex items-start text-sm text-gray-700 mb-2 gap-1">
        <FiMapPin size={15} className="mt-1" />
        <span className="font-medium text-base">{place}</span>
      </div>

      <div className="text-sm text-gray-600 mb-4">{description}</div>

      <div className="flex flex-col gap-3 justify-between">
        <button
          className="bg-gray-100 text-gray-800 px-4 py-2 rounded-xl text-sm hover:bg-gray-200 transition"
          onClick={handleDetailsClick}
        >
          Подробнее
        </button>

        {!is_registred && !isPastEvent && (
          <button
            className={`font-medium px-4 py-2 rounded-xl text-sm transition ${
              isFull
                ? "bg-blue-400 text-white cursor-not-allowed"
                : "bg-blue-600 text-white hover:bg-blue-700"
            }`}
            disabled={isFull}
            onClick={handleRegisterClick}
          >
            {isFull ? "Нет мест" : "Записаться"}
          </button>
        )}

        {is_registred && !isPastEvent && (
          <button
            className="font-medium px-4 py-2 rounded-xl text-sm mt-2 bg-red-600 text-white hover:bg-red-700"
            onClick={handleUnregisterClick}
          >
            Отменить запись
          </button>
        )}
      </div>
    </div>
  );
};

export default EventCard;
