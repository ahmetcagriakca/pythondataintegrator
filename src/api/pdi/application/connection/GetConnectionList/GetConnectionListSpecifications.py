from injector import inject
from pdip.api.specifications import OrderBySpecification
from pdip.api.specifications import PagingSpecification
from pdip.data.repository import RepositoryProvider
from sqlalchemy.orm import Query

from pdi.application.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from pdi.domain.connection import Connection, ConnectionServer, ConnectionDatabase, ConnectionType, ConnectorType


class GetConnectionListSpecifications:
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.repository_provider = repository_provider
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def __specified_query(self, query: GetConnectionListQuery) -> Query:
        connection_repository = self.repository_provider.get(Connection)
        data_query = connection_repository.table
        specified_query = data_query \
            .join(ConnectionType, ConnectionType.Id == Connection.ConnectionTypeId) \
            .join(ConnectionServer, ConnectionServer.ConnectionId == Connection.Id) \
            .join(ConnectionDatabase, ConnectionDatabase.ConnectionId == Connection.Id) \
            .join(ConnectorType, ConnectorType.Id == ConnectionDatabase.ConnectorTypeId)
        if query.request.Id is not None:
            specified_query = specified_query.filter(Connection.Id == query.request.Id)
        if query.request.ConnectionTypeId is not None:
            specified_query = specified_query.filter(ConnectionType.Id == query.request.ConnectionTypeId)
        if query.request.ConnectorTypeId is not None:
            specified_query = specified_query.filter(ConnectorType.Id == query.request.ConnectorTypeId)
        if query.request.OnlyUndeleted is not None and query.request.OnlyUndeleted:
            specified_query = specified_query.filter(Connection.IsDeleted == 0)
        return specified_query

    def specify(self, query: GetConnectionListQuery) -> Query:
        data_query = self.__specified_query(query=query)
        order_by = self.order_by_specification.specify(order_by_parameter=query.request)
        if order_by is not None:
            data_query = data_query.order_by(order_by)

        page_size, offset = self.paging_specification.specify(paging_parameter=query.request)
        if page_size is not None:
            data_query = data_query.limit(page_size)
        if offset is not None:
            data_query = data_query.offset(offset)
        return data_query

    def count(self, query: GetConnectionListQuery) -> Query:
        return self.__specified_query(query=query).count()
