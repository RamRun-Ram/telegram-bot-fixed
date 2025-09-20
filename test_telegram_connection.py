#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование подключения к Telegram каналу
"""
import os
import sys
import asyncio

async def test_telegram_connection():
    """Тестирует подключение к Telegram каналу"""
    print("🔧 ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ К TELEGRAM КАНАЛУ")
    print("=" * 60)
    
    try:
        from telegram_client import TelegramClient
        from config import TELEGRAM_CHANNEL_ID, TELEGRAM_BOT_TOKEN
        
        print(f"📱 TELEGRAM_BOT_TOKEN: {'установлен' if TELEGRAM_BOT_TOKEN and not TELEGRAM_BOT_TOKEN.startswith('YOUR_') else 'НЕ УСТАНОВЛЕН'}")
        print(f"📺 TELEGRAM_CHANNEL_ID: {TELEGRAM_CHANNEL_ID}")
        
        # Создаем клиент
        client = TelegramClient()
        
        # Тестируем подключение
        print(f"\n🔌 Тестируем подключение к Telegram...")
        connection_ok = await client.test_connection()
        
        if connection_ok:
            print(f"✅ Подключение к Telegram успешно!")
            
            # Пробуем отправить тестовое сообщение
            print(f"\n📤 Отправляем тестовое сообщение...")
            test_text = "🧪 Тестовое сообщение для проверки подключения к каналу"
            
            success = await client.send_text_message(test_text)
            
            if success:
                print(f"✅ Тестовое сообщение отправлено успешно!")
                print(f"📱 Проверьте канал: {TELEGRAM_CHANNEL_ID}")
                return True
            else:
                print(f"❌ Ошибка отправки тестового сообщения")
                return False
        else:
            print(f"❌ Ошибка подключения к Telegram")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_channel_access():
    """Тестирует доступ к каналу разными способами"""
    print("\n🔍 ТЕСТИРОВАНИЕ ДОСТУПА К КАНАЛУ")
    print("=" * 60)
    
    try:
        from telegram_client import TelegramClient
        from config import TELEGRAM_CHANNEL_ID
        
        client = TelegramClient()
        
        # Тестируем разные форматы ID канала
        test_ids = [
            TELEGRAM_CHANNEL_ID,
            str(TELEGRAM_CHANNEL_ID),
            f"@{TELEGRAM_CHANNEL_ID}" if not str(TELEGRAM_CHANNEL_ID).startswith('@') else TELEGRAM_CHANNEL_ID,
            int(TELEGRAM_CHANNEL_ID) if str(TELEGRAM_CHANNEL_ID).startswith('-100') else TELEGRAM_CHANNEL_ID
        ]
        
        for i, test_id in enumerate(test_ids):
            print(f"\n🧪 Тест {i+1}: {test_id} (тип: {type(test_id)})")
            
            try:
                chat_info = await client.bot.get_chat(test_id)
                print(f"   ✅ Успешно: {chat_info.title} (ID: {chat_info.id})")
                return True
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Ошибка тестирования канала: {e}")
        return False

async def main():
    """Основная функция"""
    print("🔧 ПОЛНОЕ ТЕСТИРОВАНИЕ TELEGRAM ПОДКЛЮЧЕНИЯ")
    print("=" * 70)
    
    # Тестируем подключение
    connection_ok = await test_telegram_connection()
    
    # Тестируем доступ к каналу
    channel_ok = await test_channel_access()
    
    print(f"\n📊 РЕЗУЛЬТАТЫ:")
    print(f"   Подключение к Telegram: {'✅ OK' if connection_ok else '❌ ERROR'}")
    print(f"   Доступ к каналу: {'✅ OK' if channel_ok else '❌ ERROR'}")
    
    if connection_ok and channel_ok:
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print(f"📱 Telegram канал готов к работе")
    else:
        print(f"\n❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        if not connection_ok:
            print(f"   - Проверьте TELEGRAM_BOT_TOKEN")
        if not channel_ok:
            print(f"   - Проверьте TELEGRAM_CHANNEL_ID")
            print(f"   - Убедитесь, что бот добавлен в канал")
            print(f"   - Убедитесь, что бот имеет права администратора")

if __name__ == "__main__":
    asyncio.run(main())
