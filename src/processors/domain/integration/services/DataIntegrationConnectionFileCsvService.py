from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnectionFile, DataIntegrationConnectionFileCsv
from models.viewmodels.integration import DataIntegrationConnectionFileCsv


class DataIntegrationConnectionFileCsvService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_connection_file_csv_repository: Repository[DataIntegrationConnectionFileCsv] = \
            Repository[DataIntegrationConnectionFileCsv](database_session_manager)

    #######################################################################################
    def get_by_id(self, id: int) -> DataIntegrationConnectionFileCsv:
        entity = self.data_integration_connection_file_csv_repository.first(IsDeleted=0,
                                                                            Id=id,
                                                                            )
        return entity

    def get_by_data_integration_connection_file_id(self,
                                                   data_integration_connection_file_id: int) -> DataIntegrationConnectionFileCsv:
        entity = self.data_integration_connection_file_csv_repository.first(IsDeleted=0,
                                                                            DataIntegrationConnectionFileId=data_integration_connection_file_id,
                                                                            )
        return entity

    def insert(self,
               data_integration_connection_file: DataIntegrationConnectionFile,
               data: DataIntegrationConnectionFileCsv) -> DataIntegrationConnectionFileCsv:
        data_integration_connection_file_csv = DataIntegrationConnectionFileCsv(
            HasHeader=data.HasHeader,
            Header=data.Header,
            Separator=data.Separator,
            DataIntegrationConnectionFile=data_integration_connection_file)
        self.data_integration_connection_file_csv_repository.insert(data_integration_connection_file_csv)
        return data_integration_connection_file_csv

    def update(self,
               data_integration_connection_file: DataIntegrationConnectionFile,
               data: DataIntegrationConnectionFileCsv) -> DataIntegrationConnectionFileCsv:
        data_integration_connection_file_csv = self.get_by_data_integration_connection_file_id(
            data_integration_connection_file_id=data_integration_connection_file.Id,
        )
        data_integration_connection_file_csv.DataIntegrationConnectionFile = data_integration_connection_file
        data_integration_connection_file_csv.HasHeader = data.HasHeader
        data_integration_connection_file_csv.Header = data.Header
        data_integration_connection_file_csv.Separator = data.Separator
        return data_integration_connection_file_csv

    def delete(self, id: int):
        entity = self.get_by_id(id=id)
        if entity is not None:
            self.data_integration_connection_file_csv_repository.delete_by_id(id)
