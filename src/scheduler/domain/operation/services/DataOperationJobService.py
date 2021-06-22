from injector import inject

from infrastructor.configuration.ConfigService import ConfigService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.delivery.EmailProvider import EmailProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.ApplicationConfig import ApplicationConfig
from models.dao.aps import ApSchedulerJob
from models.dao.operation import DataOperationJob


class DataOperationJobService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 email_provider: EmailProvider,
                 config_service: ConfigService,
                 application_config: ApplicationConfig
                 ):
        self.application_config = application_config
        self.sql_logger: SqlLogger = sql_logger
        self.email_provider = email_provider
        self.config_service = config_service
        self.database_session_manager = database_session_manager
        self.data_operation_job_repository: Repository[DataOperationJob] = Repository[DataOperationJob](
            database_session_manager)

    def get_by_job_id(self, job_id: int) -> DataOperationJob:
        entity = self.data_operation_job_repository.first(IsDeleted=0,
                                                          ApSchedulerJobId=job_id)
        return entity

    def send_data_operation_miss_mail(self, ap_scheduler_job: ApSchedulerJob):
        data_operation_job = self.get_by_job_id(job_id=ap_scheduler_job.Id)
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
                self.sql_logger.info(f'{data_operation_job.DataOperation.Name} mail sending contact not found')
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
                self.sql_logger.error(f"Error on mail sending. Error:{ex}")
