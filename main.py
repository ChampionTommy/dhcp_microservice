import os
from dotenv import load_dotenv
from src.excel import ExcelProcessor
from src.parser import WebParser
from src.errors import ColorizedErrors
from src.logger import Logger

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    logger = Logger(log_path='logs/').get_logger()

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        logger.warning("Файл .env не найден.")

    file_path = os.getenv('FILE_PATH')
    sheet_name = os.getenv('SHEET_NAME')
    url = os.getenv('URL_DHCP')
    error_sheet_name = os.getenv('ERROR_SHEET_NAME', 'СПИСОК К УДАЛЕНИЮ')  # default value if not provided
    if not file_path or not sheet_name or not url:
        logger.error("Переменные окружения FILE_PATH, SHEET_NAME или URL_DHCP отсутствуют.")
        return

    try:       
        processor = ExcelProcessor(file_path, logger)
        colorized_errors = ColorizedErrors(file_path, error_sheet_name, logger)
        parser = WebParser(url, processor, colorized_errors, logger)
        parser.check_data(sheet_name)
    
    except Exception as e:
        logger.error(f"Произошла ошибка в основном процессе: {e}")

if __name__ == "__main__":
    main()

