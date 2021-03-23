from queue import Queue
from time import time
from injector import inject
from pandas import DataFrame, notnull

from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.operation.execution.adapters.connection.ConnectionAdapterFactory import ConnectionAdapterFactory
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from infrastructor.connection.models.DataQueueTask import DataQueueTask
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.dto.PagingModifier import PagingModifier
from models.enums.StatusTypes import StatusTypes
from models.enums.events import EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, \
    EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT, EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY


class IntegrationExecutionService(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 data_integration_service: DataIntegrationService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService,
                 connection_adapter_factory: ConnectionAdapterFactory):
        self.data_integration_service = data_integration_service
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service
        self.sql_logger = sql_logger
        self.connection_adapter_factory = connection_adapter_factory

    def start_execute_integration_unpredicted_source(self, data_integration_id: int, limit: int) -> int:

        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        target_adapter = self.connection_adapter_factory.get_target_adapter(
            data_integration_id=data_integration_id)
        data_queue = Queue()
        result_queue = Queue()
        source_adapter.start_source_data_process(data_integration_id=data_integration_id,
                                                 limit=limit,
                                                 data_queue=data_queue,
                                                 result_queue=result_queue)
        total_row_count = 0
        while True:
            try:
                new_task: DataQueueTask = data_queue.get()
                if new_task.IsFinished:
                    if new_task.Exception is not None:
                        raise new_task.Exception
                    self.sql_logger.info(f"process finished")
                    break
                else:
                    start = time()
                    self.sql_logger.info("process got a new task")
                    source_data_json = new_task.Data
                    source_data_frame: DataFrame = DataFrame(source_data_json)
                    df = source_data_frame.where(notnull(source_data_frame), None)
                    source_data = df.values.tolist()
                    prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id,
                                                                source_data=source_data)
                    target_adapter.write_target_data(
                        data_integration_id=data_integration_id,
                        prepared_data=prepared_data)
                    total_row_count = total_row_count + len(source_data)
                    end = time()
                    self.sql_logger.info(f"process finished task. time:{end - start}")
                    new_task.IsProcessed = True

                    result_queue.put(True)
            except Exception as ex:
                result_queue.put(False)
                raise
        return total_row_count

    def start_execute_integration(self, data_integration_id: int, paging_modifier: PagingModifier) -> int:
        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        source_data = source_adapter.get_source_data(data_integration_id=data_integration_id,
                                                     paging_modifier=paging_modifier)

        target_adapter = self.connection_adapter_factory.get_target_adapter(
            data_integration_id=data_integration_id)
        prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id,
                                                    source_data=source_data)
        target_adapter.write_target_data(data_integration_id=data_integration_id,
                                                              prepared_data=prepared_data)
        return 0

    def start_execute_integration(self, data_integration_id: int, paging_modifier: PagingModifier) -> int:
        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        source_data = source_adapter.get_source_data(data_integration_id=data_integration_id,
                                                     paging_modifier=paging_modifier)

        target_adapter = self.connection_adapter_factory.get_target_adapter(
            data_integration_id=data_integration_id)
        prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id,
                                                    source_data=source_data)
        affected_row_count = target_adapter.write_target_data(data_integration_id=data_integration_id,
                                                              prepared_data=prepared_data)
        return affected_row_count

    def clear_data(self, data_operation_job_execution_integration_id: int, data_integration_id: int):
        is_target_truncate = self.data_integration_service.get_is_target_truncate(id=data_integration_id)

        if is_target_truncate:
            connection_adapter = self.connection_adapter_factory.get_target_adapter(
                data_integration_id=data_integration_id)
            truncate_affected_rowcount = connection_adapter.clear_data(data_integration_id)

            self.data_operation_job_execution_integration_service.create_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, affected_row=truncate_affected_rowcount)

    def get_source_data_count(self,
                              data_operation_job_execution_integration_id: int,
                              data_integration_id: int):
        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        data_count = source_adapter.get_source_data_count(data_integration_id=data_integration_id)
        self.data_operation_job_execution_integration_service.update_source_data_count(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            source_data_count=data_count)
        self.data_operation_job_execution_integration_service.create_event(
            data_operation_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT, affected_row=data_count)
        return data_count

    def execute_query(self,
                      data_operation_job_execution_integration_id: int,
                      data_integration_id: int) -> int:
        target_adapter = self.connection_adapter_factory.get_target_adapter(
            data_integration_id=data_integration_id)
        affected_rowcount = target_adapter.do_target_operation(data_integration_id=data_integration_id)

        self.data_operation_job_execution_integration_service.update_source_data_count(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            source_data_count=affected_rowcount)

        self.data_operation_job_execution_integration_service.create_event(
            data_operation_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, affected_row=affected_rowcount)
        return affected_rowcount

    def update_status(self, data_operation_job_execution_id: int, data_operation_job_execution_integration_id, log: str,
                      status: StatusTypes, event_code: int,
                      is_finished: bool = False):
        self.sql_logger.info(log, job_id=data_operation_job_execution_id)
        self.data_operation_job_execution_integration_service.update_status(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            status_id=status.value, is_finished=is_finished)
        if is_finished:
            self.data_operation_job_execution_integration_service.update_log(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                log=log)
        self.data_operation_job_execution_integration_service.create_event(
            data_operation_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=event_code)
