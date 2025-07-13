import logo from '../assets/MEPHI_logo.png';

export default function UserSurvey() {
  return (
    <div className="flex flex-col items-center min-h-screen bg-gradient-to-br from-rose-100 via-white to-sky-100 px-6 py-12">
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
        {/* ФИО */}
        <input
          type="text"
          placeholder="Фамилия Имя Отчество"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        {/* Возраст */}
        <input
          type="number"
          placeholder="Возраст"
          min={0}
          max={120}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        {/* Пол */}
        <select className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm">
          <option disabled selected>Пол</option>
          <option>Мужской</option>
          <option>Женский</option>
          <option>Предпочитаю не указывать</option>
        </select>

        {/* Факультет */}
        <input
          type="text"
          placeholder="Факультет / Институт"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        {/* Группа */}
        <input
          type="text"
          placeholder="Учебная группа"
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        {/* Вес */}
        <input
          type="number"
          placeholder="Вес (кг)"
          min={0}
          max={1000}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        {/* Болел ли чем-то серьёзным */}
        <select className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm">
          <option disabled selected>Есть ли хронические заболевания?</option>
          <option>Нет</option>
          <option>Да</option>
        </select>

        {/* Сдавал ли кровь ранее */}
        <select className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm">
          <option disabled selected>Сдавали ли вы кровь раньше?</option>
          <option>Нет</option>
          <option>Да, один раз</option>
          <option>Да, регулярно</option>
        </select>

        {/* Кнопка отправки */}
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
