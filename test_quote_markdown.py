#!/usr/bin/env python3
"""
Тестирование исправленного форматирования цитат с Markdown
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

async def test_quote_markdown():
    """Тестирует исправленное форматирование цитат с Markdown"""
    
    print("🔧 Тестирование исправленного форматирования цитат с Markdown...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем тестовые цитаты с Markdown форматированием
    test_quotes = []
    
    # Цитата 1: Простая цитата без изображения
    quote1_time = now + timedelta(minutes=1)
    test_quotes.append({
        'date': quote1_time.strftime("%d.%m.%Y"),
        'time': quote1_time.strftime("%H:%M"),
        'text': "> Когда мы перестаём притворяться, чтобы понравиться, начинаются настоящие отношения.",
        'prompt_ru': 'Цитата о настоящих отношениях',
        'prompt_en': 'Quote about real relationships',
        'image_urls': '',  # Без изображения
        'status': STATUS_PENDING,
        'description': 'Простая цитата без изображения'
    })
    
    # Цитата 2: Цитата с изображением
    quote2_time = now + timedelta(minutes=2)
    test_quotes.append({
        'date': quote2_time.strftime("%d.%m.%Y"),
        'time': quote2_time.strftime("%H:%M"),
        'text': "> Истинная любовь – это когда два человека принимают недостатки друг друга с такой же нежностью, с какой ценят достоинства.",
        'prompt_ru': 'Цитата об истинной любви',
        'prompt_en': 'Quote about true love',
        'image_urls': 'https://picsum.photos/800/600?random=1',  # С изображением
        'status': STATUS_PENDING,
        'description': 'Цитата с изображением'
    })
    
    # Цитата 3: Многострочная цитата
    quote3_time = now + timedelta(minutes=3)
    test_quotes.append({
        'date': quote3_time.strftime("%d.%m.%Y"),
        'time': quote3_time.strftime("%H:%M"),
        'text': "> Главное в отношениях – не найти идеального человека,\n> а создать идеальные отношения с тем, кого любишь.",
        'prompt_ru': 'Многострочная цитата',
        'prompt_en': 'Multiline quote',
        'image_urls': '',  # Без изображения
        'status': STATUS_PENDING,
        'description': 'Многострочная цитата без изображения'
    })
    
    # Цитата 4: Цитата с Markdown форматированием и изображением
    quote4_time = now + timedelta(minutes=4)
    test_quotes.append({
        'date': quote4_time.strftime("%d.%m.%Y"),
        'time': quote4_time.strftime("%H:%M"),
        'text': "> **Любовь** — это не тогда, когда вы смотрите друг на друга,\n> а когда вы смотрите в *одном направлении*.\n\n*— Антуан де Сент-Экзюпери*",
        'prompt_ru': 'Цитата с Markdown форматированием',
        'prompt_en': 'Quote with Markdown formatting',
        'image_urls': 'https://picsum.photos/800/600?random=2',  # С изображением
        'status': STATUS_PENDING,
        'description': 'Цитата с Markdown форматированием и изображением'
    })
    
    # Цитата 5: Цитата с несколькими изображениями
    quote5_time = now + timedelta(minutes=5)
    test_quotes.append({
        'date': quote5_time.strftime("%d.%m.%Y"),
        'time': quote5_time.strftime("%H:%M"),
        'text': "> Успех — это способность переходить от одной неудачи к другой,\n> не теряя энтузиазма.\n\n*— Уинстон Черчилль*",
        'prompt_ru': 'Цитата с несколькими изображениями',
        'prompt_en': 'Quote with multiple images',
        'image_urls': 'https://picsum.photos/800/600?random=3, https://picsum.photos/800/600?random=4',  # Несколько изображений
        'status': STATUS_PENDING,
        'description': 'Цитата с несколькими изображениями'
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
    print(f"   ✅ Цитаты должны отображаться с Markdown форматированием:")
    print(f"      > Текст цитаты")
    print(f"   ✅ Цитаты с изображениями должны показывать изображения")
    print(f"   ✅ Markdown форматирование должно работать в цитатах")
    print(f"   🔄 Система проверяет каждые 2 минуты")
    print(f"   📱 Проверьте канал через 2-3 минуты")

if __name__ == "__main__":
    asyncio.run(test_quote_markdown())
