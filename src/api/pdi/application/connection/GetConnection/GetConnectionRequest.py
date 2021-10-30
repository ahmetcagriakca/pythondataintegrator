from pdip.cqrs.decorators import requestclass


@requestclass
class GetConnectionRequest:
    Id: int = None
