#!/usr/bin/env python3
"""
Тестирование логики публикации цитат
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

async def test_quote_logic():
    """Тестирует логику публикации цитат"""
    
    print("🔧 Тестирование логики публикации цитат...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем тестовые цитаты с разными вариантами поля изображений
    test_quotes = []
    
    # Цитата 1: Пустое поле изображений
    quote1_time = now + timedelta(minutes=1)
    test_quotes.append({
        'date': quote1_time.strftime("%d.%m.%Y"),
        'time': quote1_time.strftime("%H:%M"),
        'text': "> **Цитата 1 (пустое поле изображений)**\n\nЛюбовь — это не тогда, когда вы смотрите друг на друга, а когда вы смотрите в одном направлении.\n\n*— Антуан де Сент-Экзюпери*",
        'prompt_ru': 'Цитата 1',
        'prompt_en': 'Quote 1',
        'image_urls': '',  # Пустая строка
        'status': STATUS_PENDING,
        'description': 'Цитата с пустым полем изображений'
    })
    
    # Цитата 2: Поле изображений с пробелами
    quote2_time = now + timedelta(minutes=2)
    test_quotes.append({
        'date': quote2_time.strftime("%d.%m.%Y"),
        'time': quote2_time.strftime("%H:%M"),
        'text': "> **Цитата 2 (поле с пробелами)**\n\nУспех — это способность переходить от одной неудачи к другой, не теряя энтузиазма.\n\n*— Уинстон Черчилль*",
        'prompt_ru': 'Цитата 2',
        'prompt_en': 'Quote 2',
        'image_urls': '   ',  # Только пробелы
        'status': STATUS_PENDING,
        'description': 'Цитата с полем изображений из пробелов'
    })
    
    # Цитата 3: Поле изображений с пустыми элементами
    quote3_time = now + timedelta(minutes=3)
    test_quotes.append({
        'date': quote3_time.strftime("%d.%m.%Y"),
        'time': quote3_time.strftime("%H:%M"),
        'text': "> **Цитата 3 (пустые элементы)**\n\nЖизнь — это то, что происходит с тобой, пока ты строишь планы.\n\n*— Джон Леннон*",
        'prompt_ru': 'Цитата 3',
        'prompt_en': 'Quote 3',
        'image_urls': ', , ,',  # Пустые элементы через запятую
        'status': STATUS_PENDING,
        'description': 'Цитата с пустыми элементами в поле изображений'
    })
    
    # Цитата 4: Поле изображений с невалидными URL
    quote4_time = now + timedelta(minutes=4)
    test_quotes.append({
        'date': quote4_time.strftime("%d.%m.%Y"),
        'time': quote4_time.strftime("%H:%M"),
        'text': "> **Цитата 4 (невалидные URL)**\n\nЕдинственный способ делать великую работу — это любить то, что ты делаешь.\n\n*— Стив Джобс*",
        'prompt_ru': 'Цитата 4',
        'prompt_en': 'Quote 4',
        'image_urls': 'invalid, not-a-url, empty',  # Невалидные URL
        'status': STATUS_PENDING,
        'description': 'Цитата с невалидными URL в поле изображений'
    })
    
    # Цитата 5: Поле изображений с одним валидным URL (должна быть как пост с изображением)
    quote5_time = now + timedelta(minutes=5)
    test_quotes.append({
        'date': quote5_time.strftime("%d.%m.%Y"),
        'time': quote5_time.strftime("%H:%M"),
        'text': "<b>Цитата 5 (с валидным изображением)</b>\n\n<i>Время не ждет, но оно дает нам возможность стать лучше.</i>\n\n<u>— Неизвестный автор</u>",
        'prompt_ru': 'Цитата 5',
        'prompt_en': 'Quote 5',
        'image_urls': 'https://picsum.photos/800/600?random=1',  # Валидный URL
        'status': STATUS_PENDING,
        'description': 'Цитата с валидным изображением (должна быть как пост с изображением)'
    })
    
    print(f"\n📊 Создано {len(test_quotes)} тестовых цитат:")
    for i, quote in enumerate(test_quotes, 1):
        print(f"   {i}. {quote['description']} - {quote['time']}")
        print(f"      image_urls: '{quote['image_urls']}'")
    
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
    print(f"   ✅ Цитаты 1-4 должны публиковаться как Markdown (без изображений)")
    print(f"   ✅ Цитата 5 должна публиковаться как HTML (с изображением)")
    print(f"   🔄 Система проверяет каждые 2 минуты")
    print(f"   📱 Проверьте канал через 2-3 минуты")

if __name__ == "__main__":
    asyncio.run(test_quote_logic())
