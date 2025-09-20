#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Добавляет тестовый пост, который должен быть опубликован прямо сейчас
"""
import os
import sys
from datetime import datetime, timedelta
import pytz

def add_test_post_now():
    """Добавляет тестовый пост на прямо сейчас"""
    print("🚀 ДОБАВЛЕНИЕ ТЕСТОВОГО ПОСТА НА ПРЯМО СЕЙЧАС")
    print("=" * 60)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        from config import STATUS_PENDING
        
        # Инициализируем клиент
        client = GoogleSheetsClient()
        
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        # Текущее время по Москве
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"🕐 Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
        
        # Создаем тестовый пост на прямо сейчас
        test_post = {
            "date": current_time.strftime("%d.%m.%y"),
            "time": current_time.strftime("%H:%M"),
            "text": f"<b>🚀 ТЕСТОВЫЙ ПОСТ НА ПРЯМО СЕЙЧАС</b><br><br>Этот пост должен быть опубликован немедленно, так как он запланирован на текущее время.<br><br><i>Время публикации:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        }
        
        print(f"\n📝 Тестовый пост:")
        print(f"   Дата: {test_post['date']}")
        print(f"   Время: {test_post['time']}")
        print(f"   Статус: {test_post['status']}")
        print(f"   Текст: {test_post['text'][:100]}...")
        
        # Добавляем пост в Google Sheets
        print(f"\n📋 Добавляем пост в Google Sheets...")
        result = client.add_post(test_post)
        
        if result:
            print(f"✅ Пост успешно добавлен в Google Sheets")
            print(f"🎯 Пост должен быть опубликован в течение 2 минут")
            return True
        else:
            print(f"❌ Ошибка добавления поста в Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def add_test_post_past():
    """Добавляет тестовый пост на 1 минуту назад"""
    print("\n🕐 ДОБАВЛЕНИЕ ТЕСТОВОГО ПОСТА НА 1 МИНУТУ НАЗАД")
    print("=" * 60)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        from config import STATUS_PENDING
        
        # Инициализируем клиент
        client = GoogleSheetsClient()
        
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        # Время 1 минуту назад
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        past_time = current_time - timedelta(minutes=1)
        
        print(f"🕐 Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
        print(f"🕐 Время поста: {past_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
        
        # Создаем тестовый пост на 1 минуту назад
        test_post = {
            "date": past_time.strftime("%d.%m.%y"),
            "time": past_time.strftime("%H:%M"),
            "text": f"<b>⏰ ТЕСТОВЫЙ ПОСТ НА 1 МИНУТУ НАЗАД</b><br><br>Этот пост был запланирован на 1 минуту назад и должен быть опубликован немедленно.<br><br><i>Запланирован на:</i> {past_time.strftime('%H:%M:%S MSK')}<br><i>Текущее время:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        }
        
        print(f"\n📝 Тестовый пост:")
        print(f"   Дата: {test_post['date']}")
        print(f"   Время: {test_post['time']}")
        print(f"   Статус: {test_post['status']}")
        print(f"   Текст: {test_post['text'][:100]}...")
        
        # Добавляем пост в Google Sheets
        print(f"\n📋 Добавляем пост в Google Sheets...")
        result = client.add_post(test_post)
        
        if result:
            print(f"✅ Пост успешно добавлен в Google Sheets")
            print(f"🎯 Пост должен быть опубликован в течение 2 минут")
            return True
        else:
            print(f"❌ Ошибка добавления поста в Google Sheets")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция"""
    print("🧪 ДОБАВЛЕНИЕ ТЕСТОВЫХ ПОСТОВ ДЛЯ ПРОВЕРКИ СИСТЕМЫ")
    print("=" * 70)
    
    # Добавляем пост на прямо сейчас
    success1 = add_test_post_now()
    
    # Добавляем пост на 1 минуту назад
    success2 = add_test_post_past()
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Пост на сейчас: {'✅ OK' if success1 else '❌ ERROR'}")
    print(f"   Пост на -1 мин: {'✅ OK' if success2 else '❌ ERROR'}")
    
    if success1 or success2:
        print(f"\n🎉 ТЕСТОВЫЕ ПОСТЫ ДОБАВЛЕНЫ!")
        print(f"⏰ Проверьте Telegram-канал в течение 2 минут")
        print(f"📱 Посты должны появиться автоматически")
    else:
        print(f"\n❌ НЕ УДАЛОСЬ ДОБАВИТЬ ТЕСТОВЫЕ ПОСТЫ")

if __name__ == "__main__":
    main()
