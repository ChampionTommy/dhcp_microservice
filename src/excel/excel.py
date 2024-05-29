from openpyxl import load_workbook
import logging

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = load_workbook(filename=file_path)
        logging.basicConfig(level=logging.INFO)
    
    def read_sheet(self, sheet_name):
        try:
            sheet = self.workbook[sheet_name]
            rows = list(sheet.values)
            rows.sort(key=lambda row: str(row[1]) if len(row) > 1 and row[1] is not None else str(row[0]) if row else '')
            return rows
        except KeyError:
            logging.error(f"Лист '{sheet_name}' не найден.")
            return []
        except Exception as e:
            logging.error(f"Произошла ошибка при чтении листа '{sheet_name}': {e}")
            return []


