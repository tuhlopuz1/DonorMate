<h1 align="center">
  <img src="https://placehold.co/200x100?text=DonorMate+Logo" alt="DonorMate Logo" width="200"/>
  <br>DonorMate 🩸
</h1>

<h3 align="center">Telegram-бот для организации донорских мероприятий</h3>

<div align="center">
  <p>Для доноров и организаторов донорских акций</p>
</div>

## 📂 Структура репозитория

```plaintext
donormate/
├── backend/              # Бэкенд часть приложения
├── frontend-web/         # Фронтенд сайта
├── frontend-tg-bot/      # Фронтенд Telegram бота
├── nginx/                # Конфигурация Nginx
├── docker-compose.yml    # Конфигурация Docker Compose
└── .env.example          # Пример файла с переменными окружения```

## 🚀 Запуск проекта
Проект размещен на хостинге и готов к использованию. Для локального запуска:

```
docker-compose up --build
```

Перед запуском:

- Создайте .env файл на основе .env.example
- Заполните все необходимые переменные окружения
