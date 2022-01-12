from typing import List

from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from pdip.integrator.connection.domain.enums import ConnectionTypes

from src.application.connection.services.ConnectionService import ConnectionService
from src.application.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from src.application.integration.services.DataIntegrationConnectionBigDataService import \
    DataIntegrationConnectionBigDataService
from src.application.integration.services.DataIntegrationConnectionDatabaseService import \
    DataIntegrationConnectionDatabaseService
from src.application.integration.services.DataIntegrationConnectionFileService import \
    DataIntegrationConnectionFileService
from src.application.integration.services.DataIntegrationConnectionQueueService import \
    DataIntegrationConnectionQueueService
from src.application.operation.CreateDataOperation.CreateDataIntegrationRequest import CreateDataIntegrationRequest
from src.domain.integration.DataIntegration import DataIntegration
from src.domain.integration.DataIntegrationConnection import DataIntegrationConnection


class DataIntegrationConnectionService(IScoped):
    @inject
    def __init__(self,
                 data_integration_column_service: DataIntegrationColumnService,
                 data_integration_connection_database_service: DataIntegrationConnectionDatabaseService,
                 data_integration_connection_big_data_service: DataIntegrationConnectionBigDataService,
                 data_integration_connection_file_service: DataIntegrationConnectionFileService,
                 data_integration_connection_queue_service: DataIntegrationConnectionQueueService,
                 connection_service: ConnectionService,
                 repository_provider: RepositoryProvider,
                 ):
        self.data_integration_connection_big_data_service = data_integration_connection_big_data_service
        self.repository_provider = repository_provider
        self.data_integration_connection_repository = repository_provider.get(DataIntegrationConnection)
        self.data_integration_connection_queue_service = data_integration_connection_queue_service
        self.data_integration_connection_file_service = data_integration_connection_file_service
        self.data_integration_connection_database_service = data_integration_connection_database_service
        self.connection_service = connection_service
        self.data_integration_column_service = data_integration_column_service

    #######################################################################################
    def get_by_id(self, id: int) -> DataIntegrationConnection:
        entity = self.data_integration_connection_repository.first(IsDeleted=0, Id=id)
        return entity

    def get_all_by_id(self, id: int) -> List[DataIntegrationConnection]:
        entities = self.data_integration_connection_repository.filter_by(IsDeleted=0,
                                                                         Id=id)
        return entities

    def get_source_connection(self, data_integration_id: int) -> DataIntegrationConnection:
        entity = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                   DataIntegrationId=data_integration_id,
                                                                   SourceOrTarget=0)
        return entity

    def get_target_connection(self, data_integration_id: int) -> DataIntegrationConnection:
        entity = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                   DataIntegrationId=data_integration_id,
                                                                   SourceOrTarget=1)
        return entity

    def insert(self,
               data_integration: DataIntegration,
               data: CreateDataIntegrationRequest):

        source_connection = None
        if data.SourceConnections is not None and data.SourceConnections.ConnectionName is not None and data.SourceConnections.ConnectionName != '':
            source = self.connection_service.get_by_name(name=data.SourceConnections.ConnectionName)
            if source is None:
                raise OperationalException(
                    f"{data_integration.Code} - {data.SourceConnections.ConnectionName} source connection not found")
            source_connection = DataIntegrationConnection(
                SourceOrTarget=0, DataIntegration=data_integration, Connection=source)
            if source.ConnectionType.Id == ConnectionTypes.Sql.value:
                if source_connection is not None \
                        and (
                        data.SourceConnections.Database.Query is None or data.SourceConnections.Database.Query == '') \
                        and data.SourceConnections.Database.Schema is not None and data.SourceConnections.Database.Schema != '' and data.SourceConnections.Database.TableName is not None and data.SourceConnections.Database.TableName != '':
                    data.SourceConnections.Database.Query = self.data_integration_column_service.get_source_query(
                        connection=source,
                        data_integration=data_integration,
                        schema=data.SourceConnections.Database.Schema,
                        table_name=data.SourceConnections.Database.TableName)
                self.data_integration_connection_database_service.insert(data_integration_connection=source_connection,
                                                                         data=data.SourceConnections.Database)
            elif source.ConnectionType.Id == ConnectionTypes.BigData.value:
                if source_connection is not None \
                        and (
                        data.SourceConnections.BigData.Query is None or data.SourceConnections.BigData.Query == '') \
                        and data.SourceConnections.BigData.Schema is not None and data.SourceConnections.BigData.Schema != '' and data.SourceConnections.BigData.TableName is not None and data.SourceConnections.BigData.TableName != '':
                    data.SourceConnections.BigData.Query = self.data_integration_column_service.get_source_query(
                        connection=source,
                        data_integration=data_integration,
                        schema=data.SourceConnections.BigData.Schema,
                        table_name=data.SourceConnections.BigData.TableName)
                self.data_integration_connection_big_data_service.insert(data_integration_connection=source_connection,
                                                                         data=data.SourceConnections.BigData)
            elif source.ConnectionType.Id == ConnectionTypes.File.value:
                self.data_integration_connection_file_service.insert(data_integration_connection=source_connection,
                                                                     data=data.SourceConnections.File)
            elif source.ConnectionType.Id == ConnectionTypes.Queue.value:
                self.data_integration_connection_queue_service.insert(data_integration_connection=source_connection,
                                                                      data=data.SourceConnections.Queue)
            else:
                raise OperationalException("Connection Type not supported yet")
            self.data_integration_connection_repository.insert(source_connection)

        if data.TargetConnections is None or data.TargetConnections.ConnectionName is None or data.TargetConnections.ConnectionName == '':
            raise OperationalException(
                f"{data_integration.Code} - {data.TargetConnections.ConnectionName} target connection cannot be empty")

        target = self.connection_service.get_by_name(name=data.TargetConnections.ConnectionName)
        if target is None:
            raise OperationalException(
                f"{data_integration.Code} - {data.TargetConnections.ConnectionName} target connection not found")
        target_connection = DataIntegrationConnection(
            SourceOrTarget=1, DataIntegration=data_integration, Connection=target)
        if target.ConnectionType.Id == ConnectionTypes.Sql.value:
            if data.TargetConnections.Database.Query is None or data.TargetConnections.Database.Query == '':
                data.TargetConnections.Database.Query = self.data_integration_column_service.get_target_query(
                    connection=target,
                    data_integration=data_integration,
                    schema=data.TargetConnections.Database.Schema,
                    table_name=data.TargetConnections.Database.TableName)
            self.data_integration_connection_database_service.insert(data_integration_connection=target_connection,
                                                                     data=data.TargetConnections.Database)
        elif target.ConnectionType.Id == ConnectionTypes.BigData.value:
            if data.TargetConnections.BigData.Query is None or data.TargetConnections.BigData.Query == '':
                data.TargetConnections.BigData.Query = self.data_integration_column_service.get_target_query(
                    connection=target,
                    data_integration=data_integration,
                    schema=data.TargetConnections.BigData.Schema,
                    table_name=data.TargetConnections.BigData.TableName)
            self.data_integration_connection_big_data_service.insert(data_integration_connection=target_connection,
                                                                     data=data.TargetConnections.BigData)
        elif target.ConnectionType.Id == ConnectionTypes.File.value:
            self.data_integration_connection_file_service.insert(data_integration_connection=target_connection,
                                                                 data=data.TargetConnections.File)
        elif target.ConnectionType.Id == ConnectionTypes.Queue.value:
            self.data_integration_connection_queue_service.insert(data_integration_connection=target_connection,
                                                                  data=data.TargetConnections.Queue)
        else:
            raise OperationalException("Connection Type not supported yet")
        self.data_integration_connection_repository.insert(target_connection)

    def update(self,
               data_integration: DataIntegration,
               data: CreateDataIntegrationRequest):

        source_connection = None
        if data.SourceConnections is not None and data.SourceConnections.ConnectionName is not None and data.SourceConnections.ConnectionName != '':

            source_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                                  DataIntegration=data_integration,
                                                                                  SourceOrTarget=0)
            source = self.connection_service.get_by_name(name=data.SourceConnections.ConnectionName)
            if source is None:
                raise OperationalException(
                    f"{data_integration.Code} - {data.SourceConnections.ConnectionName} source connection not found")
            source_connection.Connection = source
            if source.ConnectionType.Id == ConnectionTypes.Sql.value:
                if (
                        data.SourceConnections.Database.Query is None or data.SourceConnections.Database.Query == '') \
                        and data.SourceConnections.Database.Schema is not None and data.SourceConnections.Database.Schema != '' and data.SourceConnections.Database.TableName is not None and data.SourceConnections.Database.TableName != '':
                    data.SourceConnections.Database.Query = self.data_integration_column_service.get_source_query(
                        connection=source,
                        data_integration=data_integration,
                        schema=data.SourceConnections.Database.Schema,
                        table_name=data.SourceConnections.Database.TableName)
                if source_connection.Database is not None:
                    self.data_integration_connection_database_service.update(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.Database)
                else:
                    self.data_integration_connection_database_service.insert(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.Database)
            elif source.ConnectionType.Id == ConnectionTypes.BigData.value:
                if (
                        data.SourceConnections.BigData.Query is None or data.SourceConnections.BigData.Query == '') \
                        and data.SourceConnections.BigData.Schema is not None and data.SourceConnections.BigData.Schema != '' and data.SourceConnections.BigData.TableName is not None and data.SourceConnections.BigData.TableName != '':
                    data.SourceConnections.BigData.Query = self.data_integration_column_service.get_source_query(
                        connection=source,
                        data_integration=data_integration,
                        schema=data.SourceConnections.BigData.Schema,
                        table_name=data.SourceConnections.BigData.TableName)
                if source_connection.BigData is not None:
                    self.data_integration_connection_big_data_service.update(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.BigData)
                else:
                    self.data_integration_connection_big_data_service.insert(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.BigData)
            elif source.ConnectionType.Id == ConnectionTypes.File.value:
                if source_connection.File is not None:
                    self.data_integration_connection_file_service.update(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.File)
                else:
                    self.data_integration_connection_file_service.insert(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.File)
            elif source.ConnectionType.Id == ConnectionTypes.Queue.value:
                if source_connection.Queue is not None:
                    self.data_integration_connection_queue_service.update(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.Queue)
                else:
                    self.data_integration_connection_queue_service.insert(
                        data_integration_connection=source_connection,
                        data=data.SourceConnections.Queue)
            else:
                raise OperationalException("Connection Type not supported yet")

        if data.TargetConnections.ConnectionName is None or data.TargetConnections.ConnectionName == '':
            raise OperationalException(
                f"{data_integration.Code} - {data.TargetConnections.ConnectionName} target connection cannot be empty")
        target_connection = self.data_integration_connection_repository.first(IsDeleted=0,
                                                                              DataIntegration=data_integration,
                                                                              SourceOrTarget=1)
        target = self.connection_service.get_by_name(name=data.TargetConnections.ConnectionName)
        if target is None:
            raise OperationalException(
                f"{data_integration.Code} - {data.TargetConnections.ConnectionName} target connection not found")
        target_connection.Connection = target
        if target.ConnectionType.Id == ConnectionTypes.Sql.value:
            if data.TargetConnections.Database.Query is None or data.TargetConnections.Database.Query == '':
                data.TargetConnections.Database.Query = self.data_integration_column_service.get_target_query(
                    connection=target,
                    data_integration=data_integration,
                    schema=data.TargetConnections.Database.Schema,
                    table_name=data.TargetConnections.Database.TableName)
            if target_connection.Database is not None:
                self.data_integration_connection_database_service.update(data_integration_connection=target_connection,
                                                                         data=data.TargetConnections.Database)
            else:
                self.data_integration_connection_database_service.insert(data_integration_connection=target_connection,
                                                                         data=data.TargetConnections.Database)
        elif target.ConnectionType.Id == ConnectionTypes.BigData.value:
            if data.TargetConnections.BigData.Query is None or data.TargetConnections.BigData.Query == '':
                data.TargetConnections.BigData.Query = self.data_integration_column_service.get_target_query(
                    connection=target,
                    data_integration=data_integration,
                    schema=data.TargetConnections.BigData.Schema,
                    table_name=data.TargetConnections.BigData.TableName)
            if target_connection.BigData is not None:
                self.data_integration_connection_big_data_service.update(data_integration_connection=target_connection,
                                                                         data=data.TargetConnections.BigData)
            else:
                self.data_integration_connection_big_data_service.insert(data_integration_connection=target_connection,
                                                                         data=data.TargetConnections.BigData)
        elif target.ConnectionType.Id == ConnectionTypes.File.value:
            if target_connection.File is not None:
                self.data_integration_connection_file_service.update(
                    data_integration_connection=target_connection,
                    data=data.TargetConnections.File)
            else:
                self.data_integration_connection_file_service.insert(
                    data_integration_connection=target_connection,
                    data=data.TargetConnections.File)
        elif target.ConnectionType.Id == ConnectionTypes.Queue.value:
            if target_connection.Queue is not None:
                self.data_integration_connection_queue_service.update(
                    data_integration_connection=target_connection,
                    data=data.TargetConnections.Queue)
            else:
                self.data_integration_connection_queue_service.insert(
                    data_integration_connection=target_connection,
                    data=data.TargetConnections.Queue)
        else:
            raise OperationalException("Connection Type not supported yet")
        self.data_integration_connection_repository.insert(target_connection)

        return data_integration

    def delete(self, id: int):
        data_integration_connection = self.get_by_id(id=id)
        if data_integration_connection is not None:
            if data_integration_connection.Database is not None:
                self.data_integration_connection_database_service.delete(id=data_integration_connection.Database.Id)
            if data_integration_connection.BigData is not None:
                self.data_integration_connection_big_data_service.delete(id=data_integration_connection.BigData.Id)
            if data_integration_connection.File is not None:
                self.data_integration_connection_file_service.delete(id=data_integration_connection.File.Id)
            if data_integration_connection.Queue is not None:
                self.data_integration_connection_queue_service.delete(id=data_integration_connection.Queue.Id)
            self.data_integration_connection_repository.delete_by_id(id)
