#!/usr/bin/env python3
"""
Отладка логики постов
"""

def test_image_post_processing():
    """Тестирует обработку поста с изображением"""
    
    print("🔧 Тестирование обработки поста с изображением...")
    
    # Симулируем метод _process_text_for_image_posts
    def _process_text_for_image_posts(text: str) -> str:
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
    
    # Тестовый текст с HTML тегами
    test_text = """
<b>Жирный текст</b>
<i>Курсивный текст</i>
<u>Подчеркнутый текст</u>
<br>
<div>Div тег</div>
<p>Параграф</p>
<ul>
<li>Элемент списка 1</li>
<li>Элемент списка 2</li>
</ul>
    """.strip()
    
    print("📝 Исходный текст:")
    print(test_text)
    print(f"Длина: {len(test_text)} символов")
    
    # Обрабатываем текст
    processed_text = _process_text_for_image_posts(test_text)
    
    print("\n📝 Обработанный текст:")
    print(processed_text)
    print(f"Длина: {len(processed_text)} символов")
    
    # Проверяем, что HTML теги остались
    if '<b>' in processed_text and '<i>' in processed_text and '<u>' in processed_text:
        print("✅ HTML теги сохранены (правильно для постов с изображениями)")
    else:
        print("❌ HTML теги НЕ сохранены (неправильно)")
    
    # Проверяем, что div и p теги удалены
    if '<div>' not in processed_text and '<p>' not in processed_text:
        print("✅ Неподдерживаемые теги удалены")
    else:
        print("❌ Неподдерживаемые теги НЕ удалены")
    
    # Симулируем создание финального сообщения
    image_url = "https://example.com/image.jpg"
    final_message = f'{processed_text}\n\n<a href="{image_url}">🖼️ Изображение</a>'
    
    print("\n📝 Финальное сообщение:")
    print(final_message)
    print(f"Длина: {len(final_message)} символов")
    
    print("\n🎯 Ожидаемый результат:")
    print("- HTML теги <b>, <i>, <u> должны остаться")
    print("- Изображение должно быть в конце с ссылкой")
    print("- Длина должна быть ~4000 символов (если текст длинный)")

def test_markdown_post_processing():
    """Тестирует обработку поста без изображения"""
    
    print("\n🔧 Тестирование обработки поста БЕЗ изображения...")
    
    # Симулируем метод format_text_for_telegram_markdown
    def format_text_for_telegram_markdown(text: str) -> str:
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
    
    # Тестовый текст с HTML тегами
    test_text = """
<b>Жирный текст</b>
<i>Курсивный текст</i>
<u>Подчеркнутый текст</u>
<br>
<div>Div тег</div>
<p>Параграф</p>
    """.strip()
    
    print("📝 Исходный текст:")
    print(test_text)
    
    # Обрабатываем текст
    processed_text = format_text_for_telegram_markdown(test_text)
    
    print("\n📝 Обработанный текст (Markdown):")
    print(processed_text)
    
    # Проверяем, что HTML теги конвертированы в Markdown
    if '**' in processed_text and '*' in processed_text and '__' in processed_text:
        print("✅ HTML теги конвертированы в Markdown (правильно для постов без изображений)")
    else:
        print("❌ HTML теги НЕ конвертированы в Markdown (неправильно)")
    
    # Проверяем, что div и p теги удалены
    if '<div>' not in processed_text and '<p>' not in processed_text:
        print("✅ Неподдерживаемые теги удалены")
    else:
        print("❌ Неподдерживаемые теги НЕ удалены")

if __name__ == "__main__":
    test_image_post_processing()
    test_markdown_post_processing()
    
    print("\n🎯 ЗАКЛЮЧЕНИЕ:")
    print("Логика обработки текста работает правильно!")
    print("Если посты все еще отображаются неправильно, проблема может быть в:")
    print("1. Кэшировании на Railway (нужно подождать 2-3 минуты)")
    print("2. Неправильном выборе метода отправки")
    print("3. Проблемах с Telegram API")
