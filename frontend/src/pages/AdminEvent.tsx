// pages/EventPage.tsx
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import AdminEventCard from "../components/layouts/AdminEventCard";

import { MdEvent } from "react-icons/md";
import { ScanLine } from "lucide-react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

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
    date: "2025-07-17",
    timeRange: "15:00 – 17:00",
    location: "ул. Пушкина, д. 10, Москва",
    description:
      "Приглашаем вас на мастер-класс, где вы узнаете основы композиции, работы со светом и постобработки.",
    totalSpots: 20,
    spotsLeft: 5,
    isRegistered: true,
  };
};

const AdminEventPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<EventData | null>(null);
  const [loading, setLoading] = useState(true);
  const MySwal = withReactContent(Swal);

  useEffect(() => {
    if (id) {
      mockFetchEventById(id).then((data) => {
        setEvent(data);
        setLoading(false);
      });
    }
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

  const handleSendBroadcast = async () => {
    const { value: formValues } = await MySwal.fire({
      title: "Рассылка участникам",
      html: `
        <textarea id="message-text" class="swal2-textarea" placeholder="Введите сообщение"></textarea>
        <select id="recipient-type" class="swal2-select" style="margin-top: 10px">
          <option value="registered">Зарегистрированные участники</option>
          <option value="registered-not-attended">Зарегистрированные, не пришли</option>
          <option value="attended">Те, кто пришёл</option>
          <option value="not-registered">Не зарегистрированные</option>
        </select>
      `,
      focusConfirm: false,
      showCancelButton: true,
      confirmButtonText: "Отправить рассылку",
      preConfirm: () => {
        const message = (
          document.getElementById("message-text") as HTMLTextAreaElement
        )?.value;
        const recipient = (
          document.getElementById("recipient-type") as HTMLSelectElement
        )?.value;

        if (!message || !recipient) {
          Swal.showValidationMessage("Пожалуйста, заполните все поля.");
          return;
        }

        return { message, recipient };
      },
    });

    if (formValues) {
      console.log("Сообщение:", formValues.message);
      console.log("Кому отправить:", formValues.recipient);

      // Здесь вы можете отправить данные на сервер:
      // await sendBroadcastMessage(event.id, formValues.message, formValues.recipient);

      MySwal.fire("Успешно!", "Рассылка отправлена.", "success");
    }
  };

  if (loading || !event) {
    return <div className="p-6 text-gray-600">Загрузка мероприятия...</div>;
  }

  return (
    <div className="p-6 pt-16 max-w-2xl mx-auto">
      <AdminPageTopBar title="Страница мероприятия" icon={<MdEvent size={20} />} />

      <AdminEventCard
        title={event.title}
        date={event.date}
        timeRange={event.timeRange}
        location={event.location}
        spotsLeft={event.spotsLeft}
        totalSpots={event.totalSpots}
        description={event.description}
        isRegistered={event.isRegistered}
      />

      {(isToday(event.date) && event.isRegistered) ? (
        <div className="flex justify-between items-center mt-6 bg-blue-600 text-white px-4 py-2 rounded-xl text-sm">
          <p>Отметить участника по QR-коду</p>
          <ScanLine />
        </div>
      ) : (
        <div></div>
      )}

      {/* Кнопка рассылки */}
      <div className="mt-6">
        <button
          onClick={handleSendBroadcast}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl text-sm"
        >
          Сделать рассылку
        </button>
      </div>
    </div>
  );
};

export default AdminEventPage;
