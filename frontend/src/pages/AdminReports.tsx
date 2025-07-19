import { useState, useEffect } from "react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiMessageSquare, FiTrash2, FiSend, FiCalendar } from "react-icons/fi";
import apiRequest from "../components/utils/apiRequest";

interface Question {
  id: string;
  user_id: number;
  question: string;
}

const AdminReportPage = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [answerModalOpen, setAnswerModalOpen] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [answerText, setAnswerText] = useState("");

  const sendNotification = async (userId: number, message: string) => {
    try {
      const response = await apiRequest({
        url: `https://api.donor.vickz.ru/api/send-message/${userId}`,
        method: "POST",
        params: { msg: message },
        auth: true,
      });

      if (!response.ok) {
        throw new Error("Не удалось отправить уведомление");
      }
    } catch (err) {
      throw new Error(err instanceof Error ? err.message : "Ошибка отправки уведомления");
    }
  };

  // Функция для загрузки вопросов с сервера
  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const response = await apiRequest({
        url: "https://api.donor.vickz.ru/api/get-all-questions",
        method: "GET",
        auth: true,
      });

      if (!response.ok) {
        throw new Error("Не удалось загрузить вопросы");
      }

      const data: Question[] = await response.json();
      setQuestions(data);
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Неизвестная ошибка");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  // Функция для удаления вопроса
  const handleDeleteQuestion = async (questionId: string) => {
    try {
      const response = await apiRequest({
        url: `https://api.donor.vickz.ru/api/delete-question/${questionId}`,
        method: "DELETE",
        auth: true,
      });

      if (!response.ok) {
        throw new Error("Не удалось удалить вопрос");
      }

      // Обновляем список вопросов
      setQuestions(questions.filter((q) => q.id !== questionId));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось удалить вопрос");
    }
  };

  // Функция для отправки ответа
  const handleSendAnswer = async () => {
    if (!currentQuestion || !answerText.trim()) return;

    try {
      // 1. Удаляем вопрос
      await handleDeleteQuestion(currentQuestion.id);

      // 2. Отправляем уведомление пользователю (заглушка)

      const tg_message =  "!Администратор ответил на ваш вопрос!\n" + "❓ *Вопрос:*\n" + currentQuestion.question + "💡 *Ответ:*\n" + answerText

      await sendNotification(currentQuestion.user_id, tg_message);
      // В реальном приложении здесь будет вызов API для отправки уведомления

      // Закрываем модальное окно и сбрасываем состояние
      setAnswerModalOpen(false);
      setCurrentQuestion(null);
      setAnswerText("");

      // Обновляем список вопросов
      await fetchQuestions();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось отправить ответ");
    }
  };

  // Функция для открытия модального окна ответа
  const openAnswerModal = (question: Question) => {
    setCurrentQuestion(question);
    setAnswerModalOpen(true);
  };

  if (loading) {
    return (
      <div className="pt-10 pb-14">
        <AdminPageTopBar title="Вопросы от пользователей" icon={<FiCalendar size={20} />} />
        <div className="p-6 mt-14 text-center">Загрузка...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="pt-10 pb-14">
        <AdminPageTopBar title="Вопросы от пользователей" icon={<FiCalendar size={20} />} />
        <div className="p-6 mt-14 text-center text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="pt-10 pb-14">
      <AdminPageTopBar title="Вопросы от пользователей" icon={<FiCalendar size={20} />} />

      {/* Список вопросов */}
      <div className="flex flex-col gap-4 p-6 mt-14">
        {questions.length === 0 ? (
          <p className="text-center text-gray-500">Нет вопросов для отображения</p>
        ) : (
          questions.map((question) => (
            <div
              key={question.id}
              className="p-4 border border-gray-200 rounded-lg shadow-sm"
            >
              <p className="text-gray-800 mb-3">{question.question}</p>
              <div className="flex justify-end gap-2">
                <button
                  onClick={() => openAnswerModal(question)}
                  className="flex items-center gap-1 px-3 py-1 text-sm text-white bg-blue-600 rounded hover:bg-blue-700"
                >
                  <FiMessageSquare size={14} />
                  Ответить
                </button>
                <button
                  onClick={() => handleDeleteQuestion(question.id)}
                  className="flex items-center gap-1 px-3 py-1 text-sm text-white bg-red-600 rounded hover:bg-red-700"
                >
                  <FiTrash2 size={14} />
                  Удалить
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Модальное окно для ответа */}
      {answerModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg w-full max-w-md mx-4">
            <h3 className="text-lg font-medium mb-4">Ответ на вопрос</h3>
            <p className="text-gray-700 mb-2">{currentQuestion?.question}</p>
            <textarea
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded mb-4"
              rows={4}
              placeholder="Введите ваш ответ..."
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => {
                  setAnswerModalOpen(false);
                  setAnswerText("");
                }}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded hover:bg-gray-50"
              >
                Отмена
              </button>
              <button
                onClick={handleSendAnswer}
                className="flex items-center gap-1 px-4 py-2 text-white bg-blue-600 rounded hover:bg-blue-700"
                disabled={!answerText.trim()}
              >
                <FiSend size={16} />
                Отправить
              </button>
            </div>
          </div>
        </div>
      )}

      <AdminBottomNavBar />
    </div>
  );
};

export default AdminReportPage;