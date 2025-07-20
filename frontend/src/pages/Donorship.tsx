import React from "react";
import logo from '../assets/MEPHI_logo.png';
import '../index.css';

const Donorship: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-12">
        
        {/* Назад кнопка */}
        <div className="flex justify-center sm:justify-end animate-fade-in-up delay-100">
          <button 
            onClick={() => {window.location.href = '/#/main'}} 
            className="inline-flex items-center px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white text-base sm:text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            Назад
          </button>
        </div>

        {/* Заголовок */}
        <div className="text-center animate-fade-in">
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-blue-800 mb-6 tracking-tight">
            О донорстве
          </h1>
          <div className="w-20 sm:w-24 h-2 bg-blue-600 mx-auto mb-6 rounded-full"></div>
        </div>

        {/* Основной контент */}
        <div className="bg-white rounded-xl shadow-lg p-6 sm:p-8 animate-fade-in-up-10 space-y-8">

          {/* Логотип и вступление */}
          <div className="flex flex-col sm:flex-row items-center gap-6">
            <img
              src={logo}
              alt="МИФИ"
              className="w-32 h-32 object-contain drop-shadow-md animate-fade-in"
            />
            <p className="text-base sm:text-lg text-gray-700 leading-relaxed">
              Донорство крови и костного мозга — это шанс подарить жизнь. Каждая донация может спасти нескольких человек. Ниже — все, что нужно знать будущему донору.
            </p>
          </div>

          {/* Требования к донорам */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">1. Требования к донорам</h2>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Возраст: от 18 лет</li>
              <li>Вес: не менее 50 кг</li>
              <li>Температура тела не выше 37°C</li>
              <li>Давление: 90–160/60–100 мм рт. ст.</li>
              <li>Гемоглобин: ≥120 г/л для женщин, ≥130 г/л для мужчин</li>
              <li>Отсутствие острых хронических заболеваний</li>
              <li>Не болели ОРВИ, ангиной, гриппом менее месяца назад</li>
              <li>Цельная кровь: мужчины – до 5 раз/год, женщины – до 4 раз/год</li>
            </ul>
          </section>

          {/* Подготовка к донации */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">2. Подготовка к донации</h2>
            <p className="text-gray-700 font-semibold">За 2–3 дня:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1 mb-2">
              <li>Исключить жирное, острое, копчености, фастфуд, молочные продукты, яйца</li>
              <li>Отказ от алкоголя (за 48 ч), отмена лекарств (за 72 ч)</li>
              <li>Избегать сильных физических нагрузок</li>
            </ul>
            <p className="text-gray-700 font-semibold">Накануне:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1 mb-2">
              <li>Легкий ужин до 20:00</li>
              <li>Сон не менее 8 часов</li>
            </ul>
            <p className="text-gray-700 font-semibold">Утром:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Обязательный завтрак: каша на воде, сладкий чай, сухари</li>
              <li>Не курить минимум 1 час до донации</li>
            </ul>
          </section>

          {/* Рацион донора */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">3. Рацион донора за 2–3 дня до донации</h2>
            <p className="text-gray-700 mb-2">Пейте 1.5–2 л воды в день (вода, морсы, компоты).</p>
            <p className="text-gray-700 font-semibold">Рекомендуется:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1 mb-2">
              <li>Крупы на воде</li>
              <li>Отварное нежирное мясо и белая рыба</li>
              <li>Овощи и фрукты (не все)</li>
            </ul>
            <p className="text-gray-700 font-semibold">Запрещено:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Жирное мясо, молочные продукты, яйца, орехи</li>
              <li>Фастфуд, майонез, копчености</li>
              <li>Цитрусовые, бананы, виноград, клубника, шпинат, свекла</li>
            </ul>
          </section>

          {/* Противопоказания */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">4–5. Противопоказания</h2>
            <p className="text-gray-700 font-semibold">Абсолютные:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1 mb-2">
              <li>ВИЧ, гепатиты B/C, сифилис, туберкулез</li>
              <li>Онкология, заболевания крови</li>
              <li>Болезни сердца, сосудов, ЦНС</li>
              <li>Бронхиальная астма, паразитарные инфекции</li>
            </ul>
            <p className="text-gray-700 font-semibold">Временные:</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>ОРВИ, ангина – 1 месяц</li>
              <li>Удаление зуба – 10 дней</li>
              <li>Менструация – +5 дней</li>
              <li>Тату/пирсинг – до 12 месяцев</li>
              <li>Прививки – 1 месяц</li>
              <li>Антибиотики – 2 недели, анальгетики – 3 дня</li>
            </ul>
          </section>

          {/* Донорство костного мозга */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">6–7. Донорство костного мозга</h2>
            <p className="text-gray-700 mb-2">
              Более 5 000 человек ежегодно нуждаются в трансплантации костного мозга. Только 30–40% находят донора среди родственников. Регистр ФРДКМ в России насчитывает ~200 000 человек (2024), в Германии — 9 млн, в США — 12 млн.
            </p>
            <p className="text-gray-700 font-semibold">Как вступить в регистр:</p>
            <ol className="list-decimal list-inside text-gray-700 space-y-1 mb-2">
              <li>{"Заполнение анкеты: 18–45 лет, >50 кг, нет противопоказаний"}</li>
              <li>Сдача крови (10 мл) или мазка с щеки</li>
              <li>HLA-типирование, данные вносятся в регистр</li>
              <li>Ожидание совпадения (2–10 лет), подтверждение, обследование, донация</li>
            </ol>
          </section>

          {/* Способы сдачи костного мозга */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">8. Способы сдачи костного мозга</h2>
            <p className="text-gray-700 font-semibold">Периферический способ (80% случаев):</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1 mb-2">
              <li>5 дней подготовки</li>
              <li>Забор стволовых клеток через аппарат афереза (4–6 ч)</li>
              <li>Восстановление: 1–2 дня</li>
            </ul>
            <p className="text-gray-700 font-semibold">Пункция костного мозга (20% случаев):</p>
            <ul className="list-disc list-inside text-gray-700 space-y-1">
              <li>Забор под наркозом из костей таза (500–1000 мл)</li>
              <li>Длительность: 1–1.5 ч, восстановление: 3–7 дней</li>
            </ul>
          </section>

          {/* Процедура сдачи крови в МИФИ */}
          <section>
            <h2 className="text-xl sm:text-2xl font-semibold text-blue-700 mb-4">9. Как проходит донация в МИФИ</h2>
            <ol className="list-decimal list-inside text-gray-700 space-y-1">
              <li>Прибытие в студенческий офис</li>
              <li>Регистрация, заполнение анкеты, получение бахил</li>
              <li>Медобследование: терапевт (давление), лаборант (анализ из пальца)</li>
              <li>Сдача крови: 450 мл, одноразовый комплект, длительность 10–15 мин</li>
              <li>Перекус и отдых, выбор сувенира</li>
              <li>Выдача справки (2 дня отдыха) и компенсации питания</li>
            </ol>
          </section>

        </div>
      </div>
    </div>
  );
};

export default Donorship;
