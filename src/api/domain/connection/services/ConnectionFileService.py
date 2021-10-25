from typing import List
from injector import inject
from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionFile import ConnectionFile


class ConnectionFileService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 connector_type_service: ConnectorTypeService
                 ):
        self.repository_provider = repository_provider
        self.connector_type_service = connector_type_service
        self.connection_file_repository = repository_provider.get(ConnectionFile)

    def get_connection_files(self, ) -> List[ConnectionFile]:
        """
        Data data_integration data preparing
        """
        entities = self.connection_file_repository.filter_by(IsDeleted=0).all()
        return entities

    def create(self, connection: Connection, connector_type_name: str) -> ConnectionFile:
        """
        Create File connection
        """

        connector_type = self.connector_type_service.get_by_name(name=connector_type_name)

        if connector_type is None:
            raise OperationalException(f"{connector_type_name} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_name} incompatible with {connection.ConnectionType.Name}")
        connection_file = ConnectionFile(Connection=connection,
                                         ConnectorType=connector_type)

        self.connection_file_repository.insert(connection_file)
        return ConnectionFile

    def update(self, connection: Connection, connector_type_name: str) -> ConnectionFile:
        """
        Update File connection
        """

        connection_file = self.connection_file_repository.first(ConnectionId=connection.Id)
        connector_type = self.connector_type_service.get_by_name(name=connector_type_name)
        if connector_type is None:
            raise OperationalException(f"{connector_type_name} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_name} incompatible with {connection.ConnectionType.Name}")
        connection_file.ConnectorType = connector_type

        return connection_file

    def delete(self, id: int):
        """
        Delete Database connection
        """
        self.connection_file_repository.delete_by_id(id)
