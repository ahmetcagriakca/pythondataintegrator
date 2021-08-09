from infrastructure.cqrs.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobExecutionIntegrationListRequest:
    ExecutionId: int = None
