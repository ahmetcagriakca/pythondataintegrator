from injector import inject

from domain.integration.services.DataIntegrationConnectionFileCsvService import DataIntegrationConnectionFileCsvService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnectionFile
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.DataIntegrationConnectionFile import \
    DataIntegrationConnectionFile


class DataIntegrationConnectionFileService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 data_integration_connection_file_csv_service: DataIntegrationConnectionFileCsvService,

                 ):
        self.data_integration_connection_file_csv_service = data_integration_connection_file_csv_service
        self.database_session_manager = database_session_manager
        self.data_integration_connection_file_repository: Repository[DataIntegrationConnectionFile] = \
            Repository[DataIntegrationConnectionFile](database_session_manager)

    #######################################################################################
    def get_by_id(self, id: int) -> DataIntegrationConnectionFile:
        entity = self.data_integration_connection_file_repository.first(IsDeleted=0, Id=id)
        return entity

    def get_by_data_integration_connection_id(self,
                                              data_integration_connection_id: int) -> DataIntegrationConnectionFile:
        entity = self.data_integration_connection_file_repository.first(IsDeleted=0,
                                                                        DataIntegrationConnectionId=data_integration_connection_id,
                                                                        )
        return entity

    def insert(self,
               data_integration_connection: DataIntegrationConnection,
               data: DataIntegrationConnectionFile) -> DataIntegrationConnectionFile:
        data_integration_connection_file = DataIntegrationConnectionFile(
            Folder=data.Folder,
            FileName=data.FileName,
            DataIntegrationConnection=data_integration_connection)
        if data.Csv is not None:
            self.data_integration_connection_file_csv_service.insert(
                data_integration_connection_file=data_integration_connection_file, data=data.Csv)
        self.data_integration_connection_file_repository.insert(data_integration_connection_file)
        return data_integration_connection_file

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: DataIntegrationConnectionFile) -> DataIntegrationConnectionFile:
        data_integration_connection_file = self.get_by_data_integration_connection_id(
            data_integration_connection_id=data_integration_connection.Id,
        )
        data_integration_connection_file.DataIntegrationConnection = data_integration_connection
        data_integration_connection_file.Folder = data.Folder
        data_integration_connection_file.FileName = data.FileName

        if data.Csv is not None and data_integration_connection_file.Csv is None:
            self.data_integration_connection_file_csv_service.insert(
                data_integration_connection_file=data_integration_connection_file, data=data.Csv)
        elif data.Csv is not None and data_integration_connection_file.Csv is not None:
            self.data_integration_connection_file_csv_service.update(
                data_integration_connection_file=data_integration_connection_file, data=data.Csv)
        elif data.Csv is None and data_integration_connection_file.Csv is not None:
            self.data_integration_connection_file_csv_service.delete(
                id=data_integration_connection_file.Csv.Id)
        return data_integration_connection_file

    def delete(self, id: int):

        entity = self.get_by_id(id=id)
        if entity is not None:
            if entity.Csv is not None:
                self.data_integration_connection_file_csv_service.delete(
                    id=entity.Csv.Id)
            self.data_integration_connection_file_repository.delete_by_id(id)
