// pages/EventPage.tsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import PageTopBar from "../components/layouts/PageTopBar";
import { QrCode } from "lucide-react";
import { MdEvent } from "react-icons/md";
import apiRequest from "../components/utils/apiRequest";
import EventCard from "../components/layouts/EventCard"; // путь подстрой под твою структуру

type EventData = {
  id: string;
  name: string;
  description: string;
  place: string;
  registred: number;
  start_date: string;
  end_date: string;
  created_at: string;
  is_registred: boolean;
};

const EventPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<EventData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvent = async () => {
      if (!id) return;
      try {
        const response = await apiRequest({
          url: `https://api.donor.vickz.ru/api/get-event-by-id/${id}`,
          auth: true,
        });

        if (!response.ok) {
          throw new Error("Ошибка загрузки данных о мероприятии");
        }

        const data: EventData = await response.json();
        setEvent(data);
      } catch (error) {
        console.error("Ошибка при загрузке мероприятия:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [id]);

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
      <PageTopBar title="Страница мероприятия" icon={<MdEvent size={20} />} />

      {/* Карточка мероприятия */}
      <div className="mt-6">
        <EventCard event={event} />
      </div>

      {/* QR-код если сегодня и пользователь зарегистрирован */}
      {isToday(event.start_date) && event.is_registred && (
        <div className="flex justify-between items-center mt-6 bg-blue-600 text-white px-4 py-2 rounded-xl text-sm">
          <p>Получить QR-код</p>
          <QrCode />
        </div>
      )}
    </div>
  );
};

export default EventPage;
