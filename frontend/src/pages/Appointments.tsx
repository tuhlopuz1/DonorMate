import BottomNavBar from "../components/layouts/NavBar";
import PageTopBar from "../components/layouts/PageTopBar";
import { FiClipboard } from "react-icons/fi";
import EventCard from "../components/layouts/EventCard"; // Убедись, что путь корректный

const AppointmentsPage = () => {
  return (
    <>
      <PageTopBar title="Мои записи" icon={<FiClipboard size={20} />} />

      <div className="p-4 space-y-4 pb-24 py-20"> {/* Добавил отступ снизу под навбар */}


        <EventCard
          title="123123123123"
          date="2025-08-02"
          timeRange="14:00 - 16:00"
          location="123123123"
          description="12313123123"
          spotsLeft={20}
          totalSpots={30}
          isRegistered={true}
        />
      </div>

      <BottomNavBar />
    </>
  );
};

export default AppointmentsPage;