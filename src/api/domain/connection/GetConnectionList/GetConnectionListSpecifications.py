from injector import inject
from sqlalchemy.orm import Query

from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.common.specifications.OrderBySpecification import OrderBySpecification
from domain.common.specifications.PagingSpecification import PagingSpecification
from models.dao.connection import Connection, ConnectionServer, ConnectionDatabase, ConnectionType, ConnectorType


class GetConnectionListSpecifications:
    @inject
    def __init__(self,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def __specified_query(self, query: GetConnectionListQuery, data_query: Query) -> Query:
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
        return specified_query

    def specify(self, data_query: Query, query: GetConnectionListQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        order_by = self.order_by_specification.specify(order_by_parameter=query.request)
        if order_by is not None:
            data_query = data_query.order_by(order_by)

        page_size, offset = self.paging_specification.specify(paging_parameter=query.request)
        if page_size is not None:
            data_query = data_query.limit(page_size)
        if offset is not None:
            data_query = data_query.offset(offset)
        return data_query

    def count(self, query: GetConnectionListQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
