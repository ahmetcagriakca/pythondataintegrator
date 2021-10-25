from typing import List

from injector import inject

from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from models.dao.connection import ConnectionServer
from models.dao.connection.Connection import Connection


class ConnectionServerService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        self.connection_server_repository = repository_provider.get(ConnectionServer)

    def get_by_id(self, id: int) -> ConnectionServer:
        entities = self.connection_server_repository.filter_by(IsDeleted=0, Id=id)
        return entities

    def get_by_connection_id(self, connection_id: int) -> ConnectionServer:
        entity = self.connection_server_repository.first(IsDeleted=0, ConnectionId=connection_id)
        return entity

    def get_all_by_connection_id(self, connection_id: int) -> List[ConnectionServer]:
        entities = self.connection_server_repository.filter_by(IsDeleted=0, ConnectionId=connection_id)
        return entities

    def get_by_server_info(self, connection_id: int, host: str, port: int) -> ConnectionServer:
        entity = self.connection_server_repository.first(IsDeleted=0, ConnectionId=connection_id, Host=host, Port=port)
        return entity

    def create(self, connection: Connection, host: str, port: int) -> ConnectionServer:
        """
        Create Server connection
        """
        if host is None or host=='':
            raise OperationalException("Host cannot be null")
        connection_server = ConnectionServer(Connection=connection,
                                               Host=host,
                                               Port=port)

        self.connection_server_repository.insert(connection_server)
        return connection_server

    def update(self, connection: Connection, host: str, port: int) -> ConnectionServer:
        """
        Update Server connection
        """
        if host is None or host=='':
            raise OperationalException("Host cannot be null")
        connection_server = self.get_by_connection_id(connection_id=connection.Id)
        connection_server.Host = host
        connection_server.Port = port
        return connection_server

    def delete(self, id: int):
        """
        Delete Server connection
        """

        self.connection_server_repository.delete_by_id(id)
