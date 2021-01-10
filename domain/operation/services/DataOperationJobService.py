import os
from datetime import datetime
from time import time
from typing import List
from injector import inject

from domain.integration.services.DataIntegrationService import DataIntegrationService
from domain.process.services.ProcessService import ProcessService
from infrastructor.IocManager import IocManager
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.delivery.EmailProvider import EmailProvider
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from infrastructor.utils.PdiUtils import PdiUtils
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.common import OperationEvent
from models.dao.common.Log import Log
from models.dao.common.Status import Status
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dao.operation import DataOperation, DataOperationIntegration, DataOperationJobExecution, \
    DataOperationJob
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from models.dto.LimitModifier import LimitModifier
from models.enums.events import EVENT_EXECUTION_STARTED, EVENT_EXECUTION_FINISHED, EVENT_EXECUTION_INITIALIZED
from models.viewmodels.operation import CreateDataOperationModel
from models.viewmodels.operation.UpdateDataOperationModel import UpdateDataOperationModel


class ExecuteOperationDto:
    def __init__(self,
                 source_connection=None,
                 target_connection=None,
                 source_connection_manager=None,
                 target_connection_manager=None,
                 source_query=None,
                 target_query=None,
                 related_columns=None,
                 first_row=None,
                 limit_modifier=None,
                 ):
        self.source_connection = source_connection
        self.target_connection = target_connection
        self.source_connection_manager = source_connection_manager
        self.target_connection_manager = target_connection_manager
        self.source_query = source_query
        self.target_query = target_query
        self.related_columns = related_columns
        self.first_row = first_row
        self.limit_modifier = limit_modifier


class ExecuteOperationFactory:
    def __init__(self, connection_provider: ConnectionProvider):
        self.connection_provider = connection_provider

    def GetExecuteOperationDto(self,
                               source_connection,
                               target_connection,
                               integration_data_columns):
        column_rows, related_columns, final_executable = PdiUtils.get_row_column_and_values(
            target_connection.Schema, target_connection.TableName, integration_data_columns)
        source_connection_manager = self.connection_provider.get_connection(source_connection)
        target_connection_manager = self.connection_provider.get_connection(target_connection)

        target_query = PdiUtils.prepare_target_query(
            column_rows=column_rows, query=target_connection.Query,
            target_connector_name=target_connection.Connection.Database.ConnectorType.Name)

        eliminated_column_rows = [column_row for column_row in column_rows if column_row[1] is not None]
        first_row = eliminated_column_rows[0][1]
        execute_operation_dto = ExecuteOperationDto(
            source_connection=source_connection,
            target_connection=target_connection,
            source_connection_manager=source_connection_manager,
            target_connection_manager=target_connection_manager,
            source_query=source_connection.Query,
            target_query=target_query,
            related_columns=related_columns,
            first_row=first_row
        )
        return execute_operation_dto


