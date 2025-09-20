"""
Клиент для работы с Telegram Bot API
"""
import logging
from typing import List
import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)

class TelegramClient:
    """Клиент для работы с Telegram Bot API"""
    
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.channel_id = self._normalize_channel_id(TELEGRAM_CHANNEL_ID)
        self.bot = AsyncTeleBot(self.bot_token)
        logger.info(f"TelegramClient инициализирован с channel_id: {self.channel_id}")
    
    def _normalize_channel_id(self, channel_id: str) -> str:
        """Нормализует ID канала для Telegram API"""
        if not channel_id:
            return channel_id
        
        # Убираем @ если есть
        if channel_id.startswith('@'):
            return channel_id[1:]
        
        # Если это числовой ID, конвертируем в int
        if channel_id.startswith('-100'):
            try:
                return int(channel_id)
            except ValueError:
                pass
        
        return channel_id
    
    async def test_connection(self) -> bool:
        """Проверяет соединение с Telegram Bot API"""
        try:
            bot_info = await self.bot.get_me()
            logger.info(f"Бот подключен: @{bot_info.username}")
            
            # Проверяем доступ к каналу
            try:
                chat_info = await self.bot.get_chat(self.channel_id)
                logger.info(f"Канал доступен: {chat_info.title} (ID: {chat_info.id})")
                return True
            except Exception as e:
                logger.error(f"Ошибка доступа к каналу {self.channel_id}: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка подключения к Telegram: {e}")
            return False
    
    async def send_post(self, text: str, image_urls: List[str] = None) -> bool:
        """
        Отправляет пост в Telegram канал (универсальный метод)
        """
        try:
            if image_urls and len(image_urls) > 0:
                return await self.send_image_post(text, image_urls)
            else:
                return await self.send_text_message(text)
        except Exception as e:
            logger.error(f"Ошибка отправки поста: {e}")
            return False
    
    async def send_html_post_with_image(self, text: str, image_urls: List[str]) -> bool:
        """
        МЕТОД 1: Отправляет HTML пост С изображениями (для обеденных постов)
        """
        try:
            if not image_urls or len(image_urls) == 0:
                logger.error("Нет изображений для HTML поста")
                return False
            
            # Обрабатываем текст для постов с изображениями
            processed_text = self._process_text_for_image_posts(text)
            image_url = image_urls[0]
            
            logger.info(f"Отправляем HTML пост с изображением: {image_url}")
            logger.info(f"Длина текста: {len(processed_text)} символов")
            
            # Создаем новый экземпляр бота для этого запроса
            bot = AsyncTeleBot(self.bot_token)
            
            # Пробуем сначала метод с невидимым символом
            try:
                invisible_char = "&#8288;"  # Word Joiner
                message_text = f'<a href="{image_url}">{invisible_char}</a>{processed_text}'
                
                await bot.send_message(
                    chat_id=self.channel_id,
                    text=message_text,
                    parse_mode='HTML',
                    disable_web_page_preview=False
                )
                
                logger.info("HTML пост с изображением отправлен через невидимый символ")
                return True
                
            except Exception as e:
                logger.warning(f"Не удалось отправить через невидимый символ: {e}")
                
                # Если не получилось, пробуем отправить фото с подписью
                try:
                    # Ограничиваем длину подписи до 1000 символов для фото
                    caption = processed_text[:1000] if len(processed_text) > 1000 else processed_text
                    
                    await bot.send_photo(
                        chat_id=self.channel_id,
                        photo=image_url,
                        caption=caption,
                        parse_mode='HTML'
                    )
                    
                    # Если текст длиннее 1000 символов, отправляем остаток отдельным сообщением
                    if len(processed_text) > 1000:
                        remaining_text = processed_text[1000:]
                        await bot.send_message(
                            chat_id=self.channel_id,
                            text=remaining_text,
                            parse_mode='HTML'
                        )
                    
                    logger.info("HTML пост с изображением отправлен как фото с подписью")
                    return True
                    
                except Exception as e2:
                    logger.error(f"Не удалось отправить как фото: {e2}")
                    raise e2
            
        except Exception as e:
            logger.error(f"Ошибка отправки HTML поста с изображением: {e}")
            return False
    
    async def send_markdown_post(self, text: str) -> bool:
        """
        МЕТОД 2: Отправляет Markdown пост БЕЗ изображений (для утренних и вечерних постов)
        """
        try:
            # Обрабатываем текст для Markdown постов
            formatted_text = self.format_text_for_telegram_markdown(text)
            
            # Создаем новый экземпляр бота для этого запроса
            bot = AsyncTeleBot(self.bot_token)
            
            await bot.send_message(
                chat_id=self.channel_id,
                text=formatted_text,
                parse_mode='Markdown'
            )
            
            logger.info("Markdown пост без изображения отправлен")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки Markdown поста: {e}")
            return False
    
    async def send_image_post(self, text: str, image_urls: List[str]) -> bool:
        """
        МЕТОД 1: Отправляет пост С изображениями
        Использует HTML с невидимым символом (изображение внутри поста, до 4000 символов)
        """
        try:
            if not image_urls or len(image_urls) == 0:
                return False
            
            # Обрабатываем текст для постов с изображениями
            processed_text = self._process_text_for_image_posts(text)
            
            # Используем HTML с невидимым символом (изображение внутри поста)
            image_url = image_urls[0]
            invisible_char = "&#8288;"  # Word Joiner
            
            # Формируем сообщение с невидимой ссылкой (изображение внутри поста)
            message_text = f'<a href="{image_url}">{invisible_char}</a>{processed_text}'
            
            # Создаем новый экземпляр бота для этого запроса
            bot = AsyncTeleBot(self.bot_token)
            
            await bot.send_message(
                chat_id=self.channel_id,
                text=message_text,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
            logger.info("Пост с изображением отправлен через HTML с невидимым символом (до 4000 символов)")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки поста с изображением: {e}")
            return False
    
    async def send_text_message(self, text: str) -> bool:
        """
        МЕТОД 2: Отправляет пост БЕЗ изображений
        Использует HTML конвертацию для форматирования
        """
        try:
            # Конвертируем Markdown в HTML для постов без изображений
            formatted_text = self.format_text_for_telegram_html(text)
            
            # Создаем новый экземпляр бота для этого запроса
            bot = AsyncTeleBot(self.bot_token)
            
            await bot.send_message(
                chat_id=self.channel_id,
                text=formatted_text,
                parse_mode='HTML'
            )
            
            logger.info("Пост без изображения отправлен через HTML конвертацию")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки текстового поста: {e}")
            return False
    
    def _process_text_for_image_posts(self, text: str) -> str:
        """
        Обрабатывает текст для постов с изображениями (HTML формат)
        Оставляет HTML теги как есть для корректного отображения
        """
        # Заменяем <br> на переносы строк для лучшего отображения
        text = text.replace('<br>', '\n')
        text = text.replace('<br/>', '\n')
        text = text.replace('<br />', '\n')
        
        # Удаляем только неподдерживаемые HTML теги, оставляем <b>, <i>, <u>
        text = text.replace('<div>', '')
        text = text.replace('</div>', '')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '')
        
        # Обрабатываем списки
        text = text.replace('<ul>', '')
        text = text.replace('</ul>', '')
        text = text.replace('<ol>', '')
        text = text.replace('</ol>', '')
        text = text.replace('<li>', '• ')
        text = text.replace('</li>', '\n')
        
        # НЕ конвертируем <b>, <i>, <u> - оставляем HTML для постов с изображениями
        # Telegram поддерживает эти теги в HTML режиме
        
        return text
    
    def format_text_for_telegram_markdown(self, text: str) -> str:
        """
        Обрабатывает текст для Markdown постов (без изображений)
        """
        # Заменяем HTML теги на Markdown
        text = text.replace('<b>', '**')
        text = text.replace('</b>', '**')
        text = text.replace('<i>', '*')
        text = text.replace('</i>', '*')
        text = text.replace('<u>', '__')
        text = text.replace('</u>', '__')
        text = text.replace('<br>', '\n')
        text = text.replace('<br/>', '\n')
        text = text.replace('<br />', '\n')
        
        # Удаляем HTML теги
        text = text.replace('<div>', '')
        text = text.replace('</div>', '')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '')
        
        return text
    
    def format_text_for_telegram_html(self, text: str) -> str:
        """
        Конвертирует Markdown в HTML для Telegram
        """
        import re
        
        # Жирный текст - исправляем парсинг
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Курсив - исправляем парсинг
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        
        # Подчеркнутый - исправляем парсинг
        text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)
        
        # Зачеркнутый - исправляем парсинг
        text = re.sub(r'~~(.*?)~~', r'<s>\1</s>', text)
        
        # Моноширинный - исправляем парсинг
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        
        # Блок кода - исправляем парсинг
        text = re.sub(r'```(.*?)```', r'<pre>\1</pre>', text, flags=re.DOTALL)
        
        # Ссылки
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Цитаты - обрабатываем многострочные цитаты
        text = re.sub(r'^> (.+?)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)
        
        return text
