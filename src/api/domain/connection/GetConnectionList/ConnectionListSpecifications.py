from injector import inject
from sqlalchemy.orm import Query

from domain.connection.GetConnectionList.ConnectionListQuery import ConnectionListQuery
from domain.common.specifications.OrderBySpecification import OrderBySpecification
from domain.common.specifications.PagingSpecification import PagingSpecification
from models.dao.connection import Connection, ConnectionServer, ConnectionDatabase, ConnectionType, ConnectorType


class ConnectionListSpecifications:
    @inject
    def __init__(self,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def specify(self, data_query: Query, query: ConnectionListQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        order_by = self.order_by_specification.specify(order_by_parameter=query.ConnectionListRequest)
        if order_by is not None:
            data_query = data_query.order_by(order_by)

        page_size, offset = self.paging_specification.specify(paging_parameter=query.ConnectionListRequest)
        if page_size is not None:
            data_query = data_query.limit(page_size)
        if offset is not None:
            data_query = data_query.offset(offset)
        return data_query

    def __specified_query(self, query: ConnectionListQuery, data_query: Query) -> Query:
        specified_query = data_query \
            .join(ConnectionType, ConnectionType.Id == Connection.ConnectionTypeId) \
            .join(ConnectionServer, ConnectionServer.ConnectionId == Connection.Id) \
            .join(ConnectionDatabase, ConnectionDatabase.ConnectionId == Connection.Id) \
            .join(ConnectorType, ConnectorType.Id == ConnectionDatabase.ConnectorTypeId)
        if query.ConnectionListRequest.Id is not None:
            specified_query = specified_query.filter(Connection.Id == query.ConnectionListRequest.Id)
        if query.ConnectionListRequest.ConnectionTypeId is not None:
            specified_query = specified_query.filter(ConnectionType.Id == query.ConnectionListRequest.ConnectionTypeId)
        if query.ConnectionListRequest.ConnectorTypeId is not None:
            specified_query = specified_query.filter(ConnectorType.Id == query.ConnectionListRequest.ConnectorTypeId)
        return specified_query

    def count(self, query: ConnectionListQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
