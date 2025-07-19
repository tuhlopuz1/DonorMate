// pages/AdminEventPage.tsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import AdminEventCard from "../components/layouts/AdminEventCard";
import apiRequest from "../components/utils/apiRequest";

import { MdEvent } from "react-icons/md";
import { ScanLine } from "lucide-react";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

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

const AdminEventPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<EventData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        const response = await apiRequest({
          url: "https://api.donor.vickz.ru/api/get-all-events",
          method: "GET",
          auth: true,
        });

        const events: EventData[] = await response.json();
        const matchedEvent = events.find((e) => e.id === id);

        if (matchedEvent) {
          setEvent(matchedEvent);
        } else {
          Swal.fire("Ошибка", "Мероприятие не найдено", "error");
        }
      } catch (err) {
        console.error(err);
        Swal.fire("Ошибка", "Не удалось загрузить мероприятие", "error");
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchEvent();
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

    if (formValues && event) {
      try {
        console.log("Сообщение:", formValues.message);
        console.log("Кому отправить:", formValues.recipient);

        // Здесь можно отправить рассылку
        // await apiRequest({
        //   url: `https://api.donor.vickz.ru/api/send-broadcast/${event.id}`,
        //   method: "POST",
        //   body: {
        //     message: formValues.message,
        //     recipient: formValues.recipient,
        //   },
        //   auth: true,
        // });

        MySwal.fire("Успешно!", "Рассылка отправлена.", "success");
      } catch (error) {
        console.error(error);
        MySwal.fire("Ошибка", "Не удалось отправить рассылку", "error");
      }
    }
  };

  if (loading || !event) {
    return <div className="p-6 text-gray-600">Загрузка мероприятия...</div>;
  }

  return (
    <div className="p-6 pt-16 max-w-2xl mx-auto">
      <AdminPageTopBar title="Страница мероприятия" icon={<MdEvent size={20} />} />

      <AdminEventCard event={event} totalSpots={20} />

      {isToday(event.start_date) ? (
        <div onClick={() => {window.location.href = '/#/admin/scanner'}} className="flex justify-between items-center mt-6 bg-blue-600 text-white px-4 py-2 rounded-xl text-sm">
          <p>Отметить участника по QR-коду</p>
          <ScanLine />
        </div>
      ) : (
        <div></div>
      )}

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
