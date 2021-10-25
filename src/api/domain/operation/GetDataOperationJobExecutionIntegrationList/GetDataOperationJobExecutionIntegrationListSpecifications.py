from injector import inject
from sqlalchemy import func
from sqlalchemy.orm import Query

from domain.common.specifications.OrderBySpecification import OrderBySpecification
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from domain.operation.GetDataOperationJobExecutionIntegrationList.GetDataOperationJobExecutionIntegrationListQuery import \
    GetDataOperationJobExecutionIntegrationListQuery
from models.dao.common import Status
from models.dao.connection import Connection
from models.dao.integration import DataIntegrationConnection, DataIntegration
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

        source_connection_query = self.repository_provider.query(
            DataIntegrationConnection,
            DataIntegrationConnection.DataIntegrationId,
            Connection.Name.label(
                "ConnectionName")
        ) \
            .join(Connection, DataIntegrationConnection.ConnectionId == Connection.Id) \
            .filter(DataIntegrationConnection.IsDeleted == 0) \
            .filter(DataIntegrationConnection.SourceOrTarget == 0)
        source_connection_subquery = source_connection_query.subquery()

        target_connection_query = self.repository_provider.query(
            DataIntegrationConnection,
            DataIntegrationConnection.DataIntegrationId,
            Connection.Name.label(
                "ConnectionName")
        ) \
            .join(Connection, DataIntegrationConnection.ConnectionId == Connection.Id) \
            .filter(DataIntegrationConnection.IsDeleted == 0) \
            .filter(DataIntegrationConnection.SourceOrTarget == 1)
        target_connection_subquery = target_connection_query.subquery()
        specified_query = self.repository_provider.query(
            DataOperationJobExecutionIntegration,
            DataOperationIntegration,
            source_connection_subquery.c.ConnectionName.label("SourceConnectionName"),
            target_connection_subquery.c.ConnectionName.label("TargetConnectionName"),
            total_affected_row_subquery.c.AffectedRowCount.label("AffectedRowCount")
        ) \
            .join(DataOperationIntegration, isouter=True) \
            .join(DataIntegration, isouter=True) \
            .join(Status, isouter=True) \
            .join(source_connection_subquery,
                  source_connection_subquery.c.DataIntegrationId == DataIntegration.Id, isouter=True) \
            .join(target_connection_subquery,
                  target_connection_subquery.c.DataIntegrationId == DataIntegration.Id, isouter=True) \
            .join(total_affected_row_subquery,
                  total_affected_row_subquery.c.Id == DataOperationJobExecutionIntegration.Id, isouter=True)

        specified_query = specified_query.filter(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId == query.request.ExecutionId) \
            .order_by(DataOperationIntegration.Order)

        return specified_query

    def specify(self, query: GetDataOperationJobExecutionIntegrationListQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query


def count(self, query: GetDataOperationJobExecutionIntegrationListQuery) -> Query:
    return self.__specified_query(query=query).count()
