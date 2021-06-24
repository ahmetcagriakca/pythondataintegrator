from datetime import datetime
from typing import List

from injector import inject

from domain.delivery.EmailService import EmailService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.common import OperationEvent
from models.dao.common.Log import Log
from models.dao.common.Status import Status
from models.dao.integration import DataIntegrationConnection
from models.dao.operation import DataOperationJobExecution, DataOperationJob, DataOperationJobExecutionIntegration, \
    DataOperationIntegration
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from models.enums.events import EVENT_EXECUTION_INITIALIZED


class DataOperationJobExecutionService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 email_service: EmailService
                 ):
        self.email_service = email_service
        self.database_session_manager = database_session_manager
        self.data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        self.data_operation_job_execution_integration_repository: Repository[DataOperationJobExecutionIntegration] = \
            Repository[
                DataOperationJobExecutionIntegration](database_session_manager)

        self.status_repository: Repository[Status] = Repository[Status](database_session_manager)
        self.operation_event_repository: Repository[OperationEvent] = Repository[
            OperationEvent](database_session_manager)

        self.data_operation_job_execution_event_repository: Repository[DataOperationJobExecutionEvent] = Repository[
            DataOperationJobExecutionEvent](database_session_manager)
        self.data_integration_connection_repository: Repository[DataIntegrationConnection] = Repository[
            DataIntegrationConnection](database_session_manager)
        self.log_repository: Repository[Log] = Repository[Log](
            database_session_manager)
        self.sql_logger: SqlLogger = sql_logger

    def create(self, data_operation_job: DataOperationJob = None):
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

    def update_status(self, data_operation_job_execution_id: int = None,
                      status_id: int = None, is_finished: bool = False):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        status = self.status_repository.first(Id=status_id)
        if is_finished:
            data_operation_job_execution.EndDate = datetime.now()

        data_operation_job_execution.Status = status
        self.database_session_manager.commit()
        return data_operation_job_execution

    def create_event(self, data_operation_execution_id,
                     event_code) -> DataOperationJobExecutionEvent:
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

    def prepare_execution_table_data(self, data_operation_job_execution_id):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        columns = [
            {'value': 'Execution Id'},
            {'value': 'Name'},
            {'value': 'Status'},
            {'value': 'Execution Start Date'},
            {'value': 'Execution End Date'}
        ]
        rows = [
            {
                'data':
                    [
                        {'value': data_operation_job_execution.Id},
                        {
                            'value': f'{data_operation_job_execution.DataOperationJob.DataOperation.Name} ({data_operation_job_execution.DataOperationJob.DataOperation.Id})'},
                        {'value': data_operation_job_execution.Status.Description},
                        {'value': data_operation_job_execution.StartDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                         'class': 'mail-row-nowrap'},
                        {'value': data_operation_job_execution.EndDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                         'class': 'mail-row-nowrap'}
                    ]
            }
        ]
        return {'columns': columns, 'rows': rows}

    def prepare_execution_event_table_data(self, data_operation_job_execution_id):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        job_execution_events: List[
            DataOperationJobExecutionEvent] = data_operation_job_execution.DataOperationJobExecutionEvents
        columns = [
            {'value': 'Event Description'},
            {'value': 'Event Date'}
        ]
        rows = []
        for job_execution_event in job_execution_events:
            execution_operation_event: OperationEvent = job_execution_event.Event
            row = {
                "data": [
                    {'value': execution_operation_event.Description},
                    {'value': job_execution_event.EventDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                     'class': 'mail-row-nowrap'}
                ]
            }
            rows.append(row)
        return {'columns': columns, 'rows': rows}

    def prepare_execution_integration_table_data(self, data_operation_job_execution_id):
        job_execution_integrations_query = self.database_session_manager.session.query(
            DataOperationJobExecutionIntegration, DataOperationIntegration
        ) \
            .filter(DataOperationJobExecutionIntegration.DataOperationIntegrationId == DataOperationIntegration.Id) \
            .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data_operation_job_execution_id) \
            .order_by(DataOperationIntegration.Order)
        job_execution_integrations = job_execution_integrations_query.all()

        columns = [

            {'value': 'Order'},
            {'value': 'Code'},
            {'value': 'Source'},
            {'value': 'Target'},
            {'value': 'Status'},
            {'value': 'Start Date'},
            # {'value': 'End Date'},
            {'value': 'Limit'},
            {'value': 'Process Count'},
            {'value': 'Source Data Count'},
            {'value': 'Affected Row Count'},
            {'value': 'Log'}
        ]
        rows = []
        for job_execution_integration_data in job_execution_integrations:
            job_execution_integration = job_execution_integration_data.DataOperationJobExecutionIntegration
            data_integration_id = job_execution_integration.DataOperationIntegration.DataIntegration.Id
            source_connection = self.data_integration_connection_repository.table \
                .filter(DataIntegrationConnection.IsDeleted == 0) \
                .filter(DataIntegrationConnection.DataIntegrationId == data_integration_id) \
                .filter(DataIntegrationConnection.SourceOrTarget == 0) \
                .one_or_none()
            target_connection = self.data_integration_connection_repository.table \
                .filter(DataIntegrationConnection.IsDeleted == 0) \
                .filter(DataIntegrationConnection.DataIntegrationId == data_integration_id) \
                .filter(DataIntegrationConnection.SourceOrTarget == 1) \
                .one_or_none()
            source_data_count = 0
            if job_execution_integration.SourceDataCount is not None and job_execution_integration.SourceDataCount > 0:
                source_data_count = job_execution_integration.SourceDataCount
            total_affected_row_count = 0
            for event in job_execution_integration.DataOperationJobExecutionIntegrationEvents:
                if event.AffectedRowCount is not None and event.AffectedRowCount > 0:
                    total_affected_row_count = total_affected_row_count + event.AffectedRowCount
            source_connection_name = source_connection.Connection.Name if source_connection is not None else ''
            target_connection_name = target_connection.Connection.Name if target_connection is not None else ''

            row = {
                "data": [
                    {'value': job_execution_integration.DataOperationIntegration.Order},
                    {'value': job_execution_integration.DataOperationIntegration.DataIntegration.Code},
                    {'value': source_connection_name},
                    {'value': target_connection_name},
                    {'value': job_execution_integration.Status.Description},
                    {'value': job_execution_integration.StartDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3] + '',
                     'class': 'mail-row-nowrap'
                     },
                    # {'value': job_execution_integration.EndDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                    #  },
                    {'value': job_execution_integration.Limit},
                    {'value': job_execution_integration.ProcessCount},
                    {'value': source_data_count},
                    {'value': total_affected_row_count},
                    {'value': job_execution_integration.Log}
                ]
            }
            rows.append(row)
        return {'columns': columns, 'rows': rows}

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

        data_operation_name = data_operation_job_execution.DataOperationJob.DataOperation.Name
        execution_table_data = self.prepare_execution_table_data(
            data_operation_job_execution_id=data_operation_job_execution_id)
        execution_event_table_data = self.prepare_execution_event_table_data(
            data_operation_job_execution_id=data_operation_job_execution_id)
        execution_integration_table_data = self.prepare_execution_integration_table_data(
            data_operation_job_execution_id=data_operation_job_execution_id)
        self.email_service.send_data_operation_finish_mail(
            data_operation_job_execution_id=data_operation_job_execution_id,
            data_operation_job_execution_status_id=data_operation_job_execution.StatusId,
            data_operation_name=data_operation_name,
            operation_contacts=operation_contacts,
            execution_table_data=execution_table_data,
            execution_event_table_data=execution_event_table_data,
            execution_integration_table_data=execution_integration_table_data
        )
