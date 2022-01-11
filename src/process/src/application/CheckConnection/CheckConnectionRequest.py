from pdip.cqrs.decorators import requestclass


@requestclass
class CheckConnectionRequest:
    ConnectionId: int = None
