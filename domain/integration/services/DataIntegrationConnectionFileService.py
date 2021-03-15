from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnectionFile
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.CreateDataIntegrationConnectionFileModel import \
    CreateDataIntegrationConnectionFileModel


class DataIntegrationConnectionFileService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_connection_file_repository: Repository[DataIntegrationConnectionFile] = \
            Repository[DataIntegrationConnectionFile](database_session_manager)

    #######################################################################################
    def get_by_data_integration_connection_id(self,
                                              data_integration_connection_id: int) -> DataIntegrationConnectionFile:
        entity = self.data_integration_connection_file_repository.first(IsDeleted=0,
                                                                        DataIntegrationConnectionId=data_integration_connection_id,
                                                                        )
        return entity

    def insert(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionFileModel) -> DataIntegrationConnectionFile:
        data_integration_connection_file = DataIntegrationConnectionFile(FileName=data.FileName,
                                                                             DataIntegrationConnection=data_integration_connection)
        self.data_integration_connection_file_repository.insert(data_integration_connection_file)
        return data_integration_connection_file

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionFileModel) -> DataIntegrationConnectionFile:
        data_integration_connection_file = self.get_by_data_integration_connection_id(
            data_integration_connection_id=data_integration_connection.Id,
        )
        data_integration_connection_file.DataIntegrationConnection = data_integration_connection
        data_integration_connection_file.FileName = data.FileName
        return data_integration_connection_file

    def delete(self, id: int):
        self.data_integration_connection_file_repository.delete_by_id(id)
