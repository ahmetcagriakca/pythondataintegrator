from typing import List

from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.connection.Connection import Connection
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.CreateIntegrationDataModel import CreateIntegrationDataModel
from models.dao.integration.DataIntegration import DataIntegration
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationExecutionJob import DataIntegrationExecutionJob


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
        self.pyhton_data_integration_execution_job_repository: Repository[DataIntegrationExecutionJob] = \
            Repository[
                DataIntegrationExecutionJob](
                database_session_manager)
        self.connection_repository: Repository[Connection] = Repository[Connection](database_session_manager)
        self.sql_logger = sql_logger

    #######################################################################################

    def get_data_integrations(self) -> List[DataIntegration]:
        """
        Data integration data preparing
        """
        integration_datas = self.data_integration_repository.filter_by(IsDeleted=0)
        return integration_datas.all()

    def create_integration_data(self, data: CreateIntegrationDataModel):
        self.sql_logger.info('PDI Insertion for:' + data.Code)

        if data.Code is not None and data.Code != "":
            pdi = self.data_integration_repository.first(IsDeleted=0, Code=data.Code)
            if pdi is not None:
                raise OperationalException("Code already exists")
        else:
            raise OperationalException("Code required")
        inserted_pdi = self.insert_configuration(data)
        self.sql_logger.info(f'PDI Insertion for {data.Code} is Completed')
        pdi = self.data_integration_repository.get_by_id(inserted_pdi.Id)
        return pdi

    def insert_configuration(self, data: CreateIntegrationDataModel) -> DataIntegration:

        data_integration = DataIntegration(Code=data.Code, IsTargetTruncate=data.IsTargetTruncate,
                                                        IsDelta=data.IsDelta)
        self.data_integration_repository.insert(data_integration)

        source = self.connection_repository.first(Id=data.SourceConnectionId)
        if source is None:
            raise OperationalException("Source Connection not found")
        source_connection = DataIntegrationConnection(
            SourceOrTarget=0, ConnectionId=data.SourceConnectionId, Schema=data.SourceSchema,
            TableName=data.SourceTableName, DataIntegration=data_integration, Connection=source)
        self.data_integration_connection_repository.insert(source_connection)

        target = self.connection_repository.first(Id=data.TargetConnectionId)
        if target is None:
            raise OperationalException("Target Connection not found")
        target_connection = DataIntegrationConnection(
            SourceOrTarget=1, ConnectionId=data.TargetConnectionId, Schema=data.TargetSchema,
            TableName=data.TargetTableName, DataIntegration=data_integration, Connection=target)
        self.data_integration_connection_repository.insert(target_connection)

        source_columns_list = data.SourceColumns.split(",")
        target_columns_list = data.TargetColumns.split(",")
        if len(source_columns_list) != len(target_columns_list):
            raise OperationalException("Source and Target Column List must be equal")
        for relatedColumn in source_columns_list:
            target_column_name = target_columns_list[source_columns_list.index(relatedColumn)]
            data_integration_column = DataIntegrationColumn(SourceColumnName=relatedColumn,
                                                                         TargetColumnName=target_column_name,
                                                                         DataIntegration=data_integration)
            self.data_integration_column_repository.insert(data_integration_column)

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
            self.pyhton_data_integration_execution_job_repository.insert(data_integration_execution_job)

    # def update_integration_data(self, data: CreateIntegrationDataModel):
    #     self.sql_logger.info('PDI Insertion for:' + data.Code)
    #
    #     if data.Code is not None and data.Code != "":
    #         data_integration = self.data_integration_repository.first(IsDeleted=0, Code=data.Code)
    #         if data_integration is None:
    #             raise OperationalException("Code not exists")
    #     else:
    #         raise OperationalException("Code required")
    #     data_integration.IsTargetTruncate = data.IsTargetTruncate
    #     data_integration.IsDelta = data.IsDelta
    #
    #     source_connection = data_integration.Connections[0]
    #     source_connection.ConnectionId = data.SourceConnectionId
    #     source_connection.Schema = data.SourceSchema
    #     source_connection.TableName = data.SourceTableName
    #
    #     target_connection = data_integration.Connections[1]
    #     target_connection.ConnectionId = data.SourceConnectionId
    #     target_connection.Schema = data.SourceSchema
    #     target_connection.TableName = data.SourceTableName
    #
    #     source_columns_list = data.SourceColumns.split(",")
    #     target_columns_list = data.TargetColumns.split(",")
    #
    #     if len(source_columns_list) != len(target_columns_list):
    #         raise OperationalException("Source and Target Column List must be equal")
    #     for relatedColumn in source_columns_list:
    #         target_column_name = target_columns_list[source_columns_list.index(relatedColumn)]
    #         data_integration_column = DataIntegrationColumn(SourceColumnName=relatedColumn,
    #                                                                      TargetColumnName=target_column_name,
    #                                                                      DataIntegration=data_integration)
    #         self.data_integration_column_repository.insert(data_integration_column)
    #
    #     if data.PreExecutions is not None and data.PreExecutions != "":
    #         self.insert_execution_job(data.PreExecutions, 1, 0, data_integration)
    #     if data.PostExecutions is not None and data.PostExecutions != "":
    #         self.insert_execution_job(data.PostExecutions, 0, 1, data_integration)
    #
    #     self.database_session_manager.commit()
    #     return data_integration

    def delete_integration_data(self, code):
        self.sql_logger.info('PDI deletion for:' + code)

        if code is not None and code != "":
            pdi = self.data_integration_repository.first(IsDeleted=0, Code=code)
            if pdi is None:
                raise OperationalException("Code not found")
        else:
            return "Code required"
        pdi.IsDeleted = 1
        self.database_session_manager.commit()
        message = f'PDI deletion for {code} is Completed'
        self.sql_logger.info(message)
