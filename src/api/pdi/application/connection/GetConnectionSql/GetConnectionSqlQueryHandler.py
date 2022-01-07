from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from pdi.application.connection.GetConnectionSql.GetConnectionSqlMapping import GetConnectionSqlMapping
from pdi.application.connection.GetConnectionSql.GetConnectionSqlQuery import GetConnectionSqlQuery
from pdi.application.connection.GetConnectionSql.GetConnectionSqlResponse import GetConnectionSqlResponse
from pdi.application.connection.GetConnectionSql.GetConnectionSqlSpecifications import GetConnectionSqlSpecifications


class GetConnectionSqlQueryHandler(IQueryHandler[GetConnectionSqlQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetConnectionSqlSpecifications):
        self.specifications = specifications

    def handle(self, query: GetConnectionSqlQuery) -> GetConnectionSqlResponse:
        result = GetConnectionSqlResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetConnectionSqlMapping.to_dto(data_query.first())
        return result
