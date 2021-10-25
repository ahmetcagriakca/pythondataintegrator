from injector import inject
from sqlalchemy.orm import Query
from pdip.dependency import IScoped
from domain.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from models.dao.connection import ConnectionDatabase, ConnectionType, ConnectorType, Connection, ConnectionServer


class GetConnectionSpecifications(IScoped):
    @inject
    def __init__(self,
                 ):
        pass

    def __specified_query(self, query: GetConnectionQuery, data_query: Query) -> Query:
        specified_query = data_query \
            .join(ConnectionType, ConnectionType.Id == Connection.ConnectionTypeId) \
            .join(ConnectionServer, ConnectionServer.ConnectionId == Connection.Id) \
            .join(ConnectionDatabase, ConnectionDatabase.ConnectionId == Connection.Id) \
            .join(ConnectorType, ConnectorType.Id == ConnectionDatabase.ConnectorTypeId)
        specified_query = specified_query.filter(Connection.Id == query.request.Id)
        return specified_query

    def specify(self, data_query: Query, query: GetConnectionQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        return data_query

    def count(self, query: GetConnectionQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
