#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для принудительной публикации поста прямо сейчас
"""
import os
import sys
import asyncio
from datetime import datetime, timedelta
import pytz

async def force_publish_now():
    """Принудительно публикует пост прямо сейчас"""
    print("🚀 ПРИНУДИТЕЛЬНАЯ ПУБЛИКАЦИЯ ПОСТА")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        # Инициализируем систему
        automation = TelegramAutomation()
        await automation.initialize()
        
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
            'status': 'Ожидает'
        }
        
        print(f"📝 Тестовый пост создан:")
        print(f"   Дата: {test_post['date']}")
        print(f"   Время: {test_post['time']}")
        print(f"   Текст: {test_post['text'][:100]}...")
        
        # Добавляем пост в Google Sheets
        print(f"\n📋 Добавляем пост в Google Sheets...")
        result = automation.sheets_client.add_post(test_post)
        
        if result:
            print(f"✅ Пост добавлен в Google Sheets")
            
            # Публикуем пост
            print(f"\n📱 Публикуем пост в Telegram...")
            success = await automation.publish_post(test_post)
            
            if success:
                print(f"🎉 ПОСТ УСПЕШНО ОПУБЛИКОВАН!")
                return True
            else:
                print(f"❌ Ошибка публикации поста")
                return False
        else:
            print(f"❌ Ошибка добавления поста в Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

async def check_system_status():
    """Проверяет статус системы"""
    print("\n🔍 ПРОВЕРКА СТАТУСА СИСТЕМЫ")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        await automation.initialize()
        
        # Проверяем Google Sheets
        if automation.sheets_client.service:
            print("✅ Google Sheets: подключен")
            
            # Получаем посты
            posts = automation.sheets_client.get_pending_posts()
            print(f"📊 Найдено постов: {len(posts)}")
            
            if posts:
                print(f"\n📝 Последние 3 поста:")
                for i, post in enumerate(posts[:3]):
                    print(f"  {i+1}. Строка {post.get('row_index', 'N/A')}")
                    print(f"     Дата: {post.get('date', 'N/A')}")
                    print(f"     Время: {post.get('time', 'N/A')}")
                    print(f"     Статус: {post.get('status', 'N/A')}")
                    print()
        else:
            print("❌ Google Sheets: не подключен")
        
        # Проверяем Telegram
        if await automation.telegram_client.test_connection():
            print("✅ Telegram: подключен")
        else:
            print("❌ Telegram: не подключен")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка проверки системы: {e}")
        return False

async def main():
    """Основная функция"""
    print("🔧 ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА СИСТЕМЫ")
    print("=" * 60)
    
    # Проверяем статус системы
    await check_system_status()
    
    # Принудительно публикуем пост
    success = await force_publish_now()
    
    if success:
        print(f"\n🎉 СИСТЕМА РАБОТАЕТ!")
    else:
        print(f"\n❌ СИСТЕМА НЕ РАБОТАЕТ!")

if __name__ == "__main__":
    asyncio.run(main())
