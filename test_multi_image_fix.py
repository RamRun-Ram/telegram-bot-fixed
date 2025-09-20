#!/usr/bin/env python3
"""
Тестирование исправления метода для нескольких изображений
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import pytz

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_sheets_client import GoogleSheetsClient
from config import GOOGLE_SHEET_ID, STATUS_PENDING

async def test_multi_image_fix():
    """Тестирует исправленный метод для нескольких изображений"""
    
    print("🔧 Тестирование исправления метода для нескольких изображений...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Пост на текущее время
    post_time = now.strftime("%H:%M")
    post_date = now.strftime("%d.%m.%Y")
    
    # Текст до 1000 символов (для метода с несколькими изображениями)
    text = f"""
**🧪 ТЕСТ ИСПРАВЛЕНИЯ МЕТОДА ДЛЯ НЕСКОЛЬКИХ ИЗОБРАЖЕНИЙ**

*Время создания: {post_time} MSK*

Это тестовый пост для проверки исправленного метода отправки постов с несколькими изображениями.

**Что исправлено:**
- Использование InputMediaPhoto вместо словаря
- Правильный формат для send_media_group
- Корректная обработка parse_mode

**Особенности метода:**
- Markdown форматирование
- До 1000 символов
- Медиагруппа с изображениями
- Первое изображение с подписью

*Проверяем форматирование:*
- **Жирный текст** должен работать
- *Курсивный текст* должен работать
- __Подчеркнутый текст__ должен работать

**Список функций:**
- Отправка медиагруппы
- Markdown разметка
- Ограничение символов
- Поддержка множественных изображений

*Если вы видите этот пост с несколькими изображениями, значит исправление работает!*

**Заключение:**
Исправленный метод должен корректно отправлять посты с несколькими изображениями через медиагруппу Telegram.

*Тест исправления завершен!* 🎉
    """.strip()
    
    # Несколько URL изображений для теста
    image_urls = [
        "https://picsum.photos/800/600?random=1",
        "https://picsum.photos/800/600?random=2", 
        "https://picsum.photos/800/600?random=3",
        "https://picsum.photos/800/600?random=4",
        "https://picsum.photos/800/600?random=5"
    ]
    
    print(f"📝 Длина текста: {len(text)} символов")
    print(f"🖼️ Количество изображений: {len(image_urls)}")
    print(f"📅 Дата: {post_date}")
    print(f"⏰ Время: {post_time}")
    
    # Добавляем пост в Google Sheets
    post_data = {
        'date': post_date,
        'time': post_time,
        'text': text,
        'prompt_ru': 'Тест исправления метода для множественных изображений',
        'prompt_en': 'Test fix for multiple images method',
        'image_urls': ", ".join(image_urls),  # Объединяем URL через запятую
        'status': STATUS_PENDING
    }
    
    success = sheets_client.add_post(post_data)
    
    if success:
        print("✅ Тестовый пост с исправленным методом добавлен в Google Sheets")
        print("📱 Пост должен быть опубликован в течение 2 минут")
        print("🔍 Проверьте канал - должен появиться пост с медиагруппой из 5 изображений")
        print("📊 Ожидаемый результат:")
        print("   - Markdown форматирование")
        print("   - Медиагруппа с 5 изображениями")
        print("   - Текст до 1000 символов")
        print("   - БЕЗ ошибки 'dict' object has no attribute 'parse_mode'")
    else:
        print("❌ Ошибка добавления поста в Google Sheets")

if __name__ == "__main__":
    asyncio.run(test_multi_image_fix())
