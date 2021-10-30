from pdip.cqrs.decorators import requestclass


@requestclass
class CheckDatabaseConnectionTableRowCountRequest:
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
