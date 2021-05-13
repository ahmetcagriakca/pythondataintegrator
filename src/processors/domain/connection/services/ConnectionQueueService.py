from injector import inject

from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from models.dao.connection import ConnectionQueue
from models.dao.connection.Connection import Connection
from models.viewmodels.connection.ConnectionQueue import ConnectionQueue


class ConnectionQueueService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 crypto_service: CryptoService,
                 connector_type_service: ConnectorTypeService
                 ):
        self.connector_type_service = connector_type_service
        self.crypto_service = crypto_service
        self.database_session_manager = database_session_manager
        self.connection_queue_repository: Repository[ConnectionQueue] = Repository[ConnectionQueue](
            database_session_manager)

    def create(self, connection: Connection, model: ConnectionQueue) -> ConnectionQueue:
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

    def update(self, connection: Connection, model: ConnectionQueue) -> ConnectionQueue:
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
