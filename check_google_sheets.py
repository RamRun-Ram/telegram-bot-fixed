#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для проверки Google Sheets
"""
import os
import sys
from datetime import datetime, timedelta
import pytz

def check_google_sheets():
    """Проверяет Google Sheets"""
    print("📋 ПРОВЕРКА GOOGLE SHEETS")
    print("=" * 50)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        
        # Инициализируем клиент
        client = GoogleSheetsClient()
        
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        print("✅ Google Sheets API инициализирован")
        
        # Получаем все посты
        posts = client.get_all_posts()
        print(f"📊 Всего постов в таблице: {len(posts)}")
        
        if posts:
            print(f"\n📝 ПОСТЫ В ТАБЛИЦЕ:")
            for i, post in enumerate(posts[:10]):  # Показываем первые 10
                print(f"  {i+1}. Строка {post.get('row_index', 'N/A')}")
                print(f"     Дата: {post.get('date', 'N/A')}")
                print(f"     Время: {post.get('time', 'N/A')}")
                print(f"     Статус: {post.get('status', 'N/A')}")
                print(f"     Текст: {post.get('text', 'N/A')[:50]}...")
                print()
        
        # Получаем посты со статусом "Ожидает"
        pending_posts = client.get_pending_posts()
        print(f"⏰ Постов со статусом 'Ожидает': {len(pending_posts)}")
        
        if pending_posts:
            print(f"\n⏰ ПОСТЫ СО СТАТУСОМ 'ОЖИДАЕТ':")
            for i, post in enumerate(pending_posts):
                print(f"  {i+1}. Строка {post.get('row_index', 'N/A')}")
                print(f"     Дата: {post.get('date', 'N/A')}")
                print(f"     Время: {post.get('time', 'N/A')}")
                print(f"     Текст: {post.get('text', 'N/A')[:50]}...")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_time_logic_for_posts():
    """Проверяет логику времени для постов"""
    print("\n🕐 ПРОВЕРКА ЛОГИКИ ВРЕМЕНИ ДЛЯ ПОСТОВ")
    print("=" * 50)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"🕐 Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
        
        # Получаем посты
        posts = automation.sheets_client.get_pending_posts()
        
        if not posts:
            print("❌ Нет постов со статусом 'Ожидает'")
            return False
        
        print(f"📊 Найдено постов: {len(posts)}")
        
        # Проверяем каждый пост
        posts_to_publish = []
        for post in posts:
            print(f"\n🔍 Проверяем пост из строки {post.get('row_index', 'N/A')}:")
            print(f"   Дата: {post.get('date', 'N/A')}")
            print(f"   Время: {post.get('time', 'N/A')}")
            
            # Проверяем логику времени
            if automation._should_publish_post(post, current_time):
                posts_to_publish.append(post)
                print(f"   ✅ ДОЛЖЕН ПУБЛИКОВАТЬСЯ")
            else:
                print(f"   ❌ НЕ ПОДХОДИТ ПО ВРЕМЕНИ")
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Всего постов: {len(posts)}")
        print(f"   К публикации: {len(posts_to_publish)}")
        
        return len(posts_to_publish) > 0
        
    except Exception as e:
        print(f"❌ Ошибка проверки времени: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция"""
    print("🔧 ПРОВЕРКА GOOGLE SHEETS И ЛОГИКИ ВРЕМЕНИ")
    print("=" * 60)
    
    # Проверяем Google Sheets
    sheets_ok = check_google_sheets()
    
    if sheets_ok:
        # Проверяем логику времени
        time_ok = check_time_logic_for_posts()
        
        print(f"\n📊 РЕЗУЛЬТАТЫ:")
        print(f"   Google Sheets: {'OK' if sheets_ok else 'ERROR'}")
        print(f"   Логика времени: {'OK' if time_ok else 'ERROR'}")
        
        if time_ok:
            print(f"\n🎉 СИСТЕМА ДОЛЖНА РАБОТАТЬ!")
        else:
            print(f"\n⚠️ ПРОБЛЕМА С ЛОГИКОЙ ВРЕМЕНИ!")
    else:
        print(f"\n❌ ПРОБЛЕМА С GOOGLE SHEETS!")

if __name__ == "__main__":
    main()
