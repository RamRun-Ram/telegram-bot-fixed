#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Создает тестовые посты, которые должны быть опубликованы немедленно
"""
import os
import sys
from datetime import datetime, timedelta
import pytz

def create_immediate_test_posts():
    """Создает тестовые посты на прямо сейчас и в прошлом"""
    print("🚀 СОЗДАНИЕ ТЕСТОВЫХ ПОСТОВ ДЛЯ НЕМЕДЛЕННОЙ ПУБЛИКАЦИИ")
    print("=" * 70)
    
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
        
        # Создаем тестовые посты
        test_posts = []
        
        # Пост 1: На прямо сейчас
        post1_time = current_time
        test_posts.append({
            "date": post1_time.strftime("%d.%m.%Y"),
            "time": post1_time.strftime("%H:%M"),
            "text": f"<b>🚀 ТЕСТОВЫЙ ПОСТ #1 - ПРЯМО СЕЙЧАС</b><br><br>Этот пост запланирован на текущее время и должен быть опубликован немедленно.<br><br><i>Время публикации:</i> {post1_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        })
        
        # Пост 2: На 1 минуту назад
        post2_time = current_time - timedelta(minutes=1)
        test_posts.append({
            "date": post2_time.strftime("%d.%m.%Y"),
            "time": post2_time.strftime("%H:%M"),
            "text": f"<b>⏰ ТЕСТОВЫЙ ПОСТ #2 - 1 МИНУТУ НАЗАД</b><br><br>Этот пост был запланирован на 1 минуту назад и должен быть опубликован немедленно.<br><br><i>Запланирован на:</i> {post2_time.strftime('%H:%M:%S MSK')}<br><i>Текущее время:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        })
        
        # Пост 3: На 2 минуты назад
        post3_time = current_time - timedelta(minutes=2)
        test_posts.append({
            "date": post3_time.strftime("%d.%m.%Y"),
            "time": post3_time.strftime("%H:%M"),
            "text": f"<b>📅 ТЕСТОВЫЙ ПОСТ #3 - 2 МИНУТЫ НАЗАД</b><br><br>Этот пост был запланирован на 2 минуты назад и должен быть опубликован немедленно.<br><br><i>Запланирован на:</i> {post3_time.strftime('%H:%M:%S MSK')}<br><i>Текущее время:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        })
        
        # Пост 4: На 3 минуты назад
        post4_time = current_time - timedelta(minutes=3)
        test_posts.append({
            "date": post4_time.strftime("%d.%m.%Y"),
            "time": post4_time.strftime("%H:%M"),
            "text": f"<b>🔔 ТЕСТОВЫЙ ПОСТ #4 - 3 МИНУТЫ НАЗАД</b><br><br>Этот пост был запланирован на 3 минуты назад и должен быть опубликован немедленно.<br><br><i>Запланирован на:</i> {post4_time.strftime('%H:%M:%S MSK')}<br><i>Текущее время:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        })
        
        # Пост 5: На 4 минуты назад
        post5_time = current_time - timedelta(minutes=4)
        test_posts.append({
            "date": post5_time.strftime("%d.%m.%Y"),
            "time": post5_time.strftime("%H:%M"),
            "text": f"<b>🎯 ТЕСТОВЫЙ ПОСТ #5 - 4 МИНУТЫ НАЗАД</b><br><br>Этот пост был запланирован на 4 минуты назад и должен быть опубликован немедленно.<br><br><i>Запланирован на:</i> {post5_time.strftime('%H:%M:%S MSK')}<br><i>Текущее время:</i> {current_time.strftime('%H:%M:%S MSK')}<br><br>Если вы видите этот пост, значит система работает правильно!",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        })
        
        print(f"\n📝 СОЗДАНЫ ТЕСТОВЫЕ ПОСТЫ:")
        for i, post in enumerate(test_posts, 1):
            print(f"   {i}. Дата: {post['date']}, Время: {post['time']}")
            print(f"      Текст: {post['text'][:60]}...")
            print()
        
        # Добавляем посты в Google Sheets
        print(f"📋 ДОБАВЛЯЕМ ПОСТЫ В GOOGLE SHEETS...")
        success_count = 0
        
        for i, post in enumerate(test_posts):
            try:
                result = client.add_post(post)
                if result:
                    print(f"   ✅ Пост {i+1}/5 добавлен: {post['date']} {post['time']}")
                    success_count += 1
                else:
                    print(f"   ❌ Ошибка добавления поста {i+1}/5")
            except Exception as e:
                print(f"   ❌ Ошибка добавления поста {i+1}/5: {e}")
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Успешно добавлено: {success_count}/{len(test_posts)}")
        
        if success_count > 0:
            print(f"\n🎯 ТЕСТОВЫЕ ПОСТЫ ДОБАВЛЕНЫ!")
            print(f"⏰ Все посты должны быть опубликованы в течение 2 минут")
            print(f"📱 Проверьте канал: t.me/sovpalitest")
            print(f"🆔 ID канала: -1002907282373")
            return True
        else:
            print(f"\n❌ НЕ УДАЛОСЬ ДОБАВИТЬ ТЕСТОВЫЕ ПОСТЫ")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_channel_id():
    """Проверяет ID канала в конфигурации"""
    print("\n🔍 ПРОВЕРКА ID КАНАЛА")
    print("=" * 50)
    
    try:
        from config import TELEGRAM_CHANNEL_ID
        
        print(f"📱 ID канала в конфигурации: {TELEGRAM_CHANNEL_ID}")
        print(f"🎯 Ожидаемый ID: -1002907282373")
        
        if TELEGRAM_CHANNEL_ID == "-1002907282373":
            print(f"✅ ID канала правильный")
            return True
        else:
            print(f"❌ ID канала неправильный!")
            print(f"💡 Нужно обновить TELEGRAM_CHANNEL_ID в Railway")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки ID канала: {e}")
        return False

def main():
    """Основная функция"""
    print("🧪 СОЗДАНИЕ ТЕСТОВЫХ ПОСТОВ ДЛЯ НЕМЕДЛЕННОЙ ПУБЛИКАЦИИ")
    print("=" * 80)
    
    # Проверяем ID канала
    channel_ok = verify_channel_id()
    
    if not channel_ok:
        print(f"\n⚠️ ВНИМАНИЕ: ID канала неправильный!")
        print(f"🔧 Обновите TELEGRAM_CHANNEL_ID в Railway на -1002907282373")
        print(f"📱 Или измените в config.py")
    
    # Создаем тестовые посты
    success = create_immediate_test_posts()
    
    if success:
        print(f"\n🎉 ТЕСТОВЫЕ ПОСТЫ СОЗДАНЫ!")
        print(f"⏰ Подождите 2 минуты и проверьте канал t.me/sovpalitest")
        print(f"📱 Должно появиться 5 тестовых постов")
    else:
        print(f"\n❌ НЕ УДАЛОСЬ СОЗДАТЬ ТЕСТОВЫЕ ПОСТЫ")

if __name__ == "__main__":
    main()
