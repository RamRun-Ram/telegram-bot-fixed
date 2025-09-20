"""
Конфигурационный файл для автоматизации публикаций в Telegram-канал
"""
import os
from typing import Dict, Any

# Telegram Bot настройки
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "-1002907282373")  # Основной канал для постов
TELEGRAM_CHANNEL_USERNAME = os.getenv("TELEGRAM_CHANNEL_USERNAME", "@sovpalitest")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "-1003089435390")  # Группа для уведомлений об ошибках
ALERT_ADMIN_CHANNEL = os.getenv("ALERT_ADMIN_CHANNEL", "-1003089435390")  # Группа AlertChanel для команд
NOTIFICATION_CHANNEL_ID = os.getenv("NOTIFICATION_CHANNEL_ID", "-1003089435390")  # Группа для системных уведомлений
COMMAND_CHANNEL_ID = os.getenv("COMMAND_CHANNEL_ID", "-1003089435390")  # Группа для команд (тот же что и уведомления)

# Google Sheets настройки
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "YOUR_GOOGLE_SHEET_ID")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")

# Google Service Account настройки (для Railway)
# Эти переменные нужно настроить в Railway Dashboard

# AI настройки
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "google/gemini-2.5-flash-lite-preview-06-17")

# Настройки расписания проверок (время по МСК)
# Проверяем каждый час с 8:01 до 22:01 (не проверяем с 23:00 до 7:00)
CHECK_TIMES = [
    "08:01", "09:01", "10:01", "11:01", "12:01", "13:01", "14:01", 
    "15:01", "16:01", "17:01", "18:01", "19:01", "20:01", "21:01", "22:01"
]
CHECK_INTERVAL_MINUTES = 2  # Интервал проверки каждые 2 минуты (для тестирования)
LOOKBACK_MINUTES = 5  # Ищем посты за последние 5 минут (±5 минут от запланированного времени)

# Настройки для обработки изображений
MAX_IMAGES_PER_POST = 10
TEMP_IMAGES_DIR = "temp_images"

# Настройки форматирования
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# Статусы публикации
STATUS_PENDING = "Ожидает"
STATUS_PUBLISHED = "Опубликовано"
STATUS_ERROR = "Ошибка"

# Названия колонок в Google Sheets
COLUMNS = {
    'DATE': 'Date',
    'TIME': 'Time', 
    'TEXT': 'Text',
    'IMAGE_URLS': 'Image URLs',
    'STATUS': 'Status',
    'PROMPT_RU': 'Промпт RU',
    'PROMPT_EN': 'Промпт EN'
}
