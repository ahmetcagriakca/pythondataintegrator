from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataMapping import GetConnectionBigDataMapping
from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataQuery import GetConnectionBigDataQuery
from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataResponse import GetConnectionBigDataResponse
from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataSpecifications import GetConnectionBigDataSpecifications


class GetConnectionBigDataQueryHandler(IQueryHandler[GetConnectionBigDataQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetConnectionBigDataSpecifications):
        self.specifications = specifications

    def handle(self, query: GetConnectionBigDataQuery) -> GetConnectionBigDataResponse:
        result = GetConnectionBigDataResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetConnectionBigDataMapping.to_dto(data_query.first())
        return result
