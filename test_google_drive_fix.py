#!/usr/bin/env python3
"""
Тестирование исправленных ссылок Google Drive
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

async def test_google_drive_fix():
    """Тестирует исправленные ссылки Google Drive"""
    
    print("🔧 Тестирование исправленных ссылок Google Drive...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем тестовые посты с Google Drive изображениями
    test_posts = []
    
    # Пост 1: Обычный пост с Google Drive изображением
    post1_time = now + timedelta(minutes=1)
    test_posts.append({
        'date': post1_time.strftime("%d.%m.%Y"),
        'time': post1_time.strftime("%H:%M"),
        'text': "Тестовый пост с изображением из Google Drive. Это должно работать правильно после исправления ссылок.",
        'prompt_ru': 'Тест Google Drive',
        'prompt_en': 'Google Drive test',
        'image_urls': 'https://drive.google.com/file/d/1lHiVjQ7Xuh3PG8dJHg6pGnfXaT0pvwa3/view?usp=sharing',
        'status': STATUS_PENDING,
        'description': 'Обычный пост с Google Drive изображением'
    })
    
    # Пост 2: Цитата с Google Drive изображением
    post2_time = now + timedelta(minutes=2)
    test_posts.append({
        'date': post2_time.strftime("%d.%m.%Y"),
        'time': post2_time.strftime("%H:%M"),
        'text': "> Главное в отношениях – не найти идеального человека, а создать идеальные отношения с тем, кого любишь.",
        'prompt_ru': 'Цитата с Google Drive',
        'prompt_en': 'Quote with Google Drive',
        'image_urls': 'https://drive.google.com/file/d/1lHiVjQ7Xuh3PG8dJHg6pGnfXaT0pvwa3/view?usp=sharing',
        'status': STATUS_PENDING,
        'description': 'Цитата с Google Drive изображением'
    })
    
    # Пост 3: Пост с несколькими изображениями (Google Drive + picsum)
    post3_time = now + timedelta(minutes=3)
    test_posts.append({
        'date': post3_time.strftime("%d.%m.%Y"),
        'time': post3_time.strftime("%H:%M"),
        'text': "Пост с несколькими изображениями: одно из Google Drive, другое из picsum. Оба должны отображаться правильно.",
        'prompt_ru': 'Множественные изображения',
        'prompt_en': 'Multiple images',
        'image_urls': 'https://drive.google.com/file/d/1lHiVjQ7Xuh3PG8dJHg6pGnfXaT0pvwa3/view?usp=sharing, https://picsum.photos/800/600?random=1',
        'status': STATUS_PENDING,
        'description': 'Пост с несколькими изображениями (Google Drive + picsum)'
    })
    
    # Пост 4: Цитата без изображения (для сравнения)
    post4_time = now + timedelta(minutes=4)
    test_posts.append({
        'date': post4_time.strftime("%d.%m.%Y"),
        'time': post4_time.strftime("%H:%M"),
        'text': "> Когда мы перестаём притворяться, чтобы понравиться, начинаются настоящие отношения.",
        'prompt_ru': 'Цитата без изображения',
        'prompt_en': 'Quote without image',
        'image_urls': '',
        'status': STATUS_PENDING,
        'description': 'Цитата без изображения (для сравнения)'
    })
    
    # Пост 5: Обычный пост с picsum изображением (для сравнения)
    post5_time = now + timedelta(minutes=5)
    test_posts.append({
        'date': post5_time.strftime("%d.%m.%Y"),
        'time': post5_time.strftime("%H:%M"),
        'text': "Обычный пост с picsum изображением. Это должно работать как обычно.",
        'prompt_ru': 'Тест picsum',
        'prompt_en': 'Picsum test',
        'image_urls': 'https://picsum.photos/800/600?random=2',
        'status': STATUS_PENDING,
        'description': 'Обычный пост с picsum изображением'
    })
    
    print(f"\n📊 Создано {len(test_posts)} тестовых постов:")
    for i, post in enumerate(test_posts, 1):
        print(f"   {i}. {post['description']} - {post['time']}")
        print(f"      Изображения: {'да' if post['image_urls'] else 'нет'}")
        if post['image_urls']:
            image_count = len(post['image_urls'].split(','))
            print(f"      Количество: {image_count}")
            if 'drive.google.com' in post['image_urls']:
                print(f"      Google Drive: да")
    
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
    print(f"   ✅ Google Drive изображения должны отображаться правильно")
    print(f"   ✅ Ссылки преобразуются в формат: https://drive.google.com/uc?export=view&id=FILE_ID")
    print(f"   ✅ Цитаты с Google Drive изображениями должны работать")
    print(f"   ✅ Посты с несколькими изображениями должны работать")
    print(f"   🔄 Система проверяет каждые 2 минуты")
    print(f"   📱 Проверьте канал через 2-3 минуты")

if __name__ == "__main__":
    asyncio.run(test_google_drive_fix())
