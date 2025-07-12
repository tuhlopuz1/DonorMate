import { useEffect, useState } from 'react'

type TelegramUser = {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  photo_url?: string
  is_premium?: boolean
}

declare global {
  interface Window {
    Telegram: any
  }
}

export default function App() {
  const [user, setUser] = useState<TelegramUser | null>(null)

  const mockUser: TelegramUser = {
    id: 123456789,
    first_name: "Иван",
    last_name: "Иванов",
    username: "ivan_ivanov",
    language_code: "ru",
    photo_url: "https://t.me/i/userpic/320/Fi3tevnNM1S7O78KOWi9OhcruJjouym2VjWrc0jWXJoX2bceYivJAWMirAdpbkWr.svg",
    is_premium: false,
  };

  useEffect(() => {
    console.log(123123123)
    const tg = window.Telegram?.WebApp
    console.log(tg)
    tg?.ready()
    const initDataUnsafe = tg?.initDataUnsafe
    console.log(initDataUnsafe)
    if (initDataUnsafe?.user) {
      setUser(initDataUnsafe.user)
      console.log(user)
    }
    else {
        setUser(mockUser)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white shadow-xl rounded-2xl p-6 max-w-md w-full text-center">
        <h1 className="text-2xl font-bold mb-4">Telegram Профиль</h1>
        {user ? (
          <div>
            <img
              src={user.photo_url}
              alt="Avatar"
              className="w-24 h-24 rounded-full mx-auto mb-4"
            />
            <p><strong>ID:</strong> {user.id}</p>
            <p><strong>Имя:</strong> {user.first_name} {user.last_name}</p>
            <p><strong>Username:</strong> @{user.username}</p>
            <p><strong>Язык:</strong> {user.language_code}</p>
            {user.is_premium && <p className="text-yellow-500 font-bold">Premium</p>}
          </div>
        ) : (
          <p>Загрузка данных пользователя...</p>
        )}
      </div>
    </div>
  )
}
