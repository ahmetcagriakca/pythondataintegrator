from injector import inject
from pdip.dependency import IScoped
from pdip.logging.loggers.database import SqlLogger

from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationStrategy import \
    ExecuteIntegrationStrategy
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.execution.services.OperationCacheService import OperationCacheService


class ExecuteIntegrationSerial(ExecuteIntegrationStrategy, IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 operation_cache_service: OperationCacheService,
                 integration_execution_service: IntegrationExecutionService):
        self.operation_cache_service = operation_cache_service
        self.integration_execution_service = integration_execution_service
        self.sql_logger = sql_logger

    def execute(self,
                data_operation_job_execution_id: int,
                data_operation_job_execution_integration_id: int,
                data_operation_integration_id: int) -> int:
        try:
            data_operation_integration = self.operation_cache_service.get_data_operation_integration_by_id(
                data_operation_integration_id=data_operation_integration_id)
            data_integration_id = data_operation_integration.DataIntegrationId
            limit = data_operation_integration.Limit
            total_row_count = self.integration_execution_service.start_integration_with_paging(
                data_integration_id=data_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                limit=limit)
            return total_row_count
        except Exception as ex:
            self.sql_logger.error(f"Integration getting error.Error:{ex}", job_id=data_operation_job_execution_id)
            raise
