import os
from time import time
from typing import List
from injector import inject
from domain.operation.services.DataOperationJobExecutionService import DataOperationJobExecutionService
from domain.process.services.ProcessService import ProcessService
from infrastructor.IocManager import IocManager
from infrastructor.data.ConnectionManager import ConnectionManager
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dao.integration.DataIntegrationExecutionJob import DataIntegrationExecutionJob
from models.dao.operation import DataOperation, DataOperationIntegration, DataOperationJob
from models.dto.ExecuteOperationDto import ExecuteOperationDto
from models.dto.LimitModifier import LimitModifier
from models.enums.events import EVENT_EXECUTION_STARTED, EVENT_EXECUTION_FINISHED, \
    EVENT_EXECUTION_INTEGRATION_EXECUTE_PRE_PROCEDURE, EVENT_EXECUTION_INTEGRATION_EXECUTE_POST_PROCEDURE, \
    EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, \
    EVENT_EXECUTION_INTEGRATION_FINISHED, EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION


class DataOperationJobService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 connection_provider: ConnectionProvider,
                 process_service: ProcessService,
                 data_operation_job_execution_service: DataOperationJobExecutionService,

                 ):
        self.database_session_manager = database_session_manager
        self.connection_provider: ConnectionProvider = connection_provider
        self.sql_logger: SqlLogger = sql_logger
        self.process_service = process_service
        self.data_operation_job_execution_service = data_operation_job_execution_service
        self.data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        self.data_operation_integration_repository: Repository[DataOperationIntegration] = Repository[
            DataOperationIntegration](database_session_manager)
        self.data_operation_job_repository: Repository[DataOperationJob] = Repository[DataOperationJob](
            database_session_manager)

        self.data_integration_repository: Repository[DataIntegration] = Repository[
            DataIntegration](
            database_session_manager)
        self.data_integration_connection_repository: Repository[DataIntegrationConnection] = Repository[
            DataIntegrationConnection](
            database_session_manager)
        self.data_integration_execution_job_repository: Repository[DataIntegrationExecutionJob] = Repository[
            DataIntegrationExecutionJob](
            database_session_manager)

    def get_data_operation_by_id(self, data_operation_id=None) -> DataOperation:
        """
        Data data_integration data preparing
        """
        data_operation = self.data_operation_repository.first(IsDeleted=0, Id=data_operation_id)
        return data_operation

    def get_execute_operation_dto(self,
                                  source_connection: DataIntegrationConnection,
                                  target_connection: DataIntegrationConnection,
                                  data_integration_columns: List[DataIntegrationColumn]):
        column_rows = [(data_integration_column.ResourceType, data_integration_column.SourceColumnName,
                        data_integration_column.TargetColumnName) for data_integration_column in
                       data_integration_columns]
        execute_operation_dto = ExecuteOperationDto(
            source_connection=source_connection,
            target_connection=target_connection,
            source_query=source_connection.Query,
            target_query=target_connection.Query,
            column_rows=column_rows,
            first_row=data_integration_columns[0].SourceColumnName
        )
        return execute_operation_dto

    def get_limit_modifiers(self, data_count, limit):
        top_limit = limit + 1
        sub_limit = 1
        limit_modifiers = []
        id = 0
        while True:
            if top_limit != limit and top_limit - data_count > limit:
                break
            id = id + 1
            limit_modifier = LimitModifier(Id=id, TopLimit=top_limit, SubLimit=sub_limit)
            limit_modifiers.append(limit_modifier)
            top_limit += limit
            sub_limit += limit
        return limit_modifiers

    def prepare_insert_row(self, extracted_datas, column_rows):
        insert_rows = []
        for extracted_data in extracted_datas:
            row = []
            for column_row in column_rows:
                row.append(extracted_data[column_rows.index(column_row)])
            insert_rows.append(tuple(row))
        return insert_rows

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

            data_integration_connection_repository: Repository[DataIntegrationConnection] = Repository[
                DataIntegrationConnection](
                database_session_manager)
            data_integration = data_integration_repository.first(Id=process_id, IsDeleted=0)

            source_connection = data_integration_connection_repository.first(IsDeleted=0,
                                                                             DataIntegration=data_integration,
                                                                             SourceOrTarget=0)
            target_connection = data_integration_connection_repository.first(IsDeleted=0,
                                                                             DataIntegration=data_integration,
                                                                             SourceOrTarget=1)
            execute_operation_dto = data_operation_job_service.get_execute_operation_dto(
                source_connection=source_connection,
                target_connection=target_connection,
                data_integration_columns=data_integration.Columns)

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
        source_connection_manager = self.connection_provider.get_connection_manager(
            connection=execute_operation_dto.source_connection)
        target_connection_manager = self.connection_provider.get_connection_manager(
            connection=execute_operation_dto.target_connection)
        # Extracted data fetched from source database
        extracted_data = source_connection_manager.get_table_data(
            query=execute_operation_dto.source_query,
            first_row=execute_operation_dto.first_row,
            sub_limit=execute_operation_dto.limit_modifier.SubLimit,
            top_limit=execute_operation_dto.limit_modifier.TopLimit
        )
        prepared_datas = self.prepare_insert_row(extracted_datas=extracted_data,
                                                 column_rows=execute_operation_dto.column_rows)
        prepared_target_query = target_connection_manager.prepare_target_query(
            column_rows=execute_operation_dto.column_rows,
            query=execute_operation_dto.target_connection.Query)
        # rows insert to database
        target_connection_manager.execute_many(query=prepared_target_query, data=prepared_datas)

    def execute_procedures(self, target_connection_manager: ConnectionManager,
                           execution_jobs: List[DataIntegrationExecutionJob]):
        if len(execution_jobs) > 0:
            for execution_job in execution_jobs:
                if execution_job.ExecutionProcedure is not None and execution_job.ExecutionProcedure != '':
                    procedure = execution_job.ExecutionProcedure
                    target_connection_manager.execute_procedure(procedure=procedure)

    def integration_run_query(self, data_operation_integration: DataOperationIntegration, job_id):
        data_operation_job_execution_integration = self.data_operation_job_execution_service.create_data_operation_job_execution_integration(
            data_operation_job_execution_id=job_id, data_operation_integration=data_operation_integration)
        data_operation_job_execution_integration_id=data_operation_job_execution_integration.Id
        data_integration: DataIntegration = data_operation_integration.DataIntegration
        self.sql_logger.info(
            f"{data_integration.Code} integration run query started",
            job_id=job_id)
        affected_rowcount = 0
        try:

            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                status_id=2)
            target_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                                  DataIntegration=data_integration,
                                                                                  SourceOrTarget=1)
            target_connection_manager = self.connection_provider.get_connection_manager(connection=target_connection)
            pre_execution_jobs = self.data_integration_execution_job_repository.filter_by(
                DataIntegration=data_integration, IsPre=True, IsPost=False, IsDeleted=0).all()
            if pre_execution_jobs is not None and len(pre_execution_jobs) > 0:
                # Pre exec job
                self.execute_procedures(
                    target_connection_manager=target_connection_manager,
                    execution_jobs=pre_execution_jobs)

                self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                    data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                    event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_PRE_PROCEDURE)

            if data_integration.IsTargetTruncate:
                truncate_affected_rowcount = target_connection_manager.truncate_table(schema=target_connection.Schema,
                                                                                      table=target_connection.TableName)

                self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                    data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                    event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, affected_row=truncate_affected_rowcount)

            affected_rowcount = target_connection_manager.execute(query=target_connection.Query)

            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_source_data_count(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                source_data_count=affected_rowcount)
            self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_QUERY, affected_row=affected_rowcount)

            post_execution_jobs = self.data_integration_execution_job_repository.filter_by(
                DataIntegration=data_integration, IsPre=False, IsPost=True, IsDeleted=0).all()
            if post_execution_jobs is not None and len(post_execution_jobs) > 0:
                # Pre exec job
                self.execute_procedures(
                    target_connection_manager=target_connection_manager,
                    execution_jobs=post_execution_jobs)

                self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                    data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                    event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_POST_PROCEDURE)

            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                status_id=3, is_finished=True)
            self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_FINISHED)
            # affected_rowcount_string=affected_rowcount>0
            self.sql_logger.info(
                f"{data_integration.Code} integration run query finished. (affected row count:{affected_rowcount})",
                job_id=job_id)
        except Exception as ex:
            log = f"{data_integration.Code} integration run query getting error. Error:{ex}"
            self.sql_logger.info(log, job_id=job_id)
            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                status_id=4, is_finished=True)
            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_log(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                log=log)
            self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_FINISHED)

    def integration_execute_operation(self, data_operation_integration: DataOperationIntegration, job_id):
        data_operation_job_execution_integration = self.data_operation_job_execution_service.create_data_operation_job_execution_integration(
            data_operation_job_execution_id=job_id, data_operation_integration=data_operation_integration)
        data_operation_job_execution_integration_id=data_operation_job_execution_integration.Id
        data_integration: DataIntegration = data_operation_integration.DataIntegration
        try:
            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                status_id=2)
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

            source_connection_manager = self.connection_provider.get_connection_manager(connection=source_connection)
            target_connection_manager = self.connection_provider.get_connection_manager(connection=target_connection)

            pre_execution_jobs = self.data_integration_execution_job_repository.filter_by(
                DataIntegration=data_integration, IsPre=True, IsPost=False, IsDeleted=0).all()
            if pre_execution_jobs is not None and len(pre_execution_jobs) > 0:
                # Pre exec job
                self.execute_procedures(
                    target_connection_manager=target_connection_manager,
                    execution_jobs=pre_execution_jobs)

                self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                    data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                    event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_PRE_PROCEDURE)

            if data_integration.IsTargetTruncate:
                truncate_affected_rowcount = target_connection_manager.truncate_table(schema=target_connection.Schema,
                                                                                      table=target_connection.TableName)

                self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                    data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                    event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_TRUNCATE, affected_row=truncate_affected_rowcount)

            data_count = source_connection_manager.get_table_count(source_connection.Query)

            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_source_data_count(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                source_data_count=data_count)
            limit = data_operation_integration.Limit
            process_count = data_operation_integration.ProcessCount
            if limit != 0:
                if process_count > 1:
                    # Integration Start
                    self.sql_logger.info(
                        f"{data_integration.Code} - operation will execute parallel. {process_count}-{limit}",
                        job_id=job_id)
                    limit_modifiers = self.get_limit_modifiers(data_count=data_count, limit=limit)
                    unprocessed_task_list = self.process_service.start_parallel_process(process_id=data_integration.Id,
                                                                                        datas=limit_modifiers,
                                                                                        process_count=process_count,
                                                                                        process_method=DataOperationJobService.parallel_operation,
                                                                                        result_method=DataOperationJobService.parallel_operation_result)
                    print("parallel finished")
                    if unprocessed_task_list is not None and len(unprocessed_task_list) > 0:
                        print(f"Unprocessed tasks founded")
                        execute_operation_dto = self.get_execute_operation_dto(
                            source_connection=source_connection,
                            target_connection=target_connection,
                            data_integration_columns=data_integration.Columns)
                        limit_modifiers = [unprocessed_task.Data for unprocessed_task in unprocessed_task_list]

                        self.execute_limit_modifiers(sql_logger=self.sql_logger,
                                                     limit_modifiers=limit_modifiers,
                                                     execute_operation_dto=execute_operation_dto)

                else:
                    self.sql_logger.info(f"{data_integration.Code} - operation will execute serial. {limit}",
                                         job_id=job_id)

                    execute_operation_dto = self.get_execute_operation_dto(
                        source_connection=source_connection,
                        target_connection=target_connection,
                        data_integration_columns=data_integration.Columns)
                    limit_modifiers = self.get_limit_modifiers(data_count=data_count, limit=limit)
                    self.execute_limit_modifiers(sql_logger=self.sql_logger,
                                                 limit_modifiers=limit_modifiers,
                                                 execute_operation_dto=execute_operation_dto)

            self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_OPERATION, affected_row=data_count)
            post_execution_jobs = self.data_integration_execution_job_repository.filter_by(
                DataIntegration=data_integration, IsPre=False, IsPost=True, IsDeleted=0).all()
            if post_execution_jobs is not None and len(post_execution_jobs) > 0:
                # Pre exec job
                self.execute_procedures(
                    target_connection_manager=target_connection_manager,
                    execution_jobs=post_execution_jobs)

                self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                    data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                    event_code=EVENT_EXECUTION_INTEGRATION_EXECUTE_POST_PROCEDURE)

            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                status_id=3, is_finished=True)
            self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_FINISHED)

            self.sql_logger.info(
                f"{data_integration.Code} - {target_connection.Schema}.{target_connection.TableName} integration execute operation finished. (Source Data Count:{data_count})",
                job_id=job_id)
        except Exception as ex:
            log = f"{data_integration.Code} integration run query getting error. Error:{ex}"
            self.sql_logger.info(log, job_id=job_id)

            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_status(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                status_id=4, is_finished=True)
            self.data_operation_job_execution_service.update_data_operation_job_execution_integration_log(
                data_operation_job_execution_integration_id=data_operation_job_execution_integration_id,
                log=log)
            self.data_operation_job_execution_service.create_data_operation_job_execution_integration_event(
                data_operation_execution_integration_id=data_operation_job_execution_integration_id,
                event_code=EVENT_EXECUTION_INTEGRATION_FINISHED)
            raise ex

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

        data_operation_job_execution = self.data_operation_job_execution_service.create_data_operation_job_execution(
            data_operation_job=data_operation_job)

        data_operation_job_execution_id = data_operation_job_execution.Id
        try:
            self.sql_logger.info(f'{data_operation.Name} data operation is begin',
                                 job_id=data_operation_job_execution_id)
            if data_operation.Integrations is None or len(data_operation.Integrations) == 0:
                self.sql_logger.info('Data operation has no data_integration ',
                                     job_id=data_operation_job_execution_id)
                return None
            # execution started
            self.data_operation_job_execution_service.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution_id,
                status_id=2)
            self.data_operation_job_execution_service.create_data_operation_job_execution_event(
                data_operation_execution_id=data_operation_job_execution_id,
                event_code=EVENT_EXECUTION_STARTED)
            data_operation_integrations = self.data_operation_integration_repository.filter_by(
                IsDeleted=0, DataOperationId=data_operation.Id).order_by("Order").all()

            for data_operation_integration in data_operation_integrations:
                data_integration= self.data_integration_repository.first(Id=data_operation_integration.DataIntegrationId)
                # data_integration: DataIntegration = data_operation_integration.DataIntegration
                # Source and target database managers instantiate
                source_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                                      DataIntegration=data_integration,
                                                                                      SourceOrTarget=0)
                # only target query run
                if source_connection is None or source_connection.Query is None or source_connection.Query == '':
                    self.integration_run_query(data_operation_integration=data_operation_integration,
                                               job_id=data_operation_job_execution_id)
                else:
                    self.integration_execute_operation(data_operation_integration=data_operation_integration,
                                                       job_id=data_operation_job_execution_id)
            self.sql_logger.info(f'{data_operation.Name} data operation is completed',
                                 job_id=data_operation_job_execution_id)
            self.data_operation_job_execution_service.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution_id,
                status_id=3, is_finished=True)
            self.data_operation_job_execution_service.create_data_operation_job_execution_event(
                data_operation_execution_id=data_operation_job_execution_id,
                event_code=EVENT_EXECUTION_FINISHED)
            self.data_operation_job_execution_service.send_data_operation_finish_mail(data_operation_job_execution_id)
        except Exception as ex:
            self.sql_logger.error(f'{data_operation.Name} data operation has error. Error: {ex}',
                                  job_id=data_operation_job_execution_id)
            self.data_operation_job_execution_service.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution_id,
                status_id=4, is_finished=True)
            self.data_operation_job_execution_service.create_data_operation_job_execution_event(
                data_operation_execution_id=data_operation_job_execution_id,
                event_code=EVENT_EXECUTION_FINISHED)
            self.data_operation_job_execution_service.send_data_operation_finish_mail(data_operation_job_execution_id)
            raise ex
