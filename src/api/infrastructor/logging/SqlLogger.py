from datetime import datetime
from logging import DEBUG, FATAL, ERROR, WARNING, INFO, NOTSET

from IocManager import IocManager
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.ConsoleLogger import ConsoleLogger
from infrastructor.utils.Utils import Utils
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.common.Log import Log


class SqlLogger(IScoped):
    def __init__(self):
        pass

    @staticmethod
    def log_to_db(level, log_string, job_id=None):
        application_config: ApplicationConfig = IocManager.config_manager.get(ApplicationConfig)
        console_logger: ConsoleLogger = IocManager.injector.get(ConsoleLogger)
        log_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        process_info = Utils.get_process_info()
        comment = f'{application_config.name}-{application_config.environment}-{process_info}'
        try:
            log_repository = RepositoryProvider().get(Log)
            log = Log(TypeId=level, Content=log_string[0:4000], LogDatetime=log_datetime,
                      JobId=job_id, Comments=comment)
            log_repository.insert(log)
            log_repository.commit()
        except Exception as ex:
            console_logger.error(f'Sql logging getting error{ex}')
        finally:
            console_logger.log(level, f'{log_string}')

    #######################################################################################
    def logger_method(self, level, log_string, job_id=None):
        SqlLogger.log_to_db(level=level, log_string=log_string, job_id=job_id)
        # Process(target=self.log_to_db, name="Log Process", args=(type_of_log, log_string, job_id,)).start()

    #######################################################################################
    def fatal(self, error_string, job_id=None):
        self.logger_method(FATAL, error_string, job_id)

    #######################################################################################
    def error(self, error_string, job_id=None):
        self.logger_method(ERROR, error_string, job_id)

    #######################################################################################
    def warning(self, info_string, job_id=None):
        self.logger_method(WARNING, info_string, job_id)

    #######################################################################################
    def info(self, info_string, job_id=None):
        self.logger_method(INFO, info_string, job_id)

    #######################################################################################
    def debug(self, info_string, job_id=None):
        self.logger_method(DEBUG, info_string, job_id)

    #######################################################################################
    def log(self, info_string, job_id=None):
        self.logger_method(NOTSET, info_string, job_id)
