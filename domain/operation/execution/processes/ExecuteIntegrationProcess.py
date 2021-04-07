import multiprocessing
import traceback
from queue import Queue
from time import time
from injector import inject
from pandas import DataFrame
from infrastructor.multi_processing.ProcessManager import ProcessManager
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from infrastructor.IocManager import IocManager
from infrastructor.connection.models.DataQueueTask import DataQueueTask
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger


class ExecuteIntegrationProcess(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 data_operation_integration_service: DataOperationIntegrationService,
                 integration_execution_service: IntegrationExecutionService):
        self.data_operation_integration_service = data_operation_integration_service
        self.integration_execution_service = integration_execution_service
        self.sql_logger = sql_logger

    @staticmethod
    def start_source_data_process(sub_process_id,
                                  data_integration_id: int,
                                  data_operation_job_execution_integration_id: int,
                                  limit: int,
                                  process_count: int,
                                  data_queue: Queue,
                                  data_result_queue: Queue):
        return IocManager.injector.get(ExecuteIntegrationProcess).start_source_data_operation(
            sub_process_id=sub_process_id,
            data_integration_id=data_integration_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            limit=limit,
            process_count=process_count,
            data_queue=data_queue,
            data_result_queue=data_result_queue,
        )

    def start_source_data_operation(self, sub_process_id,
                                    data_integration_id: int,
                                    data_operation_job_execution_integration_id: int,
                                    limit: int,
                                    process_count: int,
                                    data_queue: Queue,
                                    data_result_queue: Queue):
        self.sql_logger.info(f"Source Data started on process. SubProcessId: {sub_process_id}")
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
        except Exception as ex:
            for i in range(process_count):
                data_queue_error_task = DataQueueTask(IsFinished=True, Traceback=traceback.format_exc(), Exception=ex)
                data_queue.put(data_queue_error_task)
            raise

    @staticmethod
    def start_execute_data_process(sub_process_id,
                                   data_integration_id: int,
                                   data_operation_job_execution_integration_id: int,
                                   data_queue: Queue,
                                   data_result_queue: Queue) -> int:
        return IocManager.injector.get(ExecuteIntegrationProcess).start_execute_data_operation(
            sub_process_id=sub_process_id,
            data_integration_id=data_integration_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_queue=data_queue,
            data_result_queue=data_result_queue,
        )

    def start_execute_data_operation(self,
                                     sub_process_id: int,
                                     data_integration_id: int,
                                     data_operation_job_execution_integration_id: int,
                                     data_queue: Queue,
                                     data_result_queue: Queue) -> int:
        total_row_count = 0
        try:
            while True:
                data_task: DataQueueTask = data_queue.get()
                if data_task.IsFinished:
                    if data_task.Exception is not None:
                        exc = Exception(data_task.Traceback + '\n' + str(data_task.Exception))
                        raise exc
                    self.sql_logger.info(f"{sub_process_id} process tasks finished")
                    return total_row_count
                else:
                    start = time()
                    source_data_json = data_task.Data
                    source_data_frame: DataFrame = DataFrame(source_data_json)
                    if source_data_frame is not None and len(source_data_frame) > 0:
                        if data_task.DataTypes is not None:
                            data = source_data_frame.astype( dtype=data_task.DataTypes)
                        else:
                            data = source_data_frame
                        self.sql_logger.info(
                            f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process got a new task")
                        self.integration_execution_service.start_execute_integration(
                            data_integration_id=data_integration_id,
                            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                            data=data)
                    else:
                        self.sql_logger.info(
                            f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process got an empty task")

                    total_row_count = total_row_count + len(data)
                    end = time()
                    self.sql_logger.info(
                        f"{sub_process_id}-{data_task.Message}:{data_task.Id}-{data_task.Start}-{data_task.End} process finished task. time:{end - start}")
                    data_task.IsProcessed = True
                    data_result_queue.put(True)
            return total_row_count
        except Exception as ex:
            data_result_queue.put(False)
            raise

    def start_source_data_subprocess(self,
                                     source_data_process_manager: ProcessManager,
                                     data_integration_id: int,
                                     data_operation_job_execution_integration_id: int,
                                     limit: int,
                                     process_count: int,
                                     data_queue: Queue,
                                     data_result_queue: Queue):

        source_data_kwargs = {
            "data_integration_id": data_integration_id,
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
                                      data_operation_job_execution_integration_id: int,
                                      data_queue: Queue,
                                      data_result_queue: Queue) -> int:
        total_row_count = 0
        execute_data_kwargs = {
            "data_integration_id": data_integration_id,
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

    def start_integration_execution(self, data_operation_job_execution_integration_id: int,
                                    data_operation_integration_id: int) -> int:
        manager = multiprocessing.Manager()
        source_data_process_manager = ProcessManager()
        execute_data_process_manager = ProcessManager()
        try:
            data_operation_integration = self.data_operation_integration_service.get_by_id(
                id=data_operation_integration_id)
            if data_operation_integration.ProcessCount is not None and data_operation_integration.ProcessCount >= 1:
                process_count = data_operation_integration.ProcessCount
            else:
                process_count = 1
            data_integration_id = data_operation_integration.DataIntegrationId
            limit = data_operation_integration.Limit

            data_queue = manager.Queue()
            data_result_queue = manager.Queue()

            self.start_source_data_subprocess(source_data_process_manager=source_data_process_manager,
                                              data_integration_id=data_integration_id,
                                              data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                                              limit=limit,
                                              process_count=process_count, data_queue=data_queue,
                                              data_result_queue=data_result_queue)
            if process_count > 1:
                total_row_count = self.start_execute_data_subprocess(
                    execute_data_process_manager=execute_data_process_manager,
                    process_count=process_count,
                    data_integration_id=data_integration_id,
                    data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                    data_queue=data_queue,
                    data_result_queue=data_result_queue)
            else:
                total_row_count = self.start_execute_data_operation(sub_process_id=0,
                                                                    data_integration_id=data_integration_id,
                                                                    data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                                                                    data_queue=data_queue,
                                                                    data_result_queue=data_result_queue)
            return total_row_count
        except Exception as ex:
            self.sql_logger.error("Integration getting error")
            raise
        finally:
            manager.shutdown()
            del source_data_process_manager
            del execute_data_process_manager
