import { useEffect, useState } from "react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminEventCard from "../components/layouts/AdminEventCard";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiCalendar, FiDownload, FiPlus } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest";

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

const AdminEventsPage = () => {
  const [activeTab, setActiveTab] = useState<"upcoming" | "past">("upcoming");
  const [events, setEvents] = useState<EventData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-all-events",
          auth: true,
        });

        if (!response.ok) {
          throw new Error("Ошибка при загрузке мероприятий");
        }

        const data: EventData[] = await response.json();
        setEvents(data);
      } catch (error) {
        console.error("Ошибка загрузки мероприятий:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const upcomingEvents = events.filter(
    (event) => new Date(event.start_date) >= today
  );

  const pastEvents = events.filter(
    (event) => new Date(event.start_date) < today
  );

  return (
    <div className="pt-10 pb-14">
      <AdminPageTopBar
        title="Расписание мероприятий"
        icon={<FiCalendar size={20} />}
      />

      <div className="flex mt-6 mx-4 gap-3 items-center justify-between bg-blue-500 shadow rounded-2xl p-5">
        <p className="text-lg font-bold text-white">Экспорт данных в XLSX</p>
        <FiDownload color="white" size={23} />
      </div>

      <div
        className="flex mt-6 mx-4 gap-3 items-center justify-between bg-white shadow rounded-2xl p-5 cursor-pointer"
        onClick={() => {
          window.location.href = "/#/admin/create-event";
        }}
      >
        <p className="text-lg font-bold text-black">Новое мероприятие</p>
        <FiPlus size={23} />
      </div>

      <div className="w-full flex justify-center mt-4 border-b border-gray-300 bg-white">
        <button
          onClick={() => setActiveTab("upcoming")}
          className={`px-6 py-2 font-medium ${
            activeTab === "upcoming"
              ? "border-b-2 border-red-600 text-red-600"
              : "text-gray-500"
          }`}
        >
          Предстоящие
        </button>
        <button
          onClick={() => setActiveTab("past")}
          className={`px-6 py-2 font-medium ${
            activeTab === "past"
              ? "border-b-2 border-red-600 text-red-600"
              : "text-gray-500"
          }`}
        >
          Завершённые
        </button>
      </div>

      <div className="flex flex-col gap-6 p-6">
        {loading ? (
          <p>Загрузка мероприятий...</p>
        ) : activeTab === "upcoming" ? (
          upcomingEvents.length ? (
            upcomingEvents.map((event) => (
              <AdminEventCard key={event.id} event={event} />
            ))
          ) : (
            <p>Нет предстоящих мероприятий</p>
          )
        ) : pastEvents.length ? (
          pastEvents.map((event) => (
            <AdminEventCard key={event.id} event={event} />
          ))
        ) : (
          <p>Нет завершённых мероприятий</p>
        )}
      </div>

      <AdminBottomNavBar />
    </div>
  );
};

export default AdminEventsPage;
