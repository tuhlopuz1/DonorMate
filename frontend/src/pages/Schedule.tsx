import { useEffect, useState } from "react";
import BottomNavBar from "../components/layouts/NavBar";
import EventCard from "../components/layouts/EventCard";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiCalendar } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest"; // убедитесь, что путь к apiRequest правильный

type EventFromServer = {
  id: string;
  name: string;
  description: string;
  registred: number;
  start_date: string;
  end_date: string;
  created_at: string;
  is_registred: boolean;
};

const SchedulePage = () => {
  const [activeTab, setActiveTab] = useState<"upcoming" | "past">("upcoming");
  const [events, setEvents] = useState<EventFromServer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-all-events",
          auth: true,
        });

        if (!response.ok) {
          throw new Error("Не удалось загрузить мероприятия");
        }

        const data: EventFromServer[] = await response.json();
        setEvents(data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const today = new Date();

  const upcomingEvents = events.filter(
    (event) => new Date(event.start_date) >= today
  );

  const pastEvents = events.filter(
    (event) => new Date(event.start_date) < today
  );

  return (
    <div className="pt-10 pb-14">
      <PageTopBar
        title="Расписание мероприятий"
        icon={<FiCalendar size={20} />}
      />

      {/* Tabs */}
      <div className="fixed w-full flex justify-center mt-4 border-b border-gray-300 bg-white z-10">
        <button
          onClick={() => setActiveTab("upcoming")}
          className={`px-6 py-2 font-medium ${
            activeTab === "upcoming"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500"
          }`}
        >
          Предстоящие
        </button>
        <button
          onClick={() => setActiveTab("past")}
          className={`px-6 py-2 font-medium ${
            activeTab === "past"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500"
          }`}
        >
          Завершённые
        </button>
      </div>

      {/* Content */}
      <div className="flex flex-col gap-6 p-6 mt-14">
        {loading && <p>Загрузка мероприятий...</p>}
        {error && <p className="text-red-600">{error}</p>}

        {!loading && !error && activeTab === "upcoming" && (
          <>
            {upcomingEvents.length ? (
              upcomingEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))
            ) : (
              <p>Нет предстоящих мероприятий</p>
            )}
          </>
        )}

        {!loading && !error && activeTab === "past" && (
          <>
            {pastEvents.length ? (
              pastEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))
            ) : (
              <p>Нет завершённых мероприятий</p>
            )}
          </>
        )}
      </div>

      <BottomNavBar />
    </div>
  );
};

export default SchedulePage;
