from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListMapping import \
    GetDataOperationJobExecutionListMapping
from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListQuery import \
    GetDataOperationJobExecutionListQuery
from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListResponse import \
    GetDataOperationJobExecutionListResponse
from src.application.operation.GetDataOperationJobExecutionList.GetDataOperationJobExecutionListSpecifications import \
    GetDataOperationJobExecutionListSpecifications
from src.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class GetDataOperationJobExecutionListQueryHandler(IQueryHandler[GetDataOperationJobExecutionListQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: GetDataOperationJobExecutionListSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobExecutionListQuery) -> GetDataOperationJobExecutionListResponse:
        result = GetDataOperationJobExecutionListResponse()
        repository = self.repository_provider.get(DataOperationJobExecution)
        data_query = repository.table

        result.Count = self.specifications.count(query=query, data_query=data_query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = GetDataOperationJobExecutionListMapping.to_dtos(data_query)
        return result
