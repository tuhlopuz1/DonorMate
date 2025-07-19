import { useEffect, useState } from "react";
import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiClipboard } from "react-icons/fi";
import EventCard from "../components/layouts/EventCard";
import apiRequest from "../components/utils/apiRequest";

interface RegisteredEvent {
  id: string;
  name: string;
  description: string;
  registred: number;
  start_date: string;
  end_date: string;
  created_at: string;
  is_registred: boolean;
  place: string;
}

const AppointmentsPage = () => {
  const [events, setEvents] = useState<RegisteredEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRegistrations = async () => {
      try {
        const res = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-registrations",
          method: "GET",
          auth: true,
        });

        if (!res.ok) throw new Error("Ошибка при получении записей");

        const data: RegisteredEvent[] = await res.json();
        setEvents(data);
      } catch (error) {
        console.error("Ошибка загрузки записей:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRegistrations();
  }, []);

  return (
    <>
      <PageTopBar title="Мои записи" icon={<FiClipboard size={20} />} />

      <div className="p-4 space-y-4 pb-24 py-20 flex flex-col items-center">
        {loading ? (
          <p className="text-lg text-gray-500">Загрузка...</p>
        ) : events.length === 0 ? (
          <p className="text-lg text-gray-600">У вас нет активных записей.</p>
        ) : (
          events.map((event) => (
            <EventCard
              key={event.id}
              event={event}
              // totalSpots можно передать, если есть в API, здесь 20 по умолчанию
              totalSpots={20}
            />
          ))
        )}
      </div>

      <BottomNavBar />
    </>
  );
};

export default AppointmentsPage;
