from abc import ABC, abstractmethod

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionIntegrationService import \
    DataOperationJobExecutionIntegrationService
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.logging.SqlLogger import SqlLogger
from models.enums.StatusTypes import StatusTypes
from models.enums.events import EVENT_EXECUTION_INTEGRATION_STARTED, EVENT_EXECUTION_INTEGRATION_FINISHED, \
    EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE


class ExecuteAdapter(ABC):
    def __init__(self,
                 raise_exception: bool,
                 sql_logger: SqlLogger,
                 connection_provider:ConnectionProvider,
                 data_integration_service:DataIntegrationService,
                 data_integration_connection_service:DataIntegrationConnectionService,
                 data_operation_integration_service:DataOperationIntegrationService,
                 data_operation_job_execution_integration_service: DataOperationJobExecutionIntegrationService):
        self.data_operation_integration_service = data_operation_integration_service
        self.connection_provider = connection_provider
        self.data_integration_connection_service = data_integration_connection_service
        self.data_integration_service = data_integration_service
        self.raise_exception = raise_exception
        self.sql_logger = sql_logger
        self.data_operation_job_execution_integration_service = data_operation_job_execution_integration_service

    def _clear_data(self, data_operation_job_execution_integration_id: int, data_integration_id: int):
        is_target_truncate = self.data_integration_service.get_is_target_truncate(id=data_integration_id)

        if is_target_truncate:
            target_connection = self.data_integration_connection_service.get_target_connection(
                data_integration_id=data_integration_id)
            target_connection_manager = self.connection_provider.get_connection_manager(
                connection=target_connection.Connection)
            truncate_affected_rowcount = target_connection_manager.truncate_table(schema=target_connection.Schema,
                                                                                  table=target_connection.TableName)

            self.data_operation_job_execution_integration_service.create_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, affected_row=truncate_affected_rowcount)

    def _event(self, data_operation_job_execution_id: int, data_operation_job_execution_integration_id, log: str,
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

    @abstractmethod
    def _get_start_log(self, data_integration_id: int):
        pass

    @abstractmethod
    def _get_finish_log(self, data_integration_id: int, data_count: int):
        pass

    @abstractmethod
    def _get_error_log(self, data_integration_id: int):
        pass

    @abstractmethod
    def _execute(self,
                 data_operation_integration_id: int,
                 data_operation_job_execution_id: int,
                 data_operation_job_execution_integration_id: int):
        pass

    def start_execute(self, data_operation_integration_id: int, data_operation_job_execution_id: int):
        data_operation_integration = self.data_operation_integration_service.get_by_id(
            id=data_operation_integration_id)
        data_operation_job_execution_integration = self.data_operation_job_execution_integration_service.create(
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_integration=data_operation_integration)
        data_operation_job_execution_integration_id = data_operation_job_execution_integration.Id
        data_operation_integration_order = data_operation_integration.Order
        data_integration_code = data_operation_integration.DataIntegration.Code
        data_integration_id = data_operation_integration.DataIntegration.Id
        try:
            start_log = self._get_start_log(data_integration_id=data_integration_id)
            log = f"{data_operation_integration_order}-{data_integration_code} - {start_log}"
            self._event(data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                        data_operation_job_execution_id=data_operation_job_execution_id,
                        log=log,
                        status=StatusTypes.Start,
                        event_code=EVENT_EXECUTION_INTEGRATION_STARTED)
            data_count = self._execute(
                data_operation_integration_id=data_operation_integration_id,
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id)

            finish_log = self._get_finish_log(data_integration_id=data_integration_id,data_count=data_count)
            log = f"{data_operation_integration_order}-{data_integration_code} - {finish_log}"
            self._event(data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                        data_operation_job_execution_id=data_operation_job_execution_id,
                        log=log,
                        status=StatusTypes.Finish,
                        event_code=EVENT_EXECUTION_INTEGRATION_FINISHED,
                        is_finished=True)

        except Exception as ex:
            error_log = self._get_error_log(data_integration_id=data_integration_id)
            log = f"{data_operation_integration_order}-{data_integration_code} - {error_log} Error:{ex}"
            self._event(data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                        data_operation_job_execution_id=data_operation_job_execution_id,
                        log=log,
                        status=StatusTypes.Error,
                        event_code=EVENT_EXECUTION_INTEGRATION_FINISHED,
                        is_finished=True)
            if self.raise_exception:
                raise
