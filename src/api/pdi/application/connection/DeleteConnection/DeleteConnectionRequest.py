from pdip.cqrs.decorators import requestclass


@requestclass
class DeleteConnectionRequest:
    Id: int = None
