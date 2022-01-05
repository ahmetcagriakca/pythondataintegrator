from injector import inject
from pdip.api.specifications import OrderBySpecification
from pdip.api.specifications import PagingSpecification
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import func
from sqlalchemy.orm import Query

from pdi.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListQuery import \
    GetDataOperationJobExecutionListQuery
from pdi.domain.common import Status
from pdi.domain.operation import DataOperationJob, DataOperation, DataOperationJobExecutionIntegration, \
    DataOperationJobExecution, DataOperationJobExecutionIntegrationEvent


class GetDataOperationJobExecutionListSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.repository_provider = repository_provider
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def __specified_query(self, query: GetDataOperationJobExecutionListQuery, data_query: Query) -> Query:

        max_integration_query = self.repository_provider.query(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId,
            func.max(DataOperationJobExecutionIntegration.Id).label('DataOperationJobExecutionIntegrationId')).group_by(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId)
        max_integration_subquery = max_integration_query.subquery()

        total_source_data_count_query = self.repository_provider.query(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId,
            func.coalesce(func.sum(DataOperationJobExecutionIntegration.SourceDataCount), 0).label(
                "SourceDataCount")).group_by(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId)
        total_source_data_count_subquery = total_source_data_count_query.subquery()

        total_affected_row_query = self.repository_provider.query(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId,
            func.coalesce(func.sum(DataOperationJobExecutionIntegrationEvent.AffectedRowCount), 0).label(
                "AffectedRowCount")) \
            .join(DataOperationJobExecutionIntegration.DataOperationJobExecutionIntegrationEvents).group_by(
            DataOperationJobExecutionIntegration.DataOperationJobExecutionId)
        total_affected_row_subquery = total_affected_row_query.subquery()

        specified_query = self.repository_provider.query(
            DataOperationJobExecution,
            DataOperationJob,
            DataOperation,
            Status,
            DataOperationJobExecutionIntegration.Log,
            total_source_data_count_subquery.c.SourceDataCount.label("SourceDataCount"),
            total_affected_row_subquery.c.AffectedRowCount.label("AffectedRowCount")
        ) \
            .join(DataOperationJob, DataOperationJob.Id == DataOperationJobExecution.DataOperationJobId) \
            .join(DataOperation, DataOperation.Id == DataOperationJob.DataOperationId) \
            .join(Status, Status.Id == DataOperationJobExecution.StatusId) \
            .join(max_integration_subquery,
                  max_integration_subquery.c.DataOperationJobExecutionId == DataOperationJobExecution.Id, isouter=True) \
            .join(DataOperationJobExecutionIntegration,
                  max_integration_subquery.c.DataOperationJobExecutionIntegrationId == DataOperationJobExecutionIntegration.Id,
                  isouter=True) \
            .join(total_source_data_count_subquery,
                  total_source_data_count_subquery.c.DataOperationJobExecutionId == DataOperationJobExecution.Id,
                  isouter=True) \
            .join(total_affected_row_subquery,
                  total_affected_row_subquery.c.DataOperationJobExecutionId == DataOperationJobExecution.Id,
                  isouter=True)

        if query.request.DataOperationId is not None and query.request.DataOperationId != '':
            specified_query = specified_query.filter(DataOperation.Id == query.request.DataOperationId)

        if query.request.DataOperationJobId is not None and query.request.DataOperationJobId != '':
            specified_query = specified_query.filter(DataOperationJob.Id == query.request.DataOperationJobId)

        if query.request.DataOperationName is not None and query.request.DataOperationName != '':
            specified_query = specified_query.filter(DataOperation.Name == query.request.DataOperationName)

        if query.request.OnlyCron is not None and query.request.OnlyCron:
            specified_query = specified_query.filter(DataOperationJob.Cron != None)

        if query.request.StatusId is not None:
            specified_query = specified_query.filter(DataOperationJobExecution.StatusId == query.request.StatusId)

        return specified_query

    def specify(self, data_query: Query, query: GetDataOperationJobExecutionListQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)

        order_by = self.order_by_specification.specify(order_by_parameter=query.request)
        if order_by is not None:
            data_query = data_query.order_by(order_by)

        page_size, offset = self.paging_specification.specify(paging_parameter=query.request)
        if page_size is not None:
            data_query = data_query.limit(page_size)
        if offset is not None:
            data_query = data_query.offset(offset)
        return data_query

    def count(self, query: GetDataOperationJobExecutionListQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
