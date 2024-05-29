import openpyxl
from openpyxl.styles import PatternFill
import logging

class ColorizedErrors:
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = openpyxl.load_workbook(filename=file_path)

    def mark_row(self, search_data, color):
        try:
            sheet = self.workbook["СПИСОК К УДАЛЕНИЮ"]
            fill = PatternFill(fill_type="solid", start_color=color, end_color=color)

            found = False
            for row_idx in range(1, sheet.max_row + 1):
                row_values = [cell.value for cell in sheet[row_idx][:3]]

                # Приведение типов к строкам для сравнения
                row_values_str = [str(val) for val in row_values]
                search_data_str = [str(val) for val in search_data[:3]]

                if row_values_str == search_data_str:
                    logging.info(f"Совпадение найдено в строке {row_idx}")
                    for cell in sheet[row_idx]:
                        cell.fill = fill
                    last_cell = sheet.cell(row=row_idx, column=sheet.max_column)
                    last_cell.value = "Удалено"
                    found = True
                    break

            if not found:
                logging.warning("Строка для закрашивания не найдена.")
            else:
                self.workbook.save(self.file_path)
                logging.info(f"Строка с данными {search_data_str} найдена и закрашена.")

        except KeyError:
            logging.error(f"Лист 'СПИСОК К УДАЛЕНИЮ' не найден.")
        except Exception as e:
            logging.error(f"Ошибка: {e}")

