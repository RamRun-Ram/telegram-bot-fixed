# Telegram Automation Bot

Автоматизированная система для публикации постов в Telegram-канал с использованием ИИ.

## Возможности

- 🤖 Автоматическая генерация постов с помощью Claude 3.7 Sonnet
- 📊 Интеграция с Google Sheets для хранения постов
- ⏰ Автоматическая публикация по расписанию
- 💬 Управление через команды в Telegram группе
- 🚀 Готов для деплоя на Railway

## Установка

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Настройте переменные окружения
4. Запустите: `python run_full_system.py`

## Переменные окружения

Создайте файл `.env` с переменными:

```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_channel
ADMIN_CHAT_ID=your_admin_chat_id
GOOGLE_SHEET_ID=your_sheet_id
OPENROUTER_API_KEY=your_api_key
```

## Деплой на Railway

1. Создайте проект на Railway
2. Подключите GitHub репозиторий
3. Настройте переменные окружения
4. Деплойте

## Команды

- `/start` - запуск бота
- `/post` - генерация постов
- `/status` - статистика
- `/help` - справка