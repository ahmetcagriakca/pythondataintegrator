from injector import inject

from domain.integration.services.DataIntegrationConnectionService import DataIntegrationConnectionService
from domain.operation.adapters.ExecuteAdapter import ExecuteAdapter
from domain.operation.adapters.ExecuteOperationAdapter import ExecuteOperationAdapter
from domain.operation.adapters.ExecuteQueryAdapter import ExecuteQueryAdapter
from infrastructor.dependency.scopes import IScoped


class ExecuteAdapterFactory(IScoped):
    @inject
    def __init__(self,
                 data_integration_connection_service:DataIntegrationConnectionService,
                 execute_query_adapter: ExecuteQueryAdapter,
                 execute_operation_adapter: ExecuteOperationAdapter):
        self.data_integration_connection_service = data_integration_connection_service
        self.execute_operation_adapter = execute_operation_adapter
        self.execute_query_adapter = execute_query_adapter

    def get_execute_adapter(self, data_integration_id) -> ExecuteAdapter:
        # Source and target database managers instantiate
        source_connection = self.data_integration_connection_service.get_source_connection(
            data_integration_id=data_integration_id)
        # only target query run
        if source_connection is None or source_connection.Query is None or source_connection.Query == '':
            return self.execute_query_adapter
        else:
            return self.execute_operation_adapter

