"""
Клиент для работы с Google Sheets API
"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME, STATUS_PUBLISHED, STATUS_PENDING

logger = logging.getLogger(__name__)

class GoogleSheetsClient:
    """Клиент для работы с Google Sheets API"""
    
    def __init__(self):
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self._authenticate()
    
    def _authenticate(self):
        """Аутентификация в Google Sheets API через Service Account"""
        try:
            # Получаем Service Account credentials из переменных окружения
            service_account_info = {
                "type": "service_account",
                "project_id": os.getenv("GOOGLE_PROJECT_ID", "YOUR_GOOGLE_PROJECT_ID"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID", "YOUR_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "YOUR_PRIVATE_KEY").replace('\\n', '\n'),
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL", "YOUR_CLIENT_EMAIL"),
                "client_id": os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL", "YOUR_CLIENT_X509_CERT_URL")
            }
            
            # Создаем credentials из Service Account
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.SCOPES
            )
            
            # Создаем сервис
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets API инициализирован успешно через Service Account")
            
        except Exception as e:
            logger.error(f"Ошибка Service Account аутентификации: {e}")
            logger.warning("Google Sheets API не инициализирован - система будет работать без него")
            self.service = None
    
    def add_post(self, post_data: Dict[str, Any]) -> bool:
        """Добавляет пост в Google Sheets"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, пропускаем добавление поста")
            return True
            
        try:
            # Подготавливаем данные для записи
            values = [
                [
                    post_data.get('date', ''),
                    post_data.get('time', ''),
                    post_data.get('text', ''),
                    post_data.get('image_urls', ''),
                    STATUS_PUBLISHED
                ]
            ]
            
            # Добавляем строку в конец таблицы
            body = {'values': values}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{GOOGLE_SHEET_NAME}!A:E',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Пост добавлен в Google Sheets: {result.get('updates', {}).get('updatedRows', 0)} строк")
            return True
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка добавления поста: {e}")
            return False
    
    def get_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получает последние посты из Google Sheets"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, возвращаем пустой список")
            return []
            
        try:
            # Получаем данные из таблицы
            result = self.service.spreadsheets().values().get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{GOOGLE_SHEET_NAME}!A:E'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.info("Таблица пуста")
                return []
            
            # Пропускаем заголовок и берем последние записи
            posts = []
            for row in values[1:][-limit:]:
                if len(row) >= 5:
                    posts.append({
                        'date': row[0] if len(row) > 0 else '',
                        'time': row[1] if len(row) > 1 else '',
                        'text': row[2] if len(row) > 2 else '',
                        'image_urls': row[3] if len(row) > 3 else '',
                        'status': row[4] if len(row) > 4 else ''
                    })
            
            logger.info(f"Получено {len(posts)} постов из Google Sheets")
            return posts
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return []
        except Exception as e:
            logger.error(f"Ошибка получения постов: {e}")
            return []
    
    def get_pending_posts(self) -> List[Dict[str, Any]]:
        """Получает посты со статусом 'Ожидает' для публикации"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, возвращаем пустой список")
            return []
            
        try:
            # Получаем данные из таблицы
            result = self.service.spreadsheets().values().get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{GOOGLE_SHEET_NAME}!A:E'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.info("Таблица пуста")
                return []
            
            # Пропускаем заголовок и ищем посты со статусом "Ожидает"
            pending_posts = []
            for i, row in enumerate(values[1:], start=2):  # start=2 потому что пропускаем заголовок
                if len(row) >= 5:
                    status = row[4] if len(row) > 4 else ''
                    if status == STATUS_PENDING:
                        # Парсим image_urls если они есть
                        image_urls = []
                        if len(row) > 3 and row[3]:
                            try:
                                # Предполагаем, что URLs разделены запятыми
                                image_urls = [url.strip() for url in row[3].split(',') if url.strip()]
                            except Exception as e:
                                logger.warning(f"Ошибка парсинга image_urls: {e}")
                                image_urls = []
                        
                        pending_posts.append({
                            'row_index': i - 1,  # Индекс строки в таблице (0-based)
                            'date': row[0] if len(row) > 0 else '',
                            'time': row[1] if len(row) > 1 else '',
                            'text': row[2] if len(row) > 2 else '',
                            'image_urls': image_urls,
                            'status': status
                        })
            
            logger.info(f"Найдено {len(pending_posts)} постов со статусом 'Ожидает'")
            return pending_posts
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return []
        except Exception as e:
            logger.error(f"Ошибка получения постов для публикации: {e}")
            return []
    
    def update_post_status(self, row_index: int, status: str) -> bool:
        """Обновляет статус поста в Google Sheets"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, пропускаем обновление")
            return True
            
        try:
            # Обновляем статус в колонке E (индекс 4)
            values = [[status]]
            body = {'values': values}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{GOOGLE_SHEET_NAME}!E{row_index + 1}',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Статус поста обновлен: {result.get('updatedCells', 0)} ячеек")
            return True
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка обновления статуса: {e}")
            return False
    
    def clear_sheet(self) -> bool:
        """Очищает таблицу (оставляет только заголовки)"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, пропускаем очистку")
            return True
            
        try:
            # Очищаем все данные кроме заголовка
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{GOOGLE_SHEET_NAME}!A2:E'
            ).execute()
            
            logger.info("Таблица очищена")
            return True
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка очистки таблицы: {e}")
            return False
    
    def setup_headers(self) -> bool:
        """Настраивает заголовки таблицы"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, пропускаем настройку заголовков")
            return True
            
        try:
            # Добавляем заголовки
            headers = [['Дата', 'Время', 'Текст', 'Изображения', 'Статус']]
            body = {'values': headers}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{GOOGLE_SHEET_NAME}!A1:E1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info("Заголовки таблицы настроены")
            return True
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка настройки заголовков: {e}")
            return False