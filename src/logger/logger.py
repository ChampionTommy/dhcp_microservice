
import logging
import os

class Logger:
    def __init__(self, log_path='logs/'):
        # Создание директории для логов, если ее нет
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        
        # Настройка основного логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # Установите уровень логирования на DEBUG, чтобы все сообщения попадали в основной лог
        
        # Создание и добавление форматтера
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Обработчик для INFO уровня
        info_handler = logging.FileHandler(os.path.join(log_path, 'info.log'))
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        self.logger.addHandler(info_handler)
        
        # Обработчик для WARNING уровня
        warning_handler = logging.FileHandler(os.path.join(log_path, 'warning.log'))
        warning_handler.setLevel(logging.WARNING)
        warning_handler.setFormatter(formatter)
        self.logger.addHandler(warning_handler)
        
        # Обработчик для ERROR уровня
        error_handler = logging.FileHandler(os.path.join(log_path, 'error.log'))
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def get_logger(self):
        return self.logger  # Возвращаем сам логгер, а не его атрибут
   
