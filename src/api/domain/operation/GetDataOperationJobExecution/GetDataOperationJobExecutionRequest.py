from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobExecutionRequest:
    Id: int = None
