from injector import inject
from domain.connection.services.ConnectionService import ConnectionService
from domain.integration.services.DataIntegrationColumnService import DataIntegrationColumnService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from models.dao.integration import DataIntegrationConnectionDatabase
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.enums import ConnectionTypes
from models.viewmodels.integration.CreateDataIntegrationConnectionDatabaseModel import \
    CreateDataIntegrationConnectionDatabaseModel
from models.viewmodels.integration.CreateDataIntegrationModel import CreateDataIntegrationModel
from models.dao.integration.DataIntegration import DataIntegration


class DataIntegrationConnectionDatabaseService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_connection_database_repository: Repository[DataIntegrationConnectionDatabase] = \
            Repository[DataIntegrationConnectionDatabase](database_session_manager)

    #######################################################################################
    def get_by_data_integration_connection_id(self, data_integration_connection_id: int) -> DataIntegrationConnectionDatabase:
        entity = self.data_integration_connection_database_repository.first(IsDeleted=0,
                                                                            DataIntegrationConnectionId=data_integration_connection_id,
                                                                            )
        return entity

    def insert(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionDatabaseModel) -> DataIntegrationConnectionDatabase:

        data_integration_connection_database = DataIntegrationConnectionDatabase(Schema=data.Schema,
                                                                                 TableName=data.TableName,
                                                                                 Query=data.Query,
                                                                                 DataIntegrationConnection=data_integration_connection)
        self.data_integration_connection_database_repository.insert(data_integration_connection_database)
        return data_integration_connection_database

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionDatabaseModel) -> DataIntegrationConnectionDatabase:
        data_integration_connection_database = self.get_by_data_integration_connection_id(
            data_integration_connection_id=data_integration_connection.Id,
        )
        data_integration_connection_database.DataIntegrationConnection = data_integration_connection
        data_integration_connection_database.Schema = data.Schema
        data_integration_connection_database.TableName = data.TableName
        data_integration_connection_database.Query = data.Query
        return data_integration_connection_database

    def delete(self, id: int):
        self.data_integration_connection_database_repository.delete_by_id(id)
