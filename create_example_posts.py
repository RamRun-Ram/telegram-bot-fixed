#!/usr/bin/env python3
"""
Создание примеров постов с разными типами изображений
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

async def create_example_posts():
    """Создает примеры постов с разными типами изображений"""
    
    print("🔧 Создание примеров постов с разными типами изображений...")
    
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
    
    # ПРИМЕР 1: Пост БЕЗ изображений
    print("\n📝 Создаем пример 1: Пост БЕЗ изображений")
    post1_time = (base_time + timedelta(minutes=1)).strftime("%H:%M")
    post1_date = (base_time + timedelta(minutes=1)).strftime("%d.%m.%Y")
    
    text1 = """
**Утренний пост без изображений**

Доброе утро! Сегодня прекрасный день для новых начинаний.

**Планы на день:**
- Встреча с командой
- Работа над проектом
- Спортивная тренировка

*Желаю всем продуктивного дня!*
    """.strip()
    
    posts.append({
        'date': post1_date,
        'time': post1_time,
        'text': text1,
        'prompt_ru': 'Утренний пост',
        'prompt_en': 'Morning post',
        'image_urls': '',  # ПУСТАЯ СТРОКА - нет изображений
        'status': STATUS_PENDING,
        'description': 'Пост БЕЗ изображений (Markdown метод)'
    })
    
    # ПРИМЕР 2: Пост с ОДНИМ изображением
    print("🖼️ Создаем пример 2: Пост с ОДНИМ изображением")
    post2_time = (base_time + timedelta(minutes=2)).strftime("%H:%M")
    post2_date = (base_time + timedelta(minutes=2)).strftime("%d.%m.%Y")
    
    text2 = """
<b>Обеденный пост с одним изображением</b>

<i>Время обеда!</i> Сегодня у нас вкусный обед с командой.

<b>Меню:</b>
- Салат из свежих овощей
- Горячее блюдо
- Десерт

<u>Приятного аппетита всем!</u>

<b>Длинный текст для проверки лимита символов:</b>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.

Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incididunt ut labore et dolore magnam aliquam quaerat voluptatem.

Ut enim ad minima veniam, quis nostrud exercitationem ullamco laboris nisi ut aliquid ex ea commodo consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur.

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
        'prompt_ru': 'Обеденный пост',
        'prompt_en': 'Lunch post',
        'image_urls': 'https://picsum.photos/800/600?random=1',  # ОДНА ССЫЛКА
        'status': STATUS_PENDING,
        'description': 'Пост с ОДНИМ изображением (HTML метод)'
    })
    
    # ПРИМЕР 3: Пост с НЕСКОЛЬКИМИ изображениями
    print("🖼️🖼️ Создаем пример 3: Пост с НЕСКОЛЬКИМИ изображениями")
    post3_time = (base_time + timedelta(minutes=3)).strftime("%H:%M")
    post3_date = (base_time + timedelta(minutes=3)).strftime("%d.%m.%Y")
    
    text3 = """
**Вечерний пост с несколькими изображениями**

*Время подводить итоги дня!*

**Что мы сделали сегодня:**
- Завершили важный проект
- Провели успешную презентацию
- Отпраздновали достижения

**Результаты:**
- Проект сдан в срок
- Клиент доволен результатом
- Команда мотивирована

*Спасибо всем за отличную работу!*

**Завтра планируем:**
- Новые задачи
- Развитие проекта
- Командные активности

*До встречи завтра!* 🎉
    """.strip()
    
    posts.append({
        'date': post3_date,
        'time': post3_time,
        'text': text3,
        'prompt_ru': 'Вечерний пост',
        'prompt_en': 'Evening post',
        'image_urls': 'https://picsum.photos/800/600?random=1, https://picsum.photos/800/600?random=2, https://picsum.photos/800/600?random=3, https://picsum.photos/800/600?random=4, https://picsum.photos/800/600?random=5',  # НЕСКОЛЬКО ССЫЛОК ЧЕРЕЗ ЗАПЯТУЮ
        'status': STATUS_PENDING,
        'description': 'Пост с НЕСКОЛЬКИМИ изображениями (Markdown метод с медиагруппой)'
    })
    
    # Добавляем все посты в Google Sheets
    for i, post in enumerate(posts, 1):
        print(f"\n📝 Добавляем {post['description']}")
        print(f"   Длина текста: {len(post['text'])} символов")
        print(f"   Изображения: '{post['image_urls']}'")
        
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
    
    print(f"\n🎯 Примеры созданы!")
    print(f"📊 Создано {len(posts)} примеров постов:")
    print(f"   1. Пост БЕЗ изображений - пустая ячейка в колонке 'Изображение'")
    print(f"   2. Пост с ОДНИМ изображением - одна ссылка")
    print(f"   3. Пост с НЕСКОЛЬКИМИ изображениями - несколько ссылок через запятую")
    
    print(f"\n📋 ИНСТРУКЦИЯ ДЛЯ GOOGLE ТАБЛИЦЫ:")
    print(f"   Колонка 'Изображение' (F):")
    print(f"   - Без изображений: (пустая ячейка)")
    print(f"   - 1 изображение: https://example.com/image1.jpg")
    print(f"   - 2+ изображений: https://example.com/image1.jpg, https://example.com/image2.jpg")
    
    print(f"\n📱 Посты будут опубликованы в течение 2-3 минут")
    print(f"🔍 Проверьте канал для подтверждения работы всех методов")

if __name__ == "__main__":
    asyncio.run(create_example_posts())
