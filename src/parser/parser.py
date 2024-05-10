import requests
import subprocess
import pandas as pd
from bs4 import BeautifulSoup
from src.excel import ExcelProcessor

class WebParser:
    def __init__(self, url, file_path):
        self.url = url
        self.excel_processor = ExcelProcessor(file_path)

    def check_and_delete(self, sheet_name):
        rows = self.excel_processor.read_sheet(sheet_name)
        if rows is None:
            print(f"Не удалось прочитать данные из листа '{sheet_name}'.")
            return

        web_rows = self.get_web_table_rows(self.url)
        found_match = False
        for row in rows:
            for web_row in web_rows:
                if self.compare_rows(row, web_row):
                    self.delete_row(row)
                    found_match = True
                    print(f"Совпадение найдено и удалено: {row}")
                    break  # Останавливаем внутренний цикл после нахождения соответствия
            if found_match:
                break  # Останавливаем внешний цикл после нахождения соответствия

        if not found_match:
            print("Совпадений не найдено.")
    
    def get_web_table_rows(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')[1:]  # Исключаем первую строку с заголовками
        return rows
    
    def compare_rows(self, excel_row, web_row):
        # Пример сравнения первых трех полей с учетом типов данных
        excel_data = excel_row[:3]

        web_data = [td.text.strip() for td in web_row.find_all('td')[:3]]  # Удаляем лишние пробелы
        
        # Проверяем на NaN и преобразуем числа, если это необходимо
        excel_data = [int(val) if not pd.isna(val) and isinstance(val, (int, float)) else val for val in excel_data]
        web_data = [int(val) if val.isdigit() else val for val in web_data]

        # Сравниваем данные после преобразования
        return excel_data == web_data

    
    def delete_row(self, row):
        # Здесь предполагается, что первый столбец в строке - это значение, которое нужно удалить
        value_to_delete = row[0]

        # Формируем команду для curl с выводом статуса ответа и телом ответа
        curl_command = [
            'curl',
            '-i',  # Включаем заголовки ответа
            '-X', 'POST',
            '-d', f'value={value_to_delete}&delete=Delete',
            'http://localhost/delete.php'
        ]

        # Выполняем команду и получаем статус ответа
        response = subprocess.run(curl_command, capture_output=True, text=True)

        # Проверяем статус ответа и тело ответа
        if response.returncode == 0:
            # Извлекаем статус ответа из заголовков
            status_line = response.stdout.split('\n')[0]
            status_code = status_line.split(' ')[1]

            # Проверяем статус ответа
            if status_code == '200':
                print('Данные успешно удалены')
            else:
                print('Ошибка при удалении данных')
                print(f'Код ответа: {status_code}')
        else:
            print('Ошибка при выполнении запроса')
            print(response.stderr)

