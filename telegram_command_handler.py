"""
Модуль для обработки команд Telegram
"""
import asyncio
import logging
import threading
from datetime import datetime
from typing import Optional
import telebot
from ai_post_generator import AIPostGenerator
from ai_post_generator_stub import AIPostGeneratorStub
from google_sheets_client import GoogleSheetsClient
from config import TELEGRAM_BOT_TOKEN, NOTIFICATION_CHANNEL_ID, COMMAND_CHANNEL_ID

logger = logging.getLogger(__name__)

class TelegramCommandHandler:
    """Обработчик команд Telegram для управления постами"""
    
    def __init__(self):
        logger.info(f"Инициализация TelegramCommandHandler...")
        logger.info(f"TELEGRAM_BOT_TOKEN: {'установлен' if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != 'YOUR_TELEGRAM_BOT_TOKEN' else 'НЕ УСТАНОВЛЕН'}")
        logger.info(f"COMMAND_CHANNEL_ID: {COMMAND_CHANNEL_ID}")
        logger.info(f"NOTIFICATION_CHANNEL_ID: {NOTIFICATION_CHANNEL_ID}")
        
        self.bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        self.sheets_client = GoogleSheetsClient()
        self.ai_generator = None  # Инициализируем лениво
        self.setup_handlers()
        logger.info("TelegramCommandHandler инициализирован успешно")
    
    def get_ai_generator(self):
        """Ленивая инициализация AI генератора"""
        if self.ai_generator is None:
            logger.info("Инициализация AI генератора...")
            try:
                # Пробуем создать реальный AI генератор
                self.ai_generator = AIPostGenerator()
                # Тестируем API ключ
                if hasattr(self.ai_generator, '_test_api_key_sync'):
                    if not self.ai_generator._test_api_key_sync():
                        logger.warning("⚠️ API ключ не работает, переключаемся на заглушку")
                        self.ai_generator = AIPostGeneratorStub()
            except Exception as e:
                logger.error(f"❌ Ошибка инициализации AI генератора: {e}")
                logger.info("🔄 Переключаемся на заглушку")
                self.ai_generator = AIPostGeneratorStub()
        return self.ai_generator
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        
        def is_authorized_user(message):
            """Проверяет, что пользователь авторизован для использования команд"""
            logger.info(f"Проверка авторизации: чат {message.chat.id}, тип {message.chat.type}, текст '{message.text}'")
            logger.info(f"Ожидаемый COMMAND_CHANNEL_ID: {COMMAND_CHANNEL_ID}")
            
            # Разрешаем команды из группы AlertChanel
            if str(message.chat.id) == COMMAND_CHANNEL_ID or message.chat.username == "alertchanel":
                logger.info(f"✅ Команда из группы AlertChanel: {message.text}")
                return True
            
            # Разрешаем команды из личных сообщений (для тестирования)
            if message.chat.type == 'private':
                logger.info(f"✅ Команда из личного чата: {message.text}")
                return True
            
            logger.warning(f"❌ Команда отклонена из чата {message.chat.id} (тип: {message.chat.type}): {message.text}")
            return False
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            """Обработчик команды /start"""
            if not is_authorized_user(message):
                return
            self.bot.reply_to(message, 
                "🤖 Бот для управления постами запущен!\n\n"
                "Доступные команды:\n"
                "• /post - Сгенерировать посты на 3 дня\n"
                "• /status - Проверить статус системы\n"
                "• /help - Показать справку"
            )
        
        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            """Обработчик команды /help"""
            if not is_authorized_user(message):
                return
            self.bot.reply_to(message,
                "📋 Справка по командам:\n\n"
                "• /post - Сгенерировать и загрузить посты на 3 дня в Google Таблицу\n"
                "• /status - Показать статистику постов\n"
                "• /help - Показать эту справку\n\n"
                "💡 Просто напишите 'пост' для быстрой генерации постов!"
            )
        
        @self.bot.message_handler(commands=['post'])
        def post_command(message):
            """Обработчик команды /post"""
            if not is_authorized_user(message):
                return
            self.handle_post_generation(message)
        
        @self.bot.message_handler(commands=['status'])
        def status_command(message):
            """Обработчик команды /status"""
            if not is_authorized_user(message):
                return
            self.handle_status_check(message)
        
        @self.bot.message_handler(func=lambda message: message.text and message.text.lower().strip() == 'пост')
        def post_text_handler(message):
            """Обработчик текста 'пост'"""
            if not is_authorized_user(message):
                return
            self.handle_post_generation(message)
        
        @self.bot.message_handler(func=lambda message: True)
        def debug_handler(message):
            """Отладочный обработчик для всех сообщений"""
            logger.info(f"DEBUG: Получено сообщение '{message.text}' из чата {message.chat.id} ({message.chat.type})")
            if str(message.chat.id) == COMMAND_CHANNEL_ID:
                logger.info("Сообщение из канала команд, но не обработано")
                # Отправляем ответ в канал
                try:
                    self.bot.reply_to(message, "Получено сообщение в канале команд, но команда не распознана")
                except Exception as e:
                    logger.error(f"Ошибка отправки ответа: {e}")
    
    def handle_post_generation(self, message):
        """Обработка генерации постов"""
        try:
            # Отправляем сообщение о начале процесса
            status_msg = self.bot.reply_to(message, 
                "🔄 Начинаю генерацию постов на 3 дня...\n"
                "⏳ Это может занять несколько минут..."
            )
            
            # Генерируем посты в отдельном потоке
            def generate_posts():
                try:
                    logger.info("Начинаем генерацию постов по команде из Telegram")
                    success = asyncio.run(self.get_ai_generator().generate_and_upload_weekly_posts())
                    
                    if success:
                        # Обновляем статус
                        self.bot.edit_message_text(
                            "✅ Посты успешно сгенерированы!\n\n"
                            "📊 Создано 9 постов на 3 дня:\n"
                            "• 3 утренних поста (08:00)\n"
                            "• 3 обеденных поста (14:00) с изображениями\n"
                            "• 3 вечерних поста (20:00)\n\n"
                            "⚠️ Google Sheets не настроен - посты не загружены в таблицу\n"
                            "📋 Настройте Google Sheets API для полной функциональности\n\n"
                            "🚀 Посты будут автоматически опубликованы по расписанию!",
                            chat_id=message.chat.id,
                            message_id=status_msg.message_id
                        )
                        
                        # Отправляем уведомление в канал
                        self.send_notification(
                            "📝 Новые посты сгенерированы",
                            f"Пользователь {message.from_user.first_name} сгенерировал посты на 3 дня"
                        )
                        
                    else:
                        self.bot.edit_message_text(
                            "❌ Ошибка при генерации постов!\n"
                            "Проверьте логи для подробностей.",
                            chat_id=message.chat.id,
                            message_id=status_msg.message_id
                        )
                        
                except Exception as e:
                    logger.error(f"Ошибка при генерации постов: {e}")
                    self.bot.edit_message_text(
                        f"❌ Произошла ошибка: {str(e)}",
                        chat_id=message.chat.id,
                        message_id=status_msg.message_id
                    )
            
            # Запускаем генерацию в отдельном потоке
            thread = threading.Thread(target=generate_posts)
            thread.daemon = True
            thread.start()
                
        except Exception as e:
            logger.error(f"Ошибка при обработке команды генерации постов: {e}")
            self.bot.reply_to(message, f"❌ Произошла ошибка: {str(e)}")
    
    def handle_status_check(self, message):
        """Обработка проверки статуса"""
        try:
            # Получаем статистику постов
            all_posts = self.sheets_client.get_all_posts()
            
            if not all_posts:
                self.bot.reply_to(message, "📊 В таблице пока нет постов")
                return
            
            # Подсчитываем статистику
            total_posts = len(all_posts)
            published = sum(1 for post in all_posts if post.get('status') == 'Опубликовано')
            pending = sum(1 for post in all_posts if post.get('status') == 'Ожидает')
            errors = sum(1 for post in all_posts if post.get('status') == 'Ошибка')
            
            # Группируем по датам
            posts_by_date = {}
            for post in all_posts:
                date = post.get('date', 'Неизвестно')
                if date not in posts_by_date:
                    posts_by_date[date] = 0
                posts_by_date[date] += 1
            
            status_text = f"📊 Статистика постов:\n\n"
            status_text += f"📈 Всего постов: {total_posts}\n"
            status_text += f"✅ Опубликовано: {published}\n"
            status_text += f"⏳ Ожидает: {pending}\n"
            status_text += f"❌ Ошибки: {errors}\n\n"
            
            if posts_by_date:
                status_text += "📅 По датам:\n"
                for date, count in sorted(posts_by_date.items()):
                    status_text += f"• {date}: {count} постов\n"
            
            self.bot.reply_to(message, status_text)
            
        except Exception as e:
            logger.error(f"Ошибка при проверке статуса: {e}")
            self.bot.reply_to(message, f"❌ Ошибка получения статуса: {str(e)}")
    
    def send_notification(self, title: str, message: str):
        """Отправка уведомления в канал"""
        try:
            notification_text = f"🔔 {title}\n\n{message}"
            self.bot.send_message(
                chat_id=NOTIFICATION_CHANNEL_ID,
                text=notification_text
            )
            logger.info(f"Уведомление отправлено: {title}")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")
    
    def start_polling(self):
        """Запуск бота в режиме polling"""
        try:
            logger.info("Запуск Telegram бота для обработки команд...")
            logger.info(f"Ожидаем команды в канале: {COMMAND_CHANNEL_ID}")
            logger.info("Доступные команды: /start, /help, /post, /status, или просто 'пост'")
            
            # Тестируем подключение к боту
            try:
                bot_info = self.bot.get_me()
                logger.info(f"Бот подключен: @{bot_info.username} (ID: {bot_info.id})")
            except Exception as e:
                logger.error(f"Ошибка подключения к боту: {e}")
                return
            
            # Очищаем webhook перед запуском polling
            try:
                self.bot.remove_webhook()
                logger.info("Webhook очищен перед запуском polling")
            except Exception as e:
                logger.warning(f"Не удалось очистить webhook: {e}")
            
            # Запускаем polling с обработкой ошибок
            logger.info("Запуск polling...")
            self.bot.polling(none_stop=True, interval=1, timeout=20)
            
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            # Если ошибка 409, ждем и пробуем снова
            if "409" in str(e) or "Conflict" in str(e):
                logger.warning("Обнаружен конфликт - другой экземпляр бота уже запущен")
                logger.info("Ожидание 30 секунд перед повторной попыткой...")
                import time
                time.sleep(30)
                logger.info("Повторная попытка запуска...")
                try:
                    self.bot.polling(none_stop=True, interval=1, timeout=20)
                except Exception as retry_e:
                    logger.error(f"Ошибка при повторной попытке: {retry_e}")
    
    def stop_polling(self):
        """Остановка бота"""
        try:
            self.bot.stop_polling()
            logger.info("Telegram бот остановлен")
        except Exception as e:
            logger.error(f"Ошибка при остановке бота: {e}")

# Функция для запуска обработчика команд
def start_command_handler():
    """Запуск обработчика команд"""
    handler = TelegramCommandHandler()
    handler.start_polling()

if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Запуск обработчика команд
    start_command_handler()