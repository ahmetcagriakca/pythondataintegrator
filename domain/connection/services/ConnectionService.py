from typing import List
from injector import inject

from domain.connection.services.ConnectionFileService import ConnectionFileService
from domain.connection.services.ConnectionDatabaseService import ConnectionDatabaseService
from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from domain.connection.services.ConnectionTypeService import ConnectionTypeService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from infrastructor.exception.OperationalException import OperationalException
from infrastructor.logging.SqlLogger import SqlLogger
from models.dao.connection.Connection import Connection
from models.enums.ConnectionTypes import ConnectionTypes
from models.viewmodels.connection.CreateConnectionDatabaseModel import CreateConnectionDatabaseModel
from models.viewmodels.connection.CreateConnectionFileModel import CreateConnectionFileModel


class ConnectionService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 sql_logger: SqlLogger,
                 connection_type_service: ConnectionTypeService,
                 connection_database_service: ConnectionDatabaseService,
                 connection_file_service: ConnectionFileService,
                 connection_secret_service: ConnectionSecretService
                 ):
        self.connection_secret_service = connection_secret_service
        self.connection_type_service = connection_type_service
        self.sql_logger: SqlLogger = sql_logger
        self.connection_file_service = connection_file_service
        self.connection_database_service = connection_database_service
        self.database_session_manager = database_session_manager
        self.connection_repository: Repository[Connection] = Repository[Connection](
            database_session_manager)

    def get_connections(self) -> List[Connection]:
        """
        Data data_integration data preparing
        """
        connections = self.connection_repository.filter_by(IsDeleted=0).all()
        return connections

    def get_by_name(self, name):
        connection = self.connection_repository.first(IsDeleted=0, Name=name)
        return connection

    def check_connection_name(self, name):
        connection = self.get_by_name(name=name)
        return connection is not None

    def create_connection(self, name: str, connection_type_name: str) -> Connection:
        connection_type = self.connection_type_service.get_by_name(name=connection_type_name)
        connection = Connection(Name=name, ConnectionType=connection_type)
        return connection

    def create_connection_file(self, connection_file_model: CreateConnectionFileModel) -> Connection:
        """
        Create File connection
        """

        connection = self.get_by_name(name=connection_file_model.Name)
        if connection is None:
            connection = self.create_connection(name=connection_file_model.Name,
                                                connection_type_name=ConnectionTypes.File.name)

            self.connection_secret_service.create(connection=connection, user=connection_file_model.User,
                                                  password=connection_file_model.Password)
            self.connection_file_service.create(connection=connection, model=connection_file_model)
        else:
            self.connection_secret_service.update(connection=connection, user=connection_file_model.User,
                                                  password=connection_file_model.Password)
            self.connection_file_service.update(connection=connection, model=connection_file_model)

        self.connection_repository.insert(connection)
        self.database_session_manager.commit()
        connection = self.connection_repository.first(Id=connection.Id)
        return connection

    def create_connection_database(self, connection_database_model: CreateConnectionDatabaseModel) -> Connection:
        """
        Create File connection
        """

        connection = self.connection_repository.first(IsDeleted=0, Name=connection_database_model.Name)

        if connection is None:
            connection = self.create_connection(name=connection_database_model.Name,
                                                connection_type_name=ConnectionTypes.Database.name)
            self.connection_secret_service.create(connection=connection, user=connection_database_model.User,
                                                  password=connection_database_model.Password)
            self.connection_database_service.create(connection, connection_database_model)
        else:
            self.connection_secret_service.update(connection=connection, user=connection_database_model.User,
                                                  password=connection_database_model.Password)
            self.connection_database_service.update(connection, connection_database_model)
        self.connection_repository.insert(connection)
        self.database_session_manager.commit()
        connection = self.connection_repository.first(Id=connection.Id)
        return connection

    def delete_connection(self, id: int):
        """
        Delete Database connection
        """
        connection = self.connection_repository.first(Id=id, IsDeleted=0)
        if connection is None:
            raise OperationalException("Connection Not Found")

        self.connection_repository.delete_by_id(connection.Id)
        if connection.Database is not None:
            self.connection_database_service.delete(id=connection.Database.Id)
        if connection.File is not None:
            self.connection_file_service.delete(id=connection.File.Id)

        if connection.ConnectionSecrets is not None:
            for connection_secret in connection.ConnectionSecrets:
                self.connection_secret_service.delete(id=connection_secret.Id)
        message = f'{connection.Name} connection deleted'
        self.sql_logger.info(message)
        self.database_session_manager.commit()
