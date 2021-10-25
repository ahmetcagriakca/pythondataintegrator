from injector import inject
from pdip.configuration.models.database import DatabaseConfig
from pdip.dependency.container import DependencyContainer
from pdip.data import RepositoryProvider
from pdip.delivery import EmailProvider
from pdip.exceptions import OperationalException
from pdip.logging.loggers.database import SqlLogger
from pdip.configuration.models.application import ApplicationConfig

from scheduler.domain.dao.operation.DataOperationJob import DataOperationJob


class SendSchedulerErrorMailCommand:
    @inject
    def __init__(self):
        self.database_config = DependencyContainer.Instance.get(DatabaseConfig)
        self.repository_provider = RepositoryProvider(database_config=self.database_config,
                                                      database_session_manager=None)
        self.sql_logger = DependencyContainer.Instance.get(SqlLogger)
        self.email_provider = DependencyContainer.Instance.get(EmailProvider)
        self.application_config = DependencyContainer.Instance.get(ApplicationConfig)

    def send(self, job_id: int, exception: Exception, data_operation_job_execution_id=None):
        try:
            data_operation_job_repository = self.repository_provider.get(DataOperationJob)
            data_operation_job = data_operation_job_repository.first(JobId=job_id)
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
                    <p>{exception}<p/>
                  '''
            try:
                self.email_provider.send(operation_contacts, subject, body)
            except Exception as ex:
                self.sql_logger.error(f"Scheduler  mail sending. Error:{ex}", job_id=data_operation_job_execution_id)
        except Exception as ex:
            self.sql_logger.error(f"Scheduler getting error. Error:{ex}", job_id=data_operation_job_execution_id)
