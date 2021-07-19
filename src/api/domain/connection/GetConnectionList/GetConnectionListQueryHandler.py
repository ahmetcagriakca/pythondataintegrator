from injector import inject
from domain.connection.GetConnectionList.GetConnectionListMapping import GetConnectionListMapping
from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from domain.connection.GetConnectionList.GetConnectionListSpecifications import GetConnectionListSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.connection import Connection


class GetConnectionListQueryHandler(IQueryHandler[GetConnectionListQuery],IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: GetConnectionListSpecifications):
        self.specifications = specifications
        self.repository_provider = repository_provider

    def handle(self, query: GetConnectionListQuery) -> GetConnectionListResponse:
        result = GetConnectionListResponse()
        connection_repository = self.repository_provider.get(Connection)
        data_query = connection_repository.table \
            .filter(Connection.IsDeleted == 0)

        result.Count = self.specifications.count(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        data_query = self.specifications.specify(query=query, data_query=data_query)

        result.Data = GetConnectionListMapping.to_dtos(data_query)
        return result
