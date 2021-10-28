import multiprocessing
import traceback
from queue import Queue
from time import time

import pandas as pd
from func_timeout import FunctionTimedOut
from injector import inject
from pandas import DataFrame, notnull
from pdip.connection.models import DataQueueTask
from pdip.data.decorators import transactionhandler
from pdip.dependency import IScoped
from pdip.dependency.container import DependencyContainer
from pdip.exceptions import OperationalException
from pdip.logging.loggers.database import SqlLogger
from pdip.processing import ProcessManager

from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationStrategy import \
    ExecuteIntegrationStrategy
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from models.dto.PagingModifier import PagingModifier


class ExecuteIntegrationProcess(ExecuteIntegrationStrategy, IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 operation_cache_service: OperationCacheService,
                 integration_execution_service: IntegrationExecutionService):
        self.operation_cache_service = operation_cache_service
        self.integration_execution_service = integration_execution_service
        self.sql_logger = sql_logger

    @staticmethod
    def start_source_data_process(sub_process_id,
                                  data_integration_id: int,
                                  data_operation_job_execution_id: int,
                                  data_operation_job_execution_integration_id: int,
                                  limit: int,
                                  process_count: int,
                                  data_queue: Queue,
                                  data_result_queue: Queue):
        return DependencyContainer.Instance.get(ExecuteIntegrationProcess).start_source_data_operation(
            sub_process_id=sub_process_id,
            data_integration_id=data_integration_id,
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            limit=limit,
            process_count=process_count,
            data_queue=data_queue,
            data_result_queue=data_result_queue,
        )

    @transactionhandler
    def start_source_data_operation(self, sub_process_id,
                                    data_integration_id: int,
                                    data_operation_job_execution_id: int,
                                    data_operation_job_execution_integration_id: int,
                                    limit: int,
                                    process_count: int,
                                    data_queue: Queue,
                                    data_result_queue: Queue):
        self.operation_cache_service.create_data_integration(data_integration_id=data_integration_id)
        self.sql_logger.info(f"Source data operation started on process. SubProcessId: {sub_process_id}",
                             job_id=data_operation_job_execution_id)
        try:
            self.integration_execution_service.start_source_data_operation(
                data_integration_id=data_integration_id,
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                limit=limit,
                process_count=process_count,
                data_queue=data_queue,
                data_result_queue=data_result_queue)
            for i in range(process_count):
                data_queue_finish_task = DataQueueTask(IsFinished=True)
                data_queue.put(data_queue_finish_task)

            self.sql_logger.info(f"Source data operation finished successfully. SubProcessId: {sub_process_id}",
                                 job_id=data_operation_job_execution_id)
        except Exception as ex:
            exception_traceback = traceback.format_exc()
            for i in range(process_count):
                data_queue_error_task = DataQueueTask(IsFinished=True, Traceback=exception_traceback, Exception=ex)
                data_queue.put(data_queue_error_task)
            self.sql_logger.info(
                f"Source data operation finished with error. SubProcessId: {sub_process_id}. Error:{ex} traceback:{exception_traceback}",
                job_id=data_operation_job_execution_id)
            raise

    @staticmethod
    def start_execute_data_process(sub_process_id,
                                   data_integration_id: int,
                                   data_operation_job_execution_id: int,
                                   data_operation_job_execution_integration_id: int,
                                   data_queue: Queue,
                                   data_result_queue: Queue) -> int:
        return DependencyContainer.Instance.get(ExecuteIntegrationProcess).start_execute_data_operation(
            sub_process_id=sub_process_id,
            data_integration_id=data_integration_id,
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_queue=data_queue,
            data_result_queue=data_result_queue,
        )

    @transactionhandler
    def start_execute_data_operation_on_process(self,
                                                sub_process_id: int,
                                                data_integration_id: int,
                                                data_operation_job_execution_id: int,
                                                data_operation_job_execution_integration_id: int,
                                                data_queue: Queue,
                                                data_result_queue: Queue) -> int:
        return DependencyContainer.Instance.get(ExecuteIntegrationProcess).start_execute_data_operation(
            sub_process_id=sub_process_id,
            data_integration_id=data_integration_id,
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_queue=data_queue,
            data_result_queue=data_result_queue,
        )

    def start_execute_data_operation(self,
                                     sub_process_id: int,
                                     data_integration_id: int,
                                     data_operation_job_execution_id: int,
                                     data_operation_job_execution_integration_id: int,
                                     data_queue: Queue,
                                     data_result_queue: Queue) -> int:

        self.operation_cache_service.create_data_integration(data_integration_id=data_integration_id)
        total_row_count = 0
        try:
            while True:
                data_task: DataQueueTask = data_queue.get()
                if data_task.IsFinished:
                    if data_task.Exception is not None:
                        exc = Exception(data_task.Traceback + '\n' + str(data_task.Exception))
                        raise exc
                    self.sql_logger.info(f"{sub_process_id} process tasks finished",
                                         job_id=data_operation_job_execution_id)
                    return total_row_count
                else:
                    start = time()
                    data = data_task.Data
                    paging_modifier = PagingModifier(Id=data_task.Id, End=data_task.End, Start=data_task.Start,
                                                     Limit=data_task.Limit)
                    if data_task.IsDataFrame and data is not None:
                        source_data_json = data_task.Data
                        data: DataFrame = DataFrame(source_data_json)
                    data_count = 0
                    if data is None:
                        self.sql_logger.info(
                            f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process got a new task without data",
                            job_id=data_operation_job_execution_id)
                        data_count = self.integration_execution_service.start_execute_integration_with_paging(
                            data_integration_id=data_integration_id,
                            data_operation_job_execution_id=data_operation_job_execution_id,
                            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                            paging_modifier=paging_modifier)
                    elif data is not None and len(data) > 0:
                        if data_task.IsDataFrame and data_task.DataTypes is not None:
                            source_data = data.astype(dtype=data_task.DataTypes)
                        else:
                            source_data = data
                        if data_task.IsDataFrame:
                            source_data = source_data.where(notnull(data), None)
                            source_data = source_data.replace({pd.NaT: None})

                        self.sql_logger.info(
                            f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process got a new task",
                            job_id=data_operation_job_execution_id)
                        data_count = self.integration_execution_service.start_execute_integration_with_source_data(
                            data_integration_id=data_integration_id,
                            data_operation_job_execution_id=data_operation_job_execution_id,
                            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                            source_data=source_data)
                    else:
                        self.sql_logger.info(
                            f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process got an empty task",
                            job_id=data_operation_job_execution_id)

                    total_row_count = total_row_count + data_count
                    end = time()
                    self.sql_logger.info(
                        f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process finished task. time:{end - start}",
                        job_id=data_operation_job_execution_id)
                    data_task.IsProcessed = True
                    data_result_queue.put(True)
                data_queue.task_done()
            return total_row_count
        except FunctionTimedOut as fto:
            data_result_queue.put(False)
            end = time()
            self.sql_logger.info(
                f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process getting error. time:{end - start} - Error {fto.getMsg()}",
                job_id=data_operation_job_execution_id)
            raise Exception(f'Execution Operation timed out after {fto.timedOutAfter} seconds.')
        except Exception as ex:
            data_result_queue.put(False)
            raise

    def start_source_data_subprocess(self,
                                     source_data_process_manager: ProcessManager,
                                     data_integration_id: int,
                                     data_operation_job_execution_id: int,
                                     data_operation_job_execution_integration_id: int,
                                     limit: int,
                                     process_count: int,
                                     data_queue: Queue,
                                     data_result_queue: Queue):

        source_data_kwargs = {
            "data_integration_id": data_integration_id,
            "data_operation_job_execution_id": data_operation_job_execution_id,
            "data_operation_job_execution_integration_id": data_operation_job_execution_integration_id,
            "limit": limit,
            "process_count": process_count,
            "data_queue": data_queue,
            "data_result_queue": data_result_queue,
        }

        source_data_process_manager.start_processes(
            process_count=1,
            target_method=self.start_source_data_process,
            kwargs=source_data_kwargs)

    def start_execute_data_subprocess(self, execute_data_process_manager: ProcessManager,
                                      process_count: int,
                                      data_integration_id: int,
                                      data_operation_job_execution_id: int,
                                      data_operation_job_execution_integration_id: int,
                                      data_queue: Queue,
                                      data_result_queue: Queue) -> int:
        total_row_count = 0
        execute_data_kwargs = {
            "data_integration_id": data_integration_id,
            "data_operation_job_execution_id": data_operation_job_execution_id,
            "data_operation_job_execution_integration_id": data_operation_job_execution_integration_id,
            "data_queue": data_queue,
            "data_result_queue": data_result_queue,
        }
        execute_data_process_manager.start_processes(
            process_count=process_count,
            target_method=self.start_execute_data_process,
            kwargs=execute_data_kwargs)
        execute_data_process_results = execute_data_process_manager.get_results()
        for result in execute_data_process_results:
            if result.Exception is not None:
                raise result.Exception
            if result.Result is not None:
                total_row_count = total_row_count + result.Result
        return total_row_count

    def execute(self,
                data_operation_job_execution_id: int,
                data_operation_job_execution_integration_id: int,
                data_operation_integration_id: int) -> int:
        try:
            data_operation_integration = self.operation_cache_service.get_data_operation_integration_by_id(
                data_operation_integration_id=data_operation_integration_id)
            data_integration_id = data_operation_integration.DataIntegrationId
            if data_operation_integration.ProcessCount is None or data_operation_integration.ProcessCount <= 1:
                raise OperationalException("Parallel execution process count must bigger than 1")
            process_count = data_operation_integration.ProcessCount
            limit = data_operation_integration.Limit

            try:
                manager = multiprocessing.Manager()
                source_data_process_manager = ProcessManager()
                execute_data_process_manager = ProcessManager()
                data_queue = manager.Queue()
                data_result_queue = manager.Queue()
                self.start_source_data_subprocess(source_data_process_manager=source_data_process_manager,
                                                  data_integration_id=data_integration_id,
                                                  data_operation_job_execution_id=data_operation_job_execution_id,
                                                  data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                                                  limit=limit,
                                                  process_count=process_count, data_queue=data_queue,
                                                  data_result_queue=data_result_queue)
                if process_count > 1:
                    total_row_count = self.start_execute_data_subprocess(
                        execute_data_process_manager=execute_data_process_manager,
                        process_count=process_count,
                        data_integration_id=data_integration_id,
                        data_operation_job_execution_id=data_operation_job_execution_id,
                        data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                        data_queue=data_queue,
                        data_result_queue=data_result_queue)
                else:
                    total_row_count = self.start_execute_data_operation(sub_process_id=0,
                                                                        data_integration_id=data_integration_id,
                                                                        data_operation_job_execution_id=data_operation_job_execution_id,
                                                                        data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                                                                        data_queue=data_queue,
                                                                        data_result_queue=data_result_queue)
            finally:
                manager.shutdown()
                del source_data_process_manager
                del execute_data_process_manager

            return total_row_count
        except Exception as ex:
            self.sql_logger.error(f"Integration getting error.Error:{ex}", job_id=data_operation_job_execution_id)
            raise
