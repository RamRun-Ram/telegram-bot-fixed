"""
Система уведомлений для администраторов
"""
import logging
from typing import Dict, Any, Optional
from telegram_client import TelegramClient
from config import ADMIN_CHAT_ID, NOTIFICATION_CHANNEL_ID

logger = logging.getLogger(__name__)

class NotificationType:
    INFO = "info"
    ERROR = "error"
    WARNING = "warning"

class NotificationSystem:
    """Система уведомлений для администраторов"""
    
    def __init__(self, telegram_client: TelegramClient):
        self.telegram_client = telegram_client
        self.admin_chat_id = ADMIN_CHAT_ID
        self.notification_channel_id = NOTIFICATION_CHANNEL_ID
    
    async def send_info_notification(self, title: str, details: Dict[str, str]):
        """Отправляет информационное уведомление"""
        try:
            message = f"📢 {title}\n\n"
            for key, value in details.items():
                message += f"• {key}: {value}\n"
            
            await self._send_notification(message, NotificationType.INFO)
        except Exception as e:
            logger.error(f"Ошибка отправки информационного уведомления: {e}")
    
    async def send_error_notification(self, message: str, post: Optional[Dict[str, Any]] = None):
        """Отправляет уведомление об ошибке"""
        try:
            error_message = f"❌ ОШИБКА ПУБЛИКАЦИИ\n\n"
            error_message += f"Сообщение: {message}\n"
            
            if post:
                error_message += f"\nДетали поста:\n"
                error_message += f"• Дата: {post.get('date', 'Неизвестно')}\n"
                error_message += f"• Время: {post.get('time', 'Неизвестно')}\n"
                error_message += f"• Длина: {len(post.get('text', ''))} символов\n"
                error_message += f"• Изображения: {'да' if post.get('image_urls') else 'нет'}\n"
            
            await self._send_notification(error_message, NotificationType.ERROR)
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления об ошибке: {e}")
    
    async def _send_notification(self, message: str, notification_type: str):
        """Отправляет уведомление в канал или чат"""
        try:
            # Сначала пытаемся отправить в канал уведомлений
            if self.notification_channel_id:
                try:
                    success = await self.telegram_client.bot.send_message(
                        chat_id=self.notification_channel_id,
                        text=message,
                        parse_mode='HTML'
                    )
                    if success:
                        logger.info(f"Уведомление отправлено в канал: {notification_type}")
                        return
                except Exception as e:
                    logger.warning(f"Не удалось отправить в канал уведомлений: {e}")
            
            # Если не получилось, отправляем в админский чат
            if self.admin_chat_id:
                await self.telegram_client.bot.send_message(
                    chat_id=self.admin_chat_id,
                    text=message,
                    parse_mode='HTML'
                )
                logger.info(f"Уведомление отправлено в админский чат: {notification_type}")
            else:
                logger.warning("Не настроен админский чат для уведомлений")
                
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")
