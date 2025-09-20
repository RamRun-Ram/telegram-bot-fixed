#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки часовых поясов и времени
"""
import os
import sys
from datetime import datetime
import pytz

def check_timezones():
    """Проверяет различные часовые пояса"""
    print("🕐 ПРОВЕРКА ЧАСОВЫХ ПОЯСОВ")
    print("=" * 50)
    
    # UTC время
    utc_now = datetime.now(pytz.UTC)
    print(f"🌍 UTC время: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Московское время
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_now = datetime.now(moscow_tz)
    print(f"🇷🇺 Москва время: {moscow_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Локальное время системы
    local_now = datetime.now()
    print(f"💻 Локальное время: {local_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Проверяем разницу
    print(f"\n📊 РАЗНИЦА ВРЕМЕНИ:")
    print(f"Москва - UTC: {moscow_now.utcoffset()}")
    print(f"Москва - Локальное: {(moscow_now - local_now.replace(tzinfo=moscow_tz)).total_seconds() / 3600:.1f} часов")
    
    return moscow_now

def check_system_time_logic():
    """Проверяет логику времени в системе"""
    print("\n🔍 ПРОВЕРКА ЛОГИКИ ВРЕМЕНИ СИСТЕМЫ")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"🕐 Текущее время (система): {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        # Создаем тестовый пост на 1 минуту в будущем
        test_post = {
            'date': current_time.strftime('%d.%m.%y'),
            'time': (current_time + pytz.timedelta(minutes=1)).strftime('%H:%M'),
            'row_index': 999
        }
        
        print(f"📝 Тестовый пост: {test_post['date']} {test_post['time']}")
        
        # Проверяем логику
        should_publish = automation._should_publish_post(test_post, current_time)
        print(f"✅ Должен публиковаться: {should_publish}")
        
        # Детальная проверка
        print(f"\n🔍 ДЕТАЛЬНАЯ ПРОВЕРКА:")
        post_date_str = test_post['date']
        post_time_str = test_post['time']
        
        try:
            post_datetime = datetime.strptime(f"{post_date_str} {post_time_str}", "%d.%m.%Y %H:%M")
            post_datetime = moscow_tz.localize(post_datetime)
            print(f"📅 Время поста: {post_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            
            time_diff = (current_time - post_datetime).total_seconds() / 60
            print(f"⏰ Разница: {time_diff:.1f} минут")
            
            from config import LOOKBACK_MINUTES
            print(f"📏 LOOKBACK_MINUTES: {LOOKBACK_MINUTES}")
            print(f"🎯 Условие: -{LOOKBACK_MINUTES} <= {time_diff:.1f} <= 0")
            print(f"✅ Результат: {-LOOKBACK_MINUTES <= time_diff <= 0}")
            
        except Exception as e:
            print(f"❌ Ошибка парсинга времени: {e}")
        
        return should_publish
        
    except Exception as e:
        print(f"❌ Ошибка проверки системы: {e}")
        return False

def check_google_sheets_posts():
    """Проверяет посты в Google Sheets"""
    print("\n📋 ПРОВЕРКА ПОСТОВ В GOOGLE SHEETS")
    print("=" * 50)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        
        client = GoogleSheetsClient()
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        posts = client.get_pending_posts()
        print(f"📊 Найдено постов: {len(posts)}")
        
        if posts:
            print("\n📝 Первые 3 поста:")
            for i, post in enumerate(posts[:3]):
                print(f"  {i+1}. Строка {post.get('row_index', 'N/A')}")
                print(f"     Дата: {post.get('date', 'N/A')}")
                print(f"     Время: {post.get('time', 'N/A')}")
                print(f"     Статус: {post.get('status', 'N/A')}")
                print(f"     Текст: {post.get('text', 'N/A')[:50]}...")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Google Sheets: {e}")
        return False

def main():
    """Основная функция"""
    print("🔧 ДИАГНОСТИКА ЧАСОВЫХ ПОЯСОВ И ВРЕМЕНИ")
    print("=" * 60)
    
    # Проверяем часовые пояса
    moscow_time = check_timezones()
    
    # Проверяем логику системы
    system_ok = check_system_time_logic()
    
    # Проверяем посты в Google Sheets
    sheets_ok = check_google_sheets_posts()
    
    print("\n📊 РЕЗУЛЬТАТЫ")
    print("=" * 30)
    print(f"🕐 Часовые пояса: OK")
    print(f"🔍 Логика системы: {'OK' if system_ok else 'ERROR'}")
    print(f"📋 Google Sheets: {'OK' if sheets_ok else 'ERROR'}")
    
    if system_ok and sheets_ok:
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
    else:
        print("\n⚠️ ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")

if __name__ == "__main__":
    main()
