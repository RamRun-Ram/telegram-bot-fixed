"""
Упрощенный клиент для работы с Google Sheets API (без аутентификации для тестирования)
"""
import logging
from typing import List, Dict, Any, Optional
from config import STATUS_PUBLISHED

logger = logging.getLogger(__name__)

class GoogleSheetsClient:
    """Упрощенный клиент для работы с Google Sheets API"""
    
    def __init__(self):
        self.service = None
        logger.info("Google Sheets API отключен для тестирования")
    
    def add_post(self, post_data: Dict[str, Any]) -> bool:
        """Добавляет пост в Google Sheets (заглушка)"""
        logger.info(f"ЗАГЛУШКА: Пост добавлен в Google Sheets: {post_data.get('text', '')[:50]}...")
        return True
    
    def get_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получает последние посты из Google Sheets (заглушка)"""
        logger.info(f"ЗАГЛУШКА: Получено {limit} постов из Google Sheets")
        return []
    
    def update_post_status(self, row_index: int, status: str) -> bool:
        """Обновляет статус поста в Google Sheets (заглушка)"""
        logger.info(f"ЗАГЛУШКА: Статус поста {row_index} обновлен на {status}")
        return True
    
    def clear_sheet(self) -> bool:
        """Очищает таблицу (заглушка)"""
        logger.info("ЗАГЛУШКА: Таблица очищена")
        return True
    
    def setup_headers(self) -> bool:
        """Настраивает заголовки таблицы (заглушка)"""
        logger.info("ЗАГЛУШКА: Заголовки таблицы настроены")
        return True
