from injector import inject
from pdip.data import RepositoryProvider
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from domain.common.LookupStatus.LookupStatusMapping import LookupStatusMapping
from domain.common.LookupStatus.LookupStatusQuery import LookupStatusQuery
from domain.common.LookupStatus.LookupStatusResponse import LookupStatusResponse
from domain.common.LookupStatus.LookupStatusSpecifications import LookupStatusSpecifications
from models.dao.common.Status import Status


class LookupStatusQueryHandler(IQueryHandler[LookupStatusQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: LookupStatusSpecifications):
        self.specifications = specifications

    def handle(self, query: LookupStatusQuery) -> LookupStatusResponse:
        result = LookupStatusResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = LookupStatusMapping.to_dtos(data_query)
        return result
