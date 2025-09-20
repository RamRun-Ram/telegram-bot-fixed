#!/usr/bin/env python3
"""
Принудительная публикация всех постов для немедленной проверки
"""

import asyncio
import sys
import os
from datetime import datetime
import pytz

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import PostAutomation
from config import STATUS_PENDING

async def force_publish_all():
    """Принудительно публикует все посты"""
    
    print("🔧 Принудительная публикация всех постов...")
    
    # Инициализируем систему
    automation = PostAutomation()
    await automation.initialize()
    
    print("✅ Система инициализирована")
    
    # Получаем все посты
    posts = automation.sheets_client.get_all_posts()
    
    if not posts:
        print("❌ Нет постов для публикации")
        return
    
    print(f"📋 Найдено {len(posts)} постов")
    
    # Фильтруем только неопубликованные посты
    pending_posts = [post for post in posts if post.get('status') == STATUS_PENDING]
    
    if not pending_posts:
        print("❌ Нет неопубликованных постов")
        return
    
    print(f"📋 Найдено {len(pending_posts)} неопубликованных постов")
    
    # Публикуем каждый пост
    for i, post in enumerate(pending_posts, 1):
        print(f"\n📝 Публикуем пост {i}/{len(pending_posts)}")
        print(f"   Строка: {post.get('row_index', 'N/A')}")
        print(f"   Время: {post.get('time', 'N/A')}")
        print(f"   Изображения: {'да' if post.get('image_urls') else 'нет'}")
        print(f"   Длина текста: {len(post.get('text', ''))} символов")
        
        # Показываем первые 100 символов текста
        text_preview = post.get('text', '')[:100]
        if len(post.get('text', '')) > 100:
            text_preview += "..."
        print(f"   Текст: {text_preview}")
        
        # Публикуем пост
        success = await automation.publish_post(post)
        
        if success:
            print(f"   ✅ Пост {i} опубликован успешно")
        else:
            print(f"   ❌ Ошибка публикации поста {i}")
        
        # Небольшая пауза между постами
        await asyncio.sleep(2)
    
    print(f"\n🎯 Публикация завершена!")
    print(f"📊 Статистика:")
    print(f"   Всего постов: {len(posts)}")
    print(f"   Неопубликованных: {len(pending_posts)}")
    print(f"   Опубликовано: {automation.daily_stats['published']}")
    print(f"   Ошибок: {automation.daily_stats['errors']}")
    
    print("\n📱 Проверьте канал Telegram:")
    print("   - Посты с изображениями должны иметь изображение ВНИЗУ")
    print("   - HTML теги должны работать корректно")
    print("   - Посты без изображений должны использовать Markdown")

if __name__ == "__main__":
    asyncio.run(force_publish_all())