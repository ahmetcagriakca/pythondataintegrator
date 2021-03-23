from datetime import datetime
from time import time
from injector import inject
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import ParallelMultiProcessing
from infrastructor.multi_processing.models.TaskData import TaskData
from infrastructor.IocManager import IocManager


class TaskValue:
    def __init__(self,
                 Value: any = None):
        self.Value: any = Value
        self.Result: any


class ProcessService(IScoped):

    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 ):
        self.sql_logger: SqlLogger = sql_logger

    def start_parallel_process(self, process_id, datas, process_count, process_function, job_id, result_function=None):
        start = time()
        start_datetime = datetime.now()

        sql_logger = IocManager.injector.get(SqlLogger)
        sql_logger.info(f"MultiThread Operations Started")
        parallel_multi_processing = ParallelMultiProcessing(process_count)
        parallel_multi_processing.configure_process()
        parallel_multi_processing.start_processes(process_id=process_id, job_id=job_id,
                                                  process_function=process_function)
        for data in datas:
            td = TaskData(data)
            parallel_multi_processing.add_task(td)
        parallel_multi_processing.finish_tasks()
        parallel_multi_processing.check_processes(result_function)
        end_datetime = datetime.now()
        end = time()
        print(f"Start :{start_datetime}")
        print(f"End :{end_datetime}")
        print(f"ElapsedTime :{end - start}")
        processed_task = parallel_multi_processing.processed_tasks()
        unprocessed_task = parallel_multi_processing.unprocessed_tasks()
        del parallel_multi_processing
        return unprocessed_task, processed_task
