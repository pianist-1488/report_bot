import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from gspread.exceptions import IncorrectCellLabel

# Авторизация и создание клиента Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("info.json", scope)
client = gspread.authorize(creds)


# Получение или создание рабочего листа
def get_or_create_worksheet(sheet_name):
    try:
        sheet = client.open("SheetsTest").worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        sheet = None
    return sheet


# Создание рабочего листа из шаблона
def create_worksheet_from_template(sheet_name):
    template = client.open("SheetsTest").worksheet(
        "template table")  # Измените "template table" на название вашего листа-шаблона
    new_sheet = client.open("SheetsTest").duplicate_sheet(template.id, new_sheet_name=sheet_name)
    return new_sheet


# Определение столбцов для каждого дня месяца
column_map = {
    1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K',
    11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U',
    21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'AA', 27: 'AB', 28: 'AC', 29: 'AD', 30: 'AE', 31: 'AF'
}


# Получение текущего столбца на основе даты
def get_current_date_column():
    today = datetime.now().day
    column = column_map.get(today, None)
    print(f"Текущий столбец: {column}")
    return column


# Функция для инкремента значения в ячейке
def increment_cell(worksheet, cell):
    try:
        cell_range = f'{cell}:{cell}'
        values = worksheet.get(cell_range)
        if not values or not values[0] or values[0][0] is None:
            value = 0
        else:
            try:
                value = int(values[0][0])
            except ValueError:
                print(
                    f"Ошибка при обработке значения ячейки: {cell_range} - значение не является числом: {values[0][0]}")
                return
        new_value = value + 1
        worksheet.update(cell_range, [[new_value]])
    except IncorrectCellLabel:
        print(f"Неправильная метка ячейки: {cell}")
    except IndexError:
        print(f"Ошибка: list index out of range при обработке ячейки: {cell}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")


# Инкремент ячеек на основе списка выбранных продуктов
def increment_cells_based_on_selection(worksheet, selected_products):
    cell_map = {
        'Комбо или ККК': 'A8',
        'БС с покупкой акций': 'A9',
        'НС до 50 т.р.': 'A10',
        'НС от 50 т.р.': 'A11',
        'Реферальная программа': 'A12',
        'Цифровой профиль': 'A13',
        'КэшБэк': 'A14',
        'AlfaPay': 'A15',
        'Установка пин кода': 'A17',
        'Цифровой профиль (пин)': 'A18',  # Изменено для уникальности
        'КэшБэк (пин)': 'A19',  # Изменено для уникальности
        'AlfaPay (пин)': 'A20',  # Изменено для уникальности
        'Селфи ДК': 'A22',
        'Селфи СС': 'A23',
        'Транзакция': 'A24',
        'PPI': 'A27',
        'БС с покупкой акций (CC1)': 'A28',  # Изменено для уникальности
        'КДК к CC1': 'A29',
        'НС до 50 т.р. (CC1)': 'A30',  # Изменено для уникальности
        'НС от 50 т.р. (CC1)': 'A31',  # Изменено для уникальности
        'Реферальная программа (CC1)': 'A32',
        'Цифровой профиль (CC1)': 'A33',  # Изменено для уникальности
        'КэшБэк (CC1)': 'A34',  # Изменено для уникальности
        'AlfaPay (CC1)': 'A35',  # Изменено для уникальности
        'Транзакция (CC2)': 'A37',  # Изменено для уникальности
        'PPI (CC2)': 'A38',  # Изменено для уникальности
        'БС с покупкой акций (CC2)': 'A39',  # Изменено для уникальности
        'КДК к CC2': 'A40',
        'НС до 50 т.р. (CC2)': 'A41',  # Изменено для уникальности
        'НС от 50 т.р. (CC2)': 'A42',  # Изменено для уникальности
        'Реферальная программа (CC2)': 'A43',  # Изменено для уникальности
        'Цифровой профиль (CC2)': 'A44',  # Изменено для уникальности
        'КэшБэк (CC2)': 'A45',  # Изменено для уникальности
        'AlfaPay (CC2)': 'A46',  # Изменено для уникальности
        'ДК для Кор счета': 'A48',
        'ДК для физ.': 'A49'
    }


    date_column = get_current_date_column()

    for product in selected_products:
        if product in cell_map:
            cell = cell_map[product].replace('A', date_column)
            print(f"Попытка обновить ячейку: {cell} для продукта {product}")
            increment_cell(worksheet, cell)

    # Инкремент ячейки с текущей датой
    increment_cell(worksheet, f'{date_column}6')


# Инкремент категорий
def increment_category(worksheet, cell):
    try:
        cell_value = worksheet.acell(cell).value
        if cell_value is None:
            worksheet.update_acell(cell, 1)
        else:
            worksheet.update_acell(cell, int(cell_value) + 1)
    except Exception as e:
        print(f"Ошибка при инкременте ячейки {cell}: {str(e)}")
