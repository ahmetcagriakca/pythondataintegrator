from injector import inject
from domain.operation.LookupDataOperation.LookupDataOperationMapping import LookupDataOperationMapping
from domain.operation.LookupDataOperation.LookupDataOperationQuery import LookupDataOperationQuery
from domain.operation.LookupDataOperation.LookupDataOperationResponse import LookupDataOperationResponse
from domain.operation.LookupDataOperation.LookupDataOperationSpecifications import LookupDataOperationSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation.DataOperation import DataOperation


class LookupDataOperationQueryHandler(IQueryHandler[LookupDataOperationQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: LookupDataOperationSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: LookupDataOperationQuery) -> LookupDataOperationResponse:
        result = LookupDataOperationResponse()
        repository = self.repository_provider.get(DataOperation)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupDataOperationMapping.to_dtos(data_query)
        return result
