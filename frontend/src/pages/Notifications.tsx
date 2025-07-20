import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiBell } from "react-icons/fi";
import { FiInfo, FiAlertTriangle, FiXCircle } from "react-icons/fi";

type NotificationType = "info" | "warning" | "error";

interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  content: string;
  date: string;
}

const notifications: Notification[] = [
  {
    id: 1,
    type: "info",
    title: "Напоминание о донации",
    content: "Вы можете сдать кровь снова с 12 августа 2025 года.",
    date: "2025-07-10",
  },
  {
    id: 2,
    type: "warning",
    title: "Мероприятие отменено",
    content: "Донорское мероприятие капля жизни 20 июля отменено",
    date: "2025-07-08",
  },
  {
    id: 3,
    type: "error",
    title: "Медицинский отвод",
    content: "Вы временно не допущены к донации по медицинским показаниям.",
    date: "2025-07-05",
  },
  {
    id: 3,
    type: "error",
    title: "Медицинский отвод",
    content: "Вы временно не допущены к донации по медицинским показаниям.",
    date: "2025-07-05",
  },
  {
    id: 3,
    type: "error",
    title: "Медицинский отвод",
    content: "Вы временно не допущены к донации по медицинским показаниям.",
    date: "2025-07-05",
  },
  {
    id: 3,
    type: "error",
    title: "Медицинский отвод",
    content: "Вы временно не допущены к донации по медицинским показаниям.",
    date: "2025-07-05",
  },
  {
    id: 3,
    type: "error",
    title: "Медицинский отвод",
    content: "Вы временно не допущены к донации по медицинским показаниям.",
    date: "2025-07-05",
  },
];

const getNotificationStyle = (type: NotificationType) => {
  switch (type) {
    case "info":
      return {
        icon: <FiInfo className="text-blue-600" size={20} />,
        bg: "bg-blue-50",
        border: "border-blue-200",
        text: "text-blue-800",
      };
    case "warning":
      return {
        icon: <FiAlertTriangle className="text-yellow-600" size={20} />,
        bg: "bg-yellow-50",
        border: "border-yellow-200",
        text: "text-yellow-800",
      };
    case "error":
      return {
        icon: <FiXCircle className="text-red-600" size={20} />,
        bg: "bg-red-50",
        border: "border-red-200",
        text: "text-red-800",
      };
    default:
      return {
        icon: null,
        bg: "bg-gray-100",
        border: "border-gray-200",
        text: "text-gray-800",
      };
  }
};

const NotificationsPage = () => {
  return (
    <>
      <PageTopBar title="Уведомления" icon={<FiBell size={20} />} />

      <div className="p-4 pt-20 pb-20 space-y-4">
        {notifications.map((note) => {
          const style = getNotificationStyle(note.type);

          return (
            <div
              key={note.id}
              className={`flex items-start gap-4 p-4 rounded-xl shadow-sm border ${style.bg} ${style.border}`}
            >
              <div className="pt-1">{style.icon}</div>
              <div className="flex-1">
                <h4 className={`font-semibold ${style.text}`}>{note.title}</h4>
                <p className="text-sm text-gray-700">{note.content}</p>
                <p className="text-xs text-gray-500 mt-1">{note.date}</p>
              </div>
            </div>
          );
        })}
      </div>

      <BottomNavBar />
    </>
  );
};

export default NotificationsPage;
