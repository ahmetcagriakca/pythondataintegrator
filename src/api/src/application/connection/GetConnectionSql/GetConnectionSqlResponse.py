from pdip.cqrs.decorators import responseclass

from src.application.connection.GetConnectionSql.GetConnectionSqlDto import GetConnectionSqlDto


@responseclass
class GetConnectionSqlResponse:
    Data: GetConnectionSqlDto = None
