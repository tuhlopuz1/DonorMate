import React from "react";
import { FiMapPin, FiCalendar } from "react-icons/fi";


type EventCardProps = {
  title: string;
  date: string; // например "2025-07-20"
  timeRange: string; // например "13:00–15:00"
  location: string;
  spotsLeft: number;
  totalSpots: number;
  description: string;
};

const EventCard: React.FC<EventCardProps> = ({
  title,
  date,
  timeRange,
  location,
  spotsLeft,
  totalSpots,
  description,
}) => {
  const formattedDate = new Date(date).toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });

  const isFull = spotsLeft <= 0;

  return (
    <div className="bg-white shadow-md rounded-2xl p-6 w-full max-w-md border border-gray-100">
      <div className="mb-2">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">{title}</h2>
        <div className="flex items-center text-sm text-gray-700 mb-2 gap-1">
            <FiCalendar size={15}/>
            <span className="font-medium text-base"> 
            {formattedDate}, {timeRange}
            </span>
        </div>
      </div>

      <div className="flex items-start text-sm text-gray-700 mb-2 gap-1">
        <FiMapPin size={15} className="mt-1"/> <span className="font-medium text-base">{location}</span>
      </div>

      <div className="text-sm text-gray-600 mb-4">{description}</div>

      <div className="flex flex-col gap-3 justify-between">
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

        <button
          className="text-white bg-blue-600 hover:bg-blue-700 font-medium px-4 py-2 rounded-xl text-sm disabled:opacity-50"
          disabled={isFull}
        >
          Записаться
        </button>
      </div>
    </div>
  );
};

export default EventCard;
