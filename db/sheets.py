import gspread
from db.db import *
from google.oauth2.service_account import Credentials
import os

home = os.path.dirname(__file__)
CRED_PATH = os.path.join(home, 'cred.json')

# Авторизация с помощью сервисного аккаунта Google Sheets
async def authenticate_google_sheets():
    creds = Credentials.from_service_account_file(
        CRED_PATH,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    return client

# Открытие Google Sheets по URL
async def open_sheet_by_id(client, spreadsheet_url):
    spreadsheet = client.open_by_url(spreadsheet_url)
    sheet = spreadsheet.sheet1  # Открытие первого листа
    return sheet

# Асинхронная запись данных в Google Sheets
async def write_data_to_sheet(sheet, data):
    # Запись заголовков
    headers = list(data[0].keys())
    sheet.append_row(headers)
    
    # Асинхронная запись данных построчно
    for row in data:
        values = list(row.values())
        sheet.append_row(values)

# Главная функция для работы с Google Sheets
async def sheets_main(spreadsheet_url):
    client = await authenticate_google_sheets()
    sheet = await open_sheet_by_id(client, spreadsheet_url)
    
    # Получение данных из базы
    applications = await get_all_applications()  # Предполагается, что эта функция возвращает список словарей
    
    await write_data_to_sheet(sheet, applications)