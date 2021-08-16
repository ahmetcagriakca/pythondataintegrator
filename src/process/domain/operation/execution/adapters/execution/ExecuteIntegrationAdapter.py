from injector import inject

from domain.operation.execution.adapters.execution.ExecuteAdapter import ExecuteAdapter
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.execution.processes.ExecuteIntegrationProcess import ExecuteIntegrationProcess
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from infrastructure.dependency.scopes import IScoped
from infrastructure.logging.SqlLogger import SqlLogger
from models.enums.events import EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION


class ExecuteIntegrationAdapter(ExecuteAdapter, IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 operation_cache_service: OperationCacheService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService,
                 integration_execution_service: IntegrationExecutionService,
                 execute_integration_process: ExecuteIntegrationProcess,
                 ):
        self.operation_cache_service = operation_cache_service
        self.execute_integration_process = execute_integration_process
        self.integration_execution_service = integration_execution_service
        self.sql_logger = sql_logger
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service

    def execute(self,
                data_operation_integration_id: int,
                data_operation_job_execution_id: int,
                data_operation_job_execution_integration_id: int) -> int:
        data_operation_integration = self.operation_cache_service.get_data_operation_integration_by_id(
            data_operation_integration_id=data_operation_integration_id)
        data_integration_id = data_operation_integration.DataIntegrationId
        self.integration_execution_service.clear_data(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_integration_id=data_integration_id)
        affected_row_count = self.execute_integration(
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_operation_integration_id=data_operation_integration_id)
        return affected_row_count

    def get_start_log(self, data_integration_id: int):

        target_connection = self.operation_cache_service.get_target_connection(data_integration_id=data_integration_id)

        if target_connection.Database is not None:
            log = f"{target_connection.Database.Schema}.{target_connection.Database.TableName} integration execute started"
        elif target_connection.File is not None:
            log = f"{target_connection.File.Folder}\\{target_connection.File.FileName} integration execute started"
        elif target_connection.Queue is not None:
            log = f"{target_connection.Queue.TopicName} integration execute started"
        else:
            log = f"Integration execute started"
        return log

    def get_finish_log(self, data_integration_id: int, data_count: int):
        target_connection = self.operation_cache_service.get_target_connection(data_integration_id=data_integration_id)
        if target_connection.Database is not None:
            log = f"{target_connection.Database.Schema}.{target_connection.Database.TableName} integration execute finished. (Source Data Count:{data_count})"
        elif target_connection.File is not None:
            log = f"{target_connection.File.Folder}\\{target_connection.File.FileName} integration execute finished. (Source Data Count:{data_count})"
        elif target_connection.Queue is not None:
            log = f"{target_connection.Queue.TopicName} integration execute finished. (Source Data Count:{data_count})"
        else:
            log = f"Integration execute finished"

        return log

    def get_error_log(self, data_integration_id: int):
        target_connection = self.operation_cache_service.get_target_connection(data_integration_id=data_integration_id)
        if target_connection.Database is not None:
            log = f"{target_connection.Database.Schema}.{target_connection.Database.TableName} integration execute getting error"
        elif target_connection.File is not None:
            log = f"{target_connection.File.Folder}\\{target_connection.File.FileName} integration execute getting error"
        elif target_connection.Queue is not None:
            log = f"{target_connection.Queue.TopicName} integration execute getting error"
        else:
            log = f"Integration execute getting error"
        return log

    def check_error_raise(self) -> bool:
        return True

    def execute_integration(self,
                            data_operation_job_execution_id: int,
                            data_operation_job_execution_integration_id: int,
                            data_operation_integration_id: int) -> int:

        data_operation_integration = self.operation_cache_service.get_data_operation_integration_by_id(data_operation_integration_id=data_operation_integration_id)
        limit = data_operation_integration.Limit
        process_count = data_operation_integration.ProcessCount

        data_operation_integration_order = data_operation_integration.Order
        data_integration_code = data_operation_integration.DataIntegration.Code
        if limit is not None and limit > 0:
            if process_count > 1:
                self.sql_logger.info(
                    f"{data_operation_integration_order}-{data_integration_code} - integration will execute parallel. {process_count}-{limit}",
                    job_id=data_operation_job_execution_id)
            else:
                self.sql_logger.info(
                    f"{data_operation_integration_order}-{data_integration_code} - integration will execute serial. {limit}",
                    job_id=data_operation_job_execution_id)

            affected_row_count = self.execute_integration_process.start_integration_execution(
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                data_operation_integration_id=data_operation_integration_id)

            self.data_operation_job_execution_integration_service.update_source_data_count(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                source_data_count=affected_row_count)
            self.data_operation_job_execution_integration_service.create_event(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION, affected_row=affected_row_count)
        return affected_row_count
