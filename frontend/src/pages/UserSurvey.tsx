import { useState } from 'react';
import logo from '../assets/donor_logo.jpg';
import { useMedotvodModal } from '../components/layouts/Medotvod';
import type { MedotvodData } from '../components/layouts/Medotvod';
import apiRequest from '../components/utils/apiRequest';

export default function UserSurvey() {
  const [fullname, setFullname] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [gender, setGender] = useState('');
  const [university, setUniversity] = useState('');
  const [group, setGroup] = useState('');
  const [weight, setWeight] = useState('');
  const [chronicDisease, setChronicDisease] = useState('');
  const [medicalExemption, setMedicalExemption] = useState<'yes' | 'no' | ''>('');
  const [donorEarlier, setDonorEarlier] = useState('');
  const [feedback, setFeedback] = useState('');

  const [medotvodInfo, setMedotvodInfo] = useState<MedotvodData | null>(null);
  console.log(medotvodInfo)
  const handleMedotvodSubmit = (data: MedotvodData) => {
    setMedotvodInfo(data);
  };

  const openMedotvodModal = useMedotvodModal(handleMedotvodSubmit);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const nameParts = fullname.trim().split(' ');
    const [surname = '', name = '', patronymic = ''] = nameParts;
    console.log(name)
    const body = {
      fullname,
      surname,
      patronymic,
      birth_date: birthDate,
      gender: gender === 'Мужской' ? 'MALE' : gender === 'Женский' ? 'FEMALE' : 'OTHER',
      university,
      group,
      weight: parseInt(weight, 10),
      chronic_disease: chronicDisease === 'Да',
      medical_exemption: medicalExemption === 'yes',
      donor_earlier:
        donorEarlier === 'Да, один раз'
          ? 'ONCE'
          : donorEarlier === 'Да, регулярно'
          ? 'REGULARLY'
          : 'NO',
      feedback
    };

    try {
      const response = await apiRequest({
        url: 'https://api.donor.vickz.ru/api/post-register',
        method: 'POST',
        body,
        auth: true,
      });

      if (response.ok) {
        window.location.href = '/#/main';
      } else {
        const errorData = await response.json();
        console.error('Ошибка при отправке:', errorData);
        alert('Не удалось отправить анкету. Проверьте данные.');
      }
    } catch (error) {
      console.error('Ошибка сети:', error);
      alert('Произошла ошибка при отправке анкеты.');
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen px-6 py-12">
      <img
        src={logo}
        alt="МИФИ"
        className="w-28 h-28 mb-8 drop-shadow-md animate-fade-in"
      />

      <h1 className="text-2xl font-semibold text-blue-700 mb-6 animate-fade-in">
        Первый шаг к донорству
      </h1>

      <form
        className="w-full max-w-md space-y-5 animate-fade-in-slow"
        onSubmit={handleSubmit}
      >
        <input
          type="text"
          placeholder="Фамилия Имя Отчество"
          value={fullname}
          onChange={(e) => setFullname(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <input
          type="date"
          placeholder="Дата рождения"
          value={birthDate}
          onChange={(e) => setBirthDate(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <select
          value={gender}
          onChange={(e) => setGender(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        >
          <option disabled value="">Пол</option>
          <option>Мужской</option>
          <option>Женский</option>
          <option>Предпочитаю не указывать</option>
        </select>

        <input
          type="text"
          placeholder="Факультет / Институт"
          value={university}
          onChange={(e) => setUniversity(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <input
          type="text"
          placeholder="Учебная группа"
          value={group}
          onChange={(e) => setGroup(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <input
          type="number"
          placeholder="Вес (кг)"
          min={0}
          max={1000}
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <select
          value={chronicDisease}
          onChange={(e) => setChronicDisease(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        >
          <option disabled value="">Есть ли хронические заболевания?</option>
          <option>Нет</option>
          <option>Да</option>
        </select>

        <fieldset className="border border-blue-300 rounded-xl p-4 shadow-sm">
          <legend className="text-gray-700 mb-2">Есть ли у вас медицинский отвод?</legend>
          <div className="flex space-x-6">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="medotvod"
                value="yes"
                checked={medicalExemption === 'yes'}
                onChange={() => setMedicalExemption('yes')}
                className="w-5 h-5 text-blue-600 focus:ring-blue-400"
              />
              <span>Да</span>
            </label>

            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="medotvod"
                value="no"
                checked={medicalExemption === 'no'}
                onChange={() => setMedicalExemption('no')}
                className="w-5 h-5 text-blue-600 focus:ring-blue-400"
              />
              <span>Нет</span>
            </label>
          </div>

          {medicalExemption === 'yes' && (
            <button
              type="button"
              onClick={openMedotvodModal}
              className="mt-4 px-5 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
            >
              Прикрепить медотвод
            </button>
          )}
        </fieldset>

        <select
          value={donorEarlier}
          onChange={(e) => setDonorEarlier(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        >
          <option disabled value="">Сдавали ли вы кровь раньше?</option>
          <option>Нет</option>
          <option>Да, один раз</option>
          <option>Да, регулярно</option>
        </select>

        <textarea
          placeholder="Есть ли что-то, что вы хотите сообщить организаторам?"
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          rows={3}
          className="w-full px-4 py-3 rounded-xl border border-blue-300 text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-400 shadow-sm"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl shadow-lg transition-all duration-300 mt-4"
        >
          Отправить анкету
        </button>
      </form>
    </div>
  );
}
