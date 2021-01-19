from injector import inject
from infrastructor.data.connectors.ConnectorStrategy import ConnectorStrategy
from infrastructor.data.connectors.MssqlDbConnector import MssqlDbConnector
from infrastructor.data.connectors.OracleDbConnector import OracleDbConnector
from infrastructor.data.connectors.PostgreDbConnector import PostgreDbConnector
from infrastructor.dependency.scopes import IScoped
from models.configs.DatabaseConfig import DatabaseConfig


class ConnectionPolicy(IScoped):
    @inject
    def __init__(self, database_config: DatabaseConfig):
        self.database_config = database_config
        self.connecter: ConnectorStrategy = None
        if database_config.type == "MSSQL":
            self.connector: ConnectorStrategy = MssqlDbConnector(database_config)
        elif database_config.type == "ORACLE":
            self.connector: ConnectorStrategy = OracleDbConnector(database_config)
        elif database_config.type == "POSTGRESQL":
            self.connector: ConnectorStrategy = PostgreDbConnector(database_config)
