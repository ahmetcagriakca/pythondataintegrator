from injector import inject

from domain.operation.CreateDataOperation.CreateDataIntegrationConnectionDatabaseRequest import \
    CreateDataIntegrationConnectionDatabaseRequest
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from models.dao.integration import DataIntegrationConnectionDatabase
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection


class DataIntegrationConnectionDatabaseService(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_integration_connection_database_repository = repository_provider.get(DataIntegrationConnectionDatabase)

    #######################################################################################
    def get_by_id(self, id: int) -> DataIntegrationConnectionDatabase:
        entity = self.data_integration_connection_database_repository.first(IsDeleted=0,
                                                                            Id=id,
                                                                            )
        return entity

    def get_by_data_integration_connection_id(self,
                                              data_integration_connection_id: int) -> DataIntegrationConnectionDatabase:
        entity = self.data_integration_connection_database_repository.first(IsDeleted=0,
                                                                            DataIntegrationConnectionId=data_integration_connection_id,
                                                                            )
        return entity

    def insert(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionDatabaseRequest) -> DataIntegrationConnectionDatabase:
        data_integration_connection_database = DataIntegrationConnectionDatabase(Schema=data.Schema,
                                                                                 TableName=data.TableName,
                                                                                 Query=data.Query,
                                                                                 DataIntegrationConnection=data_integration_connection)
        self.data_integration_connection_database_repository.insert(data_integration_connection_database)
        return data_integration_connection_database

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionDatabaseRequest) -> DataIntegrationConnectionDatabase:
        data_integration_connection_database = self.get_by_data_integration_connection_id(
            data_integration_connection_id=data_integration_connection.Id,
        )
        data_integration_connection_database.DataIntegrationConnection = data_integration_connection
        data_integration_connection_database.Schema = data.Schema
        data_integration_connection_database.TableName = data.TableName
        data_integration_connection_database.Query = data.Query
        return data_integration_connection_database

    def delete(self, id: int):
        entity = self.get_by_id(id=id)
        if entity is not None:
            self.data_integration_connection_database_repository.delete_by_id(id)
