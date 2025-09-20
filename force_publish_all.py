#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Принудительно публикует все посты, готовые к публикации
"""
import os
import sys
import asyncio
from datetime import datetime, timedelta
import pytz

async def force_publish_all_posts():
    """Принудительно публикует все посты"""
    print("🚀 ПРИНУДИТЕЛЬНАЯ ПУБЛИКАЦИЯ ВСЕХ ПОСТОВ")
    print("=" * 60)
    
    try:
        from main import TelegramAutomation
        
        # Инициализируем систему
        print("🔧 Инициализация системы...")
        automation = TelegramAutomation()
        await automation.initialize()
        
        print("✅ Система инициализирована")
        
        # Получаем все посты со статусом "Ожидает"
        print("📋 Получаем посты из Google Sheets...")
        pending_posts = automation.sheets_client.get_pending_posts()
        
        if not pending_posts:
            print("❌ Нет постов со статусом 'Ожидает'")
            return False
        
        print(f"📊 Найдено постов: {len(pending_posts)}")
        
        # Показываем все посты
        print(f"\n📝 ВСЕ ПОСТЫ СО СТАТУСОМ 'ОЖИДАЕТ':")
        for i, post in enumerate(pending_posts):
            print(f"   {i+1}. Строка {post.get('row_index', 'N/A')}")
            print(f"      Дата: {post.get('date', 'N/A')}")
            print(f"      Время: {post.get('time', 'N/A')}")
            print(f"      Текст: {post.get('text', 'N/A')[:50]}...")
            print()
        
        # Публикуем все посты принудительно
        print(f"📱 ПУБЛИКУЕМ ВСЕ ПОСТЫ ПРИНУДИТЕЛЬНО...")
        published_count = 0
        error_count = 0
        
        for i, post in enumerate(pending_posts):
            try:
                print(f"\n🔍 Публикуем пост {i+1}/{len(pending_posts)}:")
                print(f"   Строка: {post.get('row_index', 'N/A')}")
                print(f"   Дата: {post.get('date', 'N/A')}")
                print(f"   Время: {post.get('time', 'N/A')}")
                
                # Публикуем пост
                success = await automation.publish_post(post)
                
                if success:
                    published_count += 1
                    print(f"   ✅ УСПЕШНО ОПУБЛИКОВАН")
                else:
                    error_count += 1
                    print(f"   ❌ ОШИБКА ПУБЛИКАЦИИ")
                
            except Exception as e:
                error_count += 1
                print(f"   ❌ ОШИБКА: {e}")
        
        # Итоговый отчет
        print(f"\n📊 ИТОГОВЫЙ ОТЧЕТ:")
        print(f"   Всего постов: {len(pending_posts)}")
        print(f"   Опубликовано: {published_count}")
        print(f"   Ошибок: {error_count}")
        
        if published_count > 0:
            print(f"\n🎉 УСПЕШНО ОПУБЛИКОВАНО {published_count} ПОСТОВ!")
            print(f"📱 Проверьте канал: -1002907282373")
            return True
        else:
            print(f"\n❌ НЕ УДАЛОСЬ ОПУБЛИКОВАТЬ НИ ОДНОГО ПОСТА")
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
            print(f"📊 Постов со статусом 'Ожидает': {len(posts)}")
            
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
    print("🔧 ПРИНУДИТЕЛЬНАЯ ПУБЛИКАЦИЯ ВСЕХ ПОСТОВ")
    print("=" * 70)
    
    # Проверяем статус системы
    await check_system_status()
    
    # Принудительно публикуем все посты
    success = await force_publish_all_posts()
    
    if success:
        print(f"\n🎉 СИСТЕМА РАБОТАЕТ!")
        print(f"📱 Проверьте канал -1002907282373")
    else:
        print(f"\n❌ СИСТЕМА НЕ РАБОТАЕТ!")
        print(f"🔧 Запустите диагностику: python full_diagnosis.py")

if __name__ == "__main__":
    asyncio.run(main())
