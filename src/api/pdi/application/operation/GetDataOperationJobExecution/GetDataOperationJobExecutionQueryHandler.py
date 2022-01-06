from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionMapping import \
    GetDataOperationJobExecutionMapping
from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionQuery import \
    GetDataOperationJobExecutionQuery
from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import \
    GetDataOperationJobExecutionResponse
from pdi.application.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionSpecifications import \
    GetDataOperationJobExecutionSpecifications
from pdi.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class GetDataOperationJobExecutionQueryHandler(IQueryHandler[GetDataOperationJobExecutionQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: GetDataOperationJobExecutionSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: GetDataOperationJobExecutionQuery) -> GetDataOperationJobExecutionResponse:
        result = GetDataOperationJobExecutionResponse()
        repository = self.repository_provider.get(DataOperationJobExecution)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = GetDataOperationJobExecutionMapping.to_dto(data_query.first())
        return result
