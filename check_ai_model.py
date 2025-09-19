#!/usr/bin/env python3
"""
Скрипт для проверки текущей модели AI
"""
import os
import logging
from config import AI_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_ai_model():
    """Проверяет текущую модель AI"""
    
    logger.info("🔍 Проверка модели AI...")
    
    # Проверяем переменную окружения
    env_model = os.getenv("AI_MODEL")
    if env_model:
        logger.info(f"✅ AI_MODEL из переменных окружения: {env_model}")
    else:
        logger.warning("⚠️ AI_MODEL не установлен в переменных окружения")
    
    # Проверяем значение по умолчанию из config.py
    default_model = AI_MODEL
    logger.info(f"📋 Модель по умолчанию из config.py: {default_model}")
    
    # Проверяем, какая модель будет использоваться
    actual_model = env_model if env_model else default_model
    logger.info(f"🎯 Фактически используемая модель: {actual_model}")
    
    if "gemini" in actual_model.lower():
        logger.info("✅ Используется модель Gemini")
    elif "claude" in actual_model.lower():
        logger.warning("⚠️ Используется модель Claude (не обновлена)")
    else:
        logger.info(f"ℹ️ Используется другая модель: {actual_model}")

if __name__ == "__main__":
    check_ai_model()
