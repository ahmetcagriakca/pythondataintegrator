from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.GetConnectionSql.GetConnectionSqlRequest import GetConnectionSqlRequest
from src.application.connection.GetConnectionSql.GetConnectionSqlResponse import GetConnectionSqlResponse


@dataclass
class GetConnectionSqlQuery(IQuery[GetConnectionSqlResponse]):
    request: GetConnectionSqlRequest = None
