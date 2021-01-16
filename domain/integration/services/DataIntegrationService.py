from typing import List

from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from infrastructor.utils.PdiUtils import PdiUtils
from models.dao.connection.Connection import Connection
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationExecutionJob import DataIntegrationExecutionJob
from models.viewmodels.integration.UpdateDataIntegrationModel import UpdateDataIntegrationModel


class DataIntegrationService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_repository: Repository[DataIntegration] = Repository[DataIntegration](
            database_session_manager)
        self.data_integration_column_repository: Repository[DataIntegrationColumn] = Repository[
            DataIntegrationColumn](
            database_session_manager)
        self.data_integration_connection_repository: Repository[DataIntegrationConnection] = Repository[
            DataIntegrationConnection](
            database_session_manager)
        self.data_integration_execution_job_repository: Repository[DataIntegrationExecutionJob] = \
            Repository[
                DataIntegrationExecutionJob](
                database_session_manager)
        self.connection_repository: Repository[Connection] = Repository[Connection](database_session_manager)
        self.sql_logger = sql_logger

    #######################################################################################

    def get_data_integrations(self) -> List[DataIntegration]:
        """
        Data data_integration data preparing
        """
        integration_datas = self.data_integration_repository.filter_by(IsDeleted=0)
        return integration_datas.all()

    def create_data_integration(self, data: CreateDataIntegrationModel):
        if data.Code is not None and data.Code != "":
            data_integration = self.data_integration_repository.first(IsDeleted=0, Code=data.Code)
            if data_integration is not None:
                raise OperationalException("Code already exists")
        else:
            raise OperationalException("Code required")
        data_integration = self.insert_data_integration(data)
        data_integration_result = self.data_integration_repository.first(IsDeleted=0, Id=data_integration.Id)
        return data_integration_result

    def insert_data_integration(self, data: CreateDataIntegrationModel) -> DataIntegration:
        if data.IsTargetTruncate \
                and (data.TargetSchema is not None and data.TargetSchema != '') \
                and (data.TargetTableName is not None and data.TargetTableName != ''):
            raise OperationalException("TargetSchema and TargetTableName cannot be empty if IsTargetTruncate is true")

        data_integration = DataIntegration(Code=data.Code, IsTargetTruncate=data.IsTargetTruncate,
                                           IsDelta=data.IsDelta)
        self.data_integration_repository.insert(data_integration)

        source_columns_list = data.SourceColumns.split(",")
        target_columns_list = data.TargetColumns.split(",")
        if len(source_columns_list) != len(target_columns_list):
            raise OperationalException("Source and Target Column List must be equal")
        data_integration_columns = []
        for relatedColumn in source_columns_list:
            target_column_name = target_columns_list[source_columns_list.index(relatedColumn)]
            data_integration_column = DataIntegrationColumn(SourceColumnName=relatedColumn,
                                                            TargetColumnName=target_column_name,
                                                            DataIntegration=data_integration)
            data_integration_columns.append(data_integration_column)
            self.data_integration_column_repository.insert(data_integration_column)
        source_connection = None
        if data.SourceConnectionName is not None and data.SourceConnectionName != '':
            source = self.connection_repository.first(Name=data.SourceConnectionName)
            if source is None:
                raise OperationalException("Source Connection not found")
            source_connection = DataIntegrationConnection(
                SourceOrTarget=0, Schema=data.SourceSchema, TableName=data.SourceTableName, Query=data.SourceQuery,
                DataIntegration=data_integration, Connection=source)
            self.data_integration_connection_repository.insert(source_connection)

        if data.TargetConnectionName is not None and data.TargetConnectionName != '':
            target = self.connection_repository.first(Name=data.TargetConnectionName)
            if target is None:
                raise OperationalException("Target Connection not found")
            target_connection = DataIntegrationConnection(
                SourceOrTarget=1, Schema=data.TargetSchema, TableName=data.TargetTableName, Query=data.TargetQuery,
                DataIntegration=data_integration, Connection=target)
            self.data_integration_connection_repository.insert(target_connection)

            column_rows, related_columns, target_execute_query = PdiUtils.get_row_column_and_values(
                schema=target_connection.Schema, table_name=target_connection.TableName,
                data_integration_columns=data_integration_columns)
            selected_rows = PdiUtils.get_selected_rows(column_rows)
            if source_connection is not None and (source_connection.Query is None or source_connection.Query == ''):
                if source_connection.Schema is not None and source_connection.Schema != '' and source_connection.TableName is not None and source_connection.TableName != '':
                    query = f'SELECT {selected_rows} FROM "{source_connection.Schema}"."{source_connection.TableName}"'
                    source_connection.Query = query
            if target_connection.Query is None or target_connection.Query == '':
                target_connection.Query = target_execute_query

        if data.PreExecutions is not None and data.PreExecutions != "":
            self.insert_execution_job(data.PreExecutions, 1, 0, data_integration)
        if data.PostExecutions is not None and data.PostExecutions != "":
            self.insert_execution_job(data.PostExecutions, 0, 1, data_integration)

        self.database_session_manager.commit()
        return data_integration

    def insert_execution_job(self, ExecutionList, IsPre, IsPost, DataIntegration):
        pre_execution_list = ExecutionList.split(",")
        for preExecution in pre_execution_list:
            data_integration_execution_job = DataIntegrationExecutionJob(ExecutionProcedure=preExecution,
                                                                         IsPre=IsPre,
                                                                         IsPost=IsPost,
                                                                         DataIntegration=DataIntegration)
            self.data_integration_execution_job_repository.insert(data_integration_execution_job)

    def update_execution_job(self, ExecutionList, IsPre, IsPost, DataIntegration):
        execution_list = ExecutionList.split(",")
        for preExecution in execution_list:
            data_integration_execution_job = self.data_integration_execution_job_repository.first(
                IsDeleted=0,
                IsPre=IsPre,
                IsPost=IsPost,
                ExecutionProcedure=preExecution,
                DataIntegration=DataIntegration)
            if data_integration_execution_job is None:
                data_integration_execution_job = DataIntegrationExecutionJob(ExecutionProcedure=preExecution,
                                                                             IsPre=IsPre,
                                                                             IsPost=IsPost,
                                                                             DataIntegration=DataIntegration)
                self.data_integration_execution_job_repository.insert(data_integration_execution_job)

        data_integration_execution_jobs = self.data_integration_execution_job_repository.filter_by(
            IsDeleted=0,
            DataIntegration=DataIntegration,
            IsPre=IsPre,
            IsPost=IsPost)
        for data_integration_execution_job in data_integration_execution_jobs:
            check_execution = [execution for execution in execution_list if
                               execution == data_integration_execution_job.ExecutionProcedure]
            if not (check_execution is not None and len(check_execution) > 0 and check_execution[0] is not None):
                self.data_integration_execution_job_repository.delete(data_integration_execution_job)

    def delete_execution_job(self, IsPre, IsPost, DataIntegration):
        data_integration_execution_jobs = self.data_integration_execution_job_repository.filter_by(
            IsDeleted=0,
            DataIntegration=DataIntegration,
            IsPre=IsPre,
            IsPost=IsPost)
        for data_integration_execution_job in data_integration_execution_jobs:
            self.data_integration_execution_job_repository.delete(data_integration_execution_job)

    def update_data_integration(self, data: UpdateDataIntegrationModel):
        if data.Code is not None and data.Code != "":
            data_integration = self.data_integration_repository.first(IsDeleted=0, Code=data.Code)
            if data_integration is None:
                raise OperationalException("Code not exists")
        else:
            raise OperationalException("Code required")
        if data.IsTargetTruncate \
                and (data.TargetSchema is not None and data.TargetSchema != '') \
                and (data.TargetTableName is not None and data.TargetTableName != ''):
            raise OperationalException("TargetSchema and TargetTableName cannot be empty if IsTargetTruncate is true")
        data_integration.IsTargetTruncate = data.IsTargetTruncate
        data_integration.IsDelta = data.IsDelta

        source_columns_list = data.SourceColumns.split(",")
        target_columns_list = data.TargetColumns.split(",")

        if len(source_columns_list) != len(target_columns_list):
            raise OperationalException("Source and Target Column List must be equal")
        for source_column_name in source_columns_list:
            target_column_name = target_columns_list[source_columns_list.index(source_column_name)]
            data_integration_column = self.data_integration_column_repository.first(
                SourceColumnName=source_column_name, TargetColumnName=target_column_name,
                DataIntegration=data_integration)
            if data_integration_column is None:
                data_integration_column = DataIntegrationColumn(
                    SourceColumnName=source_column_name,
                    TargetColumnName=target_column_name,
                    DataIntegration=data_integration)
                self.data_integration_column_repository.insert(data_integration_column)
        for data_integration_column in data_integration.Columns:
            column_founded = False
            source_column_name = [source_column for source_column in source_columns_list if
                                  source_column == data_integration_column.SourceColumnName][0]
            if source_column_name is not None:
                target_column_name = target_columns_list[source_columns_list.index(source_column_name)]
                if target_column_name == data_integration_column.TargetColumnName:
                    column_founded = True
            if not column_founded:
                self.database_session_manager.session.delete(data_integration_column)
        source_connection = None
        if data.SourceConnectionName is not None and data.SourceConnectionName != '':
            source_connection = [x for x in data_integration.Connections if x.SourceOrTarget == 0][0]
            source = self.connection_repository.first(Name=data.SourceConnectionName)
            if source is None:
                raise OperationalException("Source Connection not found")
            source_connection.Connection = source
            source_connection.Schema = data.SourceSchema
            source_connection.Query = data.SourceQuery

        if data.TargetConnectionName is None or data.TargetConnectionName == '':
            raise OperationalException("Target Connection cannot be empty")
        target_connection = [x for x in data_integration.Connections if x.SourceOrTarget == 1][0]
        target = self.connection_repository.first(Name=data.TargetConnectionName)
        if target is None:
            raise OperationalException("Target Connection not found")
        target_connection.Connection = target
        target_connection.Schema = data.TargetSchema
        target_connection.TableName = data.TargetTableName
        target_connection.Query = data.TargetQuery
        data_integration_columns = self.data_integration_column_repository.filter_by(
            DataIntegration=data_integration)
        column_rows, related_columns, target_execute_query = PdiUtils.get_row_column_and_values(
            schema=target_connection.Schema, table_name=target_connection.TableName,
            data_integration_columns=data_integration_columns)
        selected_rows = PdiUtils.get_selected_rows(column_rows)
        if source_connection is not None and (source_connection.Query is None or source_connection.Query == ''):
            if source_connection.Schema is not None and source_connection.Schema != '' and source_connection.TableName is not None and source_connection.TableName != '':
                query = f'SELECT {selected_rows} FROM "{source_connection.Schema}"."{source_connection.TableName}"'
                source_connection.Query = query
        if target_connection.Query is None or target_connection.Query == '':
            target_connection.Query = target_execute_query

        if data.PreExecutions is not None and data.PreExecutions != "":
            self.update_execution_job(data.PreExecutions, True, False, data_integration)
        else:
            self.delete_execution_job(True, False, data_integration)
        if data.PostExecutions is not None and data.PostExecutions != "":
            self.update_execution_job(data.PostExecutions, False, True, data_integration)
        else:
            self.delete_execution_job(False, True, data_integration)

        self.database_session_manager.commit()
        return data_integration

    def delete_integration_data(self, code):
        self.sql_logger.info('PDI deletion for:' + code)

        if code is not None and code != "":
            data_integration = self.data_integration_repository.first(IsDeleted=0, Code=code)
            if data_integration is None:
                raise OperationalException("Code not found")
        else:
            return "Code required"
        for data_integration_connection in data_integration.Connections:
            data_integration_connection.IsDeleted = 1
        for data_integration_column in data_integration.Columns:
            data_integration_column.IsDeleted = 1
        data_integration.IsDeleted = 1
        self.database_session_manager.commit()
        message = f'PDI deletion for {code} is Completed'
        self.sql_logger.info(message)
