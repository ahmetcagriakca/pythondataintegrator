from injector import inject

from domain.operation.execution.adapters.execution.ExecuteAdapter import ExecuteAdapter
from domain.operation.execution.adapters.execution.ExecuteAdapterFactory import ExecuteAdapterFactory
from domain.operation.execution.services.IntegrationExecutionService import IntegrationExecutionService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.enums.StatusTypes import StatusTypes
from models.enums.events import EVENT_EXECUTION_INTEGRATION_STARTED, EVENT_EXECUTION_INTEGRATION_FINISHED


class IntegrationExecution(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService,
                 integration_execution_service: IntegrationExecutionService,
                 execute_adapter_factory: ExecuteAdapterFactory):
        self.execute_adapter_factory = execute_adapter_factory
        self.integration_execution_service = integration_execution_service
        self.data_operation_integration_service = data_operation_integration_service
        self.sql_logger = sql_logger
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service

    def start(self, data_operation_integration_id: int, data_operation_job_execution_id: int):
        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        # Get execute_adapter before integration
        execute_adapter: ExecuteAdapter = self.execute_adapter_factory.get_execute_adapter(
            data_operation_integration.DataIntegrationId)

        data_operation_job_execution_integration = self.data_operation_job_execution_integration_service.create(
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_integration=data_operation_integration)
        data_operation_job_execution_integration_id = data_operation_job_execution_integration.Id
        data_operation_integration_order = data_operation_integration.Order
        data_integration_code = data_operation_integration.DataIntegration.Code
        data_integration_id = data_operation_integration.DataIntegration.Id

        try:
            start_log = execute_adapter.get_start_log(data_integration_id=data_integration_id)
            log = f"{data_operation_integration_order}-{data_integration_code} - {start_log}"
            self.integration_execution_service.update_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                log=log,
                status=StatusTypes.Start,
                event_code=EVENT_EXECUTION_INTEGRATION_STARTED)
            data_count = execute_adapter.execute(
                data_operation_integration_id=data_operation_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id)

            finish_log = execute_adapter.get_finish_log(data_integration_id=data_integration_id,
                                                        data_count=data_count)
            log = f"{data_operation_integration_order}-{data_integration_code} - {finish_log}"
            self.integration_execution_service.update_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                log=log,
                status=StatusTypes.Finish,
                event_code=EVENT_EXECUTION_INTEGRATION_FINISHED,
                is_finished=True)
        except Exception as ex:
            error_log = execute_adapter.get_error_log(data_integration_id=data_integration_id)
            log = f"{data_operation_integration_order}-{data_integration_code} - {error_log} Error:{ex}"
            self.integration_execution_service.update_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                log=log,
                status=StatusTypes.Error,
                event_code=EVENT_EXECUTION_INTEGRATION_FINISHED,
                is_finished=True)
            if execute_adapter.check_error_raise():
                raise
