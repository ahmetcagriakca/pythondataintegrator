from typing import List
from injector import inject

from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionProvider import ConnectionProvider
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.connection.ConnectorType import ConnectorType
from models.dao.connection.ConnectionType import ConnectionType
from models.viewmodels.connection.CreateConnectionDatabaseModel import CreateConnectionDatabaseModel
from models.viewmodels.connection.UpdateConnectionDatabaseModel import UpdateConnectionDatabaseModel


class ConnectionService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 database_provider: ConnectionProvider,
                 crypto_service: CryptoService,
                 ):
        self.database_session_manager = database_session_manager
        self.connection_type_repository: Repository[ConnectionType] = Repository[ConnectionType](
            database_session_manager)
        self.connector_type_repository: Repository[ConnectorType] = Repository[ConnectorType](
            database_session_manager)
        self.connection_database_repository: Repository[ConnectionDatabase] = Repository[ConnectionDatabase](
            database_session_manager)
        self.connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)
        self.database_provider: ConnectionProvider = database_provider
        self.sql_logger: SqlLogger = sql_logger
        self.crypto_service = crypto_service

    def get_connection_types(self, ) -> List[ConnectionType]:
        """
        Data integration data preparing
        """
        connection_types = self.connection_type_repository.filter_by(IsDeleted=0).all()
        return connection_types

    def get_connector_types(self) -> List[ConnectorType]:
        """
        Data integration data preparing
        """
        connector_types = self.connector_type_repository.filter_by(IsDeleted=0).all()
        return connector_types

    def get_connections(self) -> List[Connection]:
        """
        Data integration data preparing
        """
        connections = self.connection_repository.filter_by(IsDeleted=0).all()
        return connections

    def get_connection_databases(self, ) -> List[ConnectionDatabase]:
        """
        Data integration data preparing
        """
        connection_databases = self.connection_database_repository.filter_by(IsDeleted=0).all()
        return connection_databases

    def check_connection_name(self, name):
        connection = self.connection_repository.first(Name=name)
        return connection is not None

    def create_connection_database(self,
                                   connection_database_model: CreateConnectionDatabaseModel) -> Connection:
        """
        Create Database connection
        """
        connection_type = self.connection_type_repository.first(Id=connection_database_model.ConnectionTypeId)
        if connection_type is None:
            raise OperationalException("Connection Type Not Found")
        if self.check_connection_name(connection_database_model.Name):
            raise OperationalException("Connection name already defined")
        connection = Connection(Name=connection_database_model.Name,
                                ConnectionType=connection_type)
        connector_type = self.connector_type_repository.first(Id=connection_database_model.ConnectorTypeId)
        if connector_type is None:
            raise OperationalException("Connector Type Not Found")
        connection_database = ConnectionDatabase(Connection=connection,
                                                 ConnectorType=connector_type,
                                                 Host=connection_database_model.Host,
                                                 Port=connection_database_model.Port, Sid=connection_database_model.Sid,
                                                 DatabaseName=connection_database_model.DatabaseName,
                                                 User=self.crypto_service.encrypt_code(
                                                     connection_database_model.User.encode()).decode(),
                                                 Password=self.crypto_service.encrypt_code(
                                                     connection_database_model.Password.encode()).decode())

        self.connection_repository.insert(connection)
        self.connection_database_repository.insert(connection_database)
        self.database_session_manager.commit()
        connection = self.connection_repository.first(Id=connection_database.Connection.Id)
        return connection

    def update_connection_database(self,
                                   connection_database_model: UpdateConnectionDatabaseModel) -> Connection:
        """
        Update Database connection
        """

        if self.check_connection_name(connection_database_model.Name):
            raise OperationalException("Connection name already defined")
        connection_database = self.connection_database_repository.first(Id=connection_database_model.Id)
        connection = connection_database.Connection
        connection.Name = connection_database_model.Name

        connector_type = self.connector_type_repository.first(Id=connection_database_model.ConnectorTypeId)
        if connector_type is None:
            raise OperationalException("Connector Type Not Found")
        connection_database.ConnectorType = connector_type
        connection_database.Host = connection_database_model.Host
        connection_database.Port = connection_database_model.Port
        connection_database.Sid = connection_database_model.Sid
        connection_database.DatabaseName = connection_database_model.DatabaseName
        connection_database.User = self.crypto_service.encrypt_code(connection_database_model.User.encode()).decode()
        connection_database.Password = self.crypto_service.encrypt_code(
            connection_database_model.Password.encode()).decode()

        self.database_session_manager.commit()
        connection = self.connection_repository.first(Id=connection_database.Connection.Id)
        return connection

    def delete_connection_database(self, id: int):
        """
        Delete Database connection
        """
        connection_database = self.connection_database_repository.first(Id=id, IsDeleted=0)
        if connection_database is None:
            raise OperationalException("Database Connection Not Found")

        self.connection_repository.delete_by_id(connection_database.ConnectionId)
        self.connection_database_repository.delete_by_id(connection_database.Id)
        message = f'{connection_database.Connection.Name} connection deleted'
        self.sql_logger.info(message)
        self.database_session_manager.commit()
