#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Диагностический скрипт для проверки всех компонентов системы
"""
import os
import sys
import asyncio
from datetime import datetime, timedelta
import pytz

# Добавляем текущую директорию в путь
sys.path.append('.')

def check_environment_variables():
    """Проверяет переменные окружения"""
    print("🔍 ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
    print("=" * 50)
    
    required_vars = {
        'TELEGRAM_BOT_TOKEN': 'Telegram Bot Token',
        'TELEGRAM_CHANNEL_ID': 'Telegram Channel ID',
        'GOOGLE_SHEET_ID': 'Google Sheet ID',
        'GOOGLE_CREDENTIALS_JSON': 'Google Service Account JSON',
        'OPENROUTER_API_KEY': 'OpenRouter API Key'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            print(f"❌ {var}: НЕ УСТАНОВЛЕН ({description})")
            missing_vars.append(var)
        else:
            # Показываем только первые и последние символы для безопасности
            masked_value = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "***"
            print(f"✅ {var}: OK ({masked_value})")
    
    if missing_vars:
        print(f"\n❌ ОТСУТСТВУЮТ: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ Все переменные окружения установлены")
        return True

def check_google_sheets():
    """Проверяет подключение к Google Sheets"""
    print("\n🔍 ПРОВЕРКА GOOGLE SHEETS")
    print("=" * 50)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        
        client = GoogleSheetsClient()
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        print("✅ Google Sheets API инициализирован")
        
        # Проверяем получение постов
        posts = client.get_pending_posts()
        print(f"📊 Найдено постов со статусом 'Ожидает': {len(posts)}")
        
        if posts:
            print("\n📝 Первые 3 поста:")
            for i, post in enumerate(posts[:3]):
                print(f"  {i+1}. Строка {post.get('row_index', 'N/A')}: {post.get('date', 'N/A')} {post.get('time', 'N/A')}")
                print(f"     Статус: {post.get('status', 'N/A')}")
                print(f"     Текст: {post.get('text', 'N/A')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Google Sheets: {e}")
        return False

def check_telegram():
    """Проверяет подключение к Telegram"""
    print("\n🔍 ПРОВЕРКА TELEGRAM")
    print("=" * 50)
    
    try:
        from telegram_client import TelegramClient
        
        client = TelegramClient()
        
        # Тестируем подключение
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(client.test_connection())
            if result:
                print("✅ Telegram Bot API подключен")
                return True
            else:
                print("❌ Ошибка подключения к Telegram Bot API")
                return False
        finally:
            loop.close()
            
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")
        return False

def check_time_logic():
    """Проверяет логику времени"""
    print("\n🔍 ПРОВЕРКА ЛОГИКИ ВРЕМЕНИ")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"🕐 Текущее время (Москва): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Создаем тестовый пост на 1 минуту в будущем
        test_post = {
            'date': current_time.strftime('%d.%m.%y'),
            'time': (current_time + timedelta(minutes=1)).strftime('%H:%M'),
            'row_index': 999
        }
        
        print(f"📝 Тестовый пост: {test_post['date']} {test_post['time']}")
        
        should_publish = automation._should_publish_post(test_post, current_time)
        print(f"✅ Должен публиковаться: {should_publish}")
        
        return should_publish
        
    except Exception as e:
        print(f"❌ Ошибка проверки времени: {e}")
        return False

def check_notification_system():
    """Проверяет систему уведомлений"""
    print("\n🔍 ПРОВЕРКА СИСТЕМЫ УВЕДОМЛЕНИЙ")
    print("=" * 50)
    
    try:
        from telegram_client import TelegramClient
        from notification_system import NotificationSystem
        
        client = TelegramClient()
        notification_system = NotificationSystem(client)
        
        print("✅ Система уведомлений инициализирована")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка системы уведомлений: {e}")
        return False

def run_full_diagnostic():
    """Запускает полную диагностику"""
    print("🔧 ДИАГНОСТИКА СИСТЕМЫ АВТОМАТИЗАЦИИ")
    print("=" * 60)
    
    results = {
        'environment': check_environment_variables(),
        'google_sheets': check_google_sheets(),
        'telegram': check_telegram(),
        'time_logic': check_time_logic(),
        'notifications': check_notification_system()
    }
    
    print("\n📊 РЕЗУЛЬТАТЫ ДИАГНОСТИКИ")
    print("=" * 50)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.upper()}: {'OK' if status else 'ERROR'}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n🎉 ВСЕ КОМПОНЕНТЫ РАБОТАЮТ КОРРЕКТНО!")
    else:
        print("\n⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        print("Исправьте ошибки выше и запустите диагностику снова.")
    
    return all_ok

if __name__ == "__main__":
    run_full_diagnostic()
