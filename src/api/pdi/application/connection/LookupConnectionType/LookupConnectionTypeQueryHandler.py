from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.connection.LookupConnectionType.LookupConnectionTypeMapping import LookupConnectionTypeMapping
from pdi.application.connection.LookupConnectionType.LookupConnectionTypeQuery import LookupConnectionTypeQuery
from pdi.application.connection.LookupConnectionType.LookupConnectionTypeResponse import LookupConnectionTypeResponse
from pdi.application.connection.LookupConnectionType.LookupConnectionTypeSpecifications import \
    LookupConnectionTypeSpecifications
from pdi.domain.connection.ConnectionType import ConnectionType


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
