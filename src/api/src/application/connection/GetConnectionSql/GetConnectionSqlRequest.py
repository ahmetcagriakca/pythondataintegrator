from pdip.cqrs.decorators import requestclass


@requestclass
class GetConnectionSqlRequest:
    Id: int = None
