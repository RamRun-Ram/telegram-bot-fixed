#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для принудительной публикации поста
"""
import asyncio
import sys
from datetime import datetime, timedelta
import pytz

# Добавляем текущую директорию в путь
sys.path.append('.')

async def force_publish_post():
    """Принудительно публикует первый доступный пост"""
    try:
        from main import TelegramAutomation
        
        print("🚀 ПРИНУДИТЕЛЬНАЯ ПУБЛИКАЦИЯ ПОСТА")
        print("=" * 50)
        
        # Инициализируем систему
        automation = TelegramAutomation()
        
        print("🔧 Инициализация системы...")
        if not await automation.initialize():
            print("❌ Ошибка инициализации системы")
            return False
        
        print("✅ Система инициализирована")
        
        # Получаем посты
        print("📋 Получение постов из Google Sheets...")
        pending_posts = automation.sheets_client.get_pending_posts()
        
        if not pending_posts:
            print("❌ Нет постов для публикации")
            return False
        
        print(f"📊 Найдено {len(pending_posts)} постов")
        
        # Показываем все посты
        print("\n📝 ВСЕ ПОСТЫ:")
        for i, post in enumerate(pending_posts):
            print(f"  {i+1}. Строка {post.get('row_index', 'N/A')}: {post.get('date', 'N/A')} {post.get('time', 'N/A')}")
            print(f"     Статус: {post.get('status', 'N/A')}")
            print(f"     Текст: {post.get('text', 'N/A')[:100]}...")
            print()
        
        # Берем первый пост
        first_post = pending_posts[0]
        print(f"🎯 Публикуем первый пост (строка {first_post.get('row_index', 'N/A')})")
        
        # Принудительно публикуем
        success = await automation.publish_post(first_post)
        
        if success:
            print("✅ Пост успешно опубликован!")
        else:
            print("❌ Ошибка публикации поста")
        
        return success
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_time_logic():
    """Тестирует логику времени"""
    print("\n🕐 ТЕСТИРОВАНИЕ ЛОГИКИ ВРЕМЕНИ")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Тестируем разные сценарии
        test_cases = [
            ("Сейчас", current_time),
            ("+1 минута", current_time + timedelta(minutes=1)),
            ("+2 минуты", current_time + timedelta(minutes=2)),
            ("+5 минут", current_time + timedelta(minutes=5)),
            ("+10 минут", current_time + timedelta(minutes=10)),
            ("-1 минута", current_time - timedelta(minutes=1)),
            ("-5 минут", current_time - timedelta(minutes=5)),
        ]
        
        for name, test_time in test_cases:
            test_post = {
                'date': test_time.strftime('%d.%m.%y'),
                'time': test_time.strftime('%H:%M'),
                'row_index': 999
            }
            
            should_publish = automation._should_publish_post(test_post, current_time)
            status = "✅ ДА" if should_publish else "❌ НЕТ"
            print(f"  {name}: {status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования времени: {e}")
        return False

async def main():
    """Основная функция"""
    print("🔧 ДИАГНОСТИКА И ПРИНУДИТЕЛЬНАЯ ПУБЛИКАЦИЯ")
    print("=" * 60)
    
    # Тестируем логику времени
    await test_time_logic()
    
    # Принудительно публикуем пост
    success = await force_publish_post()
    
    if success:
        print("\n🎉 УСПЕХ! Пост опубликован!")
    else:
        print("\n❌ ОШИБКА! Пост не опубликован!")

if __name__ == "__main__":
    asyncio.run(main())
