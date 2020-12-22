import os
from datetime import datetime
from time import time
from typing import List
from injector import inject
from sqlalchemy import not_

from domain.pdi.services.ProcessService import ProcessService
from infrastructor.IocManager import IocManager
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from infrastructor.utils.PdiUtils import PdiUtils
from models.configs.PdiConfig import PdiConfig
from models.dao.aps.ApSchedulerJob import ApSchedulerJob
from models.dao.common import OperationEvent
from models.dao.common.Status import Status
from models.dao.integration.PythonDataIntegration import PythonDataIntegration
from models.dao.operation import DataOperation, DataOperationIntegration, DataOperationJobExecution, DataOperationJob
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent
from models.enums.events import EVENT_EXECUTION_STARTED, EVENT_EXECUTION_FINISHED, EVENT_EXECUTION_INITIALIZED
from models.viewmodels.operation import CreateDataOperationModel
from models.viewmodels.operation.UpdateDataOperationModel import UpdateDataOperationModel


class DataOperationService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 connection_provider: ConnectionProvider,
                 pdi_config: PdiConfig,
                 process_service: ProcessService
                 ):
        self.process_service = process_service
        self.pdi_config: PdiConfig = pdi_config
        self.database_session_manager = database_session_manager
        self.python_data_integration_repository: Repository[PythonDataIntegration] = Repository[PythonDataIntegration](
            database_session_manager)
        self.data_operation_repository: Repository[DataOperation] = Repository[DataOperation](
            database_session_manager)
        self.data_operation_integration_repository: Repository[DataOperationIntegration] = Repository[
            DataOperationIntegration](database_session_manager)
        self.data_operation_job_execution_repository: Repository[DataOperationJobExecution] = Repository[
            DataOperationJobExecution](database_session_manager)
        self.data_operation_job_repository: Repository[DataOperationJob] = Repository[
            DataOperationJob](database_session_manager)
        self.status_repository: Repository[Status] = Repository[
            Status](database_session_manager)
        self.operation_event_repository: Repository[OperationEvent] = Repository[
            OperationEvent](database_session_manager)

        self.data_operation_job_execution_event_repository: Repository[DataOperationJobExecutionEvent] = Repository[
            DataOperationJobExecutionEvent](
            database_session_manager)
        self.ap_scheduler_job_repository: Repository[ApSchedulerJob] = Repository[ApSchedulerJob](
            database_session_manager)
        self.connection_provider: ConnectionProvider = connection_provider
        self.sql_logger: SqlLogger = sql_logger

    def get_data_operations(self) -> List[DataOperation]:
        """
        Data integration data preparing
        """
        data_operations = self.data_operation_repository.filter_by(IsDeleted=0).all()
        return data_operations

    def get_integration_datas(self, integration_code=None) -> List[PythonDataIntegration]:
        """
        Data integration data preparing
        """
        integration_datas = self.python_data_integration_repository.filter_by(IsDeleted=0)
        if integration_code is not None:
            integration_datas = integration_datas.filter_by(Code=integration_code)
        return integration_datas.all()

    def get_data_operation_by_id(self, data_operation_id=None) -> DataOperation:
        """
        Data integration data preparing
        """
        data_operation = self.data_operation_repository.first(IsDeleted=0, Id=data_operation_id)
        return data_operation

    def check_data_operation_name(self, name) -> DataOperation:
        data_operation = self.data_operation_repository.first(Name=name, IsDeleted=0)
        return data_operation is not None

    def create_data_operation(self, data_operation_model: CreateDataOperationModel) -> DataOperation:
        """
        Create Data Operation
        """
        if self.check_data_operation_name(data_operation_model.Name):
            raise OperationalException("Name already defined for other data operation")
        data_operation = DataOperation(Name=data_operation_model.Name)

        self.data_operation_repository.insert(data_operation)
        for integration in data_operation_model.Integrations:
            pdi = self.python_data_integration_repository.first(IsDeleted=0, Code=integration.Code)
            if pdi is None:
                raise OperationalException(f"{integration.Code} integration can not be found")

            data_operation_integration = DataOperationIntegration(Order=integration.Order, Limit=integration.Limit,
                                                                  ProcessCount=integration.ProcessCount,
                                                                  PythonDataIntegration=pdi,
                                                                  DataOperation=data_operation)
            self.data_operation_integration_repository.insert(data_operation_integration)

        self.database_session_manager.commit()

        data_operation = self.data_operation_repository.first(Id=data_operation.Id)
        return data_operation

    def update_data_operation(self,
                              data_operation_model: UpdateDataOperationModel) -> DataOperation:
        """
        Update Data Operation
        """
        if not self.check_data_operation_name(data_operation_model.Name):
            raise OperationalException("Data Operation not found")
        data_operation = self.data_operation_repository.first(Name=data_operation_model.Name)
        # insert or update integration
        for integration in data_operation_model.Integrations:
            pdi = self.python_data_integration_repository.first(IsDeleted=0, Code=integration.Code)
            if pdi is None:
                raise OperationalException(f"{integration.Code} integration can not be found")

            data_operation_integration = self.data_operation_integration_repository.first(
                PythonDataIntegrationId=pdi.Id)
            if data_operation_integration is None:
                new_data_operation_integration = DataOperationIntegration(Order=integration.Order,
                                                                          Limit=integration.Limit,
                                                                          ProcessCount=integration.ProcessCount,
                                                                          PythonDataIntegration=pdi,
                                                                          DataOperation=data_operation)
                self.data_operation_integration_repository.insert(new_data_operation_integration)
            else:
                data_operation_integration.Order = integration.Order
                data_operation_integration.Limit = integration.Limit
                data_operation_integration.ProcessCount = integration.ProcessCount
                data_operation_integration.IsDeleted = 0

        check_existing_integrations = self.data_operation_integration_repository.filter_by(IsDeleted=0,
                                                                                           DataOperationId=data_operation.Id)
        for existing_integration in check_existing_integrations:
            founded = False
            for integration in data_operation_model.Integrations:
                if existing_integration.PythonDataIntegration.Code == integration.Code:
                    founded = True
            if not founded:
                self.data_operation_integration_repository.delete_by_id(existing_integration.Id)
        self.database_session_manager.commit()

        data_operation = self.data_operation_repository.first(Id=data_operation.Id)
        return data_operation

    def delete_data_operation(self, id: int):
        """
        Delete Data operation
        """
        data_operation = self.data_operation_repository.first(Id=id, IsDeleted=0)
        if data_operation is None:
            raise OperationalException("Data Operation Not Found")

        self.data_operation_repository.delete_by_id(data_operation.Id)
        check_existing_integrations = self.data_operation_integration_repository.filter_by(IsDeleted=0,
                                                                                           DataOperationId=data_operation.Id)
        for existing_integration in check_existing_integrations:
            self.data_operation_integration_repository.delete_by_id(existing_integration.Id)
        message = f'{data_operation.Name} data operation deleted'
        self.sql_logger.info(message)
        self.database_session_manager.commit()

    @staticmethod
    def parallel_operation(process_id, process_name, tasks, results):
        try:
            print('[%s] evaluation routine starts' % process_name)

            root_directory = os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir, os.pardir))
            IocManager.configure_startup(root_directory)
            sql_logger = IocManager.injector.get(SqlLogger)
            database_session_manager = IocManager.injector.get(DatabaseSessionManager)
            python_data_integration_repository: Repository[PythonDataIntegration] = Repository[PythonDataIntegration](
                database_session_manager)
            connection_provider = IocManager.injector.get(ConnectionProvider)
            integration_data = python_data_integration_repository.first(Id=process_id, IsDeleted=0)

            source_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 0][0]
            target_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 1][0]
            source_connection_manager = connection_provider.get_connection(source_connection)
            target_connection_manager = connection_provider.get_connection(target_connection)
            column_rows, final_executable, related_columns = PdiUtils.get_row_column_and_values(
                target_connection.Connection.Database.ConnectorType.Name, target_connection.Schema,
                target_connection.TableName, integration_data.Columns)
            first_row, selected_rows = PdiUtils.get_first_row_and_selected_rows(column_rows)
            while True:
                # waiting for new task
                new_value = tasks.get()
                if new_value.IsFinished:
                    sql_logger.info(f"{process_name} process finished")
                    print('[%s] evaluation routine quits' % process_name)
                    # Indicate finished
                    results.put(new_value)
                    break
                else:
                    start = time()
                    print(f"StartTime :{start}")
                    sql_logger.info(
                        f"{process_name} process got a new task. limits:{new_value.Data.sub_limit}-{new_value.Data.top_limit} ")
                    executable_script = PdiUtils.prepare_executable_script(
                        source_connector_type=source_connection.Connection.Database.ConnectorType.Name,
                        source_schema=source_connection.Schema,
                        source_table_name=source_connection.TableName,
                        sub_limit=new_value.Data.sub_limit,
                        top_limit=new_value.Data.top_limit,
                        first_row=first_row,
                        selected_rows=selected_rows
                    )
                    DataOperationService.run_operation(
                        source_connection_manager=source_connection_manager,
                        target_connection_manager=target_connection_manager,
                        executable_script=executable_script,
                        related_columns=related_columns,
                        final_executable=final_executable)
                    end = time()
                    sql_logger.info(
                        f"{process_name} process finished task. limits:{new_value.Data.sub_limit}-{new_value.Data.top_limit}. time:{end - start}")
                    results.put(new_value)
        except Exception as ex:
            sql_logger.error(
                f"{process_name} process finished task. limits:{new_value.Data.sub_limit}-{new_value.Data.top_limit}. time:{end - start}- error:{ex}")
            data = TaskData(IsFinished=True)
            results.put(data)

    @staticmethod
    def parallel_operation_result(result: TaskData):
        if not result.IsFinished:
            print(f'Operation executed for limits: {result.Data.sub_limit}-{result.Data.top_limit} ')

    @staticmethod
    def run_operation(source_connection_manager, target_connection_manager, executable_script,
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
                                                   status_id: int = None):
        data_operation_job_execution = self.data_operation_job_execution_repository.first(
            Id=data_operation_job_execution_id)
        status = self.status_repository.first(Id=status_id)
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

    def start_operation(self, data_operation_id: str = None, job_id=None):  # parallel_
        """
        Integration starting operation
        """
        data_operation = self.get_data_operation_by_id(data_operation_id)

        if data_operation is None:
            self.sql_logger.info('Data operation not founded', job_id=job_id)
            return None
        data_operation_job = self.data_operation_job_repository.first(IsDeleted=0,
                                                                      DataOperationId=data_operation_id,
                                                                      ApSchedulerJobId=job_id)

        data_operation_job_execution = self.create_data_operation_job_execution(
            data_operation_job=data_operation_job)
        try:
            self.sql_logger.info(f'{data_operation.Name} data integration is Begin with data:{data_operation_id}',
                                 job_id=job_id)
            if data_operation.Integrations is None or len(data_operation.Integrations) == 0:
                self.sql_logger.info('Data operation has no integration ', job_id=job_id)
                return None
            # execution started
            self.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution.Id,
                status_id=2)
            self.create_data_operation_job_execution_event(data_operation_execution_id=data_operation_job_execution.Id,
                                                           event_code=EVENT_EXECUTION_STARTED)
            data_operation_integrations = self.data_operation_integration_repository.filter_by(IsDeleted=0).order_by(
                "Order")
            for data_operation_integration in data_operation_integrations:
                integration: PythonDataIntegration = data_operation_integration.PythonDataIntegration
                integration_code = integration.Code
                # Source and target database managers instantiate
                source_connection = [x for x in integration.Connections if x.SourceOrTarget == 0][0]
                target_connection = [x for x in integration.Connections if x.SourceOrTarget == 1][0]
                source_connection_manager = self.connection_provider.get_connection(source_connection)
                target_connection_manager = self.connection_provider.get_connection(target_connection)

                # Pre exec job
                pre_execution = [x for x in integration.ExecutionJobs if x.IsPre == 1]
                if len(pre_execution) > 0:
                    if pre_execution[0].ExecutionProcedure != '':
                        pre_execution_procedure = pre_execution[0].ExecutionProcedure
                        self.sql_logger.info(
                            f'{integration_code} Pre Execution Job is Start. {pre_execution_procedure} procedure call start.',
                            job_id=job_id)
                        target_connection_manager.run_query(f'EXEC {pre_execution_procedure}')
                        self.sql_logger.info(
                            f'{integration_code} Pre Execution Job is End. {pre_execution_procedure} procedure call end.',
                            job_id=job_id)

                # Integration Start
                self.sql_logger.info(
                    f"{integration.Code} - {target_connection.Schema}.{target_connection.TableName} integration is began",
                    job_id=job_id)

                data_count = \
                    source_connection_manager.fetch(
                        PdiUtils.count_table(source_connection.Schema, source_connection.TableName,
                                             source_connection.Connection.Database.ConnectorType.Name))[0][0]

                # Delete if target data truncate is true
                if integration.IsTargetTruncate:
                    target_connection_manager.delete(
                        PdiUtils.truncate_table(target_connection.Schema, target_connection.TableName,
                                                target_connection.Connection.Database.ConnectorType.Name))
                limit = integration.Limit
                process_count = integration.ProcessCount
                if process_count > 1:
                    # Integration Start
                    self.sql_logger.info(
                        f"{integration.Code} - operation will execute parallel. {process_count}-{limit}",
                        job_id=job_id)
                    limit_modifiers = PdiUtils.get_limit_modifiers(data_count=data_count, limit=limit)
                    self.process_service.start_parallel_process(process_id=integration.Id, datas=limit_modifiers,
                                                                process_count=process_count,
                                                                process_method=DataOperationService.parallel_operation,
                                                                result_method=DataOperationService.parallel_operation_result)
                else:
                    self.sql_logger.info(f"{integration.Code} - operation will execute serial. {limit}", job_id=job_id)
                    column_rows, final_executable, related_columns = PdiUtils.get_row_column_and_values(
                        target_connection.Connection.Database.ConnectorType.Name, target_connection.Schema,
                        target_connection.TableName, integration.Columns)
                    first_row, selected_rows = PdiUtils.get_first_row_and_selected_rows(column_rows)

                    limit_modifiers = PdiUtils.get_limit_modifiers(data_count=data_count, limit=limit)
                    for limit_modifier in limit_modifiers:
                        start = time()
                        print(f"StartTime :{start}")
                        self.sql_logger.info(
                            f"Process got a new task. limits:{limit_modifier.sub_limit}-{limit_modifier.top_limit} ")
                        executable_script = PdiUtils.prepare_executable_script(
                            source_connector_type=source_connection.Connection.Database.ConnectorType.Name,
                            source_schema=source_connection.Schema,
                            source_table_name=source_connection.TableName,
                            sub_limit=limit_modifier.sub_limit,
                            top_limit=limit_modifier.top_limit,
                            first_row=first_row,
                            selected_rows=selected_rows
                        )
                        DataOperationService.run_operation(
                            source_connection_manager=source_connection_manager,
                            target_connection_manager=target_connection_manager,
                            executable_script=executable_script,
                            related_columns=related_columns,
                            final_executable=final_executable)
                        end = time()
                        self.sql_logger.info(
                            f"Process finished task. limits:{limit_modifier.sub_limit}-{limit_modifier.top_limit}. time:{end - start}")

                # Post exec job
                post_execution = [x for x in integration.ExecutionJobs if x.IsPost == 1]
                if len(post_execution) > 0:
                    if post_execution[0].ExecutionProcedure != '':
                        post_execution_procedure = post_execution[0].ExecutionProcedure
                        self.sql_logger.info(
                            f'{integration_code} Post Execution Job is Start. {post_execution_procedure} procedure call start.',
                            job_id=job_id)
                        target_connection.run_query(f'EXEC {post_execution_procedure}')
                        self.sql_logger.info(
                            f'{integration_code} Post Execution Job is End. {post_execution_procedure} procedure call end.',
                            job_id=job_id)

                self.sql_logger.info(
                    f"{integration.Code} - {target_connection.Schema}.{target_connection.TableName} integration is completed",
                    job_id=job_id)

            # execution started
            self.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution.Id,
                status_id=3)
            self.create_data_operation_job_execution_event(data_operation_execution_id=data_operation_job_execution.Id,
                                                           event_code=EVENT_EXECUTION_FINISHED)
            self.sql_logger.info('Data Integration is completed', job_id=job_id)
        except Exception as ex:
            self.update_data_operation_job_execution_status(
                data_operation_job_execution_id=data_operation_job_execution.Id,
                status_id=4)
            self.create_data_operation_job_execution_event(data_operation_execution_id=data_operation_job_execution.Id,
                                                           event_code=EVENT_EXECUTION_FINISHED)
            raise ex
