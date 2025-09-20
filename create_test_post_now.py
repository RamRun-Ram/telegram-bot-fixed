#!/usr/bin/env python3
"""
Создание тестового поста для немедленной проверки
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

async def create_test_post():
    """Создает тестовый пост с изображением для немедленной проверки"""
    
    print("🔧 Создание тестового поста с изображением...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    # Создаем тестовый пост с длинным текстом и изображением
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Пост на текущее время
    post_time = now.strftime("%H:%M")
    post_date = now.strftime("%d.%m.%Y")
    
    long_text = f"""
<b>🧪 ТЕСТОВЫЙ ПОСТ С ИЗОБРАЖЕНИЕМ</b>

<i>Время создания: {post_time} MSK</i>

Это очень длинный тестовый пост для проверки лимита символов и правильного отображения изображения. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

<b>Проверяем HTML форматирование:</b>
- <b>Жирный текст</b> должен остаться жирным
- <i>Курсивный текст</i> должен остаться курсивным  
- <u>Подчеркнутый текст</u> должен остаться подчеркнутым

<i>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</i>

<b>Вторая часть поста:</b>
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.

<u>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</u>

<b>Третья часть поста:</b>
Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.

<i>Ut enim ad minima veniam, quis nostrud exercitationem ullamco laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur.</i>

<b>Четвертая часть поста:</b>
At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident.

<u>Similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio.</u>

<b>Пятая часть поста:</b>
Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.

<i>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae.</i>

<b>Заключение:</b>
Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.

<b>Ожидаемый результат:</b>
- Изображение должно быть ВНИЗУ поста с предпросмотром
- HTML теги должны работать корректно
- Длина поста должна быть ~4000 символов
- Ссылка на изображение должна быть кликабельной

<i>Если вы видите это сообщение, значит пост был опубликован!</i>
    """.strip()
    
    # URL изображения для теста
    image_url = "https://picsum.photos/800/600"
    
    print(f"📝 Длина текста: {len(long_text)} символов")
    print(f"🖼️ URL изображения: {image_url}")
    print(f"📅 Дата: {post_date}")
    print(f"⏰ Время: {post_time}")
    
    # Добавляем пост в Google Sheets
    post_data = {
        'date': post_date,
        'time': post_time,
        'text': long_text,
        'prompt_ru': 'Тестовый промпт RU',
        'prompt_en': 'Test prompt EN',
        'image_urls': image_url,
        'status': STATUS_PENDING
    }
    
    success = sheets_client.add_post(post_data)
    
    if success:
        print("✅ Тестовый пост добавлен в Google Sheets")
        print("📱 Пост должен быть опубликован в течение 2 минут")
        print("🔍 Проверьте канал - изображение должно быть внизу поста")
    else:
        print("❌ Ошибка добавления поста в Google Sheets")

if __name__ == "__main__":
    asyncio.run(create_test_post())
