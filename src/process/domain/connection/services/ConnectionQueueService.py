from injector import inject

from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from infrastructure.exceptions.OperationalException import OperationalException
from models.dao.connection import ConnectionQueue
from models.dao.connection.Connection import Connection
from models.viewmodels.connection.CreateConnectionQueueModel import CreateConnectionQueueModel


class ConnectionQueueService(IScoped):

    @inject
    def __init__(self,
                 connector_type_service: ConnectorTypeService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connection_queue_repository = repository_provider.get(ConnectionQueue)
        self.connector_type_service = connector_type_service

    def create(self, connection: Connection, model: CreateConnectionQueueModel) -> ConnectionQueue:
        """
        Create Queue connection
        """
        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        if connector_type is None:
            raise OperationalException(f"{model.ConnectorTypeName} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{model.ConnectorTypeName} incompatible with {connection.ConnectionType.Name}")
        connection_queue = ConnectionQueue(Connection=connection,
                                           ConnectorType=connector_type,
                                           Protocol=model.Protocol,
                                           Mechanism=model.Mechanism)

        self.connection_queue_repository.insert(connection_queue)
        return connection_queue

    def update(self, connection: Connection, model: CreateConnectionQueueModel) -> ConnectionQueue:
        """
        Update Queue connection
        """

        connection_queue = self.connection_queue_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        if connector_type is None:
            raise OperationalException(f"{model.ConnectorTypeName} not found")

        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{model.ConnectorTypeName} incompatible with {connection.ConnectionType.Name}")
        connection_queue.ConnectorType = connector_type
        connection_queue.Protocol = model.Protocol
        connection_queue.Mechanism = model.Mechanism
        return connection_queue

    def delete(self, id: int):
        """
        Delete Queue connection
        """

        self.connection_queue_repository.delete_by_id(id)
