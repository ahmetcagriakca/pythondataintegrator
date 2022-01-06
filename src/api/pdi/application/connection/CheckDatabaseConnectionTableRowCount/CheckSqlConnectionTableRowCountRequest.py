from pdip.cqrs.decorators import requestclass


@requestclass
class CheckSqlConnectionTableRowCountRequest:
    ConnectionName: str = None
    Schema: str = None
    Table: str = None
