import os
from dotenv import load_dotenv
from src.excel import ExcelProcessor
from src.parser import WebParser

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    file_path = os.getenv('FILE_PATH')
    sheet_name = os.getenv('SHEET_NAME')
    url = os.getenv('URL_DHCP')

    processor = ExcelProcessor(file_path)
    rows = processor.read_sheet(sheet_name)

    parser = WebParser(url, file_path)
    parser.check_and_delete(sheet_name)

if __name__ == "__main__":
    main()
