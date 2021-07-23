from injector import inject
from domain.connection.GetConnection.GetConnectionMapping import GetConnectionMapping
from domain.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from domain.connection.GetConnection.GetConnectionResponse import GetConnectionResponse
from domain.connection.GetConnection.GetConnectionSpecifications import GetConnectionSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.connection.Connection import Connection


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
        result.Data = GetConnectionMapping.to_dto(data_query)
        return result
