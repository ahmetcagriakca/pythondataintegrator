from injector import inject
from domain.operation.GetDataOperation.GetDataOperationMapping import GetDataOperationMapping
from domain.operation.GetDataOperation.GetDataOperationQuery import GetDataOperationQuery
from domain.operation.GetDataOperation.GetDataOperationResponse import GetDataOperationResponse
from domain.operation.GetDataOperation.GetDataOperationSpecifications import GetDataOperationSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation.DataOperation import DataOperation


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
