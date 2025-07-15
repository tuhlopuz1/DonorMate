// pages/EventPage.tsx

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import EventCard from "../components/layouts/EventCard";
import MyEventCard from "../components/layouts/MyEventCard";
import { QrCode } from "lucide-react";


type EventData = {
  id: string;
  title: string;
  date: string;
  timeRange: string;
  location: string;
  description: string;
  totalSpots: number;
  spotsLeft: number;
  isRegistered: boolean;
};

const mockFetchEventById = async (id: string): Promise<EventData> => {
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    id,
    title: "Мастер-класс по фотографии",
    date: '2025-07-15',
    timeRange: "15:00 – 17:00",
    location: "ул. Пушкина, д. 10, Москва",
    description:
      "Приглашаем вас на мастер-класс, где вы узнаете основы композиции, работы со светом и постобработки.",
    totalSpots: 20,
    spotsLeft: 5,
    isRegistered: true,
  };
};

const EventPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<EventData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      mockFetchEventById(id).then((data) => {
        setEvent(data);
        setLoading(false);
      });
    }
  }, [id]);



  const handleCancel = () => {
    if (!event) return;
    setEvent({ ...event, isRegistered: false });
  };

  const isToday = (eventDate: string) => {
    const today = new Date();
    const eventD = new Date(eventDate);
    return (
      today.getFullYear() === eventD.getFullYear() &&
      today.getMonth() === eventD.getMonth() &&
      today.getDate() === eventD.getDate()
    );
  };

  if (loading || !event) {
    return <div className="p-6 text-gray-600">Загрузка мероприятия...</div>;
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Страница мероприятия</h1>

      {event.isRegistered ? (
        <MyEventCard
          title={event.title}
          date={event.date}
          timeRange={event.timeRange}
          location={event.location}
          description={event.description}
          onCancel={handleCancel}
        />
      ) : (
        <EventCard
          title={event.title}
          date={event.date}
          timeRange={event.timeRange}
          location={event.location}
          spotsLeft={event.spotsLeft}
          totalSpots={event.totalSpots}
          description={event.description}
          isRegistered={false}
        />
      )}

      {(isToday(event.date) && event.isRegistered) ? (
        <div className="flex justify-between items-center mt-6 bg-blue-600 text-white px-4 py-2 rounded-xl text-sm">

            <p>Получить qr код</p><QrCode />

        </div>
      ) : (<div></div>)
    
    }
    </div>
  );
};

export default EventPage;
