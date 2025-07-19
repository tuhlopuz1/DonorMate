import React, { useEffect, useState } from "react";
import { FiTrendingUp } from "react-icons/fi";
import apiRequest from "../utils/apiRequest"; // убедись, что путь корректен

interface Donor {
  fsp: string;
  donations: number;
}

const TopDonors: React.FC = () => {
  const [donors, setDonors] = useState<Donor[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchDonors = async () => {
    setLoading(true);
    try {
      const response = await apiRequest({
        url: "https://api.donor.vickz.ru/api/get-top-donors",
        auth: true,
      });

      if (!response.ok) {
        throw new Error("Ошибка при получении данных о донорах");
      }

      const data = await response.json();
      // Фильтруем и сортируем по количеству донаций
      const filteredData: Donor[] = data
        .filter((donor: any) => donor.donations > 0)
        .sort((a: any, b: any) => b.donations - a.donations)
        .map((donor: any, index: number) => ({
          i: index,
          fsp: donor.fsp || "Неизвестно",
          donations: donor.donations,
        }));

      setDonors(filteredData.slice(0, 10)); // топ-10
    } catch (error) {
      console.error("Ошибка загрузки доноров:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDonors();
  }, []);

  return (
    <div className="p-4 bg-white rounded-xl shadow-md w-full max-w-md border">
      <div className="flex items-center text-lg font-semibold mb-4">
        <FiTrendingUp size={20} className="m-3" />
        Топ доноров
      </div>

      {loading ? (
        <div className="text-sm text-gray-500">Загрузка...</div>
      ) : donors.length === 0 ? (
        <div className="text-sm text-gray-500">Нет данных</div>
      ) : (
        donors.map((donor, index) => (
          <div
            key={index}
            className="flex items-center justify-between mb-3"
          >
            <div className="flex items-center">
              <div className="w-8 h-8 bg-red-100 text-red-500 font-bold rounded-full flex items-center justify-center mr-3">
                {index + 1}
              </div>
              <div className="text-sm font-semibold">
                {donor.fsp}
              </div>
            </div>
            <div className="text-right text-sm font-semibold">
              {donor.donations} донаций
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default TopDonors;
