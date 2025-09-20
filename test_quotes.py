#!/usr/bin/env python3
"""
Тестирование цитат с правильным форматированием
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

async def test_quotes():
    """Тестирует цитаты с правильным форматированием"""
    
    print("🔧 Тестирование цитат с правильным форматированием...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем тестовые цитаты
    test_quotes = []
    
    # Цитата 1: Без изображения (как на первом скриншоте)
    quote1_time = now + timedelta(minutes=1)
    test_quotes.append({
        'date': quote1_time.strftime("%d.%m.%Y"),
        'time': quote1_time.strftime("%H:%M"),
        'text': "> Главное в отношениях – не найти идеального человека, а создать идеальные отношения с тем, кого любишь.",
        'prompt_ru': 'Цитата о любви',
        'prompt_en': 'Quote about love',
        'image_urls': '',  # Без изображения
        'status': STATUS_PENDING,
        'description': 'Цитата без изображения (как на первом скриншоте)'
    })
    
    # Цитата 2: С изображением (как на втором скриншоте)
    quote2_time = now + timedelta(minutes=2)
    test_quotes.append({
        'date': quote2_time.strftime("%d.%m.%Y"),
        'time': quote2_time.strftime("%H:%M"),
        'text': "> Любовь — это не тогда, когда вы смотрите друг на друга, а когда вы смотрите в одном направлении.\n\n*— Антуан де Сент-Экзюпери*",
        'prompt_ru': 'Цитата с изображением',
        'prompt_en': 'Quote with image',
        'image_urls': 'https://picsum.photos/800/600?random=1',  # С изображением
        'status': STATUS_PENDING,
        'description': 'Цитата с изображением (как на втором скриншоте)'
    })
    
    # Цитата 3: Многострочная цитата без изображения
    quote3_time = now + timedelta(minutes=3)
    test_quotes.append({
        'date': quote3_time.strftime("%d.%m.%Y"),
        'time': quote3_time.strftime("%H:%M"),
        'text': "> Успех — это способность переходить от одной неудачи к другой,\n> не теряя энтузиазма.\n\n*— Уинстон Черчилль*",
        'prompt_ru': 'Многострочная цитата',
        'prompt_en': 'Multiline quote',
        'image_urls': '',  # Без изображения
        'status': STATUS_PENDING,
        'description': 'Многострочная цитата без изображения'
    })
    
    # Цитата 4: Цитата с несколькими изображениями
    quote4_time = now + timedelta(minutes=4)
    test_quotes.append({
        'date': quote4_time.strftime("%d.%m.%Y"),
        'time': quote4_time.strftime("%H:%M"),
        'text': "> Жизнь — это то, что происходит с тобой,\n> пока ты строишь планы.\n\n*— Джон Леннон*",
        'prompt_ru': 'Цитата с несколькими изображениями',
        'prompt_en': 'Quote with multiple images',
        'image_urls': 'https://picsum.photos/800/600?random=1, https://picsum.photos/800/600?random=2, https://picsum.photos/800/600?random=3',
        'status': STATUS_PENDING,
        'description': 'Цитата с несколькими изображениями'
    })
    
    # Цитата 5: Цитата с HTML форматированием
    quote5_time = now + timedelta(minutes=5)
    test_quotes.append({
        'date': quote5_time.strftime("%d.%m.%Y"),
        'time': quote5_time.strftime("%H:%M"),
        'text': "> <b>Единственный способ делать великую работу</b> — это <i>любить то, что ты делаешь</i>.\n\n<u>— Стив Джобс</u>",
        'prompt_ru': 'Цитата с HTML форматированием',
        'prompt_en': 'Quote with HTML formatting',
        'image_urls': 'https://picsum.photos/800/600?random=1',
        'status': STATUS_PENDING,
        'description': 'Цитата с HTML форматированием и изображением'
    })
    
    print(f"\n📊 Создано {len(test_quotes)} тестовых цитат:")
    for i, quote in enumerate(test_quotes, 1):
        print(f"   {i}. {quote['description']} - {quote['time']}")
        print(f"      Изображения: {'да' if quote['image_urls'] else 'нет'}")
    
    # Добавляем цитаты в Google Sheets
    success_count = 0
    for i, quote in enumerate(test_quotes, 1):
        print(f"\n📝 Добавляем {quote['description']}")
        
        post_data = {
            'date': quote['date'],
            'time': quote['time'],
            'text': quote['text'],
            'prompt_ru': quote['prompt_ru'],
            'prompt_en': quote['prompt_en'],
            'image_urls': quote['image_urls'],
            'status': quote['status']
        }
        
        success = sheets_client.add_post(post_data)
        
        if success:
            print(f"   ✅ Цитата {i} добавлена успешно")
            success_count += 1
        else:
            print(f"   ❌ Ошибка добавления цитаты {i}")
    
    print(f"\n🎯 Тестирование завершено!")
    print(f"📊 Добавлено {success_count}/{len(test_quotes)} цитат")
    print(f"\n📋 Ожидаемые результаты:")
    print(f"   ✅ Цитаты должны отображаться с правильным форматированием")
    print(f"   ✅ Цитаты без изображений - как обычные сообщения с blockquote")
    print(f"   ✅ Цитаты с изображениями - как медиагруппа с подписью")
    print(f"   ✅ HTML форматирование должно работать в цитатах")
    print(f"   🔄 Система проверяет каждые 2 минуты")
    print(f"   📱 Проверьте канал через 2-3 минуты")

if __name__ == "__main__":
    asyncio.run(test_quotes())
