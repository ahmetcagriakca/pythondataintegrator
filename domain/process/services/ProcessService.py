from datetime import datetime
from time import time
from injector import inject
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData, ParallelMultiProcessing
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.connection.ConnectorType import ConnectorType
from models.dao.connection.ConnectionType import ConnectionType
from models.configs.DatabaseConfig import DatabaseConfig
from infrastructor.IocManager import IocManager


class TaskValue:
    def __init__(self,
                 Value: any = None):
        self.Value: any = Value
        self.Result: any


class ProcessService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 database_provider: ConnectionProvider,
                 crypto_service: CryptoService,
                 database_config: DatabaseConfig,
                 ):
        self.database_config = database_config
        self.database_session_manager = database_session_manager
        self.connection_type_repository: Repository[ConnectionType] = Repository[ConnectionType](
            database_session_manager)
        self.connector_type_repository: Repository[ConnectorType] = Repository[ConnectorType](
            database_session_manager)
        self.connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
            database_session_manager)
        self.connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)
        self.database_provider: ConnectionProvider = database_provider
        self.sql_logger: SqlLogger = sql_logger
        self.crypto_service = crypto_service

    def start_parallel_process(self, process_id, datas, process_count, process_method, result_method):
        start = time()
        print(f"StartTime :{start}")
        start_datetime = datetime.now()

        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"MultiThread Operations Started")
        parallel_multi_processing = ParallelMultiProcessing(process_count)
        parallel_multi_processing.configure_process()
        parallel_multi_processing.start_processes(process_id, process_method)
        for data in datas:
            td = TaskData(data)
            parallel_multi_processing.add_task(td)
        parallel_multi_processing.finish_tasks()
        parallel_multi_processing.check_processes(result_method)
        end_datetime = datetime.now()
        end = time()
        print(f"Start :{start_datetime}")
        print(f"End :{end_datetime}")
        print(f"ElapsedTime :{end - start}")
        return start_datetime, end_datetime, start, end
