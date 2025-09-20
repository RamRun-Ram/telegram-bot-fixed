#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Принудительная публикация тестового поста
"""
import os
import sys
import asyncio
from datetime import datetime, timedelta
import pytz

async def force_publish_test():
    """Принудительно публикует тестовый пост"""
    print("🚀 ПРИНУДИТЕЛЬНАЯ ПУБЛИКАЦИЯ ТЕСТОВОГО ПОСТА")
    print("=" * 60)
    
    try:
        from main import TelegramAutomation
        
        # Инициализируем систему
        print("🔧 Инициализация системы...")
        automation = TelegramAutomation()
        await automation.initialize()
        
        print("✅ Система инициализирована")
        
        # Создаем тестовый пост на прямо сейчас
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        test_post = {
            'date': current_time.strftime('%d.%m.%y'),
            'time': current_time.strftime('%H:%M'),
            'text': f"<b>🚀 ПРИНУДИТЕЛЬНЫЙ ТЕСТОВЫЙ ПОСТ</b><br><br>Этот пост публикуется принудительно для проверки системы.<br><br><i>Время:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает!",
            'prompt_ru': "",
            'prompt_en': "",
            'image_urls': "",
            'status': 'Ожидает',
            'row_index': 999
        }
        
        print(f"📝 Тестовый пост создан:")
        print(f"   Дата: {test_post['date']}")
        print(f"   Время: {test_post['time']}")
        print(f"   Текст: {test_post['text'][:100]}...")
        
        # Публикуем пост напрямую
        print(f"\n📱 Публикуем пост в Telegram...")
        success = await automation.publish_post(test_post)
        
        if success:
            print(f"🎉 ПОСТ УСПЕШНО ОПУБЛИКОВАН!")
            return True
        else:
            print(f"❌ Ошибка публикации поста")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

async def check_pending_posts():
    """Проверяет посты, готовые к публикации"""
    print("\n🔍 ПРОВЕРКА ПОСТОВ, ГОТОВЫХ К ПУБЛИКАЦИИ")
    print("=" * 60)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        await automation.initialize()
        
        # Получаем посты со статусом "Ожидает"
        pending_posts = automation.sheets_client.get_pending_posts()
        
        if not pending_posts:
            print("❌ Нет постов со статусом 'Ожидает'")
            return False
        
        print(f"📊 Найдено постов: {len(pending_posts)}")
        
        # Проверяем каждый пост
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        posts_to_publish = []
        for i, post in enumerate(pending_posts):
            print(f"\n🔍 Пост {i+1}:")
            print(f"   Строка: {post.get('row_index', 'N/A')}")
            print(f"   Дата: {post.get('date', 'N/A')}")
            print(f"   Время: {post.get('time', 'N/A')}")
            
            # Проверяем логику времени
            if automation._should_publish_post(post, current_time):
                posts_to_publish.append(post)
                print(f"   ✅ ДОЛЖЕН ПУБЛИКОВАТЬСЯ")
            else:
                print(f"   ❌ НЕ ПОДХОДИТ ПО ВРЕМЕНИ")
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Всего постов: {len(pending_posts)}")
        print(f"   К публикации: {len(posts_to_publish)}")
        
        # Публикуем посты, готовые к публикации
        if posts_to_publish:
            print(f"\n📱 ПУБЛИКУЕМ ПОСТЫ...")
            published_count = 0
            for post in posts_to_publish:
                success = await automation.publish_post(post)
                if success:
                    published_count += 1
                    print(f"   ✅ Пост из строки {post.get('row_index', 'N/A')} опубликован")
                else:
                    print(f"   ❌ Ошибка публикации поста из строки {post.get('row_index', 'N/A')}")
            
            print(f"\n🎉 ОПУБЛИКОВАНО ПОСТОВ: {published_count}/{len(posts_to_publish)}")
            return published_count > 0
        else:
            print(f"\n⏰ НЕТ ПОСТОВ ДЛЯ ПУБЛИКАЦИИ")
            return False
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Основная функция"""
    print("🔧 ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА И ПУБЛИКАЦИЯ")
    print("=" * 70)
    
    # Проверяем посты, готовые к публикации
    success1 = await check_pending_posts()
    
    # Принудительно публикуем тестовый пост
    success2 = await force_publish_test()
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Посты из таблицы: {'✅ OK' if success1 else '❌ ERROR'}")
    print(f"   Тестовый пост: {'✅ OK' if success2 else '❌ ERROR'}")
    
    if success1 or success2:
        print(f"\n🎉 СИСТЕМА РАБОТАЕТ!")
        print(f"📱 Проверьте Telegram-канал")
    else:
        print(f"\n❌ СИСТЕМА НЕ РАБОТАЕТ!")
        print(f"🔧 Запустите полную диагностику: python full_diagnosis.py")

if __name__ == "__main__":
    asyncio.run(main())
