from injector import inject
from pdip.dependency import IScoped
from pdip.exceptions import IncompatibleAdapterException

from process.application.execution.adapters.execution.ExecuteAdapter import ExecuteAdapter
from process.application.execution.adapters.execution.ExecuteIntegrationAdapter import \
    ExecuteIntegrationAdapter
from process.application.execution.adapters.execution.ExecuteQueryAdapter import ExecuteQueryAdapter
from process.application.execution.services.OperationCacheService import OperationCacheService


class ExecuteAdapterFactory(IScoped):
    @inject
    def __init__(self,
                 operation_cache_service: OperationCacheService,
                 execute_query_adapter: ExecuteQueryAdapter,
                 execute_integration_adapter: ExecuteIntegrationAdapter,
                 ):
        self.operation_cache_service = operation_cache_service
        self.execute_integration_adapter = execute_integration_adapter
        self.execute_query_adapter = execute_query_adapter

    def get_execute_adapter(self, data_integration_id) -> ExecuteAdapter:
        # Source and target database managers instantiate
        source_connection = self.operation_cache_service.get_source_connection(
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
        else:
            if isinstance(self.execute_integration_adapter, ExecuteAdapter):
                return self.execute_integration_adapter
            else:
                raise IncompatibleAdapterException(
                    f"{self.execute_integration_adapter} is incompatible with {ExecuteAdapter}")