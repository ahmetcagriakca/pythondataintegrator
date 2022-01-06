from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.connection.GetConnection.GetConnectionMapping import GetConnectionMapping
from pdi.application.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from pdi.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse
from pdi.application.connection.GetConnection.GetConnectionSpecifications import GetConnectionSpecifications
from pdi.domain.connection.Connection import Connection


class GetConnectionQueryHandler(IQueryHandler[GetConnectionQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: GetConnectionSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: GetConnectionQuery) -> GetConnectionResponse:
        result = GetConnectionResponse()
        repository = self.repository_provider.get(Connection)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = GetConnectionMapping.to_dto(data_query.first())
        return result
