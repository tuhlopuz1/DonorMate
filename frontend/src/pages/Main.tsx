import BottomNavBar from "../components/layouts/NavBar";
import MainTopBar from "../components/layouts/MainTopBar";
import { FiCalendar, FiFileText } from "react-icons/fi";
import { useMedotvodModal } from '../components/layouts/Medotvod';
import type { MedotvodData } from '../components/layouts/Medotvod';
import EventCard from "../components/layouts/EventCard";


const MainPage = () => {

    
      const handleMedotvodSubmit = (data: MedotvodData) => {
        console.log("Медотвод получен:", data);
        // Сюда отправку на сервер
      };
    
      const openMedotvodModal = useMedotvodModal(handleMedotvodSubmit);


    return (
        <div className="pt-14 pb-20 flex flex-col gap-6">
            <MainTopBar />

            <div className="h-auto bg-blue-600 p-6">
                <p className="text-2xl text-white font-sans font-bold">Привет, Никитин Владимир!</p>
                <div className="flex flex-col items-center bg-blue-400/50 rounded-xl my-6 pt-8">
                    <h1 className="text-4xl font-sans font-bold text-white">7</h1>
                    <p className="text-white/75 pb-8">донаций</p>
                </div>
            </div>

            <div>
                <p className="text-2xl text-black px-5 font-sans font-bold">Быстрые действия</p>
                <div onClick={openMedotvodModal} className="flex items-center justify-between px-6 bg-orange-400 h-20 m-4 rounded-lg">
                    <p className="text-white">Добавить медицинский отвод</p>
                    <FiFileText color="white"/>
                </div>
                <div onClick={() => {window.location.href = '/#/schedule'}} className="flex items-center justify-between px-6 bg-blue-600 h-20 m-4 rounded-lg">
                    <p className="text-white">Расписание мероприятий</p>
                    <FiCalendar color="white"/>
                </div>
            </div>


            <div className="px-5">
                <p className="text-2xl text-black font-sans font-bold mb-3">Ближайшее мероприятие</p>
                <EventCard
                    title="День донора"
                    date="2025-07-20"
                    timeRange="13:00–15:00"
                    location="Актовый зал, корпус Б"
                    spotsLeft={1}
                    totalSpots={30}
                    description="Ежегодная донорская акция. При себе иметь паспорт и СНИЛС."
                    isRegistered={false}
                />
            </div>


            <BottomNavBar />
        </div>
    )
}

export default MainPage