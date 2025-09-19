#!/usr/bin/env python3
"""
Скрипт для отладки Google Sheets в Railway
Добавьте этот код в main.py для диагностики
"""
import os
import logging

def debug_railway_environment():
    """Отлаживает переменные окружения в Railway"""
    
    print("🔍 Railway Environment Debug")
    print("=" * 50)
    
    # Проверяем все Google переменные
    google_vars = [
        "GOOGLE_SHEET_ID",
        "GOOGLE_SHEET_NAME", 
        "GOOGLE_PROJECT_ID",
        "GOOGLE_PRIVATE_KEY_ID",
        "GOOGLE_PRIVATE_KEY",
        "GOOGLE_CLIENT_EMAIL",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_X509_CERT_URL"
    ]
    
    for var in google_vars:
        value = os.getenv(var)
        if value:
            if value.startswith("YOUR_"):
                print(f"❌ {var}: placeholder value")
            else:
                print(f"✅ {var}: OK ({len(value)} chars)")
                if var == "GOOGLE_PRIVATE_KEY":
                    print(f"   Contains BEGIN: {'BEGIN PRIVATE KEY' in value}")
                    print(f"   Contains \\n: {'\\n' in value}")
        else:
            print(f"❌ {var}: NOT SET")
    
    print("=" * 50)
    
    # Пробуем создать GoogleSheetsClient
    try:
        from google_sheets_client import GoogleSheetsClient
        client = GoogleSheetsClient()
        
        if client.service:
            print("✅ GoogleSheetsClient создан успешно")
            
            # Пробуем получить информацию о таблице
            sheet_id = os.getenv("GOOGLE_SHEET_ID")
            if sheet_id and not sheet_id.startswith("YOUR_"):
                try:
                    result = client.service.spreadsheets().get(spreadsheetId=sheet_id).execute()
                    print(f"✅ Таблица доступна: {result.get('properties', {}).get('title', 'Без названия')}")
                except Exception as e:
                    print(f"❌ Ошибка доступа к таблице: {e}")
            else:
                print("❌ GOOGLE_SHEET_ID не установлен")
        else:
            print("❌ GoogleSheetsClient.service = None")
            print("   Проблема с аутентификацией Service Account")
            
    except Exception as e:
        print(f"❌ Ошибка создания GoogleSheetsClient: {e}")
        import traceback
        print(f"Детали: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_railway_environment()
