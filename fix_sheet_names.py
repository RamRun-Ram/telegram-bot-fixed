#!/usr/bin/env python3
"""
Скрипт для исправления всех использований GOOGLE_SHEET_NAME
"""
import re

def fix_sheet_names():
    """Исправляет все использования GOOGLE_SHEET_NAME в google_sheets_client.py"""
    
    with open('google_sheets_client.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем все использования GOOGLE_SHEET_NAME на self.get_sheet_name()
    # Но только в методах, где это уместно
    
    # В методе get_posts
    content = re.sub(
        r'(\s+)result = self\.service\.spreadsheets\(\)\.values\(\)\.get\(\s*spreadsheetId=GOOGLE_SHEET_ID,\s*range=f\'\{GOOGLE_SHEET_NAME\}!A:E\'\s*\)\.execute\(\)',
        r'\1# Получаем имя листа\n\1sheet_name = self.get_sheet_name()\n\1\n\1result = self.service.spreadsheets().values().get(\n\1    spreadsheetId=GOOGLE_SHEET_ID,\n\1    range=f\'{sheet_name}!A:E\'\n\1).execute()',
        content
    )
    
    # В методе get_pending_posts
    content = re.sub(
        r'(\s+)result = self\.service\.spreadsheets\(\)\.values\(\)\.get\(\s*spreadsheetId=GOOGLE_SHEET_ID,\s*range=f\'\{GOOGLE_SHEET_NAME\}!A:E\'\s*\)\.execute\(\)',
        r'\1# Получаем имя листа\n\1sheet_name = self.get_sheet_name()\n\1\n\1result = self.service.spreadsheets().values().get(\n\1    spreadsheetId=GOOGLE_SHEET_ID,\n\1    range=f\'{sheet_name}!A:E\'\n\1).execute()',
        content
    )
    
    # В методе update_post_status
    content = re.sub(
        r'(\s+)result = self\.service\.spreadsheets\(\)\.values\(\)\.update\(\s*spreadsheetId=GOOGLE_SHEET_ID,\s*range=f\'\{GOOGLE_SHEET_NAME\}!E\{row_index \+ 1\}\',',
        r'\1# Получаем имя листа\n\1sheet_name = self.get_sheet_name()\n\1\n\1result = self.service.spreadsheets().values().update(\n\1    spreadsheetId=GOOGLE_SHEET_ID,\n\1    range=f\'{sheet_name}!E{row_index + 1}\',',
        content
    )
    
    # В методе clear_sheet
    content = re.sub(
        r'(\s+)result = self\.service\.spreadsheets\(\)\.values\(\)\.clear\(\s*spreadsheetId=GOOGLE_SHEET_ID,\s*range=f\'\{GOOGLE_SHEET_NAME\}!A2:E\'\s*\)\.execute\(\)',
        r'\1# Получаем имя листа\n\1sheet_name = self.get_sheet_name()\n\1\n\1result = self.service.spreadsheets().values().clear(\n\1    spreadsheetId=GOOGLE_SHEET_ID,\n\1    range=f\'{sheet_name}!A2:E\'\n\1).execute()',
        content
    )
    
    # В методе setup_headers
    content = re.sub(
        r'(\s+)result = self\.service\.spreadsheets\(\)\.values\(\)\.update\(\s*spreadsheetId=GOOGLE_SHEET_ID,\s*range=f\'\{GOOGLE_SHEET_NAME\}!A1:E1\',',
        r'\1# Получаем имя листа\n\1sheet_name = self.get_sheet_name()\n\1\n\1result = self.service.spreadsheets().values().update(\n\1    spreadsheetId=GOOGLE_SHEET_ID,\n\1    range=f\'{sheet_name}!A1:E1\',',
        content
    )
    
    with open('google_sheets_client.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Исправления применены")

if __name__ == "__main__":
    fix_sheet_names()
