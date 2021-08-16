import traceback
from datetime import datetime
from logging import DEBUG, FATAL, ERROR, WARNING, INFO, NOTSET

from IocManager import IocManager
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from infrastructure.logging.ConsoleLogger import ConsoleLogger
from infrastructure.utils.Utils import Utils
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.common.Log import Log


class SqlLogger(IScoped):
    def __init__(self):
        pass

    @staticmethod
    def log_to_db(level, message, job_id=None):
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        console_logger: ConsoleLogger = IocManager.injector.get(ConsoleLogger)
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        process_info = Utils.get_process_info()
        application_name = application_config.name
        if application_config.hostname is not None:
            application_name += f'-{application_config.hostname}'
        comment = f'{application_name}-{process_info}'
        try:
            log_repository = RepositoryProvider().get(Log)
            log = Log(TypeId=level, Content=message[0:4000], LogDatetime=log_datetime,
                      JobId=job_id, Comments=comment)
            log_repository.insert(log)
            log_repository.commit()
        except Exception as ex:
            console_logger.error(f'{job_id}-Sql logging getting error. Error:{ex}')
        finally:
            if job_id is not None:
                message = f"{job_id}-{message}"
            console_logger.log(level, f'{message}')

    #######################################################################################
    def logger_method(self, level, message, job_id=None):
        SqlLogger.log_to_db(level=level, message=message, job_id=job_id)

    #######################################################################################
    def exception(self, exception: Exception, message: str = None, job_id=None):
        exc = traceback.format_exc() + '\n' + str(exception)
        message += f"Error: {exc}"
        self.logger_method(ERROR, message, job_id)

    #######################################################################################
    def fatal(self, message, job_id=None):
        self.logger_method(FATAL, message, job_id)

    #######################################################################################
    def error(self, message, job_id=None):
        self.logger_method(ERROR, message, job_id)

    #######################################################################################
    def warning(self, message, job_id=None):
        self.logger_method(WARNING, message, job_id)

    #######################################################################################
    def info(self, message, job_id=None):
        self.logger_method(INFO, message, job_id)

    #######################################################################################
    def debug(self, message, job_id=None):
        self.logger_method(DEBUG, message, job_id)

    #######################################################################################
    def log(self, message, job_id=None):
        self.logger_method(NOTSET, message, job_id)
