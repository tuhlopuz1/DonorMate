

export default function WelcomePage() {


  const handleStart = () => {
    // Пример: вызов mainButton или переход в другой раздел
    alert("Добро пожаловать! 🚀")
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-white px-4 text-gray-800">
      <div className="w-full max-w-md rounded-2xl bg-gradient-to-br from-red-500 to-pink-500 p-6 shadow-xl">
        <h1 className="text-center text-3xl font-bold text-white drop-shadow-sm">
          Привет, донор! 🩸
        </h1>
        <p className="mt-4 text-center text-white text-sm">
          Университет проводит донорские дни. С этим ботом ты сможешь:
        </p>
        <ul className="mt-2 list-disc px-6 text-white text-sm space-y-1">
          <li>Записаться на донацию</li>
          <li>Следить за графиком</li>
          <li>Получать напоминания</li>
        </ul>
        <button
          onClick={handleStart}
          className="mt-6 w-full rounded-xl bg-white px-4 py-3 text-center text-lg font-semibold text-red-600 transition hover:bg-red-50 active:scale-95"
        >
          Начать
        </button>
      </div>

      <p className="mt-6 text-center text-xs text-gray-400">
        Поддерживается <span className="font-medium">Telegram Mini Apps</span>
      </p>
    </div>
  )
}
