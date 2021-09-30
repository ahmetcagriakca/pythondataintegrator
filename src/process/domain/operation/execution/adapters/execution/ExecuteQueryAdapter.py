from injector import inject

from domain.operation.execution.adapters.execution.ExecuteAdapter import ExecuteAdapter
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from infrastructure.dependency.scopes import IScoped


class ExecuteQueryAdapter(ExecuteAdapter, IScoped):

    @inject
    def __init__(self,
                 operation_cache_service: OperationCacheService,
                 integration_execution_service: IntegrationExecutionService):
        self.operation_cache_service = operation_cache_service
        self.integration_execution_service = integration_execution_service

    def execute(self, data_operation_integration_id: int, data_operation_job_execution_id: int,
                data_operation_job_execution_integration_id: int) -> int:
        data_operation_integration = self.operation_cache_service.get_data_operation_integration_by_id(
            data_operation_integration_id=data_operation_integration_id)
        data_integration_id = data_operation_integration.DataIntegration.Id
        self.integration_execution_service.clear_data(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_integration_id=data_integration_id)
        affected_rowcount = self.integration_execution_service.execute_query(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_integration_id=data_integration_id)
        return affected_rowcount

    def get_start_log(self, data_integration_id: int):
        return f"integration run query started"

    def get_finish_log(self, data_integration_id: int, data_count: int):
        return f"integration run query finished. (affected row count:{data_count})"

    def get_error_log(self, data_integration_id: int):
        return f"integration run query getting error."

    def check_error_raise(self) -> bool:
        return True
