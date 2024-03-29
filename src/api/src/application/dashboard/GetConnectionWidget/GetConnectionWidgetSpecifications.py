from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import distinct, func
from sqlalchemy.orm import Query

from src.application.dashboard.GetConnectionWidget.GetConnectionWidgetQuery import GetConnectionWidgetQuery
from src.domain.connection.Connection import Connection


class GetConnectionWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetConnectionWidgetQuery) -> Query:
        specified_query = self.repository_provider.query(
            func.count(distinct(Connection.Name)).label("Count"),
        )
        return specified_query

    def specify(self, query: GetConnectionWidgetQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetConnectionWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
