import time
from datetime import datetime

from injector import inject
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.decorators import transactionhandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency.container import DependencyContainer
from pdip.exceptions import OperationalException
from pdip.integrator.domain.enums import StatusTypes
from pdip.integrator.domain.enums.events import EVENT_EXECUTION_INITIALIZED
from pdip.logging.loggers.sql import SqlLogger

from src.application.SendSchedulerErrorMail.SendSchedulerErrorMailCommand import SendSchedulerErrorMailCommand
from src.application.StartJob.StartJobCommand import StartJobCommand
from src.application.StartProcess.StartProcessCommand import StartProcessCommand
from src.domain.common.OperationEvent import OperationEvent
from src.domain.common.Status import Status
from src.domain.operation.DataOperationJob import DataOperationJob
from src.domain.operation.DataOperationJobExecution import DataOperationJobExecution
from src.domain.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent


class StartJobCommandHandler(ICommandHandler[StartJobCommand]):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.logger = logger

    def handle(self, command: StartJobCommand):
        """
        :param command: Ap Scheduler Job Id
        :return:
        """
        data_operation_job_execution_id = None

        try:
            start = time.time()
            start_datetime = datetime.now()

            data_operation_job_execution_id = self.create_execution(data_operation_id=command.DataOperationId,
                                                                    ap_scheduler_job_id=command.JobId)
            self.logger.info(f"{command.DataOperationId}-{command.JobId} Scheduler Started ",
                             job_id=data_operation_job_execution_id)
            self.logger.info(
                f"{command.DataOperationId}-{command.JobId} Scheduler execution created ",
                job_id=data_operation_job_execution_id)

            service_command = StartProcessCommand(DataOperationId=command.DataOperationId, JobId=command.JobId,
                                                  DataOperationJobExecutionId=data_operation_job_execution_id)
            self.dispatcher.dispatch(service_command)

            end_datetime = datetime.now()
            end = time.time()
            self.logger.info(
                f"{command.DataOperationId}-{command.JobId} Scheduler Finished. Start :{start_datetime}-End :{end_datetime}-ElapsedTime :{end - start}",
                job_id=data_operation_job_execution_id)
        except Exception as ex:
            if data_operation_job_execution_id is not None:
                service_command = SendSchedulerErrorMailCommand(JobId=command.JobId,
                                                                DataOperationJobExecutionId=data_operation_job_execution_id,
                                                                Exception=ex)
                self.dispatcher.dispatch(service_command)
                self.logger.exception(ex,
                                      f"{command.DataOperationId}-{command.JobId} Scheduler getting error.",
                                      job_id=data_operation_job_execution_id)
            else:

                self.logger.exception(ex,
                                      f"{command.DataOperationId}-{command.JobId} Scheduler getting error.")
            raise

    @transactionhandler
    def create_execution(self, data_operation_id, ap_scheduler_job_id):
        repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
        data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
            data_operation_id=data_operation_id,
            ap_scheduler_job_id=ap_scheduler_job_id
        )
        if data_operation_job is None:
            error = f'{data_operation_id}-{ap_scheduler_job_id} Data operation job not found'
            self.logger.error(error)
            raise OperationalException(error)

        status = repository_provider.get(Status).first(Id=StatusTypes.Initialized.value)
        data_operation_job_execution = DataOperationJobExecution(
            DataOperationJob=data_operation_job,
            Status=status,
            Definition=data_operation_job.DataOperation.Definition)
        repository_provider.get(DataOperationJobExecution).insert(data_operation_job_execution)
        operation_event = repository_provider.get(OperationEvent).first(Code=EVENT_EXECUTION_INITIALIZED)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        repository_provider.get(DataOperationJobExecutionEvent).insert(data_operation_job_execution_event)
        result = data_operation_job_execution.Id
        return result

    def get_data_operation_job_by_operation_and_job_id(self, data_operation_id: int,
                                                       ap_scheduler_job_id: int, retry: int = 0) -> DataOperationJob:
        repository_provider = DependencyContainer.Instance.get(RepositoryProvider)
        data_operation_job = repository_provider.get(DataOperationJob).first(
            IsDeleted=0,
            DataOperationId=data_operation_id,
            ApSchedulerJobId=ap_scheduler_job_id
        )
        if data_operation_job is None and retry < 3:
            time.sleep(2)
            data_operation_job = self.get_data_operation_job_by_operation_and_job_id(
                data_operation_id=data_operation_id,
                ap_scheduler_job_id=ap_scheduler_job_id,
                retry=retry + 1
            )

        return data_operation_job
