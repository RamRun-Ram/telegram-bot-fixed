#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест логики времени для публикации постов
"""
from datetime import datetime, timedelta
import pytz

def test_time_logic():
    """Тестирует логику времени"""
    print("🕐 ТЕСТ ЛОГИКИ ВРЕМЕНИ")
    print("=" * 50)
    
    # Текущее время по Москве
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(moscow_tz)
    
    print(f"🕐 Текущее время: {current_time.strftime('%Y-%m-%d %H:%M:%S MSK')}")
    
    # LOOKBACK_MINUTES из config
    LOOKBACK_MINUTES = 5
    
    # Тестовые случаи
    test_cases = [
        ("Сейчас", current_time),
        ("+1 минута", current_time + timedelta(minutes=1)),
        ("+2 минуты", current_time + timedelta(minutes=2)),
        ("+5 минут", current_time + timedelta(minutes=5)),
        ("+10 минут", current_time + timedelta(minutes=10)),
        ("-1 минута", current_time - timedelta(minutes=1)),
        ("-5 минут", current_time - timedelta(minutes=5)),
        ("-10 минут", current_time - timedelta(minutes=10)),
    ]
    
    print(f"\n📊 LOOKBACK_MINUTES: {LOOKBACK_MINUTES}")
    print(f"📝 Условие: -{LOOKBACK_MINUTES} <= time_diff <= 0")
    print(f"\n🧪 ТЕСТОВЫЕ СЛУЧАИ:")
    
    for name, test_time in test_cases:
        # Создаем тестовый пост
        test_post = {
            'date': test_time.strftime('%d.%m.%y'),
            'time': test_time.strftime('%H:%M'),
            'row_index': 999
        }
        
        # Парсим время поста
        try:
            post_datetime = datetime.strptime(f"{test_post['date']} {test_post['time']}", "%d.%m.%y %H:%M")
            post_datetime = moscow_tz.localize(post_datetime)
            
            # Вычисляем разность
            time_diff = (current_time - post_datetime).total_seconds() / 60
            
            # Проверяем условие
            should_publish = -LOOKBACK_MINUTES <= time_diff <= 0
            
            status = "✅ ДА" if should_publish else "❌ НЕТ"
            print(f"  {name:12}: {status} (разница: {time_diff:6.1f} мин)")
            
        except Exception as e:
            print(f"  {name:12}: ❌ ОШИБКА - {e}")
    
    print(f"\n💡 ИНТЕРПРЕТАЦИЯ:")
    print(f"  ✅ ДА - пост должен публиковаться")
    print(f"  ❌ НЕТ - пост не должен публиковаться")
    print(f"  time_diff > 0 - пост в прошлом")
    print(f"  time_diff < 0 - пост в будущем")
    print(f"  time_diff = 0 - пост сейчас")

if __name__ == "__main__":
    test_time_logic()
