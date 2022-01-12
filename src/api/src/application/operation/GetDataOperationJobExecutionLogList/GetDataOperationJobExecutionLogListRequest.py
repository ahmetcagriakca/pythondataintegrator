from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationJobExecutionLogListRequest:
    ExecutionId: int = None
