from pdip.cqrs.decorators import requestclass


@requestclass
class CheckDatabaseTableRowCountRequest:
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
