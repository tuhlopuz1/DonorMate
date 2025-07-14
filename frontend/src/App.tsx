import logo from './assets/donor_logo.jpg'

export default function App() {
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

      {/* Можно оставить текст совсем минимальным */}
      <p className="text-xs text-gray-400 mt-1">Загрузка...</p>
    </div>
  );
}
