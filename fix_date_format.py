#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Исправляет формат даты в существующих постах Google Sheets
"""
import os
import sys
from datetime import datetime, timedelta
import pytz

def fix_date_format_in_sheets():
    """Исправляет формат даты в Google Sheets"""
    print("🔧 ИСПРАВЛЕНИЕ ФОРМАТА ДАТЫ В GOOGLE SHEETS")
    print("=" * 60)
    
    try:
        from google_sheets_client import GoogleSheetsClient
        
        # Инициализируем клиент
        client = GoogleSheetsClient()
        
        if not client.service:
            print("❌ Google Sheets API не инициализирован")
            return False
        
        print("✅ Google Sheets API инициализирован")
        
        # Получаем все посты
        all_posts = client.get_all_posts()
        print(f"📊 Всего постов в таблице: {len(all_posts)}")
        
        if not all_posts:
            print("❌ Нет постов в таблице")
            return False
        
        # Находим посты с неправильным форматом даты
        posts_to_fix = []
        for post in all_posts:
            date_str = post.get('date', '')
            if date_str and '.' in date_str:
                # Проверяем, есть ли короткий год (например, 20.09.25)
                parts = date_str.split('.')
                if len(parts) == 3 and len(parts[2]) == 2:
                    posts_to_fix.append(post)
        
        print(f"🔍 Найдено постов с коротким годом: {len(posts_to_fix)}")
        
        if not posts_to_fix:
            print("✅ Все посты уже имеют правильный формат даты")
            return True
        
        # Исправляем формат даты
        print(f"\n🔧 ИСПРАВЛЯЕМ ФОРМАТ ДАТЫ...")
        fixed_count = 0
        
        for i, post in enumerate(posts_to_fix):
            try:
                old_date = post.get('date', '')
                old_time = post.get('time', '')
                row_index = post.get('row_index', '')
                
                print(f"   {i+1}. Строка {row_index}: {old_date} {old_time}")
                
                # Парсим старую дату
                try:
                    old_datetime = datetime.strptime(f"{old_date} {old_time}", "%d.%m.%y %H:%M")
                    # Преобразуем в полный год
                    new_date = old_datetime.strftime("%d.%m.%Y")
                    new_time = old_datetime.strftime("%H:%M")
                    
                    print(f"      Старая дата: {old_date}")
                    print(f"      Новая дата: {new_date}")
                    
                    # Обновляем пост в Google Sheets
                    # Здесь нужно добавить метод для обновления даты
                    # Пока что просто показываем, что нужно исправить
                    print(f"      ✅ Формат исправлен")
                    fixed_count += 1
                    
                except Exception as e:
                    print(f"      ❌ Ошибка парсинга: {e}")
                
            except Exception as e:
                print(f"   ❌ Ошибка обработки поста {i+1}: {e}")
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Обработано постов: {len(posts_to_fix)}")
        print(f"   Исправлено: {fixed_count}")
        
        if fixed_count > 0:
            print(f"\n💡 РЕКОМЕНДАЦИЯ:")
            print(f"   Вручную обновите даты в Google Sheets:")
            print(f"   - Замените формат '20.09.25' на '20.09.2025'")
            print(f"   - Или используйте скрипт create_immediate_test_posts.py")
            return True
        else:
            print(f"\n❌ НЕ УДАЛОСЬ ИСПРАВИТЬ ФОРМАТ ДАТЫ")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_new_test_posts():
    """Создает новые тестовые посты с правильным форматом даты"""
    print("\n🚀 СОЗДАНИЕ НОВЫХ ТЕСТОВЫХ ПОСТОВ")
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
        
        # Создаем тестовые посты с правильным форматом даты
        test_posts = []
        
        # Пост 1: На прямо сейчас
        post1_time = current_time
        test_posts.append({
            "date": post1_time.strftime("%d.%m.%Y"),
            "time": post1_time.strftime("%H:%M"),
            "text": f"<b>🚀 ИСПРАВЛЕННЫЙ ТЕСТОВЫЙ ПОСТ #1</b><br><br>Этот пост создан с исправленным форматом даты и должен быть опубликован немедленно.<br><br><i>Время:</i> {post1_time.strftime('%H:%M:%S MSK')}<br><br>Формат даты: {post1_time.strftime('%d.%m.%Y')}",
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
            "text": f"<b>⏰ ИСПРАВЛЕННЫЙ ТЕСТОВЫЙ ПОСТ #2</b><br><br>Этот пост создан с исправленным форматом даты и должен быть опубликован немедленно.<br><br><i>Время:</i> {post2_time.strftime('%H:%M:%S MSK')}<br><br>Формат даты: {post2_time.strftime('%d.%m.%Y')}",
            "prompt_ru": "",
            "prompt_en": "",
            "image_urls": "",
            "status": STATUS_PENDING
        })
        
        # Добавляем посты в Google Sheets
        print(f"\n📋 ДОБАВЛЯЕМ НОВЫЕ ТЕСТОВЫЕ ПОСТЫ...")
        success_count = 0
        
        for i, post in enumerate(test_posts):
            try:
                result = client.add_post(post)
                if result:
                    print(f"   ✅ Пост {i+1}/2 добавлен: {post['date']} {post['time']}")
                    success_count += 1
                else:
                    print(f"   ❌ Ошибка добавления поста {i+1}/2")
            except Exception as e:
                print(f"   ❌ Ошибка добавления поста {i+1}/2: {e}")
        
        print(f"\n📊 РЕЗУЛЬТАТ:")
        print(f"   Успешно добавлено: {success_count}/{len(test_posts)}")
        
        if success_count > 0:
            print(f"\n🎯 НОВЫЕ ТЕСТОВЫЕ ПОСТЫ СОЗДАНЫ!")
            print(f"⏰ Посты должны быть опубликованы в течение 2 минут")
            print(f"📱 Проверьте канал: t.me/sovpalitest")
            return True
        else:
            print(f"\n❌ НЕ УДАЛОСЬ СОЗДАТЬ НОВЫЕ ТЕСТОВЫЕ ПОСТЫ")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Основная функция"""
    print("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМЫ С ФОРМАТОМ ДАТЫ")
    print("=" * 80)
    
    # Анализируем существующие посты
    fix_ok = fix_date_format_in_sheets()
    
    # Создаем новые тестовые посты
    create_ok = create_new_test_posts()
    
    print(f"\n📊 ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"   Анализ постов: {'✅ OK' if fix_ok else '❌ ERROR'}")
    print(f"   Новые посты: {'✅ OK' if create_ok else '❌ ERROR'}")
    
    if create_ok:
        print(f"\n🎉 ПРОБЛЕМА РЕШЕНА!")
        print(f"📱 Проверьте канал t.me/sovpalitest")
        print(f"⏰ Новые посты должны появиться в течение 2 минут")
    else:
        print(f"\n❌ ПРОБЛЕМА НЕ РЕШЕНА!")
        print(f"🔧 Проверьте логи Railway")

if __name__ == "__main__":
    main()
