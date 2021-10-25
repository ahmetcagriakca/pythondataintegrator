from injector import inject

from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase


class ConnectionDatabaseService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 connector_type_service: ConnectorTypeService
                 ):
        self.repository_provider = repository_provider
        self.connector_type_service = connector_type_service
        self.connection_database_repository = repository_provider.get(ConnectionDatabase)

    def create(self, connection: Connection, connector_type_name: str, sid: str, service_name: str,
               database_name: str) -> ConnectionDatabase:
        """
        Create Database connection
        """
        connector_type = self.connector_type_service.get_by_name(name=connector_type_name)
        if connector_type is None:
            raise OperationalException(f"{connector_type_name} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_name} incompatible with {connection.ConnectionType.Name}")
        connection_database = ConnectionDatabase(Connection=connection,
                                                 ConnectorType=connector_type,
                                                 Sid=sid,
                                                 ServiceName=service_name,
                                                 DatabaseName=database_name)

        self.connection_database_repository.insert(connection_database)
        return connection_database

    def update(self, connection: Connection, connector_type_name: str, sid: str, service_name: str,
               database_name: str) -> ConnectionDatabase:
        """
        Update Database connection
        """

        connection_database = self.connection_database_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=connector_type_name)
        if connector_type is None:
            raise OperationalException(f"{connector_type_name} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_name} incompatible with {connection.ConnectionType.Name}")
        connection_database.ConnectorType = connector_type
        connection_database.Sid = sid
        connection_database.ServiceName = service_name
        connection_database.DatabaseName = database_name
        return connection_database

    def delete(self, id: int):
        """
        Delete Database connection
        """

        self.connection_database_repository.delete_by_id(id)
