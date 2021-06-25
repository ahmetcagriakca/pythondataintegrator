from injector import inject

from IocManager import IocManager
from infrastructor.configuration.ConfigService import ConfigService
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.delivery.EmailProvider import EmailProvider
from infrastructor.exceptions.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.operation import DataOperationJob


class SendSchedulerErrorMailCommand:
    @inject
    def __init__(self):
        self.repository_provider = RepositoryProvider()
        self.config_service = ConfigService(self.repository_provider)
        self.sql_logger = IocManager.injector.get(SqlLogger)
        self.application_config = IocManager.injector.get(ApplicationConfig)
        self.email_provider = EmailProvider(config_service=self.config_service, sql_logger=self.sql_logger)

    def send(self, job_id:int,exception:Exception,data_operation_job_execution_id=None):
        try:
            data_operation_job_repository = self.repository_provider.get(DataOperationJob)
            data_operation_job = data_operation_job_repository.first(Id=job_id)
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
                self.sql_logger.error(f"Scheduler  mail sending. Error:{ex}",job_id=data_operation_job_execution_id)
        except Exception as ex:
            self.sql_logger.error(f"Scheduler getting error. Error:{ex}",job_id=data_operation_job_execution_id)
        finally:
            self.repository_provider.close()
