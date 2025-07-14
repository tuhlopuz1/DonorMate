import BottomNavBar from "../components/layouts/NavBar";
import EventCard from "../components/layouts/EventCard";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiCalendar } from "react-icons/fi";


const SchedulePage = () => {
    return (
        <div className="pt-14 pb-14">

        <PageTopBar 
        title="Расписание мероприятий"
        icon={<FiCalendar size={20}/>}
        />

         <div className="flex flex-col gap-6 p-6">
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
            <EventCard
                title="День донора"
                date="2025-07-20"
                timeRange="13:00–15:00"
                location="Актовый зал, корпус Б"
                spotsLeft={0}
                totalSpots={30}
                description="Ежегодная донорская акция. При себе иметь паспорт и СНИЛС."
                isRegistered={false}
            />
            <EventCard
                title="День донора"
                date="2025-07-20"
                timeRange="13:00–15:00"
                location="Актовый зал, корпус Б"
                spotsLeft={1}
                totalSpots={30}
                description="Ежегодная донорская акция. При себе иметь паспорт и СНИЛС."
                isRegistered={true}
            />
            <EventCard
                title="День донора"
                date="2025-07-20"
                timeRange="13:00–15:00"
                location="Актовый зал, корпус Б"
                spotsLeft={1}
                totalSpots={30}
                description="Ежегодная донорская акция. При себе иметь паспорт и СНИЛС. и снилс и снилс и снилс и снилс"
                isRegistered={false}
            />
        </div>
            
            
            <BottomNavBar  />
        </div>
    )
}

export default SchedulePage