from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.connection.GetConnectionList.GetConnectionListMapping import GetConnectionListMapping
from pdi.application.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from pdi.application.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from pdi.application.connection.GetConnectionList.GetConnectionListSpecifications import GetConnectionListSpecifications


class GetConnectionListQueryHandler(IQueryHandler[GetConnectionListQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetConnectionListSpecifications):
        self.specifications = specifications

    def handle(self, query: GetConnectionListQuery) -> GetConnectionListResponse:
        result = GetConnectionListResponse()

        result.Count = self.specifications.count(query=query)

        result.PageNumber = query.request.PageNumber
        result.PageSize = query.request.PageSize

        data_query = self.specifications.specify(query=query)

        result.Data = GetConnectionListMapping.to_dtos(data_query)
        return result
