import { useState } from "react";
import { Phone } from "lucide-react";
import PageTopBar from "../components/layouts/PageTopBar";
import { MessageCircleQuestion } from "lucide-react";

export default function AskOrganizers() {
  const [question, setQuestion] = useState("");

  const handleSubmit = () => {
    if (question.trim()) {
      alert("Ваш вопрос отправлен!");
      setQuestion("");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <PageTopBar title="Вопрос организаторам" icon={<MessageCircleQuestion size={20} />}/>
      <div className="w-full max-w-xl bg-white p-6 rounded-2xl shadow-lg">
        <div className="space-y-6">
          <h1 className="text-2xl font-semibold text-gray-800">Задать вопрос организаторам</h1>

          <p className="text-gray-600 text-sm">
            ⏱ Среднее время ответа — <strong>до 2 часов</strong>.
          </p>

          <p className="text-gray-600 text-sm flex items-center gap-1">
            <Phone className="w-4 h-4" />
            Срочный вопрос? Позвоните:{" "}
            <a
              href="tel:+79991234567"
              className="text-blue-600 hover:underline font-medium"
            >
              +7 (999) 123-45-67
            </a>
          </p>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Напишите ваш вопрос здесь..."
            className="w-full min-h-[120px] p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />

          <button
            onClick={handleSubmit}
            disabled={!question.trim()}
            className={`w-full py-2 px-4 rounded-lg text-white font-medium transition 
              ${question.trim()
                ? "bg-blue-600 hover:bg-blue-700"
                : "bg-gray-300 cursor-not-allowed"}`}
          >
            Отправить
          </button>
        </div>
      </div>
    </div>
  );
}
