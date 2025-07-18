import React, { useState } from "react";

const categories = [
  {
    id: "registered_dd",
    label: "Зарегистрированы на ближайший ДД",
  },
  {
    id: "not_registered_dd",
    label: "В базе, но не зарегистрированы",
  },
  {
    id: "no_show",
    label: "Зарегистрировались, но не пришли",
  },
  {
    id: "dkm_registered",
    label: "Сдали пробирку на ДКМ",
  },
];

const Broadcasts: React.FC = () => {
  const [message, setMessage] = useState("");
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

  const toggleCategory = (id: string) => {
    setSelectedCategories((prev) =>
      prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id]
    );
  };

  const handleSend = () => {
    if (!message.trim() || selectedCategories.length === 0) {
      alert("Введите сообщение и выберите хотя бы одну категорию");
      return;
    }

    console.log("Рассылка отправлена", {
      message,
      categories: selectedCategories,
    });

    alert("Рассылка отправлена!");
    setMessage("");
    setSelectedCategories([]);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-semibold mb-6">Рассылки</h1>

      {/* Card: Категории */}
      <div className="bg-white shadow-md rounded-xl mb-6">
        <div className="p-4">
          <h2 className="text-xl font-medium mb-4">Кому отправить?</h2>
          <div className="grid gap-4">
            {categories.map((category) => (
              <div key={category.id} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id={category.id}
                  checked={selectedCategories.includes(category.id)}
                  onChange={() => toggleCategory(category.id)}
                  className="w-5 h-5 accent-blue-600"
                />
                <label htmlFor={category.id} className="text-sm">
                  {category.label}
                </label>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Card: Сообщение */}
      <div className="bg-white shadow-md rounded-xl mb-6">
        <div className="p-4">
          <h2 className="text-xl font-medium mb-4">Сообщение</h2>
          <textarea
            placeholder="Введите текст рассылки..."
            className="w-full min-h-[120px] p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>
      </div>

      {/* Button */}
      <div className="text-right">
        <button
          onClick={handleSend}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg text-lg transition"
        >
          Отправить
        </button>
      </div>
    </div>
  );
};

export default Broadcasts;
