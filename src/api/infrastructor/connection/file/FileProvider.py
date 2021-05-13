import os

from injector import inject

from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from domain.connection.services.ConnectionServerService import ConnectionServerService
from infrastructor.connection.file.FileContext import FileContext
from infrastructor.connection.file.connectors.CsvConnector import CsvConnector
from infrastructor.connection.file.connectors.FileConnector import FileConnector
from infrastructor.dependency.scopes import IScoped
from infrastructor.logging.SqlLogger import SqlLogger
from models.configs.ApiConfig import ApiConfig
from models.dao.connection.Connection import Connection
from models.enums import ConnectionTypes, ConnectorTypes


class FileProvider(IScoped):
    @inject
    def __init__(self,
                 sql_logger: SqlLogger,
                 connection_secret_service: ConnectionSecretService,
                 connection_server_service: ConnectionServerService,
                 api_config: ApiConfig
                 ):
        self.connection_server_service = connection_server_service
        self.api_config = api_config
        self.connection_secret_service = connection_secret_service
        self.sql_logger = sql_logger

    def get_context(self, connection: Connection) -> FileContext:
        """
        Creating Connection
        """
        if connection.ConnectionType.Name == ConnectionTypes.File.name:
            connection_basic_authentication = self.connection_secret_service.get_connection_basic_authentication(
                connection_id=connection.Id)
            connection_server = self.connection_server_service.get_by_connection_id(
                connection_id=connection.Id)
            connector: FileConnector = None
            if connection.File.ConnectorType.Name == ConnectorTypes.CSV.name:
                host = connection_server.Host
                port = connection_server.Port
                if host is None or host == '':
                    host = os.path.join(self.api_config.root_directory, "files")
                if connection.File.ConnectorType.Name == ConnectorTypes.CSV.name:
                    connector = CsvConnector(host=host)
            if connector is not None:
                file_context: FileContext = FileContext(connector=connector)
                return file_context
            else:
                raise Exception(f"{connection.File.ConnectorType.Name} connector type not supported")

        else:
            raise Exception(f"{connection.ConnectionType.Name} connection type not supported")

    def get_file_context_with_host(self, host: str) -> FileContext:
        """
        Creating Connection
        """

        if host is None or host == '':
            host = os.path.join(self.api_config.root_directory, "files")
        connector = CsvConnector(folder=host)
        file_context: FileContext = FileContext(connector=connector)
        return file_context
