from injector import inject
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionMapping import GetDataOperationJobExecutionMapping
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionQuery import GetDataOperationJobExecutionQuery
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionResponse import GetDataOperationJobExecutionResponse
from domain.operation.GetDataOperationJobExecution.GetDataOperationJobExecutionSpecifications import GetDataOperationJobExecutionSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


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
