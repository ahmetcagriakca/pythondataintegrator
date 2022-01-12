from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import distinct, func
from sqlalchemy.orm import Query

from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetQuery import GetDataOperationWidgetQuery
from src.domain.operation import DataOperation


class GetDataOperationWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        pass

    def __specified_query(self, query: GetDataOperationWidgetQuery) -> Query:
        specified_query = self.repository_provider.query(
            func.count(distinct(DataOperation.Id)).label("Count"),
        )
        return specified_query

    def specify(self, query: GetDataOperationWidgetQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
