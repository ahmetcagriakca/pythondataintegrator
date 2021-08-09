from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobExecutionLogListRequest:
    ExecutionId: int = None
