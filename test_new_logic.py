#!/usr/bin/env python3
"""
Тестирование новой логики проверки постов
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

async def test_new_logic():
    """Тестирует новую логику проверки постов"""
    
    print("🔧 Тестирование новой логики проверки постов...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем тестовые посты с разным временем
    test_posts = []
    
    # Пост в прошлом (должен быть опубликован)
    past_time = now - timedelta(minutes=10)
    test_posts.append({
        'date': past_time.strftime("%d.%m.%Y"),
        'time': past_time.strftime("%H:%M"),
        'text': f"**Пост в прошлом**\n\nВремя: {past_time.strftime('%H:%M')}\nЭтот пост должен быть опубликован, так как его время уже прошло.",
        'prompt_ru': 'Пост в прошлом',
        'prompt_en': 'Post in the past',
        'image_urls': '',
        'status': STATUS_PENDING,
        'description': 'Пост в прошлом (должен быть опубликован)'
    })
    
    # Пост сейчас (должен быть опубликован)
    current_time = now
    test_posts.append({
        'date': current_time.strftime("%d.%m.%Y"),
        'time': current_time.strftime("%H:%M"),
        'text': f"**Пост сейчас**\n\nВремя: {current_time.strftime('%H:%M')}\nЭтот пост должен быть опубликован, так как его время наступило.",
        'prompt_ru': 'Пост сейчас',
        'prompt_en': 'Post now',
        'image_urls': '',
        'status': STATUS_PENDING,
        'description': 'Пост сейчас (должен быть опубликован)'
    })
    
    # Пост в будущем (НЕ должен быть опубликован)
    future_time = now + timedelta(minutes=5)
    test_posts.append({
        'date': future_time.strftime("%d.%m.%Y"),
        'time': future_time.strftime("%H:%M"),
        'text': f"**Пост в будущем**\n\nВремя: {future_time.strftime('%H:%M')}\nЭтот пост НЕ должен быть опубликован, так как его время еще не наступило.",
        'prompt_ru': 'Пост в будущем',
        'prompt_en': 'Post in the future',
        'image_urls': '',
        'status': STATUS_PENDING,
        'description': 'Пост в будущем (НЕ должен быть опубликован)'
    })
    
    # Пост с изображением в прошлом (должен быть опубликован)
    past_image_time = now - timedelta(minutes=5)
    test_posts.append({
        'date': past_image_time.strftime("%d.%m.%Y"),
        'time': past_image_time.strftime("%H:%M"),
        'text': f"<b>Пост с изображением в прошлом</b>\n\n<i>Время:</i> {past_image_time.strftime('%H:%M')}\nЭтот пост с изображением должен быть опубликован.",
        'prompt_ru': 'Пост с изображением в прошлом',
        'prompt_en': 'Post with image in the past',
        'image_urls': 'https://picsum.photos/800/600?random=1',
        'status': STATUS_PENDING,
        'description': 'Пост с изображением в прошлом (должен быть опубликован)'
    })
    
    # Пост с несколькими изображениями в прошлом (должен быть опубликован)
    past_multi_time = now - timedelta(minutes=3)
    test_posts.append({
        'date': past_multi_time.strftime("%d.%m.%Y"),
        'time': past_multi_time.strftime("%H:%M"),
        'text': f"**Пост с несколькими изображениями в прошлом**\n\n*Время:* {past_multi_time.strftime('%H:%M')}\nЭтот пост с несколькими изображениями должен быть опубликован.",
        'prompt_ru': 'Пост с несколькими изображениями в прошлом',
        'prompt_en': 'Post with multiple images in the past',
        'image_urls': 'https://picsum.photos/800/600?random=1, https://picsum.photos/800/600?random=2, https://picsum.photos/800/600?random=3',
        'status': STATUS_PENDING,
        'description': 'Пост с несколькими изображениями в прошлом (должен быть опубликован)'
    })
    
    print(f"\n📊 Создано {len(test_posts)} тестовых постов:")
    for i, post in enumerate(test_posts, 1):
        print(f"   {i}. {post['description']} - {post['time']}")
    
    # Добавляем посты в Google Sheets
    success_count = 0
    for i, post in enumerate(test_posts, 1):
        print(f"\n📝 Добавляем {post['description']}")
        
        post_data = {
            'date': post['date'],
            'time': post['time'],
            'text': post['text'],
            'prompt_ru': post['prompt_ru'],
            'prompt_en': post['prompt_en'],
            'image_urls': post['image_urls'],
            'status': post['status']
        }
        
        success = sheets_client.add_post(post_data)
        
        if success:
            print(f"   ✅ Пост {i} добавлен успешно")
            success_count += 1
        else:
            print(f"   ❌ Ошибка добавления поста {i}")
    
    print(f"\n🎯 Тестирование завершено!")
    print(f"📊 Добавлено {success_count}/{len(test_posts)} постов")
    print(f"\n📋 Ожидаемые результаты:")
    print(f"   ✅ Посты в прошлом и сейчас должны быть опубликованы")
    print(f"   ❌ Пост в будущем НЕ должен быть опубликован")
    print(f"   🔄 Система проверяет каждые 2 минуты")
    print(f"   📱 Проверьте канал через 2-3 минуты")

if __name__ == "__main__":
    asyncio.run(test_new_logic())
