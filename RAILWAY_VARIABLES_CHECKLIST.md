# 📋 Чек-лист переменных для Railway

## ✅ Обязательные переменные для Google Sheets API

Убедитесь, что в Railway Dashboard → Settings → Variables установлены **ТОЧНО** эти переменные:

### 1. Основные переменные
```
GOOGLE_SHEET_ID=ваш_id_таблицы_здесь
GOOGLE_SHEET_NAME=Sheet1
```

### 2. Service Account переменные (из JSON файла)
```
GOOGLE_PROJECT_ID=ваш_project_id
GOOGLE_PRIVATE_KEY_ID=ваш_private_key_id
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nваш_private_key\n-----END PRIVATE KEY-----\n"
GOOGLE_CLIENT_EMAIL=ваш_client_email@project.iam.gserviceaccount.com
GOOGLE_CLIENT_ID=ваш_client_id
GOOGLE_CLIENT_X509_CERT_URL=ваш_client_x509_cert_url
```

## ⚠️ Важные моменты:

### 1. GOOGLE_PRIVATE_KEY
- **ОБЯЗАТЕЛЬНО** используйте кавычки
- **ОБЯЗАТЕЛЬНО** используйте `\n` для переносов строк
- **НЕ** используйте реальные переносы строк в Railway

### 2. GOOGLE_CLIENT_EMAIL
- Должен заканчиваться на `@project.iam.gserviceaccount.com`
- Найти в JSON файле Service Account

### 3. GOOGLE_SHEET_ID
- Взять из URL таблицы: `https://docs.google.com/spreadsheets/d/ЭТО_ВАШ_ID/edit`
- **НЕ** включать `/edit` в ID

## 🔍 Проверка в Railway:

1. **Зайдите в Railway Dashboard**
2. **Выберите ваш проект**
3. **Settings → Variables**
4. **Убедитесь, что все 7 переменных установлены**
5. **Перезапустите приложение**

## 🧪 Тест после настройки:

Запустите команду `/post` в Telegram - посты должны появиться в Google Sheets.

## ❌ Частые ошибки:

1. **Неправильный формат GOOGLE_PRIVATE_KEY** - нужны кавычки и `\n`
2. **Неправильный GOOGLE_SHEET_ID** - включен `/edit` в конце
3. **Неправильный GOOGLE_CLIENT_EMAIL** - не тот email из JSON
4. **Отсутствие доступа** - Service Account не добавлен в таблицу
5. **Неправильные права** - Service Account должен быть "Редактор"
