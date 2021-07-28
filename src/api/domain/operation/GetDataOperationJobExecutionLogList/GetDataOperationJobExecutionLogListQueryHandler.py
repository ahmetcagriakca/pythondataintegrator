from injector import inject
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListMapping import GetDataOperationJobExecutionLogListMapping
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListQuery import GetDataOperationJobExecutionLogListQuery
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListResponse import GetDataOperationJobExecutionLogListResponse
from domain.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListSpecifications import GetDataOperationJobExecutionLogListSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped


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
