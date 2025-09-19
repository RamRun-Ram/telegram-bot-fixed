#!/usr/bin/env python3
"""
Тест Google Sheets API для диагностики проблем
"""
import os
import logging
from google_sheets_client import GoogleSheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_google_sheets():
    """Тестирует Google Sheets API"""
    
    logger.info("🔍 Тестирование Google Sheets API...")
    
    # Проверяем переменные окружения
    required_vars = [
        "GOOGLE_SHEET_ID",
        "GOOGLE_PROJECT_ID", 
        "GOOGLE_PRIVATE_KEY_ID",
        "GOOGLE_PRIVATE_KEY",
        "GOOGLE_CLIENT_EMAIL",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_X509_CERT_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            missing_vars.append(var)
            logger.error(f"❌ {var}: не установлен")
        else:
            logger.info(f"✅ {var}: установлен")
    
    if missing_vars:
        logger.error(f"❌ Отсутствуют переменные: {', '.join(missing_vars)}")
        logger.error("Установите эти переменные в Railway Dashboard")
        return False
    
    # Тестируем подключение
    try:
        client = GoogleSheetsClient()
        
        if client.service is None:
            logger.error("❌ Google Sheets API не инициализирован")
            return False
        
        logger.info("✅ Google Sheets API инициализирован")
        
        # Тестируем добавление поста
        test_post = {
            "date": "2025-09-19",
            "time": "15:00",
            "text": "Тестовый пост для проверки API",
            "image_urls": "",
            "status": "Ожидает"
        }
        
        logger.info("📝 Тестируем добавление поста...")
        result = client.add_post(test_post)
        
        if result:
            logger.info("✅ Пост успешно добавлен в Google Sheets!")
            return True
        else:
            logger.error("❌ Ошибка добавления поста")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка тестирования Google Sheets: {e}")
        return False

if __name__ == "__main__":
    test_google_sheets()
