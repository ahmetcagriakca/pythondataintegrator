from injector import inject
from domain.connection.LookupConnection.LookupConnectionMapping import LookupConnectionMapping
from domain.connection.LookupConnection.LookupConnectionQuery import LookupConnectionQuery
from domain.connection.LookupConnection.LookupConnectionResponse import LookupConnectionResponse
from domain.connection.LookupConnection.LookupConnectionSpecifications import LookupConnectionSpecifications
from pdip.cqrs import IQueryHandler 
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from models.dao.connection.Connection import Connection


class LookupConnectionQueryHandler(IQueryHandler[LookupConnectionQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: LookupConnectionSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: LookupConnectionQuery) -> LookupConnectionResponse:
        result = LookupConnectionResponse()
        repository = self.repository_provider.get(Connection)
        data_query = repository.table.filter(Connection.IsDeleted==0)
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupConnectionMapping.to_dtos(data_query)
        return result
