import time
from datetime import datetime

from injector import inject
from pdip.configuration.models.application import ApplicationConfig
from pdip.configuration.models.database import DatabaseConfig
from pdip.configuration.services import ConfigService
from pdip.cqrs import ICommandHandler, Dispatcher
from pdip.data.decorators import transactionhandler
from pdip.delivery import EmailProvider
from pdip.logging.loggers.sql import SqlLogger

from scheduler.application.CreateExecution.CreateExecutionCommand import CreateExecutionCommand
from scheduler.application.SendSchedulerErrorMail.SendSchedulerErrorMailCommand import SendSchedulerErrorMailCommand
from scheduler.application.StartJob.StartJobCommand import StartJobCommand
from scheduler.application.StartProcess.StartProcessCommand import StartProcessCommand


class StartJobCommandHandler(ICommandHandler[StartJobCommand]):
    @inject
    def __init__(self,
                 database_config: DatabaseConfig,
                 logger: SqlLogger,
                 email_provider: EmailProvider,
                 application_config: ApplicationConfig,
                 config_service: ConfigService,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher
        self.config_service = config_service
        self.application_config = application_config
        self.email_provider = email_provider
        self.logger = logger
        self.database_config = database_config

    @transactionhandler
    def handle(self, command: StartJobCommand):
        """
        :param command: Ap Scheduler Job Id
        :return:
        """
        data_operation_job_execution_id = None

        try:
            start = time.time()
            start_datetime = datetime.now()

            service_command = CreateExecutionCommand(DataOperationId=command.DataOperationId, JobId=command.JobId)
            data_operation_job_execution_id = self.dispatcher.dispatch(service_command)
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
            service_command = SendSchedulerErrorMailCommand(JobId=command.JobId,
                                                            DataOperationJobExecutionId=data_operation_job_execution_id,
                                                            Exception=ex)
            self.dispatcher.dispatch(service_command)
            self.logger.info(
                f"{command.DataOperationId}-{command.JobId} Scheduler getting error. Error:{ex}",
                job_id=data_operation_job_execution_id)
            raise
