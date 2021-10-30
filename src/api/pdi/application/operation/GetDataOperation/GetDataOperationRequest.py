from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationRequest:
    Id: int = None
