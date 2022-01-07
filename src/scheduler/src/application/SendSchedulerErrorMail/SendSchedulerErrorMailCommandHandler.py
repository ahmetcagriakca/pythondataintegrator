from injector import inject
from pdip.configuration.models.application import ApplicationConfig
from pdip.configuration.services import ConfigService
from pdip.cqrs import ICommandHandler
from pdip.data.decorators import transactionhandler
from pdip.data.repository import RepositoryProvider
from pdip.delivery import EmailProvider
from pdip.exceptions import OperationalException
from pdip.logging.loggers.sql import SqlLogger

from src.application.SendSchedulerErrorMail.SendSchedulerErrorMailCommand import SendSchedulerErrorMailCommand
from src.domain.operation.DataOperationJob import DataOperationJob


class SendSchedulerErrorMailCommandHandler(ICommandHandler[SendSchedulerErrorMailCommand]):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 email_provider: EmailProvider,
                 application_config: ApplicationConfig,
                 config_service: ConfigService,
                 repository_provider: RepositoryProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository_provider = repository_provider
        self.config_service = config_service
        self.application_config = application_config
        self.email_provider = email_provider
        self.logger = logger

    @transactionhandler
    def handle(self, command: SendSchedulerErrorMailCommand):
        try:
            data_operation_job_repository = self.repository_provider.get(DataOperationJob)
            data_operation_job = data_operation_job_repository.first(JobId=command.JobId)
            if data_operation_job is None:
                raise OperationalException("Job definition not found")
                operation_contacts = []

            default_contacts = self.config_service.get_config_by_name("DataOperationDefaultContact")
            if default_contacts is not None and default_contacts != '':
                default_contacts_emails = default_contacts.split(",")
                for default_contact in default_contacts_emails:
                    if default_contact is not None and default_contact != '':
                        operation_contacts.append(default_contact)

            data_operation_name = data_operation_job.DataOperation.Name
            subject = f"Scheduler getting error on execution create"
            subject = subject + f": {self.application_config.environment} » {data_operation_name}"

            body = f'''
                    <p>Scheduler getting error on job</p>
                    <p>{command.Exception}<p/>
                  '''
            try:
                self.email_provider.send(operation_contacts, subject, body)
            except Exception as ex:
                self.logger.error(f"Scheduler  mail sending. Error:{ex}", job_id=command.DataOperationJobExecutionId)
        except Exception as ex:
            self.logger.error(f"Scheduler getting error. Error:{ex}", job_id=command.DataOperationJobExecutionId)
