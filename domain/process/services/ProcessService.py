from datetime import datetime
from time import time
from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData, ParallelMultiProcessing
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
                 ):
        self.database_session_manager = database_session_manager
        self.sql_logger: SqlLogger = sql_logger

    def start_parallel_process(self, process_id, datas, process_count, process_function, result_method,job_id):
        start = time()
        start_datetime = datetime.now()

        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"MultiThread Operations Started")
        parallel_multi_processing = ParallelMultiProcessing(process_count)
        parallel_multi_processing.configure_process()
        parallel_multi_processing.start_processes(process_id=process_id,job_id=job_id, process_function=process_function)
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

        unprocessed_task = parallel_multi_processing.unprocessed_tasks()
        return unprocessed_task
