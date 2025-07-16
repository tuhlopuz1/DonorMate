import { useState } from "react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminEventCard from "../components/layouts/AdminEventCard";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiCalendar, FiDownload } from "react-icons/fi";

const AdminEventsPage = () => {
  // Состояние для выбранной вкладки: "upcoming" или "past"
  const [activeTab, setActiveTab] = useState("upcoming");

  // Данные мероприятий (лучше вынести в отдельный файл или загрузить с сервера)
  const events = [
    {
      title: "День донора",
      date: "2025-07-10",
      timeRange: "13:00–15:00",
      location: "Актовый зал, корпус Б",
      spotsLeft: 1,
      totalSpots: 30,
      description: "Ежегодная донорская акция. При себе иметь паспорт и СНИЛС.",
      isRegistered: false,
    },
    {
      title: "День донора",
      date: "2025-07-20",
      timeRange: "13:00–15:00",
      location: "Актовый зал, корпус Б",
      spotsLeft: 0,
      totalSpots: 30,
      description: "Ежегодная донорская акция. При себе иметь паспорт и СНИЛС.",
      isRegistered: false,
    },
    {
      title: "День донора",
      date: "2025-07-20",
      timeRange: "13:00–15:00",
      location: "Актовый зал, корпус Б",
      spotsLeft: 1,
      totalSpots: 30,
      description: "Ежегодная донорская акция. При себе иметь паспорт и СНИЛС.",
      isRegistered: true,
    },
    {
      title: "День донора",
      date: "2025-07-20",
      timeRange: "13:00–15:00",
      location: "Актовый зал, корпус Б",
      spotsLeft: 1,
      totalSpots: 30,
      description: "Ежегодная донорская акция. При себе иметь паспорт и СНИЛС. и снилс и снилс и снилс и снилс",
      isRegistered: false,
    },
    {
      title: "День донора",
      date: "2025-07-20",
      timeRange: "13:00–15:00",
      location: "Актовый зал, корпус Б",
      spotsLeft: 1,
      totalSpots: 30,
      description: "Ежегодная донорская акция. При себе иметь паспорт и СНИЛС. и снилс и снилс и снилс и снилс",
      isRegistered: false,
    },
    {
      title: "День донора",
      date: "2025-07-20",
      timeRange: "13:00–15:00",
      location: "Актовый зал, корпус Б",
      spotsLeft: 1,
      totalSpots: 30,
      description: "Ежегодная донорская акция. При себе иметь паспорт и СНИЛС. и снилс и снилс и снилс и снилс",
      isRegistered: false,
    },
  ];

  // Фильтруем мероприятия по дате относительно текущей даты
  const today = new Date();

  // Предстоящие (включая сегодняшние)
  const upcomingEvents = events.filter(
    (event) => new Date(event.date) >= today
  );

  // Завершённые (раньше сегодняшнего дня)
  const pastEvents = events.filter((event) => new Date(event.date) < today);

  return (
    <div className="pt-10 pb-14">
      <AdminPageTopBar title="Расписание мероприятий" icon={<FiCalendar size={20} />} />

            <div className="flex mt-6 mx-4 gap-3 items-center justify-between bg-red-500 shadow rounded-2xl p-5">
                <p className="text-lg font-bold text-white">Экспорт данных в CSV</p>
                <FiDownload color="white" size={23}/>
            </div>

      {/* Вкладки */}
      <div className="w-[100%] flex justify-center mt-4 border-b border-gray-300 bg-white">
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

      {/* Контент вкладок */}
      <div className="flex flex-col gap-6 p-6">
        {activeTab === "upcoming" &&
          (upcomingEvents.length ? (
            upcomingEvents.map((event, i) => <AdminEventCard key={i} {...event} />)
          ) : (
            <p>Нет предстоящих мероприятий</p>
          ))}

        {activeTab === "past" &&
          (pastEvents.length ? (
            pastEvents.map((event, i) => <AdminEventCard key={i} {...event} />)
          ) : (
            <p>Нет завершённых мероприятий</p>
          ))}
      </div>

      <AdminBottomNavBar />
    </div>
  );
};

export default AdminEventsPage;
