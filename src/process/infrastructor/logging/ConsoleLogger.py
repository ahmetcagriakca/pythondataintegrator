import logging as log
from datetime import datetime
from injector import inject
from infrastructor.dependency.scopes import ISingleton
from infrastructor.utils.Utils import Utils


class ConsoleLogger(ISingleton):
    @inject
    def __init__(self):
        self.log_level = log.DEBUG
        self.log_init()
        self.logger = log

    def log_init(self):
        """
        initialization of log file.
        """
        log.basicConfig(level=self.log_level)

    @staticmethod
    def prepare_message(message):
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        process_info = Utils.get_process_info()
        return f'{log_datetime} - {process_info} - {message} '

    def log(self, level, message):
        prepared_message = self.prepare_message(message)
        self.logger.log(level, prepared_message)

    def fatal(self, message):
        prepared_message = self.prepare_message(message)
        self.logger.fatal(prepared_message)

    def error(self, message):
        prepared_message = self.prepare_message(message)
        self.logger.error(prepared_message)

    def warning(self, message):
        prepared_message = self.prepare_message(message)
        self.logger.warning(prepared_message)

    def info(self, message):
        prepared_message = self.prepare_message(message)
        self.logger.info(prepared_message)

    def debug(self, message):
        prepared_message = self.prepare_message(message)
        self.logger.debug(prepared_message)
