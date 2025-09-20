#!/usr/bin/env python3
"""
Тестирование HTML валидации
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_html_validation():
    """Тестирует валидацию HTML тегов"""
    
    print("🔧 Тестирование HTML валидации...")
    
    # Симулируем метод _validate_html_tags
    def _validate_html_tags(text: str) -> str:
        """
        Валидирует и исправляет HTML теги для корректного парсинга Telegram
        """
        # Поддерживаемые теги
        supported_tags = ['b', 'i', 'u', 'strong', 'em']
        
        for tag in supported_tags:
            # Подсчитываем открывающие и закрывающие теги
            open_tags = text.count(f'<{tag}>')
            close_tags = text.count(f'</{tag}>')
            
            # Если есть незакрытые теги, закрываем их
            if open_tags > close_tags:
                missing_closes = open_tags - close_tags
                text += f'</{tag}>' * missing_closes
                print(f"⚠️  Исправлено {missing_closes} незакрытых тегов <{tag}>")
            
            # Если есть лишние закрывающие теги, удаляем их
            elif close_tags > open_tags:
                # Удаляем лишние закрывающие теги с конца
                extra_closes = close_tags - open_tags
                for _ in range(extra_closes):
                    text = text.rsplit(f'</{tag}>', 1)[0] + text.rsplit(f'</{tag}>', 1)[1]
                print(f"⚠️  Удалено {extra_closes} лишних закрывающих тегов </{tag}>")
        
        return text
    
    # Тестовые случаи
    test_cases = [
        {
            "name": "Корректные теги",
            "text": "<b>Жирный</b> <i>Курсив</i> <u>Подчеркнутый</u>",
            "expected": "Все теги должны остаться"
        },
        {
            "name": "Незакрытый тег <b>",
            "text": "<b>Жирный текст без закрытия",
            "expected": "Должен добавиться </b>"
        },
        {
            "name": "Незакрытый тег <i>",
            "text": "<i>Курсивный текст",
            "expected": "Должен добавиться </i>"
        },
        {
            "name": "Множественные незакрытые теги",
            "text": "<b>Жирный <i>Курсив <u>Подчеркнутый",
            "expected": "Должны добавиться все закрывающие теги"
        },
        {
            "name": "Лишние закрывающие теги",
            "text": "<b>Жирный</b></b></b>",
            "expected": "Должны удалиться лишние </b>"
        },
        {
            "name": "Смешанный случай",
            "text": "<b>Жирный <i>Курсив</b> <u>Подчеркнутый</u></u>",
            "expected": "Должны исправиться все проблемы"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Тест {i}: {test_case['name']}")
        print(f"Исходный текст: {test_case['text']}")
        
        # Валидируем
        result = _validate_html_tags(test_case['text'])
        
        print(f"Результат: {result}")
        print(f"Ожидание: {test_case['expected']}")
        
        # Проверяем, что все теги сбалансированы
        balanced = True
        for tag in ['b', 'i', 'u', 'strong', 'em']:
            open_count = result.count(f'<{tag}>')
            close_count = result.count(f'</{tag}>')
            if open_count != close_count:
                balanced = False
                print(f"❌ Тег <{tag}> не сбалансирован: {open_count} открывающих, {close_count} закрывающих")
        
        if balanced:
            print("✅ Все теги сбалансированы")
        else:
            print("❌ Есть несбалансированные теги")

def test_full_processing():
    """Тестирует полную обработку текста"""
    
    print("\n🔧 Тестирование полной обработки текста...")
    
    def _process_text_for_image_posts(text: str) -> str:
        """
        Обрабатывает текст для постов с изображениями (HTML формат)
        Валидирует и исправляет HTML теги для корректного отображения
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
        
        # ВАЖНО: Валидируем и исправляем HTML теги
        text = _validate_html_tags(text)
        
        return text
    
    def _validate_html_tags(text: str) -> str:
        """
        Валидирует и исправляет HTML теги для корректного парсинга Telegram
        """
        # Поддерживаемые теги
        supported_tags = ['b', 'i', 'u', 'strong', 'em']
        
        for tag in supported_tags:
            # Подсчитываем открывающие и закрывающие теги
            open_tags = text.count(f'<{tag}>')
            close_tags = text.count(f'</{tag}>')
            
            # Если есть незакрытые теги, закрываем их
            if open_tags > close_tags:
                missing_closes = open_tags - close_tags
                text += f'</{tag}>' * missing_closes
                print(f"⚠️  Исправлено {missing_closes} незакрытых тегов <{tag}>")
            
            # Если есть лишние закрывающие теги, удаляем их
            elif close_tags > open_tags:
                # Удаляем лишние закрывающие теги с конца
                extra_closes = close_tags - open_tags
                for _ in range(extra_closes):
                    text = text.rsplit(f'</{tag}>', 1)[0] + text.rsplit(f'</{tag}>', 1)[1]
                print(f"⚠️  Удалено {extra_closes} лишних закрывающих тегов </{tag}>")
        
        return text
    
    # Тестовый текст с проблемными HTML тегами
    problematic_text = """
<b>Жирный текст</b>
<i>Курсивный текст без закрытия
<u>Подчеркнутый текст</u>
<div>Div тег</div>
<p>Параграф</p>
<ul>
<li>Элемент списка 1</li>
<li>Элемент списка 2</li>
</ul>
    """.strip()
    
    print("📝 Исходный текст:")
    print(problematic_text)
    
    # Обрабатываем
    processed_text = _process_text_for_image_posts(problematic_text)
    
    print("\n📝 Обработанный текст:")
    print(processed_text)
    
    # Проверяем результат
    print("\n🎯 Проверка результата:")
    print(f"Длина: {len(processed_text)} символов")
    
    # Проверяем, что все теги сбалансированы
    balanced = True
    for tag in ['b', 'i', 'u', 'strong', 'em']:
        open_count = processed_text.count(f'<{tag}>')
        close_count = processed_text.count(f'</{tag}>')
        if open_count != close_count:
            balanced = False
            print(f"❌ Тег <{tag}> не сбалансирован: {open_count} открывающих, {close_count} закрывающих")
        else:
            print(f"✅ Тег <{tag}> сбалансирован: {open_count} пар")
    
    if balanced:
        print("✅ Все HTML теги корректны!")
    else:
        print("❌ Есть проблемы с HTML тегами")

if __name__ == "__main__":
    test_html_validation()
    test_full_processing()
    
    print("\n🎯 ЗАКЛЮЧЕНИЕ:")
    print("HTML валидация должна исправить проблему с незакрытыми тегами")
    print("Это должно решить ошибку 'Can't find end tag corresponding to start tag'")
