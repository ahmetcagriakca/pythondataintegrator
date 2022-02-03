from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import distinct, func, text
from sqlalchemy.orm import Query

from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetQuery import \
    GetExecutionStatusesWidgetQuery
from src.domain.operation import DataOperationJobExecution, DataOperation, DataOperationJob


class GetExecutionStatusesWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetExecutionStatusesWidgetQuery) -> Query:
        specified_query = self.repository_provider.query(
            func.count(distinct(DataOperationJobExecution.Id)).label("Count"),
        )

        most_data_operations_query = self.repository_provider.query(
            DataOperation.Name, DataOperationJobExecution.StatusId,
            func.count(distinct(DataOperationJobExecution.Id)).label("Count"),
        ).join(DataOperationJob, DataOperationJobExecution.DataOperationJob).join(DataOperation,
                                                                                  DataOperationJob.DataOperation) \
            .group_by(DataOperation.Name, DataOperationJobExecution.StatusId) \
            .order_by(text('"Count" DESC'))
        return (specified_query, most_data_operations_query)

    def specify(self, query: GetExecutionStatusesWidgetQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetExecutionStatusesWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
