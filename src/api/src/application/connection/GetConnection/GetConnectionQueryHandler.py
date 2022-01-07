from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.connection.GetConnection.GetConnectionMapping import GetConnectionMapping
from src.application.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from src.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse
from src.application.connection.GetConnection.GetConnectionSpecifications import GetConnectionSpecifications
from src.domain.connection.Connection import Connection


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
