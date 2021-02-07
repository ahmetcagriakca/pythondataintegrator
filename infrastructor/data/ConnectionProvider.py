from injector import inject
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionManager import ConnectionManager
from infrastructor.data.ConnectionPolicy import ConnectionPolicy
from infrastructor.dependency.scopes import ISingleton
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.connection.Connection import Connection


class ConnectionProvider(ISingleton):
    @inject
    def __init__(self,
                 crypto_service: CryptoService,
                 sql_logger: SqlLogger,
                 database_config: DatabaseConfig,
                 ):
        self.database_config = database_config
        self.sql_logger = sql_logger
        self.crypto_service: CryptoService = crypto_service

    def get_connection_manager(self, connection: Connection) -> ConnectionManager:
        """
        Creating connec
        """
        if connection.ConnectionType.Name == 'Database':
            if connection.Database.ConnectorType.Name == 'ORACLE':
                user = self.crypto_service.decrypt_code(connection.Database.User.encode()).decode('utf-8')
                password = self.crypto_service.decrypt_code(connection.Database.Password.encode()).decode(
                    'utf-8')
                host = connection.Database.Host
                port = connection.Database.Port
                service_name = connection.Database.ServiceName
                sid = connection.Database.Sid
                config = DatabaseConfig(type=connection.Database.ConnectorType.Name, host=host, port=port,
                                        sid=sid, service_name=service_name, username=user, password=password)
            elif connection.Database.ConnectorType.Name == 'MSSQL':
                driver = self.database_config.driver
                user = self.crypto_service.decrypt_code(connection.Database.User.encode()).decode('utf-8')
                password = self.crypto_service.decrypt_code(connection.Database.Password.encode()).decode(
                    'utf-8')
                host = connection.Database.Host
                port = connection.Database.Port
                database_name = connection.Database.DatabaseName
                config = DatabaseConfig(type=connection.Database.ConnectorType.Name, host=host, port=port,
                                        database=database_name, username=user, password=password, driver=driver)
            elif connection.Database.ConnectorType.Name == 'POSTGRESQL':
                user = self.crypto_service.decrypt_code(connection.Database.User.encode()).decode('utf-8')
                password = self.crypto_service.decrypt_code(connection.Database.Password.encode()).decode(
                    'utf-8')
                host = connection.Database.Host
                port = connection.Database.Port
                database_name = connection.Database.DatabaseName
                config = DatabaseConfig(type=connection.Database.ConnectorType.Name, host=host, port=port,
                                        database=database_name, username=user, password=password)

            connection_policy = ConnectionPolicy(config)
            connection_manager: ConnectionManager = ConnectionManager(connection_policy, self.sql_logger)
            return connection_manager
