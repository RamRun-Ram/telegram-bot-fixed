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
from google_sheets_client_simple import GoogleSheetsClient
from config import TELEGRAM_BOT_TOKEN, NOTIFICATION_CHANNEL_ID, COMMAND_CHANNEL_ID

logger = logging.getLogger(__name__)

class TelegramCommandHandler:
    """Обработчик команд Telegram для управления постами"""
    
    def __init__(self):
        self.bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        self.sheets_client = GoogleSheetsClient()
        self.ai_generator = AIPostGenerator()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        
        def is_authorized_user(message):
            """Проверяет, что пользователь авторизован для использования команд"""
            # Разрешаем команды из группы AlertChanel
            if str(message.chat.id) == COMMAND_CHANNEL_ID or message.chat.username == "alertchanel":
                logger.info(f"Команда из группы AlertChanel: {message.text}")
                return True
            
            # Разрешаем команды из личных сообщений (для тестирования)
            if message.chat.type == 'private':
                logger.info(f"Команда из личного чата: {message.text}")
                return True
            
            logger.info(f"Команда отклонена из чата {message.chat.id} (тип: {message.chat.type}): {message.text}")
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
                    success = asyncio.run(self.ai_generator.generate_and_upload_weekly_posts())
                    
                    if success:
                        # Обновляем статус
                        self.bot.edit_message_text(
                            "✅ Посты успешно сгенерированы и загружены в Google Таблицу!\n\n"
                            "📊 Создано 9 постов на 3 дня:\n"
                            "• 3 утренних поста (08:00)\n"
                            "• 3 обеденных поста (14:00) с изображениями\n"
                            "• 3 вечерних поста (20:00)\n\n"
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
            self.bot.polling(none_stop=True, interval=1)
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
    
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