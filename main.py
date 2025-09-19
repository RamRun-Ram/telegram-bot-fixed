"""
Основной скрипт для автоматизации публикаций в Telegram-канал из Google Sheets
"""
import asyncio
import logging
import threading
import time
from datetime import datetime, time as dt_time
import pytz
import os
import sys

from google_sheets_client import GoogleSheetsClient
from telegram_client import TelegramClient
from notification_system import NotificationSystem, NotificationType
from config import CHECK_TIMES, CHECK_INTERVAL_MINUTES, LOOKBACK_MINUTES, STATUS_PUBLISHED, STATUS_ERROR

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def debug_google_sheets_setup():
    """Диагностика настроек Google Sheets"""
    logger.info("🔍 Проверка настроек Google Sheets...")
    
    google_vars = [
        "GOOGLE_SHEET_ID", "GOOGLE_SHEET_NAME", "GOOGLE_PROJECT_ID",
        "GOOGLE_PRIVATE_KEY_ID", "GOOGLE_PRIVATE_KEY", "GOOGLE_CLIENT_EMAIL",
        "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_X509_CERT_URL"
    ]
    
    missing_vars = []
    for var in google_vars:
        value = os.getenv(var)
        if not value or value.startswith("YOUR_"):
            missing_vars.append(var)
            logger.error(f"❌ {var}: не установлен")
        else:
            logger.info(f"✅ {var}: OK")
    
    if missing_vars:
        logger.error(f"❌ Отсутствуют переменные: {', '.join(missing_vars)}")
        logger.error("📋 Установите переменные в Railway Dashboard → Settings → Variables")
        return False
    else:
        logger.info("✅ Все переменные Google Sheets установлены")
        return True

