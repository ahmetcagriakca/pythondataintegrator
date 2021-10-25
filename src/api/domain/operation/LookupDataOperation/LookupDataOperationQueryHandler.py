from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped

from domain.operation.LookupDataOperation.LookupDataOperationMapping import LookupDataOperationMapping
from domain.operation.LookupDataOperation.LookupDataOperationQuery import LookupDataOperationQuery
from domain.operation.LookupDataOperation.LookupDataOperationResponse import LookupDataOperationResponse
from domain.operation.LookupDataOperation.LookupDataOperationSpecifications import LookupDataOperationSpecifications
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
        data_query = repository.table.filter(DataOperation.IsDeleted==0)
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupDataOperationMapping.to_dtos(data_query)
        return result
