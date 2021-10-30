from injector import inject
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import func
from sqlalchemy.orm import Query

from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetQuery import \
    GetMonthlyExecutionsWidgetQuery
from pdi.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class GetMonthlyExecutionsWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetMonthlyExecutionsWidgetQuery) -> (Query, Query):
        count_query = self.repository_provider.query(
            func.count(DataOperationJobExecution.Id).label("Count"),
        )
        minimum_maximum_query = self.repository_provider.query(
            func.min(DataOperationJobExecution.StartDate).label("MinimumStartDate"),
            func.max(DataOperationJobExecution.StartDate).label("MaximumStartDate"),
        )
        return (count_query, minimum_maximum_query)

    def specify(self, query: GetMonthlyExecutionsWidgetQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetMonthlyExecutionsWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
