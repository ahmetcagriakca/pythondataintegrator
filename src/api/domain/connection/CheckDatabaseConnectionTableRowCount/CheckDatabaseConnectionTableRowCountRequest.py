from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class CheckDatabaseConnectionTableRowCountRequest:
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
