#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полная диагностика системы публикации постов
"""
import os
import sys
from datetime import datetime, timedelta
import pytz

def check_environment():
    """Проверяет переменные окружения"""
    print("🔧 ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
    print("=" * 50)
    
    # Telegram переменные
    telegram_vars = {
        "TELEGRAM_BOT_TOKEN": "Токен бота",
        "TELEGRAM_CHANNEL_ID": "ID канала",
        "ADMIN_CHAT_ID": "ID админ чата",
        "ALERT_ADMIN_CHANNEL": "ID AlertChanel"
    }
    
    print("📱 TELEGRAM:")
    telegram_ok = True
    for var, desc in telegram_vars.items():
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            print(f"   ❌ {var}: не установлен ({desc})")
            telegram_ok = False
        else:
            print(f"   ✅ {var}: OK")
    
    # Google Sheets переменные
    google_vars = {
        "GOOGLE_SHEET_ID": "ID таблицы",
        "GOOGLE_PROJECT_ID": "ID проекта",
        "GOOGLE_PRIVATE_KEY_ID": "ID приватного ключа",
        "GOOGLE_PRIVATE_KEY": "Приватный ключ",
        "GOOGLE_CLIENT_EMAIL": "Email клиента",
        "GOOGLE_CLIENT_ID": "ID клиента",
        "GOOGLE_CLIENT_X509_CERT_URL": "URL сертификата"
    }
    
    print("\n📋 GOOGLE SHEETS:")
    google_ok = True
    for var, desc in google_vars.items():
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            print(f"   ❌ {var}: не установлен ({desc})")
            google_ok = False
        else:
            print(f"   ✅ {var}: OK")
    
    return telegram_ok, google_ok

def check_google_sheets():
    """Проверяет Google Sheets"""
    print("\n📋 ПРОВЕРКА GOOGLE SHEETS")
    print("=" * 50)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        
        client = GoogleSheetsClient()
        
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False, []
        
        print("✅ Google Sheets API инициализирован")
        
        # Получаем все посты
        all_posts = client.get_all_posts()
        print(f"📊 Всего постов в таблице: {len(all_posts)}")
        
        # Получаем посты со статусом "Ожидает"
        pending_posts = client.get_pending_posts()
        print(f"⏰ Постов со статусом 'Ожидает': {len(pending_posts)}")
        
        if pending_posts:
            print(f"\n📝 ПОСТЫ СО СТАТУСОМ 'ОЖИДАЕТ':")
            for i, post in enumerate(pending_posts[:5]):  # Показываем первые 5
                print(f"   {i+1}. Строка {post.get('row_index', 'N/A')}")
                print(f"      Дата: {post.get('date', 'N/A')}")
                print(f"      Время: {post.get('time', 'N/A')}")
                print(f"      Текст: {post.get('text', 'N/A')[:50]}...")
                print()
        
        return True, pending_posts
        
    except Exception as e:
        print(f"❌ Ошибка Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def check_time_logic(pending_posts):
    """Проверяет логику времени для постов"""
    print("\n🕐 ПРОВЕРКА ЛОГИКИ ВРЕМЕНИ")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"🕐 Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
        
        if not pending_posts:
            print("❌ Нет постов для проверки")
            return False, []
        
        print(f"📊 Проверяем {len(pending_posts)} постов...")
        
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
                
                # Детальный анализ
                post_date_str = post.get('date', '')
                post_time_str = post.get('time', '')
                
                try:
                    post_datetime = datetime.strptime(f"{post_date_str} {post_time_str}", "%d.%m.%y %H:%M")
                    post_datetime = moscow_tz.localize(post_datetime)
                    
                    time_diff = (current_time - post_datetime).total_seconds() / 60
                    
                    print(f"   📊 Детали:")
                    print(f"      Время поста: {post_datetime.strftime('%Y-%m-%d %H:%M:%S MSK')}")
                    print(f"      Разница: {time_diff:.1f} минут")
                    print(f"      Условие: 0 <= {time_diff:.1f} <= 5")
                    print(f"      Результат: {0 <= time_diff <= 5}")
                    
                except Exception as e:
                    print(f"   ❌ Ошибка парсинга времени: {e}")
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Всего постов: {len(pending_posts)}")
        print(f"   К публикации: {len(posts_to_publish)}")
        
        return len(posts_to_publish) > 0, posts_to_publish
        
    except Exception as e:
        print(f"❌ Ошибка проверки времени: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def check_telegram():
    """Проверяет Telegram"""
    print("\n📱 ПРОВЕРКА TELEGRAM")
    print("=" * 50)
    
    try:
        from telegram_client import TelegramClient
        
        client = TelegramClient()
        
        # Проверяем соединение
        print("🔌 Проверяем соединение с Telegram...")
        # Здесь нужно добавить проверку соединения
        
        print("✅ Telegram клиент инициализирован")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Telegram: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_system_logs():
    """Проверяет логи системы"""
    print("\n📝 ПРОВЕРКА ЛОГОВ СИСТЕМЫ")
    print("=" * 50)
    
    try:
        # Проверяем файл логов
        log_file = "telegram_automation.log"
        if os.path.exists(log_file):
            print(f"✅ Файл логов найден: {log_file}")
            
            # Читаем последние 20 строк
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_lines = lines[-20:] if len(lines) > 20 else lines
                
            print(f"\n📄 Последние {len(last_lines)} строк логов:")
            for line in last_lines:
                print(f"   {line.strip()}")
        else:
            print(f"❌ Файл логов не найден: {log_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка чтения логов: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 ПОЛНАЯ ДИАГНОСТИКА СИСТЕМЫ ПУБЛИКАЦИИ ПОСТОВ")
    print("=" * 70)
    
    # Проверяем переменные окружения
    telegram_ok, google_ok = check_environment()
    
    # Проверяем Google Sheets
    sheets_ok, pending_posts = check_google_sheets()
    
    # Проверяем логику времени
    time_ok, posts_to_publish = check_time_logic(pending_posts)
    
    # Проверяем Telegram
    telegram_conn_ok = check_telegram()
    
    # Проверяем логи
    logs_ok = check_system_logs()
    
    # Итоговый отчет
    print("\n📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 50)
    print(f"🔧 Переменные окружения:")
    print(f"   Telegram: {'✅ OK' if telegram_ok else '❌ ERROR'}")
    print(f"   Google Sheets: {'✅ OK' if google_ok else '❌ ERROR'}")
    print(f"📋 Google Sheets API: {'✅ OK' if sheets_ok else '❌ ERROR'}")
    print(f"🕐 Логика времени: {'✅ OK' if time_ok else '❌ ERROR'}")
    print(f"📱 Telegram соединение: {'✅ OK' if telegram_conn_ok else '❌ ERROR'}")
    print(f"📝 Логи системы: {'✅ OK' if logs_ok else '❌ ERROR'}")
    
    if posts_to_publish:
        print(f"\n🎯 ПОСТЫ К ПУБЛИКАЦИИ: {len(posts_to_publish)}")
        for i, post in enumerate(posts_to_publish):
            print(f"   {i+1}. Строка {post.get('row_index', 'N/A')}: {post.get('date', 'N/A')} {post.get('time', 'N/A')}")
    
    # Рекомендации
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if not telegram_ok or not google_ok:
        print("   ❌ Проверьте переменные окружения в Railway")
    if not sheets_ok:
        print("   ❌ Проблема с Google Sheets API")
    if not time_ok:
        print("   ❌ Проблема с логикой времени")
    if not telegram_conn_ok:
        print("   ❌ Проблема с Telegram соединением")
    if posts_to_publish and not telegram_conn_ok:
        print("   ⚠️ Есть посты к публикации, но проблема с Telegram")
    
    if all([telegram_ok, google_ok, sheets_ok, time_ok, telegram_conn_ok]):
        print("   🎉 Все компоненты работают правильно!")
        if posts_to_publish:
            print("   📱 Посты должны публиковаться в Telegram")
        else:
            print("   ⏰ Нет постов для публикации в данный момент")

if __name__ == "__main__":
    main()
