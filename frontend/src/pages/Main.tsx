import BottomNavBar from "../components/layouts/NavBar";
import MainTopBar from "../components/layouts/MainTopBar";


const MainPage = () => {
    return (
        <div className="pt-14 pb-14 flex flex-col gap-6">
            <MainTopBar />

            <div className="h-auto bg-blue-600 p-6">
                <p className="text-2xl text-white font-sans font-bold">Привет, Никитин Владимир!</p>
                <div className="flex flex-col items-center bg-blue-400/50 rounded-xl my-6 pt-8">
                    <h1 className="text-4xl font-sans font-bold text-white">7</h1>
                    <p className="text-white/75 pb-8">донаций</p>
                </div>
            </div>

            <div>
                <p className="text-2xl text-black px-4 font-sans font-bold">Быстрые действия</p>



            </div>



            <BottomNavBar />
        </div>
    )
}

export default MainPage