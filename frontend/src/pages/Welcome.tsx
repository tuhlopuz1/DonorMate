import logo from '../assets/donor_logo.jpg'

export default function WelcomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
      {/* Логотип */}
      <img
        src={logo}
        alt="МИФИ"
        className="w-36 h-36 mb-12 drop-shadow-md animate-fade-in"
      />

      {/* Приветствие */}
      <h1 className="text-3xl font-semibold text-blue-700 mb-4 animate-fade-in">
        Добро пожаловать!
      </h1>

      <p className="max-w-md text-blue-600 text-base leading-relaxed mb-10 animate-fade-in-slow">
        Мы — студенческий проект, который помогает делать добро. Присоединяйтесь к донорским акциям прямо в МИФИ.
      </p>

      {/* Кнопки */}
<div className="flex flex-col space-y-4 w-full max-w-xs">
  {/* Кнопка "Начать" */}
  <button onClick={() => {window.location.href = '/#/survey'}} className="w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white font-semibold py-3 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 animate-fade-in">
    Начать
  </button>

  {/* Кнопка "Узнать больше" */}
  <button onClick={() => {window.location.href = '/#/about'}} className="w-full bg-white text-blue-600 font-semibold py-3 rounded-2xl border border-blue-400 hover:border-blue-500 hover:bg-blue-50 shadow-sm hover:shadow-md transition-all duration-300 animate-fade-in-slow">
     Узнать больше
  </button>
</div>

    </div>
  );
}
