from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class GetConnectionRequest:
    Id: int = None
