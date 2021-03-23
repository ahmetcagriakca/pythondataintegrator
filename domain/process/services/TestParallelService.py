import os
from datetime import datetime
from time import time
from injector import inject
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.connection.database.DatabaseProvider import DatabaseProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import ParallelMultiProcessing
from infrastructor.multi_processing.models.TaskData import TaskData
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


class TestParallelService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 database_provider: DatabaseProvider,
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
        self.database_provider: DatabaseProvider = database_provider
        self.sql_logger: SqlLogger = sql_logger
        self.crypto_service = crypto_service

    @staticmethod
    def calculate_method(sql_logger, process_name, my_value):
        start = time()
        start_datetime = datetime.now()
        sql_logger.info(f"{process_name} process worked with {my_value}")
        # Compute result and mimic a long-running task
        compute = my_value * my_value
        # Output which process received the value
        # and the calculation result
        print('[%s] received value: %i' % (process_name, my_value))
        print('[%s] calculated value: %i' % (process_name, compute))
        # Add result to the queue
        end_datetime = datetime.now()
        end = time()
        sql_logger.info(
            f"{process_name} process calculated {compute}  time:{end - start} , {start_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}-{end_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
        return compute

    @staticmethod
    def parallel_data_test(process_id, process_name, tasks, results):
        try:
            print('[%s] evaluation routine starts' % process_name)

            root_directory = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
            IocManager.configure_startup(root_directory)
            sql_logger = IocManager.injector.get(SqlLogger)
            while True:
                new_value = tasks.get()
                if new_value.IsFinished:
                    sql_logger.info(f"{process_name} process finished")
                    print('[%s] evaluation routine quits' % process_name)
                    # Indicate finished
                    results.put(new_value)
                    break
                else:
                    new_value.Data.Result = TestParallelService.calculate_method(sql_logger, process_name,
                                                                                 new_value.Data.Value)
                    # Add result to the queue
                    results.put(new_value)
        except Exception as ex:
            data = TaskData(IsFinished=True)
            results.put(data)

    @staticmethod
    def parallel_test_result(result: TaskData):
        if not result.IsFinished:
            print(f'value {result.Data.Value} result:{result.Data.Result}')

    def test_performance_parallel(self, data, thread_count):
        p_start_datetime, p_end_datetime, p_start, p_end = self.test_parallel(data, thread_count)

        start_datetime, end_datetime, start, end = self.test_with_not_parallel(data)

        result_message = ''
        result_message += f"Parallel Performance\n"
        result_message += f"Start :{p_start_datetime}\n"
        result_message += f"End :{p_end_datetime}\n"
        result_message += f"ElapsedTime :{p_end - p_start}\n"

        result_message += f"One Thread Performance\n"
        result_message += f"Start :{start_datetime}\n"
        result_message += f"End :{end_datetime}\n"
        result_message += f"ElapsedTime :{end - start}\n"
        return result_message

    def test_parallel(self, data, thread_count):

        start = time()
        start_datetime = datetime.now()

        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"MultiThread Operations Started")
        parallel_multi_processing = ParallelMultiProcessing(thread_count)
        parallel_multi_processing.configure_process()
        parallel_multi_processing.start_processes(None, TestParallelService.parallel_data_test)
        for i in range(data):
            tv = TaskValue(i)
            td = TaskData(tv)
            parallel_multi_processing.add_task(td)
        parallel_multi_processing.finish_tasks()
        parallel_multi_processing.check_processes(TestParallelService.parallel_test_result)
        end_datetime = datetime.now()
        end = time()
        print(f"Start :{start_datetime}")
        print(f"End :{end_datetime}")
        print(f"ElapsedTime :{end - start}")
        return start_datetime, end_datetime, start, end

    def test_with_not_parallel(self, data):

        start = time()
        start_datetime = datetime.now()
        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"One Thread Operations Started")
        for i in range(data):
            tv = TaskValue(i)
            td = TaskData(tv)
            td.Data.Result = TestParallelService.calculate_method(sql_logger, "MainProcess", td.Data.Value)
            TestParallelService.parallel_test_result(td)
        end_datetime = datetime.now()
        end = time()
        print(f"Start :{start_datetime}")
        print(f"End :{end_datetime}")
        print(f"ElapsedTime :{end - start}")
        return start_datetime, end_datetime, start, end
