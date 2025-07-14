import { useEffect, useState } from 'react';
import logo from './assets/donor_logo.jpg';

interface TelegramUser {
  id: number;
  first_name: string;
  last_name: string;
  username: string;
  language_code: string;
  is_premium: boolean;
  added_to_attachment_menu: boolean;
  allows_write_to_pm: boolean;
  photo_url: string;
}

declare global {
  interface Window {
    Telegram: {
      WebApp: {
        ready: () => void;
        initDataUnsafe: {
          user: TelegramUser;
        };
        initData: string;
      };
    };
  }
}

export default function App() {
  const [user, setUser] = useState<TelegramUser | null>(null);

  useEffect(() => {
    if (window.Telegram && window.Telegram.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready(); // Обязательно вызываем при инициализации

      const userData = tg.initDataUnsafe?.user;
      if (userData) {
        setUser(userData);
      }
      console.log(tg)
      console.log(user)
      console.log(window.Telegram.WebApp.initDataUnsafe)
      try {
        localStorage.setItem('donor_photo_url', window.Telegram.WebApp.initDataUnsafe.user.photo_url)
        localStorage.setItem('donor_username', window.Telegram.WebApp.initDataUnsafe.user.username)
        localStorage.setItem('donor_id', window.Telegram.WebApp.initDataUnsafe.user.id.toString())
      }
      catch (error) {
        window.location.href = '/#/not-available'
      }
      console.log(localStorage.getItem('donor_photo_url'))


      const formData = new URLSearchParams();
      formData.append("initData", window.Telegram.WebApp.initData);


    // Отправляем initData на бэкенд
    fetch("https://api.donor.vickz.ru/api/auth/telegram", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            console.log("Token:", data.token);
            // использовать token для API-запросов
        } else {
            console.log(data)
            console.log(data.detail)
            alert("Ошибка авторизации");
        }
    });












    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 pb-24">
      {/* Логотип ВУЗа */}
      <img
        src={logo}
        alt="Университет"
        className="w-40 h-40 mb-24 drop-shadow-2xl animate-fade-in"
      />

      {/* Анимация загрузки */}
      <div className="flex space-x-3 mb-2">
        <span className="w-4 h-4 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.4s]" />
        <span className="w-4 h-4 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.2s]" />
        <span className="w-4 h-4 bg-blue-600 rounded-full animate-bounce" />
      </div>

    </div>
  );
}
