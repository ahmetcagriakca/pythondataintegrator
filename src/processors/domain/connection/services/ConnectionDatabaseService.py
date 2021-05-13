from injector import inject

from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.OperationalException import OperationalException
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.viewmodels.connection.ConnectionDatabase import ConnectionDatabase


class ConnectionDatabaseService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 connector_type_service: ConnectorTypeService
                 ):
        self.connector_type_service = connector_type_service
        self.database_session_manager = database_session_manager
        self.connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
            database_session_manager)

    def create(self, connection: Connection, model: ConnectionDatabase) -> ConnectionDatabase:
        """
        Create Database connection
        """
        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        if connector_type is None:
            raise OperationalException(f"{model.ConnectorTypeName} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{model.ConnectorTypeName} incompatible with {connection.ConnectionType.Name}")
        connection_database = ConnectionDatabase(Connection=connection,
                                                 ConnectorType=connector_type,
                                                 Sid=model.Sid,
                                                 ServiceName=model.ServiceName,
                                                 DatabaseName=model.DatabaseName)

        self.connection_database_repository.insert(connection_database)
        return connection_database

    def update(self, connection: Connection, model: ConnectionDatabase) -> ConnectionDatabase:
        """
        Update Database connection
        """

        connection_database = self.connection_database_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        if connector_type is None:
            raise OperationalException(f"{model.ConnectorTypeName} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{model.ConnectorTypeName} incompatible with {connection.ConnectionType.Name}")
        connection_database.ConnectorType = connector_type
        connection_database.Sid = model.Sid
        connection_database.ServiceName = model.ServiceName
        connection_database.DatabaseName = model.DatabaseName
        return connection_database

    def delete(self, id: int):
        """
        Delete Database connection
        """

        self.connection_database_repository.delete_by_id(id)
