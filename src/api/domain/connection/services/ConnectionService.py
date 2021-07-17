from typing import List
from injector import inject

from domain.connection.CreateConnectionDatabase.CreateConnectionDatabaseRequest import CreateConnectionDatabaseRequest
from domain.connection.CreateConnectionFile.CreateConnectionFileRequest import CreateConnectionFileRequest
from domain.connection.CreateConnectionQueue.CreateConnectionQueueRequest import CreateConnectionQueueRequest
from domain.connection.services.ConnectionFileService import ConnectionFileService
from domain.connection.services.ConnectionDatabaseService import ConnectionDatabaseService
from domain.connection.services.ConnectionQueueService import ConnectionQueueService
from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from domain.connection.services.ConnectionServerService import ConnectionServerService
from domain.connection.services.ConnectionTypeService import ConnectionTypeService
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from infrastructure.exceptions.OperationalException import OperationalException
from infrastructure.logging.SqlLogger import SqlLogger
from models.dao.connection.Connection import Connection
from models.enums.ConnectionTypes import ConnectionTypes


class ConnectionService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 sql_logger: SqlLogger,
                 connection_type_service: ConnectionTypeService,
                 connection_database_service: ConnectionDatabaseService,
                 connection_file_service: ConnectionFileService,
                 connection_queue_service: ConnectionQueueService,
                 connection_secret_service: ConnectionSecretService,
                 connection_server_service: ConnectionServerService
                 ):
        self.repository_provider = repository_provider
        self.connection_queue_service = connection_queue_service
        self.connection_server_service = connection_server_service
        self.connection_secret_service = connection_secret_service
        self.connection_type_service = connection_type_service
        self.sql_logger: SqlLogger = sql_logger
        self.connection_file_service = connection_file_service
        self.connection_database_service = connection_database_service
        self.connection_repository = repository_provider.get(Connection)

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

    def create_connection_database(self, request: CreateConnectionDatabaseRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.connection_repository.first(IsDeleted=0, Name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_name=ConnectionTypes.Database.name)
            self.connection_secret_service.create(connection=connection, user=request.User,
                                                  password=request.Password)
            self.connection_server_service.create(connection=connection, host=request.Host, port=request.Port)
            self.connection_database_service.create(connection=connection,
                                                    connector_type_name=request.ConnectorTypeName, sid=request.Sid,
                                                    service_name=request.ServiceName,
                                                    database_name=request.DatabaseName)
        else:
            self.connection_secret_service.update(connection=connection, user=request.User,
                                                  password=request.Password)
            self.connection_server_service.update(connection=connection, host=request.Host, port=request.Port)
            self.connection_database_service.update(connection=connection,
                                                    connector_type_name=request.ConnectorTypeName, sid=request.Sid,
                                                    service_name=request.ServiceName,
                                                    database_name=request.DatabaseName)
        self.connection_repository.insert(connection)
        self.repository_provider.commit()
        connection = self.connection_repository.first(Id=connection.Id)
        return connection

    def create_connection_file(self, request: CreateConnectionFileRequest) -> Connection:
        """
        Create File connection
        """
        connection = self.get_by_name(name=request.Name)
        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_name=ConnectionTypes.File.name)
            self.connection_secret_service.create(connection=connection, user=request.User,
                                                  password=request.Password)
            self.connection_server_service.create(connection=connection, host=request.Host, port=request.Port)
            self.connection_file_service.create(connection=connection, connector_type_name=request.ConnectorTypeName)
        else:
            self.connection_secret_service.update(connection=connection, user=request.User,
                                                  password=request.Password)
            self.connection_server_service.update(connection=connection, host=request.Host, port=request.Port)
            self.connection_file_service.update(connection=connection, connector_type_name=request.ConnectorTypeName)

        self.connection_repository.insert(connection)
        self.repository_provider.commit()
        connection = self.connection_repository.first(Id=connection.Id)
        return connection

    def create_connection_queue(self, request: CreateConnectionQueueRequest) -> Connection:
        """
        Create File connection
        """

        connection = self.connection_repository.first(IsDeleted=0, Name=request.Name)

        if connection is None:
            connection = self.create_connection(name=request.Name,
                                                connection_type_name=ConnectionTypes.Queue.name)
            self.connection_secret_service.create(connection=connection, user=request.User,
                                                  password=request.Password)
            for server in request.Servers:
                self.connection_server_service.create(connection=connection, host=server.Host, port=server.Port)
            self.connection_queue_service.create(connection=connection, connector_type_name=request.ConnectorTypeName,
                                                 protocol=request.Protocol, mechanism=request.Mechanism)
        else:
            self.connection_secret_service.update(connection=connection, user=request.User,
                                                  password=request.Password)

            for server in request.Servers:
                connection_server = self.connection_server_service.get_by_server_info(connection_id=connection.Id,
                                                                                      host=server.Host,
                                                                                      port=server.Port)
                if connection_server is not None:
                    self.connection_server_service.update(connection=connection, host=server.Host, port=server.Port)
                else:
                    self.connection_server_service.create(connection=connection, host=server.Host, port=server.Port)

            connection_servers = self.connection_server_service.get_all_by_connection_id(connection_id=connection.Id)
            for connection_server in connection_servers:
                check = [server for server in request.Servers if
                         server.Host == connection_server.Host and server.Port == connection_server.Port]
                if check is None or len(check) == 0:
                    self.connection_server_service.delete(id=connection_server.Id)

            self.connection_queue_service.update(connection=connection, connector_type_name=request.ConnectorTypeName,
                                                 protocol=request.Protocol, mechanism=request.Mechanism)
        self.connection_repository.insert(connection)
        self.repository_provider.commit()
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

        if connection.ConnectionServers is not None:
            for connection_server in connection.ConnectionServers:
                self.connection_server_service.delete(id=connection_server.Id)
        if connection.ConnectionSecrets is not None:
            for connection_secret in connection.ConnectionSecrets:
                self.connection_secret_service.delete(id=connection_secret.Id)
        message = f'{connection.Name} connection deleted'
        self.sql_logger.info(message)
        self.repository_provider.commit()
        return message
