#!/usr/bin/env python3
"""
Тестирование исправленных цитат с изображениями
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

async def test_quote_images_fixed():
    """Тестирует исправленные цитаты с изображениями"""
    
    print("🔧 Тестирование исправленных цитат с изображениями...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем тестовые цитаты с изображениями
    test_quotes = []
    
    # Цитата 1: Цитата с одним изображением (picsum)
    quote1_time = now + timedelta(minutes=1)
    test_quotes.append({
        'date': quote1_time.strftime("%d.%m.%Y"),
        'time': quote1_time.strftime("%H:%M"),
        'text': "> Истинная любовь – это когда два человека принимают недостатки друг друга с такой же нежностью, с какой ценят достоинства.",
        'prompt_ru': 'Цитата с одним изображением',
        'prompt_en': 'Quote with one image',
        'image_urls': 'https://picsum.photos/800/600?random=1',
        'status': STATUS_PENDING,
        'description': 'Цитата с одним изображением (picsum)'
    })
    
    # Цитата 2: Цитата с одним изображением (Google Drive)
    quote2_time = now + timedelta(minutes=2)
    test_quotes.append({
        'date': quote2_time.strftime("%d.%m.%Y"),
        'time': quote2_time.strftime("%H:%M"),
        'text': "> Главное в отношениях – не найти идеального человека, а создать идеальные отношения с тем, кого любишь.",
        'prompt_ru': 'Цитата с Google Drive изображением',
        'prompt_en': 'Quote with Google Drive image',
        'image_urls': 'https://drive.google.com/file/d/1lHiVjQ7Xuh3PG8dJHg6pGnfXaT0pvwa3/view?usp=sharing',
        'status': STATUS_PENDING,
        'description': 'Цитата с Google Drive изображением'
    })
    
    # Цитата 3: Цитата с несколькими изображениями
    quote3_time = now + timedelta(minutes=3)
    test_quotes.append({
        'date': quote3_time.strftime("%d.%m.%Y"),
        'time': quote3_time.strftime("%H:%M"),
        'text': "> Успех — это способность переходить от одной неудачи к другой, не теряя энтузиазма.\n\n*— Уинстон Черчилль*",
        'prompt_ru': 'Цитата с несколькими изображениями',
        'prompt_en': 'Quote with multiple images',
        'image_urls': 'https://picsum.photos/800/600?random=2, https://picsum.photos/800/600?random=3',
        'status': STATUS_PENDING,
        'description': 'Цитата с несколькими изображениями'
    })
    
    # Цитата 4: Цитата с HTML форматированием и изображением
    quote4_time = now + timedelta(minutes=4)
    test_quotes.append({
        'date': quote4_time.strftime("%d.%m.%Y"),
        'time': quote4_time.strftime("%H:%M"),
        'text': "> <b>Любовь</b> — это не тогда, когда вы смотрите друг на друга,\n> а когда вы смотрите в <i>одном направлении</i>.\n\n*— Антуан де Сент-Экзюпери*",
        'prompt_ru': 'Цитата с HTML форматированием',
        'prompt_en': 'Quote with HTML formatting',
        'image_urls': 'https://picsum.photos/800/600?random=4',
        'status': STATUS_PENDING,
        'description': 'Цитата с HTML форматированием и изображением'
    })
    
    # Цитата 5: Простая цитата без изображения (для сравнения)
    quote5_time = now + timedelta(minutes=5)
    test_quotes.append({
        'date': quote5_time.strftime("%d.%m.%Y"),
        'time': quote5_time.strftime("%H:%M"),
        'text': "> Когда мы перестаём притворяться, чтобы понравиться, начинаются настоящие отношения.",
        'prompt_ru': 'Цитата без изображения',
        'prompt_en': 'Quote without image',
        'image_urls': '',
        'status': STATUS_PENDING,
        'description': 'Цитата без изображения (для сравнения)'
    })
    
    print(f"\n📊 Создано {len(test_quotes)} тестовых цитат:")
    for i, quote in enumerate(test_quotes, 1):
        print(f"   {i}. {quote['description']} - {quote['time']}")
        print(f"      Изображения: {'да' if quote['image_urls'] else 'нет'}")
        if quote['image_urls']:
            image_count = len(quote['image_urls'].split(','))
            print(f"      Количество: {image_count}")
    
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
    print(f"   ✅ Цитаты без изображений: <blockquote> форматирование")
    print(f"   ✅ Цитаты с 1 изображением: HTML метод (как обычные посты)")
    print(f"   ✅ Цитаты с несколькими изображениями: Markdown метод (как обычные посты)")
    print(f"   ✅ Google Drive изображения должны работать")
    print(f"   🔄 Система проверяет каждые 2 минуты")
    print(f"   📱 Проверьте канал через 2-3 минуты")

if __name__ == "__main__":
    asyncio.run(test_quote_images_fixed())
