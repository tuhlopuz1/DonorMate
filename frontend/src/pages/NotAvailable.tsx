export default function NotAvailable() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 px-4">
      <div className="bg-white shadow-xl rounded-2xl p-6 text-center max-w-md w-full">
        <h1 className="text-2xl font-semibold text-red-600 mb-4">
          Это приложение доступно только из Telegram WebApp
        </h1>
        <p className="text-gray-700 mb-4">
          Пожалуйста, откройте это приложение через Telegram на мобильном устройстве или в Telegram Web.
        </p>
        <a
          href="https://t.me/MEPHIDonorBot"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition duration-300"
        >
          @MEPHIDonorBot
        </a>
      </div>
    </div>
  );
}
