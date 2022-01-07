from injector import inject
from pdip.configuration.models.database import DatabaseConfig
from pdip.configuration.services import ConfigService
from pdip.cqrs import ICommandHandler
from pdip.data.decorators import transactionhandler
from pdip.data.repository import RepositoryProvider
from pdip.delivery import EmailProvider
from pdip.logging.loggers.sql import SqlLogger
from pdip.configuration.models.application import ApplicationConfig

from src.application.SendMissMail.SendMissMailCommand import SendMissMailCommand
from src.domain.aps.ApSchedulerJob import ApSchedulerJob
from src.domain.operation.DataOperationJob import DataOperationJob


class SendMissMailCommandHandler(ICommandHandler[SendMissMailCommand]):
    @inject
    def __init__(self,
                 database_config: DatabaseConfig,
                 logger: SqlLogger,
                 email_provider: EmailProvider,
                 application_config: ApplicationConfig,
                 config_service: ConfigService,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_service = config_service
        self.application_config = application_config
        self.email_provider = email_provider
        self.logger = logger
        self.database_config = database_config

    @transactionhandler
    def handle(self, command: SendMissMailCommand):
        try:
            repository_provider = RepositoryProvider(database_config=self.database_config,
                                                     database_session_manager=None)
            data_operation_job_repository = repository_provider.get(DataOperationJob)
            ap_scheduler_job_repository = repository_provider.get(ApSchedulerJob)
            ap_scheduler_job = ap_scheduler_job_repository.first(JobId=command.JobId)
            data_operation_job = data_operation_job_repository.first(IsDeleted=0,
                                                                     ApSchedulerJobId=ap_scheduler_job.Id)
            if data_operation_job is not None:
                next_run_time = ap_scheduler_job.NextRunTime
                operation_contacts = []
                for contact in data_operation_job.DataOperation.Contacts:
                    if contact.IsDeleted == 0:
                        operation_contacts.append(contact.Email)

                default_contacts = self.config_service.get_config_by_name("DataOperationDefaultContact")
                if default_contacts is not None and default_contacts != '':
                    default_contacts_emails = default_contacts.split(",")
                    for default_contact in default_contacts_emails:
                        if default_contact is not None and default_contact != '':
                            operation_contacts.append(default_contact)
                if operation_contacts is None:
                    self.logger.info(f'{data_operation_job.DataOperation.Name} mail sending contact not found')
                    return

                data_operation_name = data_operation_job.DataOperation.Name
                subject = f"Job Missed"
                subject = subject + f": {self.application_config.environment} » {data_operation_name}"

                if next_run_time is not None:
                    next_run_time_text = f"{next_run_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
                else:
                    next_run_time_text = ''

                if data_operation_job.StartDate is not None:
                    job_start_time_text = f"{data_operation_job.StartDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
                else:
                    job_start_time_text = ''

                body = f'''
                              Scheduled job missed  
                              </br>
                              Job start time : {job_start_time_text}
                              </br>
                              Job next run time : {next_run_time_text}
                              '''
                try:
                    self.email_provider.send(operation_contacts, subject, body)
                except Exception as ex:
                    self.logger.error(f"Error on mail sending. Error:{ex}")
        except Exception as ex:
            self.logger.error(f"Miss mail sending getting error. Error:{ex}")
