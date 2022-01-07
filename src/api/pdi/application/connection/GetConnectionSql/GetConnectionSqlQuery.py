from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.GetConnectionSql.GetConnectionSqlRequest import GetConnectionSqlRequest
from pdi.application.connection.GetConnectionSql.GetConnectionSqlResponse import GetConnectionSqlResponse


@dataclass
class GetConnectionSqlQuery(IQuery[GetConnectionSqlResponse]):
    request: GetConnectionSqlRequest = None
