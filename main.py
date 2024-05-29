import os
from dotenv import load_dotenv
from src.excel import ExcelProcessor
from src.parser import WebParser
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        logging.warning("Файл .env не найден.")

    file_path = os.getenv('FILE_PATH')
    sheet_name = os.getenv('SHEET_NAME')
    url = os.getenv('URL_DHCP')


    if not file_path or not sheet_name or not url:
        logging.error("Переменные окружения FILE_PATH, SHEET_NAME или URL_DHCP отсутствуют.")
        return

    try:
        processor = ExcelProcessor(file_path)
        processor.read_sheet(sheet_name)
        
        parser = WebParser(url, file_path)
        parser.check_data(sheet_name)
    except Exception as e:
        logging.error(f"Произошла ошибка в основном процессе: {e}")

if __name__ == "__main__":
    main()

