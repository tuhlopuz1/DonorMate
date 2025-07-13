
import { Sparkles } from 'lucide-react';

const WelcomePage = () => {
  return (
    <div className="relative h-screen w-full bg-gradient-to-br from-indigo-900 via-purple-900 to-indigo-900 overflow-hidden font-sans">
      {/* Фоновые световые круги */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-pink-500 opacity-20 rounded-full filter blur-3xl animate-pulse" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-500 opacity-20 rounded-full filter blur-3xl animate-pulse" />

      {/* Навигация */}
      <header className="z-10 relative flex items-center justify-between px-10 py-6">
        <h1 className="text-white text-2xl font-bold tracking-wide">MyGlassSite</h1>
        <nav className="space-x-6 text-white/80 text-sm md:text-base">
          <a href="#" className="hover:text-white transition">Home</a>
          <a href="#" className="hover:text-white transition">Features</a>
          <a href="#" className="hover:text-white transition">Contact</a>
        </nav>
      </header>

      {/* Основной блок */}
      <main className="z-10 relative flex flex-col items-center justify-center h-[80vh] text-center px-4">
        <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-10 shadow-2xl max-w-2xl">
          <h2 className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 via-pink-300 to-purple-400 animate-fade-in">
            Добро пожаловать!
          </h2>
          <p className="mt-4 text-lg text-white/80">
            Это красивая демонстрационная страница с эффектом <strong>liquid glass</strong>. Наслаждайтесь эстетикой и плавностью.
          </p>

          {/* Кнопка */}
          <button
            className="mt-8 px-6 py-3 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold rounded-full shadow-lg hover:scale-105 hover:shadow-xl transition-transform flex items-center gap-2"
          >
            <Sparkles className="w-5 h-5" /> Начать
          </button>
        </div>
      </main>

      {/* Декоративный центральный элемент */}
      <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-white/5 backdrop-blur-2xl blur-3xl animate-pulse pointer-events-none" />

      {/* Footer */}
      <footer className="absolute bottom-4 w-full text-center text-white/50 text-xs">
        &copy; 2025 MyGlassSite. Все права защищены.
      </footer>
    </div>
  );
};

export default WelcomePage;
