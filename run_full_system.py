#!/usr/bin/env python3
"""
Скрипт для запуска полной системы:
- Основное приложение (публикация постов)
- Обработчик команд Telegram
"""
import asyncio
import logging
import signal
import sys
import threading
import time
import os
from main import TelegramAutomation
from telegram_command_handler import TelegramCommandHandler
from health_check import run_health_server

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('full_system.log')
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

def run_command_handler():
    """Запуск обработчика команд в отдельном потоке"""
    try:
        logger.info("Инициализация обработчика команд...")
        handler = TelegramCommandHandler()
        
        # Небольшая задержка перед запуском polling
        import time
        time.sleep(5)
        
        logger.info("Запуск обработчика команд...")
        handler.start_polling()
    except Exception as e:
        logger.error(f"Ошибка в обработчике команд: {e}")
        # Если ошибка 409, ждем и пробуем снова
        if "409" in str(e) or "Conflict" in str(e):
            logger.warning("Конфликт обнаружен, ожидание 60 секунд...")
            time.sleep(60)
            try:
                handler = TelegramCommandHandler()
                handler.start_polling()
            except Exception as retry_e:
                logger.error(f"Ошибка при повторной попытке: {retry_e}")

def run_main_automation():
    """Запуск основного приложения автоматизации"""
    try:
        automation = TelegramAutomation()
        asyncio.run(automation.initialize())
        automation.run()
    except Exception as e:
        logger.error(f"Ошибка в основном приложении: {e}")

async def main():
    """Основная функция"""
    global running
    
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("🚀 Запуск полной системы автоматизации...")
        logger.info("📱 Включен обработчик команд Telegram")
        logger.info("⏰ Включена автоматическая публикация постов (каждые 10 минут)")
        logger.info("💬 Команды работают в канале уведомлений: /post, /status, /help или просто 'пост'")
        logger.info("⏹️  Для остановки нажмите Ctrl+C")
        
        # Запускаем health check сервер в отдельном потоке
        health_thread = threading.Thread(target=run_health_server)
        health_thread.daemon = True
        health_thread.start()
        
        # Запускаем основное приложение в отдельном потоке
        automation_thread = threading.Thread(target=run_main_automation)
        automation_thread.daemon = True
        automation_thread.start()
        
        # Небольшая задержка перед запуском обработчика команд
        import time
        time.sleep(10)
        
        # Запускаем обработчик команд в отдельном потоке
        command_thread = threading.Thread(target=run_command_handler)
        command_thread.daemon = True
        command_thread.start()
        
        # Ждем завершения
        automation_thread.join()
        
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки от пользователя")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        logger.info("🛑 Система остановлена")

if __name__ == "__main__":
    asyncio.run(main())
