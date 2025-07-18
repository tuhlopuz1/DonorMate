import React from "react";
import logo from '../assets/MEPHI_logo.png';
import '../index.css'

const About: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12 animate-fade-in">
          <h1 className="text-5xl font-extrabold text-blue-800 mb-6 tracking-tight">
            О нашем проекте
          </h1>
          <div className="w-24 h-2 bg-blue-600 mx-auto mb-8 rounded-full"></div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8 mb-12 animate-fade-in-up-10">
        <div className="flex items-center gap-6 mb-6">
          <img
            src={logo}
            alt="МИФИ"
            className="w-30 h-30 drop-shadow-md animate-fade-in flex-shrink-0"
          />
          <p className="text-lg text-gray-700 leading-relaxed">
            Добро пожаловать в наш проект! Мы создаем инновационного Telegram-бота для автоматизации 
            взаимодействия с донорами в учебных заведениях.
          </p>
        </div>
          
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            Университеты регулярно проводят донорские мероприятия, но координация сотен студентов, 
          отслеживание регистраций, учет медицинских отводов и напоминание о сроках — это сложная 
            организационная задача.
          </p>
          
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            Наш бот не просто отправляет сообщения — он обеспечивает полноценное взаимодействие 
            с пользователями, запоминает важные данные и автоматически реагирует на события 
            в нужное время.
          </p>
          
          <p className="text-lg text-gray-700 leading-relaxed">
            Проект разрабатывается по заданию Донорского центра МИФИ с целью упрощения 
            и оптимизации процесса донорства в учебных заведениях.
          </p>
        </div>

        <div className="text-center animate-fade-in-up delay-100">
          <button 
            onClick={() => {window.location.href = '/#/survey'}} 
            className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
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