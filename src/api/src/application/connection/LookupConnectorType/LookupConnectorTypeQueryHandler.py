from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.connection.LookupConnectorType.LookupConnectorTypeMapping import LookupConnectorTypeMapping
from src.application.connection.LookupConnectorType.LookupConnectorTypeQuery import LookupConnectorTypeQuery
from src.application.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse
from src.application.connection.LookupConnectorType.LookupConnectorTypeSpecifications import \
    LookupConnectorTypeSpecifications
from src.domain.connection.ConnectorType import ConnectorType


class LookupConnectorTypeQueryHandler(IQueryHandler[LookupConnectorTypeQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: LookupConnectorTypeSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: LookupConnectorTypeQuery) -> LookupConnectorTypeResponse:
        result = LookupConnectorTypeResponse()
        repository = self.repository_provider.get(ConnectorType)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupConnectorTypeMapping.to_dtos(data_query)
        return result
