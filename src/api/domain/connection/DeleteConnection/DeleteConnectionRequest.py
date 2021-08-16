from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class DeleteConnectionRequest:
    Id: int = None
