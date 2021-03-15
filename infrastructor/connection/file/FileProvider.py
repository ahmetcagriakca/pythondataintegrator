import os
from sys import path

from injector import inject

from domain.connection.services.ConnectionSecretService import ConnectionSecretService
from infrastructor.connection.file.FileContext import FileContext
from infrastructor.connection.file.connectors.CsvConnector import CsvConnector
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
                 api_config: ApiConfig
                 ):
        self.api_config = api_config
        self.connection_secret_service = connection_secret_service
        self.sql_logger = sql_logger

    def get_file_context(self, connection: Connection) -> FileContext:
        """
        Creating Connection
        """
        if connection.ConnectionType.Name == ConnectionTypes.File.name:
            folder = connection.File.Folder
            if folder is None or folder == '':
                folder = os.path.join(self.api_config.root_directory, "files")
            if connection.File.ConnectorType.Name == ConnectorTypes.CSV.name:
                connector = CsvConnector(folder=folder)
            file_context: FileContext = FileContext(connector=connector)
            return file_context

    def get_file_context_with_folder(self, folder: str) -> FileContext:
        """
        Creating Connection
        """

        if folder is None or folder == '':
            folder = self.api_config.root_directory
        connector = CsvConnector(folder=folder)
        file_context: FileContext = FileContext(connector=connector)
        return file_context
