from datetime import datetime
from injector import inject

from infrastructor.configuration.ConfigService import ConfigService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.delivery.EmailProvider import EmailProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.ApiConfig import ApiConfig
from models.dao.common import OperationEvent
from models.dao.common.Log import Log
from models.dao.common.Status import Status
from models.dao.operation import DataOperationJobExecution, DataOperationJob
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from models.enums.events import EVENT_EXECUTION_INITIALIZED


class DataOperationJobExecutionService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 email_provider: EmailProvider,
                 config_service: ConfigService,
                 api_config: ApiConfig

                 ):
        self.api_config: ApiConfig = api_config
        self.database_session_manager = database_session_manager
        self.data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        self.status_repository: Repository[Status] = Repository[Status](database_session_manager)
        self.operation_event_repository: Repository[OperationEvent] = Repository[
            OperationEvent](database_session_manager)

        self.data_operation_job_execution_event_repository: Repository[DataOperationJobExecutionEvent] = Repository[
            DataOperationJobExecutionEvent](database_session_manager)
        self.log_repository: Repository[Log] = Repository[Log](
            database_session_manager)
        self.sql_logger: SqlLogger = sql_logger
        self.email_provider = email_provider
        self.config_service = config_service

    def create_data_operation_job_execution(self, data_operation_job: DataOperationJob = None):
        # not_finished_execution = self.data_operation_job_execution_repository.table \
        #     .filter_by(DataOperationJobId=data_operation_job.Id).first()

        # not_finished_execution = self.data_operation_job_execution_repository.table.first(
        #     self.data_operation_job_execution_repository.type.EventId != 3, DataOperationId=data_operation_id,
        #     ApSchedulerJobId=job_id)
        # if not_finished_execution is not None:
        #     self.sql_logger.info(f'Data operation({data_operation_job.DataOperation.Name}) already running',
        #                          job_id=data_operation_job.ApSchedulerJobId)
        #     raise OperationalException("Already running execution")
        status = self.status_repository.first(Id=1)
        data_operation_job_execution = DataOperationJobExecution(
            DataOperationJob=data_operation_job,
            Status=status,
            Definition=data_operation_job.DataOperation.Definition)
        self.data_operation_job_execution_repository.insert(data_operation_job_execution)
        operation_event = self.operation_event_repository.first(Code=EVENT_EXECUTION_INITIALIZED)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        self.data_operation_job_execution_event_repository.insert(data_operation_job_execution_event)
        self.database_session_manager.commit()
        return data_operation_job_execution

    def update_data_operation_job_execution_status(self, data_operation_job_execution_id: int = None,
                                                   status_id: int = None, is_finished: bool = False):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        status = self.status_repository.first(Id=status_id)
        if is_finished:
            data_operation_job_execution.EndDate = datetime.now()

        data_operation_job_execution.Status = status
        self.database_session_manager.commit()
        return data_operation_job_execution

    def create_data_operation_job_execution_event(self, data_operation_execution_id: str = None,
                                                  event_code=None) -> DataOperationJobExecutionEvent:
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_execution_id)
        operation_event = self.operation_event_repository.first(Code=event_code)
        data_operation_job_execution_event = DataOperationJobExecutionEvent(
            EventDate=datetime.now(),
            DataOperationJobExecution=data_operation_job_execution,
            Event=operation_event)
        self.data_operation_job_execution_event_repository.insert(data_operation_job_execution_event)
        self.database_session_manager.commit()
        return data_operation_job_execution_event

    def send_data_operation_finish_mail(self, data_operation_job_execution_id):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        if data_operation_job_execution is None:
            self.sql_logger.info(f'{data_operation_job_execution_id} mail sending execution not found',
                                 job_id=data_operation_job_execution_id)
            return

        operation_contacts = []
        for contact in data_operation_job_execution.DataOperationJob.DataOperation.Contacts:
            if contact.IsDeleted == 0:
                operation_contacts.append(contact.Email)

        default_contacts = self.config_service.get_config_by_name("DataOperationDefaultContact")
        if default_contacts is not None and default_contacts != '':
            default_contacts_emails = default_contacts.split(",")
            for default_contact in default_contacts_emails:
                if default_contact is not None and default_contact != '':
                    operation_contacts.append(default_contact)
        if operation_contacts is None:
            self.sql_logger.info(f'{data_operation_job_execution_id} mail sending contact not found',
                                 job_id=data_operation_job_execution_id)
            return

        data_operation_name = data_operation_job_execution.DataOperationJob.DataOperation.Name
        subject = f"Execution completed"
        if data_operation_job_execution.StatusId == 3:
            subject = subject + " successfully"
        elif data_operation_job_execution.StatusId == 4:
            subject = subject + " with error"
        subject = subject + f": {self.api_config.environment} » {data_operation_name} » {data_operation_job_execution_id}"

        logs = self.log_repository.filter_by(JobId=data_operation_job_execution_id).order_by("Id").all()
        log_texts = ""
        for log in logs:
            log_time = log.LogDatetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            log_texts = log_texts + f"</br> {log_time} - {log.Content}"
        body = f'''
Job started at : {data_operation_job_execution.StartDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
</br>
Job finished at : {data_operation_job_execution.EndDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
</br>
Job Logs:{log_texts}
'''
        self.email_provider.send(operation_contacts, subject, body)
