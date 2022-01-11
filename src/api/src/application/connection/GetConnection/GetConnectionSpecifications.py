from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy.orm import Query

from src.application.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from src.domain.connection import ConnectionType, Connection


class GetConnectionSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetConnectionQuery) -> Query:
        repository = self.repository_provider.get(Connection)
        data_query = repository.table
        specified_query = data_query \
            .join(ConnectionType, ConnectionType.Id == Connection.ConnectionTypeId)
        specified_query = specified_query.filter(Connection.Id == query.request.Id)
        return specified_query

    def specify(self, query: GetConnectionQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetConnectionQuery) -> Query:
        return self.__specified_query(query=query).count()
