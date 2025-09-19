#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для просмотра постов в Google Sheets
"""
import os
import sys
from google_sheets_client import GoogleSheetsClient

def view_posts():
    """Показывает все посты из Google Sheets"""
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    # Проверяем подключение
    if not sheets_client.service:
        print("❌ Ошибка: Google Sheets API не инициализирован")
        print("Проверьте переменные окружения:")
        print("- GOOGLE_SHEET_ID")
        print("- GOOGLE_CREDENTIALS_JSON")
        return False
    
    print("📋 Получаем посты из Google Sheets...")
    
    try:
        # Получаем все посты
        posts = sheets_client.get_all_posts()
        
        if not posts:
            print("📭 Таблица пуста")
            return True
        
        print(f"\n📊 Найдено {len(posts)} постов:")
        print("=" * 80)
        
        for i, post in enumerate(posts, 1):
            print(f"\n📝 Пост #{i}:")
            print(f"   📅 Дата: {post.get('date', 'N/A')}")
            print(f"   ⏰ Время: {post.get('time', 'N/A')}")
            print(f"   📄 Текст: {post.get('text', 'N/A')[:100]}...")
            print(f"   🖼️ Изображения: {'Да' if post.get('image_urls') else 'Нет'}")
            print(f"   🎨 Промпт RU: {'Есть' if post.get('prompt_ru') else 'Нет'}")
            print(f"   🎨 Промпт EN: {'Есть' if post.get('prompt_en') else 'Нет'}")
            print(f"   📊 Статус: {post.get('status', 'N/A')}")
            print("-" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка получения постов: {e}")
        return False

if __name__ == "__main__":
    print("👀 Просмотр постов в Google Sheets")
    print("=" * 50)
    
    success = view_posts()
    
    if not success:
        sys.exit(1)
