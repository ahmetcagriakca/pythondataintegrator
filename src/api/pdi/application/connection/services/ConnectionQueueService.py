from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from pdi.application.connection.services.ConnectorTypeService import ConnectorTypeService
from pdi.domain.connection import ConnectionQueue
from pdi.domain.connection.Connection import Connection


class ConnectionQueueService(IScoped):

    @inject
    def __init__(self,
                 connector_type_service: ConnectorTypeService,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connection_queue_repository = repository_provider.get(ConnectionQueue)
        self.connector_type_service = connector_type_service

    def create(self, connection: Connection, connector_type_name: str, protocol: str,
               mechanism: str) -> ConnectionQueue:
        """
        Create Queue connection
        """
        connector_type = self.connector_type_service.get_by_name(name=connector_type_name)
        if connector_type is None:
            raise OperationalException(f"{connector_type_name} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_name} incompatible with {connection.ConnectionType.Name}")
        connection_queue = ConnectionQueue(Connection=connection,
                                           ConnectorType=connector_type,
                                           Protocol=protocol,
                                           Mechanism=mechanism)

        self.connection_queue_repository.insert(connection_queue)
        return connection_queue

    def update(self, connection: Connection, connector_type_name: str, protocol: str,
               mechanism: str) -> ConnectionQueue:
        """
        Update Queue connection
        """

        connection_queue = self.connection_queue_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=connector_type_name)
        if connector_type is None:
            raise OperationalException(f"{connector_type_name} not found")

        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_name} incompatible with {connection.ConnectionType.Name}")
        connection_queue.ConnectorType = connector_type
        connection_queue.Protocol = protocol
        connection_queue.Mechanism = mechanism
        return connection_queue

    def delete(self, id: int):
        """
        Delete Queue connection
        """

        self.connection_queue_repository.delete_by_id(id)
