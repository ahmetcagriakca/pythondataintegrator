from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobRequest:
    Id: int = None
