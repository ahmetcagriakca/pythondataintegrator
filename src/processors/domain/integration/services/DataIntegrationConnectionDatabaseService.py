from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnectionDatabase
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.DataIntegrationConnectionDatabase import \
    DataIntegrationConnectionDatabase


class DataIntegrationConnectionDatabaseService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_connection_database_repository: Repository[DataIntegrationConnectionDatabase] = \
            Repository[DataIntegrationConnectionDatabase](database_session_manager)

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
               data: DataIntegrationConnectionDatabase) -> DataIntegrationConnectionDatabase:
        data_integration_connection_database = DataIntegrationConnectionDatabase(Schema=data.Schema,
                                                                                 TableName=data.TableName,
                                                                                 Query=data.Query,
                                                                                 DataIntegrationConnection=data_integration_connection)
        self.data_integration_connection_database_repository.insert(data_integration_connection_database)
        return data_integration_connection_database

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: DataIntegrationConnectionDatabase) -> DataIntegrationConnectionDatabase:
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
