
import logo from "../../assets/donor_day.jpg"

export default function AdminMainTopBar() {
  return (
    <header className="fixed top-0 left-0 z-50 w-full bg-red-500 text-white px-4 py-2 flex items-center justify-between shadow-md">
      <div className="flex items-center space-x-3">

        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
          <img src={logo} className="rounded-full"></img>
        </div>
        <h1 className="text-xl font-semibold">Панель организатора</h1>
      </div>


    </header>
  );
}
