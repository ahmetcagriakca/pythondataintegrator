from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.operation.adapters.ExecuteAdapter import ExecuteAdapter
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.enums.events import EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY


class ExecuteQueryAdapter(ExecuteAdapter, IScoped):

    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 connection_provider: ConnectionProvider,
                 data_integration_service: DataIntegrationService,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService):
        super().__init__(
            raise_exception=False,
            sql_logger=sql_logger,
            connection_provider=connection_provider,
            data_integration_service=data_integration_service,
            data_integration_connection_service=data_integration_connection_service,
            data_operation_integration_service=data_operation_integration_service,
            data_operation_job_execution_integration_service=data_operation_job_execution_integration_service)
        self.connection_provider = connection_provider
        self.data_integration_connection_service = data_integration_connection_service
        self.data_integration_service = data_integration_service
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service
        self.data_operation_integration_service = data_operation_integration_service

    def _execute(self, data_operation_integration_id: int, data_operation_job_execution_id: int,
                 data_operation_job_execution_integration_id: int) -> int:
        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        data_integration_id = data_operation_integration.DataIntegration.Id
        self._clear_data(data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                         data_integration_id=data_integration_id)
        affected_rowcount = self.execute_query(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_integration_id=data_integration_id)
        return affected_rowcount

    def _get_start_log(self, data_integration_id: int):
        return f"integration run query started"

    def _get_finish_log(self, data_integration_id: int, data_count: int):
        return f"integration run query finished. (affected row count:{data_count})"

    def _get_error_log(self, data_integration_id: int):
        return f"integration run query getting error."

    def execute_query(self,
                      data_operation_job_execution_integration_id: int,
                      data_integration_id: int) -> int:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        target_connection_manager = self.connection_provider.get_connection_manager(
            connection=target_connection.Connection)

        affected_rowcount = target_connection_manager.execute(query=target_connection.Query)

        self.data_operation_job_execution_integration_service.update_source_data_count(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            source_data_count=affected_rowcount)

        self.data_operation_job_execution_integration_service.create_event(
            data_operation_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, affected_row=affected_rowcount)
        return affected_rowcount
