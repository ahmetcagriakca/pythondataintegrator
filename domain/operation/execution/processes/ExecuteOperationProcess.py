import traceback
from time import time
from injector import inject

from domain.operation.execution.services.OperationExecution import OperationExecution
from infrastructor.IocManager import IocManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData


class ExecuteOperationProcess(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 operation_execution: OperationExecution):
        self.operation_execution = operation_execution
        self.sql_logger = sql_logger

    def job_start_operation(self, data_operation_id, job_id, sub_process_id, process_name, tasks, results):

        try:
            print('[%s] evaluation routine starts' % process_name)

            while True:
                # waiting for new task
                new_task: TaskData = tasks.get()
                new_task.SubProcessId = sub_process_id
                start = time()
                self.sql_logger.info(
                    f"{job_id}-{data_operation_id} process started.")

                result = self.operation_execution.start(data_operation_id=data_operation_id, job_id=job_id)
                end = time()
                self.sql_logger.info(
                    f"{job_id}-{data_operation_id} process finished. time:{end - start}")
                new_task.IsProcessed = True
                new_task.IsFinished = True
                new_task.Data.State = 1
                new_task.Data.Result = result
                results.put(new_task)
        except Exception as ex:
            self.sql_logger.error(f"{job_id}-{data_operation_id} process getting error:{ex}", job_id=job_id)
            data = new_task.Data
            data.State = 2
            data.Message = str(ex)
            data.Exception = ex
            data.Traceback = traceback.format_exc()
            data = TaskData(Data=data, SubProcessId=sub_process_id, IsFinished=True)
            results.put(data)

    @staticmethod
    def job_start_thread(process_id, job_id, sub_process_id, process_name, tasks, results):
        IocManager.initialize()
        operation_executor = IocManager.injector.get(ExecuteOperationProcess)
        operation_executor.job_start_operation(data_operation_id=process_id, job_id=job_id,
                                               sub_process_id=sub_process_id, process_name=process_name,
                                               tasks=tasks, results=results)
