import gspread
from db.db import *
from google.oauth2.service_account import Credentials

# Авторизация с помощью сервисного аккаунта
def authenticate_google_sheets():
    creds = Credentials.from_service_account_file(
        'cred.json',  # Путь к вашему credentials.json
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    return client

def open_sheet_by_id(client, spreadsheet_id):
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.sheet1  # Открытие первого листа
    return sheet

def write_data_to_sheet(sheet, data):
    # Запись заголовков
    sheet.append_row(data[0].keys())
    
    # Запись данных из базы
    for row in data:
        sheet.append_row(row.values())

def sheets_main():
    client = authenticate_google_sheets()

    spreadsheet_id = '1NgffQSCqM7b8vS0Ls71uyCeNURgfuiz8K34zrq2ZFU8'  # Замените на реальный ID
    sheet = open_sheet_by_id(client, spreadsheet_id)

    applications = get_all_applications()

    write_data_to_sheet(sheet, applications)

