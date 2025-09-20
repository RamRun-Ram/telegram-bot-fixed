#!/usr/bin/env python3
"""
Проверка статуса Google Sheets
"""

import os
import sys
from google_sheets_client import GoogleSheetsClient

def check_google_sheets_status():
    """Проверяет статус Google Sheets"""
    
    print("🔍 Проверка статуса Google Sheets...")
    
    # Проверяем переменные окружения
    required_vars = [
        'GOOGLE_SHEET_ID',
        'GOOGLE_CREDENTIALS_JSON'
    ]
    
    print("\n📋 Переменные окружения:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'GOOGLE_CREDENTIALS_JSON':
                print(f"   ✅ {var}: установлена (длина: {len(value)} символов)")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: НЕ УСТАНОВЛЕНА")
    
    # Проверяем файл token.json
    if os.path.exists('token.json'):
        print(f"   ✅ token.json: файл существует")
    else:
        print(f"   ❌ token.json: файл НЕ НАЙДЕН")
    
    # Инициализируем клиент Google Sheets
    print("\n🔧 Инициализация Google Sheets клиента...")
    sheets_client = GoogleSheetsClient()
    
    if sheets_client.service:
        print("   ✅ Google Sheets API инициализирован успешно")
        
        # Пробуем получить информацию о таблице
        try:
            sheet_name = sheets_client.get_sheet_name()
            print(f"   ✅ Имя листа: {sheet_name}")
            
            # Пробуем получить посты
            posts = sheets_client.get_all_posts()
            print(f"   ✅ Количество постов в таблице: {len(posts)}")
            
        except Exception as e:
            print(f"   ❌ Ошибка при работе с таблицей: {e}")
    else:
        print("   ❌ Google Sheets API НЕ инициализирован")
        print("   💡 Проверьте переменные окружения и файл token.json")
    
    print("\n🎯 Результат:")
    if sheets_client.service:
        print("   ✅ Google Sheets настроен правильно - посты будут загружаться в таблицу")
    else:
        print("   ❌ Google Sheets НЕ настроен - посты НЕ будут загружаться в таблицу")
        print("   📋 Настройте переменные окружения в Railway:")

if __name__ == "__main__":
    check_google_sheets_status()
