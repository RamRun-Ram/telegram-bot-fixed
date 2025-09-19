# 📊 Настройка Google Sheets API для Railway

## ❌ Проблема
Google Sheets API не настроен в Railway, поэтому посты генерируются, но не загружаются в таблицу.

## ✅ Решение

### 1. Создайте Service Account в Google Cloud Console

1. **Зайдите в Google Cloud Console**: https://console.cloud.google.com/
2. **Выберите ваш проект** (или создайте новый)
3. **Перейдите в IAM & Admin → Service Accounts**
4. **Создайте новый Service Account**:
   - Название: `telegram-bot-sheets`
   - Описание: `Service account for Telegram bot Google Sheets integration`
5. **Создайте ключ**:
   - Выберите Service Account → Keys → Add Key → Create new key
   - Тип: JSON
   - Скачайте файл

### 2. Настройте доступ к Google Sheets

1. **Создайте Google Sheets таблицу**:
   - Перейдите на https://sheets.google.com/
   - Создайте новую таблицу
   - Скопируйте ID из URL: `https://docs.google.com/spreadsheets/d/ВАШ_ID_ТАБЛИЦЫ/edit`

2. **Предоставьте доступ Service Account**:
   - Откройте таблицу
   - Нажмите "Поделиться" (Share)
   - Добавьте email Service Account (из JSON файла)
   - Права: "Редактор" (Editor)

### 3. Настройте переменные в Railway

Добавьте эти переменные в Railway Dashboard → Settings → Variables:

```bash
# ID вашей Google Sheets таблицы
GOOGLE_SHEET_ID=ваш_id_таблицы_здесь

# Данные из JSON файла Service Account
GOOGLE_PROJECT_ID=ваш_project_id
GOOGLE_PRIVATE_KEY_ID=ваш_private_key_id
GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nваш_private_key\n-----END PRIVATE KEY-----\n"
GOOGLE_CLIENT_EMAIL=ваш_client_email
GOOGLE_CLIENT_ID=ваш_client_id
GOOGLE_CLIENT_X509_CERT_URL=ваш_client_x509_cert_url
```

### 4. Формат переменных

**GOOGLE_PRIVATE_KEY** должен быть в таком формате:
```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
-----END PRIVATE KEY-----
```

**Важно**: Используйте кавычки и `\n` для переносов строк!

### 5. Проверка

После настройки переменных:
1. **Перезапустите приложение** в Railway
2. **Попробуйте команду** `/post`
3. **Проверьте Google Sheets** - должны появиться посты

## 🔧 Альтернативное решение (временно)

Если не хотите настраивать Google Sheets сейчас, система будет работать с заглушкой:
- Посты генерируются
- Логируются в консоль
- НЕ загружаются в таблицу

## 📋 Структура таблицы

Таблица должна иметь колонки:
- **A**: Date (дата)
- **B**: Time (время)  
- **C**: Text (текст поста)
- **D**: Image URLs (ссылки на изображения)
- **E**: Status (статус: Ожидает/Опубликовано/Ошибка)

## 🚨 Безопасность

- **НЕ добавляйте** JSON файл Service Account в репозиторий
- **Используйте только** переменные окружения
- **Ограничьте права** Service Account только к нужной таблице
