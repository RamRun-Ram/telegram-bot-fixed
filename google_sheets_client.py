"""
Клиент для работы с Google Sheets API
"""
import os
import logging
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from config import GOOGLE_SHEET_ID, GOOGLE_SHEET_NAME, STATUS_PUBLISHED, STATUS_PENDING

logger = logging.getLogger(__name__)

class GoogleSheetsClient:
    """Клиент для работы с Google Sheets API"""
    
    def __init__(self):
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self._authenticate()
        
        # Кэш для имени листа
        self._sheet_name = None
    
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
        
        # Кэш для имени листа
        self._sheet_name = None
    
    def get_sheet_name(self) -> str:
        """Получает имя первого доступного листа"""
        if not self.service:
            return GOOGLE_SHEET_NAME
        
        if self._sheet_name:
            return self._sheet_name
        
        try:
            # Получаем информацию о таблице
            result = self.service.spreadsheets().get(spreadsheetId=GOOGLE_SHEET_ID).execute()
            sheets = result.get('sheets', [])
            
            if sheets:
                # Берем первый лист
                first_sheet = sheets[0].get('properties', {}).get('title', GOOGLE_SHEET_NAME)
                self._sheet_name = first_sheet
                logger.info(f"📋 Используем лист: '{first_sheet}'")
                return first_sheet
            else:
                logger.warning("⚠️ В таблице нет листов, используем значение по умолчанию")
                return GOOGLE_SHEET_NAME
                
        except Exception as e:
            logger.error(f"❌ Ошибка получения имени листа: {e}")
            logger.info(f"📋 Используем значение по умолчанию: '{GOOGLE_SHEET_NAME}'")
            return GOOGLE_SHEET_NAME
    
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
                    STATUS_PUBLISHED,
                    post_data.get('prompt_ru', ''),
                    post_data.get('prompt_en', '')
                ]
            ]
            
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Добавляем строку в конец таблицы
            body = {'values': values}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A:G',
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
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Получаем данные из таблицы
            result = self.service.spreadsheets().values().get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A:G'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.info("Таблица пуста")
                return []
            
            # Пропускаем заголовок, берем последние записи
            posts = []
            for row in values[1:][-limit:]:  # Пропускаем заголовок, берем последние limit записей
                if len(row) >= 5:  # Проверяем, что строка содержит основные колонки
                    post = {
                        'date': row[0] if len(row) > 0 else '',
                        'time': row[1] if len(row) > 1 else '',
                        'text': row[2] if len(row) > 2 else '',
                        'image_urls': row[3] if len(row) > 3 else '',
                        'status': row[4] if len(row) > 4 else '',
                        'prompt_ru': row[5] if len(row) > 5 else '',
                        'prompt_en': row[6] if len(row) > 6 else ''
                    }
                    posts.append(post)
            
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
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Получаем данные из таблицы
            result = self.service.spreadsheets().values().get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A:G'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.info("Таблица пуста")
                return []
            
            # Фильтруем посты со статусом "Ожидает"
            pending_posts = []
            for i, row in enumerate(values[1:], start=2):  # Пропускаем заголовок, начинаем с строки 2
                if len(row) >= 5 and row[4] == STATUS_PENDING:  # Проверяем статус в колонке E
                    # Парсим URL изображений
                    image_urls = []
                    if len(row) > 3 and row[3]:  # Если есть URL изображений
                        image_urls = [url.strip() for url in row[3].split(',') if url.strip()]
                    
                    post = {
                        'date': row[0] if len(row) > 0 else '',
                        'time': row[1] if len(row) > 1 else '',
                        'text': row[2] if len(row) > 2 else '',
                        'image_urls': image_urls,
                        'status': row[4] if len(row) > 4 else '',
                        'prompt_ru': row[5] if len(row) > 5 else '',
                        'prompt_en': row[6] if len(row) > 6 else '',
                        'row_index': i  # Добавляем индекс строки для обновления статуса
                    }
                    pending_posts.append(post)
            
            logger.info(f"Найдено {len(pending_posts)} постов для публикации")
            return pending_posts
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return []
        except Exception as e:
            logger.error(f"Ошибка получения постов для публикации: {e}")
            return []
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Получает все посты из Google Sheets"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, возвращаем пустой список")
            return []
            
        try:
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Получаем данные из таблицы
            result = self.service.spreadsheets().values().get(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A:G'
            ).execute()
            
            values = result.get('values', [])
            if not values:
                logger.info("Таблица пуста")
                return []
            
            # Обрабатываем все посты
            posts = []
            for i, row in enumerate(values[1:], start=2):  # Пропускаем заголовок
                if len(row) >= 5:  # Проверяем, что строка содержит основные колонки
                    # Парсим URL изображений
                    image_urls = []
                    if len(row) > 3 and row[3]:  # Если есть URL изображений
                        image_urls = [url.strip() for url in row[3].split(',') if url.strip()]
                    
                    post = {
                        'date': row[0] if len(row) > 0 else '',
                        'time': row[1] if len(row) > 1 else '',
                        'text': row[2] if len(row) > 2 else '',
                        'image_urls': image_urls,
                        'status': row[4] if len(row) > 4 else '',
                        'prompt_ru': row[5] if len(row) > 5 else '',
                        'prompt_en': row[6] if len(row) > 6 else '',
                        'row_index': i  # Добавляем индекс строки для обновления статуса
                    }
                    posts.append(post)
            
            logger.info(f"Получено {len(posts)} постов из Google Sheets")
            return posts
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return []
        except Exception as e:
            logger.error(f"Ошибка получения всех постов: {e}")
            return []
    
    def update_post_status(self, row_index: int, status: str) -> bool:
        """Обновляет статус поста в Google Sheets"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, пропускаем обновление")
            return True
            
        try:
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Обновляем статус в колонке E
            result = self.service.spreadsheets().values().update(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!E{row_index}',
                valueInputOption='RAW',
                body={'values': [[status]]}
            ).execute()
            
            logger.info(f"Статус поста в строке {row_index} обновлен на '{status}'")
            return True
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка обновления статуса поста: {e}")
            return False
    
    def clear_sheet(self) -> bool:
        """Очищает таблицу (удаляет все данные кроме заголовков)"""
        if not self.service:
            logger.warning("Google Sheets API не инициализирован, пропускаем очистку")
            return True
            
        try:
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Очищаем данные (оставляем заголовки)
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A2:G'
            ).execute()
            
            logger.info("Таблица очищена (заголовки сохранены)")
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
            # Получаем имя листа
            sheet_name = self.get_sheet_name()
            
            # Устанавливаем заголовки
            headers = [['Date', 'Time', 'Text', 'Image URLs', 'Status', 'Промпт RU', 'Промпт EN']]
            result = self.service.spreadsheets().values().update(
                spreadsheetId=GOOGLE_SHEET_ID,
                range=f'{sheet_name}!A1:G1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            logger.info("Заголовки таблицы настроены")
            return True
            
        except HttpError as e:
            logger.error(f"Ошибка Google Sheets API: {e}")
            return False
        except Exception as e:
            logger.error(f"Ошибка настройки заголовков: {e}")
            return False
