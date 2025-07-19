import React from "react";
import logo from '../assets/MEPHI_logo.png';
import { HeartPulse, Users, Clock, Bot, ShieldCheck } from "lucide-react";
import '../index.css';

const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Заголовок */}
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-blue-800 mb-4">
            О проекте
          </h1>
          <div className="w-20 h-1.5 bg-blue-600 mx-auto rounded-full"></div>
        </div>

        {/* Основной контент */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8">
          {/* Логотип и краткое описание */}
          <div className="p-6 sm:p-8 flex flex-col sm:flex-row items-center gap-6 border-b border-gray-100">
            <img
              src={logo}
              alt="МИФИ"
              className="w-20 h-20 sm:w-24 sm:h-24 object-contain"
            />
            <p className="text-lg text-gray-800 font-medium text-center sm:text-left">
              Telegram-бот для автоматизации донорских мероприятий в учебных заведениях
            </p>
          </div>

          {/* Ключевые преимущества */}
          <div className="p-6 sm:p-8 space-y-6">
            <div className="flex items-start gap-4">
              <div className="bg-blue-100 p-2 rounded-full flex-shrink-0">
                <HeartPulse className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">400+ доноров</h3>
                <p className="text-gray-600">Участвуют в акциях через наш сервис</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="bg-blue-100 p-2 rounded-full flex-shrink-0">
                <Users className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1"></h3>
                <p className="text-gray-600">Уже используют наше решение для донорских акций</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="bg-blue-100 p-2 rounded-full flex-shrink-0">
                <ShieldCheck className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Безопасность данных</h3>
                <p className="text-gray-600">Полное соответствие требованиям защиты персональных данных</p>
              </div>
            </div>
          </div>
        </div>

        {/* Как это работает */}
        <div className="bg-white rounded-xl shadow-md p-6 sm:p-8 mb-8">
          <h2 className="text-2xl font-bold text-blue-800 mb-6 flex items-center gap-3">
            <Bot className="w-6 h-6" />
            <span>Как это работает?</span>
          </h2>
          
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="bg-blue-600 text-white font-bold rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">
                1
              </div>
              <p className="text-gray-700">Студент регистрируется в боте чере Telegram</p>
            </div>
            
            <div className="flex gap-4">
              <div className="bg-blue-600 text-white font-bold rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">
                2
              </div>
              <p className="text-gray-700">Студент выбирает мероприятие в личном кабинете</p>
            </div>
            
            <div className="flex gap-4">
              <div className="bg-blue-600 text-white font-bold rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">
                3
              </div>
              <p className="text-gray-700">Бот напоминает о дате акции и предоставляет инструкции</p>
            </div>
            
            <div className="flex gap-4">
              <div className="bg-blue-600 text-white font-bold rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">
                4
              </div>
              <p className="text-gray-700">После сдачи крови бот записывает дату следующей возможной сдачи</p>
            </div>
          </div>
        </div>

        {/* Кнопка CTA */}
        <div className="text-center">
          <button 
            onClick={() => {window.location.href = '/#/survey'}} 
            className="inline-flex items-center px-6 py-3 sm:px-8 sm:py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white text-base sm:text-lg font-semibold rounded-lg shadow-md hover:shadow-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Начать использование
            <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default About;