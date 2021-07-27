from domain.common.decorators.requestclass import requestclass


@requestclass
class GetDataOperationJobRequest:
    Id: int = None
