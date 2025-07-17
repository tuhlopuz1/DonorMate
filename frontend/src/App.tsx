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
  console.log(user)
  useEffect(() => {
    if (window.Telegram && window.Telegram.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();

      const userData = tg.initDataUnsafe?.user;
      if (userData) {
        setUser(userData);
      }

      try {
        localStorage.setItem('donor_photo_url', userData.photo_url);
        localStorage.setItem('donor_username', userData.username);
        localStorage.setItem('donor_id', userData.id.toString());
      } catch (error) {
        window.location.href = '/#/not-available';
        return;
      }

      const formData = new URLSearchParams();
      formData.append('initData', tg.initData);

      fetch('https://api.donor.vickz.ru/api/get-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.access && data.refresh) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            // Теперь проверим, зарегистрирован ли пользователь
            const userId = userData.id;
            fetch(`https://api.donor.vickz.ru/api/is-registred/${userId}`, {
              method: 'GET',
              headers: {
                Authorization: `Bearer ${data.access}`,
              },
            })
              .then((res) => {
                if (res.status === 200) {
                  window.location.href = '/#/main';
                } else if (res.status === 204) {
                  window.location.href = '/#/welcome';
                } else {
                  console.error('Unexpected status:', res.status);
                  alert('Ошибка проверки регистрации');
                }
              })
              .catch((error) => {
                console.error('Ошибка при проверке регистрации:', error);
                alert('Ошибка соединения с сервером');
              });
          } else {
            console.log(data);
            alert('Ошибка авторизации');
          }
        })
        .catch((error) => {
          console.error('Ошибка при получении токена:', error);
          alert('Не удалось получить токены');
        });
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 pb-24">
      <img
        src={logo}
        alt="Университет"
        className="w-40 h-40 mb-24 drop-shadow-2xl animate-fade-in"
      />

      <div className="flex space-x-3 mb-2">
        <span className="w-4 h-4 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.4s]" />
        <span className="w-4 h-4 bg-blue-500 rounded-full animate-bounce [animation-delay:-0.2s]" />
        <span className="w-4 h-4 bg-blue-600 rounded-full animate-bounce" />
      </div>
    </div>
  );
}
