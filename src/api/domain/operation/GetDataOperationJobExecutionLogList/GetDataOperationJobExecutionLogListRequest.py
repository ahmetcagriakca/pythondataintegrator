from domain.common.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobExecutionLogListRequest:
    ExecutionId: int = None
