from domain.common.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobExecutionIntegrationListRequest:
    ExecutionId: int = None
