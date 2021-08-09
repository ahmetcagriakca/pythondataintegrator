from injector import inject
from sqlalchemy import distinct, func
from sqlalchemy.orm import Query
from infrastructure.dependency.scopes import IScoped
from infrastructure.data.RepositoryProvider import RepositoryProvider
from models.dao.operation import DataOperationJobExecutionIntegrationEvent
from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration
from domain.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetQuery import \
    GetSourceDataAffectedRowWidgetQuery


class GetSourceDataAffectedRowWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetSourceDataAffectedRowWidgetQuery) -> (Query, Query):
        source_data_count_query = self.repository_provider.query(
            func.sum(DataOperationJobExecutionIntegration.SourceDataCount).label("Count"),
        )

        affected_row_query = self.repository_provider.query(
            func.sum(DataOperationJobExecutionIntegrationEvent.AffectedRowCount).label("Count"),
        )
        return (source_data_count_query, affected_row_query)

    def specify(self, query: GetSourceDataAffectedRowWidgetQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query
