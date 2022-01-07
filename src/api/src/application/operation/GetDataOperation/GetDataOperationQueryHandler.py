from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.operation.GetDataOperation.GetDataOperationMapping import GetDataOperationMapping
from src.application.operation.GetDataOperation.GetDataOperationQuery import GetDataOperationQuery
from src.application.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse
from src.application.operation.GetDataOperation.GetDataOperationSpecifications import GetDataOperationSpecifications
from src.domain.operation.DataOperation import DataOperation


class GetDataOperationQueryHandler(IQueryHandler[GetDataOperationQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: GetDataOperationSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: GetDataOperationQuery) -> GetDataOperationResponse:
        result = GetDataOperationResponse()
        repository = self.repository_provider.get(DataOperation)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = GetDataOperationMapping.to_dto(data_query.first())
        return result
