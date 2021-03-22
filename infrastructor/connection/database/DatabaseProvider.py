from injector import inject

from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from domain.connection.services.ConnectionServerService import ConnectionServerService
from infrastructor.connection.database.DatabaseContext import DatabaseContext
from infrastructor.connection.database.DatabasePolicy import DatabasePolicy
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.connection.Connection import Connection
from models.enums import ConnectionTypes, ConnectorTypes


class DatabaseProvider(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 connection_secret_service: ConnectionSecretService,
                 connection_server_service: ConnectionServerService
                 ):
        self.connection_server_service = connection_server_service
        self.connection_secret_service = connection_secret_service
        self.sql_logger = sql_logger

    def get_context(self, connection: Connection) -> DatabaseContext:
        """
        Creating Connection
        """
        if connection.ConnectionType.Name == ConnectionTypes.Database.name:
            connection_basic_authentication = self.connection_secret_service.get_connection_basic_authentication(
                connection_id=connection.Id)
            connection_server = self.connection_server_service.get_by_connection_id(
                connection_id=connection.Id)
            if connection.Database.ConnectorType.Name == ConnectorTypes.ORACLE.name:
                user = connection_basic_authentication.User
                password = connection_basic_authentication.Password
                host = connection_server.Host
                port = connection_server.Port
                service_name = connection.Database.ServiceName
                sid = connection.Database.Sid
                config = DatabaseConfig(type=connection.Database.ConnectorType.Name, host=host, port=port,
                                        sid=sid, service_name=service_name, username=user, password=password)
            elif connection.Database.ConnectorType.Name == ConnectorTypes.MSSQL.name:
                user = connection_basic_authentication.User
                password = connection_basic_authentication.Password
                host = connection_server.Host
                port = connection_server.Port
                database_name = connection.Database.DatabaseName
                config = DatabaseConfig(type=connection.Database.ConnectorType.Name, host=host, port=port,
                                        database=database_name, username=user, password=password)
            elif connection.Database.ConnectorType.Name == ConnectorTypes.POSTGRESQL.name:
                user = connection_basic_authentication.User
                password = connection_basic_authentication.Password
                host = connection_server.Host
                port = connection_server.Port
                database_name = connection.Database.DatabaseName
                config = DatabaseConfig(type=connection.Database.ConnectorType.Name, host=host, port=port,
                                        database=database_name, username=user, password=password)

            database_policy = DatabasePolicy(database_config=config)
            database_context: DatabaseContext = DatabaseContext(database_policy=database_policy,
                                                                sql_logger=self.sql_logger)
            return database_context
