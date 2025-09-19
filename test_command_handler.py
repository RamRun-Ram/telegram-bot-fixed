#!/usr/bin/env python3
"""
Тестовый скрипт для проверки обработчика команд
"""
import logging
import sys
from telegram_command_handler import TelegramCommandHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Тестирование обработчика команд"""
    try:
        logger.info("🧪 Тестирование обработчика команд...")
        
        # Создаем обработчик
        handler = TelegramCommandHandler()
        
        # Тестируем подключение к боту
        try:
            bot_info = handler.bot.get_me()
            logger.info(f"✅ Бот подключен: @{bot_info.username} (ID: {bot_info.id})")
        except Exception as e:
            logger.error(f"❌ Ошибка подключения к боту: {e}")
            return
        
        logger.info("✅ Обработчик команд работает корректно")
        logger.info("💡 Для полного тестирования запустите: python run_command_handler.py")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    main()
