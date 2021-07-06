from queue import Queue
from time import time
from typing import List

from injector import inject
from pandas import notnull
import pandas as pd
from domain.operation.execution.adapters.connection.ConnectionAdapterFactory import ConnectionAdapterFactory
from domain.operation.execution.services.OperationCacheService import OperationCacheService
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
                 operation_cache_service: OperationCacheService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService,
                 connection_adapter_factory: ConnectionAdapterFactory):
        self.operation_cache_service = operation_cache_service
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

    def start_integration(self,
                          data_integration_id: int,
                          limit: int,
                          data_operation_job_execution_id: int,
                          data_operation_job_execution_integration_id: int):

        target_adapter = self.connection_adapter_factory.get_target_adapter(data_integration_id=data_integration_id)
        data_count = self.get_source_data_count(
            data_integration_id=data_integration_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id)
        if data_count > 0:
            paging_modifiers = self.get_paging_modifiers(data_count=data_count, limit=limit)
            for paging_modifier in paging_modifiers:
                start_time = time()
                source_data = self.get_source_data(data_integration_id=data_integration_id,
                                                   paging_modifier=paging_modifier)
                # df = DataFrame(source_data)
                task_id = paging_modifier.Id
                start = paging_modifier.Start
                end = paging_modifier.End
                self.sql_logger.info(f"0-data readed:{task_id}-{start}-{end} process got a new task",
                                     job_id=data_operation_job_execution_id)
                prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id,
                                                            source_data=source_data)
                target_adapter.write_target_data(data_integration_id=data_integration_id, prepared_data=prepared_data)
                end_time = time()
                self.sql_logger.info(
                    f"0-data readed:{task_id}-{start}-{end}  process finished task. time:{end_time - start_time}",
                    job_id=data_operation_job_execution_id)
        return data_count

    def start_integration_temp(self,
                               data_integration_id: int,
                               limit: int,
                               data_operation_job_execution_id: int,
                               data_operation_job_execution_integration_id: int):

        source_adapter = self.connection_adapter_factory.get_source_adapter(data_integration_id=data_integration_id)
        target_adapter = self.connection_adapter_factory.get_target_adapter(data_integration_id=data_integration_id)
        task_id = 0
        total_data_count = 0
        for data in source_adapter.read_data(data_integration_id=data_integration_id,
                                             limit=limit):
            start_time = time()
            source_data = data.where(notnull(data), None)
            source_data = source_data.replace({pd.NaT: None})
            task_id = task_id + 1
            data_count = len(source_data)
            total_data_count = total_data_count + data_count
            start = total_data_count - data_count
            end = total_data_count
            self.sql_logger.info(f"0-data readed:{task_id}-{start}-{end} process got a new task",
                                 job_id=data_operation_job_execution_id)
            prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id,
                                                        source_data=source_data)
            target_adapter.write_target_data(data_integration_id=data_integration_id, prepared_data=prepared_data)
            end_time = time()
            self.sql_logger.info(
                f"0-data readed:{task_id}-{start}-{end}  process finished task. time:{end_time - start_time}",
                job_id=data_operation_job_execution_id)
        return total_data_count

    def start_execute_integration(self,
                                  data_integration_id: int,
                                  data_operation_job_execution_id: int,
                                  data_operation_job_execution_integration_id: int,
                                  paging_modifier: PagingModifier,
                                  source_data: any):
        if source_data is None:
            source_data = self.get_source_data(data_integration_id=data_integration_id, paging_modifier=paging_modifier)
        target_adapter = self.connection_adapter_factory.get_target_adapter(data_integration_id=data_integration_id)
        prepared_data = target_adapter.prepare_data(data_integration_id=data_integration_id, source_data=source_data)
        target_adapter.write_target_data(data_integration_id=data_integration_id, prepared_data=prepared_data)
        return len(source_data)

    def get_source_data(self, data_integration_id: int, paging_modifier: PagingModifier) -> List[any]:
        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        source_data = source_adapter.get_source_data(data_integration_id=data_integration_id,
                                                     paging_modifier=paging_modifier)
        return source_data

    def clear_data(self, data_operation_job_execution_integration_id: int, data_integration_id: int):
        is_target_truncate = self.operation_cache_service.get_data_integration_by_id(
            data_integration_id=data_integration_id).IsTargetTruncate

        if is_target_truncate:
            connection_adapter = self.connection_adapter_factory.get_target_adapter(
                data_integration_id=data_integration_id)
            truncate_affected_rowcount = connection_adapter.clear_data(data_integration_id)

            self.data_operation_job_execution_integration_service.create_event(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, affected_row=truncate_affected_rowcount)

    def get_source_data_count(self,
                              data_operation_job_execution_integration_id: int,
                              data_integration_id: int):
        source_adapter = self.connection_adapter_factory.get_source_adapter(
            data_integration_id=data_integration_id)
        data_count = source_adapter.get_source_data_count(data_integration_id=data_integration_id)
        self.data_operation_job_execution_integration_service.create_event(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT, affected_row=data_count)
        self.data_operation_job_execution_integration_service.update_source_data_count(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            source_data_count=data_count)
        return data_count

    def execute_query(self,
                      data_operation_job_execution_integration_id: int,
                      data_integration_id: int) -> int:
        target_adapter = self.connection_adapter_factory.get_target_adapter(
            data_integration_id=data_integration_id)
        affected_rowcount = target_adapter.do_target_operation(data_integration_id=data_integration_id)

        self.data_operation_job_execution_integration_service.create_event(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, affected_row=affected_rowcount)
        # self.data_operation_job_execution_integration_service.update_source_data_count(
        #     data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
        #     source_data_count=affected_rowcount)

        return affected_rowcount

    def update_status(self, data_operation_job_execution_id: int, data_operation_job_execution_integration_id, log: str,
                      status: StatusTypes, event_code: int,
                      is_finished: bool = False):
        self.sql_logger.info(log, job_id=data_operation_job_execution_id)
        self.data_operation_job_execution_integration_service.create_event(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=event_code)
        self.data_operation_job_execution_integration_service.update_status(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            status_id=status.value, is_finished=is_finished)
        if is_finished:
            self.data_operation_job_execution_integration_service.update_log(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                log=log)
