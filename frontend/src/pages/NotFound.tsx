// src/pages/NotFound.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';


const NotFound: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50 text-blue-800 px-4">
      <h1 className="text-9xl font-bold">404</h1>
      <p className="text-2xl mt-4">Упс! Страница не найдена.</p>
      <p className="mt-2 text-blue-600">Возможно, вы ввели неверный адрес или страница была удалена.</p>
      <button
        onClick={() => navigate(-1)}
        className="mt-6 inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg shadow transition duration-300"
      >
        Вернуться назад
      </button>

    </div>
  );
};

export default NotFound;
