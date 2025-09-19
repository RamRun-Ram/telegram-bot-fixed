#!/usr/bin/env python3
"""
Скрипт для проверки доступных листов в Google Sheets
"""
import os
import logging
from google_sheets_client import GoogleSheetsClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_sheet_names():
    """Проверяет доступные листы в Google Sheets"""
    
    logger.info("🔍 Проверка доступных листов в Google Sheets...")
    
    try:
        client = GoogleSheetsClient()
        
        if not client.service:
            logger.error("❌ Google Sheets API не инициализирован")
            return
        
        sheet_id = os.getenv("GOOGLE_SHEET_ID")
        if not sheet_id or sheet_id.startswith("YOUR_"):
            logger.error("❌ GOOGLE_SHEET_ID не установлен")
            return
        
        logger.info(f"📊 Проверяем таблицу: {sheet_id}")
        
        # Получаем информацию о таблице
        result = client.service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        
        logger.info(f"✅ Таблица найдена: {result.get('properties', {}).get('title', 'Без названия')}")
        
        # Получаем список листов
        sheets = result.get('sheets', [])
        logger.info(f"📋 Найдено листов: {len(sheets)}")
        
        for i, sheet in enumerate(sheets):
            sheet_props = sheet.get('properties', {})
            sheet_name = sheet_props.get('title', f'Лист {i+1}')
            sheet_id_num = sheet_props.get('sheetId', 'N/A')
            logger.info(f"   {i+1}. Название: '{sheet_name}' (ID: {sheet_id_num})")
        
        # Проверяем, есть ли лист "Sheet1"
        sheet_names = [sheet.get('properties', {}).get('title', '') for sheet in sheets]
        if 'Sheet1' in sheet_names:
            logger.info("✅ Лист 'Sheet1' найден")
        else:
            logger.warning("⚠️ Лист 'Sheet1' НЕ найден")
            logger.info("💡 Возможные варианты:")
            for name in sheet_names:
                logger.info(f"   - '{name}'")
            
            # Предлагаем использовать первый лист
            if sheet_names:
                first_sheet = sheet_names[0]
                logger.info(f"💡 Рекомендуется использовать: '{first_sheet}'")
                logger.info(f"   Установите GOOGLE_SHEET_NAME={first_sheet}")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при проверке листов: {e}")
        import traceback
        logger.error(f"Детали: {traceback.format_exc()}")

if __name__ == "__main__":
    check_sheet_names()
