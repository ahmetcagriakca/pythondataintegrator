from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from pdi.application.connection.services.ConnectorTypeService import ConnectorTypeService
from pdi.domain.connection.Connection import Connection
from pdi.domain.connection.ConnectionBigData import ConnectionBigData


class ConnectionBigDataService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 connector_type_service: ConnectorTypeService
                 ):
        self.repository_provider = repository_provider
        self.connector_type_service = connector_type_service
        self.connection_big_data_repository = repository_provider.get(ConnectionBigData)

    def create(self, connection: Connection, connector_type_id: int, ssl: bool, use_only_sspi: bool,
               database_name: str) -> ConnectionBigData:
        """
        Create BigData connection
        """
        connector_type = self.connector_type_service.get_by_id(id=connector_type_id)
        if connector_type is None:
            raise OperationalException(f"{connector_type_id} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_id} incompatible with {connection.ConnectionType.Name}")
        connection_big_data = ConnectionBigData(Connection=connection,
                                                 ConnectorType=connector_type,
                                                 Ssl=ssl,
                                                 UseOnlySspi=use_only_sspi,
                                                 DatabaseName=database_name)

        self.connection_big_data_repository.insert(connection_big_data)
        return connection_big_data

    def update(self, connection: Connection, connector_type_id: int, ssl: bool, use_only_sspi: bool,
               database_name: str) -> ConnectionBigData:
        """
        Update BigData connection
        """

        connection_big_data = self.connection_big_data_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_id(id=connector_type_id)
        if connector_type is None:
            raise OperationalException(f"{connector_type_id} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{connector_type_id} incompatible with {connection.ConnectionType.Name}")
        connection_big_data.ConnectorType = connector_type
        connection_big_data.Ssl = ssl
        connection_big_data.UseOnlySspi = use_only_sspi
        connection_big_data.DatabaseName = database_name
        return connection_big_data

    def delete(self, id: int):
        """
        Delete BigData connection
        """

        self.connection_big_data_repository.delete_by_id(id)
