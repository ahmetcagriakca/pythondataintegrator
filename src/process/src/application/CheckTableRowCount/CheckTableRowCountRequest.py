from pdip.cqrs.decorators import requestclass


@requestclass
class CheckTableRowCountRequest:
    ConnectionId: str = None
    Schema: str = None
    Table: str = None
