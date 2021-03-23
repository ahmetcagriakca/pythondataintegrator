from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.operation.execution.adapters.execution.ExecuteIntegrationUnpredictedSourceAdapter import \
    ExecuteIntegrationUnpredictedSourceAdapter
from domain.operation.execution.adapters.execution.ExecuteAdapter import ExecuteAdapter
from domain.operation.execution.adapters.execution.ExecuteIntegrationAdapter import ExecuteIntegrationAdapter
from domain.operation.execution.adapters.execution.ExecuteQueryAdapter import ExecuteQueryAdapter
from infrastructor.dependency.scopes import IScoped
from infrastructor.exceptions.IncompatibleAdapterException import IncompatibleAdapterException
from models.enums import ConnectionTypes


class ExecuteAdapterFactory(IScoped):
    @inject
    def __init__(self,
                 data_integration_connection_service: DataIntegrationConnectionService,
                 execute_query_adapter: ExecuteQueryAdapter,
                 execute_operation_adapter: ExecuteIntegrationAdapter,
                 execute_operation_unpredicted_source_adapter: ExecuteIntegrationUnpredictedSourceAdapter,
                 ):
        self.execute_operation_unpredicted_source_adapter = execute_operation_unpredicted_source_adapter
        self.data_integration_connection_service = data_integration_connection_service
        self.execute_operation_adapter = execute_operation_adapter
        self.execute_query_adapter = execute_query_adapter

    def get_execute_adapter(self, data_integration_id) -> ExecuteAdapter:
        # Source and target database managers instantiate
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        # only target query run
        if source_connection is None or (
                source_connection.Database is not None
                and
                (
                        source_connection.Database.Query is None
                        or
                        source_connection.Database.Query == ''
                )
        ):
            if isinstance(self.execute_query_adapter, ExecuteAdapter):
                return self.execute_query_adapter
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_query_adapter} is incompatible with {ExecuteAdapter}")
        elif (source_connection.Connection.ConnectionTypeId == ConnectionTypes.Queue.value) or (
                source_connection.Connection.ConnectionTypeId == ConnectionTypes.File.value):
            if isinstance(self.execute_operation_unpredicted_source_adapter, ExecuteAdapter):
                return self.execute_operation_unpredicted_source_adapter
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_operation_unpredicted_source_adapter} is incompatible with {ExecuteAdapter}")
        else:
            if isinstance(self.execute_operation_adapter, ExecuteAdapter):
                return self.execute_operation_adapter
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_operation_adapter} is incompatible with {ExecuteAdapter}")
