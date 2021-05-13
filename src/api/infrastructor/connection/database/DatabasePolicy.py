from injector import inject
from infrastructor.connection.database.connectors.DatabaseConnector import DatabaseConnector
from infrastructor.connection.database.connectors.MssqlDbConnector import MssqlDbConnector
from infrastructor.connection.database.connectors.OracleDbConnector import OracleDbConnector
from infrastructor.connection.database.connectors.PostgreDbConnector import PostgreDbConnector
from models.configs.DatabaseConfig import DatabaseConfig


class DatabasePolicy:
    @inject
    def __init__(self, database_config: DatabaseConfig):
        self.database_config = database_config
        self.connector: DatabaseConnector = None
        if database_config.type == "MSSQL":
            self.connector: DatabaseConnector = MssqlDbConnector(database_config)
        elif database_config.type == "ORACLE":
            self.connector: DatabaseConnector = OracleDbConnector(database_config)
        elif database_config.type == "POSTGRESQL":
            self.connector: DatabaseConnector = PostgreDbConnector(database_config)
