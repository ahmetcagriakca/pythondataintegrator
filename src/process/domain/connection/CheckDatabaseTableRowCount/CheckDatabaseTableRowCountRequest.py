from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CheckDatabaseTableRowCountRequest:
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
