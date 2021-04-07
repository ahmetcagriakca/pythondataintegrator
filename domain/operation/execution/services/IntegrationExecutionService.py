from queue import Queue
from typing import List

from injector import inject
from pandas import DataFrame, notnull
import pandas as pd
from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.operation.execution.adapters.connection.ConnectionAdapterFactory import ConnectionAdapterFactory
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
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

    def start_source_data_operation(self,
                                    data_integration_id: int,
                                    data_operation_job_execution_integration_id: int,
                                    limit: int,
                                    process_count: int,
                                    data_queue: Queue,
                                    data_result_queue: Queue):

        source_adapter = self.connection_adapter_factory.get_source_adapter(data_integration_id=data_integration_id)
        source_adapter.start_source_data_operation(data_integration_id=data_integration_id,
                                                   data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                                                   limit=limit,
                                                   process_count=process_count,
                                                   data_queue=data_queue,
                                                   data_result_queue=data_result_queue)

    def start_execute_integration(self,
                                  data_integration_id: int,
                                  data_operation_job_execution_integration_id: int,
                                  data: DataFrame):
        target_adapter = self.connection_adapter_factory.get_target_adapter(data_integration_id=data_integration_id)
        source_data = data.where(notnull(data), None)
        source_data = source_data.replace({pd.NaT: None})

        prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id, source_data=source_data)
        target_adapter.write_target_data(data_integration_id=data_integration_id, prepared_data=prepared_data)

    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> List[any]:
        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        source_data = source_adapter.get_source_data(data_integration_id=data_integration_id,
                                                     paging_modifier=paging_modifier)
        return source_data

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