class DataOperationJobService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 connection_provider: ConnectionProvider,
                 process_service: ProcessService,
                 data_integration_service: DataIntegrationService,
                 email_provider: EmailProvider

                 ):
        self.database_session_manager = database_session_manager
        self.data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        self.data_operation_integration_repository: Repository[DataOperationIntegration] = Repository[
            DataOperationIntegration](database_session_manager)
        self.data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        self.data_operation_job_repository: Repository[DataOperationJob] = Repository[DataOperationJob](
            database_session_manager)
        self.status_repository: Repository[Status] = Repository[Status](database_session_manager)
        self.operation_event_repository: Repository[OperationEvent] = Repository[
            OperationEvent](database_session_manager)

        self.data_operation_job_execution_event_repository: Repository[DataOperationJobExecutionEvent] = Repository[
            DataOperationJobExecutionEvent](
            database_session_manager)
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        self.data_integration_connection_repository: Repository[DataIntegrationConnection] = Repository[
            DataIntegrationConnection](
            database_session_manager)
        self.log_repository: Repository[Log] = Repository[Log](
            database_session_manager)
        self.connection_provider: ConnectionProvider = connection_provider
        self.sql_logger: SqlLogger = sql_logger
        self.email_provider = email_provider
        self.data_integration_service = data_integration_service
        self.process_service = process_service

    def get_data_operations(self) -> List[DataOperation]:
        """
        Data data_integration data preparing
        """
        data_operations = self.data_operation_repository.filter_by(IsDeleted=0).all()
        return data_operations

    def get_data_operation_by_id(self, data_operation_id=None) -> DataOperation:
        """
        Data data_integration data preparing
        """
        data_operation = self.data_operation_repository.first(IsDeleted=0, Id=data_operation_id)
        return data_operation

    @staticmethod
    def parallel_operation(process_id, sub_process_id, process_name, tasks, results):
        try:
            print('[%s] evaluation routine starts' % process_name)

            root_directory = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
            IocManager.configure_startup(root_directory)
            sql_logger = IocManager.injector.get(SqlLogger)
            database_session_manager = IocManager.injector.get(DatabaseSessionManager)
            data_operation_job_service = IocManager.injector.get(DataOperationJobService)

            data_integration_repository: Repository[DataIntegration] = Repository[
                DataIntegration](
                database_session_manager)
            connection_provider = IocManager.injector.get(ConnectionProvider)
            integration_data = data_integration_repository.first(Id=process_id, IsDeleted=0)
            source_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 0][0]
            target_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 1][0]
            execute_operation_dto = ExecuteOperationFactory(connection_provider=connection_provider) \
                .GetExecuteOperationDto(
                source_connection=source_connection,
                target_connection=target_connection,
                integration_data_columns=integration_data.Columns)

            while True:
                # waiting for new task
                new_task: TaskData = tasks.get()
                new_task.SubProcessId = sub_process_id
                if new_task.IsFinished:
                    sql_logger.info(f"{process_name} process finished")
                    # Indicate finished
                    results.put(new_task)
                    break
                else:
                    start = time()
                    sql_logger.info(
                        f"{process_name}-{sub_process_id} process got a new task.Id:{new_task.Data.Id} limits:{new_task.Data.SubLimit}-{new_task.Data.TopLimit} ")
                    execute_operation_dto.limit_modifier = new_task.Data
                    data_operation_job_service.execute_operation(execute_operation_dto=execute_operation_dto)
                    end = time()
                    sql_logger.info(
                        f"{process_name} process finished task. limits:{new_task.Data.SubLimit}-{new_task.Data.TopLimit}. time:{end - start}")
                    new_task.IsProcessed = True
                    results.put(new_task)

        except Exception as ex:
            sql_logger.error(
                f"{process_name} process finished task. limits:{new_task.Data.SubLimit}-{new_task.Data.TopLimit}. time:{end - start}- error:{ex}")

            data = TaskData(SubProcessId=sub_process_id, IsFinished=True)
            results.put(data)

    @staticmethod
    def parallel_operation_result(result: TaskData):
        if not result.IsFinished:
            print(f'Operation executed for limits: {result.Data.SubLimit}-{result.Data.TopLimit} ')

    def run_operation(self, source_connection_manager, target_connection_manager, executable_script,
                      related_columns, final_executable):
        # Extracted data fetched from source database
        extracted_data = source_connection_manager.fetch(executable_script)
        # Insert rows preparing
        inserted_rows = PdiUtils.prepare_insert_row(extracted_data, related_columns)
        # rows inserted to database
        target_connection_manager.insert_many(final_executable, inserted_rows)

    def create_data_operation_job_execution(self, data_operation_job: DataOperationJob = None):
        not_finished_execution = self.data_operation_job_execution_repository.table \
            .filter(self.data_operation_job_execution_repository.type.StatusId != 3) \
            .filter_by(DataOperationJobId=data_operation_job.Id).first()

        # not_finished_execution = self.data_operation_job_execution_repository.table.first(
        #     self.data_operation_job_execution_repository.type.EventId != 3, DataOperationId=data_operation_id,
        #     ApSchedulerJobId=job_id)
        if not_finished_execution is not None:
            self.sql_logger.info(f'Data operation({data_operation_job.DataOperation.Name}) already running',
                                 job_id=data_operation_job.ApSchedulerJobId)
            raise OperationalException("Already running execution")
        status = self.status_repository.first(Id=1)
        data_operation_job_execution = DataOperationJobExecution(
            DataOperationJob=data_operation_job,
            Status=status)
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

    def execute_limit_modifiers(self, sql_logger, limit_modifiers, execute_operation_dto):

        for limit_modifier in limit_modifiers:
            start = time()
            sql_logger.info(
                f"Process got a new task. limits:{limit_modifier.SubLimit}-{limit_modifier.TopLimit} ")
            execute_operation_dto.limit_modifier = limit_modifier
            self.execute_operation(execute_operation_dto=execute_operation_dto)
            end = time()
            sql_logger.info(
                f"Process finished task. limits:{limit_modifier.SubLimit}-{limit_modifier.TopLimit}. time:{end - start}")

    def execute_operation(self, execute_operation_dto: ExecuteOperationDto):
        executable_script = PdiUtils.prepare_executable_script(
            source_connector_type=execute_operation_dto.source_connection.Connection.Database.ConnectorType.Name,
            query=execute_operation_dto.source_query,
            sub_limit=execute_operation_dto.limit_modifier.SubLimit,
            top_limit=execute_operation_dto.limit_modifier.TopLimit,
            first_row=execute_operation_dto.first_row
        )
        self.run_operation(
            source_connection_manager=execute_operation_dto.source_connection_manager,
            target_connection_manager=execute_operation_dto.target_connection_manager,
            executable_script=executable_script,
            related_columns=execute_operation_dto.related_columns,
            final_executable=execute_operation_dto.target_query)

    def execute_procedures(self, data_integration, target_connection_manager, is_pre, is_post):
        pre_execution = [x for x in data_integration.ExecutionJobs if
                         x.IsPre == is_pre and x.IsPost == is_post and x.IsDeleted == 0]
        if len(pre_execution) > 0:
            if pre_execution[0].ExecutionProcedure != '':
                pre_execution_procedure = pre_execution[0].ExecutionProcedure
                target_connection_manager.run_query(f'EXEC {pre_execution_procedure}')

    def integration_run_query(self, data_integration, job_id):
        self.sql_logger.info(
            f"{data_integration.Code} integration run query started",
            job_id=job_id)

        target_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                              DataIntegration=data_integration,
                                                                              SourceOrTarget=1)
        target_connection_manager = self.connection_provider.get_connection(
            target_connection)  # Pre exec job

        self.execute_procedures(data_integration=data_integration, target_connection_manager=target_connection_manager,
                                is_pre=1, is_post=0)

        if data_integration.IsTargetTruncate:
            target_connection_manager.delete(
                PdiUtils.truncate_table(target_connection.Schema,
                                        target_connection.TableName))

        target_connection_manager.run_query(target_connection.Query)

        self.execute_procedures(data_integration=data_integration, target_connection_manager=target_connection_manager,
                                is_pre=0, is_post=1)

        self.sql_logger.info(
            f"{data_integration.Code} integration run query finished",
            job_id=job_id)

    def integration_execute_operation(self, data_integration, limit,
                                      process_count, job_id):
        source_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                              DataIntegration=data_integration,
                                                                              SourceOrTarget=0)
        target_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                              DataIntegration=data_integration,
                                                                              SourceOrTarget=1)
        # Integration Start
        self.sql_logger.info(
            f"{data_integration.Code} - {target_connection.Schema}.{target_connection.TableName} integration execute operation started",
            job_id=job_id)

        target_connection_manager = self.connection_provider.get_connection(target_connection)
        source_connection_manager = self.connection_provider.get_connection(source_connection)
        # Pre exec job

        self.execute_procedures(data_integration=data_integration, target_connection_manager=target_connection_manager,
                                is_pre=1, is_post=0)

        if data_integration.IsTargetTruncate:
            target_connection_manager.run_query(
                PdiUtils.truncate_table(target_connection.Schema,
                                        target_connection.TableName))
        data_count = 0
        if source_connection.Connection.Database.ConnectorType.Name == 'MSSQL':
            data_count = \
                source_connection_manager.fetch(PdiUtils.count_table_mssql(source_connection.Query))[
                    0][0]
        elif source_connection.Connection.Database.ConnectorType.Name == 'POSTGRESQL':
            data_count = \
                source_connection_manager.fetch(
                    PdiUtils.count_table_postgresql(source_connection.Query))[0][0]
        elif source_connection.Connection.Database.ConnectorType.Name == 'ORACLE':
            data_count = \
                source_connection_manager.fetch(PdiUtils.count_table_oracle(source_connection.Query))[
                    0][0]
        # Delete if target data truncate is true
        if limit != 0:
            if process_count > 1:
                # Integration Start
                self.sql_logger.info(
                    f"{data_integration.Code} - operation will execute parallel. {process_count}-{limit}",
                    job_id=job_id)
                limit_modifiers = PdiUtils.get_limit_modifiers(data_count=data_count, limit=limit)
                unprocessed_task_list = self.process_service.start_parallel_process(process_id=data_integration.Id,
                                                                                    datas=limit_modifiers,
                                                                                    process_count=process_count,
                                                                                    process_method=DataOperationJobService.parallel_operation,
                                                                                    result_method=DataOperationJobService.parallel_operation_result)
                print("parallel finished")
                if unprocessed_task_list is not None and len(unprocessed_task_list) > 0:
                    self.sql_logger.info(f"Unprocessed tasks founded",
                                         job_id=job_id)
                    execute_operation_dto = ExecuteOperationFactory(connection_provider=self.connection_provider) \
                        .GetExecuteOperationDto(
                        source_connection=source_connection,
                        target_connection=target_connection,
                        integration_data_columns=data_integration.Columns)
                    limit_modifiers = [unprocessed_task.Data for unprocessed_task in unprocessed_task_list]

                    self.execute_limit_modifiers(sql_logger=self.sql_logger,
                                                 limit_modifiers=limit_modifiers,
                                                 execute_operation_dto=execute_operation_dto)

            else:
                self.sql_logger.info(f"{data_integration.Code} - operation will execute serial. {limit}",
                                     job_id=job_id)

                execute_operation_dto = ExecuteOperationFactory(connection_provider=self.connection_provider) \
                    .GetExecuteOperationDto(
                    source_connection=source_connection,
                    target_connection=target_connection,
                    integration_data_columns=data_integration.Columns)
                limit_modifiers = PdiUtils.get_limit_modifiers(data_count=data_count, limit=limit)
                self.execute_limit_modifiers(sql_logger=self.sql_logger,
                                             limit_modifiers=limit_modifiers,
                                             execute_operation_dto=execute_operation_dto)

        # Post exec job
        self.execute_procedures(data_integration=data_integration, target_connection_manager=target_connection_manager,
                                is_pre=0, is_post=1)

        self.sql_logger.info(
            f"{data_integration.Code} - {target_connection.Schema}.{target_connection.TableName} integration execute operation finished",
            job_id=job_id)

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
        if operation_contacts is None:
            self.sql_logger.info(f'{data_operation_job_execution_id} mail sending contact not found',
                                 job_id=data_operation_job_execution_id)
            return

        data_operation_name = data_operation_job_execution.DataOperationJob.DataOperation.Name
        subject = f"{data_operation_name} execution completed"
        if data_operation_job_execution.StatusId == 3:
            subject = subject + " successfully"
        elif data_operation_job_execution.StatusId == 4:
            subject = subject + " with error"
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

    def start_operation(self, data_operation_id: str = None, job_id=None):  # parallel_
        """
        Integration starting operation
        """
        data_operation = self.get_data_operation_by_id(data_operation_id)

        if data_operation is None:
            self.sql_logger.info('Data operation not founded')
            return None
        data_operation_job = self.data_operation_job_repository.first(IsDeleted=0,
                                                                      DataOperationId=data_operation_id,
                                                                      ApSchedulerJobId=job_id)

        data_operation_job_execution = self.create_data_operation_job_execution(
            data_operation_job=data_operation_job)

        data_operation_job_execution_id = data_operation_job_execution.Id
        try:
            self.sql_logger.info(f'{data_operation.Name} data operation is begin',
                                 job_id=data_operation_job_execution_id)
            if data_operation.Integrations is None or len(data_operation.Integrations) == 0:
                self.sql_logger.info('Data operation has no data_integration ', job_id=data_operation_job_execution_id)
                return None
            # execution started
            self.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution_id,
                status_id=2)
            self.create_data_operation_job_execution_event(
                data_operation_execution_id=data_operation_job_execution_id,
                event_code=EVENT_EXECUTION_STARTED)
            data_operation_integrations = self.data_operation_integration_repository.filter_by(
                IsDeleted=0, DataOperationId=data_operation.Id).order_by("Order").all()
            for data_operation_integration in data_operation_integrations:
                data_integration: DataIntegration = data_operation_integration.DataIntegration
                # Source and target database managers instantiate
                source_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                                      DataIntegration=data_integration,
                                                                                      SourceOrTarget=0)
                # only target query run
                if source_connection is None or source_connection.Query is None or source_connection.Query == '':
                    self.integration_run_query(data_integration=data_integration,
                                               job_id=data_operation_job_execution_id)
                else:
                    self.integration_execute_operation(data_integration=data_integration,
                                                       limit=data_operation_integration.Limit,
                                                       process_count=data_operation_integration.ProcessCount,
                                                       job_id=data_operation_job_execution_id)
            self.sql_logger.info(f'{data_operation.Name} data operation is completed',
                                 job_id=data_operation_job_execution_id)
            self.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution_id,
                status_id=3, is_finished=True)
            self.create_data_operation_job_execution_event(
                data_operation_execution_id=data_operation_job_execution_id,
                event_code=EVENT_EXECUTION_FINISHED)
            # execution started
            self.send_data_operation_finish_mail(data_operation_job_execution_id)
        except Exception as ex:
            self.sql_logger.error(f'{data_operation.Name} data operation has error. Error: {ex}',
                                  job_id=data_operation_job_execution_id)
            self.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution_id,
                status_id=4, is_finished=True)
            self.create_data_operation_job_execution_event(
                data_operation_execution_id=data_operation_job_execution_id,
                event_code=EVENT_EXECUTION_FINISHED)
            self.send_data_operation_finish_mail(data_operation_job_execution_id)
            raise ex
