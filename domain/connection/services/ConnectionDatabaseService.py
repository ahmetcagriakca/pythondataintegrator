from injector import inject

from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.viewmodels.connection.CreateConnectionDatabaseModel import CreateConnectionDatabaseModel


class ConnectionDatabaseService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 crypto_service: CryptoService,
                 connector_type_service: ConnectorTypeService
                 ):
        self.connector_type_service = connector_type_service
        self.crypto_service = crypto_service
        self.database_session_manager = database_session_manager
        self.connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
            database_session_manager)

    def create(self, connection: Connection, model: CreateConnectionDatabaseModel) -> ConnectionDatabase:
        """
        Create Database connection
        """
        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        connection_database = ConnectionDatabase(Connection=connection,
                                                 ConnectorType=connector_type,
                                                 Host=model.Host,
                                                 Port=model.Port,
                                                 Sid=model.Sid,
                                                 ServiceName=model.ServiceName,
                                                 DatabaseName=model.DatabaseName)

        self.connection_database_repository.insert(connection_database)
        return connection_database

    def update(self, connection: Connection, model: CreateConnectionDatabaseModel) -> ConnectionDatabase:
        """
        Update Database connection
        """

        connection_database = self.connection_database_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        connection_database.ConnectorType = connector_type
        connection_database.Host = model.Host
        connection_database.Port = model.Port
        connection_database.Sid = model.Sid
        connection_database.ServiceName = model.ServiceName
        connection_database.DatabaseName = model.DatabaseName
        return connection_database

    def delete(self, id: int):
        """
        Delete Database connection
        """

        self.connection_database_repository.delete_by_id(id)
