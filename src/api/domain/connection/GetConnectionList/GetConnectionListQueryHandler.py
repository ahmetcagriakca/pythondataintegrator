from injector import inject
from domain.connection.GetConnectionList.GetConnectionListMapping import GetConnectionListMapping
from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from domain.connection.GetConnectionList.GetConnectionListSpecifications import GetConnectionListSpecifications
from infrastructor.cqrs.IQueryHandler import IQueryHandler
from infrastructor.data.RepositoryProvider import RepositoryProvider
from models.dao.connection import Connection


class GetConnectionListQueryHandler(IQueryHandler[GetConnectionListQuery]):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 get_connection_list_specifications: GetConnectionListSpecifications):
        self.get_connection_list_specifications = get_connection_list_specifications
        self.repository_provider = repository_provider

    def handle(self, query: GetConnectionListQuery) -> GetConnectionListResponse:
        result = GetConnectionListResponse()
        connection_repository = self.repository_provider.get(Connection)
        data_query = connection_repository.table \
            .filter(Connection.IsDeleted == 0)

        result.Count = self.get_connection_list_specifications.count(query=query, data_query=data_query)

        data_query = self.get_connection_list_specifications.specify(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        result.PageData = GetConnectionListMapping.to_dtos(data_query)
        return result
