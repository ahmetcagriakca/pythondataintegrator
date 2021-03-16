from typing import List
from injector import inject
from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from infrastructor.cryptography.CryptoService import CryptoService
from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.data.Repository import Repository
from infrastructor.dependency.scopes import IScoped
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionFile import ConnectionFile
from models.viewmodels.connection.CreateConnectionFileModel import CreateConnectionFileModel


class ConnectionFileService(IScoped):

    @inject
    def __init__(self,
                 database_session_manager: DatabaseSessionManager,
                 connector_type_service: ConnectorTypeService
                 ):
        self.connector_type_service = connector_type_service
        self.database_session_manager = database_session_manager
        self.connection_file_repository: Repository[ConnectionFile] = Repository[ConnectionFile](
            database_session_manager)

    def get_connection_files(self, ) -> List[ConnectionFile]:
        """
        Data data_integration data preparing
        """
        entities = self.connection_file_repository.filter_by(IsDeleted=0).all()
        return entities

    def create(self, connection: Connection, model: CreateConnectionFileModel) -> ConnectionFile:
        """
        Create File connection
        """

        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)

        connection_file = ConnectionFile(Connection=connection,
                                         Host=model.Host,
                                         Port=model.Port,
                                         ConnectorType=connector_type)

        self.connection_file_repository.insert(connection_file)
        return ConnectionFile

    def update(self, connection: Connection, model: CreateConnectionFileModel) -> ConnectionFile:
        """
        Update File connection
        """

        connection_file = self.connection_file_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)

        connection_file.ConnectorType = connector_type
        connection_file.Host = model.Host
        connection_file.Port = model.Port

        return connection_file

    def delete(self, id: int):
        """
        Delete Database connection
        """

        self.connection_file_repository.delete_by_id(id)
