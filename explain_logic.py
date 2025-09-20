#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Объяснение логики работы системы публикации постов
"""
from datetime import datetime, timedelta
import pytz

def explain_system_logic():
    """Объясняет логику работы системы"""
    print("🔍 ЛОГИКА РАБОТЫ СИСТЕМЫ ПУБЛИКАЦИИ ПОСТОВ")
    print("=" * 60)
    
    # Текущее время
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz)
    
    print(f"🕐 ТЕКУЩЕЕ ВРЕМЯ: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
    
    # Параметры системы
    CHECK_INTERVAL_MINUTES = 2  # Проверяем каждые 2 минуты
    LOOKBACK_MINUTES = 5        # Ищем посты за последние 5 минут
    
    print(f"\n📊 ПАРАМЕТРЫ СИСТЕМЫ:")
    print(f"   🔄 Проверка каждые: {CHECK_INTERVAL_MINUTES} минуты")
    print(f"   ⏰ Поиск постов: за последние {LOOKBACK_MINUTES} минут")
    
    print(f"\n🧮 ЛОГИКА ВРЕМЕНИ:")
    print(f"   Формула: 0 <= time_diff <= {LOOKBACK_MINUTES}")
    print(f"   time_diff = (текущее_время - время_поста) в минутах")
    print(f"   time_diff > 0  = пост в прошлом")
    print(f"   time_diff = 0  = пост сейчас")
    print(f"   time_diff < 0  = пост в будущем")
    
    print(f"\n✅ ПОСТ ПУБЛИКУЕТСЯ, ЕСЛИ:")
    print(f"   0 <= time_diff <= {LOOKBACK_MINUTES}")
    print(f"   То есть пост должен быть:")
    print(f"   • Сейчас (time_diff = 0)")
    print(f"   • В прошлом (но не более чем на {LOOKBACK_MINUTES} минут)")
    print(f"   • НЕ в будущем!")
    
    # Примеры
    print(f"\n📝 ПРИМЕРЫ:")
    
    examples = [
        ("Пост на +10 минут", current_time + timedelta(minutes=10)),
        ("Пост на +5 минут", current_time + timedelta(minutes=5)),
        ("Пост на +2 минуты", current_time + timedelta(minutes=2)),
        ("Пост на +1 минуту", current_time + timedelta(minutes=1)),
        ("Пост сейчас", current_time),
        ("Пост -1 минуту назад", current_time - timedelta(minutes=1)),
        ("Пост -5 минут назад", current_time - timedelta(minutes=5)),
        ("Пост -10 минут назад", current_time - timedelta(minutes=10)),
    ]
    
    for name, post_time in examples:
        time_diff = (current_time - post_time).total_seconds() / 60
        should_publish = 0 <= time_diff <= LOOKBACK_MINUTES
        status = "✅ ДА" if should_publish else "❌ НЕТ"
        
        print(f"   {name:20}: {status} (разница: {time_diff:6.1f} мин)")
    
    print(f"\n🎯 ПРАКТИЧЕСКИЙ ПРИМЕР:")
    print(f"   Если сейчас {current_time.strftime('%H:%M')}, то публикуются посты:")
    print(f"   • Запланированные на {current_time.strftime('%H:%M')} (сейчас)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=1)).strftime('%H:%M')} (-1 мин)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=2)).strftime('%H:%M')} (-2 мин)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=3)).strftime('%H:%M')} (-3 мин)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=4)).strftime('%H:%M')} (-4 мин)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=5)).strftime('%H:%M')} (-5 мин)")
    
    print(f"\n❌ НЕ ПУБЛИКУЮТСЯ ПОСТЫ:")
    print(f"   • Запланированные на {(current_time + timedelta(minutes=1)).strftime('%H:%M')} (+1 мин)")
    print(f"   • Запланированные на {(current_time + timedelta(minutes=5)).strftime('%H:%M')} (+5 мин)")
    print(f"   • Запланированные на {(current_time + timedelta(minutes=10)).strftime('%H:%M')} (+10 мин)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=6)).strftime('%H:%M')} (-6 мин)")
    print(f"   • Запланированные на {(current_time - timedelta(minutes=10)).strftime('%H:%M')} (-10 мин)")

def check_actual_posts():
    """Проверяет реальные посты в системе"""
    print(f"\n🔍 ПРОВЕРКА РЕАЛЬНЫХ ПОСТОВ")
    print("=" * 60)
    
    try:
        from main import TelegramAutomation
        
        automation = TelegramAutomation()
        moscow_tz = pytz.timezone('Europe/Moscow')
        current_time = datetime.now(moscow_tz)
        
        print(f"🕐 Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
        
        # Получаем посты
        posts = automation.sheets_client.get_pending_posts()
        
        if not posts:
            print("❌ Нет постов со статусом 'Ожидает'")
            return
        
        print(f"📊 Найдено постов: {len(posts)}")
        
        for i, post in enumerate(posts):
            print(f"\n📝 ПОСТ #{i+1}:")
            print(f"   Строка: {post.get('row_index', 'N/A')}")
            print(f"   Дата: {post.get('date', 'N/A')}")
            print(f"   Время: {post.get('time', 'N/A')}")
            print(f"   Статус: {post.get('status', 'N/A')}")
            
            # Проверяем логику времени
            if automation._should_publish_post(post, current_time):
                print(f"   ✅ ДОЛЖЕН ПУБЛИКОВАТЬСЯ")
            else:
                print(f"   ❌ НЕ ПОДХОДИТ ПО ВРЕМЕНИ")
                
                # Детальный анализ
                post_date_str = post.get('date', '')
                post_time_str = post.get('time', '')
                
                try:
                    post_datetime = datetime.strptime(f"{post_date_str} {post_time_str}", "%d.%m.%y %H:%M")
                    post_datetime = moscow_tz.localize(post_datetime)
                    
                    time_diff = (current_time - post_datetime).total_seconds() / 60
                    
                    print(f"   📊 Детали:")
                    print(f"      Время поста: {post_datetime.strftime('%Y-%m-%d %H:%M:%S MSK')}")
                    print(f"      Разница: {time_diff:.1f} минут")
                    print(f"      Условие: -5 <= {time_diff:.1f} <= 0")
                    print(f"      Результат: {-5 <= time_diff <= 0}")
                    
                except Exception as e:
                    print(f"   ❌ Ошибка парсинга времени: {e}")
    
    except Exception as e:
        print(f"❌ Ошибка проверки постов: {e}")

def main():
    """Основная функция"""
    explain_system_logic()
    check_actual_posts()

if __name__ == "__main__":
    main()
