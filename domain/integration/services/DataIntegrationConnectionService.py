from injector import inject
from domain.connection.services.ConnectionService import ConnectionService
from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel
from models.dao.integration.DataIntegration import DataIntegration


class DataIntegrationConnectionService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 data_integration_column_service: DataIntegrationColumnService,
                 connection_service:ConnectionService
                 ):
        self.connection_service = connection_service
        self.data_integration_column_service = data_integration_column_service
        self.database_session_manager = database_session_manager
        self.data_integration_connection_repository: Repository[DataIntegrationConnection] = Repository[
            DataIntegrationConnection](
            database_session_manager)

    #######################################################################################

    def insert(self,
               data_integration: DataIntegration,
               data: CreateDataIntegrationModel):

        source_connection = None
        if data.SourceConnectionName is not None and data.SourceConnectionName != '':
            source = self.connection_service.get_by_name(name=data.SourceConnectionName)
            if source is None:
                raise OperationalException("Source Connection not found")
            source_connection = DataIntegrationConnection(
                SourceOrTarget=0, Schema=data.SourceSchema, TableName=data.SourceTableName, Query=data.SourceQuery,
                DataIntegration=data_integration, Connection=source)
            self.data_integration_connection_repository.insert(source_connection)

        if data.TargetConnectionName is None or data.TargetConnectionName == '':
            raise OperationalException("Target Connection cannot be empty")

        target = self.connection_service.get_by_name(name=data.TargetConnectionName)
        if target is None:
            raise OperationalException("Target Connection not found")
        target_connection = DataIntegrationConnection(
            SourceOrTarget=1, Schema=data.TargetSchema, TableName=data.TargetTableName, Query=data.TargetQuery,
            DataIntegration=data_integration, Connection=target)
        self.data_integration_connection_repository.insert(target_connection)

        if source_connection is not None \
                and (source_connection.Query is None or source_connection.Query == '') \
                and source_connection.Schema is not None and source_connection.Schema != '' and source_connection.TableName is not None and source_connection.TableName != '':
            source_connection.Query = self.data_integration_column_service.get_source_query(
                data_integration=data_integration,
                schema=source_connection.Schema,
                table_name=source_connection.TableName)
        if target_connection.Query is None or target_connection.Query == '':
            target_connection.Query = self.data_integration_column_service.get_target_query(
                data_integration=data_integration,
                schema=target_connection.Schema,
                table_name=target_connection.TableName)

    def update(self,
               data_integration: DataIntegration,
               data: CreateDataIntegrationModel):

        source_connection = None
        if data.SourceConnectionName is not None and data.SourceConnectionName != '':

            source_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                                  DataIntegration=data_integration,
                                                                                  SourceOrTarget=0)
            source = self.connection_service.get_by_name(name=data.SourceConnectionName)
            if source is None:
                raise OperationalException("Source Connection not found")
            source_connection.Connection = source
            source_connection.Schema = data.SourceSchema
            source_connection.Query = data.SourceQuery

        if data.TargetConnectionName is None or data.TargetConnectionName == '':
            raise OperationalException("Target Connection cannot be empty")
        target_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                              DataIntegration=data_integration,
                                                                              SourceOrTarget=1)
        target = self.connection_service.get_by_name(name=data.TargetConnectionName)
        if target is None:
            raise OperationalException("Target Connection not found")
        target_connection.Connection = target
        target_connection.Schema = data.TargetSchema
        target_connection.TableName = data.TargetTableName
        target_connection.Query = data.TargetQuery
        if source_connection is not None \
                and (source_connection.Query is None or source_connection.Query == '') \
                and source_connection.Schema is not None and source_connection.Schema != '' and source_connection.TableName is not None and source_connection.TableName != '':
            source_connection.Query = self.data_integration_column_service.get_source_query(
                data_integration=data_integration,
                schema=source_connection.Schema,
                table_name=source_connection.TableName)
        if target_connection.Query is None or target_connection.Query == '':
            target_connection.Query = self.data_integration_column_service.get_target_query(
                data_integration=data_integration,
                schema=target_connection.Schema,
                table_name=target_connection.TableName)

        return data_integration

    def delete(self, id: int):
        self.data_integration_connection_repository.delete_by_id(id)
