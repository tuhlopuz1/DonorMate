<h1 align="center">
  <img src="frontend\src\assets\donor_logo_bad.jpg" alt="DonorMate Logo" width="200"/>
  <br>DonorMate
</h1>

<h3 align="center">Telegram-бот для организации донорских мероприятий</h3>

<div align="center">
  <p>Для доноров и организаторов донорских акций</p>
</div>

## 📂 Структура репозитория

```plaintext
donormate/
├── backend/              # Бэкенд часть приложения
├── frontend/             # Фронтенд WebApp приложения
├── bot/                  # Фронтенд Telegram бота
├── config/               # Конфигурация Nginx и Конфигурация Docker Compose
└── .env.example/         # Пример файла с переменными окружения
```
## 🚀 Запуск проекта
Проект размещен на хостинге и готов к использованию. Для локального запуска:

```plaintext
docker-compose up --build
```

# Перед запуском:

- Создайте .env файл на основе .env.example
- Заполните все необходимые переменные окружения
