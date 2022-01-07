from pdip.cqrs.decorators import responseclass

from pdi.application.connection.GetConnectionSql.GetConnectionSqlDto import GetConnectionSqlDto


@responseclass
class GetConnectionSqlResponse:
    Data: GetConnectionSqlDto = None
