from pdip.cqrs.decorators import requestclass


@requestclass
class GetDataOperationJobExecutionIntegrationListRequest:
    ExecutionId: int = None
