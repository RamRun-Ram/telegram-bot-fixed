#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для очистки тестовых постов из Google Sheets
"""
import os
import sys
from google_sheets_client import GoogleSheetsClient

def clear_test_posts():
    """Очищает все посты из Google Sheets"""
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    # Проверяем подключение
    if not sheets_client.service:
        print("❌ Ошибка: Google Sheets API не инициализирован")
        print("Проверьте переменные окружения:")
        print("- GOOGLE_SHEET_ID")
        print("- GOOGLE_CREDENTIALS_JSON")
        return False
    
    print("🗑️ Очищаем Google Sheets...")
    
    try:
        # Очищаем таблицу
        result = sheets_client.clear_sheet()
        if result:
            print("✅ Google Sheets успешно очищена")
            return True
        else:
            print("❌ Ошибка очистки Google Sheets")
            return False
    except Exception as e:
        print(f"❌ Ошибка очистки: {e}")
        return False

if __name__ == "__main__":
    print("🧹 Очистка тестовых постов из Google Sheets")
    print("=" * 50)
    
    # Подтверждение
    confirm = input("Вы уверены, что хотите очистить ВСЕ посты из таблицы? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Операция отменена")
        sys.exit(0)
    
    success = clear_test_posts()
    
    if success:
        print("\n✅ Google Sheets успешно очищена!")
    else:
        print("\n❌ Ошибка очистки Google Sheets")
        sys.exit(1)
