#!/usr/bin/env python3
"""
Тест OpenRouter API для диагностики проблем
"""
import asyncio
import aiohttp
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_openrouter_api():
    """Тестирует OpenRouter API с разными моделями"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("❌ OPENROUTER_API_KEY не найден в переменных окружения")
        return
    
    logger.info(f"🔑 Тестируем API ключ: {api_key[:10]}...")
    logger.info(f"🔑 Длина ключа: {len(api_key)} символов")
    
    # Список моделей для тестирования
    models_to_test = [
        "google/gemini-2.5-flash-lite-preview-06-17",
        "google/gemini-pro",
        "anthropic/claude-3.5-sonnet",
        "anthropic/claude-3.7-sonnet", 
        "meta-llama/llama-3.1-8b-instruct",
        "openai/gpt-3.5-turbo"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    for model in models_to_test:
        logger.info(f"🤖 Тестируем модель: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Привет! Это тест."}
            ],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    logger.info(f"📊 Статус ответа: {response.status}")
                    
                    if response.status == 200:
                        result = await response.json()
                        content = result["choices"][0]["message"]["content"]
                        logger.info(f"✅ Модель {model} работает! Ответ: {content}")
                        return model  # Возвращаем первую рабочую модель
                    elif response.status == 401:
                        logger.error(f"❌ Модель {model}: Ошибка аутентификации (401)")
                    elif response.status == 400:
                        error_text = await response.text()
                        logger.warning(f"⚠️ Модель {model}: Недоступна (400) - {error_text}")
                    elif response.status == 429:
                        logger.warning(f"⚠️ Модель {model}: Лимит запросов (429)")
                    else:
                        error_text = await response.text()
                        logger.warning(f"⚠️ Модель {model}: Ошибка {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"❌ Ошибка при тестировании модели {model}: {e}")
    
    logger.error("❌ Ни одна модель не работает")
    return None

if __name__ == "__main__":
    asyncio.run(test_openrouter_api())
