from pdip.cqrs.decorators import requestclass


@requestclass
class CheckSqlConnectionRequest:
    ConnectionName: str = None
