#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для добавления тестовых постов в Google Sheets
Добавляет 10 моковых постов с разными временами для тестирования публикации
"""
import os
import sys
from datetime import datetime, timedelta
import pytz
from google_sheets_client import GoogleSheetsClient

def add_test_posts():
    """Добавляет 10 тестовых постов в Google Sheets"""
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    # Проверяем подключение
    if not sheets_client.service:
        print("❌ Ошибка: Google Sheets API не инициализирован")
        print("Проверьте переменные окружения:")
        print("- GOOGLE_SHEET_ID")
        print("- GOOGLE_CREDENTIALS_JSON")
        return False
    
    # Устанавливаем заголовки
    print("📋 Устанавливаем заголовки таблицы...")
    sheets_client.setup_headers()
    
    # Получаем текущее время по Москве
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Создаем 10 тестовых постов
    test_posts = []
    
    # Посты с изображениями (дневные)
    for i in range(5):
        post_time = now + timedelta(minutes=2 + i*2)  # Каждые 2 минуты
        test_posts.append({
            "date": post_time.strftime("%d.%m.%y"),
            "time": post_time.strftime("%H:%M"),
            "text": f"<b>ТЕСТОВЫЙ ПОСТ #{i+1} (С ИЗОБРАЖЕНИЕМ)</b><br><br>Это тестовый пост для проверки автоматической публикации в Telegram-канал. Пост содержит HTML-разметку и должен быть опубликован с изображением.<br><br><i>Время публикации:</i> {post_time.strftime('%H:%M')}<br><br>Этот пост используется для тестирования системы автоматизации.",
            "prompt_ru": "",
            "prompt_en": f"A couple in a cozy coffee shop, sitting opposite each other, sincerely laughing, completely relaxed, natural, without masks, warm lighting, atmosphere of trust, close-up, photorealistic, depth of field --test{i+1}",
            "image_urls": f"https://picsum.photos/800/600?random={i+1}",
            "status": "Ожидает"
        })
    
    # Посты без изображений (утренние и вечерние)
    for i in range(5):
        post_time = now + timedelta(minutes=12 + i*2)  # Начиная с 12-й минуты, каждые 2 минуты
        if i % 2 == 0:
            # Утренние цитаты
            test_posts.append({
                "date": post_time.strftime("%d.%m.%y"),
                "time": post_time.strftime("%H:%M"),
                "text": f"> Тестовая цитата #{i+1}: Любовь — это не тогда, когда вы смотрите друг на друга, а когда вы смотрите в одном направлении.",
                "prompt_ru": "",
                "prompt_en": "",
                "image_urls": "",
                "status": "Ожидает"
            })
        else:
            # Вечерние посты
            test_posts.append({
                "date": post_time.strftime("%d.%m.%y"),
                "time": post_time.strftime("%H:%M"),
                "text": f"**ТЕСТОВЫЙ ВЕЧЕРНИЙ ПОСТ #{i+1}**\n\nЭто тестовый вечерний пост для проверки автоматической публикации. Пост написан в формате Markdown и не содержит изображений.\n\n*Время публикации:* {post_time.strftime('%H:%M')}\n\nЭтот пост используется для тестирования системы автоматизации без изображений.",
                "prompt_ru": "",
                "prompt_en": "",
                "image_urls": "",
                "status": "Ожидает"
            })
    
    # Добавляем посты в таблицу
    print(f"📤 Добавляем {len(test_posts)} тестовых постов в Google Sheets...")
    
    success_count = 0
    for i, post in enumerate(test_posts):
        try:
            result = sheets_client.add_post(post)
            if result:
                print(f"✅ Пост {i+1}/10 добавлен: {post['date']} {post['time']}")
                success_count += 1
            else:
                print(f"❌ Ошибка добавления поста {i+1}/10: {post['date']} {post['time']}")
        except Exception as e:
            print(f"❌ Ошибка добавления поста {i+1}/10: {e}")
    
    print(f"\n📊 Результат:")
    print(f"✅ Успешно добавлено: {success_count}/{len(test_posts)} постов")
    print(f"❌ Ошибок: {len(test_posts) - success_count}")
    
    if success_count > 0:
        print(f"\n🎯 Тестовые посты добавлены!")
        print(f"⏰ Первый пост будет опубликован через 2 минуты")
        print(f"⏰ Последний пост будет опубликован через {2 + (len(test_posts)-1)*2} минут")
        print(f"📱 Проверьте Telegram-канал для публикации постов")
    
    return success_count > 0

if __name__ == "__main__":
    print("🧪 Добавление тестовых постов в Google Sheets")
    print("=" * 50)
    
    success = add_test_posts()
    
    if success:
        print("\n✅ Тестовые посты успешно добавлены!")
        print("🔄 Система будет проверять таблицу каждые 2 минуты")
        print("📱 Следите за публикациями в Telegram-канале")
    else:
        print("\n❌ Ошибка добавления тестовых постов")
        sys.exit(1)
