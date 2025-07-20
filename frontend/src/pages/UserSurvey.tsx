import { useEffect, useState } from 'react';
import logo from '../assets/donor_logo.jpg';
import apiRequest from '../components/utils/apiRequest';

// Валидация ФИО: только кириллица и пробелы
const isValidFullname = (name: string) => /^[А-Яа-яЁё\s]+$/.test(name.trim());

export default function UserSurvey() {
  const [fullname, setFullname] = useState('');
  const [role, setRole] = useState('');
  const [group, setGroup] = useState('');
  const [consent, setConsent] = useState(false);

  // Получение токенов при загрузке страницы
  useEffect(() => {
    const tg = (window as any)?.Telegram?.WebApp;
    const initData = tg?.initData;
    if (localStorage.getItem('phone')) {
      if (localStorage.getItem('role') == 'DONOR') {
        window.location.href = '/#/main'
      }
      if (localStorage.getItem('role') == 'ADMIN') {
        window.location.href = '/#/admin/main'
      }
    }
    if (!initData) {
      console.warn('initData не найдено');
      return;
    }

      const formData = new URLSearchParams();
      formData.append('initData', tg.initData);

    const fetchTokens = async () => {
      try {
        const response = await fetch('https://api.donor.vickz.ru/api/get-token', {
          method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
        });

        if (!response.ok) throw new Error('Не удалось получить токены');

        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
      } catch (err) {
        console.error('Ошибка получения токенов:', err);
        alert('Ошибка авторизации через Telegram.');
      }
    };

    fetchTokens();
  }, []);

  const isFormValid = () => {
    const nameParts = fullname.trim().split(' ');
    return (
      nameParts.length >= 2 &&
      isValidFullname(fullname) &&
      role &&
      (role !== 'Студент МИФИ' || group.trim() !== '') &&
      consent
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const body = {
      fsp: fullname.trim(),
      group: role === 'Студент МИФИ' ? group.trim() : '',
      user_class: role,
    };

    try {
      const response = await apiRequest({
        url: 'https://api.donor.vickz.ru/api/post-register',
        method: 'POST',
        body,
        auth: true,
      });

      if (response.ok) {
        window.location.href = '/#/main';
      } else {
        const errorData = await response.json();
        console.error('Ошибка при отправке:', errorData);
        alert('Не удалось отправить анкету. Проверьте данные.');
      }
    } catch (error) {
      console.error('Ошибка сети:', error);
      alert('Произошла ошибка при отправке анкеты.');
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen px-6 py-12">
      <img src={logo} alt="МИФИ" className="w-28 h-28 mb-8 drop-shadow-md animate-fade-in" />

      <h1 className="text-2xl font-semibold text-blue-700 mb-6 animate-fade-in">
        Первый шаг к донорству
      </h1>

      <form
        className="w-full max-w-md space-y-5 animate-fade-in-slow"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          placeholder="Фамилия Имя Отчество"
          value={fullname}
          onChange={(e) => setFullname(e.target.value)}
          required
          className={`w-full px-4 py-3 rounded-xl border ${
            isValidFullname(fullname) || fullname === ''
              ? 'border-blue-300'
              : 'border-red-500'
          } focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm`}
        />

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        >
          <option disabled value="">Выберите вашу роль</option>
          <option>Студент МИФИ</option>
          <option>Сотрудник МИФИ</option>
          <option>Внешний донор</option>
        </select>

        {role === 'Студент МИФИ' && (
          <input
            type="text"
            placeholder="Учебная группа"
            value={group}
            onChange={(e) => setGroup(e.target.value)}
            required
            className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
          />
        )}

        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={consent}
            onChange={(e) => setConsent(e.target.checked)}
            className="w-5 h-5 text-blue-600 focus:ring-blue-400"
          />
          <span className="text-sm text-gray-700">
            Я даю согласие на обработку персональных данных
          </span>
        </label>

        <button
          type="submit"
          disabled={!isFormValid()}
          className={`w-full ${
            isFormValid() ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
          } text-white font-semibold py-3 rounded-xl shadow-lg transition-all duration-300 mt-4`}
        >
          Отправить анкету
        </button>
      </form>
    </div>
  );
}
