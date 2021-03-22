from injector import inject
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnectionQueue
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.viewmodels.integration.CreateDataIntegrationConnectionQueueModel import \
    CreateDataIntegrationConnectionQueueModel


class DataIntegrationConnectionQueueService(IScoped):
    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.data_integration_connection_queue_repository: Repository[DataIntegrationConnectionQueue] = \
            Repository[DataIntegrationConnectionQueue](database_session_manager)

    #######################################################################################
    def get_by_id(self, id: int) -> DataIntegrationConnectionQueue:
        entity = self.data_integration_connection_queue_repository.first(IsDeleted=0,
                                                                         Id=id,
                                                                         )
        return entity

    def get_by_data_integration_connection_id(self,
                                              data_integration_connection_id: int) -> DataIntegrationConnectionQueue:
        entity = self.data_integration_connection_queue_repository.first(IsDeleted=0,
                                                                         DataIntegrationConnectionId=data_integration_connection_id,
                                                                         )
        return entity

    def insert(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionQueueModel) -> DataIntegrationConnectionQueue:
        data_integration_connection_queue = DataIntegrationConnectionQueue(TopicName=data.TopicName,
                                                                              DataIntegrationConnection=data_integration_connection)
        self.data_integration_connection_queue_repository.insert(data_integration_connection_queue)
        return data_integration_connection_queue

    def update(self,
               data_integration_connection: DataIntegrationConnection,
               data: CreateDataIntegrationConnectionQueueModel) -> DataIntegrationConnectionQueue:
        data_integration_connection_queue = self.get_by_data_integration_connection_id(
            data_integration_connection_id=data_integration_connection.Id,
        )
        data_integration_connection_queue.DataIntegrationConnection = data_integration_connection
        data_integration_connection_queue.TopicName = data.TopicName
        return data_integration_connection_queue

    def delete(self, id: int):
        entity = self.get_by_id(id=id)
        if entity is not None:
            self.data_integration_connection_queue_repository.delete_by_id(id)
