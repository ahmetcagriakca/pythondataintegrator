from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class GetDataOperationRequest:
    Id: int = None
