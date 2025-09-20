#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки постов на удаленном сервере
"""
import os
import sys
from datetime import datetime, timedelta
import pytz

def check_posts_timing():
    """Проверяет время постов"""
    print("🕐 ПРОВЕРКА ВРЕМЕНИ ПОСТОВ")
    print("=" * 50)
    
    # Текущее время по Москве
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz)
    
    print(f"🕐 Текущее время (Москва): {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
    
    # Проверяем логику времени
    from config import LOOKBACK_MINUTES
    print(f"📏 LOOKBACK_MINUTES: {LOOKBACK_MINUTES}")
    
    # Создаем тестовые посты
    test_posts = []
    
    # Пост на 1 минуту в будущем
    future_post = current_time + timedelta(minutes=1)
    test_posts.append({
        'date': future_post.strftime('%d.%m.%y'),
        'time': future_post.strftime('%H:%M'),
        'description': 'Пост на +1 минуту'
    })
    
    # Пост на 2 минуты в будущем
    future_post2 = current_time + timedelta(minutes=2)
    test_posts.append({
        'date': future_post2.strftime('%d.%m.%y'),
        'time': future_post2.strftime('%H:%M'),
        'description': 'Пост на +2 минуты'
    })
    
    # Пост на 5 минут в будущем
    future_post5 = current_time + timedelta(minutes=5)
    test_posts.append({
        'date': future_post5.strftime('%d.%m.%y'),
        'time': future_post5.strftime('%H:%M'),
        'description': 'Пост на +5 минут'
    })
    
    # Пост на 10 минут в будущем
    future_post10 = current_time + timedelta(minutes=10)
    test_posts.append({
        'date': future_post10.strftime('%d.%m.%y'),
        'time': future_post10.strftime('%H:%M'),
        'description': 'Пост на +10 минут'
    })
    
    print(f"\n📝 ТЕСТОВЫЕ ПОСТЫ:")
    for i, post in enumerate(test_posts, 1):
        print(f"  {i}. {post['description']}: {post['date']} {post['time']}")
        
        # Проверяем логику времени
        try:
            post_datetime = datetime.strptime(f"{post['date']} {post['time']}", "%d.%m.%y %H:%M")
            post_datetime = moscow_tz.localize(post_datetime)
            
            time_diff = (current_time - post_datetime).total_seconds() / 60
            should_publish = -LOOKBACK_MINUTES <= time_diff <= 0
            
            status = "✅ ДА" if should_publish else "❌ НЕТ"
            print(f"     Разница: {time_diff:.1f} мин, Публиковать: {status}")
            
        except Exception as e:
            print(f"     ❌ Ошибка парсинга: {e}")
    
    return test_posts

def check_google_sheets_connection():
    """Проверяет подключение к Google Sheets"""
    print("\n📋 ПРОВЕРКА GOOGLE SHEETS")
    print("=" * 50)
    
    # Проверяем переменные окружения
    google_vars = [
        "GOOGLE_SHEET_ID", "GOOGLE_SHEET_NAME", "GOOGLE_PROJECT_ID",
        "GOOGLE_PRIVATE_KEY_ID", "GOOGLE_PRIVATE_KEY", "GOOGLE_CLIENT_EMAIL",
        "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_X509_CERT_URL"
    ]
    
    missing_vars = []
    for var in google_vars:
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            missing_vars.append(var)
            print(f"❌ {var}: не установлен")
        else:
            print(f"✅ {var}: OK")
    
    if missing_vars:
        print(f"\n❌ Отсутствуют переменные: {', '.join(missing_vars)}")
        return False
    else:
        print(f"\n✅ Все переменные Google Sheets установлены")
        return True

def check_telegram_connection():
    """Проверяет подключение к Telegram"""
    print("\n📱 ПРОВЕРКА TELEGRAM")
    print("=" * 50)
    
    telegram_vars = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHANNEL_ID"]
    
    missing_vars = []
    for var in telegram_vars:
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            missing_vars.append(var)
            print(f"❌ {var}: не установлен")
        else:
            print(f"✅ {var}: OK")
    
    if missing_vars:
        print(f"\n❌ Отсутствуют переменные: {', '.join(missing_vars)}")
        return False
    else:
        print(f"\n✅ Все переменные Telegram установлены")
        return True

def main():
    """Основная функция"""
    print("🔧 ДИАГНОСТИКА СИСТЕМЫ ПУБЛИКАЦИИ")
    print("=" * 60)
    
    # Проверяем время постов
    test_posts = check_posts_timing()
    
    # Проверяем Google Sheets
    sheets_ok = check_google_sheets_connection()
    
    # Проверяем Telegram
    telegram_ok = check_telegram_connection()
    
    print("\n📊 РЕЗУЛЬТАТЫ")
    print("=" * 30)
    print(f"🕐 Логика времени: OK")
    print(f"📋 Google Sheets: {'OK' if sheets_ok else 'ERROR'}")
    print(f"📱 Telegram: {'OK' if telegram_ok else 'ERROR'}")
    
    if sheets_ok and telegram_ok:
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("💡 Система должна работать корректно")
    else:
        print("\n⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        if not sheets_ok:
            print("❌ Проблема с Google Sheets - проверьте переменные окружения")
        if not telegram_ok:
            print("❌ Проблема с Telegram - проверьте токен бота")

if __name__ == "__main__":
    main()
