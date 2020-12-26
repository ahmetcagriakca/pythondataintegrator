from injector import inject
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.ConnectionManager import ConnectionManager
from infrastructor.data.ConnectionPolicy import ConnectionPolicy
from infrastructor.dependency.scopes import ISingleton
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.DatabaseConfig import DatabaseConfig
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection


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

    def get_connection(self, connection: DataIntegrationConnection) -> ConnectionManager:
        """
         Database getting from integration_data
        """
        if connection.Connection.ConnectionType.Name == 'Database':
            if connection.Connection.Database.ConnectorType.Name == 'ORACLE':
                user = self.crypto_service.decrypt_code(connection.Connection.Database.User.encode()).decode('utf-8')
                password = self.crypto_service.decrypt_code(connection.Connection.Database.Password.encode()).decode('utf-8')
                host = connection.Connection.Database.Host
                port = connection.Connection.Database.Port
                database_name = connection.Connection.Database.DatabaseName
                sid = connection.Connection.Database.Sid
                if sid is not None and sid != '':
                    config = DatabaseConfig(type=connection.Connection.Database.ConnectorType.Name, host=host,
                                            port=port, database=sid, username=user, password=password)
                else:
                    connection_string = f"{user}/{password}@{host}:{port}/{database_name}"
                    config = DatabaseConfig(type=connection.Connection.Database.ConnectorType.Name,
                                            connection_string=connection_string)
            elif connection.Connection.Database.ConnectorType.Name == 'MSSQL':
                driver = self.database_config.driver
                user = self.crypto_service.decrypt_code(connection.Connection.Database.User.encode()).decode('utf-8')
                password = self.crypto_service.decrypt_code(connection.Connection.Database.Password.encode()).decode('utf-8')
                host = connection.Connection.Database.Host
                database_name = connection.Connection.Database.DatabaseName
                config = DatabaseConfig(type=connection.Connection.Database.ConnectorType.Name, host=host,
                                        database=database_name, username=user, password=password, driver=driver)
            elif connection.Connection.Database.ConnectorType.Name == 'POSTGRESQL':
                user = self.crypto_service.decrypt_code(connection.Connection.Database.User.encode()).decode('utf-8')
                password = self.crypto_service.decrypt_code(connection.Connection.Database.Password.encode()).decode('utf-8')
                host = connection.Connection.Database.Host
                port = connection.Connection.Database.Port
                database_name = connection.Connection.Database.DatabaseName
                config = DatabaseConfig(type=connection.Connection.Database.ConnectorType.Name, host=host, port=port,
                                        database=database_name, username=user, password=password)

            database_policy = ConnectionPolicy(config)
            database_manager: ConnectionManager = ConnectionManager(database_policy, self.sql_logger)
            return database_manager
