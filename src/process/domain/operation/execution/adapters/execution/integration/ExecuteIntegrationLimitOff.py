from injector import inject

from domain.operation.execution.adapters.execution.integration.ExecuteIntegrationStrategy import ExecuteIntegrationStrategy
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from infrastructure.dependency.scopes import IScoped
from infrastructure.logging.SqlLogger import SqlLogger


class ExecuteIntegrationLimitOff(ExecuteIntegrationStrategy, IScoped):
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
            total_row_count = self.integration_execution_service.start_integration(
                data_integration_id=data_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id)

            return total_row_count
        except Exception as ex:
            self.sql_logger.error(f"Integration getting error.Error:{ex}", job_id=data_operation_job_execution_id)
            raise
