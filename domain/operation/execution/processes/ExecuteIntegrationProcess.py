import traceback
from time import time
from typing import List
from injector import inject
from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.process.services.ProcessService import ProcessService
from infrastructor.IocManager import IocManager
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from models.dto.PagingModifier import PagingModifier


class ExecuteIntegrationProcess(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 process_service: ProcessService,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_integration_column_service: DataIntegrationColumnService,
                 integration_execution_service: IntegrationExecutionService):
        self.integration_execution_service = integration_execution_service
        self.process_service = process_service
        self.sql_logger = sql_logger
        self.data_integration_column_service = data_integration_column_service
        self.data_operation_integration_service = data_operation_integration_service

    def start_parallel_process(self, data_operation_job_execution_id: int, data_operation_integration_id: int,
                               data_count: int):

        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        paging_modifiers = self.get_paging_modifiers(data_count=data_count, limit=data_operation_integration.Limit)
        unprocessed_task_list, processed_task_list = self.process_service.start_parallel_process(
            process_id=data_operation_integration.DataIntegrationId,
            datas=paging_modifiers,
            process_count=data_operation_integration.ProcessCount,
            process_function=ExecuteIntegrationProcess.parallel_operation,
            job_id=data_operation_job_execution_id)
        print("parallel finished")
        total_affected_row_count = sum([int(processed_task.Data.Message) for processed_task in processed_task_list if
                                        processed_task.Data is not None])
        if unprocessed_task_list is not None and len(unprocessed_task_list) > 0:
            print(f"Unprocessed tasks founded")
            paging_modifiers = [unprocessed_task.Data for unprocessed_task in unprocessed_task_list]
            result = self.execute_paging_modifiers(
                data_integration_id=data_operation_integration.DataIntegrationId,
                paging_modifiers=paging_modifiers)
            total_affected_row_count = total_affected_row_count + result
        return total_affected_row_count

    def start_serial_process(self, data_operation_integration_id: int,
                             data_count: int) -> int:

        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        paging_modifiers = self.get_paging_modifiers(data_count=data_count, limit=data_operation_integration.Limit)
        total_affected_row_count = self.execute_paging_modifiers(
            data_integration_id=data_operation_integration.DataIntegrationId,
            paging_modifiers=paging_modifiers)
        return total_affected_row_count

    @staticmethod
    def get_paging_modifiers(data_count, limit):
        end = limit
        start = 0
        paging_modifiers = []
        id = 0
        while True:
            if end != limit and end - data_count > limit:
                break
            id = id + 1
            paging_modifier = PagingModifier(Id=id, End=end, Start=start, Limit=limit)
            paging_modifiers.append(paging_modifier)
            end += limit
            start += limit
        return paging_modifiers

    def execute_paging_modifiers(self, data_integration_id: int, paging_modifiers: List[PagingModifier]) -> int:
        total_affected_row_count = 0
        for paging_modifier in paging_modifiers:
            start = time()
            self.sql_logger.info(
                f"Process got a new task.Id:{paging_modifier.Id}  limits:{paging_modifier.Start}-{paging_modifier.End} ")
            affected_row_count = self.integration_execution_service.start_execute_integration(
                data_integration_id=data_integration_id,
                paging_modifier=paging_modifier)
            if affected_row_count is None:
                affected_row_count = 0
            total_affected_row_count = total_affected_row_count + affected_row_count
            end = time()
            self.sql_logger.info(
                f"Process finished task. limits:{paging_modifier.Start}-{paging_modifier.End}. time:{end - start}")

        return total_affected_row_count

    def start_parallel_operation(self, process_id, job_id, sub_process_id, process_name, tasks, results):
        try:
            print('[%s] evaluation routine starts' % process_name)

            while True:
                # waiting for new task
                new_task: TaskData = tasks.get()
                new_task.SubProcessId = sub_process_id
                if new_task.IsFinished:
                    self.sql_logger.info(f"{process_name} process finished")
                    # Indicate finished
                    results.put(new_task)
                    break
                else:
                    start = time()
                    self.sql_logger.info(
                        f"{process_name}-{sub_process_id} process got a new task.Id:{new_task.Data.Id} limits:{new_task.Data.Start}-{new_task.Data.End} ")
                    paging_modifier: PagingModifier = new_task.Data
                    result = self.integration_execution_service.start_execute_integration(
                        data_integration_id=process_id,
                        paging_modifier=paging_modifier)
                    end = time()
                    self.sql_logger.info(
                        f"{process_name} process finished task. limits:{new_task.Data.Start}-{new_task.Data.End}. time:{end - start}")
                    new_task.IsProcessed = True
                    new_task.Data.State = 1
                    new_task.Data.Message = result
                    results.put(new_task)
        except Exception as ex:
            self.sql_logger.error(f"{process_name} process getting error:{ex}", job_id=job_id)
            data = new_task.Data
            data.State = 2
            data.Message = str(ex)
            data.Exception = ex
            data.Traceback = traceback.format_exc()
            data = TaskData(Data=data, SubProcessId=sub_process_id, IsFinished=True)
            results.put(data)

    @staticmethod
    def parallel_operation(process_id, job_id, sub_process_id, process_name, tasks, results):
        IocManager.initialize()
        execute_operation_adapter = IocManager.injector.get(ExecuteIntegrationProcess)
        execute_operation_adapter.start_parallel_operation(process_id=process_id, job_id=job_id,
                                                           sub_process_id=sub_process_id, process_name=process_name,
                                                           tasks=tasks, results=results)
