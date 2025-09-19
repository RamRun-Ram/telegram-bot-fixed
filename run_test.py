#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска тестирования системы публикации
"""
import os
import sys
import time
import subprocess
from datetime import datetime
import pytz

def run_test():
    """Запускает тестирование системы"""
    
    print("🧪 Запуск тестирования системы публикации")
    print("=" * 60)
    
    # Получаем текущее время по Москве
    moscow_tz = pytz.timezone('Europe/Moscow')
    now = datetime.now(moscow_tz)
    
    print(f"🕐 Текущее время (Москва): {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ Интервал проверки: каждые 2 минуты")
    print(f"🔍 Поиск постов: за последние 5 минут")
    
    print("\n📋 Доступные команды:")
    print("1. Добавить тестовые посты")
    print("2. Просмотреть посты в таблице")
    print("3. Очистить все посты")
    print("4. Запустить основную систему")
    print("5. Выход")
    
    while True:
        try:
            choice = input("\nВыберите действие (1-5): ").strip()
            
            if choice == "1":
                print("\n📤 Добавляем тестовые посты...")
                result = subprocess.run([sys.executable, "add_test_posts.py"], 
                                      capture_output=True, text=True, encoding='utf-8')
                print(result.stdout)
                if result.stderr:
                    print("Ошибки:", result.stderr)
                    
            elif choice == "2":
                print("\n👀 Просматриваем посты...")
                result = subprocess.run([sys.executable, "view_posts.py"], 
                                      capture_output=True, text=True, encoding='utf-8')
                print(result.stdout)
                if result.stderr:
                    print("Ошибки:", result.stderr)
                    
            elif choice == "3":
                print("\n🗑️ Очищаем посты...")
                result = subprocess.run([sys.executable, "clear_test_posts.py"], 
                                      capture_output=True, text=True, encoding='utf-8')
                print(result.stdout)
                if result.stderr:
                    print("Ошибки:", result.stderr)
                    
            elif choice == "4":
                print("\n🚀 Запускаем основную систему...")
                print("⚠️ Система будет проверять таблицу каждые 2 минуты")
                print("⚠️ Нажмите Ctrl+C для остановки")
                try:
                    subprocess.run([sys.executable, "main.py"])
                except KeyboardInterrupt:
                    print("\n⏹️ Система остановлена")
                    
            elif choice == "5":
                print("\n👋 Выход из программы")
                break
                
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\n👋 Выход из программы")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    run_test()
