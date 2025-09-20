#!/usr/bin/env python3
"""
Создание тестового поста с несколькими изображениями
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

async def create_multi_image_test():
    """Создает тестовый пост с несколькими изображениями"""
    
    print("🔧 Создание тестового поста с несколькими изображениями...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    # Создаем тестовый пост с несколькими изображениями
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Пост на текущее время
    post_time = now.strftime("%H:%M")
    post_date = now.strftime("%d.%m.%Y")
    
    # Текст до 1000 символов (для метода с несколькими изображениями)
    text = f"""
**🧪 ТЕСТОВЫЙ ПОСТ С НЕСКОЛЬКИМИ ИЗОБРАЖЕНИЯМИ**

*Время создания: {post_time} MSK*

Это тестовый пост для проверки нового метода отправки постов с несколькими изображениями. Пост использует Markdown форматирование и ограничен 1000 символами.

**Особенности нового метода:**
- Использует медиагруппу для отправки изображений
- Поддерживает до 10 изображений в одном посте
- Markdown форматирование текста
- Ограничение в 1000 символов

*Проверяем форматирование:*
- **Жирный текст** должен работать
- *Курсивный текст* должен работать
- __Подчеркнутый текст__ должен работать

**Список функций:**
- Отправка медиагруппы
- Markdown разметка
- Ограничение символов
- Поддержка множественных изображений

*Если вы видите этот пост с несколькими изображениями, значит новый метод работает корректно!*

**Заключение:**
Новый метод позволяет отправлять посты с несколькими изображениями, используя медиагруппу Telegram. Это более эффективно, чем отправка каждого изображения отдельно.

*Тест завершен успешно!* 🎉
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
        'prompt_ru': 'Тестовый промпт RU для множественных изображений',
        'prompt_en': 'Test prompt EN for multiple images',
        'image_urls': ", ".join(image_urls),  # Объединяем URL через запятую
        'status': STATUS_PENDING
    }
    
    success = sheets_client.add_post(post_data)
    
    if success:
        print("✅ Тестовый пост с несколькими изображениями добавлен в Google Sheets")
        print("📱 Пост должен быть опубликован в течение 2 минут")
        print("🔍 Проверьте канал - должен появиться пост с медиагруппой из 5 изображений")
        print("📊 Ожидаемый результат:")
        print("   - Markdown форматирование")
        print("   - Медиагруппа с 5 изображениями")
        print("   - Текст до 1000 символов")
    else:
        print("❌ Ошибка добавления поста в Google Sheets")

if __name__ == "__main__":
    asyncio.run(create_multi_image_test())
