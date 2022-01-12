from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import distinct, func
from sqlalchemy.orm import Query

from src.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import \
    GetDataOperationJobWidgetQuery
from src.domain.operation.DataOperationJob import DataOperationJob


class GetDataOperationJobWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetDataOperationJobWidgetQuery) -> Query:
        specified_query = self.repository_provider.query(
            func.count(distinct(DataOperationJob.Id)).label("Count"),
        )
        return specified_query

    def specify(self, query: GetDataOperationJobWidgetQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationJobWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
