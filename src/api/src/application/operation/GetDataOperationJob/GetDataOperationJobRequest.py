from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationJobRequest:
    Id: int = None
