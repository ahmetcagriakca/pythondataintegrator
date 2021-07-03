from typing import List

from injector import inject

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.connection import ConnectionServer
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase


class ConnectionServerService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 ):
        self.database_session_manager = database_session_manager
        self.connection_server_repository: Repository[ConnectionServer] = Repository[ConnectionServer](
            database_session_manager)

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
        connection_server = ConnectionServer(Connection=connection,
                                               Host=host,
                                               Port=port)

        self.connection_server_repository.insert(connection_server)
        return connection_server

    def update(self, connection: Connection, host: str, port: int) -> ConnectionServer:
        """
        Update Server connection
        """

        connection_server = self.get_by_connection_id(connection_id=connection.Id)
        connection_server.Host = host
        connection_server.Port = port
        return connection_server

    def delete(self, id: int):
        """
        Delete Server connection
        """

        self.connection_server_repository.delete_by_id(id)
