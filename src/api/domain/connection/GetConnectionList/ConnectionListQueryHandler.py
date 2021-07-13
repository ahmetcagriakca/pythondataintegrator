from injector import inject
from domain.connection.GetConnectionList.ConnectionListMapping import ConnectionListMapping
from domain.connection.GetConnectionList.ConnectionListQuery import ConnectionListQuery
from domain.connection.GetConnectionList.ConnectionListResponse import ConnectionListResponse
from domain.connection.GetConnectionList.ConnectionListSpecifications import ConnectionListSpecifications
from infrastructor.data.RepositoryProvider import RepositoryProvider
from models.dao.connection import Connection


class ConnectionListQueryHandler:
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 connection_list_specification: ConnectionListSpecifications):
        self.connection_list_specification = connection_list_specification
        self.repository_provider = repository_provider

    def handle(self, query: ConnectionListQuery) -> ConnectionListResponse:
        result = ConnectionListResponse()
        connection_repository = self.repository_provider.get(Connection)
        data_query = connection_repository.table \
            .filter(Connection.IsDeleted == 0)

        result.Count = self.connection_list_specification.count(query=query, data_query=data_query)

        data_query = self.connection_list_specification.specify(query=query, data_query=data_query)

        result.PageNumber = query.ConnectionListRequest.PageNumber
        result.PageSize = query.ConnectionListRequest.PageSize

        result.PageData = ConnectionListMapping.to_dtos(data_query)
        return result
