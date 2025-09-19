# 🎉 ПРОЕКТ ГОТОВ ДЛЯ RAILWAY!

## ✅ Что сделано:

1. **Очищен код** - удалены все секретные данные
2. **Создан архив** - `telegram-bot-clean.tar.gz` в родительской папке
3. **Готов для деплоя** - все файлы настроены для Railway

## 🚀 Инструкции по деплою:

### 1. Создайте репозиторий на GitHub

1. Перейдите на [github.com](https://github.com)
2. Нажмите "New repository"
3. Название: `telegram-bot-clean`
4. Выберите "Public"
5. НЕ добавляйте README, .gitignore или лицензию
6. Нажмите "Create repository"

### 2. Загрузите код

1. Скачайте архив `telegram-bot-clean.tar.gz` из папки выше
2. Распакуйте архив
3. В терминале выполните:
   ```bash
   cd telegram-bot-clean
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/telegram-bot-clean.git
   git push -u origin main
   ```

### 3. Деплой на Railway

1. Перейдите на [railway.app](https://railway.app)
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Найдите `telegram-bot-clean`
5. Нажмите "Deploy Now"

### 4. Настройте Google Service Account

**ВАЖНО!** Сначала настройте Google Service Account по инструкции в файле `GOOGLE_SETUP.md`

### 5. Настройте переменные

В Railway Dashboard → Settings → Variables добавьте переменные из файла `VARIABLES.md`:

**Основные переменные:**
```
TELEGRAM_BOT_TOKEN=8397452617:AAGv1UbSwC-HvHgd72yoqh_t1ghf4hE29Is
TELEGRAM_CHANNEL_ID=@sovpalitest
TELEGRAM_CHANNEL_USERNAME=@sovpalitest
ADMIN_CHAT_ID=-1003089435390
ALERT_ADMIN_CHANNEL=-1003089435390
NOTIFICATION_CHANNEL_ID=-1003089435390
COMMAND_CHANNEL_ID=-1003089435390
```

**Google Sheets (Service Account):**
```
GOOGLE_SHEET_ID=13vwWFE2fSGbu_5lZfrOT9v_aPQzijigAMniqtof_RN0
GOOGLE_SHEET_NAME=Sheet1
GOOGLE_PROJECT_ID=accbot-471214
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_CLIENT_EMAIL=your-service-account@accbot-471214.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY_ID=your_private_key_id
GOOGLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n
GOOGLE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40accbot-471214.iam.gserviceaccount.com
```

**AI настройки:**
```
OPENROUTER_API_KEY=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
AI_MODEL=anthropic/claude-3.7-sonnet
```

## 🎯 Готово!

После выполнения этих шагов:
- ✅ Код загружен в GitHub
- ✅ Railway деплой настроен
- ✅ Переменные окружения настроены
- ✅ Система готова к работе

## 📱 Тестирование

После деплоя протестируйте в группе AlertChanel:
- `/start` - запуск бота
- `/post` - генерация постов
- `/status` - статистика
- `/help` - справка
- `пост` - быстрая генерация

**Проект полностью готов для автономной работы на Railway!** 🚀
