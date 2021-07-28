from injector import inject
from sqlalchemy import func
from sqlalchemy.orm import Query

from domain.common.specifications.OrderBySpecification import OrderBySpecification
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListQuery import \
    GetDataOperationJobExecutionIntegrationListQuery
from models.dao.operation import DataOperationIntegration, DataOperationJobExecutionIntegration, \
    DataOperationJobExecutionIntegrationEvent


class GetDataOperationJobExecutionIntegrationListSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetDataOperationJobExecutionIntegrationListQuery) -> Query:
        total_affected_row_query = self.repository_provider.query(
            DataOperationJobExecutionIntegration.Id,
            func.coalesce(func.sum(DataOperationJobExecutionIntegrationEvent.AffectedRowCount), 0).label(
                "AffectedRowCount")) \
            .join(DataOperationJobExecutionIntegration.DataOperationJobExecutionIntegrationEvents).group_by(
            DataOperationJobExecutionIntegration.Id)
        total_affected_row_subquery = total_affected_row_query.subquery()

        specified_query = self.repository_provider.query(
            DataOperationJobExecutionIntegration,
            DataOperationIntegration,
            total_affected_row_subquery.c.AffectedRowCount.label("AffectedRowCount")
        ) \
            .join(DataOperationIntegration) \
            .join(total_affected_row_subquery,
                  total_affected_row_subquery.c.Id == DataOperationJobExecutionIntegration.Id)

        specified_query = specified_query.filter(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId == query.request.ExecutionId) \
            .order_by(DataOperationIntegration.Order)

        return specified_query

    def specify(self, query: GetDataOperationJobExecutionIntegrationListQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationJobExecutionIntegrationListQuery) -> Query:
        return self.__specified_query(query=query).count()
