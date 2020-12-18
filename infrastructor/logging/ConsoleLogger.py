import logging as log
from datetime import datetime
from injector import inject
from infrastructor.dependency.scopes import ISingleton


class ConsoleLogger(ISingleton):
    @inject
    def __init__(self):
        self.log_level = log.DEBUG
        self.log_init()
        self.log = log

    def log_init(self):
        """
        initialization of log file.
        """
        log.basicConfig(level=self.log_level)

    @staticmethod
    def prepare_message(message):
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return f'{log_datetime} - {message}'

    def info(self, message):
        prepared_message = self.prepare_message(message);
        self.log.info(prepared_message)

    def error(self, message):
        prepared_message = self.prepare_message(message);
        self.log.error(prepared_message)

    def warning(self, message):
        prepared_message = self.prepare_message(message);
        self.log.warning(prepared_message)
