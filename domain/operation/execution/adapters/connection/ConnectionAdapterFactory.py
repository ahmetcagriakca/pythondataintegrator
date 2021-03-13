from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from domain.operation.execution.adapters.connection.DatabaseAdapter import DatabaseAdapter
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.IncompatibleAdapterException import IncompatibleAdapterException
from models.enums import ConnectionTypes


class ConnectionAdapterFactory(IScoped):
    @inject
    def __init__(self,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 database_adapter: DatabaseAdapter):
        self.data_integration_connection_service = data_integration_connection_service
        self.database_adapter = database_adapter

    def get_source_connection_adapter(self, data_integration_id) -> ConnectionAdapter:

        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        if source_connection.Connection.ConnectionType.Id == ConnectionTypes.Database.value:
            if isinstance(self.database_adapter, ConnectionAdapter):
                return self.database_adapter
            else:
                raise IncompatibleAdapterException(f"{self.database_adapter} is incompatible with ConectionAdapter")

    def get_target_connection_adapter(self, data_integration_id) -> ConnectionAdapter:

        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        if target_connection.Connection.ConnectionType.Id == ConnectionTypes.Database.value:
            if isinstance(self.database_adapter, ConnectionAdapter):
                return self.database_adapter
            else:
                raise IncompatibleAdapterException(f"{self.database_adapter} is incompatible with ConectionAdapter")
