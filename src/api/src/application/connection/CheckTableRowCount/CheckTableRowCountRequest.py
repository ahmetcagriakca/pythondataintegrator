from pdip.cqrs.decorators import requestclass


@requestclass
class CheckTableRowCountRequest:
    ConnectionId: int = None
    Schema: str = None
    Table: str = None
