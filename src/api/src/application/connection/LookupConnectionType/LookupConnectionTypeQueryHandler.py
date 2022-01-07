from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.connection.LookupConnectionType.LookupConnectionTypeMapping import LookupConnectionTypeMapping
from src.application.connection.LookupConnectionType.LookupConnectionTypeQuery import LookupConnectionTypeQuery
from src.application.connection.LookupConnectionType.LookupConnectionTypeResponse import LookupConnectionTypeResponse
from src.application.connection.LookupConnectionType.LookupConnectionTypeSpecifications import \
    LookupConnectionTypeSpecifications
from src.domain.connection.ConnectionType import ConnectionType


class LookupConnectionTypeQueryHandler(IQueryHandler[LookupConnectionTypeQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: LookupConnectionTypeSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: LookupConnectionTypeQuery) -> LookupConnectionTypeResponse:
        result = LookupConnectionTypeResponse()
        repository = self.repository_provider.get(ConnectionType)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupConnectionTypeMapping.to_dtos(data_query)
        return result
