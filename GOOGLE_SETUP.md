# 🔧 Настройка Google Service Account для Railway

## Проблема
Railway не поддерживает OAuth аутентификацию с браузером. Нужно использовать Service Account.

## Решение

### 1. Создайте Service Account в Google Cloud Console

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Выберите проект `accbot-471214`
3. Перейдите в "IAM & Admin" → "Service Accounts"
4. Нажмите "Create Service Account"
5. Название: `railway-bot-service`
6. Описание: `Service account for Railway bot`
7. Нажмите "Create and Continue"

### 2. Настройте права доступа

1. В разделе "Grant this service account access to the project"
2. Роль: `Editor` или `Google Sheets API User`
3. Нажмите "Continue" → "Done"

### 3. Создайте ключ

1. Найдите созданный Service Account
2. Нажмите на него
3. Перейдите в "Keys" → "Add Key" → "Create new key"
4. Тип: JSON
5. Нажмите "Create"
6. Скачается JSON файл

### 4. Извлеките данные из JSON

Откройте скачанный JSON файл и найдите:

```json
{
  "type": "service_account",
  "project_id": "accbot-471214",
  "private_key_id": "YOUR_PRIVATE_KEY_ID",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "railway-bot-service@accbot-471214.iam.gserviceaccount.com",
  "client_id": "YOUR_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/railway-bot-service%40accbot-471214.iam.gserviceaccount.com"
}
```

### 5. Настройте переменные в Railway

В Railway Dashboard → Settings → Variables добавьте:

```
GOOGLE_PROJECT_ID=accbot-471214
GOOGLE_CLIENT_ID=YOUR_CLIENT_ID
GOOGLE_CLIENT_EMAIL=railway-bot-service@accbot-471214.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY_ID=YOUR_PRIVATE_KEY_ID
GOOGLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n
GOOGLE_CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/railway-bot-service%40accbot-471214.iam.gserviceaccount.com
```

### 6. Предоставьте доступ к Google Sheets

1. Откройте вашу Google Таблицу
2. Нажмите "Поделиться"
3. Добавьте email: `railway-bot-service@accbot-471214.iam.gserviceaccount.com`
4. Права: "Редактор"
5. Нажмите "Отправить"

## ✅ Готово!

После настройки Service Account:
- ✅ Railway сможет работать с Google Sheets
- ✅ Не будет ошибок с браузером
- ✅ Система заработает автономно
