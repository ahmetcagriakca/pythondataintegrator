from injector import inject

from domain.operation.commands.CreateExecutionCommand import CreateExecutionCommand
from domain.operation.execution.services.IntegrationExecution import IntegrationExecution
from domain.operation.execution.services.OperationCacheService import OperationCacheService
from domain.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService
from domain.operation.services.DataOperationJobService import DataOperationJobService
from infrastructor.data.decorators.TransactionHandler import transaction_handler
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.enums.StatusTypes import StatusTypes
from models.enums.events import EVENT_EXECUTION_STARTED, EVENT_EXECUTION_FINISHED


class OperationExecution(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 operation_cache_service: OperationCacheService,
                 create_execution_command: CreateExecutionCommand,
                 data_operation_job_execution_service: DataOperationJobExecutionService,
                 integration_execution: IntegrationExecution):
        self.create_execution_command = create_execution_command
        self.operation_cache_service = operation_cache_service
        self.integration_execution = integration_execution
        self.data_operation_job_execution_service = data_operation_job_execution_service
        self.sql_logger = sql_logger

    def __start_execution(self, data_operation_id: int, data_operation_job_execution_id: int):
        data_operation_integrations = self.operation_cache_service.get_data_operation_integrations_by_data_operation_id(
            data_operation_id=data_operation_id)

        for data_operation_integration in data_operation_integrations:
            self.integration_execution.start(
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_integration_id=data_operation_integration.Id)

    @transaction_handler
    def start(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int):
        self.operation_cache_service.create(data_operation_id=data_operation_id)
        if data_operation_job_execution_id is None:
            data_operation_job_execution_id = self.create_execution_command.execute(data_operation_id=data_operation_id,
                                                                                    job_id=job_id)
        data_operation_name = self.operation_cache_service.get_data_operation_name(data_operation_id=data_operation_id)
        try:

            self.__event(data_operation_job_execution_id=data_operation_job_execution_id,
                         log=f'{data_operation_name} data operation is begin',
                         status=StatusTypes.Start,
                         event_code=EVENT_EXECUTION_STARTED)
            self.__start_execution(data_operation_id=data_operation_id,
                                   data_operation_job_execution_id=data_operation_job_execution_id)
            self.__event(data_operation_job_execution_id=data_operation_job_execution_id,
                         log=f'{data_operation_name} data operation is completed',
                         status=StatusTypes.Finish,
                         event_code=EVENT_EXECUTION_FINISHED,
                         is_finished=True)

            return "Operation Completed"
        except Exception as ex:

            self.__event(data_operation_job_execution_id=data_operation_job_execution_id,
                         log=f'{data_operation_name} data operation has error. Error: {ex}',
                         status=StatusTypes.Error,
                         event_code=EVENT_EXECUTION_FINISHED,
                         is_finished=True)
            raise

    def __event(self, data_operation_job_execution_id, log: str, status: StatusTypes, event_code: int,
                is_finished: bool = False):
        self.sql_logger.info(log,
                             job_id=data_operation_job_execution_id)
        self.data_operation_job_execution_service.create_event(
            data_operation_execution_id=data_operation_job_execution_id,
            event_code=event_code)
        self.data_operation_job_execution_service.update_status(
            data_operation_job_execution_id=data_operation_job_execution_id,
            status_id=status.value, is_finished=is_finished)
        if is_finished:
            self.data_operation_job_execution_service.send_data_operation_finish_mail(data_operation_job_execution_id)
