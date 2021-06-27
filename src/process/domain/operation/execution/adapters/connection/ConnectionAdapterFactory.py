from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.operation.execution.adapters.connection.FileAdapter import FileAdapter
from domain.operation.execution.adapters.connection.QueueAdapter import QueueAdapter
from infrastructor.connection.adapters.ConnectionAdapter import ConnectionAdapter
from domain.operation.execution.adapters.connection.DatabaseAdapter import DatabaseAdapter
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.IncompatibleAdapterException import IncompatibleAdapterException
from infrastructor.exceptions.NotSupportedFeatureException import NotSupportedFeatureException
from models.enums import ConnectionTypes


class ConnectionAdapterFactory(IScoped):
    @inject
    def __init__(self,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 database_adapter: DatabaseAdapter,
                 file_adapter: FileAdapter,
                 queue_adapter: QueueAdapter,
                 ):
        self.queue_adapter = queue_adapter
        self.file_adapter = file_adapter
        self.data_integration_connection_service = data_integration_connection_service
        self.database_adapter = database_adapter

    def get_source_adapter(self, data_integration_id) -> ConnectionAdapter:

        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        if source_connection.Connection.ConnectionType.Id == ConnectionTypes.Database.value:
            if isinstance(self.database_adapter, ConnectionAdapter):
                return self.database_adapter
            else:
                raise IncompatibleAdapterException(f"{self.database_adapter} is incompatible with ConectionAdapter")
        elif source_connection.Connection.ConnectionType.Id == ConnectionTypes.File.value:
            if isinstance(self.file_adapter, ConnectionAdapter):
                return self.file_adapter
            else:
                raise IncompatibleAdapterException(f"{self.file_adapter} is incompatible with ConectionAdapter")
        elif source_connection.Connection.ConnectionType.Id == ConnectionTypes.Queue.value:
            if isinstance(self.queue_adapter, ConnectionAdapter):
                return self.queue_adapter
            else:
                raise IncompatibleAdapterException(f"{self.queue_adapter} is incompatible with ConectionAdapter")
        else:
            raise NotSupportedFeatureException(f"{source_connection.Connection.ConnectionType}")

    def get_target_adapter(self, data_integration_id) -> ConnectionAdapter:
        target_connection = self.data_integration_connection_service.get_target_connection(
            data_integration_id=data_integration_id)
        if target_connection.Connection.ConnectionType.Id == ConnectionTypes.Database.value:
            if isinstance(self.database_adapter, ConnectionAdapter):
                return self.database_adapter
            else:
                raise IncompatibleAdapterException(f"{self.database_adapter} is incompatible with ConectionAdapter")
        elif target_connection.Connection.ConnectionType.Id == ConnectionTypes.File.value:
            if isinstance(self.file_adapter, ConnectionAdapter):
                return self.file_adapter
            else:
                raise IncompatibleAdapterException(f"{self.file_adapter} is incompatible with ConectionAdapter")
        elif target_connection.Connection.ConnectionType.Id == ConnectionTypes.Queue.value:
            if isinstance(self.queue_adapter, ConnectionAdapter):
                return self.queue_adapter
            else:
                raise IncompatibleAdapterException(f"{self.queue_adapter} is incompatible with ConectionAdapter")
        else:
            raise NotSupportedFeatureException(f"{target_connection.Connection.ConnectionType}")
