import pandas as pd

class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_sheet(self, sheet_name):
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            df = df[df.iloc[:, 13].isnull()]  # Фильтруем строки, где в 14-ом столбце (индекс 13) значение None
            df = df.sort_values(by=df.columns[1])  # Сортируем по второму столбцу (индекс 1)
            return df.values.tolist()  # Возвращаем список строк
        except FileNotFoundError:
            print(f"Файл '{self.file_path}' не найден.")
            return []
        except ValueError:
            print(f"Лист '{sheet_name}' не найден.")
            return []

    def delete_row(self, sheet_name, index):
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            df = df.drop(index)  # Удаляем строку по индексу
            df.to_excel(self.file_path, sheet_name=sheet_name, index=False)  # Записываем обратно в Excel файл
            print(f"Строка с индексом {index} успешно удалена из листа '{sheet_name}'.")
        except FileNotFoundError:
            print(f"Файл '{self.file_path}' не найден.")
        except ValueError:
            print(f"Лист '{sheet_name}' не найден.")
        
