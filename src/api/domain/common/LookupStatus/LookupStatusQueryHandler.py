from injector import inject
from domain.common.LookupStatus.LookupStatusMapping import LookupStatusMapping
from domain.common.LookupStatus.LookupStatusQuery import LookupStatusQuery
from domain.common.LookupStatus.LookupStatusResponse import LookupStatusResponse
from domain.common.LookupStatus.LookupStatusSpecifications import LookupStatusSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.common.Status import Status


class LookupStatusQueryHandler(IQueryHandler[LookupStatusQuery], IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 specifications: LookupStatusSpecifications):
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: LookupStatusQuery) -> LookupStatusResponse:
        result = LookupStatusResponse()
        repository = self.repository_provider.get(Status)
        data_query = repository.table
        data_query = self.specifications.specify(query=query, data_query=data_query)
        result.Data = LookupStatusMapping.to_dtos(data_query)
        return result
