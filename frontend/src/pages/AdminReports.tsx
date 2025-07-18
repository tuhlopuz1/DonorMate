import { useState, useEffect } from "react";
import AdminPageTopBar from "../components/layouts/AdminPageTopBar";
import { FiMessageSquare, FiTrash2, FiSend } from "react-icons/fi";
import { MessageCircleQuestion } from "lucide-react";
import AdminBottomNavBar from "../components/layouts/AdminNavBar";
interface Question {
  id: string;
  userId: string;
  text: string;
}

const AdminReportPage = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [answerModalOpen, setAnswerModalOpen] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [answerText, setAnswerText] = useState("");

  // Функция для загрузки вопросов с сервера
  const fetchQuestions = async () => {
    try {
      setLoading(true);
      // Здесь будет реальный GET запрос к вашему API
      // const response = await fetch('/api/questions');
      // const data = await response.json();
      
      // Заглушка для демонстрации
      const mockData: Question[] = [
        { id: "1", userId: "user123", text: "Как мне зарегистрироваться  на мероприятие?" },
        { id: "2", userId: "user456", text: "Где будет проходить день донора?" },
        { id: "3", userId: "user789", text: "Нужно ли приносить свои документы?" },
      ];
      
      setQuestions(mockData);
      setLoading(false);
    } catch (err) {
      setError("Не удалось загрузить вопросы");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  // Функция для удаления вопроса
  const handleDeleteQuestion = async (questionId: string) => {
    try {
      // Здесь будет реальный DELETE запрос к вашему API
      // await fetch(`/api/questions/${questionId}`, { method: 'DELETE' });
      
      // Заглушка для демонстрации
      console.log(`Deleting question with ID: ${questionId}`);
      
      // Обновляем список вопросов
      setQuestions(questions.filter(q => q.id !== questionId));
    } catch (err) {
      setError("Не удалось удалить вопрос");
    }
  };

  // Функция для отправки ответа
  const handleSendAnswer = async () => {
    if (!currentQuestion || !answerText.trim()) return;

    try {
      // 1. Удаляем вопрос
      await handleDeleteQuestion(currentQuestion.id);
      
      // 2. Отправляем уведомление пользователю
      // Здесь будет реальный POST запрос к вашему API
      // await fetch('/api/notifications', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     userId: currentQuestion.userId,
      //     message: answerText
      //   })
      // });
      
      // Заглушка для демонстрации
      console.log(`Sending answer to user ${currentQuestion.userId}: ${answerText}`);
      
      // Закрываем модальное окно и сбрасываем состояние
      setAnswerModalOpen(false);
      setCurrentQuestion(null);
      setAnswerText("");
      
      // Обновляем список вопросов
      await fetchQuestions();
    } catch (err) {
      setError("Не удалось отправить ответ");
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
        <AdminPageTopBar title="Ответы на вопросы" icon={<MessageCircleQuestion size={20} />} />
        <div className="p-6 mt-14 text-center">Загрузка...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="pt-10 pb-14">
        <AdminPageTopBar title="Расписание мероприятий" icon={<MessageCircleQuestion size={20} />} />
        <div className="p-6 mt-14 text-center text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="pt-10 pb-14">
      <AdminPageTopBar title="Расписание мероприятий" icon={<MessageCircleQuestion size={20} />} />

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
              <p className="text-gray-800 mb-3">{question.text}</p>
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
            <p className="text-gray-700 mb-2">{currentQuestion?.text}</p>
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