from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.connection.GetConnection.GetConnectionMapping import GetConnectionMapping
from src.application.connection.GetConnection.GetConnectionQuery import GetConnectionQuery
from src.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse
from src.application.connection.GetConnection.GetConnectionSpecifications import GetConnectionSpecifications


class GetConnectionQueryHandler(IQueryHandler[GetConnectionQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetConnectionSpecifications):
        self.specifications = specifications

    def handle(self, query: GetConnectionQuery) -> GetConnectionResponse:
        result = GetConnectionResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetConnectionMapping.to_dto(data_query.first())
        return result
