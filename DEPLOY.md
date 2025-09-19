# Деплой на Railway

## 1. Создайте проект на Railway

1. Перейдите на [railway.app](https://railway.app)
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Найдите ваш репозиторий
5. Нажмите "Deploy Now"

## 2. Настройте переменные окружения

В Railway Dashboard → Settings → Variables добавьте:

```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHANNEL_ID=@ваш_канал
ADMIN_CHAT_ID=ваш_chat_id
GOOGLE_SHEET_ID=ваш_sheet_id
OPENROUTER_API_KEY=ваш_api_key
```

## 3. Проверьте работу

После деплоя система будет работать автоматически.
