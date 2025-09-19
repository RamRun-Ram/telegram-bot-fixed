#!/usr/bin/env python3
"""
Скрипт для запуска обработчика команд Telegram
"""
import logging
import signal
import sys
from telegram_command_handler import start_command_handler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('command_handler.log')
    ]
)

logger = logging.getLogger(__name__)

# Глобальная переменная для контроля работы
running = True

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения"""
    global running
    logger.info(f"Получен сигнал {signum}, завершаем работу...")
    running = False

def main():
    """Основная функция"""
    global running
    
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("🚀 Запуск обработчика команд Telegram...")
        logger.info("📱 Бот будет отвечать на команды в канале уведомлений")
        logger.info("💬 Доступные команды: /post, /status, /help")
        logger.info("💬 Или просто напишите 'пост' для быстрой генерации")
        logger.info("⏹️  Для остановки нажмите Ctrl+C")
        
        # Запускаем обработчик команд
        start_command_handler()
        
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки от пользователя")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        logger.info("🛑 Обработчик команд остановлен")

if __name__ == "__main__":
    main()
