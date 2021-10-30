from pdip.cqrs.decorators import requestclass


@requestclass
class CheckDatabaseConnectionRequest:
    ConnectionName: str = None
