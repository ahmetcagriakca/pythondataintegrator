from injector import inject
from domain.connection.GetConnectionList.GetConnectionListMapping import GetConnectionListMapping
from domain.connection.GetConnectionList.GetConnectionListQuery import GetConnectionListQuery
from domain.connection.GetConnectionList.GetConnectionListResponse import GetConnectionListResponse
from domain.connection.GetConnectionList.GetConnectionListSpecifications import GetConnectionListSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.dependency.scopes import IScoped


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