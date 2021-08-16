from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CheckDatabaseConnectionRequest:
    ConnectionName: str = None
