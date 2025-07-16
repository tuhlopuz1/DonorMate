import React from "react";

import { FiMapPin, FiCalendar } from "react-icons/fi";


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

      </div>
    </div>
  );
};

export default EventCard;
