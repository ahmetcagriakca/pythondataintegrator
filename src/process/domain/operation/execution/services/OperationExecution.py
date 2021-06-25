from injector import inject

from domain.operation.execution.services.IntegrationExecution import IntegrationExecution
from domain.operation.services.DataOperationIntegrationService import DataOperationIntegrationService
from domain.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService
from domain.operation.services.DataOperationJobService import DataOperationJobService
from domain.operation.services.DataOperationService import DataOperationService
from IocManager import IocManager
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
                 data_operation_service: DataOperationService,
                 data_operation_integration_service: DataOperationIntegrationService,
                 data_operation_job_service: DataOperationJobService,
                 data_operation_job_execution_service: DataOperationJobExecutionService,
                 integration_execution: IntegrationExecution):
        self.integration_execution = integration_execution
        self.data_operation_integration_service = data_operation_integration_service
        self.data_operation_job_service = data_operation_job_service
        self.data_operation_job_execution_service = data_operation_job_execution_service
        self.data_operation_service = data_operation_service
        self.sql_logger = sql_logger

    def __start_execution(self, data_operation_id: int, data_operation_job_execution_id: int):
        data_operation_integrations = self.data_operation_integration_service.get_all_by_data_operation_id(
            data_operation_id=data_operation_id).order_by("Order").all()
        if data_operation_integrations is None or len(data_operation_integrations) == 0:
            self.sql_logger.info(f'Data operation has no data_integration ', job_id=data_operation_job_execution_id)
            return None

        for data_operation_integration in data_operation_integrations:
            self.integration_execution.start(
                data_operation_job_execution_id=data_operation_job_execution_id,
                data_operation_integration_id=data_operation_integration.Id)

    @transaction_handler
    def start(self, data_operation_id: int, job_id: int, data_operation_job_execution_id: int):
        if data_operation_job_execution_id is None:
            self.__check(data_operation_id=data_operation_id, job_id=job_id)
            data_operation_job_execution = self.__create(data_operation_id=data_operation_id,
                                                         job_id=job_id)
            data_operation_job_execution_id = data_operation_job_execution.Id
        data_operation_name = self.data_operation_service.get_name(id=data_operation_id)
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

    def __check(self, data_operation_id: int, job_id: int):
        data_operation = self.data_operation_service.get_by_id(id=data_operation_id)
        if data_operation is None:
            error = f'{data_operation_id}-{job_id} Data operation not found'
            self.sql_logger.error(error)
            return OperationalException(error)

        data_operation_job = self.data_operation_job_service.get_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        if data_operation_job is None:
            error = f'{data_operation_id}-{job_id} Data operation job not found'
            self.sql_logger.error(error)
            return OperationalException(error)

    def __create(self, data_operation_id: int, job_id: int):
        data_operation_job = self.data_operation_job_service.get_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            job_id=job_id)
        data_operation_job_execution = self.data_operation_job_execution_service.create(
            data_operation_job=data_operation_job)
        return data_operation_job_execution

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
