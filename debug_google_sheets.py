#!/usr/bin/env python3
"""
Детальная диагностика Google Sheets API
"""
import os
import logging
from google_sheets_client import GoogleSheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_google_sheets():
    """Детальная диагностика Google Sheets API"""
    
    logger.info("🔍 Детальная диагностика Google Sheets API...")
    
    # Проверяем каждую переменную отдельно
    vars_to_check = {
        "GOOGLE_SHEET_ID": os.getenv("GOOGLE_SHEET_ID"),
        "GOOGLE_PROJECT_ID": os.getenv("GOOGLE_PROJECT_ID"),
        "GOOGLE_PRIVATE_KEY_ID": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "GOOGLE_PRIVATE_KEY": os.getenv("GOOGLE_PRIVATE_KEY"),
        "GOOGLE_CLIENT_EMAIL": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
        "GOOGLE_CLIENT_X509_CERT_URL": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
    }
    
    logger.info("📋 Проверка переменных окружения:")
    for var_name, var_value in vars_to_check.items():
        if var_value and not var_value.startswith("YOUR_"):
            logger.info(f"✅ {var_name}: установлен ({len(var_value)} символов)")
        else:
            logger.error(f"❌ {var_name}: не установлен или содержит placeholder")
    
    # Проверяем формат GOOGLE_PRIVATE_KEY
    private_key = os.getenv("GOOGLE_PRIVATE_KEY")
    if private_key and not private_key.startswith("YOUR_"):
        logger.info("🔍 Анализ GOOGLE_PRIVATE_KEY:")
        logger.info(f"   Длина: {len(private_key)} символов")
        logger.info(f"   Начинается с: {private_key[:20]}...")
        logger.info(f"   Заканчивается на: ...{private_key[-20:]}")
        logger.info(f"   Содержит BEGIN: {'BEGIN PRIVATE KEY' in private_key}")
        logger.info(f"   Содержит END: {'END PRIVATE KEY' in private_key}")
        logger.info(f"   Содержит \\n: {'\\n' in private_key}")
    
    # Пробуем создать клиент
    logger.info("🔧 Попытка создания GoogleSheetsClient...")
    try:
        client = GoogleSheetsClient()
        
        if client.service is None:
            logger.error("❌ GoogleSheetsClient.service = None")
            logger.error("   Это означает, что аутентификация не удалась")
        else:
            logger.info("✅ GoogleSheetsClient.service создан успешно")
            
            # Пробуем простую операцию
            logger.info("🧪 Тестируем простую операцию...")
            try:
                # Пробуем получить информацию о таблице
                sheet_id = os.getenv("GOOGLE_SHEET_ID")
                if sheet_id and not sheet_id.startswith("YOUR_"):
                    result = client.service.spreadsheets().get(spreadsheetId=sheet_id).execute()
                    logger.info(f"✅ Таблица найдена: {result.get('properties', {}).get('title', 'Без названия')}")
                else:
                    logger.warning("⚠️ GOOGLE_SHEET_ID не установлен, пропускаем тест таблицы")
            except Exception as e:
                logger.error(f"❌ Ошибка при обращении к таблице: {e}")
                
    except Exception as e:
        logger.error(f"❌ Ошибка создания GoogleSheetsClient: {e}")
        logger.error(f"   Тип ошибки: {type(e).__name__}")
        import traceback
        logger.error(f"   Детали: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_google_sheets()
