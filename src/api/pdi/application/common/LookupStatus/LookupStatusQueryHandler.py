from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.common.LookupStatus.LookupStatusMapping import LookupStatusMapping
from pdi.application.common.LookupStatus.LookupStatusQuery import LookupStatusQuery
from pdi.application.common.LookupStatus.LookupStatusResponse import LookupStatusResponse
from pdi.application.common.LookupStatus.LookupStatusSpecifications import LookupStatusSpecifications


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
