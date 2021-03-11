from injector import inject

from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.operation.adapters.ExecuteAdapter import ExecuteAdapter
from domain.operation.adapters.ExecuteIntegrationService import ExecuteIntegrationService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from domain.process.services.ProcessService import ProcessService
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.enums.events import EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION, \
    EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT


class ExecuteOperationAdapter(ExecuteAdapter, IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 process_service: ProcessService,
                 data_integration_service: DataIntegrationService,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 data_integration_column_service: DataIntegrationColumnService,
                 execute_integration_service: ExecuteIntegrationService,
                 connection_provider: ConnectionProvider):
        super().__init__(
            raise_exception=True,
            sql_logger=sql_logger,
            connection_provider=connection_provider,
            data_integration_service=data_integration_service,
            data_integration_connection_service=data_integration_connection_service,
            data_operation_integration_service=data_operation_integration_service,
            data_operation_job_execution_integration_service=data_operation_job_execution_integration_service)
        self.execute_integration_service = execute_integration_service
        self.process_service = process_service
        self.sql_logger = sql_logger
        self.connection_provider = connection_provider
        self.data_integration_service = data_integration_service
        self.data_integration_column_service = data_integration_column_service
        self.data_integration_connection_service = data_integration_connection_service
        self.data_operation_integration_service = data_operation_integration_service
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service

    def _execute(self,
                 data_operation_integration_id: int,
                 data_operation_job_execution_id: int,
                 data_operation_job_execution_integration_id: int) -> int:
        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        data_integration_id = data_operation_integration.DataIntegrationId
        data_count = self.get_source_data_count(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_integration_id=data_integration_id)
        self._clear_data(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_integration_id=data_integration_id)
        affected_row_count = self.execute_operation(
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            data_operation_integration_id=data_operation_integration_id,
            data_count=data_count)
        if affected_row_count < 0:
            affected_row_count = data_count
        return affected_row_count

    def _get_start_log(self, data_integration_id: int):
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        return f"{target_connection.Schema}.{target_connection.TableName} integration execute operation started"

    def _get_finish_log(self, data_integration_id: int, data_count: int):
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        return f"{target_connection.Schema}.{target_connection.TableName} integration execute operation finished. (Source Data Count:{data_count})"

    def _get_error_log(self, data_integration_id: int):
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        return f"{target_connection.Schema}.{target_connection.TableName} integration execute operation getting error."

    def get_source_data_count(self,
                              data_operation_job_execution_integration_id: int,
                              data_integration_id: int):
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)

        source_connection_manager = self.connection_provider.get_connection_manager(
            connection=source_connection.Connection)
        data_count = source_connection_manager.get_table_count(source_connection.Query)
        self.data_operation_job_execution_integration_service.update_source_data_count(
            data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
            source_data_count=data_count)
        self.data_operation_job_execution_integration_service.create_event(
            data_operation_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_GET_SOURCE_DATA_COUNT, affected_row=data_count)
        return data_count

    def execute_operation(self,
                          data_operation_job_execution_id: int,
                          data_operation_job_execution_integration_id: int,
                          data_operation_integration_id: int,
                          data_count: int) -> int:
        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        data_operation_integration_order = data_operation_integration.Order
        limit = data_operation_integration.Limit
        process_count = data_operation_integration.ProcessCount
        data_integration_code = data_operation_integration.DataIntegration.Code
        if limit != 0:
            if process_count > 1:
                self.sql_logger.info(
                    f"{data_operation_integration_order}-{data_integration_code} - operation will execute parallel. {process_count}-{limit}",
                    job_id=data_operation_job_execution_id)
                affected_row_count = self.execute_integration_service.start_parallel_process(
                    data_operation_job_execution_id=data_operation_job_execution_id,
                    data_operation_integration_id=data_operation_integration_id,
                    data_count=data_count)

            else:
                self.sql_logger.info(
                    f"{data_operation_integration_order}-{data_integration_code} - operation will execute serial. {limit}",
                    job_id=data_operation_job_execution_id)

                affected_row_count = self.execute_integration_service.start_serial_process(
                    data_operation_integration_id=data_operation_integration_id,
                    data_count=data_count)

        self.data_operation_job_execution_integration_service.create_event(
            data_operation_execution_integration_id=data_operation_job_execution_integration_id,
            event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION, affected_row=data_count)
        return affected_row_count
