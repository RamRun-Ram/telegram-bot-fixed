"""
Система уведомлений для администраторов
"""
import logging
from typing import Dict, Any, Optional
from telegram_client import TelegramClient
from config import ADMIN_CHAT_ID, NOTIFICATION_CHANNEL_ID, ALERT_ADMIN_CHANNEL

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
        self.alert_channel_id = ALERT_ADMIN_CHANNEL
    
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
    
    async def send_check_notification(self, total_pending: int, published_count: int, errors_count: int, current_time: str):
        """Отправляет уведомление о результатах проверки в AlertChanel"""
        try:
            # Определяем статус проверки
            if errors_count > 0:
                status_emoji = "⚠️"
                status_text = "с ошибками"
            elif published_count > 0:
                status_emoji = "✅"
                status_text = "успешно"
            else:
                status_emoji = "ℹ️"
                status_text = "без публикаций"
            
            message = f"{status_emoji} <b>ПРОВЕРКА ЗАВЕРШЕНА</b>\n\n"
            message += f"🕐 <b>Время:</b> {current_time} (Москва)\n"
            message += f"📊 <b>Статус:</b> {status_text}\n\n"
            message += f"📝 <b>Найдено постов:</b> {total_pending}\n"
            message += f"✅ <b>Опубликовано:</b> {published_count}\n"
            message += f"❌ <b>Ошибок:</b> {errors_count}\n"
            
            if published_count > 0:
                message += f"\n🎉 <b>Успешно опубликовано {published_count} постов!</b>"
            elif total_pending > 0:
                message += f"\n⏰ <b>Найдено {total_pending} постов, но время публикации еще не наступило</b>"
            else:
                message += f"\n😴 <b>Нет постов для публикации</b>"
            
            # Отправляем в AlertChanel
            await self._send_alert_notification(message)
            
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления о проверке: {e}")
    
    async def _send_alert_notification(self, message: str):
        """Отправляет уведомление в AlertChanel"""
        try:
            if self.alert_channel_id:
                await self.telegram_client.bot.send_message(
                    chat_id=self.alert_channel_id,
                    text=message,
                    parse_mode='HTML'
                )
                logger.info("Уведомление о проверке отправлено в AlertChanel")
            else:
                logger.warning("AlertChanel не настроен")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления в AlertChanel: {e}")
    
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
