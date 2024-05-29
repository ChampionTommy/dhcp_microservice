import requests
import pandas as pd
from bs4 import BeautifulSoup
from src.excel import ExcelProcessor
from src.errors import ColorizedErrors
import logging

class WebParser:
    def __init__(self, url, file_path):
        self.url = url
        self.excel_processor = ExcelProcessor(file_path)
        self.colorized_errors = ColorizedErrors(file_path)
        logging.basicConfig(level=logging.INFO)
     
    def get_web_table_rows(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if not table:
                logging.warning("Таблица не найдена на веб-странице.")
                return []
            
            tbody = table.find('tbody')
            if not tbody:
                logging.warning("Тело таблицы не найдено на веб-странице.")
                return []
            
            return tbody.find_all('tr')
        
        except requests.RequestException as e:
            logging.error(f"Ошибка запроса: {e}")
            return []   
    
    def compare_rows(self, excel_row, web_row):
        excel_data = excel_row[:3]
        
        web_data = [td.text.strip() for td in web_row.find_all('td')[:3]]
        if len(web_data) < 3:
            return False
        
        excel_data = [int(val) if isinstance(val, (int, float)) and not pd.isna(val) else val for val in excel_data]
        web_data = [int(val) if val.isdigit() else val for val in web_data]
        
        return excel_data == web_data   
    
    def check_data(self, sheet_name):
        try:
            rows = self.excel_processor.read_sheet(sheet_name)
            if not rows:
                logging.error(f"Не удалось прочитать данные из листа '{sheet_name}'.")
                return
            
            web_rows = self.get_web_table_rows(self.url)
            if not web_rows:
                logging.warning("Нет строк для сравнения на веб-странице.")
                return
            
            rows_to_mark = []
            for i, row in enumerate(rows, start=3):
                for web_row in web_rows:
                    if self.compare_rows(row, web_row):
                        rows_to_mark.append(i)
                        logging.info(f"Совпадение найдено и будет удалено: {row[:13]}")
                        self.delete_row(row)
                        break
            else:
                logging.info("Совпадений не найдено.")
            
        except Exception as e:
            logging.error(f"Произошла ошибка при проверке данных: {e}")

    def delete_row(self, row):
        try:
            response = requests.post(f'{self.url}/delete.php', data={'value': row[0], 'delete': 'Delete'})
            response.raise_for_status()
            logging.info(f'Строка c лицевым счетом {row[0]} удалена')
            self.colorized_errors.mark_row(row, 'ccffcc')  # Передаём строку и цвет
        except requests.RequestException as e:
            logging.error(f"Ошибка при удалении данных: {e}")

