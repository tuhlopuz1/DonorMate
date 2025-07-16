import React, { useEffect, useState } from "react";
import { FiTrendingUp } from "react-icons/fi";


interface Donor {
  rank: number;
  name: string;
  username: string;
  donations: number;
}

const TopDonors: React.FC = () => {
  const [donors, setDonors] = useState<Donor[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Заглушка для получения данных
  const fetchDonors = async () => {
    setLoading(true);
    await new Promise((res) => setTimeout(res, 1000)); // имитация запроса
    const fakeData: Donor[] = [
      {
        rank: 1,
        name: "Александра Петрова",
        username: "MGTU2024001",
        donations: 8,
      },
      {
        rank: 2,
        name: "Иван Сидоров",
        username: "MGTU2024012",
        donations: 6,
      },
      {
        rank: 3,
        name: "Мария Смирнова",
        username: "MGTU2024055",
        donations: 5,
      },
    ];
    setDonors(fakeData);
    setLoading(false);
  };

  useEffect(() => {
    fetchDonors();
  }, []);

  return (
    <div className="p-4 bg-white rounded-xl shadow-md w-full max-w-md border">
      <div className="flex items-center text-lg font-semibold mb-4">
        <FiTrendingUp size={20} className="m-3"/>
        Топ доноров
      </div>

      {loading ? (
        <div className="text-sm text-gray-500">Загрузка...</div>
      ) : (
        donors.map((donor) => (
          <div
            key={donor.rank}
            className="flex items-center justify-between mb-3"
          >
            <div className="flex items-center">
              <div className="w-8 h-8 bg-red-100 text-red-500 font-bold rounded-full flex items-center justify-center mr-3">
                {donor.rank}
              </div>
              <div>
                <div className="text-sm font-semibold">{donor.name}</div>
                <div className="text-xs text-gray-500">{donor.username}</div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm font-semibold">
                {donor.donations} донаций
              </div>
           </div>
          </div>
        ))
      )}
    </div>
  );
};

export default TopDonors;
