from domain.common.decorators.requestclass import requestclass


@requestclass
class GetConnectionRequest:
    Id: int = None
