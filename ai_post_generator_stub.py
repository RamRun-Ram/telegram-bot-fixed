#!/usr/bin/env python3
"""
Заглушка для генерации постов без OpenRouter API
Используется когда API ключ заблокирован
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from google_sheets_client import GoogleSheetsClient

logger = logging.getLogger(__name__)

class AIPostGeneratorStub:
    """Заглушка для генерации постов без AI"""
    
    def __init__(self):
        self.sheets_client = GoogleSheetsClient()
        logger.info("🤖 AIPostGeneratorStub инициализирован (без AI)")
    
    async def generate_weekly_posts(self) -> List[Dict[str, Any]]:
        """Генерирует тестовые посты на 3 дня"""
        logger.info("🎯 Генерация тестовых постов (заглушка)")
        
        posts = []
        start_date = datetime.now()
        
        # Предустановленные посты для тестирования
        sample_posts = [
            {
                "text": "💕 Любовь - это не поиск идеального человека, а создание идеальных отношений с неидеальным человеком.",
                "image_urls": ["https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=500"],
                "category": "ЦитатаОтношений"
            },
            {
                "text": "🌟 В настоящих отношениях нет места для эгоизма. Любовь - это отдавать, а не брать.",
                "image_urls": ["https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=500"],
                "category": "МыслиВслух"
            },
            {
                "text": "💝 Семья - это не только кровные узы, но и узы сердца, которые связывают нас навсегда.",
                "image_urls": ["https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=500"],
                "category": "Совпало"
            },
            {
                "text": "🤝 Понимание - это мост между двумя сердцами, который позволяет им говорить на одном языке.",
                "image_urls": ["https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=500"],
                "category": "Человечность"
            },
            {
                "text": "💖 Истинная любовь не ищет совершенства, а принимает несовершенство и делает его прекрасным.",
                "image_urls": ["https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=500"],
                "category": "ЦитатаОтношений"
            },
            {
                "text": "🌱 Отношения - это сад, который нужно поливать каждый день вниманием, заботой и пониманием.",
                "image_urls": ["https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=500"],
                "category": "МыслиВслух"
            },
            {
                "text": "💕 В любви нет места для страха. Любовь - это смелость быть собой и принимать другого.",
                "image_urls": ["https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=500"],
                "category": "Совпало"
            },
            {
                "text": "🌟 Счастье в отношениях - это не отсутствие проблем, а умение решать их вместе.",
                "image_urls": ["https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=500"],
                "category": "Человечность"
            },
            {
                "text": "💝 Любовь - это не то, что мы получаем, а то, что мы отдаем. Чем больше отдаем, тем больше получаем.",
                "image_urls": ["https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=500"],
                "category": "ЦитатаОтношений"
            }
        ]
        
        for i, post_data in enumerate(sample_posts):
            # Добавляем дату к посту
            post_date = start_date + timedelta(days=i//3, hours=(i%3)*8)
            
            post = {
                "text": post_data["text"],
                "image_urls": post_data["image_urls"],
                "category": post_data["category"],
                "scheduled_time": post_date.strftime("%Y-%m-%d %H:%M"),
                "status": "Ожидает"
            }
            
            posts.append(post)
            logger.info(f"📝 Создан пост {i+1}/9: {post['text'][:50]}...")
        
        logger.info(f"✅ Сгенерировано {len(posts)} тестовых постов")
        return posts
    
    async def generate_and_upload_weekly_posts(self) -> bool:
        """Генерирует и загружает посты в Google Sheets"""
        try:
            logger.info("🚀 Начинаем генерацию и загрузку постов (заглушка)")
            
            # Инициализируем заголовки таблицы
            await self.initialize_sheet_headers()
            
            # Генерируем посты
            posts = await self.generate_weekly_posts()
            
            if not posts:
                logger.error("❌ Не удалось сгенерировать посты")
                return False
            
            # Загружаем посты в Google Sheets
            await self.upload_posts_to_sheets(posts)
            
            logger.info("✅ Посты успешно сгенерированы и загружены (заглушка)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации постов (заглушка): {e}")
            return False
    
    async def initialize_sheet_headers(self):
        """Инициализирует заголовки таблицы"""
        logger.info("📋 Инициализируем заголовки таблицы (заглушка)")
        self.sheets_client.setup_headers()
        logger.info("✅ Заголовки таблицы инициализированы (заглушка)")
    
    async def upload_posts_to_sheets(self, posts: List[Dict[str, Any]]):
        """Загружает посты в Google Sheets"""
        logger.info(f"📤 Загружаем {len(posts)} постов в Google Sheets (заглушка)")
        
        for i, post in enumerate(posts):
            try:
                # Форматируем данные поста для Google Sheets
                post_data = {
                    "text": post["text"],
                    "image_urls": ", ".join(post["image_urls"]) if post["image_urls"] else "",
                    "category": post["category"],
                    "scheduled_time": post["scheduled_time"],
                    "status": post["status"]
                }
                
                # Добавляем пост в таблицу
                self.sheets_client.add_post(post_data)
                logger.info(f"✅ Пост {i+1}/{len(posts)} загружен в таблицу")
                
            except Exception as e:
                logger.error(f"❌ Ошибка при загрузке поста {i+1}: {e}")
        
        logger.info("✅ Все посты загружены в Google Sheets (заглушка)")
