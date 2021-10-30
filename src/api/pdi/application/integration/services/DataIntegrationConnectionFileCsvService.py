from injector import inject
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.operation.CreateDataOperation.CreateDataIntegrationConnectionFileCsvRequest import \
    CreateDataIntegrationConnectionFileCsvRequest
from pdi.domain.integration import DataIntegrationConnectionFile, DataIntegrationConnectionFileCsv


class DataIntegrationConnectionFileCsvService(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_integration_connection_file_csv_repository = repository_provider.get(DataIntegrationConnectionFileCsv)

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
               data: CreateDataIntegrationConnectionFileCsvRequest) -> DataIntegrationConnectionFileCsv:
        data_integration_connection_file_csv = DataIntegrationConnectionFileCsv(
            HasHeader=data.HasHeader,
            Header=data.Header,
            Separator=data.Separator,
            DataIntegrationConnectionFile=data_integration_connection_file)
        self.data_integration_connection_file_csv_repository.insert(data_integration_connection_file_csv)
        return data_integration_connection_file_csv

    def update(self,
               data_integration_connection_file: DataIntegrationConnectionFile,
               data: CreateDataIntegrationConnectionFileCsvRequest) -> DataIntegrationConnectionFileCsv:
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
