from domain.common.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobExecutionRequest:
    Id: int = None
