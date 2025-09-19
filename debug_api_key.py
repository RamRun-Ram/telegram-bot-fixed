#!/usr/bin/env python3
"""
Скрипт для диагностики API ключа OpenRouter
"""
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_api_key():
    """Диагностика API ключа"""
    
    # Получаем ключ из переменных окружения
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        logger.error("❌ OPENROUTER_API_KEY не найден в переменных окружения")
        return
    
    logger.info("🔍 Диагностика API ключа:")
    logger.info(f"📏 Длина ключа: {len(api_key)} символов")
    logger.info(f"🔤 Первые 10 символов: {api_key[:10]}")
    logger.info(f"🔤 Последние 10 символов: {api_key[-10:]}")
    logger.info(f"✅ Начинается с sk-or-v1-: {api_key.startswith('sk-or-v1-')}")
    
    # Проверяем на скрытые символы
    logger.info(f"🔍 Содержит только ASCII: {api_key.isascii()}")
    logger.info(f"🔍 Содержит пробелы: {' ' in api_key}")
    newline_check = '\n' in api_key or '\r' in api_key
    logger.info(f"🔍 Содержит переносы строк: {newline_check}")
    
    # Показываем ключ в разных форматах
    logger.info("📋 Ключ в разных форматах:")
    logger.info(f"Raw: {repr(api_key)}")
    logger.info(f"Strip: {repr(api_key.strip())}")
    
    # Проверяем, что ключ правильной длины
    if len(api_key) != 73:
        logger.error(f"❌ Неправильная длина ключа! Ожидается 73, получено {len(api_key)}")
    else:
        logger.info("✅ Длина ключа правильная")
    
    # Проверяем формат
    if not api_key.startswith('sk-or-v1-'):
        logger.error("❌ Ключ не начинается с 'sk-or-v1-'")
    else:
        logger.info("✅ Формат ключа правильный")

if __name__ == "__main__":
    debug_api_key()
