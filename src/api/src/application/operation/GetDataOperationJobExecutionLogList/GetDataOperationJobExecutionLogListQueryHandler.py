from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListMapping import \
    GetDataOperationJobExecutionLogListMapping
from src.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListQuery import \
    GetDataOperationJobExecutionLogListQuery
from src.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListResponse import \
    GetDataOperationJobExecutionLogListResponse
from src.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListSpecifications import \
    GetDataOperationJobExecutionLogListSpecifications


class GetDataOperationJobExecutionLogListQueryHandler(IQueryHandler[GetDataOperationJobExecutionLogListQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: GetDataOperationJobExecutionLogListSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobExecutionLogListQuery) -> GetDataOperationJobExecutionLogListResponse:
        result = GetDataOperationJobExecutionLogListResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetDataOperationJobExecutionLogListMapping.to_dtos(data_query)
        return result
