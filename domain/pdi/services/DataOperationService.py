import os
from time import time
from typing import List
from injector import inject

from domain.pdi.services.ProcessService import ProcessService
from infrastructor.IocManager import IocManager
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.multi_processing.ParallelMultiProcessing import TaskData
from infrastructor.utils.PdiUtils import PdiUtils
from models.configs.PdiConfig import PdiConfig
from models.dao.integration.PythonDataIntegration import PythonDataIntegration


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
        self.connection_provider: ConnectionProvider = connection_provider
        self.sql_logger: SqlLogger = sql_logger

    def get_integration_datas(self, integration_code=None) -> List[PythonDataIntegration]:
        """
        Data integration data preparing
        """
        integration_datas = self.python_data_integration_repository.filter_by(IsDeleted=0)
        if integration_code is not None:
            integration_datas = integration_datas.filter_by(Code=integration_code)
        return integration_datas.all()

    def start_operation_old(self, integration_code: str = None, job_id=None):
        """
        Integration starting operation
        """
        self.sql_logger.info(f'Data Integration is Begin with data:{integration_code}', job_id=job_id)
        integration_datas = self.get_integration_datas(integration_code)

        if integration_datas is None or len(integration_datas) == 0:
            self.sql_logger.info('Data Integration is completed with no result', job_id=job_id)
            return None
        for integration_data in integration_datas:

            # Source and target database managers instantiate
            source_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 0][0]
            target_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 1][0]
            source_connection_manager = self.connection_provider.get_connection(source_connection)
            target_connection_manager = self.connection_provider.get_connection(target_connection)

            # Pre exec job
            pre_execution = [x for x in integration_data.ExecutionJobs if x.IsPre == 1]
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
                f"{integration_data.Code} - {target_connection.Schema}.{target_connection.TableName} integration is began",
                job_id=job_id)

            column_rows, final_executable, related_columns = PdiUtils.get_row_column_and_values(
                target_connection.Connection.Database.ConnectorType.Name, target_connection.Schema,
                target_connection.TableName, integration_data.Columns)

            data_count = \
                source_connection_manager.fetch(
                    PdiUtils.count_table(source_connection.Schema, source_connection.TableName,
                                         source_connection.Connection.Database.ConnectorType.Name))[0][0]
            self.pdi_config.limit = 10000
            executable_scripts = PdiUtils.prepare_executable_scripts(data_count=data_count,
                                                                     source_connector_type=source_connection.Connection.Database.ConnectorType.Name,
                                                                     source_schema=source_connection.Schema,
                                                                     source_table_name=source_connection.TableName,
                                                                     column_rows=column_rows,
                                                                     limit=self.pdi_config.limit)

            # Delete if target data truncate is true
            if integration_data.IsTargetTruncate:
                target_connection_manager.delete(
                    PdiUtils.truncate_table(target_connection.Schema, target_connection.TableName,
                                            target_connection.Connection.Database.ConnectorType.Name))
            for executable_script in executable_scripts:
                # Extracted data fetched from source database
                extracted_data = source_connection_manager.fetch(executable_script)
                # Insert rows preparing
                inserted_rows = PdiUtils.prepare_insert_row(extracted_data, related_columns)
                # rows inserted to database
                target_connection_manager.insert_many(final_executable, inserted_rows)

            # Post exec job
            post_execution = [x for x in integration_data.ExecutionJobs if x.IsPost == 1]
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
                f"{integration_data.Code} - {target_connection.Schema}.{target_connection.TableName} integration is completed",
                job_id=job_id)

        self.sql_logger.info('Data Integration is completed', job_id=job_id)

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

    def start_operation(self, integration_code: str = None, job_id=None):  # parallel_
        """
        Integration starting operation
        """
        self.sql_logger.info(f'Data Integration is Begin with data:{integration_code}', job_id=job_id)
        integration_datas = self.get_integration_datas(integration_code)

        if integration_datas is None or len(integration_datas) == 0:
            self.sql_logger.info('Data Integration is completed with no result', job_id=job_id)
            return None
        for integration_data in integration_datas:

            # Source and target database managers instantiate
            source_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 0][0]
            target_connection = [x for x in integration_data.Connections if x.SourceOrTarget == 1][0]
            source_connection_manager = self.connection_provider.get_connection(source_connection)
            target_connection_manager = self.connection_provider.get_connection(target_connection)

            # Pre exec job
            pre_execution = [x for x in integration_data.ExecutionJobs if x.IsPre == 1]
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
                f"{integration_data.Code} - {target_connection.Schema}.{target_connection.TableName} integration is began",
                job_id=job_id)

            data_count = \
                source_connection_manager.fetch(
                    PdiUtils.count_table(source_connection.Schema, source_connection.TableName,
                                         source_connection.Connection.Database.ConnectorType.Name))[0][0]

            # Delete if target data truncate is true
            if integration_data.IsTargetTruncate:
                target_connection_manager.delete(
                    PdiUtils.truncate_table(target_connection.Schema, target_connection.TableName,
                                            target_connection.Connection.Database.ConnectorType.Name))
            limit = int(self.pdi_config.limit)
            process_count = int(self.pdi_config.process_count)
            do_parallel = bool(self.pdi_config.do_parallel)
            if do_parallel and data_count > limit * process_count:
                # Integration Start
                self.sql_logger.info(
                    f"{integration_data.Code} - operation will execute parallel. {process_count}-{limit}",
                    job_id=job_id)
                limit_modifiers = PdiUtils.get_limit_modifiers(data_count=data_count, limit=limit)
                self.process_service.start_parallel_process(process_id=integration_data.Id, datas=limit_modifiers,
                                                            process_count=process_count,
                                                            process_method=DataOperationService.parallel_operation,
                                                            result_method=DataOperationService.parallel_operation_result)
            else:
                self.sql_logger.info(f"{integration_data.Code} - operation will execute serial. {limit}", job_id=job_id)
                column_rows, final_executable, related_columns = PdiUtils.get_row_column_and_values(
                    target_connection.Connection.Database.ConnectorType.Name, target_connection.Schema,
                    target_connection.TableName, integration_data.Columns)
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
            post_execution = [x for x in integration_data.ExecutionJobs if x.IsPost == 1]
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
                f"{integration_data.Code} - {target_connection.Schema}.{target_connection.TableName} integration is completed",
                job_id=job_id)

        self.sql_logger.info('Data Integration is completed', job_id=job_id)
