#!/usr/bin/env python3
"""
Скрипт для принудительного обновления заголовков Google Sheets
"""
import os
import logging
from google_sheets_client import GoogleSheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_sheet_headers():
    """Принудительно обновляет заголовки Google Sheets"""
    
    logger.info("🔄 Принудительное обновление заголовков Google Sheets...")
    
    try:
        client = GoogleSheetsClient()
        
        if not client.service:
            logger.error("❌ Google Sheets API не инициализирован")
            return False
        
        # Получаем имя листа
        sheet_name = client.get_sheet_name()
        logger.info(f"📋 Работаем с листом: '{sheet_name}'")
        
        # Устанавливаем новые заголовки
        headers = [['Date', 'Time', 'Text', 'Image URLs', 'Status', 'Промпт RU', 'Промпт EN']]
        
        result = client.service.spreadsheets().values().update(
            spreadsheetId=os.getenv("GOOGLE_SHEET_ID"),
            range=f'{sheet_name}!A1:G1',
            valueInputOption='RAW',
            body={'values': headers}
        ).execute()
        
        logger.info("✅ Заголовки Google Sheets обновлены!")
        logger.info("📊 Новые заголовки:")
        for i, header in enumerate(headers[0], 1):
            logger.info(f"   {i}. {header}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка обновления заголовков: {e}")
        return False

if __name__ == "__main__":
    update_sheet_headers()
