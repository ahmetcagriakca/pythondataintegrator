from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationJobExecutionRequest:
    Id: int = None
