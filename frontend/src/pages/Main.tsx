import { useEffect, useState} from "react";
import BottomNavBar from "../components/layouts/NavBar";
import MainTopBar from "../components/layouts/MainTopBar";
import { FiFileText } from "react-icons/fi";
// import { useMedotvodModal } from '../components/layouts/Medotvod';
// import type { MedotvodData } from '../components/layouts/Medotvod';
import EventCard from "../components/layouts/EventCard";
import { MessageCircleQuestion, Info } from "lucide-react";
import apiRequest from "../components/utils/apiRequest";

interface UserProfile {
  fsp: string
  donations: number
  phone: number
}

const MainPage = () => {
    const [user, setUser] = useState<UserProfile | null>(null);
    const [loadingUser, setLoadingUser] = useState(true);
    // const handleMedotvodSubmit = (data: MedotvodData) => {
    //     console.log("Медотвод получен:", data);

    //   };
    
    //   const openMedotvodModal = useMedotvodModal(handleMedotvodSubmit);
    useEffect(() => {
        const fetchUserProfile = async () => {
        try {
            const res = await apiRequest({
            url: "https://api.donor.vickz.ru/api/profile",
            method: "GET",
            auth: true,
            });

            if (!res.ok) throw new Error("Ошибка при получении профиля");
            const data: UserProfile = await res.json();
            localStorage.setItem('phone', data.phone.toString())
            setUser(data);
        } catch (error) {
            console.error("Ошибка загрузки профиля:", error);
        } finally {
            setLoadingUser(false);
        }
        }
        fetchUserProfile();
    }, []
    );



    return (
        <div className="pt-14 pb-14 flex flex-col gap-6">
            <MainTopBar />
            <div>
            {loadingUser ? 
            (<p className="text-2xl bg-blue-600 font-sans font-bold"> Загрузка...
                </p>)
                :
            (
                <div className="h-auto bg-blue-600 p-6">
                    <p className="text-2xl text-white font-sans font-bold"> {"Привет, " + user?.fsp + "!"}
                </p>
                    <div className="flex flex-col items-center bg-blue-400/50 rounded-xl my-6 pt-8">
                        <h1 className="text-4xl font-sans font-bold text-white">{user?.donations}</h1>
                        <p className="text-white/75 pb-8">донаций</p>
                    </div>
                </div>)
            }
            </div>

                <div>
                   <p className="text-2xl text-black px-5 font-sans font-bold">Быстрые действия</p>
                <div onClick={() => {window.location.href = '/#/add-medotvod'}} className="flex items-center justify-between px-6 bg-orange-400 h-20 m-4 rounded-lg">
                    <p className="text-white">Добавить медицинский отвод</p>
                    <FiFileText color="white"/>
                </div>
                {/* <div  className="flex items-center justify-between px-6 bg-blue-600 h-20 m-4 rounded-lg">
                    <p className="text-white">Расписание мероприятий</p>
                    <FiCalendar color="white"/>
                </div> */}

                    <div onClick={() => {window.location.href = '/#/donorship'}} className="flex items-center justify-between px-6 bg-green-600 h-20 m-4 text-white rounded-lg">
                        <p>Больше о донорстве</p>
                        <Info size={17}/>
                    </div>
                    <div onClick={() => {window.location.href = '/#/ask-organizers'}} className="flex items-center justify-between px-6 bg-purple-600 h-20 m-4 text-white rounded-lg">
                        <p>Вопрос организаторам</p>
                        <MessageCircleQuestion size={17}/>
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