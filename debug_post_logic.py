#!/usr/bin/env python3
"""
Диагностика логики публикации постов
"""

import asyncio
import sys
import os
from datetime import datetime
import pytz

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_sheets_client import GoogleSheetsClient
from main import TelegramAutomation

async def debug_post_logic():
    """Диагностирует логику публикации постов"""
    
    print("🔧 Диагностика логики публикации постов...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    # Получаем все посты
    all_posts = sheets_client.get_all_posts()
    
    if not all_posts:
        print("❌ Нет постов в Google Sheets")
        return
    
    print(f"📊 Найдено {len(all_posts)} постов в Google Sheets")
    
    # Анализируем каждый пост
    for i, post in enumerate(all_posts, 1):
        print(f"\n📝 Пост {i}:")
        print(f"   Строка: {post.get('row_index', 'N/A')}")
        print(f"   Дата: {post.get('date', 'N/A')}")
        print(f"   Время: {post.get('time', 'N/A')}")
        print(f"   Статус: {post.get('status', 'N/A')}")
        
        # Анализируем изображения
        image_urls = post.get('image_urls', [])
        print(f"   image_urls: {image_urls}")
        print(f"   Тип image_urls: {type(image_urls)}")
        print(f"   Длина image_urls: {len(image_urls) if image_urls else 0}")
        
        # Проверяем логику определения типа поста
        has_images = post.get('image_urls') and len(post['image_urls']) > 0
        print(f"   has_images: {has_images}")
        
        if has_images:
            image_count = len(post['image_urls'])
            print(f"   Количество изображений: {image_count}")
            
            if image_count > 1:
                print(f"   🎯 Метод: Markdown с медиагруппой (несколько изображений)")
            else:
                print(f"   🎯 Метод: HTML с предпросмотром (одно изображение)")
        else:
            print(f"   🎯 Метод: Markdown без изображений")
        
        # Показываем первые 100 символов текста
        text = post.get('text', '')
        text_preview = text[:100] if text else 'Нет текста'
        if len(text) > 100:
            text_preview += "..."
        print(f"   Текст: {text_preview}")
        
        print(f"   {'='*50}")
    
    # Тестируем логику выбора метода
    print(f"\n🧪 Тестирование логики выбора метода:")
    
    # Симулируем разные типы постов
    test_cases = [
        {
            'name': 'Пост без изображений',
            'image_urls': [],
            'expected_method': 'Markdown без изображений'
        },
        {
            'name': 'Пост с пустым image_urls',
            'image_urls': None,
            'expected_method': 'Markdown без изображений'
        },
        {
            'name': 'Пост с одним изображением',
            'image_urls': ['https://example.com/image1.jpg'],
            'expected_method': 'HTML с предпросмотром'
        },
        {
            'name': 'Пост с несколькими изображениями',
            'image_urls': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'],
            'expected_method': 'Markdown с медиагруппой'
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 {test_case['name']}:")
        print(f"   image_urls: {test_case['image_urls']}")
        
        # Симулируем логику из publish_post
        has_images = test_case['image_urls'] and len(test_case['image_urls']) > 0
        print(f"   has_images: {has_images}")
        
        if has_images:
            image_count = len(test_case['image_urls'])
            print(f"   Количество изображений: {image_count}")
            
            if image_count > 1:
                method = "Markdown с медиагруппой"
            else:
                method = "HTML с предпросмотром"
        else:
            method = "Markdown без изображений"
        
        print(f"   Выбранный метод: {method}")
        print(f"   Ожидаемый метод: {test_case['expected_method']}")
        print(f"   ✅ Совпадает: {method == test_case['expected_method']}")

if __name__ == "__main__":
    asyncio.run(debug_post_logic())
