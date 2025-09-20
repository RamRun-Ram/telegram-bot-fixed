#!/usr/bin/env python3
"""
Тестирование всех трех методов отправки постов
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
import pytz

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google_sheets_client import GoogleSheetsClient
from config import GOOGLE_SHEET_ID, STATUS_PENDING

async def create_all_test_posts():
    """Создает тестовые посты для всех трех методов"""
    
    print("🔧 Создание тестовых постов для всех методов...")
    
    # Инициализируем клиент Google Sheets
    sheets_client = GoogleSheetsClient()
    
    if not sheets_client.service:
        print("❌ Google Sheets API не инициализирован")
        return
    
    print("✅ Google Sheets API инициализирован")
    
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    # Базовое время
    base_time = now
    posts = []
    
    # ТЕСТ 1: Пост БЕЗ изображений (Markdown метод)
    print("\n📝 Создаем тест 1: Пост БЕЗ изображений")
    post1_time = (base_time + timedelta(minutes=1)).strftime("%H:%M")
    post1_date = (base_time + timedelta(minutes=1)).strftime("%d.%m.%Y")
    
    text1 = f"""
**ТЕСТ 1: Пост БЕЗ изображений**

*Время: {post1_time} MSK*

Это тестовый пост без изображений. Должен использовать Markdown метод.

**Особенности:**
- Markdown форматирование
- До 4000 символов
- Без изображений

*Проверяем форматирование:*
- **Жирный текст**
- *Курсивный текст*
- __Подчеркнутый текст__

**Список:**
- Элемент 1
- Элемент 2
- Элемент 3

*Этот пост должен отправиться через send_markdown_post()*
    """.strip()
    
    posts.append({
        'date': post1_date,
        'time': post1_time,
        'text': text1,
        'prompt_ru': 'Тест 1 - без изображений',
        'prompt_en': 'Test 1 - no images',
        'image_urls': '',  # Нет изображений
        'status': STATUS_PENDING,
        'description': 'Пост БЕЗ изображений (Markdown метод)'
    })
    
    # ТЕСТ 2: Пост с ОДНИМ изображением (HTML метод)
    print("🖼️ Создаем тест 2: Пост с ОДНИМ изображением")
    post2_time = (base_time + timedelta(minutes=2)).strftime("%H:%M")
    post2_date = (base_time + timedelta(minutes=2)).strftime("%d.%m.%Y")
    
    text2 = f"""
<b>ТЕСТ 2: Пост с ОДНИМ изображением</b>

<i>Время: {post2_time} MSK</i>

Это тестовый пост с одним изображением. Должен использовать HTML метод.

<b>Особенности:</b>
- HTML форматирование
- До 4000 символов
- Одно изображение с предпросмотром

<i>Проверяем форматирование:</i>
- <b>Жирный текст</b>
- <i>Курсивный текст</i>
- <u>Подчеркнутый текст</u>

<b>Список:</b>
- Элемент 1
- Элемент 2
- Элемент 3

<i>Этот пост должен отправиться через send_html_post_with_image()</i>

<b>Длинный текст для проверки лимита символов:</b>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.

Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incididunt ut labore et dolore magnam aliquam quaerat voluptatem.

Ut enim ad minima veniam, quis nostrud exercitationem ullamco laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur.

At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident.

Similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio.

Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.

Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae.

Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.

<b>Конец длинного текста</b>
    """.strip()
    
    posts.append({
        'date': post2_date,
        'time': post2_time,
        'text': text2,
        'prompt_ru': 'Тест 2 - одно изображение',
        'prompt_en': 'Test 2 - single image',
        'image_urls': 'https://picsum.photos/800/600?random=1',
        'status': STATUS_PENDING,
        'description': 'Пост с ОДНИМ изображением (HTML метод)'
    })
    
    # ТЕСТ 3: Пост с НЕСКОЛЬКИМИ изображениями (Markdown метод с медиагруппой)
    print("🖼️🖼️ Создаем тест 3: Пост с НЕСКОЛЬКИМИ изображениями")
    post3_time = (base_time + timedelta(minutes=3)).strftime("%H:%M")
    post3_date = (base_time + timedelta(minutes=3)).strftime("%d.%m.%Y")
    
    text3 = f"""
**ТЕСТ 3: Пост с НЕСКОЛЬКИМИ изображениями**

*Время: {post3_time} MSK*

Это тестовый пост с несколькими изображениями. Должен использовать Markdown метод с медиагруппой.

**Особенности:**
- Markdown форматирование
- До 1000 символов
- Медиагруппа с изображениями

*Проверяем форматирование:*
- **Жирный текст**
- *Курсивный текст*
- __Подчеркнутый текст__

**Список:**
- Элемент 1
- Элемент 2
- Элемент 3

*Этот пост должен отправиться через send_markdown_post_with_multiple_images()*

**Заключение:**
Новый метод позволяет отправлять посты с несколькими изображениями, используя медиагруппу Telegram. Это более эффективно, чем отправка каждого изображения отдельно.

*Тест завершен!* 🎉
    """.strip()
    
    posts.append({
        'date': post3_date,
        'time': post3_time,
        'text': text3,
        'prompt_ru': 'Тест 3 - несколько изображений',
        'prompt_en': 'Test 3 - multiple images',
        'image_urls': 'https://picsum.photos/800/600?random=1, https://picsum.photos/800/600?random=2, https://picsum.photos/800/600?random=3, https://picsum.photos/800/600?random=4, https://picsum.photos/800/600?random=5',
        'status': STATUS_PENDING,
        'description': 'Пост с НЕСКОЛЬКИМИ изображениями (Markdown метод с медиагруппой)'
    })
    
    # Добавляем все посты в Google Sheets
    for i, post in enumerate(posts, 1):
        print(f"\n📝 Добавляем {post['description']}")
        print(f"   Длина текста: {len(post['text'])} символов")
        print(f"   Изображения: {len(post['image_urls'].split(', ')) if post['image_urls'] else 0}")
        
        post_data = {
            'date': post['date'],
            'time': post['time'],
            'text': post['text'],
            'prompt_ru': post['prompt_ru'],
            'prompt_en': post['prompt_en'],
            'image_urls': post['image_urls'],
            'status': post['status']
        }
        
        success = sheets_client.add_post(post_data)
        
        if success:
            print(f"   ✅ Пост {i} добавлен успешно")
        else:
            print(f"   ❌ Ошибка добавления поста {i}")
    
    print(f"\n🎯 Тестирование завершено!")
    print(f"📊 Создано {len(posts)} тестовых постов:")
    print(f"   1. Пост БЕЗ изображений (Markdown метод)")
    print(f"   2. Пост с ОДНИМ изображением (HTML метод)")
    print(f"   3. Пост с НЕСКОЛЬКИМИ изображениями (Markdown метод с медиагруппой)")
    print(f"\n📱 Посты будут опубликованы в течение 2-3 минут")
    print(f"🔍 Проверьте канал для подтверждения работы всех методов")

if __name__ == "__main__":
    asyncio.run(create_all_test_posts())
