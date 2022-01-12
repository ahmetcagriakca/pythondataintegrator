from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.operation.CreateDataOperation.CreateDataIntegrationConnectionBigDataRequest import \
    CreateDataIntegrationConnectionBigDataRequest
from src.domain.integration import DataIntegrationConnectionBigData
from src.domain.integration.DataIntegrationConnection import DataIntegrationConnection


class DataIntegrationConnectionBigDataService(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.data_integration_connection_big_data_repository = repository_provider.get(
            DataIntegrationConnectionBigData)

    #######################################################################################
    def get_by_id(self, id: int) -> DataIntegrationConnectionBigData:
        entity = self.data_integration_connection_big_data_repository.first(IsDeleted=0,
                                                                            Id=id,
                                                                            )
        return entity

    def get_by_data_integration_connection_id(self,
                                              data_integration_connection_id: int) -> DataIntegrationConnectionBigData:
        entity = self.data_integration_connection_big_data_repository.first(IsDeleted=0,
                                                                            DataIntegrationConnectionId=data_integration_connection_id,
                                                                            )
        return entity

    def insert(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionBigDataRequest) -> DataIntegrationConnectionBigData:
        data_integration_connection_big_data = DataIntegrationConnectionBigData(Schema=data.Schema,
                                                                                TableName=data.TableName,
                                                                                Query=data.Query,
                                                                                DataIntegrationConnection=data_integration_connection)
        self.data_integration_connection_big_data_repository.insert(data_integration_connection_big_data)
        return data_integration_connection_big_data

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionBigDataRequest) -> DataIntegrationConnectionBigData:
        data_integration_connection_big_data = self.get_by_data_integration_connection_id(
            data_integration_connection_id=data_integration_connection.Id,
        )
        data_integration_connection_big_data.DataIntegrationConnection = data_integration_connection
        data_integration_connection_big_data.Schema = data.Schema
        data_integration_connection_big_data.TableName = data.TableName
        data_integration_connection_big_data.Query = data.Query
        return data_integration_connection_big_data

    def delete(self, id: int):
        entity = self.get_by_id(id=id)
        if entity is not None:
            self.data_integration_connection_big_data_repository.delete_by_id(id)
