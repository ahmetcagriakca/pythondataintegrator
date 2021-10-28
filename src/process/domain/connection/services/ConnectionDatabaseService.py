from injector import inject
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from pdip.exceptions import OperationalException

from domain.connection.services.ConnectorTypeService import ConnectorTypeService
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.viewmodels.connection.CreateConnectionDatabaseModel import CreateConnectionDatabaseModel


class ConnectionDatabaseService(IScoped):

    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 connector_type_service: ConnectorTypeService
                 ):
        self.repository_provider = repository_provider
        self.connector_type_service = connector_type_service
        self.connection_database_repository = repository_provider.get(ConnectionDatabase)

    def create(self, connection: Connection, model: CreateConnectionDatabaseModel) -> ConnectionDatabase:
        """
        Create Database connection
        """
        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        if connector_type is None:
            raise OperationalException(f"{model.ConnectorTypeName} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{model.ConnectorTypeName} incompatible with {connection.ConnectionType.Name}")
        connection_database = ConnectionDatabase(Connection=connection,
                                                 ConnectorType=connector_type,
                                                 Sid=model.Sid,
                                                 ServiceName=model.ServiceName,
                                                 DatabaseName=model.DatabaseName)

        self.connection_database_repository.insert(connection_database)
        return connection_database

    def update(self, connection: Connection, model: CreateConnectionDatabaseModel) -> ConnectionDatabase:
        """
        Update Database connection
        """

        connection_database = self.connection_database_repository.first(ConnectionId=connection.Id)

        connector_type = self.connector_type_service.get_by_name(name=model.ConnectorTypeName)
        if connector_type is None:
            raise OperationalException(f"{model.ConnectorTypeName} not found")
        if connector_type.ConnectionTypeId != connection.ConnectionTypeId:
            raise OperationalException(f"{model.ConnectorTypeName} incompatible with {connection.ConnectionType.Name}")
        connection_database.ConnectorType = connector_type
        connection_database.Sid = model.Sid
        connection_database.ServiceName = model.ServiceName
        connection_database.DatabaseName = model.DatabaseName
        return connection_database

    def delete(self, id: int):
        """
        Delete Database connection
        """

        self.connection_database_repository.delete_by_id(id)
