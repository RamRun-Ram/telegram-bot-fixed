#!/usr/bin/env python3
"""
Проверка текущей логики отправки постов
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_telegram_client_logic():
    """Проверяет логику в telegram_client.py"""
    
    print("🔍 Проверка логики отправки постов...")
    
    try:
        with open('telegram_client.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("\n📋 Анализ метода send_html_post_with_image:")
        
        # Ищем метод send_html_post_with_image
        if 'async def send_html_post_with_image(self, text: str, image_urls: List[str]) -> bool:' in content:
            print("✅ Метод send_html_post_with_image найден")
            
            # Ищем строку с добавлением изображения
            if 'message_text = f\'{processed_text}\\n\\n<a href="{image_url}">🖼️ Изображение</a>\'' in content:
                print("✅ Изображение добавляется в конец поста")
            else:
                print("❌ Изображение НЕ добавляется в конец поста")
                
            # Ищем disable_web_page_preview=False
            if 'disable_web_page_preview=False' in content:
                print("✅ Предпросмотр изображения включен")
            else:
                print("❌ Предпросмотр изображения отключен")
                
            # Ищем parse_mode='HTML'
            if 'parse_mode=\'HTML\'' in content:
                print("✅ Используется HTML форматирование")
            else:
                print("❌ НЕ используется HTML форматирование")
        
        print("\n📋 Анализ метода send_markdown_post:")
        
        # Ищем метод send_markdown_post
        if 'async def send_markdown_post(self, text: str) -> bool:' in content:
            print("✅ Метод send_markdown_post найден")
            
            # Ищем parse_mode='Markdown'
            if 'parse_mode=\'Markdown\'' in content:
                print("✅ Используется Markdown форматирование")
            else:
                print("❌ НЕ используется Markdown форматирование")
        
        print("\n📋 Анализ метода _process_text_for_image_posts:")
        
        # Ищем метод _process_text_for_image_posts
        if 'def _process_text_for_image_posts(self, text: str) -> str:' in content:
            print("✅ Метод _process_text_for_image_posts найден")
            
            # Проверяем, что HTML теги НЕ конвертируются в Markdown
            if 'text.replace(\'<b>\', \'**\')' in content:
                print("❌ HTML теги конвертируются в Markdown (НЕПРАВИЛЬНО)")
            else:
                print("✅ HTML теги НЕ конвертируются в Markdown (ПРАВИЛЬНО)")
        
        print("\n📋 Анализ метода format_text_for_telegram_markdown:")
        
        # Ищем метод format_text_for_telegram_markdown
        if 'def format_text_for_telegram_markdown(self, text: str) -> str:' in content:
            print("✅ Метод format_text_for_telegram_markdown найден")
            
            # Проверяем, что HTML теги конвертируются в Markdown
            if 'text.replace(\'<b>\', \'**\')' in content:
                print("✅ HTML теги конвертируются в Markdown (ПРАВИЛЬНО)")
            else:
                print("❌ HTML теги НЕ конвертируются в Markdown (НЕПРАВИЛЬНО)")
        
        print("\n🎯 ЗАКЛЮЧЕНИЕ:")
        print("Логика должна быть следующей:")
        print("1. Посты с изображениями: HTML форматирование + изображение в конце")
        print("2. Посты без изображений: Markdown форматирование")
        print("3. HTML теги в постах с изображениями НЕ должны конвертироваться")
        print("4. HTML теги в постах без изображений ДОЛЖНЫ конвертироваться в Markdown")
        
    except Exception as e:
        print(f"❌ Ошибка при анализе файла: {e}")

if __name__ == "__main__":
    check_telegram_client_logic()