class TelegramAutomation:
    """Основной класс для автоматизации публикаций"""
    
    def __init__(self):
        self.sheets_client = None
        self.telegram_client = None
        self.notification_system = None
        self.moscow_tz = pytz.timezone('Europe/Moscow')
        self.daily_stats = {'published': 0, 'errors': 0, 'pending': 0}
        
    async def initialize(self):
        """Инициализация клиентов"""
        try:
            logger.info("Инициализация клиентов...")
            
            # Диагностика Google Sheets
            debug_google_sheets_setup()
            
            self.sheets_client = GoogleSheetsClient()
            
            # Принудительно обновляем заголовки Google Sheets
            if self.sheets_client.service:
                logger.info("🔄 Принудительно обновляем заголовки Google Sheets...")
                self.sheets_client.setup_headers()
            self.telegram_client = TelegramClient()
            self.notification_system = NotificationSystem(self.telegram_client)
            
            # Проверяем соединение с Telegram
            if not await self.telegram_client.test_connection():
                raise Exception("Не удалось подключиться к Telegram Bot API")
            
            logger.info("Клиенты успешно инициализированы")
            
            # Отправляем уведомление о запуске
            await self.notification_system.send_info_notification(
                "🚀 Система автоматизации запущена",
                {
                    "время": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "проверка": f"каждые {CHECK_INTERVAL_MINUTES} минут",
                    "поиск": f"за последние {LOOKBACK_MINUTES} минут",
                    "канал": "@sovpalitest",
                    "статус": "готов к работе"
                }
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка инициализации: {e}")
            return False
    
    def _should_publish_post(self, post: dict, current_time: datetime) -> bool:
        """Проверяет, подходит ли время поста для публикации"""
        try:
            post_date_str = post.get('date', '')
            post_time_str = post.get('time', '')
            
            if not post_date_str or not post_time_str:
                logger.warning(f"Пост из строки {post['row_index']} не имеет даты или времени")
                return False
            
            # Парсим дату и время поста
            try:
                post_datetime = datetime.strptime(f"{post_date_str} {post_time_str}", "%Y-%m-%d %H:%M")
                post_datetime = self.moscow_tz.localize(post_datetime)
            except ValueError:
                # Пробуем другие форматы
                try:
                    post_datetime = datetime.strptime(f"{post_date_str} {post_time_str}", "%d.%m.%Y %H:%M")
                    post_datetime = self.moscow_tz.localize(post_datetime)
                except ValueError:
                    try:
                        post_datetime = datetime.strptime(f"{post_date_str} {post_time_str}", "%Y-%m-%d %H:%M:%S")
                        post_datetime = self.moscow_tz.localize(post_datetime)
                    except ValueError:
                        logger.warning(f"Не удалось распарсить дату/время поста: {post_date_str} {post_time_str}")
                        return False
            
            # Проверяем, подходит ли время (в пределах LOOKBACK_MINUTES)
            time_diff = (current_time - post_datetime).total_seconds() / 60  # в минутах
            
            # Пост должен быть в пределах LOOKBACK_MINUTES от текущего времени
            if 0 <= time_diff <= LOOKBACK_MINUTES:
                logger.info(f"Пост из строки {post['row_index']} подходит по времени (разница: {time_diff:.1f} мин)")
                return True
            else:
                logger.debug(f"Пост из строки {post['row_index']} не подходит по времени (разница: {time_diff:.1f} мин)")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка проверки времени поста: {e}")
            return False
    
    async def process_pending_posts(self):
        """Обрабатывает посты, готовые к публикации"""
        try:
            logger.info("Начинаем обработку постов...")
            
            # Получаем список постов для публикации
            pending_posts = self.sheets_client.get_pending_posts()
            
            if not pending_posts:
                logger.info("Нет постов для публикации")
                # Отправляем уведомление о пустой проверке
                current_time = datetime.now(self.moscow_tz).strftime('%H:%M:%S')
                await self.notification_system.send_check_notification(0, 0, 0, current_time)
                return
            
            logger.info(f"Найдено {len(pending_posts)} постов со статусом 'Ожидает'")
            
            # Фильтруем посты по времени
            current_time = datetime.now(self.moscow_tz)
            posts_to_publish = []
            
            for post in pending_posts:
                if self._should_publish_post(post, current_time):
                    posts_to_publish.append(post)
                else:
                    logger.info(f"Пост из строки {post['row_index']} не подходит по времени (время: {post['time']}, дата: {post['date']})")
            
            if not posts_to_publish:
                logger.info("Нет постов, готовых к публикации по времени")
                # Отправляем уведомление о проверке без публикаций
                current_time_str = current_time.strftime('%H:%M:%S')
                await self.notification_system.send_check_notification(len(pending_posts), 0, 0, current_time_str)
                return
            
            logger.info(f"Найдено {len(posts_to_publish)} постов, готовых к публикации")
            self.daily_stats['pending'] = len(posts_to_publish)
            
            # Счетчики для уведомления
            published_count = 0
            errors_count = 0
            
            for post in posts_to_publish:
                success = await self.publish_post(post)
                if success:
                    published_count += 1
                else:
                    errors_count += 1
            
            # Отправляем уведомление о результатах проверки
            current_time_str = current_time.strftime('%H:%M:%S')
            await self.notification_system.send_check_notification(
                len(pending_posts), published_count, errors_count, current_time_str
            )
                
        except Exception as e:
            logger.error(f"Ошибка при обработке постов: {e}")
            await self.notification_system.send_error_notification(
                f"Ошибка обработки постов: {str(e)}"
            )
    
    async def publish_post(self, post: dict) -> bool:
        """Публикует один пост. Возвращает True если успешно, False если ошибка"""
        row_index = post['row_index']
        post_time = post['time']
        has_images = post.get('image_urls') and len(post['image_urls']) > 0
        
        try:
            logger.info(f"Публикуем пост из строки {row_index} (время: {post_time})")
            logger.info(f"🖼️ Изображения: {'да' if has_images else 'нет'}")
            
            # Определяем метод публикации по наличию изображений
            if has_images:
                # Пост С изображениями - HTML метод
                logger.info("🖼️ Пост с изображениями - используем HTML метод")
                success = await self.telegram_client.send_html_post_with_image(
                    text=post['text'],
                    image_urls=post['image_urls']
                )
            else:
                # Пост БЕЗ изображений - Markdown метод
                logger.info("📝 Пост без изображений - используем Markdown метод")
                success = await self.telegram_client.send_markdown_post(
                    text=post['text']
                )
            
            if success:
                # Обновляем статус на "Опубликовано"
                self.sheets_client.update_post_status(row_index, STATUS_PUBLISHED)
                self.daily_stats['published'] += 1
                logger.info(f"Пост из строки {row_index} успешно опубликован")
                
                # Отправляем уведомление об успехе
                await self.notification_system.send_info_notification(
                    "Пост опубликован",
                    {
                        "Дата": post['date'],
                        "Время": post['time'],
                        "Длина": f"{len(post['text'])} символов",
                        "Изображения": "да" if has_images else "нет",
                        "Формат": "HTML" if has_images else "Markdown"
                    }
                )
                return True
            else:
                # Обновляем статус на "Ошибка"
                error_msg = "Ошибка отправки в Telegram"
                self.sheets_client.update_post_status(row_index, STATUS_ERROR, error_msg)
                self.daily_stats['errors'] += 1
                logger.error(f"Ошибка публикации поста из строки {row_index}")
                
                # Отправляем уведомление об ошибке
                await self.notification_system.send_error_notification(error_msg, post)
                return False
                
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            logger.error(f"Ошибка публикации поста из строки {row_index}: {e}")
            
            try:
                self.sheets_client.update_post_status(row_index, STATUS_ERROR, error_msg)
                self.daily_stats['errors'] += 1
            except Exception as update_error:
                logger.error(f"Ошибка обновления статуса: {update_error}")
            
            # Отправляем уведомление об ошибке
            await self.notification_system.send_error_notification(error_msg, post)
            return False
    
    def _run_process_posts_thread(self):
        """Запускает обработку постов в отдельном потоке"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.process_pending_posts())
            loop.close()
        except Exception as e:
            logger.error(f"Ошибка в _run_process_posts_thread: {e}")
    
    def _schedule_worker(self):
        """Рабочий поток для расписания"""
        logger.info("Запуск системы автоматических проверок...")
        logger.info("Время работы: 8:01 - 22:01 (МСК)")
        logger.info("Время отдыха: 23:00 - 7:00 (МСК)")
        logger.info(f"Проверяем каждые {CHECK_INTERVAL_MINUTES} минут")
        logger.info(f"Ищем посты за последние {LOOKBACK_MINUTES} минут")
        
        while True:
            try:
                current_time = datetime.now(self.moscow_tz)
                current_hour = current_time.hour
                
                # Проверяем, нужно ли работать сейчас (8:00 - 22:00)
                if 8 <= current_hour <= 22:
                    logger.info(f"🕐 Рабочее время: {current_time.strftime('%H:%M')} - проверяем посты")
                    
                    # Запускаем обработку в отдельном потоке
                    thread = threading.Thread(target=self._run_process_posts_thread)
                    thread.daemon = True
                    thread.start()
                    thread.join()  # Ждем завершения
                else:
                    logger.info(f"😴 Время отдыха: {current_time.strftime('%H:%M')} - пропускаем проверку")
                
                # Ждем 10 минут до следующей проверки
                time.sleep(600)
                
            except Exception as e:
                logger.error(f"Ошибка в _schedule_worker: {e}")
                time.sleep(600)
    
    async def run_scheduled_checks(self):
        """Запускает проверки по расписанию"""
        # Запускаем рабочий поток в фоне
        schedule_thread = threading.Thread(target=self._schedule_worker)
        schedule_thread.daemon = True
        schedule_thread.start()
        
        # Основной поток ждет
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
    
    async def run_manual_check(self):
        """Запускает ручную проверку (для тестирования)"""
        logger.info("Запуск ручной проверки...")
        await self.process_pending_posts()
    
    def run(self, manual=False):
        """Основной метод запуска"""
        try:
            # Инициализируем клиентов
            if not asyncio.run(self.initialize()):
                logger.error("Не удалось инициализировать клиенты")
                return
            
            if manual:
                # Ручная проверка
                asyncio.run(self.run_manual_check())
            else:
                # Автоматические проверки по расписанию
                asyncio.run(self.run_scheduled_checks())
                
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")

def main():
    """Точка входа в приложение"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Автоматизация публикаций в Telegram-канал')
    parser.add_argument('--manual', action='store_true', 
                       help='Запустить ручную проверку вместо автоматического режима')
    parser.add_argument('--test', action='store_true',
                       help='Тестировать соединения без публикации постов')
    
    args = parser.parse_args()
    
    automation = TelegramAutomation()
    
    if args.test:
        # Тестовый режим
        logger.info("Тестовый режим: проверка соединений...")
        asyncio.run(automation.initialize())
        logger.info("Тест завершен")
    else:
        # Основной режим
        automation.run(manual=args.manual)

if __name__ == "__main__":
    main()
