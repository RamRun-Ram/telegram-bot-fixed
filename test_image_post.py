#!/usr/bin/env python3
"""
Тестирование поста с изображением
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import pytz

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_client import TelegramClient
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

async def test_image_post():
    """Тестирует отправку поста с изображением"""
    
    print("🔧 Тестирование поста с изображением...")
    
    # Инициализируем клиент
    client = TelegramClient(TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID)
    
    # Тестируем соединение
    if not await client.test_connection():
        print("❌ Ошибка соединения с Telegram")
        return
    
    print("✅ Соединение с Telegram установлено")
    
    # Создаем тестовый пост с длинным текстом
    long_text = """
<b>Тестовый пост с изображением</b>

Это очень длинный пост для проверки лимита символов. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

<i>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</i>

<b>Вторая часть поста:</b>
Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

<u>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</u>

<b>Третья часть поста:</b>
Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.

<i>Ut enim ad minima veniam, quis nostrud exercitationem ullamco laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur.</i>

<b>Четвертая часть поста:</b>
At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident.

<u>Similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio.</u>

<b>Пятая часть поста:</b>
Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.

<i>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae.</i>

<b>Заключение:</b>
Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.

Этот пост должен содержать более 2000 символов и изображение должно появиться внизу с предпросмотром.
    """.strip()
    
    # URL изображения для теста
    image_url = "https://picsum.photos/800/600"
    
    print(f"📝 Длина текста: {len(long_text)} символов")
    print(f"🖼️ URL изображения: {image_url}")
    
    # Отправляем пост с изображением
    success = await client.send_html_post_with_image(long_text, [image_url])
    
    if success:
        print("✅ Пост с изображением отправлен успешно!")
        print("📱 Проверьте канал - изображение должно быть внизу поста с предпросмотром")
    else:
        print("❌ Ошибка отправки поста с изображением")
    
    # Также тестируем пост без изображения для сравнения
    print("\n🔧 Тестирование поста БЕЗ изображения...")
    
    short_text = """
**Тестовый пост без изображения**

Это короткий пост для проверки Markdown форматирования.

*Курсивный текст*
**Жирный текст**
__Подчеркнутый текст__

- Список 1
- Список 2
- Список 3

Этот пост должен использовать Markdown форматирование.
    """.strip()
    
    success2 = await client.send_markdown_post(short_text)
    
    if success2:
        print("✅ Пост без изображения отправлен успешно!")
        print("📱 Проверьте канал - должен использовать Markdown форматирование")
    else:
        print("❌ Ошибка отправки поста без изображения")

if __name__ == "__main__":
    asyncio.run(test_image_post())
