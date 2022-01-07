from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import or_
from sqlalchemy.orm import Query

from pdi.application.connection.GetConnectionSql.GetConnectionSqlQuery import GetConnectionSqlQuery
from pdi.domain.connection import ConnectionDatabase, ConnectionType, ConnectorType, Connection, ConnectionServer


class GetConnectionSqlSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetConnectionSqlQuery) -> Query:
        repository = self.repository_provider.get(Connection)
        data_query = repository.table
        specified_query = data_query \
            .join(ConnectionType, ConnectionType.Id == Connection.ConnectionTypeId) \
            .join(ConnectionServer, ConnectionServer.ConnectionId == Connection.Id) \
            .join(ConnectionDatabase, ConnectionDatabase.ConnectionId == Connection.Id) \
            .join(ConnectorType, or_(ConnectorType.Id == ConnectionDatabase.ConnectorTypeId))
        specified_query = specified_query.filter(Connection.Id == query.request.Id)
        return specified_query

    def specify(self, query: GetConnectionSqlQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetConnectionSqlQuery) -> Query:
        return self.__specified_query(query=query).count()
