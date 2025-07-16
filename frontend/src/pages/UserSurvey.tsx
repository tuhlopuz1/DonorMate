import logo from '../assets/donor_logo.jpg';
import { useMedotvodModal } from '../components/layouts/Medotvod';
import type { MedotvodData } from '../components/layouts/Medotvod';

import { useState } from 'react';

export default function UserSurvey() {
  const [medotvod, setMedotvod] = useState<'yes' | 'no' | ''>('');

  const handleMedotvodSubmit = (data: MedotvodData) => {
    console.log("Медотвод получен:", data);
    // Сюда отправку на сервер
  };

  const openMedotvodModal = useMedotvodModal(handleMedotvodSubmit);

  return (
    <div className="flex flex-col items-center min-h-screen px-6 py-12">
      {/* Логотип */}
      <img
        src={logo}
        alt="МИФИ"
        className="w-28 h-28 mb-8 drop-shadow-md animate-fade-in"
      />

      <h1 className="text-2xl font-semibold text-blue-700 mb-6 animate-fade-in">
        Первый шаг к донорству
      </h1>

      <form className="w-full max-w-md space-y-5 animate-fade-in-slow">
        <input
          type="text"
          placeholder="Фамилия Имя Отчество"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <input
          type="number"
          placeholder="Возраст"
          min={0}
          max={120}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <select className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm">
          <option disabled selected>Пол</option>
          <option>Мужской</option>
          <option>Женский</option>
          <option>Предпочитаю не указывать</option>
        </select>

        <input
          type="text"
          placeholder="Факультет / Институт"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <input
          type="text"
          placeholder="Учебная группа"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <input
          type="number"
          placeholder="Вес (кг)"
          min={0}
          max={1000}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <select className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm">
          <option disabled selected>Есть ли хронические заболевания?</option>
          <option>Нет</option>
          <option>Да</option>
        </select>

        <fieldset className="border border-blue-300 rounded-xl p-4 shadow-sm">
          <legend className="text-gray-700 mb-2">Есть ли у вас медицинский отвод?</legend>
          <div className="flex space-x-6">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="medotvod"
                value="yes"
                checked={medotvod === 'yes'}
                onChange={() => setMedotvod('yes')}
                className="w-5 h-5 text-blue-600 focus:ring-blue-400"
              />
              <span>Да</span>
            </label>

            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="medotvod"
                value="no"
                checked={medotvod === 'no'}
                onChange={() => setMedotvod('no')}
                className="w-5 h-5 text-blue-600 focus:ring-blue-400"
              />
              <span>Нет</span>
            </label>
          </div>

          {medotvod === 'yes' && (
            <button
              type="button"
              onClick={openMedotvodModal}
              className="mt-4 px-5 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
            >
              Прикрепить медотвод
            </button>
          )}
        </fieldset>


        <select className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm">
          <option disabled selected>Сдавали ли вы кровь раньше?</option>
          <option>Нет</option>
          <option>Да, один раз</option>
          <option>Да, регулярно</option>
        </select>

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl shadow-lg transition-all duration-300 mt-4"
        >
          Отправить анкету
        </button>
      </form>


    </div>
  );
}
