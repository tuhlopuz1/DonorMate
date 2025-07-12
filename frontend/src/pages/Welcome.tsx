import React from "react";

const WelcomePage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-8 text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Добро пожаловать!
        </h1>
        <p className="text-lg text-gray-600 mb-6">
          Рады видеть вас на нашем сайте. Начните своё путешествие прямо сейчас!
        </p>
        <button onClick={() => {window.location.href = '/about'}} className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-6 rounded-xl transition duration-300">
          Начать
        </button>
      </div>
    </div>
  );
};

export default WelcomePage;
