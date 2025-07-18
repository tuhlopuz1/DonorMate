import React from "react";
import logo from '../assets/MEPHI_logo.png';
import '../index.css';

const Donorship: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-12">
        
        {/* Назад кнопка */}
        <div className="flex justify-center sm:justify-end animate-fade-in-up delay-100">
          <button 
            onClick={() => {window.location.href = '/#/main'}} 
            className="inline-flex items-center px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white text-base sm:text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Назад
          </button>
        </div>

        {/* Заголовок */}
        <div className="text-center animate-fade-in">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-blue-800 mb-6 tracking-tight">
            О донорстве
          </h1>
          <div className="w-20 sm:w-24 h-2 bg-blue-600 mx-auto mb-6 rounded-full"></div>
        </div>

        {/* Основной контент */}
        <div className="bg-white rounded-xl shadow-lg p-6 sm:p-8 animate-fade-in-up-10 space-y-8">

          {/* Логотип и вступление */}
          <div className="flex flex-col sm:flex-row items-center gap-6">
            <img
              src={logo}
              alt="МИФИ"
              className="w-32 h-32 object-contain drop-shadow-md animate-fade-in"
            />
            <p className="text-base sm:text-lg text-gray-700 leading-relaxed">
              Донорство крови — это важный и благородный поступок, который может спасти жизни. Каждая сдача крови может помочь сразу нескольким пациентам.
            </p>
          </div>

          {/* Кто может быть донором */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">Кто может стать донором?</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              <li>Граждане РФ в возрасте от 18 лет</li>
              <li>Масса тела не менее 50 кг</li>
              <li>Отсутствие противопоказаний к донорству</li>
              <li>Прохождение предварительного медицинского осмотра</li>
            </ul>
          </section>

          {/* Противопоказания */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">Противопоказания</h2>
            <p className="text-gray-700 mb-2">Противопоказания бывают временные и постоянные:</p>

            <h3 className="font-semibold text-gray-800 mt-2">⏳ Временные противопоказания:</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-1 mb-4">
              <li>Простудные и инфекционные заболевания (30 дней после выздоровления)</li>
              <li>После прививок — от 10 до 30 дней</li>
              <li>Удаление зуба — 10 дней</li>
              <li>Татуировки, пирсинг — 1 год</li>
              <li>Контакт с больным гепатитом — 1 год</li>
              <li>Менструация — 5 дней</li>
              <li>Беременность и кормление грудью — 1 год после родов</li>
            </ul>

            <h3 className="font-semibold text-gray-800 mt-2">⛔️ Постоянные противопоказания:</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Гепатит B или C</li>
              <li>ВИЧ-инфекция</li>
              <li>Туберкулез</li>
              <li>Онкологические заболевания</li>
              <li>Серьезные сердечно-сосудистые болезни</li>
              <li>Заболевания крови</li>
              <li>Наркомания, алкоголизм</li>
            </ul>
          </section>

          {/* Перед сдачей */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">Что нужно знать перед сдачей крови?</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Накануне не употребляйте жирную, жареную, молочную пищу и алкоголь</li>
              <li>Выспитесь, будьте отдохнувшими</li>
              <li>Утром — лёгкий завтрак (чай, хлеб, сухари)</li>
              <li>Не сдавайте кровь натощак</li>
            </ul>
          </section>

          {/* После сдачи */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">После сдачи крови:</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Отдохните 10–15 минут</li>
              <li>Не курите минимум 1 час</li>
              <li>Избегайте физических нагрузок в течение суток</li>
              <li>Пейте больше жидкости</li>
              <li>Не снимайте повязку минимум 4 часа</li>
            </ul>
          </section>

          <p className="text-base sm:text-lg text-gray-700 leading-relaxed mt-6">
            Донорство — это не только помощь другим, но и вклад в собственное здоровье. У доноров наблюдается обновление крови и укрепление иммунной системы.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Donorship;
